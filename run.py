#!/usr/bin/env python3
"""
Edu-Ride Application Runner
Simple script to run the Flask application with proper setup
"""

import os
import sys
from app import app, db

def setup_database():
    """Initialize the database with tables"""
    with app.app_context():
        db.create_all()
        print("✅ Database initialized successfully!")

def main():
    """Main function to run the application"""
    print("🚀 Starting Edu-Ride Application...")
    print("=" * 50)
    
    # Setup database
    setup_database()
    
    # Get configuration
    debug_mode = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    host = os.environ.get('FLASK_HOST', '127.0.0.1')
    port = int(os.environ.get('FLASK_PORT', 5000))
    
    print(f"🌐 Server will run on: http://{host}:{port}")
    print(f"🔧 Debug mode: {'ON' if debug_mode else 'OFF'}")
    print("=" * 50)
    print("📱 Open your browser and navigate to the URL above")
    print("👥 Register as a student or driver to get started")
    print("=" * 50)
    
    try:
        app.run(host=host, port=port, debug=debug_mode)
    except KeyboardInterrupt:
        print("\n👋 Edu-Ride application stopped. Goodbye!")
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
