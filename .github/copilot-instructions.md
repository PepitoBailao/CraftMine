# CraftMine Discord Bot

This is a Discord bot for monitoring Minecraft server status with the following features:
- Real-time server status monitoring with automatic updates every 30 seconds
- Player count display and online player list
- Server IP and version information
- Admin commands for configuration management
- Modular architecture for easy maintenance and extension
- Comprehensive error handling and user-friendly messages

## Project Structure
- `src/` - Main application code
  - `main.py` - Entry point and bot orchestration
  - `utils/minecraft.py` - Minecraft server management utilities
- `commands/` - Discord command modules
  - `public.py` - Public commands (status, ip, version, players, help)
  - `admin.py` - Admin commands (configuration management)
- `config/` - Configuration management
  - `settings.py` - Centralized configuration class
- `.env` - Environment variables (not tracked in git)
- `config.json` - Runtime configuration (auto-generated)

## Technologies Used
- Python 3.11+ with virtual environment
- discord.py >=2.3.0 - Discord API wrapper
- mcstatus >=11.0.0 - Minecraft server status checking (JavaServer)
- python-dotenv >=1.0.0 - Environment variable management

## Setup Instructions
1. Install dependencies: `pip install -r requirements.txt`
2. Copy `.env.example` to `.env` and fill in your Discord token
3. Run the bot: `python src/main.py` or use `start_bot.bat`

## Commands
### Public Commands (all users)
- `!status` - Check server status and player count
- `!ip` - Show server IP and port
- `!version` - Show configured Minecraft version
- `!joueurs` - List online players (requires server query enabled)
- `!aide` / `!help` / `!h` - Show command help

### Admin Commands (restricted by Discord ID)
- `!parametres` - Show current configuration and available admin commands
- `!parametres setip <ip> [port]` - Update server address
- `!parametres setversion <version>` - Update displayed Minecraft version
- `!parametres reload` - Reload configuration from file
- `!parametres test` - Test connection to Minecraft server

## Features
- Automatic status updates every 30 seconds
- Discord presence showing "X/Y players online" or "Server offline"
- Persistent configuration with JSON file storage
- Secure token management with environment variables
- Comprehensive error handling and user feedback
- Modular command system for easy extension
