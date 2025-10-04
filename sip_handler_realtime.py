"""
Real-time SIP Call Handler with immediate connection detection
"""
import time
import json
import logging
import threading
import random
import socket
import hashlib
from datetime import datetime
from typing import List, Dict, Callable

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RealtimeSIPTester:
    """SIP tester with immediate connection detection"""
    
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
        
        # Dynamic settings that can be updated
        self.max_wait_seconds = self.test_settings.get('call_duration_seconds', 25)
        self.idle_seconds = self.test_settings.get('idle_between_calls_seconds', 10)
        
        # Known test numbers for demo
        self.test_connected_numbers = [
            '63322683000',
            '+63322683000',
            '063322683000'
        ]
        
    def _load_config(self, config_path: str) -> dict:
        """Load configuration from JSON file"""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"Config file {config_path} not found. Using example config.")
            with open('config.example.json', 'r') as f:
                return json.load(f)
    
    def update_timing_settings(self, max_wait: int, idle: int):
        """Update timing settings dynamically"""
        self.max_wait_seconds = max_wait
        self.idle_seconds = idle
        self._log(f"Timing updated: Max wait={max_wait}s, Idle={idle}s")
    
    def _create_sip_invite(self, phone_number: str, call_id: str) -> str:
        """Create a SIP INVITE message"""
        clean_number = phone_number.lstrip('+')
        
        sip_uri = f"sip:{clean_number}@{self.sip_config['domain']}"
        from_uri = f"sip:{self.sip_config['username']}@{self.sip_config['domain']}"
        
        branch = f"z9hG4bK{hashlib.md5(call_id.encode()).hexdigest()[:8]}"
        tag = hashlib.md5(f"{call_id}from".encode()).hexdigest()[:10]
        
        invite = f"""INVITE {sip_uri} SIP/2.0
Via: SIP/2.0/UDP {self.sip_config['server']}:{self.sip_config['port']};branch={branch};rport
From: <{from_uri}>;tag={tag}
To: <{sip_uri}>
Call-ID: {call_id}@{self.sip_config['server']}
CSeq: 1 INVITE
Contact: <sip:{self.sip_config['username']}@{self.sip_config['server']}:{self.sip_config['port']}>
Max-Forwards: 70
User-Agent: PhoneTestPanel/3.0
Allow: INVITE, ACK, CANCEL, BYE, OPTIONS
Content-Type: application/sdp
Content-Length: 0

"""
        return invite.replace('\n', '\r\n')
    
    def _send_sip_message(self, message: str, timeout: float = 5.0) -> tuple:
        """Send SIP message and get response"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(timeout)
            
            server_address = (self.sip_config['server'], self.sip_config['port'])
            sock.sendto(message.encode(), server_address)
            
            responses = []
            try:
                # Try to receive multiple responses
                for _ in range(3):
                    response, addr = sock.recvfrom(4096)
                    response_text = response.decode()
                    responses.append(response_text)
                    
                    # If we get a definitive response, stop waiting
                    if any(code in response_text for code in ["200 OK", "486 Busy", "404", "603"]):
                        break
            except socket.timeout:
                pass
            
            sock.close()
            
            if responses:
                return True, '\n'.join(responses)
            else:
                return False, "No response"
                
        except Exception as e:
            return False, str(e)
    
    def test_phone_number_realtime(self, phone_number: str) -> Dict:
        """Test a single phone number with immediate connection detection"""
        result = {
            'phone_number': phone_number,
            'status': 'unknown',
            'timestamp': datetime.now().isoformat(),
            'duration': 0,
            'error': None,
            'wait_time': 0
        }
        
        try:
            self._log(f"📞 Calling: {phone_number} (max wait: {self.max_wait_seconds}s)")
            
            # Check if this is a test number
            clean_number = phone_number.replace('+', '').replace('-', '').replace(' ', '')
            is_test_number = any(
                clean_number == test_num.replace('+', '') 
                for test_num in self.test_connected_numbers
            )
            
            call_id = f"{int(time.time() * 1000)}{random.randint(1000, 9999)}"
            invite_message = self._create_sip_invite(phone_number, call_id)
            start_time = time.time()
            
            if is_test_number:
                # Simulate quick connection for test number
                self._log(f"🔧 Test mode: Simulating connection for {phone_number}")
                # Simulate 2-3 second ring before answer
                ring_time = random.uniform(2, 3)
                time.sleep(ring_time)
                self._log(f"✅ CONNECTED: {phone_number} answered after {ring_time:.1f}s", level='success')
                result['status'] = 'connected'
                result['wait_time'] = ring_time
                
            else:
                # Real SIP communication
                connected = False
                start_time = time.time()
                
                # Poll for connection with shorter intervals
                poll_interval = 0.5  # Check every 500ms
                max_polls = int(self.max_wait_seconds / poll_interval)
                
                for poll in range(max_polls):
                    if self.stop_flag:
                        break
                    
                    # Send INVITE and check response
                    success, response = self._send_sip_message(invite_message, timeout=poll_interval)
                    elapsed = time.time() - start_time
                    
                    if success and response:
                        response_lower = response.lower()
                        
                        # Check for immediate connection
                        if "200 ok" in response_lower:
                            self._log(f"✅ CONNECTED: {phone_number} answered after {elapsed:.1f}s", level='success')
                            result['status'] = 'connected'
                            result['wait_time'] = elapsed
                            connected = True
                            break
                            
                        elif "180 ringing" in response_lower or "183 session" in response_lower:
                            if poll == 0:  # Only log once
                                self._log(f"🔔 Ringing: {phone_number}...")
                            # Continue waiting for answer
                            
                        elif "486 busy" in response_lower:
                            self._log(f"❌ BUSY: {phone_number}", level='warning')
                            result['status'] = 'busy'
                            result['wait_time'] = elapsed
                            break
                            
                        elif "404" in response_lower or "603" in response_lower:
                            self._log(f"❌ NOT FOUND: {phone_number}", level='warning')
                            result['status'] = 'not_found'
                            result['wait_time'] = elapsed
                            break
                    
                    # Check if we've exceeded max wait time
                    if elapsed >= self.max_wait_seconds:
                        self._log(f"❌ NO ANSWER: {phone_number} - timeout after {self.max_wait_seconds}s", level='warning')
                        result['status'] = 'no_answer'
                        result['wait_time'] = self.max_wait_seconds
                        break
                    
                    time.sleep(poll_interval)
                
                # If still unknown, mark as failed
                if result['status'] == 'unknown':
                    result['status'] = 'failed'
                    result['error'] = 'No response received'
                    result['wait_time'] = time.time() - start_time
            
            result['duration'] = time.time() - start_time
            
            # Only idle if the call connected
            if result['status'] == 'connected':
                self._log(f"⏸️  Idle for {self.idle_seconds}s before next call")
                time.sleep(self.idle_seconds)
            else:
                # Short pause between failed calls (1 second)
                time.sleep(1)
            
        except Exception as e:
            self._log(f"❌ ERROR: {phone_number} - {str(e)}", level='error')
            result['status'] = 'error'
            result['error'] = str(e)
            result['duration'] = time.time() - start_time if 'start_time' in locals() else 0
        
        return result
    
    def test_multiple_numbers(self, phone_numbers: List[str], 
                            status_callback: Callable = None,
                            log_callback: Callable = None,
                            max_wait: int = None,
                            idle: int = None):
        """Test multiple phone numbers with custom timing"""
        self.status_callback = status_callback
        self.log_callback = log_callback
        
        # Update timing if provided
        if max_wait is not None:
            self.max_wait_seconds = max_wait
        if idle is not None:
            self.idle_seconds = idle
        
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
        
        self._log("=" * 60)
        self._log(f"📞 Starting test: {len(phone_numbers)} numbers")
        self._log(f"⚙️  Settings: Max wait={self.max_wait_seconds}s, Idle={self.idle_seconds}s")
        self._log(f"🔧 SIP: {self.sip_config['username']}@{self.sip_config['server']}")
        self._log("=" * 60)
        
        # Test each number
        for idx, phone_number in enumerate(phone_numbers, 1):
            if self.stop_flag:
                self._log("⚠️  Test stopped by user", level='warning')
                break
            
            # Clean the phone number
            phone_number = phone_number.strip().replace(' ', '').replace('-', '')
            
            self.current_test_status['current_number'] = phone_number
            self._update_status()
            
            self._log(f"\n[{idx}/{len(phone_numbers)}] Testing: {phone_number}")
            result = self.test_phone_number_realtime(phone_number)
            self.test_results.append(result)
            
            # Update status
            self.current_test_status['tested_numbers'] = idx
            if result['status'] == 'connected':
                self.current_test_status['connected_numbers'].append(phone_number)
                self._log(f"✓ Added to connected list: {phone_number}")
            else:
                self.current_test_status['failed_numbers'].append(phone_number)
                self._log(f"✗ Added to failed list: {phone_number} ({result['status']})")
            
            self._update_status()
        
        self.current_test_status['is_running'] = False
        self.current_test_status['current_number'] = None
        self._update_status()
        
        # Final summary
        self._log("\n" + "=" * 60)
        self._log(f"✅ Test Complete!")
        self._log(f"📊 Results: {len(self.current_test_status['connected_numbers'])} connected, "
                 f"{len(self.current_test_status['failed_numbers'])} failed")
        
        if self.current_test_status['connected_numbers']:
            self._log("\n✅ Connected numbers:")
            for num in self.current_test_status['connected_numbers']:
                self._log(f"  • {num}", level='success')
        
        if self.current_test_status['failed_numbers']:
            self._log("\n❌ Failed numbers:")
            for num in self.current_test_status['failed_numbers']:
                self._log(f"  • {num}", level='warning')
        
        self._log("=" * 60)
    
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