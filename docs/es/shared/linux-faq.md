#### Q: ¿Por qué el editor Defold se ve muy pequeño cuando se ejecuta en un monitor 4k o HiDPI?

A: Si usas GNOME, puedes cambiar el factor de escala antes de ejecutar Defold. [fuente](https://unix.stackexchange.com/a/552411)

```bash
$ gsettings set org.gnome.desktop.interface scaling-factor 2
$ ./Defold
```

A: Una solución alternativa, especialmente si quieres aumentar la escala por una fracción, es modificar el archivo `Defold/config` y agregar `glass.gtk.uiScale` en la línea `vmargs`: [fuente](https://forum.defold.com/t/4k-hidpi-monitor-support-solved/64108/12?u=britzl)

```
vmargs = -Dglass.gtk.uiScale=1.5,-Dfile.encoding=UTF-8,...
vmargs = -Dglass.gtk.uiScale=175%,-Dfile.encoding=UTF-8,...
vmargs = -Dglass.gtk.uiScale=192dpi,-Dfile.encoding=UTF-8,...
```

Más información sobre este valor en el [artículo de la wiki de Arch Linux sobre HiDPI](https://wiki.archlinux.org/title/HiDPI#JavaFX).

A: Si usas KDE, puedes definir `GDK_SCALE`:

```bash
$ GDK_SCALE=2 ./Defold
```

#### Q: ¿Por qué los clicks del mouse en Elementary OS atraviesan el editor y afectan lo que haya debajo?

A: Inicia el editor así:

```bash
$ GTK_CSD=0 ./Defold
```


#### Q: El editor Defold se cierra inesperadamente al abrir una colección o un objeto de juego y el crash hace referencia a `com.jogamp.opengl`

A: En ciertas distribuciones (como Ubuntu 18) hay un problema entre la versión de `jogamp`/`jogl` que usa Defold y la versión de [Mesa](https://docs.mesa3d.org/) en el sistema. Puedes sobrescribir la versión de GL que se reporta al llamar a `glGetString(GL_VERSION)` definiendo `MESA_GL_VERSION_OVERRIDE` en 2.1 o en un valor mayor, pero menor o igual que la versión de tu driver. Puedes comprobar cuál es la versión máxima de OpenGL que soporta tu driver con `glxinfo`:

```bash
glxinfo | grep version
```

Ejemplo de salida (busca "OpenGL version string: x.y"):

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

Usa la versión 2.1 o la versión que coincida con tu driver gráfico:

```bash
$ MESA_GL_VERSION_OVERRIDE=2.1 ./Defold
```

```bash
$ MESA_GL_VERSION_OVERRIDE=4.6 ./Defold
```


#### Q: ¿Por qué obtengo `com.jogamp.opengl.GLException: Graphics configuration failed` cuando inicio Defold?

A: En ciertas distribuciones (por ejemplo Ubuntu 20.04) hay un problema con los drivers nuevos de [Mesa](https://docs.mesa3d.org/) (Iris) al ejecutar Defold. Puedes intentar usar una versión anterior del driver al ejecutar Defold:

```bash
$ MESA_LOADER_DRIVER_OVERRIDE=i965 ./Defold
```


#### Q: El editor Defold se cierra inesperadamente al abrir una colección o un objeto de juego y el crash hace referencia a `libffi.so`

A: La versión de [libffi](https://sourceware.org/libffi/) de tu distribución y la que requiere Defold (versión 6 o 7) no coinciden. Asegúrate de que `libffi.so.6` o `libffi.so.7` esté instalado en `/usr/lib/x86_64-linux-gnu`. Puedes descargar `libffi.so.7` así:

```bash
$ wget http://ftp.br.debian.org/debian/pool/main/libf/libffi/libffi7_3.3-6_amd64.deb
$ sudo dpkg -i libffi7_3.3-6_amd64.deb
```

Luego especifica la ruta a esta versión en la variable de ambiente `LD_PRELOAD` al ejecutar Defold:

```bash
$ LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libffi.so.7 ./Defold
```


#### Q: Mis drivers de OpenGL están desactualizados. ¿Puedo seguir usando Defold?

A: Sí, puede ser posible usar Defold si habilitas el renderizado por software. Puedes habilitar el renderizado por software definiendo la variable de ambiente `LIBGL_ALWAYS_SOFTWARE` en 1:

```bash
$ LIBGL_ALWAYS_SOFTWARE=1 ./Defold
```


#### Q: ¿Por qué mi juego de Defold no se inicia cuando intento ejecutarlo en Linux?

A: Revisa la salida de la consola en el editor. Si obtienes el siguiente mensaje:

```
dmengine: error while loading shared libraries: libopenal.so.1: cannot open shared object file: No such file or directory
```

Entonces necesitas instalar *`libopenal1`*. El nombre del paquete varía entre distribuciones, y en algunos casos puede que tengas que instalar los paquetes *`openal`* y *`openal-dev`* o *`openal-devel`*.

```bash
$ apt-get install libopenal-dev
```

#### Q: ¿Por qué el menú superior se cierra antes de que pueda seleccionar algo?

A: Probablemente lo causa el gestor de ventanas utilizado (por ejemplo `Qtile` o i3). Es un [problema conocido de JavaFX](https://bugs.openjdk.org/browse/JDK-8251240?focusedCommentId=14362084&page=com.atlassian.jira.plugin.system.issuetabpanels%3Acomment-tabpanel#comment-14362084) y se puede resolver definiendo la variable de ambiente `GDK_DISPLAY` en 1:

```bash
$ GDK_DISPLAY=1 ./Defold

D=2

```

O modificando el archivo `Defold/config` y agregando `-Djdk.gtk.version=2` en la línea `vmargs`:

```
vmargs = -Djdk.gtk.version=2,-Dfile.encoding=UTF-8,...
```


#### Q: ¿Por qué no puedo explorar todas las ubicaciones de archivos disponibles cuando selecciono Open From Disk?

A: Si ejecutas Defold desde [Steam usando Flatpak](https://flathub.org/apps/com.valvesoftware.Steam), necesitas dar permiso a Steam para acceder a tus otros discos. Puedes modificar los permisos de tus aplicaciones Flatpak con [Flatseal](https://flathub.org/apps/com.github.tchx84.Flatseal) o una herramienta similar.


#### Q: ¿Por qué no puedo abrir el profiler web ni ninguna otra opción de menú que requiere un navegador?

A: Es probable que falle una llamada interna a `Desktop.getDesktop().browse(new URI(url));` porque no se detecta ningún navegador en sistemas que no son GNOME. Intenta instalar `libgnome`.

```bash
$ apt-get install libgnome
```
