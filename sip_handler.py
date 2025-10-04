"""
Lightweight SIP Call Handler for Phone Number Testing
"""
import time
import json
import logging
import threading
from datetime import datetime
from typing import List, Dict, Callable
from pyVoIP.VoIP import VoIPPhone, CallState

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SIPCallTester:
    """Handles SIP calls to test phone numbers connectivity"""
    
    def __init__(self, config_path: str = 'config.json'):
        """Initialize SIP tester with configuration"""
        self.config = self._load_config(config_path)
        self.sip_config = self.config['sip']
        self.test_settings = self.config['test_settings']
        
        self.phone = None
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
        
    def _load_config(self, config_path: str) -> dict:
        """Load configuration from JSON file"""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"Config file {config_path} not found. Using example config.")
            with open('config.example.json', 'r') as f:
                return json.load(f)
    
    def initialize_phone(self) -> bool:
        """Initialize VoIP phone with SIP credentials"""
        try:
            self.phone = VoIPPhone(
                server=self.sip_config['server'],
                port=self.sip_config['port'],
                username=self.sip_config['username'],
                password=self.sip_config['password'],
                callCallback=self._call_callback
            )
            
            # Start the phone in a separate thread
            phone_thread = threading.Thread(target=self.phone.start)
            phone_thread.daemon = True
            phone_thread.start()
            
            # Wait for registration
            time.sleep(2)
            
            self._log(f"SIP phone initialized: {self.sip_config['username']}@{self.sip_config['server']}")
            return True
            
        except Exception as e:
            self._log(f"Failed to initialize SIP phone: {str(e)}", level='error')
            return False
    
    def _call_callback(self, call):
        """Callback for handling call events"""
        # This callback is called when receiving calls
        # For our use case (making calls), we'll handle it differently
        pass
    
    def test_phone_number(self, phone_number: str) -> Dict:
        """Test a single phone number"""
        result = {
            'phone_number': phone_number,
            'status': 'unknown',
            'timestamp': datetime.now().isoformat(),
            'duration': 0,
            'error': None
        }
        
        try:
            self._log(f"Testing number: {phone_number}")
            
            # Make the call
            start_time = time.time()
            call = self.phone.call(phone_number)
            
            # Wait for connection or timeout
            max_wait = self.test_settings['timeout_seconds']
            connected = False
            
            while time.time() - start_time < max_wait:
                if call.state == CallState.ANSWERED:
                    connected = True
                    self._log(f"✓ Connected: {phone_number}", level='success')
                    result['status'] = 'connected'
                    
                    # Wait for configured duration
                    time.sleep(self.test_settings['call_duration_seconds'])
                    break
                elif call.state == CallState.ENDED:
                    self._log(f"✗ Failed: {phone_number} - Call ended", level='warning')
                    result['status'] = 'failed'
                    result['error'] = 'Call ended without connection'
                    break
                
                time.sleep(0.5)
            
            if not connected and result['status'] == 'unknown':
                self._log(f"✗ Timeout: {phone_number}", level='warning')
                result['status'] = 'timeout'
                result['error'] = 'Connection timeout'
            
            # Hang up the call
            try:
                call.hangup()
            except:
                pass
            
            result['duration'] = time.time() - start_time
            
            # Idle between calls
            if result['status'] == 'connected':
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
        
        # Initialize phone if not already done
        if not self.phone:
            if not self.initialize_phone():
                self.current_test_status['is_running'] = False
                self._update_status()
                return
        
        # Test each number
        for idx, phone_number in enumerate(phone_numbers, 1):
            if not self.current_test_status['is_running']:
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
        self.current_test_status['is_running'] = False
        self._log("Test stopped by user", level='warning')
    
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
        if self.phone:
            try:
                self.phone.stop()
            except:
                pass