import discord
from discord.ext import commands, tasks
from discord import app_commands
import aiohttp
import json
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
SERVER_ID = os.getenv('FIVEM_SERVER_ID', 'javxzp')
UPDATE_CHANNEL_ID = int(os.getenv('UPDATE_CHANNEL_ID', '0'))
TRACKED_PLAYERS_FILE = 'tracked_players.json'

# Bot setup with required intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Global variables
last_message_id = None
session = None


class PlayerTracker:
    """Handles player tracking data storage and retrieval"""
    
    def __init__(self, filepath):
        self.filepath = filepath
        self.players = self.load_players()
    
    def load_players(self):
        """Load tracked players from JSON file"""
        if os.path.exists(self.filepath):
            with open(self.filepath, 'r') as f:
                return json.load(f)
        return {}
    
    def save_players(self):
        """Save tracked players to JSON file"""
        with open(self.filepath, 'w') as f:
            json.dump(self.players, f, indent=4)
    
    def add_player(self, fivem_name, nickname):
        """Add or update a tracked player"""
        self.players[fivem_name] = nickname
        self.save_players()
    
    def remove_player(self, fivem_name):
        """Remove a tracked player"""
        if fivem_name in self.players:
            del self.players[fivem_name]
            self.save_players()
            return True
        return False
    
    def get_all_players(self):
        """Get all tracked players"""
        return self.players


# Initialize tracker
tracker = PlayerTracker(TRACKED_PLAYERS_FILE)


async def fetch_fivem_players():
    """Fetch current players from FiveM server"""
    try:
        url = f"https://servers-frontend.fivem.net/api/servers/single/{SERVER_ID}"
        async with session.get(url, timeout=10) as response:
            if response.status == 200:
                data = await response.json()
                
                # Extract player names from the Data object
                if 'Data' in data and 'players' in data['Data']:
                    players = data['Data']['players']
                    return [player.get('name', '') for player in players if player.get('name')]
                
        return []
    except Exception as e:
        print(f"Error fetching FiveM data: {e}")
        return []


