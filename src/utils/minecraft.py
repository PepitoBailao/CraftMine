from mcstatus import JavaServer
from typing import Optional, Dict, Any

class MinecraftServerManager:
    def __init__(self, config):
        self.config = config
    
    def get_server(self) -> JavaServer:
        """Récupère l'instance du serveur Minecraft"""
        return JavaServer.lookup(self.config.server_address)
    
    async def get_status(self) -> Dict[str, Any]:
        """
        Récupère le statut du serveur
        Retourne un dictionnaire avec les informations ou None si hors ligne
        """
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
        """
        Récupère la liste des joueurs connectés
        """
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
    
    def format_status_message(self, status: Dict[str, Any]) -> str:
        """Formate le message de statut pour Discord"""
        if status["online"]:
            return f"Serveur en ligne : {status['players_online']}/{status['players_max']} joueurs"
        else:
            return f"Serveur hors ligne ou injoignable"
    
    def format_players_message(self, players_data: Dict[str, Any]) -> str:
        """Formate la liste des joueurs pour Discord"""
        if not players_data["success"]:
            return f"Impossible de récupérer la liste des joueurs.\nErreur : `{players_data['error']}`"
        
        if players_data["count"] == 0:
            return "Aucun joueur connecté pour l'instant."
        
        players_list = ", ".join(players_data["players"])
        return f"Joueurs connectés ({players_data['count']}) : {players_list}"
