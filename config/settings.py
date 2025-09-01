import json
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

class Config:
    def __init__(self, config_file="config.json"):
        self.config_file = config_file
        
        # Gestion sécurisée de l'ID admin
        admin_id_str = os.getenv("ADMIN_USER_ID", "0")
        try:
            self.admin_ids = [int(admin_id_str)] if admin_id_str.isdigit() else [0]
        except ValueError:
            print(f"⚠️  ADMIN_USER_ID invalide dans .env: '{admin_id_str}' - utilisez un ID numérique Discord")
            self.admin_ids = [0]
        
        self.token = os.getenv("DISCORD_TOKEN")
        
        # Valeurs par défaut depuis les variables d'environnement
        self.defaults = {
            "server_ip": os.getenv("DEFAULT_SERVER_IP", "localhost"),
            "server_port": int(os.getenv("DEFAULT_SERVER_PORT", "25565")),
            "minecraft_version": os.getenv("DEFAULT_MINECRAFT_VERSION", "1.20.1")
        }
        
        self.load_config()
    
    def load_config(self):
        """Charge ou crée le fichier de configuration"""
        if not os.path.exists(self.config_file):
            self.config = self.defaults.copy()
            self.save_config()
        else:
            with open(self.config_file, "r") as f:
                self.config = json.load(f)
    
    def save_config(self):
        """Sauvegarde la configuration dans le fichier JSON"""
        with open(self.config_file, "w") as f:
            json.dump(self.config, f, indent=4)
    
    def get(self, key, default=None):
        """Récupère une valeur de configuration"""
        return self.config.get(key, default)
    
    def set(self, key, value):
        """Définit une valeur de configuration"""
        self.config[key] = value
        self.save_config()
    
    @property
    def server_address(self):
        """Retourne l'adresse complète du serveur"""
        return f"{self.config['server_ip']}:{self.config['server_port']}"
