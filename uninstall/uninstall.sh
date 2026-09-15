sudo apt update
sudo apt upgrade

cd ..
cd ..
sudo rm -rf ez-ng
cd ~

sudo apt remove python3-tk -y
sudo apt remove nmap -y
sudo apt remove arp-scan -y
sudo apt remove bettercap -y
sudo apt remove wireshark -y
sudo apt remove tor -y
sudo apt autoremove -y

sudo apt update
sudo apt upgrade