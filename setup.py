#!/usr/bin/env python3
"""
Setup script for TravelRag
Run this to get everything set up quickly!
"""

import os
import subprocess
import sys

def run_command(command, description):
    """Run a command and show progress."""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during {description}: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required!")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def check_config():
    """Check if config.py has been set up."""
    try:
        with open('config.py', 'r') as f:
            content = f.read()
            if 'your-api-key-here' in content:
                print("⚠️  Warning: Please set your OpenAI API key in config.py")
                return False
            else:
                print("✅ OpenAI API key configured")
                return True
    except FileNotFoundError:
        print("❌ config.py not found!")
        return False

def main():
    """Main setup function."""
    print("🚀 Welcome to TravelRag Setup!")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return
    
    # Check if we're in the right directory
    if not os.path.exists('requirements.txt'):
        print("❌ Please run this script from the TravelRag project directory!")
        return
    
    # Install dependencies
    print("\n📦 Installing Python dependencies...")
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        print("❌ Failed to install dependencies. Please check your Python environment.")
        return
    
    # Check config
    print("\n⚙️  Checking configuration...")
    if not check_config():
        print("\n📝 Please edit config.py and add your OpenAI API key:")
        print("   OPENAI_API_KEY = 'sk-your-actual-api-key-here'")
        print("\nThen run this setup script again.")
        return
    
    # Download travel data
    print("\n📚 Downloading travel articles...")
    if not run_command("python data_collector.py", "Downloading travel data"):
        print("❌ Failed to download travel data.")
        return
    
    # Test the system
    print("\n🧪 Testing the system...")
    if not run_command("python text_processor.py", "Testing text processing"):
        print("❌ Text processing test failed.")
        return
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("\n🚀 To start the web app, run:")
    print("   streamlit run streamlit_app.py")
    print("\n📖 For more information, see README.md")
    print("=" * 50)

if __name__ == "__main__":
    main()
