# Changelog - CraftMine Discord Bot

## Version 2.0.0 (31 Août 2025)

### ✨ Nouvelles fonctionnalités
- **Architecture modulaire** : Code réorganisé en modules séparés pour une meilleure maintenabilité
- **Commande d'aide** : `!aide` pour afficher toutes les commandes disponibles
- **Test de connexion** : `!parametres test` pour tester la connexion au serveur
- **Gestion d'erreurs améliorée** : Messages d'erreur plus informatifs
- **Documentation technique** : Guide complet du fonctionnement interne

### 🔧 Améliorations
- **Configuration centralisée** : Classe `Config` pour gérer tous les paramètres
- **Interface Minecraft** : Classe `MinecraftServerManager` pour l'interaction avec mcstatus
- **Messages formatés** : Emojis et formatage amélioré pour Discord
- **Environnement virtuel** : Configuration automatique avec toutes les dépendances
- **Script de lancement** : `start_bot.bat` pour un démarrage simple

### 📁 Structure du projet
```
CraftMine/
├── .github/copilot-instructions.md    # Instructions Copilot
├── config/settings.py                 # Gestion de configuration
├── src/main.py                        # Point d'entrée principal
├── src/utils/minecraft.py             # Utilitaires Minecraft
├── commands/public.py                 # Commandes publiques
├── commands/admin.py                  # Commandes administrateur
├── .env                               # Variables d'environnement
├── README.md                          # Documentation utilisateur
├── TECHNICAL.md                       # Documentation technique
└── start_bot.bat                      # Script de lancement
```

### 🛠️ Nouvelles commandes
- `!aide` / `!help` / `!h` - Affiche l'aide complète
- `!parametres test` - Teste la connexion au serveur (admin)
- `!parametres reload` - Recharge la configuration (admin)

### 🔒 Sécurité
- **Token sécurisé** : Stockage dans `.env` (non tracké par git)
- **Permissions admin** : Système de vérification par ID Discord
- **Gestion d'erreurs** : Prévention des crashes et messages informatifs

---

## Version 1.0.0 (Initiale)

### ✨ Fonctionnalités de base
- **Surveillance automatique** : Mise à jour du statut toutes les 30 secondes
- **Commandes de base** : status, ip, version, joueurs
- **Administration** : Modification de l'IP et de la version
- **Configuration** : Sauvegarde dans config.json
