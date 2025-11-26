#!/usr/bin/env python3
"""
Server startup script with browser auto-open and port conflict handling
"""
import webbrowser
import time
import threading
import subprocess
import sys
import socket
import sys
import os
# Add parent directory to path to import main
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import app
import uvicorn

def is_port_in_use(port):
    """Check if a port is already in use"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def kill_process_on_port(port):
    """Kill the process using the specified port (Windows)"""
    try:
        # Find process using the port
        result = subprocess.run(
            ['netstat', '-ano'],
            capture_output=True,
            text=True,
            shell=True
        )
        
        for line in result.stdout.split('\n'):
            if f':{port}' in line and 'LISTENING' in line:
                parts = line.split()
                if len(parts) >= 5:
                    pid = parts[-1]
                    print(f"🛑 Found process {pid} using port {port}")
                    # Kill the process
                    subprocess.run(['taskkill', '/F', '/PID', pid], 
                                 capture_output=True, shell=True)
                    print(f"✅ Terminated process {pid}")
                    time.sleep(1)  # Wait for port to be released
                    return True
        return False
    except Exception as e:
        print(f"⚠️  Could not kill process: {e}")
        return False

def open_browser():
    """Open browser after a short delay"""
    time.sleep(2)  # Wait for server to start
    url = "http://localhost:8000"
    print(f"🌐 Opening browser at {url}...")
    try:
        webbrowser.open(url)
    except Exception as e:
        print(f"⚠️  Could not open browser automatically: {e}")
        print(f"   Please manually open: {url}")

if __name__ == "__main__":
    PORT = 8000
    
    print("\n" + "="*60)
    print("🚀 Starting InstaAuto Server...")
    print("="*60)
    
    # Check if port is in use
    if is_port_in_use(PORT):
        print(f"⚠️  Port {PORT} is already in use.")
        print("🔄 Attempting to free the port...")
        if kill_process_on_port(PORT):
            print("✅ Port freed successfully!")
        else:
            print(f"❌ Could not free port {PORT}.")
            print(f"   Please manually stop the process using port {PORT}")
            print(f"   Or change the port in main.py")
            sys.exit(1)
    
    print(f"📱 Server will be available at:")
    print(f"   • http://localhost:{PORT}")
    print(f"   • http://127.0.0.1:{PORT}")
    print("="*60)
    print("⏳ Starting server...\n")
    
    # Start browser in a separate thread
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()
    
    # Start the server
    try:
        uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="info")
    except OSError as e:
        if "10048" in str(e) or "address already in use" in str(e).lower():
            print(f"\n❌ Error: Port {PORT} is still in use.")
            print("   Please close the application using that port and try again.")
            print(f"   Or run: netstat -ano | findstr :{PORT}")
        else:
            print(f"\n❌ Error starting server: {e}")
        sys.exit(1)
