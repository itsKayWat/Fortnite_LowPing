import subprocess
import time
import os
import ctypes
import sys

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()

def run_command(command):
    try:
        process = subprocess.run(command, shell=True, capture_output=True, text=True)
        print(f"Running: {command}")
        if process.returncode == 0:
            print("✓ Success")
        else:
            print(f"⚠️ Warning: {process.stderr}")
    except Exception as e:
        print(f"Error running {command}: {str(e)}")

def fix_fortnite_network():
    print("\n🔄 Running Fortnite Network Fix...")
    
    fix_commands = [
        # Reset Windows Firewall
        'netsh advfirewall reset',
        'netsh advfirewall set allprofiles state on',
        'netsh advfirewall set allprofiles firewallpolicy allowinbound,allowoutbound',
        
        # Allow Fortnite and Epic through firewall
        'netsh advfirewall firewall add rule name="Fortnite_Game" dir=out action=allow program="C:\\Program Files\\Epic Games\\Fortnite\\FortniteGame\\Binaries\\Win64\\FortniteClient-Win64-Shipping.exe" enable=yes',
        'netsh advfirewall firewall add rule name="Epic_Launcher" dir=out action=allow program="C:\\Program Files (x86)\\Epic Games\\Launcher\\Portal\\Binaries\\Win32\\EpicGamesLauncher.exe" enable=yes',
        
        # Open Fortnite ports
        'netsh advfirewall firewall add rule name="Fortnite_UDP" dir=in action=allow protocol=UDP localport=5222,5795-5847,9000-9999 enable=yes',
        'netsh advfirewall firewall add rule name="Fortnite_UDP_Out" dir=out action=allow protocol=UDP remoteport=5222,5795-5847,9000-9999 enable=yes',
        'netsh advfirewall firewall add rule name="Fortnite_TCP" dir=in action=allow protocol=TCP localport=5222,5795-5847,80,443 enable=yes',
        'netsh advfirewall firewall add rule name="Fortnite_TCP_Out" dir=out action=allow protocol=TCP remoteport=5222,5795-5847,80,443 enable=yes',
        
        # Reset network stack
        'ipconfig /release',
        'ipconfig /renew',
        'ipconfig /flushdns',
        'netsh int ip reset',
        'netsh winsock reset',
        
        # Reset TCP/IP settings
        'netsh int tcp set global autotuninglevel=normal',
        'netsh int tcp set global congestionprovider=default',
        'netsh int tcp set global ecncapability=enabled',
        'netsh int tcp set global timestamps=enabled',
        'netsh int tcp set global initialRto=3000',
        'netsh int tcp set global rss=enabled',
        
        # Clear any DNS cache
        'ipconfig /registerdns',
        
        # Reset Windows network stack
        'netsh int ip reset c:\\resetlog.txt',
        'netsh winsock reset catalog'
    ]

    print("\n🔧 Applying network fixes...")
    for cmd in fix_commands:
        run_command(cmd)
        time.sleep(0.5)

    print("\n✅ Network fix complete!")
    print("🎮 Please try launching Fortnite again")
    print("⚠️ If issues persist, a system restart may be required")

if __name__ == "__main__":
    try:
        run_as_admin()
        fix_fortnite_network()
        input("\nPress Enter to exit...")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        input("\nPress Enter to exit...") 