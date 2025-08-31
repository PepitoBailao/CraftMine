from discord.ext import commands

def is_admin(admin_ids):
    """Décorateur pour vérifier si l'utilisateur est admin"""
    def predicate(ctx):
        return ctx.author.id in admin_ids
    return commands.check(predicate)

class AdminCommands(commands.Cog):
    def __init__(self, bot, config):
        self.bot = bot
        self.config = config
    
    @commands.group(name="parametres", invoke_without_command=True)
    @is_admin(admin_ids=[448420884059914240])  # Utiliser la config plus tard
    async def parametres(self, ctx):
        """Affiche les paramètres actuels"""
        embed_content = (
            f"⚙️ **Configuration actuelle :**\n"
            f"• **IP :** `{self.config.get('server_ip')}`\n"
            f"• **Port :** `{self.config.get('server_port')}`\n"
            f"• **Version :** `{self.config.get('minecraft_version')}`\n\n"
            f"**📝 Commandes disponibles :**\n"
            f"• `!parametres setip <ip> [port]` - Changer l'adresse\n"
            f"• `!parametres setversion <version>` - Changer la version\n"
            f"• `!parametres reload` - Recharger la config\n"
            f"• `!parametres test` - Tester la connexion"
        )
        await ctx.send(embed_content)
    
    @parametres.command(name="setip")
    @is_admin(admin_ids=[448420884059914240])
    async def set_ip(self, ctx, ip: str, port: int = 25565):
        """Changer l'IP et le port du serveur"""
        self.config.set("server_ip", ip)
        self.config.set("server_port", port)
        await ctx.send(f"✅ Adresse mise à jour : `{ip}:{port}`")
    
    @parametres.command(name="setversion")
    @is_admin(admin_ids=[448420884059914240])
    async def set_version(self, ctx, version: str):
        """Changer la version affichée"""
        self.config.set("minecraft_version", version)
        await ctx.send(f"✅ Version Minecraft mise à jour : `{version}`")
    
    @parametres.command(name="reload")
    @is_admin(admin_ids=[448420884059914240])
    async def reload_config(self, ctx):
        """Recharge la configuration depuis le fichier"""
        self.config.load_config()
        await ctx.send("🔄 Configuration rechargée depuis le fichier.")
    
    @parametres.command(name="test")
    @is_admin(admin_ids=[448420884059914240])
    async def test_connection(self, ctx):
        """Teste la connexion au serveur Minecraft"""
        from src.utils.minecraft import MinecraftServerManager
        
        minecraft_manager = MinecraftServerManager(self.config)
        status = await minecraft_manager.get_status()
        
        if status["online"]:
            await ctx.send(
                f"✅ **Test de connexion réussi !**\n"
                f"• Serveur en ligne\n"
                f"• Joueurs : {status['players_online']}/{status['players_max']}\n"
                f"• Latence : {status['latency']:.2f}ms"
            )
        else:
            await ctx.send(
                f"❌ **Échec de connexion**\n"
                f"• Erreur : `{status.get('error', 'Inconnue')}`\n"
                f"• Vérifiez l'IP et le port dans la configuration"
            )

async def setup(bot, config):
    """Fonction pour ajouter les commandes au bot"""
    await bot.add_cog(AdminCommands(bot, config))
