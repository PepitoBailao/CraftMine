import discord
from discord import app_commands
from discord.ext import commands

class SlashCommands(commands.Cog):
    def __init__(self, bot, minecraft_manager, config):
        self.bot = bot
        self.minecraft_manager = minecraft_manager
        self.config = config
    
    @app_commands.command(name="status", description="Vérifie si le serveur Minecraft est en ligne")
    async def status(self, interaction: discord.Interaction):
        """Slash command pour vérifier le statut du serveur"""
        await interaction.response.defer()  # Permet plus de temps pour la réponse
        
        status = await self.minecraft_manager.get_status()
        message = self.minecraft_manager.format_status_message(status)
        
        if not status["online"] and "error" in status:
            message += f"\nErreur : `{status['error']}`"
        
        await interaction.followup.send(message)
    
    @app_commands.command(name="ip", description="Affiche l'adresse IP du serveur Minecraft")
    async def ip(self, interaction: discord.Interaction):
        """Slash command pour afficher l'IP du serveur"""
        await interaction.response.send_message(f"IP du serveur : `{self.config.server_address}`")
    
    @app_commands.command(name="version", description="Affiche la version Minecraft configurée")
    async def version(self, interaction: discord.Interaction):
        """Slash command pour afficher la version"""
        version = self.config.get("minecraft_version")
        await interaction.response.send_message(f"Version Minecraft définie : `{version}`")
    
    @app_commands.command(name="joueurs", description="Affiche la liste des joueurs connectés")
    async def joueurs(self, interaction: discord.Interaction):
        """Slash command pour lister les joueurs"""
        await interaction.response.defer()
        
        players_data = await self.minecraft_manager.get_players()
        message = self.minecraft_manager.format_players_message(players_data)
        await interaction.followup.send(message)
    
    @app_commands.command(name="aide", description="Affiche l'aide des commandes disponibles")
    async def aide(self, interaction: discord.Interaction):
        """Slash command pour l'aide"""
        embed = discord.Embed(
            title="CraftMine Bot - Commandes disponibles",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="Surveillance du serveur",
            value="• `/status` - État du serveur et nombre de joueurs\n• `/joueurs` - Liste des joueurs connectés",
            inline=False
        )
        
        embed.add_field(
            name="Informations",
            value="• `/ip` - Adresse IP du serveur\n• `/version` - Version Minecraft\n• `/aide` - Affiche cette aide",
            inline=False
        )
        
        embed.add_field(
            name="Administration",
            value="• `/parametres` - Configuration (admin uniquement)",
            inline=False
        )
        
        embed.set_footer(text="Le statut est mis à jour automatiquement toutes les 30 secondes")
        
        await interaction.response.send_message(embed=embed)

async def setup(bot, minecraft_manager, config):
    """Fonction pour ajouter les slash commands au bot"""
    await bot.add_cog(SlashCommands(bot, minecraft_manager, config))
