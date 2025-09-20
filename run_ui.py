#!/usr/bin/env python3
"""
Simple launcher script for the Travel Bot UI
"""
import subprocess
import sys
import os

def main():
    """Launch the Streamlit UI"""
    print("🚀 Starting Travel Bot UI...")
    print("The UI will open in your default web browser.")
    print("Press Ctrl+C to stop the server.")
    print("-" * 50)
    
    # Change to the correct directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    try:
        # Run streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "chat_ui.py",
            "--server.port", "8501",
            "--server.address", "localhost",
            "--browser.gatherUsageStats", "false"
        ])
    except KeyboardInterrupt:
        print("\n👋 Travel Bot UI stopped. Goodbye!")
    except Exception as e:
        print(f"❌ Error starting UI: {e}")
        print("Make sure you have installed the requirements: pip install -r requirements.txt")

if __name__ == "__main__":
    main()
