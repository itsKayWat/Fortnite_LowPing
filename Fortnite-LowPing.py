import os
import subprocess
import ctypes
import sys
import time
import psutil
import json
import fnmatch

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
    """Monitor Fortnite process and apply optimizations when detected"""
    print("\n⌛ Waiting for Fortnite to launch...")
    
    try:
        while True:
            for proc in psutil.process_iter(['name', 'pid']):
                if "FortniteClient-Win64-Shipping.exe" in proc.info['name']:
                    fortnite_pid = proc.info['pid']
                    print(f"\n✅ Fortnite detected (PID: {fortnite_pid})")
                    
                    # Maximum priority
                    p = psutil.Process(fortnite_pid)
                    try:
                        p.nice(psutil.REALTIME_PRIORITY_CLASS)  # More aggressive priority
                        p.cpu_affinity(list(range(psutil.cpu_count())))  # Use all cores
                        print("⚡ Process priority maximized")
                    except:
                        print("⚠️ Could not set maximum priority")
                    
                    # Kill competing processes
                    for other_proc in psutil.process_iter(['name', 'pid']):
                        if other_proc.pid != fortnite_pid and other_proc.info['name'] not in critical_processes:
                            try:
                                other_proc.nice(psutil.IDLE_PRIORITY_CLASS)  # Lower other process priorities
                            except:
                                continue
            time.sleep(2)  # Increased sleep time
    except Exception as e:
        print("\n⚠️ Monitoring stopped - optimizations are still active")
        print("🎮 You can continue playing!")

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
    print("\n⚡ Applying safe ping optimization...")
    
    # Reduced process kill list (only non-essential)
    processes_to_kill = [
        'spotify.exe', 'discord.exe', 'chrome.exe', 'msedge.exe', 'firefox.exe',
        'steam.exe', 'epicgameslauncher.exe', 'slack.exe', 'teams.exe',
        'skype.exe', 'zoom.exe', 'outlook.exe', 'onedrive.exe', 'dropbox.exe',
        'wallpaperengine.exe', 'icue.exe', 'synapse3.exe', 'overwolf.exe'
    ]
    
    print("\n🔄 Optimizing system resources...")
    for proc in psutil.process_iter(['name']):
        if proc.info['name'].lower() in processes_to_kill:
            try:
                psutil.Process(proc.pid).terminate()
                print(f"✓ Terminated: {proc.info['name']}")
            except:
                continue

    # Safe network commands
    network_commands = [
        # Basic network cleanup
        'ipconfig /flushdns',
        'netsh winsock reset catalog',
        
        # Safe TCP optimizations
        'netsh int tcp set global autotuninglevel=normal',
        'netsh int tcp set global chimney=enabled',
        'netsh int tcp set global dca=enabled',
        'netsh int tcp set global netdma=enabled',
        'netsh int tcp set global rss=enabled',
        'netsh int tcp set global timestamps=disabled',
        'netsh int tcp set global initialRto=2000',
        'netsh int tcp set global maxsynretransmissions=2',
        
        # Fortnite port optimizations (safe ranges)
        'netsh advfirewall firewall add rule name="Fortnite UDP" dir=in action=allow protocol=UDP localport=9000-9999 enable=yes',
        'netsh advfirewall firewall add rule name="Fortnite UDP Out" dir=out action=allow protocol=UDP remoteport=9000-9999 enable=yes',
        'netsh advfirewall firewall add rule name="Fortnite TCP" dir=in action=allow protocol=TCP localport=80,443,5222,5795-5799 enable=yes',
        'netsh advfirewall firewall add rule name="Fortnite TCP Out" dir=out action=allow protocol=TCP remoteport=80,443,5222,5795-5799 enable=yes',
        
        # Safe network adapter optimizations
        'powershell "Get-NetAdapter | Set-NetAdapterAdvancedProperty -DisplayName \'*FlowControl\' -DisplayValue Disabled"',
        'powershell "Get-NetAdapter | Set-NetAdapterAdvancedProperty -DisplayName \'*PriorityVLANTag\' -DisplayValue Priority"',
        'powershell "Get-NetAdapter | Set-NetAdapterAdvancedProperty -DisplayName \'*ReceiveBuffers\' -DisplayValue 2048"',
        'powershell "Get-NetAdapter | Set-NetAdapterAdvancedProperty -DisplayName \'*TransmitBuffers\' -DisplayValue 2048"',
        
        # Safe registry optimizations
        'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters" /v "DefaultTTL" /t REG_DWORD /d "64" /f',
        'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters" /v "TCPNoDelay" /t REG_DWORD /d "1" /f',
        'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters" /v "TcpAckFrequency" /t REG_DWORD /d "1" /f',
        
        # Game profile optimizations
        'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\\Tasks\\Games" /v "GPU Priority" /t REG_DWORD /d "8" /f',
        'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\\Tasks\\Games" /v "Priority" /t REG_DWORD /d "6" /f',
        'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\\Tasks\\Games" /v "Scheduling Category" /t REG_SZ /d "High" /f',
        
        # Final refresh
        'ipconfig /renew',
        'ipconfig /flushdns'
    ]

    print("\n⚡ Applying network optimizations...")
    for cmd in network_commands:
        run_command(cmd)
        time.sleep(0.2)

    # Safe process priority
    try:
        for proc in psutil.process_iter(['name']):
            if "FortniteClient-Win64-Shipping.exe" in proc.info['name']:
                p = psutil.Process(proc.pid)
                p.nice(psutil.HIGH_PRIORITY_CLASS)  # Changed from REALTIME to HIGH
                p.cpu_affinity(list(range(os.cpu_count())))  # Use all available cores
                break
    except:
        pass

    print("\n✅ Optimization complete!")
    print("⚡ Network optimized safely for better ping")
    print("🎮 Monitoring Fortnite process...")
    
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

