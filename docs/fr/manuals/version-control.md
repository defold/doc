---
title: Gestion de versions
brief: Ce manuel explique comment utiliser Git avec les projets Defold et examiner les modifications locales dans l'éditeur.
---

# Gestion de versions {#version-control}

Les projets Defold fonctionnent bien avec [Git](https://git-scm.com), mais la synchronisation s'effectue en dehors de l'éditeur. Utilisez votre client Git préféré ou la ligne de commande pour cloner un dépôt, récupérer les modifications distantes, les intégrer, créer des commits, envoyer vos commits, créer des branches et résoudre les conflits.

## Fichiers modifiés {#changed-files}

Lorsque le répertoire du projet est la racine d'un arbre de travail Git comportant au moins un commit, Defold affiche les fichiers non ignorés détectés comme ajoutés, modifiés, supprimés ou renommés dans le panneau *Changed Files* de l'éditeur. Il établit cette liste en comparant directement les fichiers sur le disque au commit actuel (`HEAD`) ; l'indexation d'une modification ne change donc pas la liste. Résolvez les conflits de fusion dans un client Git externe.

![fichiers modifiés](images/workflow/changed_files.png)

Sélectionnez exactement un fichier modifié ou renommé, puis cliquez sur <kbd>Diff</kbd> pour afficher ses différences textuelles. Cliquez sur <kbd>Revert</kbd> pour abandonner les modifications sélectionnées dans l'arbre de travail et dans l'index. Les fichiers suivis sont restaurés à leur état dans `HEAD` ; les fichiers absents de `HEAD` sont supprimés, qu'ils soient ou non indexés comme ajouts ; et, pour les fichiers renommés, le nouveau chemin est supprimé et l'ancien est restauré. Cette opération ne peut pas être annulée dans l'éditeur : créez donc un commit ou une sauvegarde du travail dont vous pourriez avoir besoin.

## Git {#git}

Git stocke efficacement les fichiers de projet Defold au format texte. Des modifications fréquentes de ressources binaires volumineuses, telles que des fichiers PSD ou de production audio, peuvent néanmoins faire croître rapidement l'historique du dépôt. Envisagez d'utiliser Git LFS ou une solution distincte de stockage et de sauvegarde pour les fichiers de travail volumineux.

Le panneau *Changed Files* fournit uniquement des opérations locales de consultation de l'état, d'affichage des différences et d'annulation des modifications. Il ne sait pas si les commits ont été envoyés vers un dépôt distant et n'effectue aucune opération de récupération, d'intégration, de création de commits ou d'envoi de modifications. Effectuez ces opérations dans un client Git externe ou depuis la ligne de commande. Par défaut, Defold recharge les modifications externes et actualise le panneau lorsqu'il reprend le focus. Si *Load External Changes on App Focus* est désactivé, choisissez *File ▸ Load External Changes*.
