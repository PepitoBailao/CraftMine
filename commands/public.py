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
        await ctx.send(f"🌐 IP du serveur : `{self.config.server_address}`")
    
    @commands.command()
    async def version(self, ctx):
        """Affiche la version du serveur"""
        version = self.config.get("minecraft_version")
        await ctx.send(f"⚙️ Version Minecraft définie : `{version}`")
    
    @commands.command()
    async def joueurs(self, ctx):
        """Affiche la liste des joueurs connectés"""
        players_data = await self.minecraft_manager.get_players()
        message = self.minecraft_manager.format_players_message(players_data)
        await ctx.send(message)
    
    @commands.command(name="aide", aliases=["help", "h"])
    async def aide(self, ctx):
        """Affiche l'aide des commandes disponibles"""
        embed_content = (
            "🤖 **CraftMine Bot - Commandes disponibles**\n\n"
            "**📊 Surveillance du serveur :**\n"
            "• `!status` - État du serveur et nombre de joueurs\n"
            "• `!joueurs` - Liste des joueurs connectés\n\n"
            "**ℹ️ Informations :**\n"
            "• `!ip` - Adresse IP du serveur\n"
            "• `!version` - Version Minecraft\n"
            "• `!aide` - Affiche cette aide\n\n"
            "**⚙️ Administration :**\n"
            "• `!parametres` - Voir/modifier la configuration (admin uniquement)\n\n"
            "🔄 *Le statut est mis à jour automatiquement toutes les 30 secondes*"
        )
        await ctx.send(embed_content)

async def setup(bot, minecraft_manager, config):
    """Fonction pour ajouter les commandes au bot"""
    await bot.add_cog(PublicCommands(bot, minecraft_manager, config))
