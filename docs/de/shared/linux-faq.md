#### Q: Warum ist der Defold-Editor auf einem 4k- oder HiDPI-Monitor winzig klein? {#q-why-is-the-defold-editor-super-small-when-run-on-a-4k-or-hidpi-monitor}

A: Wenn du GNOME verwendest, kannst du den Skalierungsfaktor vor dem Start von Defold ändern. [Quelle](https://unix.stackexchange.com/a/552411)

```bash
$ gsettings set org.gnome.desktop.interface scaling-factor 2
$ ./Defold
```

A: Eine alternative Lösung, insbesondere wenn du um einen nicht ganzzahligen Faktor vergrößern möchtest, besteht darin, die Datei `Defold/config` zu ändern und in der Zeile `vmargs` den Eintrag `glass.gtk.uiScale` hinzuzufügen: [Quelle](https://forum.defold.com/t/4k-hidpi-monitor-support-solved/64108/12?u=britzl)

```
vmargs = -Dglass.gtk.uiScale=1.5,-Dfile.encoding=UTF-8,...
vmargs = -Dglass.gtk.uiScale=175%,-Dfile.encoding=UTF-8,...
vmargs = -Dglass.gtk.uiScale=192dpi,-Dfile.encoding=UTF-8,...
```

Mehr zu diesem Wert findest du im [HiDPI-Wiki-Artikel von Arch Linux](https://wiki.archlinux.org/title/HiDPI#JavaFX).

A: Wenn du KDE verwendest, kannst du `GDK_SCALE` setzen:

```bash
$ GDK_SCALE=2 ./Defold
```

#### Q: Warum gehen Mausklicks unter Elementary OS durch den Editor hindurch an das, was darunter liegt? {#q-why-does-mouse-clicks-on-elementary-os-go-through-the-editor-onto-whatever-is-below}

A: Starte den Editor wie folgt:

```bash
$ GTK_CSD=0 ./Defold
```


#### Q: Der Defold-Editor stürzt beim Öffnen einer Sammlung (collection) oder eines Spielobjekts (game object) ab, und die Absturzmeldung verweist auf `com.jogamp.opengl` {#q-the-defold-editor-crashes-when-opening-a-collection-or-game-object-and-the-crash-refers-to-comjogampopengl}

A: Bei bestimmten Distributionen (wie Ubuntu 18) gibt es ein Problem zwischen der von Defold verwendeten Version von `jogamp`/`jogl` und der Version von [Mesa](https://docs.mesa3d.org/) auf dem System. Du kannst überschreiben, welche GL-Version beim Aufruf von `glGetString(GL_VERSION)` gemeldet wird, indem du `MESA_GL_VERSION_OVERRIDE` auf 2.1 oder einen größeren Wert setzt, der aber kleiner oder gleich der von deinem Treiber unterstützten Version ist. Mit `glxinfo` kannst du prüfen, welche OpenGL-Version dein Treiber maximal unterstützt:

```bash
glxinfo | grep version
```

Beispielausgabe (suche nach "OpenGL version string: x.y"):

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

Verwende Version 2.1 oder die zu deinem Grafiktreiber passende Version:

```bash
$ MESA_GL_VERSION_OVERRIDE=2.1 ./Defold
```

```bash
$ MESA_GL_VERSION_OVERRIDE=4.6 ./Defold
```


#### Q: Warum erhalte ich beim Starten von Defold die Meldung "`com.jogamp.opengl.GLException: Graphics configuration failed`"? {#q-why-am-i-getting-comjogampopenglglexception-graphics-configuration-failed-when-launching-defold}

A: Bei bestimmten Distributionen (beispielsweise Ubuntu 20.04) gibt es beim Ausführen von Defold ein Problem mit den neuen [Mesa](https://docs.mesa3d.org/)-Treibern (Iris). Du kannst versuchen, Defold mit einer älteren Treiberversion auszuführen:

```bash
$ MESA_LOADER_DRIVER_OVERRIDE=i965 ./Defold
```


#### Q: Der Defold-Editor stürzt beim Öffnen einer Sammlung oder eines Spielobjekts ab, und die Absturzmeldung verweist auf `libffi.so` {#q-the-defold-editor-crashes-when-opening-a-collection-or-game-object-and-the-crash-refers-to-libffiso}

A: Die [libffi](https://sourceware.org/libffi/)-Version deiner Distribution stimmt nicht mit der von Defold benötigten Version (Version 6 oder 7) überein. Stelle sicher, dass `libffi.so.6` oder `libffi.so.7` unter `/usr/lib/x86_64-linux-gnu` installiert ist. Du kannst `libffi.so.7` wie folgt herunterladen:  

```bash
$ wget http://ftp.br.debian.org/debian/pool/main/libf/libffi/libffi7_3.3-6_amd64.deb
$ sudo dpkg -i libffi7_3.3-6_amd64.deb
```

Gib anschließend beim Ausführen von Defold den Pfad zu dieser Version in der Umgebungsvariablen `LD_PRELOAD` an:

```bash
$ LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libffi.so.7 ./Defold
```


#### Q: Meine OpenGL-Treiber sind veraltet. Kann ich Defold trotzdem verwenden? {#q-my-opengl-drivers-are-outdated-can-i-still-use-defold}

A: Ja, möglicherweise kannst du Defold verwenden, wenn du Software-Rendering aktivierst. Du kannst Software-Rendering aktivieren, indem du die Umgebungsvariable `LIBGL_ALWAYS_SOFTWARE` auf 1 setzt:

```bash
$ LIBGL_ALWAYS_SOFTWARE=1 ./Defold
```


#### Q: Warum startet mein Defold-Spiel nicht, wenn ich versuche, es unter Linux auszuführen? {#q-why-doesnt-my-defold-game-start-when-i-try-to-run-it-on-linux}

A: Prüfe die Konsolenausgabe im Editor. Wenn du die folgende Meldung erhältst:

```
dmengine: error while loading shared libraries: libopenal.so.1: cannot open shared object file: No such file or directory
```

Dann musst du *`libopenal1`* installieren. Der Paketname unterscheidet sich je nach Distribution, und in manchen Fällen musst du möglicherweise die Pakete *`openal`* und *`openal-dev`* oder *`openal-devel`* installieren.

```bash
$ apt-get install libopenal-dev
```

#### Q: Warum schließt sich das obere Menü, bevor ich etwas auswählen kann? {#q-why-does-the-top-menu-close-before-i-can-select-something}

A: Dies wird wahrscheinlich durch den verwendeten Fenstermanager verursacht (beispielsweise `Qtile` oder i3). Es handelt sich um ein [bekanntes Problem in JavaFX](https://bugs.openjdk.org/browse/JDK-8251240?focusedCommentId=14362084&page=com.atlassian.jira.plugin.system.issuetabpanels%3Acomment-tabpanel#comment-14362084), das sich entweder lösen lässt, indem du die Umgebungsvariable `GDK_DISPLAY` auf 1 setzt:¨

```bash
$ GDK_DISPLAY=1 ./Defold

D=2

```

Oder indem du die Datei `Defold/config` änderst und in der Zeile `vmargs` den Eintrag `-Djdk.gtk.version=2` hinzufügst:

```
vmargs = -Djdk.gtk.version=2,-Dfile.encoding=UTF-8,...
```


#### Q: Warum kann ich nicht alle verfügbaren Speicherorte durchsuchen, wenn ich Open From Disk auswähle? {#q-why-am-i-not-able-to-browse-all-available-file-locations-when-i-select-open-from-disk}

A: Wenn du Defold über [Steam als Flatpak](https://flathub.org/apps/com.valvesoftware.Steam) ausführst, musst du Steam die Berechtigung erteilen, auf deine anderen Laufwerke zuzugreifen. Du kannst die Berechtigungen deiner Flatpak-Anwendungen mit [Flatseal](https://flathub.org/apps/com.github.tchx84.Flatseal) oder einem ähnlichen Werkzeug ändern.


#### Q: Warum kann ich den Web-Profiler oder andere Menüoptionen, die einen Browser erfordern, nicht öffnen? {#q-why-am-i-not-able-to-open-the-web-profiler-or-any-other-menu-option-which-requires-a-browser}

A: Wahrscheinlich schlägt ein interner Aufruf von `Desktop.getDesktop().browse(new URI(url));` fehl, da auf Systemen ohne Gnome kein Browser erkannt wird. Versuche, `libgnome` zu installieren.

```bash
$ apt-get install libgnome
```