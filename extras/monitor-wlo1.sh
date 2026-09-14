sudo apt update

sudo ip link set wlo1 down
sudo iw dev wlo1 set type monitor
sudo ip link set wlo1 up
sudo iw dev wlo1 info