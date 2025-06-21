#!/usr/bin/env python3
import subprocess, os, sys, datetime

# -- Utility-Funktionen --
def banner():
    print("""
    ╔══════════════════════════════╗
    ║   RABENAUGE - Pentest Suite  ║
    ╚══════════════════════════════╝
    """)

def run(cmd):
    print(f"==> {cmd}")
    subprocess.run(cmd, shell=True)

def report(text):
    with open("rabenauge_report.txt", "a") as f:
        f.write(text + "\n")

# -- Hauptmenü --
def main():
    banner()
    while True:
        print("""
        [1] Netzwerk-Scan (nmap)
        [2] Port-Scan (masscan)
        [3] Web-Scan (nikto & dirb)
        [4] Traffic-Mitschnitt (tcpdump)
        [5] Schwachstellen-Check (searchsploit)
        [6] Subdomain-Scan (assetfinder)
        [7] Alles automatisch ausführen
        [8] Beenden
        """)
        wahl = input("Wähle die Nummer: ").strip()
        if wahl == "1":
            ziel = input("Target IP/Subnet: ")
            run(f"nmap -A -oN nmap_scan.txt {ziel}")
            report(f"Nmap Scan durchgeführt auf {ziel} ({datetime.datetime.now()})")
        elif wahl == "2":
            ziel = input("Target IP/Subnet: ")
            ports = input("Ports (z.B. 1-65535): ")
            run(f"masscan {ziel} -p{ports} --rate=1000 -oL masscan_scan.txt")
            report(f"Masscan durchgeführt auf {ziel}:{ports} ({datetime.datetime.now()})")
        elif wahl == "3":
            url = input("Web-URL: ")
            run(f"nikto -h {url} -output nikto_scan.txt")
            run(f"dirb {url} > dirb_scan.txt")
            report(f"Web-Scan auf {url} ({datetime.datetime.now()})")
        elif wahl == "4":
            iface = input("Interface (z.B. eth0): ")
            run(f"timeout 30 tcpdump -i {iface} -w traffic.pcap")
            report(f"Traffic-Mitschnitt für 30s auf {iface} ({datetime.datetime.now()})")
        elif wahl == "5":
            pfad = input("Pfad zu nmap/dirb output: ")
            run(f"searchsploit --nmap {pfad}")
            report(f"Schwachstellen-Check auf Basis von {pfad} ({datetime.datetime.now()})")
        elif wahl == "6":
            domain = input("Domain: ")
            run(f"assetfinder --subs-only {domain} > subdomains.txt")
            report(f"Subdomainscan auf {domain} ({datetime.datetime.now()})")
        elif wahl == "7":
            ziel = input("Target IP/Subnet: ")
            url = input("Web-URL: ")
            iface = input("Interface (z.B. eth0): ")
            run(f"nmap -A -oN nmap_scan.txt {ziel}")
            run(f"masscan {ziel} -p1-65535 --rate=1000 -oL masscan_scan.txt")
            run(f"nikto -h {url} -output nikto_scan.txt")
            run(f"dirb {url} > dirb_scan.txt")
            run(f"timeout 30 tcpdump -i {iface} -w traffic.pcap")
            run(f"searchsploit --nmap nmap_scan.txt")
            report(f"ALL-IN-ONE Scan auf {ziel}, {url}, {iface} ({datetime.datetime.now()})")
        elif wahl == "8":
            print("Auf bald, dunkler Ritter der Ports!")
            sys.exit(0)
        else:
            print("Ungültige Auswahl, versuch's nochmal.")

if __name__ == "__main__":
    main()
