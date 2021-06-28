#### Q: 在 GNOME 上使用 Defold 编辑器在 4k 或 HiDPI 显示器上显得特别小?

A: 启动 Defold 之前修改缩放参数. [参见](https://unix.stackexchange.com/a/552411)

```bash
$ gsettings set org.gnome.desktop.interface scaling-factor 2
$ ./Defold
```


#### Q:在 Elementary OS 上使用 Defold 编辑器, 鼠标点选上的都是后面的东西?

A: 尝试这样启动编辑器:

```bash
$ GTK_CSD=0 ./Defold
```


#### Q: 在 Defold 编辑器里打开集合或者游戏对象时崩溃报关于 "com.jogamp.opengl" 的错误.

A: 某些Linux版本 (如 Ubuntu 18) 下 [Mesa](https://docs.mesa3d.org/) 版所使用的 jogamp/jogl Defold 版本有冲突.
可以在调用 `glGetString(GL_VERSION)` 是设置`MESA_GL_VERSION_OVERRIDE` 为2.1或者更高的值以覆盖 GL 默认的驱动版本.
可以使用如下命令查看系统上支持 `glxinfo` 的最高 OpenGL 版本:

```bash
glxinfo | grep version
```

输出举例 (注意 "OpenGL version string: x.y"):

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

使用版本 2.1 或者更高的匹配显卡的版本:

```bash
$ MESA_GL_VERSION_OVERRIDE=2.1 ./Defold
```

```bash
$ MESA_GL_VERSION_OVERRIDE=4.6 ./Defold
```


A: 某些Linux版本 (如 Ubuntu 20.04) 在運行 Defold 時會出現新的 [Mesa](https://docs.mesa3d.org/) 驅動程序 (Iris) 的問題. 可以嘗試使用舊版本驅動程序:

```bash
$ export MESA_LOADER_DRIVER_OVERRIDE=i965
$ ./Defold
```


#### Q: 在 Defold 编辑器里打开集合或者游戏对象时崩溃报关于 "libffi.so" 的错误.

A: 这是由于Linux系统的 [libffi](https://sourceware.org/libffi/) 版本与 Defold (版本 6 或 7) 需要的版本不一致.
确保 `libffi.so.6` 或 `libffi.so.7` 已安装在 `/usr/lib/x86_64-linux-gnu` 路径下. 可以使用如下命令下载 `libffi.so.7`:

```bash
$ wget http://ftp.br.debian.org/debian/pool/main/libf/libffi/libffi7_3.3-6_amd64.deb
$ sudo dpkg -i libffi7_3.3-6_amd64.deb
```

然后需要在环境变量 `LD_PRELOAD` 中指定安装路径再启动 Defold:

```bash
$ LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libffi.so.7 ./Defold
```


#### Q: 我的 OpenGL 驱动过期了. 还能用 Defold 吗?

A: 能用, 但是需要打开 Defold 软件渲染. 可以设置环境变量 LIBGL_ALWAYS_SOFTWARE 值为 1:

```bash
~/bin/Defold$ LIBGL_ALWAYS_SOFTWARE=1 ./Defold
```


#### Q: 在 Linux 上启动 Defold 游戏无效?

A: 看看 Defold 编辑器控制台. 如果有下面这样的输出:

```
dmengine: error while loading shared libraries: libopenal.so.1: cannot open shared object file: No such file or directory
```

就需要安装 *libopenal1*. 不同版本包名不同, 另外某些用户也需要安装 *openal* 和 *openal-dev* 或者 *openal-devel* 包.

```bash
$ apt-get install libopenal-dev
```
