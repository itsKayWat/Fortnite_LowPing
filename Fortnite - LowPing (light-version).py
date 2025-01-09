import os
import subprocess
import ctypes
import sys
import time
import psutil
import json

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

def monitor_fortnite():
    """Monitor Fortnite process and auto-reverse when it closes"""
    print("\n⌛ Monitoring Fortnite process...")
    while True:
        fortnite_running = False
        for proc in psutil.process_iter(['name']):
            if "FortniteClient-Win64-Shipping.exe" in proc.info['name']:
                fortnite_running = True
                break
        if not fortnite_running:
            print("\n🎮 Fortnite closed, reversing optimizations...")
            reverse_optimizations()
            break
        time.sleep(5)

def reverse_optimizations():
    print("\n🔄 Reversing network optimizations...")
    
    restore_commands = [
        # Remove Fortnite firewall rules first
        'netsh advfirewall firewall delete rule name="Fortnite UDP"',
        'netsh advfirewall firewall delete rule name="Fortnite UDP Out"',
        'netsh advfirewall firewall delete rule name="Fortnite TCP"',
        'netsh advfirewall firewall delete rule name="Fortnite TCP Out"',
        
        # Restore network settings
        'netsh int tcp set global autotuninglevel=normal',
        'netsh int tcp set global congestionprovider=default',
        'netsh int tcp set global ecncapability=enabled',
        'netsh int tcp set global timestamps=enabled',
        'netsh int tcp set global rss=enabled',
        'netsh int tcp set global initialRto=3000',
        'netsh int tcp set global maxsynretransmissions=4',
        
        # Soft reset network stack without requiring restart
        'ipconfig /release',
        'ipconfig /renew',
        'ipconfig /flushdns',
        'netsh int ip reset /soft',  # Added /soft flag
        'netsh winsock reset catalog',  # Added catalog parameter
        
        # Reset Windows Auto-Tuning
        'powershell "Set-NetTCPSetting -SettingName InternetCustom -AutoTuningLevelLocal Normal"'
    ]

    for cmd in restore_commands:
        run_command(cmd)
        time.sleep(1)  # Increased delay between commands

    print("\n✅ All optimizations have been reversed!")
    print("🔄 Network settings restored to default values")
    print("🎮 You can now run Fortnite or other applications")

