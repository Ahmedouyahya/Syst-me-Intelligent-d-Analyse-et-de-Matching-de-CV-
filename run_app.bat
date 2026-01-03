@echo off
title CV Matcher AI - Launcher
cls
echo ==================================================================
echo      CV Matcher AI - Installation et Lancement Automatique
echo ==================================================================
echo.

REM 1. Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERREUR] Python n'est pas detecte.
    echo Veuillez installer Python 3.8+ et l'ajouter au PATH.
    echo https://www.python.org/downloads/
    pause
    exit /b
)

REM 2. Setup Virtual Environment
if not exist "venv" (
    echo [INFO] Creation de l'environnement virtuel 'venv'...
    python -m venv venv
) else (
    echo [INFO] Environnement virtuel detecte.
)

REM 3. Activate Venv
call venv\Scripts\activate

REM 4. Install Dependencies
echo [INFO] Verification et installation des dependances...
pip install -r requirements.txt

REM 5. Download Spacy Model
echo [INFO] Configuration du modele NLP...
python -m spacy download fr_core_news_sm

REM 6. Launch App
echo.
echo [SUCCES] Tout est pret !
echo [INFO] Lancement du serveur... L'application s'ouvrira dans votre navigateur.
echo.

REM Open browser in 4 seconds (background task)
start /B cmd /c "timeout /t 4 >nul & start http://127.0.0.1:5000"

REM Run Flask App
python run.py

pause

