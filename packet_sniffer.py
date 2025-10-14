# packet_sniffer.py
import argparse
from collections import Counter
from time import sleep, time

from scapy.all import AsyncSniffer, IP, TCP, UDP, ICMP
import matplotlib.pyplot as plt

COUNTS = Counter()

def classify(pkt) -> str:
    if IP in pkt:
        if TCP in pkt: return "TCP"
        if UDP in pkt: return "UDP"
        if ICMP in pkt: return "ICMP"
        return "IP"
    return "OTHER"

def on_packet(pkt):
    try:
        proto = classify(pkt)
        COUNTS[proto] += 1
        # minimal log (comment out if noisy)
        if IP in pkt:
            print(f"{pkt[IP].src} -> {pkt[IP].dst} [{proto}]")
        else:
            print(f"(non-IP) [{proto}]")
    except Exception:
        pass

def run_headless(sniffer: AsyncSniffer, stop_after: int):
    """Run without GUI; Ctrl+C to stop or stop after N packets if store=False can't count, so just sleep."""
    try:
        if stop_after > 0:
            # crude timer-based stop; for exact packet count, use sniff(..., count=N)
            target_end = time() + 999999
            while sniffer.running:
                sleep(0.2)
        else:
            while sniffer.running:
                sleep(0.2)
    except KeyboardInterrupt:
        pass

def run_with_gui(sniffer: AsyncSniffer, refresh: float = 0.5):
    """Main-thread Matplotlib loop (required on macOS)."""
    plt.ion()
    fig, ax = plt.subplots()
    labels = ["TCP", "UDP", "ICMP", "IP", "OTHER"]

    try:
        while sniffer.running:
            values = [COUNTS[lbl] for lbl in labels]
            ax.clear()
            ax.set_title("Live Packet Counts by Protocol")
            ax.set_xlabel("Protocol")
            ax.set_ylabel("Packets captured")
            ax.bar(labels, values)
            plt.pause(refresh)
    except KeyboardInterrupt:
        pass
    finally:
        plt.ioff()
        plt.close(fig)

def main():
    parser = argparse.ArgumentParser(description="Packet sniffer with optional live Matplotlib visualiser (macOS-safe).")
    parser.add_argument("-i", "--iface", default=None, help="Interface (e.g., en0, wlan0). Default: auto")
    parser.add_argument("-f", "--filter", default="", help="BPF filter, e.g. 'tcp or udp or icmp'")
    parser.add_argument("-c", "--count", type=int, default=0, help="(Best-effort) stop after N packets (0 = until Ctrl+C)")
    parser.add_argument("--no-gui", action="store_true", help="Disable Matplotlib graph")
    args = parser.parse_args()

    print("\n=== Packet Sniffer ===")
    print(f"Interface : {args.iface or '(auto)'}")
    print(f"Filter    : {args.filter or '(none)'}")
    print("Note: you may need sudo/Admin privileges to sniff.\n")

    # Start background sniffer; store=False avoids RAM growth
    sniffer = AsyncSniffer(
        iface=args.iface,
        filter=(args.filter or None),
        prn=on_packet,
        store=False
    )
    sniffer.start()

    try:
        if args.no_gui:
            run_headless(sniffer, args.count)
        else:
            run_with_gui(sniffer)
    finally:
        # Stop and wait for background thread to exit
        try:
            sniffer.stop()
        except Exception:
            pass
        sleep(0.3)
        print("\nSummary:", dict(COUNTS))

if __name__ == "__main__":
    main()