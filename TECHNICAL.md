# Documentation technique - CraftMine Bot

## Architecture du projet

### 📁 Structure modulaire

Le bot est organisé en modules séparés pour faciliter la maintenance et l'évolution :

```
├── config/settings.py      # Gestion centralisée de la configuration
├── src/main.py            # Point d'entrée et orchestration
├── src/utils/minecraft.py # Logique métier Minecraft
├── commands/public.py     # Commandes accessibles à tous
└── commands/admin.py      # Commandes administrateur
```

### 🔧 Classes principales

#### `Config` (config/settings.py)
- Gestion centralisée de la configuration
- Chargement automatique depuis `.env` et `config.json`
- Sauvegarde automatique des modifications
- Valeurs par défaut depuis les variables d'environnement

#### `MinecraftServerManager` (src/utils/minecraft.py)
- Interface avec la librairie `mcstatus`
- Méthodes `get_status()` et `get_players()`
- Formatage des messages pour Discord
- Gestion des erreurs de connexion

#### `CraftMineBot` (src/main.py)
- Orchestration principale du bot Discord
- Gestion des événements et des tâches
- Chargement dynamique des modules de commandes

## 🔄 Fonctionnement des tâches automatiques

### Mise à jour du statut (toutes les 30 secondes)
```python
@tasks.loop(seconds=30)
async def update_status(self):
    status = await self.minecraft_manager.get_status()
    if status["online"]:
        activity = discord.Game(name=f"{status['players_online']}/{status['players_max']} joueurs")
        discord_status = discord.Status.online
    else:
        activity = discord.Game(name="Serveur hors ligne")
        discord_status = discord.Status.dnd
    
    await self.bot.change_presence(activity=activity, status=discord_status)
```

## 📡 Interrogation des serveurs Minecraft

### Deux méthodes d'interrogation

1. **Status Query** (`server.status()`)
   - Informations de base : joueurs en ligne/max, latence
   - Disponible sur tous les serveurs Minecraft
   - Utilisé pour `!status`

2. **Full Query** (`server.query()`)
   - Informations détaillées : liste des joueurs, plugins, etc.
   - Nécessite `enable-query=true` dans server.properties
   - Utilisé pour `!joueurs`

### Gestion d'erreurs
```python
try:
    server = JavaServer.lookup(address)
    status = server.status()
    return {"online": True, "players_online": status.players.online, ...}
except Exception as e:
    return {"online": False, "error": str(e)}
```

## 🔐 Sécurité et configuration

### Variables d'environnement (.env)
```env
DISCORD_TOKEN=votre_token_ici              # Token du bot Discord
DEFAULT_SERVER_IP=144.24.205.125           # IP par défaut
DEFAULT_SERVER_PORT=25565                  # Port par défaut
DEFAULT_MINECRAFT_VERSION=1.20.1           # Version par défaut
```

### Configuration runtime (config.json)
```json
{
    "server_ip": "144.24.205.125",
    "server_port": 25565,
    "minecraft_version": "1.20.1"
}
```

### Permissions administrateur
- IDs Discord stockés dans `config.settings.Config.admin_ids`
- Vérification via le décorateur `@is_admin()`
- Messages d'erreur automatiques pour les non-autorisés

## 🚀 Extension du bot

### Ajouter de nouvelles commandes

1. **Commandes publiques** : Modifier `commands/public.py`
```python
@commands.command()
async def nouvelle_commande(self, ctx):
    await ctx.send("Nouvelle fonctionnalité !")
```

2. **Commandes admin** : Modifier `commands/admin.py`
```python
@commands.command()
@is_admin(admin_ids=[...])
async def admin_commande(self, ctx):
    await ctx.send("Commande administrateur !")
```

### Ajouter de nouveaux modules
1. Créer le fichier dans le dossier approprié
2. Ajouter la fonction `async def setup(bot, ...)`
3. Importer et appeler dans `src/main.py`

## 🐛 Debugging et logs

### Messages de démarrage
```
🤖 Bot connecté en tant que CraftMine#0517
📊 Serveur surveillé : 144.24.205.125:25565
✅ Commandes chargées avec succès
```

### Gestion d'erreurs
- Erreurs de commandes capturées et formatées
- Logs d'erreurs dans la console
- Messages utilisateur informatifs

### Monitoring
- Statut du bot visible dans Discord
- Logs de connexion/déconnexion
- Erreurs de connexion au serveur Minecraft affichées
