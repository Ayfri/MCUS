# 🎮 Minecraft Username Checker

A command-line tool to check if a Minecraft username is available, with automatic refresh at customizable intervals.

## 📋 Requirements

1. Make sure you have Python installed on your system
2. Run `execute.bat` or install dependencies manually:

```bash
pip install -r requirements.txt
```

## 🚀 Usage

### 💻 Using execute.bat (Recommended)

You can run the script in two ways:

1. With a username:

```bash
execute.bat desired_username
# Example: execute.bat Notch
```

2. Without arguments (uses last saved username):

```bash
execute.bat
```

The script will:

1. Create a Python virtual environment if needed
2. Install all dependencies
3. Save the username for next use (if provided)
4. Start monitoring the username

### ⌨️ Manual Usage

Run the script with the following arguments:

```bash
python check_minecraft_username.py --username "desired_username" --interval 10
```

Arguments:

- `--username`: The Minecraft username to check (required)
- `--interval`: Check interval in seconds (optional, default: 10)

## ✨ Features

- 🔄 Real-time username availability monitoring
- 🔔 Windows notifications when username becomes available
- 📝 Automatic notepad file creation with:
  - 👤 Available username
  - 🔗 Link to change Minecraft username
  - 🕒 Timestamp
- 🤖 Discord webhook integration (optional)
- ⚠️ Error handling with explicit messages
- 📊 Clean console output with timestamps
- 💾 Username persistence in execute.bat
- 🎨 ASCII art banner

## 🔌 Discord Integration

To enable Discord notifications:

1. Create a `.env` file in the same directory
2. Add your Discord webhook URL:

```
DISCORD_WEBHOOK_URL=your_webhook_url_here
```
