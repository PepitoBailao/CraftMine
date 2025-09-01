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
        ip="Nouvelle adresse IP du serveur",
        port="Nouveau port du serveur (défaut: port_par_defaut)",
        version="Nouvelle version Minecraft"
    )
    @app_commands.choices(action=[
        app_commands.Choice(name="Voir la configuration", value="show"),
        app_commands.Choice(name="Changer l'IP", value="setip"),
        app_commands.Choice(name="Changer la version", value="setversion"),
        app_commands.Choice(name="Recharger la config", value="reload"),
        app_commands.Choice(name="Tester la connexion", value="test")
    ])
    async def parametres(
        self, 
        interaction: discord.Interaction,
        action: app_commands.Choice[str],
        ip: Optional[str] = None,
        port: int = 25565,
        version: Optional[str] = None
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
            
            # Nouveaux paramètres
            embed.add_field(name="Serveur ouvert", value=f"`{'Oui' if self.config.get('server_open', True) else 'Non'}`", inline=True)
            
            drive_link = self.config.get('google_drive_mods_link', 'Non configuré')
            if len(drive_link) > 50:
                drive_link = drive_link[:47] + "..."
            embed.add_field(name="Lien Google Drive", value=f"`{drive_link}`", inline=False)
            
            embed.add_field(
                name="Actions disponibles",
                value="Utilisez `/parametres` avec les différentes actions pour modifier la configuration\nUtilisez `/config` pour gérer serveur_ouvert et lien_drive",
                inline=False
            )
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
        
        elif action.value == "setip":
            if not ip:
                await interaction.response.send_message("Vous devez spécifier une adresse IP.", ephemeral=True)
                return
            
            self.config.set("server_ip", ip)
            self.config.set("server_port", port)
            await interaction.response.send_message(f"Adresse mise à jour : `{ip}:{port}`", ephemeral=True)
        
        elif action.value == "setversion":
            if not version:
                await interaction.response.send_message("Vous devez spécifier une version.", ephemeral=True)
                return
            
            self.config.set("minecraft_version", version)
            await interaction.response.send_message(f"Version Minecraft mise à jour : `{version}`", ephemeral=True)
        
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

    @app_commands.command(name="config", description="Gère les paramètres avancés du bot (admin uniquement)")
    @app_commands.describe(
        parametre="Paramètre à modifier",
        valeur="Nouvelle valeur"
    )
    @app_commands.choices(parametre=[
        app_commands.Choice(name="serveur_ouvert", value="server_open"),
        app_commands.Choice(name="lien_drive_mods", value="google_drive_mods_link")
    ])
    async def config_command(self, interaction: discord.Interaction, parametre: str, valeur: Optional[str] = None):
        """Commande pour gérer les paramètres avancés"""
        
        # Vérification des permissions
        if not self.is_admin(interaction.user.id):
            await interaction.response.send_message("Vous n'avez pas la permission d'utiliser cette commande.", ephemeral=True)
            return
        
        if valeur is None:
            # Afficher la valeur actuelle
            current_value = self.config.get(parametre)
            if parametre == "server_open":
                display_value = "Oui" if current_value else "Non"
            else:
                display_value = current_value if current_value else "Non configuré"
            
            await interaction.response.send_message(f"Valeur actuelle de `{parametre}`: `{display_value}`", ephemeral=True)
            return
        
        # Modifier la configuration
        if parametre == "server_open":
            new_value = valeur.lower() in ['true', '1', 'oui', 'ouvert', 'on', 'yes']
            self.config.set("server_open", new_value)
            await interaction.response.send_message(f"Serveur configuré comme: `{'Ouvert' if new_value else 'Fermé'}`", ephemeral=True)
            
        elif parametre == "google_drive_mods_link":
            self.config.set("google_drive_mods_link", valeur)
            await interaction.response.send_message(f"Lien Google Drive mis à jour", ephemeral=True)

async def setup(bot, config):
    """Fonction pour ajouter les slash commands admin au bot"""
    await bot.add_cog(SlashAdminCommands(bot, config))
