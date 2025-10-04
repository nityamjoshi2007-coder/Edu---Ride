#!/usr/bin/env python3
"""
Generate a secure secret key for Flask application
"""

import secrets
import string

def generate_secret_key(length=32):
    """Generate a cryptographically secure random string"""
    alphabet = string.ascii_letters + string.digits + '!@#$%^&*'
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def generate_hex_key(length=32):
    """Generate a hex-based secret key"""
    return secrets.token_hex(length)

if __name__ == '__main__':
    print("Flask Secret Key Generator")
    print("=" * 50)
    
    # Generate different types of secret keys
    print("1. Random String Key:")
    print(f"   SECRET_KEY='{generate_secret_key()}'")
    print()
    
    print("2. Hex-based Key (recommended):")
    hex_key = generate_hex_key()
    print(f"   SECRET_KEY='{hex_key}'")
    print()
    
    print("3. URL-safe Key:")
    url_safe_key = secrets.token_urlsafe(32)
    print(f"   SECRET_KEY='{url_safe_key}'")
    print()
    
    print("Usage Instructions:")
    print("- Copy one of the keys above")
    print("- Set it as an environment variable: set SECRET_KEY=your-key-here")
    print("- Or replace the default in app.py for development")
    print()
    print("Security Notes:")
    print("- Never commit secret keys to version control")
    print("- Use different keys for development and production")
    print("- Keep your production keys secure and private")
