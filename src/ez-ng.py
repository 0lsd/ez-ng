import tkinter as tk
from tkinter import ttk
import subprocess
import os
from datetime import datetime


def run_command(command):
    output.config(state="normal")
    output.delete("1.0", "end")
    output.insert("end", subprocess.check_output(command, text=True))
    output.config(state="disabled")


def scan():
    run_command(["nmcli", "device", "wifi", "list"])


def nmap():
    run_command(["sudo", "nmap", "-sn", ip.get()])


def arp():
    run_command(["arp"])


def ip_route():
    run_command(["ip", "route"])


def wifi_connect():
    run_command(["nmcli", "device", "wifi", "connect", bssid.get()])


def wifi_disconnect():
    run_command(["nmcli", "device", "disconnect", "wlo1"])


def copy_output():
    root.clipboard_clear()
    root.clipboard_append(output.get("1.0", "end-1c"))
    root.update()


def open_terminal():
    subprocess.Popen(["x-terminal-emulator"])


def open_wireshark():
    subprocess.Popen(["sudo", "wireshark"])


def save_note():
    filename = datetime.now().strftime("ezng-report_%Y-%m-%d-%H-%M-%S.txt")
    
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    reports_dir = os.path.join(parent_dir, "reports")
    os.makedirs(reports_dir, exist_ok=True)
    
    full_path = os.path.join(reports_dir, filename)
    
    with open(full_path, "w", encoding="utf-8") as file:
        file.write(note.get("1.0", "end-1c"))


def bettercap():
    target_ip = bettercap_ip.get()

    script = f"""sudo bettercap iface wlan0
net.probe on
net.show
set arp.spoof.fullduplex true
set arp.spoof.targets {target_ip}
arp.spoof on
net.sniff on
"""

    subprocess.Popen([
        "x-terminal-emulator",
        "-e",
        "bash",
        "-c",
        f"echo '{script}' | bash; exec bash"
    ])


def monitor_on():

    script = f"""sudo ip link set wlo1 down
sudo iw dev wlo1 set type monitor
sudo ip link set wlo1 up
sudo iw dev wlo1 info
"""

    subprocess.Popen([
        "x-terminal-emulator",
        "-e",
        "bash",
        "-c",
        f"echo '{script}' | bash; exec bash"
    ])


def monitor_off():

    script = f"""sudo ip link set wlo1 down
sudo iw dev wlo1 set type managed
sudo ip link set wlo1 up
sudo iw dev wlo1 info
"""

    subprocess.Popen([
        "x-terminal-emulator",
        "-e",
        "bash",
        "-c",
        f"echo '{script}' | bash; exec bash"
    ])


root = tk.Tk()
root.title("Easy Networking Gui")

button_size = {"width": 16, "height": 1}


tabs = ttk.Notebook(root)
tabs.pack(fill="both", expand=True)


net = tk.Frame(tabs)
tabs.add(net, text="Network")

controls = tk.Frame(net)
controls.pack(side="left", anchor="nw")


tk.Button(
    controls,
    text="scan wifi",
    command=scan,
    **button_size
).pack(anchor="w")

tk.Button(
    controls,
    text="ip route",
    command=ip_route,
    **button_size
).pack(anchor="w")

tk.Button(
    controls,
    text="arp",
    bg="#ff9999",
    command=arp,
    **button_size
).pack(anchor="w")


row = tk.Frame(controls)
row.pack(anchor="w")

tk.Button(
    row,
    text="nmap scan",
    bg="#ff9999",
    command=nmap,
    **button_size
).pack(side="left")


ip = tk.Entry(row)
ip.pack(side="left")


wifi_row = tk.Frame(controls)
wifi_row.pack(anchor="w")

tk.Button(
    wifi_row,
    text="wifi connect",
    command=wifi_connect,
    **button_size
).pack(side="left")


bssid = tk.Entry(wifi_row)
bssid.pack(side="left")

tk.Button(
    controls,
    text="wifi disconnect",
    command=wifi_disconnect,
    **button_size
).pack(anchor="w")

tk.Button(
    controls,
    text="wireshark",
    bg="#add8e6",
    command=open_wireshark,
    **button_size
).pack(anchor="w")


bettercap_row = tk.Frame(controls)
bettercap_row.pack(anchor="w")

tk.Button(
    bettercap_row,
    text="sniff",
    bg="#add8e6",
    command=bettercap,
    **button_size
).pack(side="left")


bettercap_ip = tk.Entry(bettercap_row)
bettercap_ip.pack(side="left")

tk.Button(
    controls,
    text="copy output",
    command=copy_output,
    **button_size
).pack(anchor="w")

tk.Button(
    controls,
    text="terminal",
    command=open_terminal,
    **button_size
).pack(anchor="w")


monitor_row = tk.Frame(controls)
monitor_row.pack(anchor="w")

tk.Button(
    monitor_row,
    text="monitor on",
    bg="#99ffaa",
    command=monitor_on,
    **button_size
).pack(side="left")

tk.Button(
    monitor_row,
    text="monitor off",
    bg="#ff9999",
    command=monitor_off,
    **button_size
).pack(side="left")



output = tk.Text(net, state="disabled")
output.pack(fill="both", expand=True)

notepad_frame = tk.Frame(tabs)
tabs.add(notepad_frame, text="Notepad")

note = tk.Text(notepad_frame)
note.pack(fill="both", expand=True)

tk.Button(
    notepad_frame,
    text="Download",
    bg="#99ff99",
    command=save_note,
    **button_size
).pack(anchor="w")


root.mainloop()
