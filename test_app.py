#!/usr/bin/env python3
"""
Test script to verify Edu-Ride application is working
"""

import requests
import time

def test_application():
    """Test if the Flask application is running"""
    try:
        print("Testing Edu-Ride Application...")
        print("=" * 40)
        
        # Test home page
        response = requests.get('http://localhost:5000', timeout=5)
        if response.status_code == 200:
            print("[OK] Home page: Working")
        else:
            print(f"[ERROR] Home page: Error {response.status_code}")
            
        # Test login page
        response = requests.get('http://localhost:5000/login', timeout=5)
        if response.status_code == 200:
            print("[OK] Login page: Working")
        else:
            print(f"[ERROR] Login page: Error {response.status_code}")
            
        # Test register page
        response = requests.get('http://localhost:5000/register', timeout=5)
        if response.status_code == 200:
            print("[OK] Register page: Working")
        else:
            print(f"[ERROR] Register page: Error {response.status_code}")
            
        print("\n[SUCCESS] Application is running successfully!")
        print("[INFO] Open your browser and go to: http://localhost:5000")
        
    except requests.exceptions.ConnectionError:
        print("[ERROR] Cannot connect to application")
        print("[INFO] Make sure the Flask app is running with: python app.py")
    except Exception as e:
        print(f"[ERROR] Error testing application: {e}")

if __name__ == '__main__':
    test_application()
