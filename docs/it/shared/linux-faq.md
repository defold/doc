#### D: Perché l'editor Defold appare piccolissimo quando viene eseguito su un monitor 4K o HiDPI? {#q-why-is-the-defold-editor-super-small-when-run-on-a-4k-or-hidpi-monitor}

R: Se usi GNOME, puoi cambiare il fattore di scala prima di avviare Defold. [fonte](https://unix.stackexchange.com/a/552411)

```bash
$ gsettings set org.gnome.desktop.interface scaling-factor 2
$ ./Defold
```

R: Una soluzione alternativa, soprattutto se vuoi usare un fattore di scala frazionario, consiste nel modificare il file `Defold/config` e aggiungere `glass.gtk.uiScale` alla riga `vmargs`: [fonte](https://forum.defold.com/t/4k-hidpi-monitor-support-solved/64108/12?u=britzl)

```
vmargs = -Dglass.gtk.uiScale=1.5,-Dfile.encoding=UTF-8,...
vmargs = -Dglass.gtk.uiScale=175%,-Dfile.encoding=UTF-8,...
vmargs = -Dglass.gtk.uiScale=192dpi,-Dfile.encoding=UTF-8,...
```

Per ulteriori informazioni su questo valore, consulta l'[articolo su HiDPI nel wiki di Arch Linux](https://wiki.archlinux.org/title/HiDPI#JavaFX).

R: Se usi KDE, puoi impostare `GDK_SCALE`:

```bash
$ GDK_SCALE=2 ./Defold
```

#### D: Perché su Elementary OS i clic del mouse attraversano l'editor e raggiungono ciò che si trova sotto? {#q-why-does-mouse-clicks-on-elementary-os-go-through-the-editor-onto-whatever-is-below}

R: Avvia l'editor in questo modo:

```bash
$ GTK_CSD=0 ./Defold
```


#### D: L'editor Defold va in crash quando apro una collezione (collection) o un oggetto di gioco (game object) e il crash fa riferimento a `com.jogamp.opengl` {#q-the-defold-editor-crashes-when-opening-a-collection-or-game-object-and-the-crash-refers-to-comjogampopengl}

R: Su alcune distribuzioni (come Ubuntu 18) esiste un problema di compatibilità tra la versione di `jogamp`/`jogl` usata da Defold e la versione di [Mesa](https://docs.mesa3d.org/) presente nel sistema. Puoi forzare la versione di GL restituita dalla chiamata a `glGetString(GL_VERSION)` impostando `MESA_GL_VERSION_OVERRIDE` su 2.1 o su un valore maggiore, purché non superi la versione supportata dal driver. Puoi verificare la versione massima di OpenGL supportata dal driver usando `glxinfo`:

```bash
glxinfo | grep version
```

Esempio di output (cerca "OpenGL version string: x.y"):

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

Usa la versione 2.1 oppure la versione supportata dal tuo driver grafico:

```bash
$ MESA_GL_VERSION_OVERRIDE=2.1 ./Defold
```

```bash
$ MESA_GL_VERSION_OVERRIDE=4.6 ./Defold
```


#### D: Perché ricevo l'errore "`com.jogamp.opengl.GLException: Graphics configuration failed`" all'avvio di Defold? {#q-why-am-i-getting-comjogampopenglglexception-graphics-configuration-failed-when-launching-defold}

R: Su alcune distribuzioni (per esempio Ubuntu 20.04) si verifica un problema con i nuovi driver [Mesa](https://docs.mesa3d.org/) (Iris) durante l'esecuzione di Defold. Puoi provare ad avviare Defold usando una versione precedente del driver:

```bash
$ MESA_LOADER_DRIVER_OVERRIDE=i965 ./Defold
```


#### D: L'editor Defold va in crash quando apro una collezione o un oggetto di gioco e il crash fa riferimento a `libffi.so` {#q-the-defold-editor-crashes-when-opening-a-collection-or-game-object-and-the-crash-refers-to-libffiso}

R: La versione di [libffi](https://sourceware.org/libffi/) della tua distribuzione non corrisponde a quella richiesta da Defold (versione 6 o 7). Assicurati che `libffi.so.6` o `libffi.so.7` sia installato in `/usr/lib/x86_64-linux-gnu`. Puoi scaricare `libffi.so.7` in questo modo:  

```bash
$ wget http://ftp.br.debian.org/debian/pool/main/libf/libffi/libffi7_3.3-6_amd64.deb
$ sudo dpkg -i libffi7_3.3-6_amd64.deb
```

Specifica poi il percorso di questa versione nella variabile d'ambiente `LD_PRELOAD` quando avvii Defold:

```bash
$ LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libffi.so.7 ./Defold
```


#### D: I miei driver OpenGL sono obsoleti. Posso comunque usare Defold? {#q-my-opengl-drivers-are-outdated-can-i-still-use-defold}

R: Sì, potresti riuscire a usare Defold abilitando il rendering software. Puoi abilitarlo impostando la variabile d'ambiente `LIBGL_ALWAYS_SOFTWARE` su 1:

```bash
$ LIBGL_ALWAYS_SOFTWARE=1 ./Defold
```


#### D: Perché il mio gioco Defold non si avvia quando provo a eseguirlo su Linux? {#q-why-doesnt-my-defold-game-start-when-i-try-to-run-it-on-linux}

R: Controlla l'output della console nell'editor. Se ricevi il seguente messaggio:

```
dmengine: error while loading shared libraries: libopenal.so.1: cannot open shared object file: No such file or directory
```

Devi installare *`libopenal1`*. Il nome del pacchetto varia a seconda della distribuzione e, in alcuni casi, potresti dover installare i pacchetti *`openal`* e *`openal-dev`* oppure *`openal-devel`*.

```bash
$ apt-get install libopenal-dev
```

#### D: Perché il menu in alto si chiude prima che possa selezionare una voce? {#q-why-does-the-top-menu-close-before-i-can-select-something}

R: Il problema è probabilmente causato dal gestore di finestre in uso (per esempio `Qtile` o i3). È un [problema noto di JavaFX](https://bugs.openjdk.org/browse/JDK-8251240?focusedCommentId=14362084&page=com.atlassian.jira.plugin.system.issuetabpanels%3Acomment-tabpanel#comment-14362084) e puoi risolverlo impostando la variabile d'ambiente `GDK_DISPLAY` su 1:

```bash
$ GDK_DISPLAY=1 ./Defold

D=2

```

Oppure modificando il file `Defold/config` e aggiungendo `-Djdk.gtk.version=2` alla riga `vmargs`:

```
vmargs = -Djdk.gtk.version=2,-Dfile.encoding=UTF-8,...
```


#### D: Perché non riesco a sfogliare tutti i percorsi disponibili quando seleziono Open From Disk? {#q-why-am-i-not-able-to-browse-all-available-file-locations-when-i-select-open-from-disk}

R: Se esegui Defold da [Steam tramite Flatpak](https://flathub.org/apps/com.valvesoftware.Steam), devi autorizzare Steam ad accedere alle altre unità. Puoi modificare le autorizzazioni delle applicazioni Flatpak usando [Flatseal](https://flathub.org/apps/com.github.tchx84.Flatseal) o uno strumento simile.


#### D: Perché non riesco ad aprire il profilatore web o altre opzioni di menu che richiedono un browser? {#q-why-am-i-not-able-to-open-the-web-profiler-or-any-other-menu-option-which-requires-a-browser}

R: È probabile che una chiamata interna a `Desktop.getDesktop().browse(new URI(url));` fallisca perché non viene rilevato alcun browser sui sistemi che non usano GNOME. Prova a installare `libgnome`.

```bash
$ apt-get install libgnome
```