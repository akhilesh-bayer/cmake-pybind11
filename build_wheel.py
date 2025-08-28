#!/usr/bin/env python3
"""
Simple build script to test PEP 621 compliance.

This script can be used to build the package using modern Python packaging tools.
"""

import subprocess
import sys
import os

def main():
    """Build the cmakepybind11 package."""
    print("Building cmakepybind11 package with PEP 621 compliance...")
    
    # Change to project root directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    try:
        # Try using the modern build tool first
        print("Attempting to build with 'python -m build'...")
        subprocess.check_call([sys.executable, "-m", "build", "--wheel"])
        print("✓ Successfully built wheel using modern build tools!")
        
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Modern build tools not available, falling back to legacy setup.py...")
        try:
            subprocess.check_call([sys.executable, "setup.py", "bdist_wheel"])
            print("✓ Successfully built wheel using legacy setup.py!")
        except subprocess.CalledProcessError as e:
            print(f"✗ Build failed: {e}")
            return 1
    
    print("\n📦 Wheel files created in 'dist/' directory")
    return 0

if __name__ == "__main__":
    exit(main())
