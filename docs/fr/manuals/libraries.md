---
title: Utiliser les projets de bibliothèques dans Defold
brief: La fonctionnalité de bibliothèques vous permet de partager des ressources entre projets. Ce manuel explique son fonctionnement.
---

# Bibliothèques {#libraries}

La fonctionnalité de bibliothèques vous permet de partager des ressources entre projets. Il s'agit d'un mécanisme simple mais très puissant, que vous pouvez utiliser de différentes manières dans votre flux de travail.

Les bibliothèques sont utiles pour les usages suivants :

* Copier des ressources d'un projet terminé vers un nouveau projet. Si vous créez la suite d'un jeu précédent, c'est un moyen simple de démarrer.
* Constituer une bibliothèque de modèles que vous pouvez copier dans vos projets, puis personnaliser ou spécialiser.
* Constituer une ou plusieurs bibliothèques d'objets ou de scripts prêts à l'emploi que vous pouvez référencer directement. C'est très pratique pour stocker des modules de script communs ou pour constituer une bibliothèque partagée de ressources graphiques, sonores et d'animation.

## Configurer le partage de bibliothèques {#setting-up-library-sharing}

Supposons que vous souhaitiez créer une bibliothèque contenant des sprites et des sources de tuiles partagés. Commencez par [configurer un nouveau projet](/manuals/project-setup/). Choisissez les dossiers du projet que vous souhaitez partager et ajoutez leurs noms à la propriété *`include_dirs`* dans les paramètres du projet. Si vous souhaitez indiquer plusieurs dossiers, séparez leurs noms par des espaces :

![Dossiers à inclure](images/libraries/libraries_include_dirs.png)

Avant de pouvoir ajouter cette bibliothèque à un autre projet, nous devons disposer d'un moyen de la localiser.

## URL de la bibliothèque {#library-url}

Les bibliothèques sont référencées au moyen d'une URL standard. Pour un projet hébergé sur GitHub, il s'agit de l'URL d'une version publiée du projet :

