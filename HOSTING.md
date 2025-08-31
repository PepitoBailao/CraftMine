# Guide d'hébergement - CraftMine Discord Bot

## 🚀 Options d'hébergement

### 1. **Railway** (⭐ Recommandé)
**Avantages :** Gratuit, simple, déploiement Git automatique
**Limites :** 500h/mois gratuit

#### Étapes :
1. Créer un compte sur [railway.app](https://railway.app)
2. Connecter votre repository GitHub
3. Ajouter les variables d'environnement :
   ```
   DISCORD_TOKEN=votre_token_ici
   DEFAULT_SERVER_IP=144.24.205.125
   DEFAULT_SERVER_PORT=25565
   DEFAULT_MINECRAFT_VERSION=1.24.1
   ```
4. Déployer automatiquement !

---

### 2. **Render** 
**Avantages :** Gratuit, simple
**Limites :** Service s'endort après 15min d'inactivité

#### Étapes :
1. Créer un compte sur [render.com](https://render.com)
2. Nouveau → Web Service
3. Connecter GitHub repository
4. Configuration :
   - **Build Command :** `pip install -r requirements.txt`
   - **Start Command :** `python src/main.py`
5. Ajouter variables d'environnement dans l'onglet Environment

---

### 3. **Heroku** (Payant depuis Nov 2022)
**Avantages :** Très stable
**Inconvénients :** Plus gratuit

#### Étapes :
1. Installer Heroku CLI
2. `heroku create nom-de-votre-app`
3. `heroku config:set DISCORD_TOKEN=votre_token`
4. `git push heroku main`

---

### 4. **VPS (Serveur privé)**
**Avantages :** Contrôle total, toujours actif
**Inconvénients :** Configuration manuelle

#### Fournisseurs recommandés :
- **OVH** (3-5€/mois)
- **DigitalOcean** (5$/mois)
- **Contabo** (4€/mois)

#### Étapes (Ubuntu) :
```bash
# Installer Python
sudo apt update
sudo apt install python3 python3-pip git

# Cloner le projet
git clone https://github.com/votre-username/CraftMine.git
cd CraftMine

# Installer dépendances
pip3 install -r requirements.txt

# Configurer .env
nano .env
# Ajouter votre token

# Lancer le bot
python3 src/main.py

# Pour le garder actif (optionnel)
sudo apt install screen
screen -S craftmine
python3 src/main.py
# Ctrl+A puis D pour détacher
```

---

### 5. **Docker (Avancé)**
**Avantages :** Portable, isolé
**Usage :** Sur VPS ou services cloud

```bash
# Construire l'image
docker build -t craftmine-bot .

# Lancer le conteneur
docker run -d --name craftmine \
  -e DISCORD_TOKEN=votre_token \
  -e DEFAULT_SERVER_IP=144.24.205.125 \
  craftmine-bot
```

---

## 🔧 **Configuration des variables d'environnement**

Sur toutes les plateformes, définissez ces variables :

```env
DISCORD_TOKEN=votre_token_discord
DEFAULT_SERVER_IP=144.24.205.125
DEFAULT_SERVER_PORT=25565
DEFAULT_MINECRAFT_VERSION=1.24.1
```

## 📊 **Comparaison des services**

| Service | Prix | Uptime | Facilité | Recommandé pour |
|---------|------|--------|----------|-----------------|
| Railway | Gratuit (500h) | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Débutants |
| Render | Gratuit (limité) | ⭐⭐⭐ | ⭐⭐⭐⭐ | Test/développement |
| VPS | 3-5€/mois | ⭐⭐⭐⭐⭐ | ⭐⭐ | Production |
| Docker | Variable | ⭐⭐⭐⭐ | ⭐ | Experts |

## 💡 **Conseils**

### Pour débuter :
1. **Commencez avec Railway** (le plus simple)
2. Testez avec le serveur Discord de développement
3. Surveillez les logs pour détecter les erreurs

### Pour la production :
1. **VPS recommandé** pour un bot utilisé 24/7
2. Configurez un monitoring (UptimeRobot)
3. Sauvegardez votre configuration

### Sécurité :
- ⚠️ **JAMAIS** de token dans le code
- ✅ Toujours utiliser les variables d'environnement
- ✅ Activer l'authentification 2FA sur vos comptes

## 🆘 **Dépannage**

### Bot se déconnecte souvent :
- Vérifiez les logs d'erreurs
- Augmentez la mémoire allouée
- Vérifiez la stabilité réseau

### Slash commands ne s'affichent pas :
- Attendez jusqu'à 1h pour la synchronisation
- Vérifiez les permissions du bot
- Relancez le bot pour forcer la sync

### Erreurs de connexion Minecraft :
- Vérifiez que l'IP est accessible publiquement
- Testez avec `/parametres test`
- Vérifiez les règles firewall du serveur