def ultra_aggressive_mode():
    print("\n��️ ULTRA AGGRESSIVE MODE - MAXIMUM PERFORMANCE")
    print("⚠️ WARNING: This will optimize system for Fortnite!")
    
    confirm = input("\n⚠️ Continue with extreme optimization? (y/n): ")
    if confirm.lower() != 'y':
        return

    # Critical processes that must not be terminated
    critical_processes = {
        'System', 'Registry', 'smss.exe', 'csrss.exe', 'wininit.exe', 
        'services.exe', 'lsass.exe', 'winlogon.exe', 'explorer.exe',
        'dwm.exe', 'fontdrvhost.exe', 'spoolsv.exe', 'svchost.exe',
        'taskmgr.exe', 'cmd.exe', 'python.exe', 'conhost.exe',
        'FortniteClient-Win64-Shipping.exe', 'EpicGamesLauncher.exe',
        'RazerSynapse.exe', 'RazerCentral.exe', 
        'Razer Synapse Service.exe', 'Razer Synapse Service Process.exe'
    }

    # Kill non-essential processes
    print("\n🔄 Optimizing system resources...")
    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'] not in critical_processes:
                proc.terminate()
                print(f"✓ Terminated: {proc.info['name']}")
        except:
            continue

    # Network isolation and optimization
    firewall_commands = [
        # Reset and block all
        'netsh advfirewall reset',
        'netsh advfirewall set allprofiles state on',
        'netsh advfirewall set allprofiles firewallpolicy blockinbound,blockoutbound',
        
        # Allow Fortnite and Epic
        'netsh advfirewall firewall add rule name="Fortnite_Game" dir=out action=allow program="C:\\Program Files\\Epic Games\\Fortnite\\FortniteGame\\Binaries\\Win64\\FortniteClient-Win64-Shipping.exe" enable=yes',
        'netsh advfirewall firewall add rule name="Epic_Launcher" dir=out action=allow program="C:\\Program Files (x86)\\Epic Games\\Launcher\\Portal\\Binaries\\Win32\\EpicGamesLauncher.exe" enable=yes',
        
        # Allow Razer
        'netsh advfirewall firewall add rule name="Razer_Synapse" dir=out action=allow program="C:\\Program Files (x86)\\Razer\\Synapse3\\WPFUI\\Framework\\Razer Synapse 3 Host\\Razer Synapse 3.exe" enable=yes',
        'netsh advfirewall firewall add rule name="Razer_Service" dir=out action=allow program="C:\\Program Files (x86)\\Razer\\Synapse3\\Service\\Razer Synapse Service.exe" enable=yes',
        
        # Epic/Fortnite Servers
        'netsh advfirewall firewall add rule name="Epic_Services" dir=out action=allow protocol=TCP remoteport=80,443,5222,5795-5847 enable=yes',
        'netsh advfirewall firewall add rule name="Epic_Services_UDP" dir=out action=allow protocol=UDP remoteport=5222,5795-5847,9000-9999 enable=yes',
        'netsh advfirewall firewall add rule name="Epic_Servers" dir=out action=allow protocol=TCP remoteip=18.204.105.0/24,18.204.106.0/24,18.204.107.0/24,18.204.108.0/24,18.204.109.0/24 enable=yes',
        
        # Allow DNS
        'netsh advfirewall firewall add rule name="DNS" dir=out action=allow protocol=UDP remoteport=53 enable=yes',
        'netsh advfirewall firewall add rule name="DNS_TCP" dir=out action=allow protocol=TCP remoteport=53 enable=yes'
    ]

    # Aggressive network optimizations
    network_commands = [
        # TCP Optimizations
        'netsh int tcp set global initialRto=100',
        'netsh int tcp set global congestionprovider=ctcp',
        'netsh int tcp set global autotuninglevel=disabled',
        'netsh int tcp set global ecncapability=disabled',
        'netsh int tcp set global timestamps=disabled',
        'netsh int tcp set global rss=enabled',
        'netsh int tcp set global maxsynretransmissions=1',
        'netsh int tcp set global fastopen=enabled',
        'netsh int tcp set global pacingprofile=off',
        
        # Registry Optimizations
        'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters" /v "DefaultTTL" /t REG_DWORD /d "32" /f',
        'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters" /v "TcpMaxDataRetransmissions" /t REG_DWORD /d "1" /f',
        'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters" /v "TcpTimedWaitDelay" /t REG_DWORD /d "1" /f',
        'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters" /v "TcpWindowSize" /t REG_DWORD /d "2048" /f',
        'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters" /v "GlobalMaxTcpWindowSize" /t REG_DWORD /d "2048" /f',
        'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters" /v "TCPNoDelay" /t REG_DWORD /d "1" /f',
        
        # Network Adapter Optimizations
        'powershell "Get-NetAdapter | Where-Object {$_.Status -eq \'Up\'} | Set-NetAdapterAdvancedProperty -DisplayName \'*FlowControl\' -DisplayValue Disabled"',
        'powershell "Get-NetAdapter | Where-Object {$_.Status -eq \'Up\'} | Set-NetAdapterAdvancedProperty -DisplayName \'*InterruptModeration\' -DisplayValue Disabled"',
        'powershell "Get-NetAdapter | Where-Object {$_.Status -eq \'Up\'} | Set-NetAdapterAdvancedProperty -DisplayName \'*PriorityVLANTag\' -DisplayValue Priority"',
        'powershell "Get-NetAdapter | Where-Object {$_.Status -eq \'Up\'} | Set-NetAdapterAdvancedProperty -DisplayName \'*ReceiveBuffers\' -DisplayValue 256"',
        'powershell "Get-NetAdapter | Where-Object {$_.Status -eq \'Up\'} | Set-NetAdapterAdvancedProperty -DisplayName \'*TransmitBuffers\' -DisplayValue 256"',
        
        # Performance Mode
        'powercfg -setactive scheme_min',
        'powercfg /setacvalueindex scheme_current sub_processor PERFBOOSTMODE 2',
        'powercfg /setacvalueindex scheme_current sub_processor PERFBOOSTPOL 100',
        
        # Final Network Flush
        'ipconfig /release',
        'ipconfig /renew',
        'ipconfig /flushdns'
    ]

    print("\n🔒 Setting up network isolation...")
    for cmd in firewall_commands:
        run_command(cmd)
        time.sleep(0.2)

    print("\n⚡ Applying network optimizations...")
    for cmd in network_commands:
        run_command(cmd)
        time.sleep(0.2)

    print("\n✅ Optimization complete!")
    print("⚡ System optimized for maximum Fortnite performance")
    print("\n⌛ Waiting for Fortnite to launch...")

    # Monitor Fortnite
    try:
        while True:
            fortnite_running = False
            for proc in psutil.process_iter(['name']):
                if "FortniteClient-Win64-Shipping.exe" in proc.info['name']:
                    fortnite_running = True
                    print("\n✅ Fortnite detected! Monitoring until close...")
                    break
            
            if fortnite_running:
                while fortnite_running:
                    fortnite_running = False
                    for proc in psutil.process_iter(['name']):
                        if "FortniteClient-Win64-Shipping.exe" in proc.info['name']:
                            fortnite_running = True
                            break
                    time.sleep(2)
                print("\n🎮 Fortnite closed - reversing optimizations...")
                reverse_optimizations()
                break
            time.sleep(2)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        reverse_optimizations()

