# CraftMine Discord Bot

Bot Discord pour surveiller le statut de votre serveur Minecraft.

## � Installation

1. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configuration**
   - Copiez `.env.example` vers `.env`
   - Ajoutez votre token Discord dans `.env`

3. **Lancer le bot**
   ```bash
   python src/main.py
   ```
   Ou utilisez `start_bot.bat` sur Windows

## 📋 Commandes

### Slash Commands (recommandé)
- `/status` - État du serveur et nombre de joueurs
- `/joueurs` - Liste des joueurs connectés
- `/ip` - Adresse IP du serveur
- `/version` - Version Minecraft
- `/aide` - Aide des commandes
- `/parametres` - Configuration (admin uniquement)

### Commandes classiques (avec !)
- `!status`, `!joueurs`, `!ip`, `!version`, `!aide`
- `!parametres` - Configuration admin

## ⚙️ Configuration

Le bot crée automatiquement un fichier `config.json` avec les paramètres du serveur Minecraft. Ces paramètres peuvent être modifiés via les commandes admin.

### Variables d'environnement (.env)
```env
DISCORD_TOKEN=votre_token_discord
DEFAULT_SERVER_IP=votre.serveur.minecraft
DEFAULT_SERVER_PORT=25565
DEFAULT_MINECRAFT_VERSION=1.20.1
```

## 🔧 Fonctionnalités

- ✅ Surveillance automatique toutes les 30 secondes
- ✅ Statut Discord en temps réel
- ✅ Slash commands modernes
- ✅ Configuration persistante
- ✅ Gestion d'erreurs robuste
