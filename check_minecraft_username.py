import requests
import sys
from datetime import datetime, UTC
import os
from dotenv import load_dotenv
import time
import argparse
from win10toast import ToastNotifier
import subprocess

# Try to load environment variables, continue if .env doesn't exist
try:
    load_dotenv()
except Exception:
    pass

class MinecraftUsernameChecker:
    def __init__(self, username, check_interval=10):
        self.username = username
        self.check_interval = check_interval
        self.last_status = None
        self.webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
        
        if not self.webhook_url:
            print("ℹ️ Discord webhook not configured. Only Windows notifications will be used.")
            print("   To enable Discord notifications, create a .env file with DISCORD_WEBHOOK_URL=your_webhook_url\n")

    def check_username_availability(self):
        if not self.username.strip():
            return None, "Empty username"
            
        url = f"https://api.mojang.com/users/profiles/minecraft/{self.username}"
        
        try:
            response = requests.get(url)
            
            if response.status_code == 204 or response.status_code == 404:
                return True, f"Username '{self.username}' is available! 🎮"
            elif response.status_code == 200:
                return False, f"Username '{self.username}' is already taken. ❌"
            else:
                return None, f"Error during check. Error code: {response.status_code}"
                
        except requests.exceptions.RequestException as e:
            return None, f"Connection error: {e}"

    def send_windows_notification_and_note(self):
        # Create Windows notification
        toaster = ToastNotifier()
        toaster.show_toast(
            "Minecraft Username Available!",
            f"The username {self.username} is available!",
            duration=10,
            threaded=True
        )
        
        # Create notepad content
        note_content = f"""Minecraft username available: {self.username}

Link to change your username:
https://www.minecraft.net/msaprofile/mygames/editprofile

Check timestamp: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"""
        
        # Create notepad file
        note_path = os.path.join(os.path.expanduser("~"), "Desktop", f"minecraft_username_{self.username}.txt")
        with open(note_path, "w", encoding="utf-8") as f:
            f.write(note_content)
        
        # Open notepad
        subprocess.Popen(["notepad.exe", note_path])

    def send_discord_notification(self, is_available):
        if is_available and (self.last_status is None or not self.last_status):
            # Always send Windows notification, even if Discord is not configured
            self.send_windows_notification_and_note()
            
            # Skip Discord notification if webhook is not configured
            if not self.webhook_url:
                return

            embed = {
                "title": "Minecraft Username Available! 🎮",
                "description": f"The username **{self.username}** is now available!",
                "color": 5763719,  # Green
                "timestamp": datetime.now(UTC).isoformat()
            }
            
            data = {
                "content": "🎯 Availability Alert!",
                "embeds": [embed]
            }
            
            try:
                response = requests.post(self.webhook_url, json=data)
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                print(f"Error sending Discord notification: {e}")

    def run(self):
        ascii_art = """
███╗   ███╗ ██████╗██╗   ██╗███████╗
████╗ ████║██╔════╝██║   ██║██╔════╝
██╔████╔██║██║     ██║   ██║███████╗
██║╚██╔╝██║██║     ██║   ██║╚════██║
██║ ╚═╝ ██║╚██████╗╚██████╔╝███████║
╚═╝     ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝
        Minecraft Username Sniper
"""
        print(ascii_art)

        if not self.webhook_url:
            print("⚠️  Warning: Discord webhook not configured. Only Windows notifications will be used.")
            print("             To enable Discord notifications, create a .env file with DISCORD_WEBHOOK_URL=your_webhook_url\n")

        print(f"🔍 Starting monitoring for username '{self.username}'")
        print(f"⏱️  Check interval: {self.check_interval} seconds")
        print("📡 Press Ctrl+C to stop\n")
        
        try:
            while True:
                status, message = self.check_username_availability()
                current_time = datetime.now().strftime("%H:%M:%S")
                
                # If status changed or first check
                if status != self.last_status:
                    print(f"[{current_time}] {message}")
                    self.send_discord_notification(status)
                    self.last_status = status
                else:
                    print(f"[{current_time}] No status change")
                
                time.sleep(self.check_interval)
                
        except KeyboardInterrupt:
            print("\n👋 Monitoring stopped")
            sys.exit(0)

def main():
    parser = argparse.ArgumentParser(description="Minecraft Username Checker")
    parser.add_argument("--username", type=str, required=True, help="Username to check")
    parser.add_argument("--interval", type=int, default=10, help="Check interval in seconds (default: 10)")
    args = parser.parse_args()

    checker = MinecraftUsernameChecker(args.username, args.interval)
    checker.run()

if __name__ == "__main__":
    main() 