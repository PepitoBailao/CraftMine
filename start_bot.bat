@echo off
echo Démarrage du bot CraftMine...
echo.

REM Vérifier si l'environnement virtuel existe
if not exist ".venv\" (
    echo Environnement virtuel non trouvé !
    echo Exécutez d'abord : python -m venv .venv
    pause
    exit /b 1
)

REM Vérifier si le fichier .env existe
if not exist ".env" (
    echo Fichier .env non trouvé !
    echo Copiez .env.example vers .env et configurez votre token Discord
    pause
    exit /b 1
)

REM Lancer le bot
echo Lancement du bot...
.venv\Scripts\python.exe src\main.py

REM En cas d'erreur
if %ERRORLEVEL% neq 0 (
    echo.
    echo Le bot s'est arrêté avec une erreur
    pause
)
