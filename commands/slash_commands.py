import discord
from discord import app_commands
from discord.ext import commands

class SlashCommands(commands.Cog):
    def __init__(self, bot, minecraft_manager, config):
        self.bot = bot
        self.minecraft_manager = minecraft_manager
        self.config = config
    
    @app_commands.command(name="status", description="Statut du serveur Minecraft")
    async def status(self, interaction: discord.Interaction):
        """Slash command pour vérifier le statut du serveur"""
        await interaction.response.defer()
        
        status = await self.minecraft_manager.get_status()
        
        if status["online"]:
            server_state = "Ouvert" if self.config.get("server_open", True) else "Fermé"
            embed = discord.Embed(
                title="Serveur Minecraft",
                color=discord.Color.green()
            )
            embed.add_field(name="État", value=server_state, inline=True)
            embed.add_field(name="Joueurs", value=f"{status['players_online']}/{status['players_max']}", inline=True)
            embed.add_field(name="Latence", value=f"{status['latency']:.0f}ms", inline=True)
        else:
            embed = discord.Embed(
                title="Serveur Minecraft",
                description="Serveur hors ligne",
                color=discord.Color.red()
            )
        
        await interaction.followup.send(embed=embed)
    
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
    
    @app_commands.command(name="mods", description="Lien de téléchargement des mods du serveur")
    async def mods(self, interaction: discord.Interaction):
        """Slash command pour afficher le lien des mods"""
        
        drive_link = self.config.get("google_drive_mods_link")
        if drive_link:
            embed = discord.Embed(
                title="Mods du serveur",
                description=f"[Télécharger les mods]({drive_link})",
                color=discord.Color.blue()
            )
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("Lien de téléchargement des mods non configuré.", ephemeral=True)
    
    @app_commands.command(name="chercher-mod", description="Cherche un mod sur Modrinth et CurseForge")
    @app_commands.describe(nom_mod="Le nom du mod à rechercher")
    async def chercher_mod(self, interaction: discord.Interaction, nom_mod: str):
        """Slash command pour chercher un mod spécifique"""
        await interaction.response.defer()
        
        # Nettoyer le nom du mod
        clean_name = nom_mod.lower().replace(' ', '-').replace('_', '-')
        
        embed = discord.Embed(
            title=f"Recherche: {nom_mod}",
            description=f"Liens de téléchargement pour **{nom_mod}**",
            color=discord.Color.blue()
        )
        
        # Liens de recherche
        modrinth_search = f"https://modrinth.com/mods?q={nom_mod.replace(' ', '%20')}"
        curseforge_search = f"https://www.curseforge.com/minecraft/search?search={nom_mod.replace(' ', '%20')}"
        
        embed.add_field(
            name="Recherche",
            value=(
                f"[Modrinth]({modrinth_search})\n"
                f"[CurseForge]({curseforge_search})"
            ),
            inline=False
        )
        
        embed.set_footer(text="Recherchez directement sur les plateformes de mods")
        
        await interaction.followup.send(embed=embed)
    
    @app_commands.command(name="aide", description="Affiche l'aide des commandes disponibles")
    async def aide(self, interaction: discord.Interaction):
        """Slash command pour l'aide"""
        embed = discord.Embed(
            title="CraftMine Bot - Commandes disponibles",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="Surveillance du serveur",
            value="• `/status` - État du serveur et nombre de joueurs\n• `/joueurs` - Liste des joueurs connectés\n• `/mods` - Liste des mods/plugins installés\n• `/chercher-mod` - Rechercher un mod spécifique",
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
