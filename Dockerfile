# Utiliser Python 3.11 slim
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de requirements
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source
COPY . .

# Exposer le port (optionnel pour un bot Discord)
EXPOSE 8080

# Commande pour démarrer le bot
CMD ["python", "src/main.py"]
