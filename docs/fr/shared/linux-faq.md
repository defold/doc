#### Q : Pourquoi l'éditeur Defold s'affiche-t-il en tout petit sur un écran 4k ou HiDPI ? {#q-why-is-the-defold-editor-super-small-when-run-on-a-4k-or-hidpi-monitor}

R : Si vous utilisez GNOME, vous pouvez modifier le facteur d'échelle avant de lancer Defold. [source](https://unix.stackexchange.com/a/552411)

```bash
$ gsettings set org.gnome.desktop.interface scaling-factor 2
$ ./Defold
```

R : Une autre solution, particulièrement utile si vous souhaitez agrandir l'affichage selon un facteur non entier, consiste à modifier le fichier `Defold/config` et, sur la ligne `vmargs`, à ajouter `glass.gtk.uiScale` : [source](https://forum.defold.com/t/4k-hidpi-monitor-support-solved/64108/12?u=britzl)

```
vmargs = -Dglass.gtk.uiScale=1.5,-Dfile.encoding=UTF-8,...
vmargs = -Dglass.gtk.uiScale=175%,-Dfile.encoding=UTF-8,...
vmargs = -Dglass.gtk.uiScale=192dpi,-Dfile.encoding=UTF-8,...
```

Pour en savoir plus sur cette valeur, consultez l'[article du wiki Arch Linux consacré au HiDPI](https://wiki.archlinux.org/title/HiDPI#JavaFX).

R : Si vous utilisez KDE, vous pouvez définir `GDK_SCALE` :

```bash
$ GDK_SCALE=2 ./Defold
```

#### Q : Pourquoi, sous Elementary OS, les clics de souris traversent-ils l'éditeur et atteignent-ils les éléments situés en dessous ? {#q-why-does-mouse-clicks-on-elementary-os-go-through-the-editor-onto-whatever-is-below}

R : Lancez l'éditeur ainsi :

```bash
$ GTK_CSD=0 ./Defold
```


#### Q : L'éditeur Defold plante à l'ouverture d'une collection ou d'un objet de jeu (game object), et le rapport de plantage mentionne `com.jogamp.opengl` {#q-the-defold-editor-crashes-when-opening-a-collection-or-game-object-and-the-crash-refers-to-comjogampopengl}

