# Déploiement CraftMine Bot sur Oracle Cloud

## Guide complet pour héberger sur Oracle Cloud VM

### Pré-requis

- VM Oracle Cloud (Always Free tier recommandé)
- Ubuntu 20.04/22.04 LTS
- Accès SSH à votre VM
- Votre bot Discord configuré localement

## Étape 1 : Préparation de la VM Oracle Cloud

### Connexion SSH
```bash
ssh -i votre_cle_privee.pem ubuntu@adresse_ip_vm
```

### Mise à jour du système
```bash
sudo apt update && sudo apt upgrade -y
```

### Installation des dépendances
```bash
# Python 3.11 et pip
sudo apt install python3.11 python3.11-venv python3.11-dev python3-pip git curl -y

# Vérification
python3.11 --version
```

## Étape 2 : Déploiement du code

### Cloner le projet
```bash
cd ~
git clone https://github.com/PepitoBailao/CraftMine.git
cd CraftMine
```

### Créer l'environnement virtuel
```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

### Installer les dépendances
```bash
pip install -r requirements.txt
```

## Étape 3 : Configuration

### Créer le fichier .env
```bash
cp .env.example .env
nano .env
```

Configurez avec vos vraies valeurs :
```env
DISCORD_TOKEN=votre_token_discord_ici
ADMIN_USER_ID=votre_id_discord_ici
DEFAULT_SERVER_IP=votre_ip_serveur_minecraft
DEFAULT_SERVER_PORT=25565
DEFAULT_MINECRAFT_VERSION=1.20.1
```

### Configurer config.json
```bash
nano config.json
```

```json
{
    "server_ip": "votre_ip_serveur_minecraft",
    "server_port": 25565,
    "minecraft_version": "1.20.1"
}
```

## Étape 4 : Service systemd (Démarrage automatique)

### Créer le service
```bash
sudo nano /etc/systemd/system/craftmine-bot.service
```

```ini
[Unit]
Description=CraftMine Discord Bot
After=network.target
Wants=network-online.target

[Service]
Type=simple
User=ubuntu
Group=ubuntu
WorkingDirectory=/home/ubuntu/CraftMine
Environment=PATH=/home/ubuntu/CraftMine/.venv/bin
ExecStart=/home/ubuntu/CraftMine/.venv/bin/python /home/ubuntu/CraftMine/src/main.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

### Activer et démarrer le service
```bash
# Recharger systemd
sudo systemctl daemon-reload

# Activer le service (démarrage automatique)
sudo systemctl enable craftmine-bot

# Démarrer le service
sudo systemctl start craftmine-bot

# Vérifier le statut
sudo systemctl status craftmine-bot
```

## Étape 5 : Surveillance et logs

### Voir les logs en temps réel
```bash
sudo journalctl -u craftmine-bot -f
```

### Commandes utiles
```bash
# Redémarrer le bot
sudo systemctl restart craftmine-bot

# Arrêter le bot
sudo systemctl stop craftmine-bot

# Voir les logs des dernières 24h
sudo journalctl -u craftmine-bot --since "24 hours ago"

# Voir le statut détaillé
sudo systemctl status craftmine-bot -l
```

## Étape 6 : Configuration du pare-feu Oracle Cloud

### Dans la console Oracle Cloud

1. **Navigation :** Compute → Instances → Votre VM
2. **Réseaux :** Virtual Cloud Networks → Votre VCN
3. **Sécurité :** Security Lists → Default Security List
4. **Règles :** Ingress Rules → Add Ingress Rules

### Ports à ouvrir (si nécessaire)
```
Source: 0.0.0.0/0
Protocol: TCP
Port: 22 (SSH - déjà ouvert normalement)
```

**Note :** Le bot Discord n'a besoin d'aucun port entrant spécifique, seulement sortant vers Discord.

## Étape 7 : Mise à jour automatique

### Script de mise à jour
```bash
nano ~/update-craftmine.sh
```

```bash
#!/bin/bash
cd /home/ubuntu/CraftMine
git pull
source .venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart craftmine-bot
echo "CraftMine bot mis à jour et redémarré"
```

```bash
chmod +x ~/update-craftmine.sh
```

### Utilisation
```bash
# Mettre à jour le bot
~/update-craftmine.sh
```

## Étape 8 : Monitoring (Optionnel)

### Script de surveillance
```bash
nano ~/check-craftmine.sh
```

```bash
#!/bin/bash
if ! systemctl is-active --quiet craftmine-bot; then
    echo "$(date): CraftMine bot arrêté, redémarrage..." >> ~/craftmine.log
    sudo systemctl start craftmine-bot
fi
```

### Crontab pour vérification automatique
```bash
crontab -e
```

Ajouter :
```bash
# Vérifier le bot toutes les 5 minutes
*/5 * * * * /home/ubuntu/check-craftmine.sh
```

## Étape 9 : Sécurité

### Sauvegarder les configurations
```bash
# Créer un dossier de backup
mkdir ~/backup

# Sauvegarder les configs importantes
cp .env ~/backup/.env.backup
cp config.json ~/backup/config.json.backup
```

### Mise à jour automatique du système
```bash
sudo apt install unattended-upgrades -y
sudo dpkg-reconfigure unattended-upgrades
```

## Étape 10 : Vérification finale

### Test du bot
```bash
# Vérifier que le service tourne
sudo systemctl status craftmine-bot

# Voir les logs de démarrage
sudo journalctl -u craftmine-bot -n 50

# Tester dans Discord
# Utiliser /status ou !status
```

## Commandes de maintenance rapide

```bash
# Statut du bot
sudo systemctl status craftmine-bot

# Redémarrer le bot
sudo systemctl restart craftmine-bot

# Logs en temps réel
sudo journalctl -u craftmine-bot -f

# Mettre à jour le bot
cd ~/CraftMine && git pull && sudo systemctl restart craftmine-bot

# Espace disque
df -h

# Mémoire utilisée
free -h

# Processus du bot
ps aux | grep python
```

## Avantages Oracle Cloud Always Free

- **2 VMs AMD** : 1/8 OCPU, 1GB RAM chacune
- **Gratuit à vie** : Pas de limite de temps
- **Boot Volume** : 47GB de stockage
- **Bande passante** : 10TB/mois
- **IP publique** : Incluse
- **Uptime** : Excellent (datacenter Oracle)

## Dépannage

### Bot ne démarre pas
```bash
# Vérifier les logs d'erreur
sudo journalctl -u craftmine-bot -n 100

# Tester manuellement
cd ~/CraftMine
source .venv/bin/activate
python src/main.py
```

### Problèmes de permissions
```bash
# Réparer les permissions
sudo chown -R ubuntu:ubuntu /home/ubuntu/CraftMine
chmod +x /home/ubuntu/CraftMine/src/main.py
```

### Bot se déconnecte souvent
```bash
# Vérifier la mémoire
free -h

# Vérifier les logs système
sudo journalctl -f
```

## Résultat attendu

Une fois terminé, votre bot sera :
- **Toujours en ligne** (24/7)
- **Redémarrage automatique** en cas de crash
- **Mise à jour facile** avec git pull
- **Logs centralisés** avec journalctl
- **Gratuit à vie** sur Oracle Cloud
- **Performances excellentes** pour un bot Discord

Votre bot CraftMine sera accessible dans Discord avec toutes ses fonctionnalités !
