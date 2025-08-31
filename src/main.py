import discord
from discord.ext import commands, tasks
from discord import app_commands
import sys
import os

# Ajouter le dossier parent au path pour les imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import Config
from src.utils.minecraft import MinecraftServerManager

class CraftMineBot:
    def __init__(self):
        self.config = Config()
        self.minecraft_manager = MinecraftServerManager(self.config)
        
        # Configuration du bot Discord
        intents = discord.Intents.default()
        intents.message_content = True  # Requis pour les commandes
        
        # Ajouter d'autres intents si nécessaire
        intents.presences = False  # Pas besoin des statuts des utilisateurs
        intents.members = False    # Pas besoin de la liste des membres
        
        self.bot = commands.Bot(
            command_prefix="!",
            intents=intents,
            help_command=None  # Désactiver l'aide par défaut
        )
        
        self.setup_events()
    
    def setup_events(self):
        """Configure les événements du bot"""
        
        @self.bot.event
        async def on_ready():
            print(f"🤖 Bot connecté en tant que {self.bot.user}")
            print(f"📊 Serveur surveillé : {self.config.server_address}")
            
            # Synchroniser les slash commands
            try:
                synced = await self.bot.tree.sync()
                print(f"✅ {len(synced)} slash commands synchronisées")
            except Exception as e:
                print(f"❌ Erreur lors de la synchronisation des slash commands : {e}")
            
            # Démarrer la tâche de mise à jour du statut
            if not self.update_status.is_running():
                self.update_status.start()
        
        @self.bot.event
        async def on_command_error(ctx, error):
            """Gestion des erreurs de commandes"""
            if isinstance(error, commands.CommandNotFound):
                return  # Ignorer les commandes inconnues
            elif isinstance(error, commands.CheckFailure):
                await ctx.send("❌ Vous n'avez pas la permission d'utiliser cette commande.")
            elif isinstance(error, commands.MissingRequiredArgument):
                await ctx.send(f"❌ Argument manquant : `{error.param.name}`")
            else:
                print(f"Erreur de commande : {error}")
                await ctx.send("❌ Une erreur est survenue lors de l'exécution de la commande.")
    
    @tasks.loop(seconds=30)
    async def update_status(self):
        """Met à jour le statut du bot toutes les 30 secondes"""
        try:
            status = await self.minecraft_manager.get_status()
            
            if status["online"]:
                activity = discord.Game(
                    name=f"{status['players_online']}/{status['players_max']} joueurs en ligne"
                )
                discord_status = discord.Status.online
            else:
                activity = discord.Game(name="Serveur hors ligne")
                discord_status = discord.Status.dnd
            
            await self.bot.change_presence(activity=activity, status=discord_status)
        except Exception as e:
            print(f"Erreur lors de la mise à jour du statut : {e}")
    
    async def load_commands(self):
        """Charge toutes les commandes"""
        try:
            # Importer et ajouter les commandes publiques (préfixe !)
            from commands.public import setup as setup_public
            await setup_public(self.bot, self.minecraft_manager, self.config)
            
            # Importer et ajouter les commandes admin (préfixe !)
            from commands.admin import setup as setup_admin
            await setup_admin(self.bot, self.config)
            
            # Importer et ajouter les slash commands publiques
            from commands.slash_commands import setup as setup_slash
            await setup_slash(self.bot, self.minecraft_manager, self.config)
            
            # Importer et ajouter les slash commands admin
            from commands.slash_admin import setup as setup_slash_admin
            await setup_slash_admin(self.bot, self.config)
            
            print("✅ Commandes traditionnelles et slash commands chargées avec succès")
        except Exception as e:
            print(f"❌ Erreur lors du chargement des commandes : {e}")
    
    @update_status.before_loop
    async def before_update_status(self):
        """Attendre que le bot soit prêt avant de démarrer les tâches"""
        await self.bot.wait_until_ready()
    
    async def start(self):
        """Démarre le bot"""
        if not self.config.token:
            print("❌ ERREUR : Token Discord manquant!")
            print("Vérifiez que la variable DISCORD_TOKEN est définie dans votre fichier .env")
            return
        
        try:
            # Charger les commandes
            await self.load_commands()
            
            # Démarrer le bot
            print("🔗 Tentative de connexion à Discord...")
            await self.bot.start(self.config.token)
        except discord.LoginFailure:
            print("❌ ERREUR : Token Discord invalide!")
            print("Vérifiez votre token sur https://discord.com/developers/applications")
        except discord.PrivilegedIntentsRequired:
            print("❌ ERREUR : Intents privilégiés requis!")
            print("Activez les intents sur le portail Discord Developer")
        except Exception as e:
            error_code = getattr(e, 'code', 'Inconnue')
            print(f"❌ Erreur lors du démarrage : {e}")
            if str(error_code) == '4004':
                print("💡 Solution : Vérifiez que votre token est valide et que le bot n'est pas déjà en cours d'exécution")
            elif str(error_code) == '4014':
                print("💡 Solution : Activez les intents privilégiés sur le portail Discord")
            print(f"📋 Code d'erreur : {error_code}")
    
    def run(self):
        """Lance le bot (version synchrone)"""
        import asyncio
        try:
            asyncio.run(self.start())
        except KeyboardInterrupt:
            print("\n🛑 Arrêt du bot...")
        except Exception as e:
            print(f"❌ Erreur fatale : {e}")

if __name__ == "__main__":
    bot = CraftMineBot()
    bot.run()
