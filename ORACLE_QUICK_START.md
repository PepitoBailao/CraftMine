# CraftMine Oracle Cloud - Commandes Rapides

## 🚀 Installation rapide

```bash
# Sur votre VM Oracle Cloud Ubuntu
curl -sSL https://raw.githubusercontent.com/PepitoBailao/CraftMine/main/deploy-oracle.sh | bash
```

## ⚙️ Configuration

```bash
# Éditer la configuration
nano ~/CraftMine/.env

# Démarrer le bot
sudo systemctl start craftmine-bot

# Vérifier le statut
sudo systemctl status craftmine-bot
```

## 📊 Surveillance

```bash
# Logs en temps réel
sudo journalctl -u craftmine-bot -f

# Statut du service
sudo systemctl status craftmine-bot

# Redémarrer le bot
sudo systemctl restart craftmine-bot
```

## 🔄 Mise à jour

```bash
# Script automatique
~/update-craftmine.sh

# Ou manuellement
cd ~/CraftMine && git pull && sudo systemctl restart craftmine-bot
```

## 🛠️ Dépannage

```bash
# Tester manuellement
cd ~/CraftMine
source .venv/bin/activate
python src/main.py

# Vérifier les erreurs
sudo journalctl -u craftmine-bot -n 50

# Réparer les permissions
sudo chown -R ubuntu:ubuntu ~/CraftMine
```