![URL d'une bibliothèque sur GitHub](images/libraries/libraries_library_url_github.png)

::: important
Il est recommandé de toujours dépendre d'une version publiée précise d'un projet de bibliothèque plutôt que de sa branche `master`. Ainsi, en tant que développeur, vous décidez du moment où vous intégrez les modifications d'un projet de bibliothèque, au lieu de toujours recevoir les dernières modifications de sa branche `master`, qui pourraient introduire des incompatibilités.
:::

::: important
Il est recommandé de toujours examiner les bibliothèques tierces avant de les utiliser. Pour en savoir plus, consultez la section [sécuriser votre utilisation de logiciels tiers](https://defold.com/manuals/application-security/#securing-your-use-of-third-party-software).
:::

### Authentification d'accès de base {#basic-access-authentication}

Vous pouvez ajouter un nom d'utilisateur et un mot de passe ou un jeton à l'URL de la bibliothèque pour effectuer une authentification d'accès de base lorsque vous utilisez des bibliothèques qui ne sont pas accessibles publiquement :

```
https://username:password@github.com/defold/private/archive/main.zip
```

Les champs `username` et `password` sont extraits et ajoutés sous forme d'en-tête de requête `Authorization`. Cela fonctionne avec tout serveur prenant en charge l'autorisation d'accès de base.

::: important
Veillez à ne pas partager ni divulguer accidentellement le jeton d'accès personnel que vous avez généré ou votre mot de passe, car les conséquences peuvent être graves s'ils tombent entre de mauvaises mains !
:::

Pour éviter de divulguer accidentellement des identifiants en les laissant en clair dans l'URL de la bibliothèque, vous pouvez également utiliser un motif de remplacement de chaîne et stocker les identifiants dans des variables d'environnement :

```
https://__PRIVATE_USERNAME__:__PRIVATE_TOKEN__@github.com/defold/private/archive/main.zip
```

Dans l'exemple ci-dessus, le nom d'utilisateur et le jeton sont lus dans les variables d'environnement système `PRIVATE_USERNAME` et `PRIVATE_TOKEN`.

#### Authentification GitHub {#github-authentication}

Pour récupérer une bibliothèque depuis un dépôt privé sur GitHub, vous devez [générer un jeton d'accès personnel](https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/creating-a-personal-access-token) et l'utiliser comme mot de passe.

```
https://github-username:personal-access-token@github.com/defold/private/archive/main.zip
```

#### Authentification GitLab {#gitlab-authentication}

Pour récupérer une bibliothèque depuis un dépôt privé sur GitLab, vous devez [générer un jeton d'accès personnel](https://docs.gitlab.com/ee/security/token_overview.html) et l'envoyer en tant que paramètre d'URL.

```
https://gitlab.com/defold/private/-/archive/main/test-main.zip?private_token=personal-access-token
```

### Authentification d'accès avancée {#advanced-access-authentication}

Lorsque vous utilisez l'authentification d'accès de base, le jeton d'accès et le nom d'utilisateur d'un utilisateur sont partagés dans tous les dépôts utilisés pour le projet. Dans une équipe de plusieurs personnes, cela peut poser problème. Pour résoudre ce problème, un utilisateur disposant d'un accès « en lecture seule » doit être utilisé pour l'accès de la bibliothèque au dépôt. Sur GitHub, cela nécessite une organisation, une équipe et un utilisateur qui n'a pas besoin de modifier le dépôt (d'où l'accès en lecture seule).

Étapes pour GitHub :
* [Créez une organisation](https://docs.github.com/en/github/setting-up-and-managing-organizations-and-teams/creating-a-new-organization-from-scratch)
* [Créez une équipe au sein de l'organisation](https://docs.github.com/en/github/setting-up-and-managing-organizations-and-teams/creating-a-team)
* [Transférez le dépôt privé souhaité vers votre organisation](https://docs.github.com/en/github/administering-a-repository/transferring-a-repository)
* [Accordez à l'équipe un accès « en lecture seule » au dépôt](https://docs.github.com/en/github/setting-up-and-managing-organizations-and-teams/managing-team-access-to-an-organization-repository)
* [Créez ou sélectionnez un utilisateur qui fera partie de cette équipe](https://docs.github.com/en/github/setting-up-and-managing-organizations-and-teams/organizing-members-into-teams)
* Utilisez l'« authentification d'accès de base » décrite ci-dessus pour créer un jeton d'accès personnel pour cet utilisateur

À ce stade, les informations d'authentification du nouvel utilisateur peuvent être enregistrées dans un commit et poussées vers le dépôt. Toute personne travaillant avec votre dépôt privé pourra ainsi le récupérer en tant que bibliothèque sans disposer de droits de modification sur la bibliothèque elle-même.

::: important
Le jeton de l'utilisateur disposant d'un accès en lecture seule est entièrement accessible à toute personne ayant accès aux dépôts des jeux qui utilisent la bibliothèque.
:::

Cette solution a été proposée sur le forum Defold et [discutée dans ce fil](https://forum.defold.com/t/private-github-for-library-solved/67240).

## Configurer les dépendances de bibliothèques {#setting-up-library-dependencies}

Ouvrez le projet depuis lequel vous souhaitez accéder à la bibliothèque. Dans les paramètres du projet, ajoutez l'URL de la bibliothèque à la propriété *dependencies*. Vous pouvez spécifier plusieurs projets en tant que dépendances si vous le souhaitez. Ajoutez-les simplement un par un à l'aide du bouton `+` et supprimez-les à l'aide du bouton `-` :

![Dépendances](images/libraries/libraries_dependencies.png)

Sélectionnez maintenant <kbd>Project ▸ Fetch Libraries</kbd> pour mettre à jour les dépendances de bibliothèques. Cette opération s'effectue automatiquement chaque fois que vous ouvrez un projet. Vous n'avez donc besoin de la lancer que si les dépendances changent sans que vous rouvriez le projet. Cela se produit si vous ajoutez ou supprimez des bibliothèques dans les dépendances, ou si quelqu'un modifie et synchronise l'un des projets de bibliothèque utilisés comme dépendances.

![Récupération des bibliothèques](images/libraries/libraries_fetch_libraries.png)

Les dossiers que vous avez partagés apparaissent désormais dans le *panneau Assets* et vous pouvez utiliser tout ce que vous avez partagé. Toutes les modifications synchronisées du projet de bibliothèque seront disponibles dans votre projet.

![Configuration de la bibliothèque terminée](images/libraries/libraries_done.png)

## Modifier les fichiers des bibliothèques utilisées comme dépendances {#editing-files-in-library-dependencies}

Les fichiers des bibliothèques ne peuvent pas être enregistrés. Vous pouvez les modifier, et l'éditeur pourra effectuer un build avec ces modifications, ce qui est utile pour les tests. Cependant, le fichier lui-même reste inchangé et toutes les modifications seront abandonnées à sa fermeture.

Si vous souhaitez modifier des fichiers de bibliothèque, veillez à créer votre propre fork de la bibliothèque et à y apporter vos modifications. Une autre possibilité consiste à copier-coller le dossier entier de la bibliothèque dans le répertoire de votre projet et à utiliser la copie locale. Dans ce cas, votre dossier local masquera la dépendance d'origine et le lien de dépendance devra être supprimé de `game.project` (n'oubliez pas de sélectionner ensuite <kbd>Project ▸ Fetch Libraries</kbd>).

`builtins` est également une bibliothèque fournie par le moteur. Si vous souhaitez y modifier des fichiers, veillez à les copier dans votre projet et à utiliser ces copies à la place des fichiers `builtins` d'origine. Par exemple, pour modifier `default.render_script`, copiez `/builtins/render/default.render` et `/builtins/render/default.render_script` dans le dossier de votre projet sous les noms `my_custom.render` et `my_custom.render_script`. Ensuite, modifiez votre fichier local `my_custom.render` pour qu'il référence `my_custom.render_script` à la place du fichier intégré, puis sélectionnez votre fichier personnalisé `my_custom.render` dans le paramètre Render de `game.project`.

Si vous copiez-collez un matériau et souhaitez l'utiliser pour tous les composants (components) d'un certain type, il peut être utile d'utiliser des [modèles propres au projet](/manuals/editor/#creating-new-project-files).

## Références rompues {#broken-references}

Le partage de bibliothèques n'inclut que les fichiers situés dans les dossiers partagés. Si vous créez un élément qui référence des ressources situées en dehors de la hiérarchie partagée, les chemins des références seront rompus.

## Collisions de noms {#name-collisions}

Comme vous pouvez indiquer plusieurs URL de projets dans le paramètre de projet *dependencies*, vous pouvez rencontrer une collision de noms. Cela se produit si plusieurs projets utilisés comme dépendances partagent un dossier portant le même nom dans le paramètre de projet *`include_dirs`*.

Defold résout les collisions de noms en ignorant toutes les références à des dossiers portant le même nom, à l'exception de la dernière, selon l'ordre des URL de projets dans la liste *dependencies*. Par exemple, si vous indiquez trois URL de projets de bibliothèque dans les dépendances et que tous partagent un dossier nommé *items*, un seul dossier *items* apparaîtra : celui du projet placé en dernier dans la liste des URL.
