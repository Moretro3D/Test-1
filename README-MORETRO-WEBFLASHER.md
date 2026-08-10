# TamaPoke MoRetro – Web Flasher

Ce pack contient la version TamaPoke Expanded modifiée et un flasher Web automatique.

## Mise en ligne en 5 étapes

1. Crée un nouveau dépôt GitHub public, par exemple `TamaPoke-MoRetro`.
2. Envoie tout le contenu de ce dossier à la racine du dépôt.
3. Dans GitHub : **Settings > Pages > Source > GitHub Actions**.
4. Va dans **Actions** et attends que `Build firmware + deploy web flasher` soit vert.
5. GitHub affichera l'adresse de ton flasher. Ouvre-la dans **Chrome ou Edge**.

Le workflow installe Arduino CLI, le core ESP32 et les bibliothèques nécessaires, compile
la version modifiée avec les paramètres ESP32-S3 du projet, génère les 4 fichiers `.bin`,
puis publie automatiquement le dossier `web/`.

Version du firmware : `1.29.1-moretro-ui1`

## Mise à jour d'un TamaPoke déjà utilisé

Dans le flasher, choisis une installation **sans effacement** pour conserver la sauvegarde.
L'effacement complet est à réserver à une installation neuve ou à un dépannage volontaire.
