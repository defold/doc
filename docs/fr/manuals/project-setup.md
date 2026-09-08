---
title: Configuration du projet
brief: Ce manuel explique comment créer ou ouvrir un projet dans Defold.
---

# Configuration du projet {#project-setup}

Vous pouvez facilement créer un nouveau projet directement dans l'éditeur Defold. Vous pouvez aussi ouvrir un projet existant déjà présent sur votre ordinateur.

## Créer un nouveau projet local {#creating-a-new-project}

Cliquez sur l'option <kbd>New Project</kbd> et sélectionnez le type de projet que vous souhaitez créer. Indiquez l'emplacement sur votre disque dur où les fichiers du projet seront stockés. Cliquez sur <kbd>Create New Project</kbd> pour créer le projet à l'emplacement choisi. Vous pouvez créer un nouveau projet à partir d'un modèle :

![Ouvrir un projet](images/workflow/open_project.png)

Ou à partir d'un tutoriel contenant des instructions pas à pas :

![Créer un projet à partir d'un tutoriel](images/workflow/create_from_tutorial.png)

Ou à partir d'un jeu d'exemple complet :

![Créer un projet à partir d'un exemple](images/workflow/create_from_sample.png)

### Ajouter le projet à GitHub {#adding-the-project-to-github}

Un projet local n'est intégré à aucun système de gestion de versions : les fichiers résident uniquement sur votre disque dur et aucun historique ne permet d'annuler les modifications. Les fichiers supprimés depuis le panneau *Assets* de l'éditeur sont déplacés vers la corbeille du système (Trash ou Recycle Bin) lorsque cette opération est prise en charge, mais ils peuvent être définitivement supprimés si elle est indisponible ou échoue. La corbeille ne protège pas vos fichiers lorsque vous les modifiez et ne fournit pas d'historique des versions ; il est donc recommandé d'utiliser un système de gestion de versions tel que Git pour suivre les modifications apportées à vos fichiers. Cela facilite aussi grandement la collaboration sur un projet avec d'autres personnes. Quelques étapes suffisent pour transférer un projet local sur GitHub :

1. Créez un compte sur [GitHub](https://github.com/) ou connectez-vous à votre compte
2. Créez un dépôt à l'aide de l'option [New Repository](https://help.github.com/en/articles/creating-a-new-repository)
3. Transférez tous les fichiers du projet à l'aide de l'option [Upload Files](https://help.github.com/en/articles/adding-a-file-to-a-repository)

Le projet est désormais suivi par un système de gestion de versions et vous devriez [cloner le projet](https://help.github.com/en/articles/cloning-a-repository) sur votre disque dur local, puis travailler depuis ce nouvel emplacement.

## Ouvrir un projet existant {#open-an-existing-project}

Cliquez sur l'option <kbd>Open From Disk</kbd> pour ouvrir un projet déjà présent sur votre ordinateur.

![Importer un projet](images/workflow/open_from_disk.png)

## Ouvrir un projet récent {#open-a-recent-project}

Dès qu'un projet a été ouvert une première fois, il apparaît dans la liste des projets récents. Cette liste affiche les projets sur lesquels vous avez travaillé le plus récemment et vous permet d'ouvrir rapidement n'importe lequel en double-cliquant dessus.