def create_status_embed(online_players):
    """Create the Discord embed with player statuses"""
    tracked = tracker.get_all_players()
    
    # Separate online and offline players
    online_list = []
    offline_list = []
    
    for fivem_name, nickname in tracked.items():
        # Check if player is online (case-insensitive matching)
        is_online = any(fivem_name.lower() in player.lower() or player.lower() in fivem_name.lower() 
                       for player in online_players)
        
        if is_online:
            online_list.append(f"🟢 {nickname}")
        else:
            offline_list.append(f"🔴 {nickname}")
    
    # Count online players
    online_count = len(online_list)
    total_count = len(tracked)
    
    # Create embed
    embed = discord.Embed(
        title="🎮 Live Player Status",
        description=f"Real-time updates of player presence in the city.",
        color=discord.Color.from_rgb(66, 135, 245)
    )
    
    # Add player count
    embed.add_field(
        name=f"👥 {online_count} Players in the city:",
        value="\n".join(online_list) if online_list else "No tracked players online",
        inline=False
    )
    
    # Add offline players if any
    if offline_list:
        embed.add_field(
            name=f"💤 Offline ({len(offline_list)}):",
            value="\n".join(offline_list),
            inline=False
        )
    
    # Footer with timestamp
    embed.set_footer(text=f"Last updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    
    return embed


@tasks.loop(minutes=5)
async def update_status():
    """Update player status every 5 minutes"""
    global last_message_id
    
    if UPDATE_CHANNEL_ID == 0:
        print("Warning: UPDATE_CHANNEL_ID not set. Skipping update.")
        return
    
    try:
        channel = bot.get_channel(UPDATE_CHANNEL_ID)
        if not channel:
            print(f"Error: Could not find channel with ID {UPDATE_CHANNEL_ID}")
            return
        
        # Fetch current online players
        online_players = await fetch_fivem_players()
        
        # Create embed
        embed = create_status_embed(online_players)
        
        # Edit existing message or send new one
        if last_message_id:
            try:
                message = await channel.fetch_message(last_message_id)
                await message.edit(embed=embed)
                print(f"Updated status at {datetime.utcnow()}")
            except discord.NotFound:
                # Message was deleted, send a new one
                message = await channel.send(embed=embed)
                last_message_id = message.id
                print(f"Sent new status message at {datetime.utcnow()}")
        else:
            message = await channel.send(embed=embed)
            last_message_id = message.id
            print(f"Sent initial status message at {datetime.utcnow()}")
            
    except Exception as e:
        print(f"Error updating status: {e}")


@bot.event
async def on_ready():
    """Bot startup event"""
    global session
    
    # Create aiohttp session
    session = aiohttp.ClientSession()
    
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print(f'Tracking {len(tracker.get_all_players())} players')
    print('------')
    
    # Sync slash commands
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")
    
    # Start update loop
    if not update_status.is_running():
        update_status.start()


@bot.tree.command(name="set", description="Add or update a tracked player")
@app_commands.describe(
    fivem_name="The player's FiveM name (as shown in server)",
    nickname="The nickname to display in the tracker"
)
async def set_player(interaction: discord.Interaction, fivem_name: str, nickname: str):
    """Add or update a tracked player"""
    tracker.add_player(fivem_name, nickname)
    
    embed = discord.Embed(
        title="✅ Player Added",
        description=f"Now tracking **{nickname}** (FiveM: {fivem_name})",
        color=discord.Color.green()
    )
    
    await interaction.response.send_message(embed=embed, ephemeral=True)
    
    # Trigger immediate update
    await update_status()


@bot.tree.command(name="remove", description="Remove a tracked player")
@app_commands.describe(fivem_name="The player's FiveM name to remove")
async def remove_player(interaction: discord.Interaction, fivem_name: str):
    """Remove a tracked player"""
    if tracker.remove_player(fivem_name):
        embed = discord.Embed(
            title="✅ Player Removed",
            description=f"Stopped tracking **{fivem_name}**",
            color=discord.Color.orange()
        )
    else:
        embed = discord.Embed(
            title="❌ Player Not Found",
            description=f"No tracked player found with FiveM name: {fivem_name}",
            color=discord.Color.red()
        )
    
    await interaction.response.send_message(embed=embed, ephemeral=True)
    
    # Trigger immediate update if player was removed
    if fivem_name not in tracker.get_all_players():
        await update_status()


@bot.tree.command(name="list", description="List all tracked players")
async def list_players(interaction: discord.Interaction):
    """List all tracked players"""
    tracked = tracker.get_all_players()
    
    if not tracked:
        embed = discord.Embed(
            title="📋 Tracked Players",
            description="No players are currently being tracked.",
            color=discord.Color.blue()
        )
    else:
        player_list = "\n".join([f"• **{nickname}** (FiveM: {fivem_name})" 
                                 for fivem_name, nickname in tracked.items()])
        
        embed = discord.Embed(
            title="📋 Tracked Players",
            description=player_list,
            color=discord.Color.blue()
        )
        embed.set_footer(text=f"Total: {len(tracked)} players")
    
    await interaction.response.send_message(embed=embed, ephemeral=True)


@bot.tree.command(name="refresh", description="Manually refresh the player status")
async def refresh_status(interaction: discord.Interaction):
    """Manually trigger a status update"""
    await interaction.response.defer(ephemeral=True)
    
    try:
        await update_status()
        embed = discord.Embed(
            title="✅ Status Refreshed",
            description="Player status has been updated!",
            color=discord.Color.green()
        )
    except Exception as e:
        embed = discord.Embed(
            title="❌ Refresh Failed",
            description=f"Error: {str(e)}",
            color=discord.Color.red()
        )
    
    await interaction.followup.send(embed=embed, ephemeral=True)


@bot.event
async def on_close():
    """Cleanup when bot shuts down"""
    global session
    if session:
        await session.close()


if __name__ == "__main__":
    if not TOKEN:
        print("Error: DISCORD_BOT_TOKEN not found in .env file!")
        exit(1)
    
    bot.run(TOKEN)
