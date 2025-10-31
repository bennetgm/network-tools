import yaml
from ping3 import ping
from datetime import datetime
import os

def load_devices():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base_dir, "devices.yaml")
    with open(path) as f:
        return yaml.safe_load(f)["devices"]

def check_status(device):
    latency = ping(device["ip"], timeout=1)
    status = "Up" if latency else "Down"
    return {
        "name": device["name"],
        "ip": device["ip"],
        "status": status,
        "latency": round(latency*1000, 2) if latency else None,
        "time": datetime.now().strftime("%H:%M:%S")
    }

def poll_all():
    devices = load_devices()
    results = [check_status(d) for d in devices]
    return results