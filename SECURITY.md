# Guide de Sécurité - CraftMine Bot

## Variables d'environnement requises

Configurez ces variables dans votre fichier `.env` :

```env
# Token de votre bot Discord (OBLIGATOIRE)
DISCORD_TOKEN=your_discord_token_here

# Votre ID utilisateur Discord pour les permissions admin (OBLIGATOIRE)
ADMIN_USER_ID=your_discord_user_id_here

# Configuration du serveur Minecraft
DEFAULT_SERVER_IP=your_server_ip_here
DEFAULT_SERVER_PORT=25565
DEFAULT_MINECRAFT_VERSION=1.20.1
```

## Sécurisation

### 1. Token Discord
- Obtenez votre token sur https://discord.com/developers/applications
- **JAMAIS** ne partagez ce token ou ne le commitez dans Git
- Si compromis, régénérez-le immédiatement

### 2. ID Administrateur
- Trouvez votre ID Discord : Mode développeur > Clic droit sur votre profil > Copier l'ID
- Seuls les utilisateurs avec cet ID peuvent utiliser les commandes admin

### 3. Configuration serveur
- Remplacez `your_server_ip_here` par l'IP de votre serveur Minecraft
- Le port 25565 est le port par défaut de Minecraft

## Déploiement sécurisé

1. **Copiez `.env.example` vers `.env`**
2. **Configurez toutes les variables**
3. **Vérifiez que `.env` est dans `.gitignore`**
4. **Ne commitez JAMAIS le fichier `.env`**

## En cas de compromission

1. Régénérez immédiatement votre token Discord
2. Changez votre configuration
3. Vérifiez les logs de votre bot
4. Examinez l'historique Git pour les fuites

## Bonnes pratiques

- Utilisez des variables d'environnement pour TOUS les secrets
- Activez l'authentification 2FA sur vos comptes
- Surveillez les logs de votre bot
- Limitez les permissions du bot au strict nécessaire
