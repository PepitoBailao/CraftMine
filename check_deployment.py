#!/usr/bin/env python3
"""
Script de vérification avant déploiement
Vérifie que tout est prêt pour l'hébergement
"""

import os
import sys
from pathlib import Path

def check_file_exists(file_path, description):
    """Vérifie qu'un fichier existe"""
    if os.path.exists(file_path):
        print(f"✅ {description}: {file_path}")
        return True
    else:
        print(f"❌ {description} manquant: {file_path}")
        return False

def check_env_variables():
    """Vérifie les variables d'environnement"""
    required_vars = [
        "DISCORD_TOKEN",
        "DEFAULT_SERVER_IP", 
        "DEFAULT_SERVER_PORT",
        "DEFAULT_MINECRAFT_VERSION"
    ]
    
    # Charger le fichier .env si il existe
    env_file = Path(".env")
    if env_file.exists():
        with open(env_file, 'r') as f:
            content = f.read()
            for var in required_vars:
                if f"{var}=" in content and not f"{var}=your_" in content and not f"{var}=" == content.split(f"{var}=")[1].split('\n')[0]:
                    print(f"✅ Variable {var} configurée dans .env")
                else:
                    print(f"⚠️  Variable {var} non configurée ou avec valeur par défaut")
    else:
        print("❌ Fichier .env non trouvé")

def main():
    print("🔍 Vérification avant déploiement...\n")
    
    # Vérifier les fichiers requis
    files_to_check = [
        ("requirements.txt", "Fichier des dépendances"),
        ("src/main.py", "Point d'entrée principal"),
        ("Procfile", "Configuration Railway/Heroku"),
        ("runtime.txt", "Version Python"),
        (".gitignore", "Configuration Git"),
        ("README.md", "Documentation")
    ]
    
    all_files_ok = True
    for file_path, description in files_to_check:
        if not check_file_exists(file_path, description):
            all_files_ok = False
    
    print("\n🔧 Variables d'environnement:")
    check_env_variables()
    
    print("\n📦 Structure du projet:")
    essential_dirs = ["src", "commands", "config"]
    for dir_name in essential_dirs:
        if os.path.isdir(dir_name):
            print(f"✅ Dossier {dir_name}/")
        else:
            print(f"❌ Dossier {dir_name}/ manquant")
            all_files_ok = False
    
    print("\n" + "="*50)
    if all_files_ok:
        print("🎉 Projet prêt pour le déploiement !")
        print("\n📋 Prochaines étapes :")
        print("1. Pousser sur GitHub")
        print("2. Connecter à Railway/Render")
        print("3. Configurer les variables d'environnement")
        print("4. Déployer !")
    else:
        print("⚠️  Corrigez les problèmes avant de déployer")
        sys.exit(1)

if __name__ == "__main__":
    main()
