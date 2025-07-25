import time
import subprocess
import os
from SX127x.LoRa import LoRa, MODE
from SX127x.board_config import BOARD

BOARD.setup()

def show_ascii(name):
    path = f'ascii/{name}.txt'  # <-- Added .txt extension here
    try:
        with open(path, 'r') as file:
            print(file.read())
    except FileNotFoundError:
        print(f"[ERROR] ASCII art file '{path}' not found.")

def show_banner():
    try:
        with open("ascii/ghostshell_banner.txt", "r") as banner:  # <-- .txt extension here too
            print(banner.read())
    except FileNotFoundError:
        print("[BANNER] LoRa GHOSTSHELL startup banner not found.")

def check_payload():
    path = 'commands/td_script.py'
    if os.path.exists(path):
        show_ascii('payload_detected.txt')
    else:
        print("[STATUS] No payload found.")

def execute_payload(script):
    show_ascii('tango_delta.txt')
    subprocess.call(["python3", f"./commands/{script}"])

class LoRaListener(LoRa):
    def __init__(self):
        super().__init__(verbose=False)
        self.set_mode(MODE.SLEEP)
        self.set_freq(915.0)
        self.set_coding_rate(5)
        self.set_pa_config(pa_select=1)

    def on_rx_done(self):
        self.clear_irq_flags(RxDone=1)
        payload = self.read_payload(nocheck=True).decode('utf-8').strip()
        print(f"\n[LoRa] Command Received: {payload}")
        self.set_mode(MODE.STDBY)

        if payload == 'CMD:CONNECT':
            show_ascii('connected.txt')

        elif payload == 'CMD:STATUS':
            check_payload()

        elif payload == 'CMD:TD':
            execute_payload('td_script.py')
	    show_ascii(tango_delta.txt)
        elif payload == 'CMD:DISCONNECT':
            show_ascii('disconnected.txt')

        else:
            print(f"[WARNING] Unknown command: {payload}")

        self.set_mode(MODE.RXCONT)

if __name__ == '__main__':
    show_banner()
    lora = LoRaListener()
    lora.set_mode(MODE.RXCONT)
    print("[LoRa] Listening for commands...")
    while True:
        time.sleep(0.5)