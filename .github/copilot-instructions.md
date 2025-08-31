# CraftMine Discord Bot

Bot Discord pour surveiller le statut d'un serveur Minecraft avec mise à jour automatique et slash commands.

## Structure
- `src/main.py` - Point d'entrée principal
- `commands/` - Modules de commandes Discord
- `config/settings.py` - Gestion de la configuration
- `.env` - Variables d'environnement

## Technologies
- Python 3.11+ avec environnement virtuel
- discord.py >=2.3.0 - API Discord avec slash commands
- mcstatus >=11.0.0 - Interrogation serveurs Minecraft
- python-dotenv >=1.0.0 - Variables d'environnement

## Fonctionnalités
- Surveillance automatique toutes les 30 secondes
- Slash commands modernes + commandes classiques
- Configuration persistante en JSON
- Gestion d'erreurs robuste
