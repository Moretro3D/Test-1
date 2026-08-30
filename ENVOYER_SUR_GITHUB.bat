@echo off
chcp 65001 >nul
title PokeTama Moretro3D - Depot technique GitHub
cd /d "%~dp0"

echo ============================================================
echo   PokeTama Moretro3D - Depot technique Test-1
echo ============================================================
echo.

where git >nul 2>nul
if errorlevel 1 (
  echo [ERREUR] Git for Windows n'est pas installe.
  pause
  exit /b 1
)

if not exist "web\manifest.json" (
  echo [ERREUR] Le manifeste firmware est absent de ce dossier.
  pause
  exit /b 1
)
set "POKETAMA_SAFE_DIR=%CD:\=/%"
git config --global --add safe.directory "%POKETAMA_SAFE_DIR%"
git config --global user.name "Moretro3D"
git config --global user.email "morgan.duncas@gmail.com"

if not exist ".git" git init
git branch -M main
git remote remove origin >nul 2>nul
git remote add origin https://github.com/Moretro3D/Test-1.git

echo [1/4] Recuperation du depot distant...
git fetch origin main
if errorlevel 1 goto :fail
git reset --mixed origin/main

echo [2/4] Preparation du depot technique...
git add -A

echo [3/4] Creation du commit...
git commit -m "PokeTama - GitHub transforme en depot technique"
if errorlevel 1 echo Aucun nouveau changement a committer, verification du push...

echo [4/4] Publication sur GitHub...
git push -u origin main
if errorlevel 1 goto :fail

git fetch origin main >nul 2>nul
git show origin/main:web/manifest.json | findstr /C:"ESP32-S3" >nul 2>nul
if errorlevel 1 goto :fail
echo.
echo ============================================================
echo PUBLICATION TERMINEE - DEPOT TECHNIQUE VERIFIE SUR GITHUB
echo ============================================================
start "" "https://github.com/Moretro3D/Test-1/actions"
pause
exit /b 0

:fail
echo.
echo [ERREUR] Le depot technique n'a pas pu etre publie ou verifie.
echo Connecte-toi a GitHub si une fenetre d'authentification apparait,
echo puis relance ce fichier.
pause
exit /b 1
