import time
from SX127x.LoRa import LoRa
from SX127x.board_config import BOARD
from SX127x.constants import MODE  # Make sure MODE is imported

BOARD.setup()

def show_banner():
    try:
        with open("ascii/ghostshell_banner.txt", "r") as banner:
            print(banner.read())
    except FileNotFoundError:
        print("[BANNER] LoRa GHOSTSHELL startup banner not found.")

def show_ascii_art(filename):
    path = f"ascii/{filename}"
    try:
        with open(path, "r") as art:
            print(art.read())
    except FileNotFoundError:
        print(f"[ASCII] Missing ASCII file: {path}")

class LoRaController(LoRa):
    def __init__(self):
        super().__init__(verbose=False)
        self.set_mode(MODE.STDBY)
        self.set_freq(915.0)
        self.set_coding_rate(5)
        self.set_pa_config(pa_select=1)

    def send_command(self, cmd):
        print(f"[SEND] {cmd}")
        self.write_payload([ord(c) for c in cmd])
        self.set_mode(MODE.TX)
        time.sleep(1)
        self.set_mode(MODE.STDBY)

if __name__ == '__main__':
    show_banner()
    lora = LoRaController()

    command_art_map = {
        "CONNECT": "connected.txt",
        "STATUS": "payload_detected.txt",
        "TD": "tango_delta.txt",
        "DISCONNECT": "disconnect.txt"
    }

    while True:
        cmd = input("Enter Command [CONNECT / STATUS / TD / DISCONNECT]: ").upper()
        if cmd in command_art_map:
            show_ascii_art(command_art_map[cmd])
            lora.send_command(f"CMD:{cmd}")
        else:
            print("Invalid Command.")