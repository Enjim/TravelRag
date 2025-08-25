#!/usr/bin/env python3
"""
TravelRag Setup Script - Works on Windows and Mac
Simple setup with minimal dependencies
"""

import sys
import subprocess
import os
import platform

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("ERROR: Python 3.8 or higher is required!")
        print(f"Current version: {sys.version_info.major}.{sys.version_info.minor}")
        return False
    
    print(f"SUCCESS: Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def install_dependencies():
    """Install Python dependencies."""
    print("\nInstalling Python dependencies...")
    
    try:
        # Install requirements
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ], check=True, capture_output=True, text=True)
        
        print("SUCCESS: All dependencies installed!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Failed to install dependencies: {e}")
        print("\nTrying alternative approach for FAISS...")
        
        # Try installing FAISS separately
        try:
            if platform.system() == "Windows":
                print("Trying Windows-specific FAISS installation...")
                result = subprocess.run([
                    sys.executable, "-m", "pip", "install", "faiss-cpu==1.7.4", "--only-binary=all"
                ], check=True, capture_output=True, text=True)
            else:
                print("Trying conda-based FAISS installation...")
                result = subprocess.run([
                    sys.executable, "-m", "pip", "install", "faiss-cpu"
                ], check=True, capture_output=True, text=True)
            
            print("SUCCESS: FAISS installed!")
            
            # Install other dependencies
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", "sentence-transformers==2.2.2", "openai==1.3.0", "streamlit==1.28.0", "requests==2.31.0", "beautifulsoup4==4.12.2", "lxml==4.9.3", "wikipediaapi==0.6.0"
            ], check=True, capture_output=True, text=True)
            
            print("SUCCESS: All dependencies installed!")
            return True
            
        except subprocess.CalledProcessError as e2:
            print(f"ERROR: Alternative installation also failed: {e2}")
            print("\nManual installation required:")
            print("1. Install Anaconda/Miniconda")
            print("2. Run: conda install -c conda-forge faiss-cpu")
            print("3. Run: pip install -r requirements.txt")
            return False

def check_config():
    """Check if config.py exists and has API key."""
    if not os.path.exists('config.py'):
        print("\nCreating config.py template...")
        
        config_content = '''# OpenAI API Configuration
OPENAI_API_KEY = "your-api-key-here"  # Replace with your actual API key

# RAG Configuration
TOP_K_CHUNKS = 5  # Number of document chunks to retrieve
'''
        
        with open('config.py', 'w') as f:
            f.write(config_content)
        
        print("SUCCESS: config.py created!")
        print("IMPORTANT: Edit config.py and add your OpenAI API key")
        return False
    
    # Check if API key is set
    try:
        with open('config.py', 'r') as f:
            content = f.read()
        
        if 'your-api-key-here' in content:
            print("WARNING: Please set your OpenAI API key in config.py")
            return False
        else:
            print("SUCCESS: OpenAI API key configured")
            return True
            
    except Exception as e:
        print(f"ERROR: Could not read config.py: {e}")
        return False

def download_sample_data():
    """Download sample travel data."""
    print("\nDownloading sample travel data...")
    
    try:
        result = subprocess.run([
            sys.executable, "data_collector.py"
        ], check=True, capture_output=True, text=True)
        
        print("SUCCESS: Sample data downloaded!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"WARNING: Could not download sample data: {e}")
        print("You can run this manually later with: python data_collector.py")
        return False

def main():
    """Main setup function."""
    print("TravelRag Setup - Cross-Platform")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        return
    
    # Check if we're in the right directory
    if not os.path.exists('requirements.txt'):
        print("ERROR: Please run this script from the TravelRag project directory!")
        return
    
    # Install dependencies
    if not install_dependencies():
        return
    
    # Check configuration
    config_ok = check_config()
    
    # Download sample data
    download_sample_data()
    
    print("\n" + "=" * 40)
    print("SETUP COMPLETE!")
    print("=" * 40)
    
    if not config_ok:
        print("\nNEXT STEPS:")
        print("1. Edit config.py and add your OpenAI API key")
        print("2. Run: python data_collector.py (if not already done)")
        print("3. Run: streamlit run streamlit_app.py")
    else:
        print("\nREADY TO GO!")
        print("Run: streamlit run streamlit_app.py")
    
    print("\nFor testing, run: python test.py")

if __name__ == "__main__":
    main()
