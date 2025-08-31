from discord.ext import commands

def is_admin(config):
    """Décorateur pour vérifier si l'utilisateur est admin"""
    def predicate(ctx):
        return ctx.author.id in config.admin_ids
    return commands.check(predicate)

class AdminCommands(commands.Cog):
    def __init__(self, bot, config):
        self.bot = bot
        self.config = config
    
    @commands.group(name="parametres", invoke_without_command=True)
    async def parametres(self, ctx):
        """Affiche les paramètres actuels"""
        # Vérification des permissions
        if ctx.author.id not in self.config.admin_ids:
            await ctx.send("Vous n'avez pas la permission d'utiliser cette commande.")
            return
            
        embed_content = (
            f"**Configuration actuelle :**\n"
            f"• **IP :** `{self.config.get('server_ip')}`\n"
            f"• **Port :** `{self.config.get('server_port')}`\n"
            f"• **Version :** `{self.config.get('minecraft_version')}`\n\n"
            f"**Commandes disponibles :**\n"
            f"• `!parametres setip <ip> [port]` - Changer l'adresse\n"
            f"• `!parametres setversion <version>` - Changer la version\n"
            f"• `!parametres reload` - Recharger la config\n"
            f"• `!parametres test` - Tester la connexion"
        )
        await ctx.send(embed_content)
    
    @parametres.command(name="setip")
    async def set_ip(self, ctx, ip: str, port: int = 25565):
        """Changer l'IP et le port du serveur"""
        if ctx.author.id not in self.config.admin_ids:
            await ctx.send("Vous n'avez pas la permission d'utiliser cette commande.")
            return
            
        self.config.set("server_ip", ip)
        self.config.set("server_port", port)
        await ctx.send(f"Adresse mise à jour : `{ip}:{port}`")
    
    @parametres.command(name="setversion")
    async def set_version(self, ctx, version: str):
        """Changer la version affichée"""
        if ctx.author.id not in self.config.admin_ids:
            await ctx.send("Vous n'avez pas la permission d'utiliser cette commande.")
            return
            
        self.config.set("minecraft_version", version)
        await ctx.send(f"Version Minecraft mise à jour : `{version}`")
    
    @parametres.command(name="reload")
    async def reload_config(self, ctx):
        """Recharge la configuration depuis le fichier"""
        if ctx.author.id not in self.config.admin_ids:
            await ctx.send("Vous n'avez pas la permission d'utiliser cette commande.")
            return
            
        self.config.load_config()
        await ctx.send("Configuration rechargée depuis le fichier.")
    
    @parametres.command(name="test")
    async def test_connection(self, ctx):
        """Teste la connexion au serveur Minecraft"""
        if ctx.author.id not in self.config.admin_ids:
            await ctx.send("Vous n'avez pas la permission d'utiliser cette commande.")
            return
            
        from src.utils.minecraft import MinecraftServerManager
        
        minecraft_manager = MinecraftServerManager(self.config)
        status = await minecraft_manager.get_status()
        
        if status["online"]:
            await ctx.send(
                f"**Test de connexion réussi !**\n"
                f"• Serveur en ligne\n"
                f"• Joueurs : {status['players_online']}/{status['players_max']}\n"
                f"• Latence : {status['latency']:.2f}ms"
            )
        else:
            await ctx.send(
                f"**Échec de connexion**\n"
                f"• Erreur : `{status.get('error', 'Inconnue')}`\n"
                f"• Vérifiez l'IP et le port dans la configuration"
            )

async def setup(bot, config):
    """Fonction pour ajouter les commandes au bot"""
    await bot.add_cog(AdminCommands(bot, config))
