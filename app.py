"""
Phone Number Testing Panel - Web Application
"""
import os
import json
import logging
from flask import Flask, render_template, request, jsonify, send_file
from flask_socketio import SocketIO, emit
from sip_handler_simple import SimpleSIPTester as SIPCallTester
from export_utils import export_to_csv, export_to_excel, export_connected_only

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Initialize SocketIO
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# Initialize SIP tester
sip_tester = SIPCallTester()


@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')


@app.route('/api/config', methods=['GET'])
def get_config():
    """Get current configuration (without sensitive data)"""
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
            # Hide password
            if 'sip' in config and 'password' in config['sip']:
                config['sip']['password'] = '***hidden***'
            return jsonify(config)
    except FileNotFoundError:
        return jsonify({'error': 'Config file not found'}), 404


@app.route('/api/config', methods=['POST'])
def update_config():
    """Update configuration"""
    try:
        data = request.json
        
        # Load existing config to preserve password if not changed
        existing_config = {}
        try:
            with open('config.json', 'r') as f:
                existing_config = json.load(f)
        except:
            pass
        
        # Merge configs
        if 'sip' in data and 'password' in data['sip']:
            if data['sip']['password'] == '***hidden***' and existing_config:
                data['sip']['password'] = existing_config['sip']['password']
        
        # Save config
        with open('config.json', 'w') as f:
            json.dump(data, f, indent=2)
        
        # Reinitialize SIP tester with new config
        global sip_tester
        sip_tester.cleanup()
        sip_tester = SIPCallTester()
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/test/start', methods=['POST'])
def start_test():
    """Start phone number testing"""
    try:
        data = request.json
        phone_numbers = data.get('phone_numbers', [])
        
        if not phone_numbers:
            return jsonify({'error': 'No phone numbers provided'}), 400
        
        if sip_tester.get_status()['is_running']:
            return jsonify({'error': 'Test already in progress'}), 400
        
        # Start test with callbacks for real-time updates
        sip_tester.test_multiple_numbers(
            phone_numbers,
            status_callback=lambda status: socketio.emit('status_update', status),
            log_callback=lambda log: socketio.emit('log_update', log)
        )
        
        return jsonify({'success': True, 'total_numbers': len(phone_numbers)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/test/stop', methods=['POST'])
def stop_test():
    """Stop current test"""
    try:
        sip_tester.stop_test()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/test/status', methods=['GET'])
def get_status():
    """Get current test status"""
    return jsonify(sip_tester.get_status())


@app.route('/api/test/results', methods=['GET'])
def get_results():
    """Get test results"""
    return jsonify(sip_tester.get_results())


@app.route('/api/export/<format>', methods=['GET'])
def export_results(format):
    """Export results to file"""
    try:
        results = sip_tester.get_results()
        
        if not results:
            return jsonify({'error': 'No results to export'}), 404
        
        connected_only = request.args.get('connected_only', 'false').lower() == 'true'
        
        if connected_only:
            filename = export_connected_only(results, format)
        elif format == 'csv':
            filename = export_to_csv(results)
        elif format == 'xlsx':
            filename = export_to_excel(results)
        else:
            return jsonify({'error': 'Invalid format'}), 400
        
        return send_file(filename, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    emit('connected', {'message': 'Connected to server'})
    # Send current status
    emit('status_update', sip_tester.get_status())


@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    logger.info('Client disconnected')


@socketio.on('request_status')
def handle_status_request():
    """Handle status request"""
    emit('status_update', sip_tester.get_status())


if __name__ == '__main__':
    # Create config.json from example if it doesn't exist
    if not os.path.exists('config.json'):
        with open('config.example.json', 'r') as f:
            config = json.load(f)
        with open('config.json', 'w') as f:
            json.dump(config, f, indent=2)
    
    # Run the application
    socketio.run(app, 
                 host=sip_tester.config['server']['host'],
                 port=sip_tester.config['server']['port'],
                 debug=sip_tester.config['server']['debug'])