@echo off
echo 🚀 Préparation pour le déploiement...

REM Vérifier si Git est installé
git --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ❌ Git n'est pas installé. Installez Git d'abord.
    pause
    exit /b 1
)

echo ✅ Git détecté

REM Initialiser le repo si nécessaire
if not exist ".git\" (
    echo 📦 Initialisation du repository Git...
    git init
    git add .
    git commit -m "Initial commit - CraftMine Discord Bot"
    echo ✅ Repository Git initialisé
) else (
    echo 📦 Repository Git existant détecté
)

echo.
echo 🌐 Prochaines étapes pour Railway :
echo 1. Créez un compte sur https://railway.app
echo 2. Connectez votre compte GitHub
echo 3. Créez un nouveau projet depuis GitHub
echo 4. Sélectionnez ce repository
echo 5. Ajoutez ces variables d'environnement :
echo    - DISCORD_TOKEN=votre_token_ici
echo    - DEFAULT_SERVER_IP=144.24.205.125
echo    - DEFAULT_SERVER_PORT=25565
echo    - DEFAULT_MINECRAFT_VERSION=1.24.1
echo 6. Déployez !
echo.
echo 📋 Pour pousser les changements futurs :
echo    git add .
echo    git commit -m "Update bot"
echo    git push origin main
echo.
pause
