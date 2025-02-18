import time
import os
import sys
import random
from datetime import datetime

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def type_text(text, delay=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

class PortHack:
    def __init__(self):
        self.sequence = []
        self.player_sequence = []
        self.level = 1

    def generate_sequence(self):
        self.sequence = [random.choice(['/', '|', '\\']) for _ in range(3 + self.level)]

    def display_sequence(self):
        print("\nMemorize this sequence:")
        print("".join(self.sequence))
        time.sleep(2)
        clear_screen()

    def get_player_input(self):
        print("\nEnter the sequence using / | \\ characters:")
        return input().strip()

    def check_sequence(self, player_input):
        return player_input == "".join(self.sequence)

class HacknetTutorial:
    def __init__(self):
        self.username = "ASCENSION222222"
        self.connected = False
        self.target_ip = "192.168.0.1"
        self.ports_required = 2
        self.ports_opened = 0
        self.files = {
            "welcome.txt": "Welcome to the terminal! Use 'help' for available commands.",
            "tutorial.txt": "Training sequence initiated.\n1. Open required ports using 'porthack'\n2. Connect to target system\n3. Download target files",
            "mission1.txt": "MISSION OBJECTIVE:\nGain access to local system 192.168.0.1\nRequired ports: 2"
        }
        self.commands = {
            "help": "Show available commands",
            "ls": "List files in current directory",
            "cat": "Read file contents (usage: cat filename)",
            "connect": "Connect to a system (usage: connect IP)",
            "disconnect": "Disconnect from current system",
            "clear": "Clear the screen",
            "porthack": "Attempt to open a port",
            "scan": "Scan target system",
            "scp": "Copy files (when connected)",
            "exit": "Exit terminal"
        }

    def display_ascii_banner(self):
        banner = """
        ╔═══════════════════════════════════════╗
        ║             HACKNET v1.0              ║
        ║      TERMINAL TRAINING PROGRAM        ║
        ╚═══════════════════════════════════════╝
        """
        print(banner)

    def display_connection_animation(self):
        frames = [
            "[    ]",
            "[=   ]",
            "[==  ]",
            "[=== ]",
            "[====]"
        ]
        for frame in frames:
            sys.stdout.write('\r' + frame)
            sys.stdout.flush()
            time.sleep(0.2)
        print()

    def show_prompt(self):
        current_time = datetime.utcnow().strftime("%H:%M:%S")
        if self.connected:
            return f"[{current_time}] {self.username}@{self.target_ip}:~$ "
        return f"[{current_time}] {self.username}@local:~$ "

    def run_porthack(self):
        if self.ports_opened >= self.ports_required:
            print("All required ports are already open!")
            return

        print("\nInitiating Port Hack sequence...")
        time.sleep(1)
        
        porthack = PortHack()
        porthack.generate_sequence()
        
        print("""
        ╔════════════════╗
        ║  PORT HACKING  ║
        ╚════════════════╝
        """)
        
        porthack.display_sequence()
        player_input = porthack.get_player_input()
        
        if porthack.check_sequence(player_input):
            self.ports_opened += 1
            print(f"\nPORT HACK SUCCESSFUL! ({self.ports_opened}/{self.ports_required} ports opened)")
            self.display_progress_bar(self.ports_opened, self.ports_required)
        else:
            print("\nPORT HACK FAILED! Sequence incorrect.")

    def display_progress_bar(self, current, total, width=20):
        percentage = current / total
        filled = int(width * percentage)
        bar = '=' * filled + ' ' * (width - filled)
        print(f"Progress: [{bar}] {int(percentage * 100)}%")

    def scan_system(self):
        print("\nScanning target system...")
        self.display_connection_animation()
        
        print(f"""
        TARGET: {self.target_ip}
        ═══════════════════════
        PORTS REQUIRED: {self.ports_required}
        PORTS OPENED: {self.ports_opened}
        STATUS: {"VULNERABLE" if self.ports_opened >= self.ports_required else "SECURE"}
        """)

    def process_command(self, command):
        if command == "help":
            print("\nAvailable commands:")
            for cmd, desc in self.commands.items():
                print(f"  {cmd:<10} - {desc}")

        elif command == "ls":
            print("\nFiles in current directory:")
            for file in self.files.keys():
                print(f"  {file}")

        elif command.startswith("cat "):
            filename = command[4:]
            if filename in self.files:
                print(f"\nContents of {filename}:")
                type_text(self.files[filename])
            else:
                print(f"Error: File '{filename}' not found.")

        elif command.startswith("connect"):
            if not self.connected:
                if self.ports_opened >= self.ports_required:
                    type_text("\nInitiating connection sequence...", 0.05)
                    self.display_connection_animation()
                    type_text("Connection successful!", 0.05)
                    self.connected = True
                else:
                    print(f"Connection failed! Need to open {self.ports_required} ports first.")
            else:
                print("Already connected!")

        elif command == "disconnect":
            if self.connected:
                type_text("\nDisconnecting...", 0.05)
                self.display_connection_animation()
                type_text("Connection terminated.", 0.05)
                self.connected = False
            else:
                print("Not connected to any system!")

        elif command == "porthack":
            self.run_porthack()

        elif command == "scan":
            self.scan_system()

        elif command == "clear":
            clear_screen()
            self.display_ascii_banner()

        elif command == "exit":
            type_text("\nTerminating session...", 0.05)
            time.sleep(1)
            type_text("Goodbye!", 0.05)
            sys.exit()

        else:
            print(f"Command not recognized: '{command}'. Type 'help' for available commands.")

    def run_tutorial(self):
        clear_screen()
        self.display_ascii_banner()
        type_text("Initializing terminal...", 0.05)
        time.sleep(1)
        type_text("\nWelcome to Advanced Terminal Training Program", 0.03)
        type_text("Type 'help' to see available commands.\n")

        while True:
            command = input(self.show_prompt()).strip().lower()
            self.process_command(command)

def main():
    tutorial = HacknetTutorial()
    
    # Introduction sequence
    clear_screen()
    tutorial.display_ascii_banner()
    type_text("Loading Terminal OS v1.0...", 0.05)
    time.sleep(1)
    type_text("System initialized.", 0.05)
    time.sleep(0.5)
    
    print("\n" + "="*50)
    type_text("ADVANCED TERMINAL TRAINING PROGRAM", 0.03)
    print("="*50 + "\n")
    
    time.sleep(1)
    type_text(f"Welcome, {tutorial.username}!", 0.03)
    type_text("This tutorial will teach you advanced terminal commands.", 0.03)
    type_text("First objective: Type 'cat mission1.txt' to see your mission.\n", 0.03)
    
    tutorial.run_tutorial()

if __name__ == "__main__":
    main()