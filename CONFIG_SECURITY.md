# Configuration Sécurisée - CraftMine Bot

## Fichiers de configuration

### .env (CONFIDENTIEL - Ne pas commiter)
Copiez `.env.example` vers `.env` et configurez :

```env
# Token de votre bot Discord
DISCORD_TOKEN=votre_token_discord_ici

# Votre ID utilisateur Discord pour les permissions admin
ADMIN_USER_ID=votre_id_discord_ici

# Configuration par défaut du serveur Minecraft
DEFAULT_SERVER_IP=votre_ip_serveur_minecraft
DEFAULT_SERVER_PORT=25565
DEFAULT_MINECRAFT_VERSION=1.20.1
```

### config.json (CONFIDENTIEL - Ne pas commiter)
Copiez `config.json.example` vers `config.json` et configurez :

```json
{
    "server_ip": "votre_ip_serveur_minecraft",
    "server_port": 25565,
    "minecraft_version": "1.20.1"
}
```

## Sécurité

### Fichiers à ne JAMAIS commiter :
- `.env` (contient le token Discord)
- `config.json` (contient l'IP de votre serveur)
- Tout fichier contenant des tokens, mots de passe, ou IPs privées

### Fichiers publics sécurisés :
- `.env.example` (placeholders uniquement)
- `config.json.example` (placeholders uniquement)
- Tous les fichiers de code source (anonymisés)

## Configuration pour le déploiement

### Local (développement)
1. Copiez les fichiers example vers les vrais fichiers
2. Configurez avec vos vraies valeurs
3. Testez localement

### Production (Oracle Cloud, etc.)
1. Créez le fichier `.env` directement sur le serveur
2. Configurez `config.json` avec les bonnes valeurs
3. Ne synchronisez jamais ces fichiers avec Git

## Vérification

Avant chaque commit, vérifiez :
```bash
git status
# S'assurer que .env et config.json n'apparaissent pas
```

Si ils apparaissent :
```bash
git reset HEAD .env config.json
```
