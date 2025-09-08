#### Q: 为什么在 4k 或 HiDPI 显示器上运行 Defold 编辑器时显得特别小？

A: 如果您使用的是 GNOME，可以在运行 Defold 之前更改缩放因子。[来源](https://unix.stackexchange.com/a/552411)

```bash
$ gsettings set org.gnome.desktop.interface scaling-factor 2
$ ./Defold
```

A: 另一种解决方案，特别是当您希望按分数比例放大时，是修改 `Defold/config` 文件并在 `vmargs` 行添加 `glass.gtk.uiScale`：[来源](https://forum.defold.com/t/4k-hidpi-monitor-support-solved/64108/12?u=britzl)

```
vmargs = -Dglass.gtk.uiScale=1.5,-Dfile.encoding=UTF-8,...
vmargs = -Dglass.gtk.uiScale=175%,-Dfile.encoding=UTF-8,...
vmargs = -Dglass.gtk.uiScale=192dpi,-Dfile.encoding=UTF-8,...
```

有关此值的更多信息，请参见 [Arch Linux HiDPI wiki 文章](https://wiki.archlinux.org/title/HiDPI#JavaFX)。

A: 如果您使用的是 KDE，可以设置 `GDK_SCALE`：

```bash
$ GDK_SCALE=2 ./Defold
```

#### Q: 为什么在 Elementary OS 上鼠标点击会穿过编辑器到达下面的任何内容？

A: 像这样启动编辑器：

```bash
$ GTK_CSD=0 ./Defold
```


#### Q: 当打开集合或游戏对象时，Defold 编辑器崩溃，崩溃信息提到 `com.jogamp.opengl`

A: 在某些发行版（如 Ubuntu 18）上，Defold 使用的 `jogamp`/`jogl` 版本与系统上的 [Mesa](https://docs.mesa3d.org/) 版本存在问题。您可以通过设置 `MESA_GL_VERSION_OVERRIDE` 为 2.1 或更大但小于或等于您驱动程序版本的值来覆盖调用 `glGetString(GL_VERSION)` 时报告的 GL 版本。您可以使用 `glxinfo` 检查您的驱动程序支持的最高 OpenGL 版本：

```bash
glxinfo | grep version
```

示例输出（查找 "OpenGL version string: x.y"）：

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

使用版本 2.1 或匹配您的图形驱动程序的版本：

```bash
$ MESA_GL_VERSION_OVERRIDE=2.1 ./Defold
```

```bash
$ MESA_GL_VERSION_OVERRIDE=4.6 ./Defold
```


#### Q: 为什么启动 Defold 时出现 "`com.jogamp.opengl.GLException: Graphics configuration failed`" 错误？

A: 在某些发行版（例如 Ubuntu 20.04）上，运行 Defold 时新的 [Mesa](https://docs.mesa3d.org/) 驱动程序（Iris）存在问题。您可以尝试在运行 Defold 时使用较旧的驱动程序版本：

```bash
$ MESA_LOADER_DRIVER_OVERRIDE=i965 ./Defold
```


#### Q: 当打开集合或游戏对象时，Defold 编辑器崩溃，崩溃信息提到 `libffi.so`

A: 您发行版的 [libffi](https://sourceware.org/libffi/) 版本与 Defold（版本 6 或 7）所需的版本不匹配。确保 `libffi.so.6` 或 `libffi.so.7` 安装在 `/usr/lib/x86_64-linux-gnu` 下。您可以像这样下载 `libffi.so.7`：

```bash
$ wget http://ftp.br.debian.org/debian/pool/main/libf/libffi/libffi7_3.3-6_amd64.deb
$ sudo dpkg -i libffi7_3.3-6_amd64.deb
```

接下来，在运行 Defold 时，在 `LD_PRELOAD` 环境变量中指定此版本的路径：

```bash
$ LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libffi.so.7 ./Defold
```


#### Q: 我的 OpenGL 驱动程序已过时。我还能使用 Defold 吗？

A: 是的，如果您启用软件渲染，可能仍然可以使用 Defold。您可以通过将 `LIBGL_ALWAYS_SOFTWARE` 环境变量设置为 1 来启用软件渲染：

```bash
$ LIBGL_ALWAYS_SOFTWARE=1 ./Defold
```


#### Q: 为什么我尝试在 Linux 上运行 Defold 游戏时无法启动？

A: 检查编辑器中的控制台输出。如果您收到以下消息：

```
dmengine: error while loading shared libraries: libopenal.so.1: cannot open shared object file: No such file or directory
```

那么您需要安装 *`libopenal1`*。软件包名称在不同发行版之间有所不同，在某些情况下，您可能需要安装 *`openal`* 和 *`openal-dev`* 或 *`openal-devel`* 软件包。

```bash
$ apt-get install libopenal-dev
```

#### Q: 为什么顶部菜单在我选择某项之前就关闭了？

A: 这很可能是由使用的窗口管理器（例如 `Qtile` 或 i3）引起的。这是 [JavaFX 中的一个已知问题](https://bugs.openjdk.org/browse/JDK-8251240?focusedCommentId=14362084&page=com.atlassian.jira.plugin.system.issuetabpanels%3Acomment-tabpanel#comment-14362084)，可以通过将 `GDK_DISPLAY` 环境变量设置为 1 来解决：

```bash
$ GDK_DISPLAY=1 ./Defold
```

或者通过修改 `Defold/config` 文件并在 `vmargs` 行添加 `-Djdk.gtk.version=2`：

```
vmargs = -Djdk.gtk.version=2,-Dfile.encoding=UTF-8,...
```


#### Q: 为什么当我选择从磁盘打开时无法浏览所有可用的文件位置？

A: 如果您通过 [使用 Flatpak 的 Steam](https://flathub.org/apps/com.valvesoftware.Steam) 运行 Defold，您需要授予 Steam 访问其他驱动器的权限。您可以使用 [Flatseal](https://flathub.org/apps/com.github.tchx84.Flatseal) 或类似工具修改您的 Flatpak 应用程序的权限。


#### Q: 为什么我无法打开 Web 分析器或任何其他需要浏览器的菜单选项？

A: 这很可能是因为在非 Gnome 系统上没有检测到浏览器，导致对 `Desktop.getDesktop().browse(new URI(url));` 的内部调用失败。尝试安装 `libgnome`。

```bash
$ apt-get install libgnome
```
