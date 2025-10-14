# Network Tools

This repo is just a collection of small networking projects I’ve been doing while learning Python and networking basics.

## Current Project
### Python Packet Sniffer
A simple packet sniffer that listens on a network interface and counts packets by protocol (TCP, UDP, ICMP etc).  
It uses Scapy to capture traffic and Matplotlib to show a live graph of what’s happening.

### How to Run
Make sure you have Python 3 and install:
```
pip install scapy matplotlib
```

Then run (you might need sudo/Admin on some systems):
```
sudo python3 packet_sniffer.py
```

Add `--no-gui` if you don’t want the graph and just want console output.

## Notes
Still learning how to improve this. Might later add a dashboard or connect it to my intrusion detection project.
