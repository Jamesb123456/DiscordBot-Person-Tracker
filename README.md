# 🎮 FiveM Player Tracker Discord Bot

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Discord.py](https://img.shields.io/badge/discord.py-2.3.0+-blue.svg)](https://github.com/Rapptz/discord.py)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A Discord bot that tracks and displays real-time player status for FiveM servers using publicly available API data. Monitor your friends' presence with beautiful, auto-updating embeds!

## Features

- 🎮 Real-time player status tracking
- 🟢 Live online/offline indicators
- ⏰ Automatic updates every 5 minutes
- 📝 Easy player management with slash commands
- 🎨 Beautiful Discord embeds matching your design
- 💾 Persistent player storage

## Preview

The bot displays tracked players with:
- Green indicators (🟢) for online players
- Red indicators (🔴) for offline players
- Player count and last update timestamp
- Automatic status updates

## Setup Instructions

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Create Discord Bot

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Go to the "Bot" section and click "Add Bot"
4. Under "Privileged Gateway Intents", enable:
   - Message Content Intent
5. Copy the bot token (you'll need this for `.env`)

### 3. Invite Bot to Your Server

1. In Developer Portal, go to "OAuth2" → "URL Generator"
2. Select scopes:
   - `bot`
   - `applications.commands`
3. Select bot permissions:
   - Send Messages
   - Embed Links
   - Read Message History
   - Use Slash Commands
4. Copy the generated URL and open it in your browser to invite the bot

### 4. Configure Environment Variables

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and fill in:
   ```env
   DISCORD_BOT_TOKEN=your_bot_token_here
   FIVEM_SERVER_ID=your_server_id
   UPDATE_CHANNEL_ID=your_channel_id_here
   ```

   - `DISCORD_BOT_TOKEN`: Your bot token from Discord Developer Portal
   - `FIVEM_SERVER_ID`: Your FiveM server ID (find it in the server URL: servers.fivem.net/servers/detail/YOUR_ID)
   - `UPDATE_CHANNEL_ID`: Right-click a Discord channel → Copy ID (enable Developer Mode in Discord settings)

### 5. Run the Bot

```bash
python bot.py
```

The bot will:
- Connect to Discord
- Sync slash commands
- Start auto-updating every 5 minutes
- Post the player status embed in your configured channel

## Commands

All commands are slash commands (type `/` to see them):

### `/set <fivem_name> <nickname>`
Add or update a tracked player.
- `fivem_name`: The player's name as shown in the FiveM server
- `nickname`: The display name to show in the tracker

**Example:**
```
/set "Richard Payne" "Richard"
/set "Wu.Jackson" "Wu Jackson"
```

### `/remove <fivem_name>`
Remove a player from tracking.

**Example:**
```
/remove "Richard Payne"
```

### `/list`
Display all currently tracked players with their FiveM names and nicknames.

### `/refresh`
Manually trigger an immediate status update (doesn't reset the 5-minute timer).

## How It Works

1. **Player Storage**: Tracked players are stored in `tracked_players.json`
2. **API Polling**: Every 5 minutes, the bot fetches current players from FiveM's public API
3. **Status Matching**: Compares tracked players with online players (case-insensitive)
4. **Embed Update**: Updates the Discord message with current online/offline status
5. **Persistent Message**: Edits the same message instead of spamming new ones

## Troubleshooting

### Bot doesn't respond to commands
- Make sure you've enabled "Message Content Intent" in Discord Developer Portal
- Verify the bot has proper permissions in your Discord server
- Check that slash commands are synced (bot logs will show "Synced X command(s)")

### Player status not updating
- Verify `UPDATE_CHANNEL_ID` is set correctly in `.env`
- Make sure the bot has permission to send messages in that channel
- Check the console for error messages

### Players showing as offline when they're online
- The FiveM name must match the server's player name
- Try using `/list` to see the exact names you've saved
- Update the player with `/set` using the exact FiveM name

### FiveM API not responding
- The public API might be temporarily down
- Verify the server ID is correct in your `.env` file
- Check your internet connection

## File Structure

```
DiscordBot-Person-Tracker/
├── bot.py                    # Main bot code
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (create from .env.example)
├── .env.example             # Example environment variables
├── .gitignore               # Git ignore file
├── tracked_players.json     # Stored tracked players (auto-generated)
└── README.md                # This file
```

## Technical Details

- **Discord.py**: Modern Discord bot framework with slash commands
- **Aiohttp**: Async HTTP client for FiveM API
- **JSON Storage**: Simple file-based storage for tracked players
- **Task Loop**: Discord.py task loop for automatic updates
- **API Endpoint**: `https://servers-frontend.fivem.net/api/servers/single/{SERVER_ID}`

## Future Enhancements

Potential features to add:
- Statistics tracking (playtime, login history)
- Multiple server support
- Configurable update intervals
- Notifications when specific players join/leave
- Web dashboard
- Database storage (SQLite/PostgreSQL)

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For issues or questions:
1. Check the [Troubleshooting](#troubleshooting) section
2. Review [QUICKSTART.md](QUICKSTART.md) for setup help
3. Open an [Issue](../../issues) on GitHub
4. Verify your `.env` configuration
5. Check bot console logs for errors

## Acknowledgments

- Built with [discord.py](https://github.com/Rapptz/discord.py)
- Uses FiveM's public server API
- Inspired by the need to track friends on FiveM servers
