#!/usr/bin/env python3
"""
Telugu Q&A Generator - Run Script
This script helps to run the application in different modes
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version() -> None:
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required")
        sys.exit(1)
    print("✅ Python version check passed")

def check_dependencies() -> None:
    """Check if required dependencies are installed"""
    try:
        import flask
        _ = flask
        print("✅ Core dependencies are installed")
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please install dependencies using: pip install -r requirements.txt")
        sys.exit(1)

def setup_environment() -> None:
    """Setup environment variables"""
    os.environ['FLASK_ENV'] = 'development'
    os.environ['FLASK_DEBUG'] = '1'
    print("✅ Environment variables set")

def run_application() -> None:
    """Run the Flask application"""
    try:
        print("🚀 Starting Telugu Q&A Generator...")
        print("📱 Access the application at: http://localhost:5000")
        print("🛑 Press Ctrl+C to stop the server")
        
        # Run the Flask app
        from app import app
        app.run(host='0.0.0.0', port=5000, debug=True)
        
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

def install_dependencies() -> None:
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        sys.exit(1)

def main() -> None:
    """Main function"""
    print("🌟 Telugu Q&A Generator - Setup & Run")
    print("=" * 50)
    
    # Check Python version
    check_python_version()
    
    # Check if requirements.txt exists
    if not Path('requirements.txt').exists():
        print("❌ requirements.txt not found")
        sys.exit(1)
    
    # Check dependencies
    try:
        check_dependencies()
    except SystemExit:
        # If dependencies missing, offer to install
        response = input("Install missing dependencies? (y/n): ").lower()
        if response == 'y':
            install_dependencies()
            check_dependencies()
        else:
            print("Please install dependencies manually")
            sys.exit(1)
    
    # Setup environment
    setup_environment()
    
    # Run the application
    run_application()

if __name__ == "__main__":
    main()
