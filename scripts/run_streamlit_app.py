#!/usr/bin/env python3
"""
Launcher for the modern Clickatell Streamlit app
"""

import subprocess
import sys
import os
from dotenv import load_dotenv

def check_requirements():
    """Check if all required packages are installed"""
    required_imports = {
        'streamlit': 'streamlit',
        'langchain': 'langchain', 
        'openai': 'openai',
        'faiss': 'faiss-cpu',
        'sentence_transformers': 'sentence-transformers',
        'dotenv': 'python-dotenv',
        'plotly': 'plotly'
    }
    
    missing_packages = []
    
    for import_name, package_name in required_imports.items():
        try:
            __import__(import_name)
        except ImportError:
            missing_packages.append(package_name)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n📦 Install missing packages with:")
        print(f"   pip install {' '.join(missing_packages)}")
        return False
    
    return True

def check_api_key():
    """Check if OpenAI API key is configured"""
    try:
        load_dotenv()
        
        api_key = os.getenv("OPENAI_API_KEY")
        
        if not api_key:
            print("❌ OPENAI_API_KEY not found in .env file")
            print("📝 Please add your OpenAI API key to the .env file")
            return False
        
        if api_key == "your_openai_api_key_here":
            print("❌ Please replace the placeholder with your actual OpenAI API key")
            return False
        
        print(f"✅ API Key configured: {api_key[:10]}...{api_key[-4:]}")
        return True
    except Exception as e:
        print(f"⚠️ Warning: Could not verify API key: {e}")
        return True  # Continue anyway

def main():
    """Main launcher function"""
    print("🚀 Starting Clickatell AI Assistant...")
    print("=" * 50)
    
    # Check requirements
    print("📦 Checking requirements...")
    if not check_requirements():
        sys.exit(1)
    
    # Check API key
    print("🔑 Checking API configuration...")
    if not check_api_key():
        sys.exit(1)
    
    print("✅ All checks passed!")
    print("🌐 Launching Streamlit app...")
    print("=" * 50)
    
    # Launch Streamlit app
    try:
        subprocess.run([
            "streamlit", "run", "streamlit_app.py",
            "--theme.base", "light",
            "--theme.primaryColor", "#667eea",
            "--theme.backgroundColor", "#ffffff",
            "--theme.secondaryBackgroundColor", "#f8f9fa",
            "--theme.textColor", "#2c3e50"
        ])
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error launching app: {e}")

if __name__ == "__main__":
    main()