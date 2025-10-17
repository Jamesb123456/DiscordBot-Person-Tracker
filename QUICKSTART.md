# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Configure Bot
1. Copy `.env.example` to `.env`
2. Get your Discord bot token from [Discord Developer Portal](https://discord.com/developers/applications)
3. Get your channel ID (Right-click channel → Copy ID)
4. Fill in `.env`:
```env
DISCORD_BOT_TOKEN=your_bot_token_here
FIVEM_SERVER_ID=javxzp
UPDATE_CHANNEL_ID=your_channel_id_here
```

### Step 3: Run Bot
**Windows:**
```bash
start.bat
```

**Linux/Mac:**
```bash
python bot.py
```

### Step 4: Add Players
In Discord, use the `/set` command:
```
/set "Richard Payne" "Richard Payne"
/set "Wu Jackson" "Wu Jackson"
```

Done! The bot will now update every 10 minutes. ✅

## 📝 Command Cheat Sheet

| Command | Description | Example |
|---------|-------------|---------|
| `/set <fivem_name> <nickname>` | Add/update player | `/set "John Doe" "Johnny"` |
| `/remove <fivem_name>` | Remove player | `/remove "John Doe"` |
| `/list` | Show all tracked players | `/list` |
| `/refresh` | Force immediate update | `/refresh` |

## ⚠️ Common Issues

**Bot not responding?**
- Enable "Message Content Intent" in Discord Developer Portal → Bot section
- Make sure bot has permissions: Send Messages, Embed Links, Use Slash Commands

**Players not showing online?**
- FiveM names must match exactly (check server player list)
- Use `/list` to verify saved names

**Can't get Channel ID?**
- Enable Developer Mode: Discord Settings → Advanced → Developer Mode
- Right-click channel → Copy ID

## 🎯 Example Workflow

1. **Initial Setup**
   ```
   /set "Richard Payne" "Richard Payne"
   /set "Wu Jackson" "Wu Jackson"
   /set "Jose Badid" "Jose Badid"
   ```

2. **Verify Setup**
   ```
   /list
   /refresh
   ```

3. **Monitor**
   - Bot automatically updates every 10 minutes
   - Check the status channel for live updates

4. **Manage Players**
   ```
   /set "NewPlayer" "New"  → Add player
   /remove "OldPlayer"      → Remove player
   ```

## 📱 Discord Bot Setup (Detailed)

### Create Application
1. Go to https://discord.com/developers/applications
2. Click "New Application"
3. Name it (e.g., "FiveM Player Tracker")

### Configure Bot
1. Click "Bot" in left sidebar
2. Click "Add Bot"
3. Copy token (you'll need this)
4. Enable "Message Content Intent"

### Invite to Server
1. Click "OAuth2" → "URL Generator"
2. Check scopes: `bot`, `applications.commands`
3. Check permissions: `Send Messages`, `Embed Links`, `Read Message History`, `Use Slash Commands`
4. Copy URL and open in browser
5. Select your server

### Get Channel ID
1. Open Discord
2. Settings → Advanced → Enable Developer Mode
3. Right-click your desired channel
4. Click "Copy ID"
5. Paste into `.env` file

That's it! Your bot is ready to track players. 🎮