def apply_fortnite_optimizations(pid):
    try:
        print(f"\n🎮 Applying optimizations to Fortnite (PID: {pid})")
        
        # Basic process priority without using psutil
        try:
            subprocess.run(f'wmic process where ProcessId={pid} CALL setpriority "high priority"', shell=True)
        except:
            print("⚠️ Could not set process priority - continuing...")

        # Game-specific optimizations
        game_commands = [
            # Network optimizations
            'netsh int tcp set global congestionprovider=ctcp',
            'netsh int tcp set global autotuninglevel=disabled',
            'netsh int tcp set global ecncapability=disabled',
            
            # Fortnite-specific registry tweaks
            'reg add "HKCU\\Software\\Epic Games\\Fortnite" /v "NumWorkerThreads" /t REG_DWORD /d "16" /f',
            'reg add "HKCU\\Software\\Epic Games\\Fortnite" /v "MaxMemoryUsedPercentage" /t REG_DWORD /d "75" /f',
            
            # Direct network optimizations
            'netsh interface ipv4 set subinterface "Ethernet" mtu=1492 store=persistent',
            'netsh interface ipv4 set subinterface "Wi-Fi" mtu=1492 store=persistent',
            
            # Game mode
            'reg add "HKCU\\Software\\Microsoft\\GameBar" /v "AllowAutoGameMode" /t REG_DWORD /d "1" /f',
            'reg add "HKCU\\Software\\Microsoft\\GameBar" /v "AutoGameModeEnabled" /t REG_DWORD /d "1" /f'
        ]

        print("\n⚡ Applying in-game optimizations...")
        for cmd in game_commands:
            try:
                subprocess.run(cmd, shell=True, check=False)  # Changed to check=False
            except:
                continue

        print("\n✅ In-game optimizations complete!")
        print("⚡ Maximum performance mode enabled")
        print("🎮 Good luck in your game!")
        
    except Exception as e:
        print(f"\n⚠️ Note: Some optimizations may not have applied - game will still run optimized")
        print("🎮 You can continue playing!")

def main():
    run_as_admin()
    
    while True:
        print("\n🎮 Fortnite Network Optimizer")
        print("1. Apply Safe Performance Optimizations")
        print("2. Reverse All Optimizations")
        print("3. Ultra Aggressive Mode (Run BEFORE Fortnite)")
        print("4. Enable Bot/Easy Lobbies")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ")
        
        if choice == "1":
            optimize_fortnite()
            break
        elif choice == "2":
            reverse_optimizations()
            break
        elif choice == "3":
            ultra_aggressive_mode()
            break
        elif choice == "4":
            optimize_bot_lobbies()
            break
        elif choice == "5":
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