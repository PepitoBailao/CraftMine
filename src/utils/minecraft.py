from mcstatus import JavaServer
from typing import Optional, Dict, Any

class MinecraftServerManager:
    def __init__(self, config):
        self.config = config
    
    def get_server(self) -> JavaServer:
        """Récupère l'instance du serveur Minecraft"""
        return JavaServer.lookup(self.config.server_address)
    
    async def get_status(self) -> Dict[str, Any]:
        """Récupère le statut du serveur"""
        try:
            server = self.get_server()
            status = server.status()
            
            return {
                "online": True,
                "players_online": status.players.online,
                "players_max": status.players.max,
                "version": status.version.name if hasattr(status.version, 'name') else "Inconnue",
                "latency": status.latency,
                "description": status.description
            }
        except Exception as e:
            return {
                "online": False,
                "error": str(e)
            }
    
    async def get_players(self) -> Dict[str, Any]:
        """Récupère la liste des joueurs connectés"""
        try:
            server = self.get_server()
            query = server.query()
            
            return {
                "success": True,
                "players": query.players.names if query.players.names else [],
                "count": len(query.players.names) if query.players.names else 0
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "players": [],
                "count": 0
            }
    
    async def get_mods(self) -> Dict[str, Any]:
        """Récupère la liste des mods installés sur le serveur"""
        try:
            # Méthode 1: Lire le dossier mods local (si le bot est sur le même serveur)
            mods_list = []
            
            # Chercher le dossier mods
            import os
            from pathlib import Path
            
            configured_path = self.config.get("mods_folder_path", "./mods")
            
            # Expander le chemin home si nécessaire
            if configured_path.startswith("~"):
                configured_path = str(Path(configured_path).expanduser())
            
            possible_paths = [
                configured_path,
                "./mods",
                "../mods",
                "mods",
                "/home/ubuntu/mods",
                "/home/minecraft/mods", 
                "/home/minecraft/server/mods",
                "/opt/minecraft/mods",
                "/srv/minecraft/mods",
                str(Path.home() / "mods")
            ]
            
            import os
            mods_folder = None
            for path in possible_paths:
                if os.path.exists(path) and os.path.isdir(path):
                    mods_folder = path
                    break
            
            if mods_folder:
                # Lire les fichiers .jar dans le dossier mods
                for filename in os.listdir(mods_folder):
                    if filename.endswith('.jar'):
                        # Nettoyer le nom du mod (enlever .jar et versions)
                        mod_name = filename.replace('.jar', '')
                        mod_name = self._clean_mod_filename(mod_name)
                        if mod_name:
                            mods_list.append(mod_name)
            
            # Méthode 2: Essayer la query Minecraft en fallback
            if not mods_list:
                try:
                    server = self.get_server()
                    query = server.query()
                    
                    # Bukkit/Spigot/Paper plugins
                    if hasattr(query, 'software') and hasattr(query.software, 'plugins'):
                        if query.software.plugins:
                            mods_list.extend(query.software.plugins)
                    
                    # Données brutes
                    if hasattr(query, 'raw'):
                        raw_data = query.raw
                        
                        # Forge/NeoForge
                        for key in ['modlist', 'forge_mods', 'mods', 'forgemods']:
                            if key in raw_data and raw_data[key]:
                                if isinstance(raw_data[key], list):
                                    mods_list.extend(raw_data[key])
                                elif isinstance(raw_data[key], dict):
                                    mods_list.extend(raw_data[key].keys())
                        
                        # Fabric/Quilt
                        for key in ['fabric_mods', 'fabricmods', 'quilt_mods', 'quiltmods']:
                            if key in raw_data and raw_data[key]:
                                if isinstance(raw_data[key], list):
                                    mods_list.extend(raw_data[key])
                                elif isinstance(raw_data[key], dict):
                                    mods_list.extend(raw_data[key].keys())
                        
                        # Plugins
                        if 'plugins' in raw_data and raw_data['plugins']:
                            if isinstance(raw_data['plugins'], list):
                                mods_list.extend(raw_data['plugins'])
                            elif isinstance(raw_data['plugins'], dict):
                                mods_list.extend(raw_data['plugins'].keys())
                except:
                    pass  # Ignore les erreurs de query
            
            # Nettoyer et dédupliquer
            mods_list = [mod for mod in set(mods_list) if mod and str(mod).strip()]
            
            return {
                "success": True,
                "mods": mods_list,
                "count": len(mods_list),
                "source": "local_folder" if mods_folder else "query"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "mods": [],
                "count": 0
            }
    
    def format_status_message(self, status: Dict[str, Any]) -> str:
        """Formate le message de statut pour Discord"""
        if status["online"]:
            # Vérifier si le serveur est configuré comme ouvert
            server_open = self.config.get("server_open", True)
            open_status = "Ouvert" if server_open else "Fermé"
            
            return f"Serveur en ligne : {status['players_online']}/{status['players_max']} joueurs\nStatut : {open_status}"
        else:
            return f"Serveur hors ligne"
    
    def format_players_message(self, players_data: Dict[str, Any]) -> str:
        """Formate la liste des joueurs pour Discord"""
        if not players_data["success"]:
            return f"Erreur : {players_data['error']}"
        
        if players_data["count"] == 0:
            return "Aucun joueur connecté."
        
        players_list = ", ".join(players_data["players"])
        return f"Joueurs connectés ({players_data['count']}) : {players_list}"
    
    def format_mods_message(self, mods_data: Dict[str, Any]) -> str:
        """Formate la liste des mods pour Discord"""
        if not mods_data["success"]:
            return f"Erreur : {mods_data['error']}"
        
        if mods_data["count"] == 0:
            return "Aucun mod détecté. Utilisez `/chercher-mod <nom>` pour rechercher."
        
        message_parts = [f"**{mods_data['count']} mods installés :**\n"]
        
        mods_to_show = mods_data["mods"][:10] if mods_data["count"] > 10 else mods_data["mods"]
        
        for mod_name in mods_to_show:
            clean_name = self._clean_mod_name(str(mod_name))
            modrinth_link = f"https://modrinth.com/mod/{clean_name.lower().replace(' ', '-')}"
            curseforge_link = f"https://www.curseforge.com/minecraft/mc-mods/{clean_name.lower().replace(' ', '-')}"
            
            message_parts.append(f"• {mod_name} - [Modrinth]({modrinth_link}) | [CurseForge]({curseforge_link})")
        
        if mods_data["count"] > 10:
            message_parts.append(f"\n...et {mods_data['count'] - 10} autres")
        
        return "\n".join(message_parts)
    
    def _clean_mod_name(self, mod_name: str) -> str:
        """Nettoie le nom du mod pour créer des URLs valides"""
        import re
        cleaned = re.sub(r'\s*\([^)]*\)', '', mod_name)
        cleaned = re.sub(r'\s*v?\d+\.\d+.*$', '', cleaned)
        cleaned = re.sub(r'\s*-\s*\d+.*$', '', cleaned)
        return cleaned.strip()
    
    def _clean_mod_filename(self, filename: str) -> str:
        """Nettoie le nom de fichier de mod pour l'affichage"""
        import re
        
        # Mapping des noms spéciaux à garder
        special_names = {
            'fabric-api': 'Fabric API',
            'xaeros_minimap': 'Xaero\'s Minimap',
            'xaerosworldmap': 'Xaero\'s World Map',
            'betterf3': 'BetterF3',
            'betterstats': 'Better Stats',
            'betteradvancements': 'Better Advancements',
            'rightclickharvest': 'Right Click Harvest',
            'nochatreports': 'No Chat Reports',
            'immediatelyfast': 'Immediately Fast',
            'tradingpost': 'Trading Post',
            'merchantmarkers': 'Merchant Markers',
            'villagernames': 'Villager Names',
            'doubledoors': 'Double Doors',
            'sound-physics-remastered': 'Sound Physics Remastered',
            'dungeons-and-taverns': 'Dungeons and Taverns',
            'mcw-bridges': 'Macaw\'s Bridges',
            'chat_heads': 'Chat Heads',
            'entity_model_features': 'Entity Model Features',
            'entity_texture_features': 'Entity Texture Features',
            'lambdynamiclights': 'LambDynamicLights',
            'now-playing': 'Now Playing',
            'music-sync': 'Music Sync'
        }
        
        cleaned = filename.lower()
        
        # Enlever l'extension .jar
        cleaned = cleaned.replace('.jar', '')
        
        # Vérifier les noms spéciaux
        for key, value in special_names.items():
            if key in cleaned:
                return value
        
        # Enlever les versions communes
        cleaned = re.sub(r'-?fabric-?', '', cleaned)
        cleaned = re.sub(r'-?mc[\d\.]+', '', cleaned)
        cleaned = re.sub(r'-?\d+\.\d+[\.\d\+]*', '', cleaned)
        cleaned = re.sub(r'-?v[\d\.]+', '', cleaned)
        cleaned = re.sub(r'-(forge|quilt|neoforge|client|server)', '', cleaned)
        
        # Nettoyer les séparateurs
        cleaned = re.sub(r'[-_]+', ' ', cleaned)
        cleaned = cleaned.strip()
        
        if cleaned:
            # Capitaliser proprement
            words = cleaned.split()
            capitalized_words = []
            for word in words:
                if len(word) <= 3 and word.upper() in ['API', 'JEI', 'EMF', 'ETF']:
                    capitalized_words.append(word.upper())
                else:
                    capitalized_words.append(word.capitalize())
            return ' '.join(capitalized_words)
        
        return filename
    
    def create_mods_embed(self, mods_data: Dict[str, Any]):
        """Crée un embed Discord pour la liste des mods"""
        import discord
        
        if not mods_data["success"]:
            embed = discord.Embed(
                title="Erreur",
                description=f"Erreur : {mods_data['error']}",
                color=discord.Color.red()
            )
            return embed
        
        if mods_data["count"] == 0:
            embed = discord.Embed(
                title="Mods",
                description="Aucun mod détecté.",
                color=discord.Color.orange()
            )
            
            embed.add_field(
                name="Recherche",
                value="Utilisez `/chercher-mod <nom>` pour rechercher un mod spécifique",
                inline=False
            )
            
            # Ajouter le bouton vers le Google Drive
            view = discord.ui.View()
            button = discord.ui.Button(
                label="Télécharger tous les mods",
                url="https://drive.google.com/file/d/15fyhnpbRik6z5RC9Fbo26HLM-iEQC-Sy/view?usp=drive_link",
                style=discord.ButtonStyle.link
            )
            view.add_item(button)
            
            return embed, view
        
        embed = discord.Embed(
            title="Mods installés",
            description=f"**{mods_data['count']} mods détectés**",
            color=discord.Color.green()
        )
        
        mods_to_show = mods_data["mods"][:10] if mods_data["count"] > 10 else mods_data["mods"]
        
        mods_list = []
        for mod_name in mods_to_show:
            clean_name = self._clean_mod_name(mod_name)
            modrinth_url = clean_name.lower().replace(' ', '-').replace('_', '-')
            curseforge_url = clean_name.lower().replace(' ', '-').replace('_', '-')
            
            mod_line = f"**{mod_name}**\n"
            mod_line += f"[Modrinth](https://modrinth.com/mod/{modrinth_url}) • "
            mod_line += f"[CurseForge](https://www.curseforge.com/minecraft/mc-mods/{curseforge_url})"
            
            mods_list.append(mod_line)
        
        if len(mods_list) <= 5:
            embed.add_field(
                name="Liste",
                value="\n\n".join(mods_list),
                inline=False
            )
        else:
            embed.add_field(
                name="Liste (1/2)",
                value="\n\n".join(mods_list[:5]),
                inline=False
            )
            embed.add_field(
                name="Liste (2/2)",
                value="\n\n".join(mods_list[5:]),
                inline=False
            )
        
        if mods_data["count"] > 10:
            embed.add_field(
                name="Info",
                value=f"{mods_data['count'] - 10} autres mods non affichés",
                inline=False
            )
        
        # Ajouter le bouton vers le Google Drive
        view = discord.ui.View()
        button = discord.ui.Button(
            label="Télécharger tous les mods",
            url="https://drive.google.com/file/d/15fyhnpbRik6z5RC9Fbo26HLM-iEQC-Sy/view?usp=drive_link",
            style=discord.ButtonStyle.link
        )
        view.add_item(button)
        
        return embed, view
