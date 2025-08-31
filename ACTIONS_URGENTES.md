# ACTIONS CRITIQUES - À FAIRE IMMÉDIATEMENT

## 🚨 URGENT - Sécurité compromise

Votre token Discord était exposé dans le code source Git. Voici les actions à effectuer IMMÉDIATEMENT :

### 1. Régénérer le token Discord (URGENT)
1. Allez sur https://discord.com/developers/applications
2. Sélectionnez votre application/bot
3. Bot → Token → Regenerate
4. Copiez le NOUVEAU token
5. Mettez-le dans votre fichier `.env` local (JAMAIS dans Git)

### 2. Configurer vos variables d'environnement
Éditez le fichier `.env` avec VOS vraies valeurs :

```env
DISCORD_TOKEN=VOTRE_NOUVEAU_TOKEN_ICI
ADMIN_USER_ID=VOTRE_ID_DISCORD_ICI
DEFAULT_SERVER_IP=VOTRE_IP_SERVEUR_ICI
DEFAULT_SERVER_PORT=25565
DEFAULT_MINECRAFT_VERSION=1.20.1
```

### 3. Trouver votre ID Discord
1. Discord → Paramètres → Avancé → Mode développeur (ON)
2. Clic droit sur votre profil → Copier l'ID
3. Mettez cet ID dans `ADMIN_USER_ID`

### 4. Vérifier la sécurité
- ✅ Le fichier `.env` est dans `.gitignore` 
- ✅ Les données sensibles ont été supprimées du code
- ✅ Les fichiers d'hébergement supprimés
- ❌ **VOUS DEVEZ RÉGÉNÉRER LE TOKEN DISCORD**

### 5. Avant de pousser sur GitHub
```bash
# Vérifiez que .env n'est pas tracké
git status

# Si .env apparaît dans "Changes to be committed", alors :
git reset HEAD .env
```

## 📋 Changements effectués

- ✅ Token Discord anonymisé
- ✅ IP du serveur anonymisée  
- ✅ ID admin rendu configurable
- ✅ Fichiers d'hébergement supprimés
- ✅ `.gitignore` renforcé
- ✅ Guide de sécurité créé (`SECURITY.md`)
- ✅ README mis à jour

## ⚠️ Points d'attention

1. **JAMAIS** commiter le fichier `.env` 
2. **TOUJOURS** utiliser des variables d'environnement pour les secrets
3. **IMMÉDIATEMENT** régénérer tout token compromis
4. **VÉRIFIER** avant chaque commit que pas de données sensibles
