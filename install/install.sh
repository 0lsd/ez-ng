sudo apt update
sudo apt upgrade

cd ..
chmod +x ez-ng.sh
cd uninstall
chmod +x uninstall.sh
cd ..
cd src
chmod +x drblueshutdown.py

sudo apt install python3 -y
sudo apt install python3-tk -y
sudo apt install nmap -y
sudo apt install arp-scan -y
sudo apt install bettercap -y
sudo apt install wireshark -y
sudo apt install tor -y
sudo apt install bluez bluetooth bluez-tools blueman -y
sudo systemctl start bluetooth
sudo systemctl enable bluetoot

sudo apt update
sudo apt upgrade