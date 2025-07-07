#!/usr/bin/env python3
"""
Quick Installation Script for LiveKit + OpenAI Realtime Testing
This script helps you get started quickly with the testing environment
"""
import subprocess
import sys
import os


def run_command(command):
    """Run a command and return success status"""
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr


def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 9:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Requires Python 3.9+")
        return False


def install_requirements():
    """Install required packages"""
    print("\n🔄 Installing LiveKit + OpenAI dependencies...")
    
    success, output = run_command("pip install -r requirements.txt")
    
    if success:
        print("✅ All dependencies installed successfully!")
        return True
    else:
        print(f"❌ Installation failed: {output}")
        return False


def check_env_file():
    """Check if .env file exists in parent directory"""
    parent_env = os.path.join("..", ".env")
    main_env = os.path.join("..", "vapi.env")
    
    print("\n🔄 Checking for environment files...")
    
    if os.path.exists(parent_env):
        print("✅ Found .env file in parent directory")
        return True
    elif os.path.exists(main_env):
        print("✅ Found vapi.env file in parent directory")
        print("💡 Consider adding OPENAI_API_KEY to this file")
        return True
    else:
        print("⚠️  No .env file found in parent directory")
        print("💡 Create a .env file in the main directory with OPENAI_API_KEY")
        return False


def main():
    """Main installation function"""
    print("🚀 LiveKit + OpenAI Realtime Setup Script")
    print("="*50)
    
    # Check Python version
    python_ok = check_python_version()
    if not python_ok:
        print("\n❌ Please upgrade to Python 3.9 or later")
        return
    
    # Install dependencies
    install_ok = install_requirements()
    if not install_ok:
        print("\n❌ Installation failed. Please check error messages above.")
        return
    
    # Check environment file
    env_ok = check_env_file()
    
    # Summary
    print("\n" + "="*50)
    print("📊 INSTALLATION SUMMARY")
    print("="*50)
    print(f"Python Version: {'✅ OK' if python_ok else '❌ FAILED'}")
    print(f"Dependencies: {'✅ OK' if install_ok else '❌ FAILED'}")
    print(f"Environment File: {'✅ OK' if env_ok else '⚠️  MISSING'}")
    
    if python_ok and install_ok:
        print("\n🎉 Installation completed successfully!")
        print("\n📋 NEXT STEPS:")
        print("1. Add OPENAI_API_KEY to your main .env file")
        print("2. Run: python setup_test.py")
        print("3. Run: python interview_agent.py")
        
        if not env_ok:
            print("\n⚠️  Don't forget to create .env file with OPENAI_API_KEY!")
    else:
        print("\n❌ Installation incomplete. Please fix issues above.")


if __name__ == "__main__":
    main()
 