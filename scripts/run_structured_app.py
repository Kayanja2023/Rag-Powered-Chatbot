#!/usr/bin/env python3
"""
Launcher for the structured Clickatell AI Assistant
"""

import subprocess
import sys
import os

def check_structure():
    """Check if the structured folders exist"""
    required_paths = [
        "src/core",
        "src/ui", 
        "src/utils",
        "app",
        "tests"
    ]
    
    missing = []
    for path in required_paths:
        if not os.path.exists(path):
            missing.append(path)
    
    if missing:
        print("Missing required directories:")
        for path in missing:
            print(f"  - {path}")
        return False
    
    return True

def run_tests():
    """Run tests before starting the app"""
    print("Running tests...")
    try:
        result = subprocess.run([sys.executable, "tests/test_core.py"], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            print("Tests failed!")
            print(result.stdout)
            print(result.stderr)
            return False
        print("Tests passed!")
        return True
    except Exception as e:
        print(f"Error running tests: {e}")
        return False

def main():
    """Main launcher function"""
    print("Starting Structured Clickatell AI Assistant...")
    print("=" * 50)
    
    # Check structure
    if not check_structure():
        print("Please ensure all required directories exist.")
        return
    
    # Run tests
    if not run_tests():
        print("Tests failed. Please fix issues before running.")
        return
    
    print("Launching structured application...")
    
    try:
        subprocess.run([
            "streamlit", "run", "app/main.py",
            "--theme.primaryColor", "#667eea"
        ])
    except KeyboardInterrupt:
        print("\nGoodbye!")
    except Exception as e:
        print(f"Error: {e}")
        print("Try running: streamlit run app/main.py")

if __name__ == "__main__":
    main()