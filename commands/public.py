import discord
from discord.ext import commands

class PublicCommands(commands.Cog):
    def __init__(self, bot, minecraft_manager, config):
        self.bot = bot
        self.minecraft_manager = minecraft_manager
        self.config = config
    
    @commands.command()
    async def status(self, ctx):
        """Vérifie si le serveur est en ligne"""
        status = await self.minecraft_manager.get_status()
        message = self.minecraft_manager.format_status_message(status)
        
        if not status["online"] and "error" in status:
            message += f"\nErreur : `{status['error']}`"
        
        await ctx.send(message)
    
    @commands.command()
    async def ip(self, ctx):
        """Affiche l'adresse IP du serveur"""
        await ctx.send(f"IP du serveur : `{self.config.server_address}`")
    
    @commands.command()
    async def version(self, ctx):
        """Affiche la version du serveur"""
        version = self.config.get("minecraft_version")
        await ctx.send(f"Version Minecraft définie : `{version}`")
    
    @commands.command()
    async def joueurs(self, ctx):
        """Affiche la liste des joueurs connectés"""
        players_data = await self.minecraft_manager.get_players()
        message = self.minecraft_manager.format_players_message(players_data)
        await ctx.send(message)
    
    @commands.command()
    async def mods(self, ctx):
        """Affiche le lien pour télécharger tous les mods du serveur"""
        embed = discord.Embed(
            title="Mods du serveur CraftMine",
            description="Plus de 80 mods Fabric pour Minecraft 1.21.4",
            color=discord.Color.green()
        )
        
        embed.add_field(
            name="Téléchargement",
            value="Cliquez sur le bouton ci-dessous pour télécharger tous les mods nécessaires",
            inline=False
        )
        
        # Bouton vers le Google Drive (lien configurable)
        drive_link = self.config.get("google_drive_mods_link", "https://drive.google.com/")
        view = discord.ui.View()
        button = discord.ui.Button(
            label="Télécharger tous les mods",
            url=drive_link,
            style=discord.ButtonStyle.link
        )
        view.add_item(button)
        
        await ctx.send(embed=embed, view=view)
    
    @commands.command(name="chercher-mod", aliases=["rechercher-mod", "search-mod"])
    async def chercher_mod(self, ctx, *, nom_mod: str):
        """Cherche un mod sur Modrinth et CurseForge"""
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
        
        await ctx.send(embed=embed)
    
    @commands.command(name="aide", aliases=["help", "h"])
    async def aide(self, ctx):
        """Affiche l'aide des commandes disponibles"""
        embed_content = (
            "**CraftMine Bot - Commandes disponibles**\n\n"
            "**Surveillance du serveur :**\n"
            "• `!status` - État du serveur et nombre de joueurs\n"
            "• `!joueurs` - Liste des joueurs connectés\n"
            "• `!mods` - Liste des mods/plugins installés\n"
            "• `!chercher-mod <nom>` - Rechercher un mod spécifique\n\n"
            "**Informations :**\n"
            "• `!ip` - Adresse IP du serveur\n"
            "• `!version` - Version Minecraft\n"
            "• `!aide` - Affiche cette aide\n\n"
            "**Administration :**\n"
            "• `!parametres` - Voir/modifier la configuration (admin uniquement)\n\n"
            "*Le statut est mis à jour automatiquement toutes les 30 secondes*"
        )
        await ctx.send(embed_content)

async def setup(bot, minecraft_manager, config):
    """Fonction pour ajouter les commandes au bot"""
    await bot.add_cog(PublicCommands(bot, minecraft_manager, config))
