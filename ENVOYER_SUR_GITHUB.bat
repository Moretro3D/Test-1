@echo off
chcp 65001 >nul
title TamaPoke MoRetro - Test-1 FINAL
cd /d "%~dp0"

echo ============================================================
echo   TamaPoke MoRetro - Envoi FINAL vers GitHub Test-1
echo ============================================================
echo.
echo Depot :
echo https://github.com/Moretro3D/Test-1.git
echo.

where git >nul 2>nul
if errorlevel 1 (
  echo [ERREUR] Git for Windows n'est pas installe.
  echo Installe Git for Windows puis relance ce fichier.
  pause
  exit /b 1
)

echo [0/6] Configuration Git...
git config --global user.name "Moretro3D"
git config --global user.email "morgan.duncas@gmail.com"

if not exist ".git" (
  echo Initialisation du depot local...
  git init
)

git branch -M main

git remote remove origin >nul 2>nul
git remote add origin https://github.com/Moretro3D/Test-1.git

echo [1/6] Recuperation du depot distant...
git fetch origin main >nul 2>nul

echo [2/6] Synchronisation...
git ls-remote --exit-code --heads origin main >nul 2>nul
if not errorlevel 1 (
  git reset --mixed origin/main
)

echo [3/6] Ajout de tous les fichiers et dossiers...
git add -A

echo [4/6] Creation du commit...
git commit -m "TamaPoke MoRetro Web Flasher FINAL"
if errorlevel 1 (
  echo Aucun nouveau changement a committer, on continue quand meme...
)

echo [5/6] Envoi vers Moretro3D/Test-1...
git push -u origin main

if errorlevel 1 (
  echo.
  echo [ERREUR] Le push a echoue.
  echo.
  echo Si GitHub demande une connexion :
  echo 1. Connecte-toi dans la fenetre qui s'ouvre.
  echo 2. Puis relance ENVOYER_SUR_GITHUB.bat
  pause
  exit /b 1
)

echo [6/6] TERMINE !
echo.
echo ============================================================
echo Tout a ete envoye vers :
echo https://github.com/Moretro3D/Test-1
echo.
echo Ouvre maintenant :
echo https://github.com/Moretro3D/Test-1/actions
echo ============================================================
echo.
pause
