#!/usr/bin/env python3
"""
فاكر؟ (Faker?) - AI Memory Assistant
One-Click Deployment Script

This script provides a simple way to deploy and test the application
for the Google Gemma 3n Hackathon judges.
"""

import os
import sys
import time
import subprocess
import platform
import argparse
from pathlib import Path

def print_banner():
    """Print the application banner."""
    print("\n" + "=" * 80)
    print("""
    🧠 فاكر؟ (Faker?) - AI Memory Assistant
    
    One-Click Deployment Script
    
    Developed by 2survivors for the Google Gemma 3n Hackathon
    """)
    print("=" * 80 + "\n")

def check_python_version():
    """Check if the Python version is compatible."""
    print("🔍 Checking Python version...")
    major, minor = sys.version_info[:2]
    if major < 3 or (major == 3 and minor < 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"   Current version: Python {major}.{minor}")
        print("   Please install a compatible Python version")
        return False
    
    print(f"✅ Python {major}.{minor} detected (compatible)")
    return True

def check_pip():
    """Check if pip is installed."""
    print("🔍 Checking pip installation...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], 
                      check=True, capture_output=True)
        print("✅ pip is installed")
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        print("❌ Error: pip is not installed or not working")
        print("   Please install pip")
        return False

def create_virtual_env():
    """Create a virtual environment."""
    print("🔧 Creating virtual environment...")
    venv_dir = Path(".venv")
    
    if venv_dir.exists():
        print("✅ Virtual environment already exists")
        return True
    
    try:
        subprocess.run([sys.executable, "-m", "venv", ".venv"], check=True)
        print("✅ Virtual environment created")
        return True
    except subprocess.SubprocessError:
        print("❌ Error: Failed to create virtual environment")
        print("   Please install the venv module")
        return False

def activate_venv():
    """Return the activation command for the virtual environment."""
    if platform.system() == "Windows":
        return str(Path(".venv") / "Scripts" / "activate")
    else:
        return f"source {Path('.venv') / 'bin' / 'activate'}"

def install_dependencies():
    """Install dependencies."""
    print("📦 Installing dependencies...")
    
    # Determine the pip command
    if platform.system() == "Windows":
        pip_cmd = str(Path(".venv") / "Scripts" / "pip")
    else:
        pip_cmd = str(Path(".venv") / "bin" / "pip")
    
    try:
        subprocess.run([pip_cmd, "install", "-r", "requirements.txt"], check=True)
        print("✅ Dependencies installed")
        return True
    except subprocess.SubprocessError:
        print("❌ Error: Failed to install dependencies")
        return False

def check_huggingface_token():
    """Check if the Hugging Face token is set."""
    print("🔑 Checking Hugging Face token...")
    
    token = os.environ.get("HF_TOKEN")
    if token:
        print("✅ Hugging Face token found in environment")
        return True
    
    print("⚠️ Hugging Face token not found")
    print("   The application will run in mock mode")
    print("   To use the full capabilities, set the HF_TOKEN environment variable")
    return False

def run_demo_mode():
    """Run the demo mode."""
    print("🚀 Starting demo mode...")
    
    # Determine the python command
    if platform.system() == "Windows":
        python_cmd = str(Path(".venv") / "Scripts" / "python")
    else:
        python_cmd = str(Path(".venv") / "bin" / "python")
    
    try:
        subprocess.run([python_cmd, "src/demo_mode.py"], check=False)
        return True
    except subprocess.SubprocessError:
        print("❌ Error: Failed to run demo mode")
        return False

def run_visualization_dashboard():
    """Run the visualization dashboard."""
    print("📊 Starting visualization dashboard...")
    
    # Determine the python command
    if platform.system() == "Windows":
        python_cmd = str(Path(".venv") / "Scripts" / "python")
    else:
        python_cmd = str(Path(".venv") / "bin" / "python")
    
    try:
        subprocess.run([python_cmd, "src/ui/visualization_dashboard.py"], check=False)
        return True
    except subprocess.SubprocessError:
        print("❌ Error: Failed to run visualization dashboard")
        return False

def run_main_application():
    """Run the main application."""
    print("🚀 Starting main application...")
    
    # Determine the python command
    if platform.system() == "Windows":
        python_cmd = str(Path(".venv") / "Scripts" / "python")
    else:
        python_cmd = str(Path(".venv") / "bin" / "python")
    
    try:
        subprocess.run([python_cmd, "src/main.py"], check=False)
        return True
    except subprocess.SubprocessError:
        print("❌ Error: Failed to run main application")
        return False

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="فاكر؟ (Faker?) - AI Memory Assistant")
    parser.add_argument("--demo", action="store_true", help="Run in demo mode")
    parser.add_argument("--dashboard", action="store_true", help="Run visualization dashboard")
    parser.add_argument("--skip-setup", action="store_true", help="Skip setup steps")
    args = parser.parse_args()
    
    print_banner()
    
    if not args.skip_setup:
        # Check requirements
        if not check_python_version():
            sys.exit(1)
        
        if not check_pip():
            sys.exit(1)
        
        # Setup environment
        if not create_virtual_env():
            sys.exit(1)
        
        # Print activation instructions
        print(f"\n📝 To activate the virtual environment manually:")
        print(f"   {activate_venv()}")
        
        # Install dependencies
        if not install_dependencies():
            sys.exit(1)
        
        # Check Hugging Face token
        check_huggingface_token()
    
    # Run the selected mode
    if args.demo:
        run_demo_mode()
    elif args.dashboard:
        run_visualization_dashboard()
    else:
        run_main_application()

if __name__ == "__main__":
    main() 