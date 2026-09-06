#### Запитання: Чому редактор Defold виглядає дуже дрібним на моніторі 4K або HiDPI? {#q-why-is-the-defold-editor-super-small-when-run-on-a-4k-or-hidpi-monitor}

Відповідь: Якщо ви використовуєте GNOME, можна змінити коефіцієнт масштабування перед запуском Defold. [Джерело](https://unix.stackexchange.com/a/552411)

```bash
$ gsettings set org.gnome.desktop.interface scaling-factor 2
$ ./Defold
```

Відповідь: Інший спосіб, особливо якщо потрібен дробовий коефіцієнт збільшення, — змінити файл `Defold/config`, додавши `glass.gtk.uiScale` до рядка `vmargs`: [джерело](https://forum.defold.com/t/4k-hidpi-monitor-support-solved/64108/12?u=britzl)

```
vmargs = -Dglass.gtk.uiScale=1.5,-Dfile.encoding=UTF-8,...
vmargs = -Dglass.gtk.uiScale=175%,-Dfile.encoding=UTF-8,...
vmargs = -Dglass.gtk.uiScale=192dpi,-Dfile.encoding=UTF-8,...
```

Докладніше про це значення див. у [статті вікі Arch Linux про HiDPI](https://wiki.archlinux.org/title/HiDPI#JavaFX).

Відповідь: Якщо ви використовуєте KDE, можна задати `GDK_SCALE`:

```bash
$ GDK_SCALE=2 ./Defold
```

#### Запитання: Чому в Elementary OS клацання мишею проходять крізь редактор до вмісту під ним? {#q-why-does-mouse-clicks-on-elementary-os-go-through-the-editor-onto-whatever-is-below}

Відповідь: Запустіть редактор так:

```bash
$ GTK_CSD=0 ./Defold
```


#### Запитання: Редактор Defold аварійно завершує роботу під час відкриття колекції або ігрового об’єкта, а в повідомленні про збій згадано `com.jogamp.opengl` {#q-the-defold-editor-crashes-when-opening-a-collection-or-game-object-and-the-crash-refers-to-comjogampopengl}

Відповідь: У деяких дистрибутивах (як-от Ubuntu 18) є проблема сумісності версії `jogamp`/`jogl`, яку використовує Defold, з версією [Mesa](https://docs.mesa3d.org/) у системі. Ви можете перевизначити версію GL, яку повертає виклик `glGetString(GL_VERSION)`, задавши для `MESA_GL_VERSION_OVERRIDE` значення 2.1 або більше, але не вище версії, яку підтримує ваш драйвер. Перевірити максимальну версію OpenGL, яку підтримує драйвер, можна за допомогою `glxinfo`:

```bash
glxinfo | grep version
```

Приклад виведення (шукайте «OpenGL version string: x.y»):

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

Використовуйте версію 2.1 або версію, що відповідає вашому графічному драйверу:

```bash
$ MESA_GL_VERSION_OVERRIDE=2.1 ./Defold
```

```bash
$ MESA_GL_VERSION_OVERRIDE=4.6 ./Defold
```


#### Запитання: Чому під час запуску Defold з’являється помилка «`com.jogamp.opengl.GLException: Graphics configuration failed`»? {#q-why-am-i-getting-comjogampopenglglexception-graphics-configuration-failed-when-launching-defold}

Відповідь: У деяких дистрибутивах (наприклад, Ubuntu 20.04) під час роботи Defold виникає проблема з новими драйверами [Mesa](https://docs.mesa3d.org/) (Iris). Ви можете спробувати запустити Defold зі старішою версією драйвера:

```bash
$ MESA_LOADER_DRIVER_OVERRIDE=i965 ./Defold
```


#### Запитання: Редактор Defold аварійно завершує роботу під час відкриття колекції або ігрового об’єкта, а в повідомленні про збій згадано `libffi.so` {#q-the-defold-editor-crashes-when-opening-a-collection-or-game-object-and-the-crash-refers-to-libffiso}

Відповідь: Версія [libffi](https://sourceware.org/libffi/) у вашому дистрибутиві не відповідає тій, яку потребує Defold (версія 6 або 7). Переконайтеся, що `libffi.so.6` або `libffi.so.7` встановлено в `/usr/lib/x86_64-linux-gnu`. Ви можете завантажити `libffi.so.7` так:  

```bash
$ wget http://ftp.br.debian.org/debian/pool/main/libf/libffi/libffi7_3.3-6_amd64.deb
$ sudo dpkg -i libffi7_3.3-6_amd64.deb
```

Далі під час запуску Defold вкажіть шлях до цієї версії у змінній середовища `LD_PRELOAD`:

```bash
$ LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libffi.so.7 ./Defold
```


#### Запитання: Мої драйвери OpenGL застаріли. Чи можу я користуватися Defold? {#q-my-opengl-drivers-are-outdated-can-i-still-use-defold}

Відповідь: Так, можливо, ви зможете користуватися Defold, якщо ввімкнете програмний рендеринг. Для цього задайте змінній середовища `LIBGL_ALWAYS_SOFTWARE` значення 1:

```bash
$ LIBGL_ALWAYS_SOFTWARE=1 ./Defold
```


#### Запитання: Чому моя гра Defold не запускається в Linux? {#q-why-doesnt-my-defold-game-start-when-i-try-to-run-it-on-linux}

Відповідь: Перевірте виведення консолі в редакторі. Якщо ви бачите таке повідомлення:

```
dmengine: error while loading shared libraries: libopenal.so.1: cannot open shared object file: No such file or directory
```

то потрібно встановити *`libopenal1`*. Назва пакета залежить від дистрибутива, і в деяких випадках може знадобитися встановити пакети *`openal`* та *`openal-dev`* або *`openal-devel`*.

```bash
$ apt-get install libopenal-dev
```

#### Запитання: Чому верхнє меню закривається, перш ніж я встигаю щось вибрати? {#q-why-does-the-top-menu-close-before-i-can-select-something}

Відповідь: Імовірно, це спричинено віконним менеджером, який ви використовуєте (наприклад, `Qtile` або i3). Це [відома проблема JavaFX](https://bugs.openjdk.org/browse/JDK-8251240?focusedCommentId=14362084&page=com.atlassian.jira.plugin.system.issuetabpanels%3Acomment-tabpanel#comment-14362084), яку можна розв’язати, задавши змінній середовища `GDK_DISPLAY` значення 1:

```bash
$ GDK_DISPLAY=1 ./Defold

D=2

```

Або змінивши файл `Defold/config` і додавши `-Djdk.gtk.version=2` до рядка `vmargs`:

```
vmargs = -Djdk.gtk.version=2,-Dfile.encoding=UTF-8,...
```


#### Запитання: Чому після вибору Open From Disk я не можу переглянути всі доступні розташування файлів? {#q-why-am-i-not-able-to-browse-all-available-file-locations-when-i-select-open-from-disk}

Відповідь: Якщо ви запускаєте Defold зі [Steam, встановленого через Flatpak](https://flathub.org/apps/com.valvesoftware.Steam), потрібно надати Steam дозвіл на доступ до інших дисків. Змінити дозволи застосунків Flatpak можна за допомогою [Flatseal](https://flathub.org/apps/com.github.tchx84.Flatseal) або подібного засобу.


#### Запитання: Чому я не можу відкрити вебпрофайлер або скористатися іншими пунктами меню, що потребують браузера? {#q-why-am-i-not-able-to-open-the-web-profiler-or-any-other-menu-option-which-requires-a-browser}

Відповідь: Імовірно, внутрішній виклик `Desktop.getDesktop().browse(new URI(url));` завершується помилкою, оскільки в системах без GNOME браузер не виявляється. Спробуйте встановити `libgnome`.

```bash
$ apt-get install libgnome
```
