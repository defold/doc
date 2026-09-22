---
title: Débogage sur iOS/macOS
brief: Ce manuel explique comment déboguer un build avec Xcode.
---

# Débogage sur iOS/macOS {#debugging-on-iosmacos}

Nous décrivons ici comment déboguer un build avec [Xcode](https://developer.apple.com/xcode/), l'IDE privilégié par Apple pour le développement sur macOS et iOS.

## Xcode {#xcode}

* Créez un bundle de l'application avec Bob, en utilisant l'option `--with-symbols` ([plus d'informations](/manuals/debugging-native-code/#symbolicate-a-callstack)) :

```sh
$ cd myproject
$ wget http://d.defold.com/archive/<sha1>/bob/bob.jar
$ java -jar bob.jar --platform armv7-darwin build --with-symbols --variant debug --archive bundle -bo build/ios -mp <app>.mobileprovision --identity "iPhone Developer: Your Name (ID)"
```

* Installez l'application avec `Xcode`, `iTunes` ou [ios-deploy](https://github.com/ios-control/ios-deploy)

```sh
$ ios-deploy -b <AppName>.ipa
```

* Récupérez le dossier `.dSYM` (c'est-à-dire les symboles de débogage)

	* Si l'application n'utilise pas d'extensions natives, vous pouvez télécharger le fichier `.dSYM` sur [d.defold.com](http://d.defold.com)

	* Si vous utilisez une extension native, le dossier `.dSYM` est généré lorsque vous créez un build avec [bob.jar](https://www.defold.com/manuals/bob/). Seul le build est nécessaire (sans archivage ni création de bundle) :

```sh
$ cd myproject
$ unzip .internal/cache/arm64-ios/build.zip
$ mv dmengine.dSYM <AppName>.dSYM
$ mv <AppName>.dSYM/Contents/Resources/DWARF/dmengine <AppName>.dSYM/Contents/Resources/DWARF/<AppName>
```

### Création du projet {#create-project}

Pour déboguer correctement, nous devons disposer d'un projet et configurer les correspondances avec le code source.
Nous utilisons ce projet uniquement pour le débogage, sans y effectuer de build.

* Créez un projet Xcode et choisissez le modèle `Game`

	![Modèle de projet](images/extensions/debugging/ios/project_template.png)

* Choisissez un nom (par exemple `debug`) et les paramètres par défaut

* Choisissez un dossier dans lequel enregistrer le projet

* Ajoutez votre code à l'application

	![Ajout de fichiers](images/extensions/debugging/ios/add_files.png)

* Vérifiez que la case « Copy items if needed » est décochée.

	![Ajout du code source](images/extensions/debugging/ios/add_source.png)

* Voici le résultat final

	![Code source ajouté](images/extensions/debugging/ios/added_source.png)


* Désactivez l'étape `Build`

	![Modification du schéma](images/extensions/debugging/ios/edit_scheme.png)

	![Désactivation du build](images/extensions/debugging/ios/disable_build.png)

* Définissez la version `Deployment target` de sorte qu'elle soit désormais supérieure à la version d'iOS de votre appareil

	![Version cible du déploiement](images/extensions/debugging/ios/deployment_version.png)

* Sélectionnez l'appareil cible

	![Sélection de l'appareil](images/extensions/debugging/ios/select_device.png)


### Lancement du débogueur {#launch-the-debugger}

Plusieurs possibilités s'offrent à vous pour déboguer une application

1. Choisissez `Debug` -> `Attach to process...`, puis sélectionnez l'application

2. Ou choisissez `Attach to process by PID or Process name`

	![Sélection de l'appareil](images/extensions/debugging/ios/attach_to_process_name.png)

3. Démarrez l'application sur l'appareil

4. Dans `Edit Scheme`, ajoutez le dossier <AppName>.app en tant qu'exécutable

### Symboles de débogage {#debug-symbols}

**Pour utiliser lldb, l'exécution doit être suspendue**

* Ajoutez le chemin de `.dSYM` à lldb

```
(lldb) add-dsym <PathTo.dSYM>
```

	![add_dsym](images/extensions/debugging/ios/add_dsym.png)

* Vérifiez que `lldb` a lu les symboles correctement

```
(lldb) image list <AppName>
```

### Correspondances des chemins {#path-mappings}

* Ajoutez le code source du moteur (adaptez les chemins à vos besoins)

```
(lldb) settings set target.source-map /Users/builder/ci/builds/engine-ios-64-master/build /Users/mathiaswesterdahl/work/defold
(lldb) settings append target.source-map /private/var/folders/m5/bcw7ykhd6vq9lwjzq1mkp8j00000gn/T/job4836347589046353012/upload/videoplayer/src /Users/mathiaswesterdahl/work/projects/extension-videoplayer-native/videoplayer/src
```

* Vous pouvez retrouver le dossier de la tâche à partir de l'exécutable. Ce dossier porte un nom tel que `job1298751322870374150`, avec un nombre aléatoire à chaque fois.

```sh
$ dsymutil -dump-debug-map <executable> 2>&1 >/dev/null | grep /job

```

* Vérifiez les correspondances avec le code source

```
(lldb) settings show target.source-map
```

Vous pouvez vérifier de quel fichier source provient un symbole à l'aide de la commande suivante

```
(lldb) image lookup -va <SymbolName>
```

### Points d'arrêt {#breakpoints}

* Ouvrez un fichier dans la vue du projet et définissez un point d'arrêt

	![Point d'arrêt](images/extensions/debugging/ios/breakpoint.png)

## Remarques {#notes}

### Vérification de l'UUID du binaire {#check-uuid-of-binary}

Pour que le débogueur accepte le dossier `.dSYM`, son UUID doit correspondre à celui de l'exécutable en cours de débogage. Vous pouvez vérifier l'UUID ainsi :

```sh
$ dwarfdump -u <PathToBinary>
```