R : Sur certaines distributions (comme Ubuntu 18), il existe un problème entre la version de `jogamp`/`jogl` utilisée par Defold et la version de [Mesa](https://docs.mesa3d.org/) présente sur le système. Vous pouvez remplacer la version de GL signalée lors d'un appel à `glGetString(GL_VERSION)` en définissant `MESA_GL_VERSION_OVERRIDE` sur 2.1 ou une valeur supérieure, mais inférieure ou égale à la version prise en charge par votre pilote. Vous pouvez vérifier la version maximale d'OpenGL prise en charge par votre pilote à l'aide de `glxinfo` :

```bash
glxinfo | grep version
```

Exemple de sortie (recherchez « OpenGL version string: x.y ») :

```
server glx version string: 1.4
client glx version string: 1.4
GLX version: 1.4
Max core profile version: 4.6
Max compat profile version: 4.6
Max GLES1 profile version: 1.1
Max GLES[23] profile version: 3.2
OpenGL core profile version string: 4.6 (Core Profile) Mesa 20.2.6
OpenGL core profile shading language version string: 4.60
OpenGL version string: 4.6 (Compatibility Profile) Mesa 20.2.6
OpenGL shading language version string: 4.60
OpenGL ES profile version string: OpenGL ES 3.2 Mesa 20.2.6
OpenGL ES profile shading language version string: OpenGL ES GLSL ES 3.20
GL_EXT_shader_implicit_conversions, GL_EXT_shader_integer_mix,
```

Utilisez la version 2.1 ou la version correspondant à votre pilote graphique :

```bash
$ MESA_GL_VERSION_OVERRIDE=2.1 ./Defold
```

```bash
$ MESA_GL_VERSION_OVERRIDE=4.6 ./Defold
```


#### Q : Pourquoi le message « `com.jogamp.opengl.GLException: Graphics configuration failed` » s'affiche-t-il au lancement de Defold ? {#q-why-am-i-getting-comjogampopenglglexception-graphics-configuration-failed-when-launching-defold}

R : Sur certaines distributions (par exemple Ubuntu 20.04), les nouveaux pilotes [Mesa](https://docs.mesa3d.org/) (Iris) posent un problème lors de l'exécution de Defold. Vous pouvez essayer d'utiliser une version plus ancienne du pilote pour lancer Defold :

```bash
$ MESA_LOADER_DRIVER_OVERRIDE=i965 ./Defold
```


#### Q : L'éditeur Defold plante à l'ouverture d'une collection ou d'un objet de jeu, et le rapport de plantage mentionne `libffi.so` {#q-the-defold-editor-crashes-when-opening-a-collection-or-game-object-and-the-crash-refers-to-libffiso}

R : La version de [libffi](https://sourceware.org/libffi/) de votre distribution ne correspond pas à celle requise par Defold (version 6 ou 7). Assurez-vous que `libffi.so.6` ou `libffi.so.7` est installé dans `/usr/lib/x86_64-linux-gnu`. Vous pouvez télécharger `libffi.so.7` ainsi :  

```bash
$ wget http://ftp.br.debian.org/debian/pool/main/libf/libffi/libffi7_3.3-6_amd64.deb
$ sudo dpkg -i libffi7_3.3-6_amd64.deb
```

Indiquez ensuite le chemin vers cette version dans la variable d'environnement `LD_PRELOAD` lors du lancement de Defold :

```bash
$ LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libffi.so.7 ./Defold
```


#### Q : Mes pilotes OpenGL sont obsolètes. Puis-je quand même utiliser Defold ? {#q-my-opengl-drivers-are-outdated-can-i-still-use-defold}

R : Oui, vous pouvez peut-être utiliser Defold en activant le rendu logiciel. Pour activer le rendu logiciel, définissez la variable d'environnement `LIBGL_ALWAYS_SOFTWARE` sur 1 :

```bash
$ LIBGL_ALWAYS_SOFTWARE=1 ./Defold
```


#### Q : Pourquoi mon jeu Defold ne démarre-t-il pas lorsque j'essaie de le lancer sous Linux ? {#q-why-doesnt-my-defold-game-start-when-i-try-to-run-it-on-linux}

R : Vérifiez la sortie de la console dans l'éditeur. Si le message suivant s'affiche :

```
dmengine: error while loading shared libraries: libopenal.so.1: cannot open shared object file: No such file or directory
```

Vous devez alors installer *`libopenal1`*. Le nom du paquet varie selon les distributions et, dans certains cas, vous devrez peut-être installer les paquets *`openal`* et *`openal-dev`* ou *`openal-devel`*.

```bash
$ apt-get install libopenal-dev
```

#### Q : Pourquoi le menu du haut se ferme-t-il avant que je puisse sélectionner une option ? {#q-why-does-the-top-menu-close-before-i-can-select-something}

R : Ce comportement est probablement dû au gestionnaire de fenêtres utilisé (par exemple `Qtile` ou i3). Il s'agit d'un [problème connu de JavaFX](https://bugs.openjdk.org/browse/JDK-8251240?focusedCommentId=14362084&page=com.atlassian.jira.plugin.system.issuetabpanels%3Acomment-tabpanel#comment-14362084), qui peut être résolu en définissant la variable d'environnement `GDK_DISPLAY` sur 1 :

```bash
$ GDK_DISPLAY=1 ./Defold

D=2

```

Ou en modifiant le fichier `Defold/config` pour ajouter, sur la ligne `vmargs`, `-Djdk.gtk.version=2` :

```
vmargs = -Djdk.gtk.version=2,-Dfile.encoding=UTF-8,...
```


#### Q : Pourquoi ne puis-je pas parcourir tous les emplacements de fichiers disponibles lorsque je sélectionne Open From Disk ? {#q-why-am-i-not-able-to-browse-all-available-file-locations-when-i-select-open-from-disk}

R : Si vous lancez Defold depuis [Steam installé avec Flatpak](https://flathub.org/apps/com.valvesoftware.Steam), vous devez autoriser Steam à accéder à vos autres disques. Vous pouvez modifier les autorisations de vos applications Flatpak à l'aide de [Flatseal](https://flathub.org/apps/com.github.tchx84.Flatseal) ou d'un outil similaire.


#### Q : Pourquoi ne puis-je pas ouvrir le profileur web ou toute autre option de menu nécessitant un navigateur ? {#q-why-am-i-not-able-to-open-the-web-profiler-or-any-other-menu-option-which-requires-a-browser}

R : Il est probable qu'un appel interne à `Desktop.getDesktop().browse(new URI(url));` échoue, car aucun navigateur n'est détecté sur les systèmes sans Gnome. Essayez d'installer `libgnome`.

```bash
$ apt-get install libgnome
```