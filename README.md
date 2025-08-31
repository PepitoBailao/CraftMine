# CraftMine Discord Bot

Un bot Discord pour surveiller le statut de votre serveur Minecraft.

## Rôle et fonctionnement du bot

Ton bot Discord sert à surveiller et administrer un serveur Minecraft directement depuis un salon Discord.

**Technologies utilisées :**
- `discord.py` - Interface avec l'API Discord
- `mcstatus` - Interrogation des serveurs Minecraft (status et query)
- `python-dotenv` - Gestion sécurisée des variables d'environnement

## Fonctionnalités

### 🌐 Surveillance automatique
- ✅ Mise à jour du statut Discord toutes les 30 secondes
- ✅ Affichage en temps réel : "X/Y joueurs en ligne" ou "Serveur hors ligne"
- ✅ Statut Discord adapté (🟢 en ligne / 🔴 hors ligne)

### 👥 Commandes publiques (accessibles à tous)
- ✅ `!status` - Vérifie si le serveur est en ligne + nombre de joueurs
- ✅ `!ip` - Affiche l'adresse IP et le port du serveur
- ✅ `!version` - Affiche la version Minecraft configurée
- ✅ `!joueurs` - Liste des pseudos connectés (via server.query())

### ⚙️ Commandes administrateur (réservées aux ADMIN_IDS)
- ✅ `!parametres` - Affiche la configuration actuelle
- ✅ `!parametres setip <ip> [port]` - Met à jour l'adresse du serveur
- ✅ `!parametres setversion <version>` - Met à jour la version affichée
- ✅ `!parametres reload` - Recharge la configuration depuis le fichier

### 💾 Persistance des données
- ✅ Configuration sauvegardée dans `config.json`
- ✅ Paramètres persistants entre les redémarrages
- ✅ Gestion sécurisée des tokens via variables d'environnement

## Installation

1. **Cloner ou télécharger le projet**
   ```bash
   git clone <votre-repo>
   cd CraftMine
   ```

2. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configuration**
   - Copiez `.env.example` vers `.env`
   - Remplissez votre token Discord dans le fichier `.env`
   ```bash
   cp .env.example .env
   # Éditez .env avec votre token
   ```

4. **Lancer le bot**
   ```bash
   python src/main.py
   ```

## Configuration

### Variables d'environnement (.env)
- `DISCORD_TOKEN` : Token de votre bot Discord
- `DEFAULT_SERVER_IP` : IP par défaut du serveur Minecraft
- `DEFAULT_SERVER_PORT` : Port par défaut (25565)
- `DEFAULT_MINECRAFT_VERSION` : Version affichée par défaut

### Fichier config.json
Le bot crée automatiquement un fichier `config.json` avec les paramètres du serveur Minecraft. Ces paramètres peuvent être modifiés via les commandes admin.

## Commandes détaillées

### 👥 Commandes publiques
Toutes ces commandes sont accessibles à tous les utilisateurs du serveur Discord.

| Commande | Description | Exemple d'utilisation |
|----------|-------------|----------------------|
| `!status` | Vérifie l'état du serveur et affiche le nombre de joueurs | `!status` → "🟢 Serveur en ligne : 3/20 joueurs" |
| `!ip` | Affiche l'adresse IP et le port du serveur | `!ip` → "🌐 IP du serveur : `play.example.com:25565`" |
| `!version` | Affiche la version Minecraft configurée | `!version` → "⚙️ Version Minecraft définie : `1.20.1`" |
| `!joueurs` | Liste les pseudos des joueurs connectés | `!joueurs` → "👥 Joueurs connectés (3) : Steve, Alex, Notch" |

### ⚙️ Commandes administrateur
Ces commandes sont réservées aux utilisateurs dont l'ID Discord est dans la liste `ADMIN_IDS`.

| Commande | Description | Exemple d'utilisation |
|----------|-------------|----------------------|
| `!parametres` | Affiche tous les paramètres actuels | `!parametres` |
| `!parametres setip <ip> [port]` | Change l'IP du serveur (port optionnel, défaut: 25565) | `!parametres setip play.example.com 25566` |
| `!parametres setversion <version>` | Change la version Minecraft affichée | `!parametres setversion 1.20.1` |
| `!parametres reload` | Recharge la config depuis le fichier | `!parametres reload` |

### 🔒 Gestion des permissions
- Les IDs des administrateurs sont définis dans `config/settings.py`
- Par défaut : `[448420884059914240]` (à modifier selon vos besoins)
- Les commandes admin retournent "❌ Vous n'avez pas la permission" aux autres utilisateurs

## Structure du projet

```
CraftMine/
├── .github/
│   └── copilot-instructions.md
├── src/
│   ├── main.py              # Point d'entrée principal
│   ├── bot.py               # Configuration du bot
│   └── utils/
│       └── minecraft.py     # Utilitaires Minecraft
├── commands/
│   ├── public.py            # Commandes publiques
│   └── admin.py             # Commandes admin
├── config/
│   └── settings.py          # Gestion de la configuration
├── .env.example             # Exemple de variables d'environnement
├── .env                     # Variables d'environnement (non tracké)
├── .gitignore              # Fichiers ignorés par git
├── requirements.txt         # Dépendances Python
└── README.md               # Ce fichier
```

## Développement

### Ajouter de nouvelles commandes
1. Créez votre commande dans le dossier `commands/`
2. Importez et enregistrez la commande dans `src/main.py`

### Contribuer
1. Fork le projet
2. Créez une branche pour votre fonctionnalité
3. Committez vos changements
4. Poussez vers la branche
5. Ouvrez une Pull Request

## Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.
