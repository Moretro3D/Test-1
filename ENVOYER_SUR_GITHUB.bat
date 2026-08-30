@echo off
chcp 65001 >nul
title PokeTama Moretro3D V9.35 - Envoi Test-1
cd /d "%~dp0"

echo ============================================================
echo   PokeTama Moretro3D V9.35
echo ============================================================
echo Depot : https://github.com/Moretro3D/Test-1
echo.

rem Refuse immediatement un ancien dossier V9.30 ouvert par erreur.
findstr /C:"Version V9.35" "web\index.html" >nul 2>nul
if errorlevel 1 (
  echo [ERREUR] Ce dossier n'est pas la V9.35.
  echo Extrais le nouveau ZIP dans un dossier vide puis relance ce fichier.
  pause
  exit /b 1
)
findstr /C:"SPR_ICON_PLAY,  52, 28, 36" "TamaPoke.ino" >nul 2>nul
if errorlevel 1 (
  echo [ERREUR] Reglage independant Poke Ball absent.
  pause
  exit /b 1
)
echo [OK] Dossier local V9.35 et reglages organises verifies.
echo.

where git >nul 2>nul
if errorlevel 1 (
  echo [ERREUR] Git for Windows n'est pas installe.
  pause
  exit /b 1
)

rem Git refuse parfois les dossiers extraits d'un ZIP avec "dubious ownership".
rem On autorise automatiquement et uniquement le dossier courant du projet.
set "TAMAPOKE_SAFE_DIR=%CD:\=/%"
git config --global --add safe.directory "%TAMAPOKE_SAFE_DIR%"

git config --global user.name "Moretro3D"
git config --global user.email "morgan.duncas@gmail.com"

if not exist ".git" git init
git branch -M main
git remote remove origin >nul 2>nul
git remote add origin https://github.com/Moretro3D/Test-1.git

echo [1/4] Recuperation du depot...
git fetch origin main >nul 2>nul
git ls-remote --exit-code --heads origin main >nul 2>nul
if not errorlevel 1 git reset --mixed origin/main

echo [2/4] Ajout des fichiers...
git add -A

echo [3/4] Commit...
git commit -m "PokeTama Moretro3D V9.35 reglages organises"
if errorlevel 1 echo Aucun nouveau changement a committer, poursuite...

echo [4/4] Push GitHub...
git push -u origin main
if errorlevel 1 (
  echo.
  echo [ERREUR] Push impossible. Connecte-toi a GitHub si une fenetre apparait puis relance.
  pause
  exit /b 1
)

echo Verification de la version reellement recue par GitHub...
git fetch origin main >nul 2>nul
git show origin/main:web/index.html | findstr /C:"Version V9.35" >nul 2>nul
if errorlevel 1 (
  echo.
  echo [ERREUR] GitHub ne contient toujours pas la V9.35.
  echo Le message PUSH TERMINE ne sera pas affiche.
  pause
  exit /b 1
)
echo [OK] GitHub origin/main contient bien la V9.35.

echo.
echo ============================================================
echo PUSH TERMINE
echo VERSION DISTANTE VERIFIEE : V9.35
echo ============================================================
echo.
echo IMPORTANT - UNE SEULE FOIS POUR CE NOUVEAU DEPOT :
echo 1. Settings ^> Pages
echo 2. Source = GitHub Actions
echo.
echo J'ouvre maintenant la page Settings ^> Pages.
echo Apres avoir choisi GitHub Actions, ouvre Actions et relance si necessaire.
echo.
start "" "https://github.com/Moretro3D/Test-1/settings/pages"
timeout /t 3 >nul
start "" "https://github.com/Moretro3D/Test-1/actions"
pause
