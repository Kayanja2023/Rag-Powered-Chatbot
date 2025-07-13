import subprocess
import sys
import os

def main():
    print("Starting Clickatell AI Assistant...")
    print("=" * 50)
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("Warning: .env file not found")
        print("Please ensure your OpenAI API key is configured")
    
    print("Launching Streamlit app...")
    
    try:
        subprocess.run([
            "streamlit", "run", "streamlit_app.py",
            "--theme.primaryColor", "#667eea"
        ])
    except KeyboardInterrupt:
        print("\nGoodbye!")
    except Exception as e:
        print(f"Error: {e}")
        print("Try running directly: streamlit run streamlit_app.py")

if __name__ == "__main__":
    main()