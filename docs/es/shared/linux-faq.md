#### Q: ¿Por qué el editor Defold es super pequeño cuando ejecuto en un monitor 4k o HiDPI utilizando GNOME?

A: Cambia el factor de escala antes de correr Defold. [source](https://unix.stackexchange.com/a/552411)

```bash
$ gsettings set org.gnome.desktop.interface scaling-factor 2
$ ./Defold
```


#### Q: ¿Por qué los clicks del ratón en Elementary OS atraviesan el editor hacia lo que haya detrás de éste?

A: Empieza el editor así:

```bash
$ GTK_CSD=0 ./Defold
```


#### Q: El editor Defold crashea cuando abro una colección u objeto de juego y el crash se refiere a "com.jogamp.opengl"

A: En ciertas distribuciones (como Ubuntu 18) existe un error con la versión de jogamp/jogl que usa Defold vs. la versión de [Mesa](https://docs.mesa3d.org/) en el sistema. Puedes sobreescribir cuál versión de GL sea reportado cuando llames a `glGetString(GL_VERSION)` cambiando el valor de `MESA_GL_VERSION_OVERRIDE` a 2.1 o un valor más alto pero menos o igual que la versión de tu driver. Puedes verificar cual es la versión máxima de OpenGL que soporta tu driver usando `glxinfo`:

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

Usa la versión 2.1 o la versión que iguala tu driver de gráficos:

```bash
$ MESA_GL_VERSION_OVERRIDE=2.1 ./Defold
```

```bash
$ MESA_GL_VERSION_OVERRIDE=4.6 ./Defold
```


#### Q: ¿Por qué obtengo "com.jogamp.opengl.GLException: Graphics configuration failed" cuando lanzo Defold?

A: En ciertas distribuciones (por ejemplo Ubuntu 20.04) existe un error con el nuevo driver de [Mesa](https://docs.mesa3d.org/) (Iris) cuando ejecutas Defold. Puedes intentar usar una versión anterior del driver cuando ejecutes Defold:

```bash
$ MESA_LOADER_DRIVER_OVERRIDE=i965 ./Defold
```


#### Q: El editor Defold crashea cuando abro una colección u objeto de juego y el cras refiere a libffi.so

A: La versión [libffi](https://sourceware.org/libffi/) de tu distribución y la requerida por Defold (version 6 or 7) no son iguales. Asegúrate que `libffi.so.6` o `libffi.so.7` estén instalados bajo `/usr/lib/x86_64-linux-gnu`. Puedes descargar `libffi.so.7` de la siguiente forma:  

```bash
$ wget http://ftp.br.debian.org/debian/pool/main/libf/libffi/libffi7_3.3-5_amd64.deb
$ sudo dpkg -i libffi7_3.3-5_amd64.deb
```

Luego especifica la ruta de esta versión en la variable del ambiente `LD_PRELOAD` cuando ejecutes Defold:

```bash
$ LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libffi.so.7 ./Defold
```


#### Q: Mis drivers de OpenGL están desactualizados. ¿Puedo seguir utilizando Defold?

A: Si, puede ser posible usar Defold si habilitas el renderizado por software. Puedes habilitar el renderizado por software cambiando la variable de ambiente `LIBGL_ALWAYS_SOFTWARE` a 1:

```bash
$ LIBGL_ALWAYS_SOFTWARE=1 ./Defold
```


#### Q: ¿Por qué mi juego Defold no inicia cuando lo intento ejecutar en Linux?

A: Verifica la salida de consola (console output) en el editor. Si obtienes el siguiente mensaje:

```
dmengine: error while loading shared libraries: libopenal.so.1: cannot open shared object file: No such file or directory
```

Entonces necesitas instalar *libopenal1*. El nombre del paquete varía entre distribuciones, y en algunos casos también necesitarás instalar los paquetes *openal* y *openal-dev* o *openal-devel*.

```bash
$ apt-get install libopenal-dev
```