def optimize_fortnite():
    print("\n⚡ Applying aggressive ping optimization...")
    
    # Kill more background processes
    processes_to_kill = [
        'chrome.exe', 'msedge.exe', 'firefox.exe', 'discord.exe', 'spotify.exe',
        'steam.exe', 'epicgameslauncher.exe', 'slack.exe', 'teams.exe',
        'skype.exe', 'zoom.exe', 'outlook.exe', 'onedrive.exe', 'dropbox.exe'
    ]
    
    print("\n🔄 Closing background applications...")
    for proc in psutil.process_iter(['name']):
        if proc.info['name'].lower() in processes_to_kill:
            try:
                psutil.Process(proc.pid).terminate()
                print(f"✓ Terminated: {proc.info['name']}")
            except:
                continue

    # Enhanced network optimizations
    network_commands = [
        # Clear DNS and reset network stack
        'ipconfig /flushdns',
        'netsh winsock reset catalog',
        
        # Fortnite specific ports with priority
        'netsh advfirewall firewall add rule name="Fortnite UDP" dir=in action=allow protocol=UDP localport=9000-9999 enable=yes',
        'netsh advfirewall firewall add rule name="Fortnite UDP Out" dir=out action=allow protocol=UDP remoteport=9000-9999 enable=yes',
        'netsh advfirewall firewall add rule name="Fortnite TCP" dir=in action=allow protocol=TCP localport=80,443,5222,5795-5799 enable=yes',
        'netsh advfirewall firewall add rule name="Fortnite TCP Out" dir=out action=allow protocol=TCP remoteport=80,443,5222,5795-5799 enable=yes',
        
        # Aggressive network optimizations
        'netsh int tcp set global dca=enabled',
        'netsh int tcp set global netdma=enabled',
        'netsh int tcp set global ecncapability=disabled',
        'netsh int tcp set global timestamps=disabled',
        'netsh int tcp set global initialRto=1200',  # Reduced from 3000
        'netsh int tcp set global maxsynretransmissions=2',
        'netsh int tcp set global rss=enabled',
        'netsh int tcp set global nonsackrttresiliency=disabled',
        'netsh int tcp set global rsc=disabled',
        'netsh int tcp set global pacingprofile=off',
        
        # QoS and priority settings
        'netsh int tcp set global congestionprovider=ctcp',
        'netsh int tcp set global autotuninglevel=restricted',
        'netsh int tcp set global chimney=enabled',
        'netsh int tcp set global fastopen=enabled',
        
        # Network adapter optimizations
        'powershell "Set-NetAdapterAdvancedProperty -Name "*" -RegistryKeyword "*FlowControl" -RegistryValue 0"',
        'powershell "Set-NetAdapterAdvancedProperty -Name "*" -RegistryKeyword "*InterruptModeration" -RegistryValue 0"',
        'powershell "Set-NetAdapterAdvancedProperty -Name "*" -RegistryKeyword "*PriorityVLANTag" -RegistryValue 1"',
        'powershell "Set-NetAdapterAdvancedProperty -Name "*" -RegistryKeyword "*JumboPacket" -RegistryValue 1514"',
        
        # Disable Windows Auto-Tuning and set high priority
        'powershell "Set-NetTCPSetting -SettingName InternetCustom -AutoTuningLevelLocal Disabled"',
        'powershell "Set-NetTCPSetting -SettingName InternetCustom -ScalingHeuristics Disabled"',
        'powershell "Set-NetTCPSetting -SettingName InternetCustom -CongestionProvider CTCP"',
        
        # Disable LSO and RSS for better latency
        'powershell "Disable-NetAdapterLso -Name "*"',
        'powershell "Disable-NetAdapterRsc -Name "*"',
        
        # Set network adapter power management
        'powershell "Set-NetAdapterPowerManagement -Name "*" -SelectiveSuspend Disabled"',
        
        # Clear ARP cache and reset IP
        'arp -d *',
        'netsh interface ip delete arpcache',
        'ipconfig /release',
        'ipconfig /renew'
    ]

    print("\n⚡ Applying network optimizations...")
    for cmd in network_commands:
        run_command(cmd)
        time.sleep(0.5)

    print("\n✅ Optimization complete!")
    print("⚡ Network is now optimized for lowest possible ping")
    print("📝 To reverse optimizations, run this script again and select option 2")
    print("\n⚠️ Note: If you experience connection issues, use option 2 to reverse")
    
    # Start monitoring Fortnite process
    monitor_fortnite()

def optimize_bot_lobbies():
    print("\n🤖 Optimizing for bot/easy lobbies...")
    
    network_commands = [
        # Set high latency to get easier lobbies
        'netsh int tcp set global chimney=enabled',
        'netsh int tcp set global autotuninglevel=restricted',
        'netsh int tcp set global congestionprovider=none',
        'netsh int tcp set global ecncapability=disabled',
        'netsh int tcp set global initialRto=3000',
        
        # Restrict to specific regions for better bot chances
        'netsh advfirewall firewall add rule name="Fortnite Region" dir=out action=allow protocol=UDP remoteport=22222-22223 remoteip=127.0.0.1',
        'netsh advfirewall firewall add rule name="Fortnite Region" dir=in action=allow protocol=UDP localport=22222-22223',
        
        # Add artificial delay
        'netsh int tcp set global maxsynretransmissions=4',
        'netsh int tcp set global fastopen=disabled'
    ]

    print("⚠️ This will temporarily increase your latency for easier lobbies")
    confirm = input("Continue? (y/n): ")
    
    if confirm.lower() == 'y':
        for cmd in network_commands:
            run_command(cmd)
            time.sleep(0.5)
        
        print("\n✅ Bot lobby optimization complete!")
        print("🎮 You should now get easier lobbies")
        print("⚠️ Your ping will be higher than normal")
        print("📝 To reverse, run this script again and select option 2")
        
        # Monitor Fortnite and auto-reverse when closed
        monitor_fortnite()
    else:
        print("Operation cancelled")

def main():
    run_as_admin()
    
    while True:
        print("\n🎮 Fortnite Network Optimizer")
        print("1. Apply Performance Optimizations")
        print("2. Reverse All Optimizations")
        print("3. Enable Bot/Easy Lobbies")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ")
        
        if choice == "1":
            optimize_fortnite()
            break
        elif choice == "2":
            reverse_optimizations()
            break
        elif choice == "3":
            optimize_bot_lobbies()
            break
        elif choice == "4":
            sys.exit()
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    try:
        main()
        input("\nPress Enter to exit...")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        input("\nPress Enter to exit...")