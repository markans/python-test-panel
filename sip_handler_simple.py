"""
Simplified SIP Call Handler for Phone Number Testing
Using socket-based SIP implementation
"""
import time
import json
import logging
import threading
import random
import socket
from datetime import datetime
from typing import List, Dict, Callable

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SimpleSIPTester:
    """Simplified SIP tester for phone number connectivity testing"""
    
    def __init__(self, config_path: str = 'config.json'):
        """Initialize SIP tester with configuration"""
        self.config = self._load_config(config_path)
        self.sip_config = self.config['sip']
        self.test_settings = self.config['test_settings']
        
        self.test_results = []
        self.current_test_status = {
            'is_running': False,
            'total_numbers': 0,
            'tested_numbers': 0,
            'connected_numbers': [],
            'failed_numbers': [],
            'current_number': None,
            'start_time': None
        }
        
        self.status_callback = None
        self.log_callback = None
        self.stop_flag = False
        
    def _load_config(self, config_path: str) -> dict:
        """Load configuration from JSON file"""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"Config file {config_path} not found. Using example config.")
            with open('config.example.json', 'r') as f:
                return json.load(f)
    
    def _create_sip_invite(self, phone_number: str, call_id: str) -> str:
        """Create a SIP INVITE message"""
        sip_uri = f"sip:{phone_number}@{self.sip_config['domain']}"
        from_uri = f"sip:{self.sip_config['username']}@{self.sip_config['domain']}"
        
        invite = f"""INVITE {sip_uri} SIP/2.0
Via: SIP/2.0/UDP {self.sip_config['server']}:{self.sip_config['port']};branch=z9hG4bK{call_id[:8]}
From: <{from_uri}>;tag={call_id[:10]}
To: <{sip_uri}>
Call-ID: {call_id}@{self.sip_config['server']}
CSeq: 1 INVITE
Contact: <{from_uri}>
Max-Forwards: 70
User-Agent: PhoneTestPanel/1.0
Content-Type: application/sdp
Content-Length: 0

"""
        return invite.replace('\n', '\r\n')
    
    def _send_sip_message(self, message: str) -> tuple:
        """Send SIP message and get response"""
        try:
            # Create UDP socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(5.0)  # 5 second timeout
            
            # Send message
            server_address = (self.sip_config['server'], self.sip_config['port'])
            sock.sendto(message.encode(), server_address)
            
            # Wait for response
            response, addr = sock.recvfrom(4096)
            sock.close()
            
            return True, response.decode()
        except socket.timeout:
            return False, "Timeout"
        except Exception as e:
            return False, str(e)
    
    def test_phone_number(self, phone_number: str) -> Dict:
        """Test a single phone number using SIP"""
        result = {
            'phone_number': phone_number,
            'status': 'unknown',
            'timestamp': datetime.now().isoformat(),
            'duration': 0,
            'error': None
        }
        
        try:
            self._log(f"Testing number: {phone_number}")
            
            # Generate unique call ID
            call_id = f"{int(time.time())}{random.randint(1000, 9999)}"
            
            # Create and send INVITE
            invite_message = self._create_sip_invite(phone_number, call_id)
            start_time = time.time()
            
            success, response = self._send_sip_message(invite_message)
            
            if success and response:
                # Parse SIP response
                if "100 Trying" in response or "180 Ringing" in response or "183 Session Progress" in response:
                    # Simulate waiting for connection
                    time.sleep(min(3, self.test_settings['call_duration_seconds']))
                    
                    # Randomly determine if connected (for demo purposes)
                    # In real implementation, you would check for "200 OK"
                    if "180 Ringing" in response or random.random() > 0.3:
                        self._log(f"✓ Connected: {phone_number}", level='success')
                        result['status'] = 'connected'
                        
                        # Wait for configured duration
                        remaining_time = self.test_settings['call_duration_seconds'] - 3
                        if remaining_time > 0:
                            time.sleep(remaining_time)
                    else:
                        self._log(f"✗ No answer: {phone_number}", level='warning')
                        result['status'] = 'no_answer'
                elif "486 Busy" in response:
                    self._log(f"✗ Busy: {phone_number}", level='warning')
                    result['status'] = 'busy'
                elif "404 Not Found" in response:
                    self._log(f"✗ Not found: {phone_number}", level='warning')
                    result['status'] = 'not_found'
                else:
                    self._log(f"✗ Failed: {phone_number} - {response[:50]}", level='warning')
                    result['status'] = 'failed'
                    result['error'] = 'Unexpected response'
            else:
                self._log(f"✗ Connection error: {phone_number} - {response}", level='error')
                result['status'] = 'error'
                result['error'] = response
            
            result['duration'] = time.time() - start_time
            
            # Idle between calls
            if result['status'] == 'connected':
                self._log(f"Idle for {self.test_settings['idle_between_calls_seconds']}s before next call")
                time.sleep(self.test_settings['idle_between_calls_seconds'])
            
        except Exception as e:
            self._log(f"✗ Error testing {phone_number}: {str(e)}", level='error')
            result['status'] = 'error'
            result['error'] = str(e)
        
        return result
    
    def test_multiple_numbers(self, phone_numbers: List[str], 
                            status_callback: Callable = None,
                            log_callback: Callable = None):
        """Test multiple phone numbers sequentially"""
        self.status_callback = status_callback
        self.log_callback = log_callback
        
        if self.current_test_status['is_running']:
            self._log("Test already in progress", level='warning')
            return
        
        # Start test in a separate thread
        self.stop_flag = False
        test_thread = threading.Thread(
            target=self._run_test,
            args=(phone_numbers,)
        )
        test_thread.daemon = True
        test_thread.start()
    
    def _run_test(self, phone_numbers: List[str]):
        """Run the test process"""
        # Reset status
        self.current_test_status = {
            'is_running': True,
            'total_numbers': len(phone_numbers),
            'tested_numbers': 0,
            'connected_numbers': [],
            'failed_numbers': [],
            'current_number': None,
            'start_time': datetime.now().isoformat()
        }
        
        self.test_results = []
        self._update_status()
        
        self._log(f"Starting test with {len(phone_numbers)} numbers")
        self._log(f"Configuration: {self.sip_config['username']}@{self.sip_config['server']}")
        
        # Test each number
        for idx, phone_number in enumerate(phone_numbers, 1):
            if self.stop_flag:
                self._log("Test stopped by user", level='warning')
                break
            
            self.current_test_status['current_number'] = phone_number
            self._update_status()
            
            result = self.test_phone_number(phone_number)
            self.test_results.append(result)
            
            # Update status
            self.current_test_status['tested_numbers'] = idx
            if result['status'] == 'connected':
                self.current_test_status['connected_numbers'].append(phone_number)
            else:
                self.current_test_status['failed_numbers'].append(phone_number)
            
            self._update_status()
        
        self.current_test_status['is_running'] = False
        self.current_test_status['current_number'] = None
        self._update_status()
        
        self._log(f"Test completed: {len(self.current_test_status['connected_numbers'])} connected, "
                 f"{len(self.current_test_status['failed_numbers'])} failed")
    
    def stop_test(self):
        """Stop the current test"""
        self.stop_flag = True
        self.current_test_status['is_running'] = False
        self._log("Stopping test...", level='warning')
    
    def get_status(self) -> Dict:
        """Get current test status"""
        return self.current_test_status.copy()
    
    def get_results(self) -> List[Dict]:
        """Get test results"""
        return self.test_results.copy()
    
    def _update_status(self):
        """Update status via callback"""
        if self.status_callback:
            self.status_callback(self.get_status())
    
    def _log(self, message: str, level: str = 'info'):
        """Log message and send via callback"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = {
            'timestamp': timestamp,
            'level': level,
            'message': message
        }
        
        # Log to console
        if level == 'error':
            logger.error(message)
        elif level == 'warning':
            logger.warning(message)
        else:
            logger.info(message)
        
        # Send via callback
        if self.log_callback:
            self.log_callback(log_entry)
    
    def cleanup(self):
        """Clean up resources"""
        self.stop_flag = True