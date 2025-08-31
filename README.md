# CraftMine Discord Bot

Un bot Discord moderne pour surveiller votre serveur Minecraft avec des commandes traditionnelles et des slash commands.

## Configuration

### 1. Pré-requis
- Python 3.11+
- Un bot Discord configuré
- Un serveur Minecraft

### 2. Installation

```bash
# Cloner le projet
git clone https://github.com/PepitoBailao/CraftMine.git
cd CraftMine

# Créer l'environnement virtuel
python -m venv .venv
.venv\Scripts\activate  # Windows
# ou source .venv/bin/activate  # Linux/Mac

# Installer les dépendances
pip install -r requirements.txt

# Configurer les variables d'environnement
cp .env.example .env
# Éditez .env avec vos informations
```

### 3. Configuration des variables

Éditez le fichier `.env` :

```env
DISCORD_TOKEN=votre_token_discord
ADMIN_USER_ID=votre_id_discord
DEFAULT_SERVER_IP=votre_ip_serveur_minecraft
DEFAULT_SERVER_PORT=25565
DEFAULT_MINECRAFT_VERSION=1.20.1
```

## Commandes disponibles

### Commandes publiques
- `!status` ou `/status` - Statut du serveur
- `!ip` ou `/ip` - Affiche l'IP du serveur
- `!version` ou `/version` - Version Minecraft
- `!joueurs` ou `/joueurs` - Liste des joueurs connectés
- `!aide` ou `/aide` - Aide

### Commandes administrateur
- `!parametres ip <nouvelle_ip>` - Changer l'IP
- `!parametres version <version>` - Changer la version
- `!parametres test` - Tester la connexion
- `/admin config` - Configuration via slash command

## Démarrage

```bash
# Windows
start_bot.bat

# Ou directement
python src/main.py
```

## Structure du projet

```
CraftMine/
├── src/
│   ├── main.py              # Point d'entrée
│   └── utils/
│       └── minecraft.py     # Gestion Minecraft
├── commands/
│   ├── public.py           # Commandes publiques
│   ├── admin.py            # Commandes admin
│   ├── slash_commands.py   # Slash commands publiques
│   └── slash_admin.py      # Slash commands admin
├── config/
│   └── settings.py         # Configuration
└── .env                    # Variables d'environnement
```

## Sécurité

- Tous les secrets sont dans `.env` (non commité)
- Permissions admin basées sur l'ID Discord
- Configuration séparée du code source
- Voir `SECURITY.md` pour plus de détails

## Support

Pour des questions ou problèmes, consultez la documentation ou créez une issue.
