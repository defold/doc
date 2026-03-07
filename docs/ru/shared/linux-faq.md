#### Q: Почему редактор Defold выглядит очень маленьким на 4k- или HiDPI-мониторе?

A: Если вы используете GNOME, можно изменить коэффициент масштабирования перед запуском Defold. [источник](https://unix.stackexchange.com/a/552411)

```bash
$ gsettings set org.gnome.desktop.interface scaling-factor 2
$ ./Defold
```

A: Альтернативный вариант, особенно если вам нужно масштабирование с дробным коэффициентом, — изменить файл `Defold/config` и добавить `glass.gtk.uiScale` в строку `vmargs`: [источник](https://forum.defold.com/t/4k-hidpi-monitor-support-solved/64108/12?u=britzl)

```
vmargs = -Dglass.gtk.uiScale=1.5,-Dfile.encoding=UTF-8,...
vmargs = -Dglass.gtk.uiScale=175%,-Dfile.encoding=UTF-8,...
vmargs = -Dglass.gtk.uiScale=192dpi,-Dfile.encoding=UTF-8,...
```

Подробнее об этом значении смотрите в [статье Arch Linux HiDPI wiki](https://wiki.archlinux.org/title/HiDPI#JavaFX).

A: Если вы используете KDE, можно задать `GDK_SCALE`:

```bash
$ GDK_SCALE=2 ./Defold
```

#### Q: Почему клики мышью в Elementary OS проходят через редактор на окно под ним?

A: Запустите редактор так:

```bash
$ GTK_CSD=0 ./Defold
```


#### Q: Редактор Defold падает при открытии collection или game object, и в сообщении об ошибке упоминается `com.jogamp.opengl`

A: На некоторых дистрибутивах (например, Ubuntu 18) есть проблема с версией `jogamp`/`jogl`, используемой в Defold, и версией [Mesa](https://docs.mesa3d.org/) в системе. Вы можете переопределить GL-версию, которая возвращается при вызове `glGetString(GL_VERSION)`, установив `MESA_GL_VERSION_OVERRIDE` в 2.1 или в большее значение, но не выше версии вашего драйвера. Проверить максимальную поддерживаемую версию OpenGL драйвера можно через `glxinfo`:

```bash
glxinfo | grep version
```

Пример вывода (ищите "OpenGL version string: x.y"):

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

Используйте версию 2.1 или версию, совпадающую с версией вашего графического драйвера:

```bash
$ MESA_GL_VERSION_OVERRIDE=2.1 ./Defold
```

```bash
$ MESA_GL_VERSION_OVERRIDE=4.6 ./Defold
```


#### Q: Почему при запуске Defold я получаю "`com.jogamp.opengl.GLException: Graphics configuration failed`"?

A: На некоторых дистрибутивах (например, Ubuntu 20.04) есть проблема с новыми драйверами [Mesa](https://docs.mesa3d.org/) (Iris) при запуске Defold. Можно попробовать использовать более старую версию драйвера при запуске Defold:

```bash
$ MESA_LOADER_DRIVER_OVERRIDE=i965 ./Defold
```


#### Q: Редактор Defold падает при открытии collection или game object, и в сообщении об ошибке упоминается `libffi.so`

A: Версия [libffi](https://sourceware.org/libffi/) в вашем дистрибутиве не совпадает с той, которая нужна Defold (версия 6 или 7). Убедитесь, что `libffi.so.6` или `libffi.so.7` установлены в `/usr/lib/x86_64-linux-gnu`. Скачать `libffi.so.7` можно так:  

```bash
$ wget http://ftp.br.debian.org/debian/pool/main/libf/libffi/libffi7_3.3-6_amd64.deb
$ sudo dpkg -i libffi7_3.3-6_amd64.deb
```

Затем укажите путь к этой версии в переменной окружения `LD_PRELOAD` при запуске Defold:

```bash
$ LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libffi.so.7 ./Defold
```


#### Q: Мои OpenGL-драйверы устарели. Могу ли я всё ещё использовать Defold?

A: Да, возможно, вы сможете использовать Defold, если включите software rendering. Это делается через установку переменной окружения `LIBGL_ALWAYS_SOFTWARE` в значение 1:

```bash
$ LIBGL_ALWAYS_SOFTWARE=1 ./Defold
```


#### Q: Почему моя игра Defold не запускается, когда я пытаюсь запустить её на Linux?

A: Проверьте вывод консоли в редакторе. Если вы видите следующее сообщение:

```
dmengine: error while loading shared libraries: libopenal.so.1: cannot open shared object file: No such file or directory
```

Тогда вам нужно установить *`libopenal1`*. Название пакета зависит от дистрибутива, и в некоторых случаях может потребоваться установить пакеты *`openal`* и *`openal-dev`* или *`openal-devel`*.

```bash
$ apt-get install libopenal-dev
```

#### Q: Почему верхнее меню закрывается раньше, чем я успеваю что-то выбрать?

A: Скорее всего, это вызвано используемым оконным менеджером (например, `Qtile` или i3). Это [известная проблема в JavaFX](https://bugs.openjdk.org/browse/JDK-8251240?focusedCommentId=14362084&page=com.atlassian.jira.plugin.system.issuetabpanels%3Acomment-tabpanel#comment-14362084), и её можно решить либо установкой переменной окружения `GDK_DISPLAY` в 1:¨

```bash
$ GDK_DISPLAY=1 ./Defold

D=2

```

Либо изменив файл `Defold/config` и добавив `-Djdk.gtk.version=2` в строку `vmargs`:

```
vmargs = -Djdk.gtk.version=2,-Dfile.encoding=UTF-8,...
```


#### Q: Почему я не могу просматривать все доступные пути при выборе Open From Disk?

A: Если вы запускаете Defold из [Steam через Flatpak](https://flathub.org/apps/com.valvesoftware.Steam), нужно выдать Steam разрешение на доступ к другим дискам. Изменить разрешения приложений Flatpak можно через [Flatseal](https://flathub.org/apps/com.github.tchx84.Flatseal) или аналогичный инструмент.


#### Q: Почему я не могу открыть web profiler или любой другой пункт меню, для которого нужен браузер?

A: Скорее всего, внутренний вызов `Desktop.getDesktop().browse(new URI(url));` завершается ошибкой, потому что в не-Gnome-системах браузер не обнаруживается. Попробуйте установить `libgnome`.

```bash
$ apt-get install libgnome
```
