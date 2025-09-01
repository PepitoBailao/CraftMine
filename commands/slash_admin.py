from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands

class SlashAdminCommands(commands.Cog):
    def __init__(self, bot, config):
        self.bot = bot
        self.config = config
    
    def is_admin(self, user_id: int) -> bool:
        """Vérifie si l'utilisateur est admin"""
        return user_id in self.config.admin_ids
    
    @app_commands.command(name="parametres", description="Configuration du bot (admin uniquement)")
    @app_commands.describe(
        action="Action à effectuer",
        parametre="Paramètre à modifier",
        valeur="Nouvelle valeur"
    )
    @app_commands.choices(action=[
        app_commands.Choice(name="Voir la configuration", value="show"),
        app_commands.Choice(name="Changer l'IP", value="setip"),
        app_commands.Choice(name="Changer la version", value="setversion"),
        app_commands.Choice(name="Serveur ouvert/fermé", value="serveropen"),
        app_commands.Choice(name="Lien Google Drive", value="drivelink"),
        app_commands.Choice(name="Recharger la config", value="reload"),
        app_commands.Choice(name="Tester la connexion", value="test")
    ])
    async def parametres(
        self, 
        interaction: discord.Interaction,
        action: app_commands.Choice[str],
        parametre: Optional[str] = None,
        valeur: Optional[str] = None
    ):
        """Slash command pour la configuration admin"""
        
        # Vérification des permissions
        if not self.is_admin(interaction.user.id):
            await interaction.response.send_message("Vous n'avez pas la permission d'utiliser cette commande.", ephemeral=True)
            return
        
        if action.value == "show":
            embed = discord.Embed(
                title="Configuration actuelle",
                color=discord.Color.green()
            )
            embed.add_field(name="IP", value=f"`{self.config.get('server_ip')}`", inline=True)
            embed.add_field(name="Port", value=f"`{self.config.get('server_port')}`", inline=True)
            embed.add_field(name="Version", value=f"`{self.config.get('minecraft_version')}`", inline=True)
            embed.add_field(name="Serveur ouvert", value=f"`{'Oui' if self.config.get('server_open', True) else 'Non'}`", inline=True)
            
            drive_link = self.config.get('google_drive_mods_link', 'Non configuré')
            if len(drive_link) > 50:
                drive_link = drive_link[:47] + "..."
            embed.add_field(name="Lien Google Drive", value=f"`{drive_link}`", inline=False)
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
        
        elif action.value == "setip":
            if not valeur:
                await interaction.response.send_message("Vous devez spécifier une adresse IP.", ephemeral=True)
                return
            
            self.config.set("server_ip", valeur)
            await interaction.response.send_message(f"Adresse mise à jour : `{valeur}`", ephemeral=True)
        
        elif action.value == "setversion":
            if not valeur:
                await interaction.response.send_message("Vous devez spécifier une version.", ephemeral=True)
                return
            
            self.config.set("minecraft_version", valeur)
            await interaction.response.send_message(f"Version Minecraft mise à jour : `{valeur}`", ephemeral=True)
        
        elif action.value == "serveropen":
            if not valeur:
                await interaction.response.send_message("Vous devez spécifier true ou false.", ephemeral=True)
                return
            
            new_value = valeur.lower() in ['true', '1', 'oui', 'ouvert', 'on', 'yes']
            self.config.set("server_open", new_value)
            await interaction.response.send_message(f"Serveur configuré comme: `{'Ouvert' if new_value else 'Fermé'}`", ephemeral=True)
        
        elif action.value == "drivelink":
            if not valeur:
                await interaction.response.send_message("Vous devez spécifier un lien Google Drive.", ephemeral=True)
                return
            
            self.config.set("google_drive_mods_link", valeur)
            await interaction.response.send_message(f"Lien Google Drive mis à jour", ephemeral=True)
        
        elif action.value == "reload":
            self.config.load_config()
            await interaction.response.send_message("Configuration rechargée depuis le fichier.", ephemeral=True)
        
        elif action.value == "test":
            await interaction.response.defer(ephemeral=True)
            
            from src.utils.minecraft import MinecraftServerManager
            minecraft_manager = MinecraftServerManager(self.config)
            status = await minecraft_manager.get_status()
            
            if status["online"]:
                embed = discord.Embed(
                    title="Test de connexion réussi !",
                    color=discord.Color.green()
                )
                embed.add_field(name="Statut", value="Serveur en ligne", inline=True)
                embed.add_field(name="Joueurs", value=f"{status['players_online']}/{status['players_max']}", inline=True)
                embed.add_field(name="Latence", value=f"{status['latency']:.2f}ms", inline=True)
            else:
                embed = discord.Embed(
                    title="Échec de connexion",
                    color=discord.Color.red()
                )
                embed.add_field(name="Erreur", value=f"`{status.get('error', 'Inconnue')}`", inline=False)
                embed.add_field(name="Solution", value="Vérifiez l'IP et le port dans la configuration", inline=False)
            
            await interaction.followup.send(embed=embed)

async def setup(bot, config):
    """Fonction pour ajouter les slash commands admin au bot"""
    await bot.add_cog(SlashAdminCommands(bot, config))
