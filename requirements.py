import subprocess
import sys

def install_requirements():
    requirements = [
        'psutil',
        'ctypes',
    ]
    
    print("📦 Installing required packages...")
    for package in requirements:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ Successfully installed {package}")
        except:
            print(f"❌ Failed to install {package}")

if __name__ == "__main__":
    install_requirements()
    input("\nPress Enter to exit...")