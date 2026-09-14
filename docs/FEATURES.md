*FEATURES*

-----------------------------------

**NETWORK**

1. 'scan wifi' button
    run_command(["nmcli", "device", "wifi", "list"])

2. 'ip route' button
    run_command(["ip", "route"])

3. 'arp' button
    run_command(["arp"])

4. 'nmap scan' button
    run_command(["sudo", "nmap", "-sn", ip.get()])

5. 'wifi connect' button
    run_command(["nmcli", "device", "wifi", "connect", bssid.get()])

6. 'wifi disconnect' button
    run_command(["nmcli", "device", "disconnect", "wlo1"])

7. 'wireshark' button
    subprocess.Popen(["sudo", "wireshark"])

8. 'sniff' button
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

9. 'copy output' button
    root.clipboard_clear()
    root.clipboard_append(output.get("1.0", "end-1c"))
    root.update()

10. 'terminal' button
    subprocess.Popen(["x-terminal-emulator"])

11. 'monitor on' button
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

12. 'monitor off' button
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

**NOTEPAD**

1. 'download" button
    filename = datetime.now().strftime("ezng-report_%Y-%m-%d-%H-%M-%S.txt")
    
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    reports_dir = os.path.join(parent_dir, "reports")
    os.makedirs(reports_dir, exist_ok=True)
    
    full_path = os.path.join(reports_dir, filename)
    
    with open(full_path, "w", encoding="utf-8") as file:
        file.write(note.get("1.0", "end-1c"))

**MORE**

1. 'tor services on' button
    subprocess.Popen(["sudo", "systemctl", "enable", "--now", "tor"])

2. 'tor services off' button
    subprocess.Popen(["sudo", "systemctl", "disable", "--now", "tor"])

3. 'TOR STATUS'
    result = subprocess.run(
        ["systemctl", "is-active", "--quiet", "tor"]
    )
    
    if result.returncode == 0:
        tor_status.config(text="TOR STATUS", fg="#00ff00")
    else:
       tor_status.config(text="TOR STATUS", fg="#ff0000")
    
    root.after(1000, update_tor_status)