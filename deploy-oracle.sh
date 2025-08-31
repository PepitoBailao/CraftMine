#!/bin/bash
# Script d'installation automatique pour Oracle Cloud
# Usage: bash deploy-oracle.sh

echo "🌩️  Installation CraftMine Bot sur Oracle Cloud"
echo "=============================================="

# Vérifier si on est sur Ubuntu
if [[ ! -f /etc/lsb-release ]]; then
    echo "❌ Ce script est conçu pour Ubuntu"
    exit 1
fi

# Mise à jour du système
echo "📦 Mise à jour du système..."
sudo apt update && sudo apt upgrade -y

# Installation des dépendances
echo "⚙️  Installation des dépendances..."
sudo apt install python3.11 python3.11-venv python3.11-dev python3-pip git curl nano -y

# Vérification Python
python3.11 --version
if [ $? -ne 0 ]; then
    echo "❌ Erreur : Python 3.11 non installé correctement"
    exit 1
fi

# Navigation vers le dossier home
cd ~

# Cloner le projet (si pas déjà fait)
if [ ! -d "CraftMine" ]; then
    echo "📥 Clonage du projet depuis GitHub..."
    git clone https://github.com/PepitoBailao/CraftMine.git
    cd CraftMine
else
    echo "📁 Projet déjà présent, mise à jour..."
    cd CraftMine
    git pull
fi

# Créer l'environnement virtuel
echo "🐍 Création de l'environnement virtuel..."
python3.11 -m venv .venv
source .venv/bin/activate

# Installer les dépendances Python
echo "📦 Installation des dépendances Python..."
pip install -r requirements.txt

# Créer le fichier .env depuis l'exemple
if [ ! -f ".env" ]; then
    echo "⚙️  Création du fichier .env..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANT: Vous devez maintenant éditer le fichier .env"
    echo "   Commande: nano ~/.CraftMine/.env"
    echo ""
    echo "   Configurez ces variables:"
    echo "   - DISCORD_TOKEN=votre_token_discord"
    echo "   - ADMIN_USER_ID=votre_id_discord"
    echo "   - DEFAULT_SERVER_IP=votre_ip_minecraft"
    echo ""
fi

# Créer le service systemd
echo "🔄 Configuration du service systemd..."
sudo tee /etc/systemd/system/craftmine-bot.service > /dev/null <<EOF
[Unit]
Description=CraftMine Discord Bot
After=network.target
Wants=network-online.target

[Service]
Type=simple
User=$USER
Group=$USER
WorkingDirectory=$HOME/CraftMine
Environment=PATH=$HOME/CraftMine/.venv/bin
ExecStart=$HOME/CraftMine/.venv/bin/python $HOME/CraftMine/src/main.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

# Recharger systemd
sudo systemctl daemon-reload

# Activer le service (démarrage automatique)
sudo systemctl enable craftmine-bot

# Créer le script de mise à jour
echo "📝 Création du script de mise à jour..."
tee ~/update-craftmine.sh > /dev/null <<EOF
#!/bin/bash
cd ~/CraftMine
git pull
source .venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart craftmine-bot
echo "CraftMine bot mis à jour et redémarré"
EOF

chmod +x ~/update-craftmine.sh

# Créer le script de surveillance
echo "👁️  Création du script de surveillance..."
tee ~/check-craftmine.sh > /dev/null <<EOF
#!/bin/bash
if ! systemctl is-active --quiet craftmine-bot; then
    echo "\$(date): CraftMine bot arrêté, redémarrage..." >> ~/craftmine.log
    sudo systemctl start craftmine-bot
fi
EOF

chmod +x ~/check-craftmine.sh

echo ""
echo "✅ Installation terminée !"
echo ""
echo "📋 Prochaines étapes :"
echo "1. Éditez le fichier .env avec vos configurations :"
echo "   nano ~/CraftMine/.env"
echo ""
echo "2. Démarrez le bot :"
echo "   sudo systemctl start craftmine-bot"
echo ""
echo "3. Vérifiez le statut :"
echo "   sudo systemctl status craftmine-bot"
echo ""
echo "4. Voir les logs :"
echo "   sudo journalctl -u craftmine-bot -f"
echo ""
echo "🔧 Commandes utiles :"
echo "   Redémarrer : sudo systemctl restart craftmine-bot"
echo "   Arrêter    : sudo systemctl stop craftmine-bot"
echo "   Logs       : sudo journalctl -u craftmine-bot -f"
echo "   Mise à jour: ~/update-craftmine.sh"
echo ""
echo "🎉 Votre bot sera accessible 24/7 une fois configuré !"
