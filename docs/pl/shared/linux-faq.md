#### P: Dlaczego edytor Defold jest supermały, gdy uruchamiam go na monitorze 4K lub HiDPI?

O: Jeśli używasz GNOME, możesz przed uruchomieniem Defold zmienić współczynnik skalowania. [źródło](https://unix.stackexchange.com/a/552411)

```bash
$ gsettings set org.gnome.desktop.interface scaling-factor 2
$ ./Defold
```

O: Alternatywnym rozwiązaniem, szczególnie gdy chcesz skalować interfejs o ułamek, jest zmodyfikowanie pliku `Defold/config` i dodanie na linii `vmargs` parametru `glass.gtk.uiScale`: [źródło](https://forum.defold.com/t/4k-hidpi-monitor-support-solved/64108/12?u=britzl)

```
vmargs = -Dglass.gtk.uiScale=1.5,-Dfile.encoding=UTF-8,...
vmargs = -Dglass.gtk.uiScale=175%,-Dfile.encoding=UTF-8,...
vmargs = -Dglass.gtk.uiScale=192dpi,-Dfile.encoding=UTF-8,...
```

Więcej o tej wartości przeczytasz w artykule wiki [Arch Linux HiDPI](https://wiki.archlinux.org/title/HiDPI#JavaFX).

O: Jeśli używasz KDE, możesz ustawić `GDK_SCALE`:

```bash
$ GDK_SCALE=2 ./Defold
```

#### P: Dlaczego kliknięcia myszy w Elementary OS przechodzą przez edytor i trafiają w to, co jest pod spodem?

O: Uruchom edytor w ten sposób:

```bash
$ GTK_CSD=0 ./Defold
```


#### P: Edytor Defold ulega awarii podczas otwierania kolekcji lub obiektu gry, a awaria dotyczy `com.jogamp.opengl`

O: W niektórych dystrybucjach, na przykład Ubuntu 18, występuje problem między wersją `jogamp`/`jogl` używaną przez Defold a wersją [Mesa](https://docs.mesa3d.org/) zainstalowaną w systemie. Możesz nadpisać wersję GL zgłaszaną przez `glGetString(GL_VERSION)`, ustawiając `MESA_GL_VERSION_OVERRIDE` na 2.1 albo na większą wartość, ale nie większą niż wersja obsługiwana przez sterownik. Maksymalną wersję OpenGL obsługiwaną przez sterownik możesz sprawdzić za pomocą `glxinfo`:

```bash
glxinfo | grep version
```

Przykładowy wynik (szukaj wiersza "OpenGL version string: x.y"):

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

Użyj wersji 2.1 albo wersji zgodnej z wersją sterownika graficznego:

```bash
$ MESA_GL_VERSION_OVERRIDE=2.1 ./Defold
```

```bash
$ MESA_GL_VERSION_OVERRIDE=4.6 ./Defold
```


#### P: Dlaczego pojawia się błąd "`com.jogamp.opengl.GLException: Graphics configuration failed`" podczas uruchamiania Defold?

O: W niektórych dystrybucjach, na przykład Ubuntu 20.04, występuje problem z nowymi sterownikami [Mesa](https://docs.mesa3d.org/) (Iris) podczas uruchamiania Defold. Możesz spróbować uruchomić Defold ze starszą wersją sterownika:

```bash
$ MESA_LOADER_DRIVER_OVERRIDE=i965 ./Defold
```


#### P: Edytor Defold ulega awarii podczas otwierania kolekcji lub obiektu gry, a awaria dotyczy `libffi.so`

O: Wersja [libffi](https://sourceware.org/libffi/) w twojej dystrybucji i wersja wymagana przez Defold (6 lub 7) nie są zgodne. Upewnij się, że `libffi.so.6` albo `libffi.so.7` jest zainstalowany w `/usr/lib/x86_64-linux-gnu`. Możesz pobrać `libffi.so.7` w taki sposób:  

```bash
$ wget http://ftp.br.debian.org/debian/pool/main/libf/libffi/libffi7_3.3-6_amd64.deb
$ sudo dpkg -i libffi7_3.3-6_amd64.deb
```

Następnie podczas uruchamiania Defold wskaż ścieżkę do tej wersji w zmiennej środowiskowej `LD_PRELOAD`:

```bash
$ LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libffi.so.7 ./Defold
```


#### P: Czy mogę nadal używać Defold, jeśli moje sterowniki OpenGL są nieaktualne?

O: Tak, może być możliwe korzystanie z Defold po włączeniu renderowania programowego. Możesz je włączyć, ustawiając zmienną środowiskową `LIBGL_ALWAYS_SOFTWARE` na 1:

```bash
$ LIBGL_ALWAYS_SOFTWARE=1 ./Defold
```


#### P: Dlaczego moja gra stworzona w Defold nie uruchamia się, gdy próbuję ją uruchomić w systemie Linux?

O: Sprawdź wyjście konsoli w edytorze. Jeśli zobaczysz następujący komunikat:

```
dmengine: error while loading shared libraries: libopenal.so.1: cannot open shared object file: No such file or directory
```

Musisz zainstalować *`libopenal1`*. Nazwa pakietu różni się w zależności od dystrybucji i w niektórych przypadkach może być konieczne zainstalowanie pakietów *`openal`* oraz *`openal-dev`* lub *`openal-devel`*.

```bash
$ apt-get install libopenal-dev
```

#### P: Dlaczego górne menu zamyka się, zanim zdążę coś wybrać?

O: Najpewniej powoduje to używany menedżer okien, na przykład `Qtile` lub i3. To [znany problem w JavaFX](https://bugs.openjdk.org/browse/JDK-8251240?focusedCommentId=14362084&page=com.atlassian.jira.plugin.system.issuetabpanels%3Acomment-tabpanel#comment-14362084) i można go rozwiązać albo przez ustawienie zmiennej środowiskowej `GDK_DISPLAY` na 1:

```bash
$ GDK_DISPLAY=1 ./Defold

D=2

```

Albo przez zmodyfikowanie pliku `Defold/config` i dodanie na linii `vmargs` parametru `-Djdk.gtk.version=2`:

```
vmargs = -Djdk.gtk.version=2,-Dfile.encoding=UTF-8,...
```


#### P: Dlaczego nie mogę przeglądać wszystkich dostępnych lokalizacji plików po wybraniu Open From Disk?

O: Jeśli uruchamiasz Defold z [Steam przez Flatpak](https://flathub.org/apps/com.valvesoftware.Steam), musisz nadać Steam uprawnienia do dostępu do innych dysków. Możesz zmienić uprawnienia aplikacji Flatpak za pomocą [Flatseal](https://flathub.org/apps/com.github.tchx84.Flatseal) lub podobnego narzędzia.


#### P: Dlaczego nie mogę otworzyć web profiler albo innej opcji menu, która wymaga przeglądarki?

O: Najprawdopodobniej wewnętrzne wywołanie `Desktop.getDesktop().browse(new URI(url));` kończy się niepowodzeniem, ponieważ w systemach innych niż GNOME nie wykryto przeglądarki. Spróbuj zainstalować `libgnome`.

```bash
$ apt-get install libgnome
```
