# CraftMine Bot

Bot Discord pour surveiller un serveur Minecraft et fournir des informations aux joueurs.

## Fonctionnalités

- **Surveillance automatique** du serveur Minecraft
- **Commandes slash** et traditionnelles
- **Statut en temps réel** : joueurs connectés, état du serveur
- **Téléchargement des mods** via lien Google Drive configurable
- **Interface minimaliste** sans emojis

## Installation

### Prérequis
- Python 3.8+
- Serveur Minecraft accessible
- Bot Discord créé sur Discord Developer Portal

### Installation rapide
```bash
# Cloner le projet
git clone https://github.com/PepitoBailao/CraftMine.git
cd CraftMine

# Installer les dépendances
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows
pip install -r requirements.txt

# Configuration
cp .env.example .env
cp config.json.example config.json
# Éditer .env et config.json avec vos valeurs
```

## Configuration

### Fichier .env
```env
DISCORD_TOKEN=votre_token_discord
ADMIN_USER_ID=votre_id_discord
DEFAULT_SERVER_IP=ip_serveur_minecraft
```

### Fichier config.json
```json
{
    "server_ip": "votre.ip.minecraft",
    "server_port": 25565,
    "minecraft_version": "1.21.4",
    "google_drive_mods_link": "https://drive.google.com/votre_lien",
    "server_open": true
}
```

## Utilisation

### Démarrage
```bash
python3 src/main.py
```

### Démarrage en arrière-plan (Linux)
```bash
# Avec tmux
tmux new-session -d -s craftmine
tmux send-keys -t craftmine 'cd ~/CraftMine && source .venv/bin/activate && python3 src/main.py' Enter

# Avec nohup
nohup python3 src/main.py &
```

## Commandes

### Commandes publiques
- `/status` - Statut du serveur et joueurs connectés
- `/mods` - Lien de téléchargement des mods
- `/ip` - Adresse IP du serveur
- `/version` - Version Minecraft
- `/joueurs` - Liste des joueurs connectés
- `/aide` - Aide des commandes

### Commandes administrateur
- `/parametres` - Configuration du bot
  - `show` - Afficher la configuration
  - `setip` - Changer l'IP du serveur
  - `setversion` - Changer la version
  - `serveropen` - Définir si le serveur est ouvert
  - `drivelink` - Modifier le lien Google Drive
  - `reload` - Recharger la configuration
  - `test` - Tester la connexion au serveur

## Déploiement

### Avec systemd (Linux)
```bash
sudo nano /etc/systemd/system/craftmine.service
```

```ini
[Unit]
Description=CraftMine Discord Bot
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/CraftMine
Environment=PATH=/home/ubuntu/CraftMine/.venv/bin
ExecStart=/home/ubuntu/CraftMine/.venv/bin/python src/main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable craftmine
sudo systemctl start craftmine
```

## Structure du projet

```
CraftMine/
├── commands/           # Commandes Discord
│   ├── slash_commands.py   # Slash commands publiques
│   ├── slash_admin.py      # Slash commands admin
│   ├── public.py          # Commandes publiques traditionnelles
│   └── admin.py           # Commandes admin traditionnelles
├── config/            # Gestionnaire de configuration
│   └── settings.py
├── src/               # Code principal
│   ├── main.py        # Point d'entrée
│   └── utils/
│       └── minecraft.py   # Gestionnaire serveur Minecraft
├── .env.example       # Template variables d'environnement
├── config.json.example # Template configuration
└── requirements.txt   # Dépendances Python
```

## Dépendances

- discord.py >= 2.3.0
- mcstatus >= 11.0.0
- python-dotenv >= 1.0.0

## Licence

Ce projet est open source.
