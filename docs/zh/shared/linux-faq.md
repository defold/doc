#### Q: 在 GNOME 上使用 Defold 编辑器在 4k 或 HiDPI 显示器上显得特别小?

A: 启动 Defold 之前修改缩放参数. [参见](https://unix.stackexchange.com/a/552411)

```bash
$ gsettings set org.gnome.desktop.interface scaling-factor 2
```


#### Q:在 Elementary OS 上使用 Defold 编辑器, 鼠标点选上的都是后面的东西?

A: 尝试这样启动编辑器:

```bash
$ GTK_CSD=0 ./Defold
```


#### Q: 在新建, 打开项目时 Defold 编辑器崩溃?

A: 某些版本 (比如 Ubuntu 18) 上 Defold 使用的 jogamp/jogl 版本与系统 Mesa 版本冲突.

详情请见:

  - https://github.com/defold/editor2-issues/issues/1905
  - https://github.com/defold/editor2-issues/issues/1886

使用如下代码可以绕过冲突:

```bash
$ export MESA_GL_VERSION_OVERRIDE=2.1
$ ./Defold
```

如果问题没有解决可以尝试 (根据你自己的驱动匹配选取大于等于 2.1 的版本号):

```bash
$ export MESA_GL_VERSION_OVERRIDE=3.1
$ ./Defold
```


#### Q: 我的 OpenGL 驱动过期了. 还能用 Defold 吗?

A: 能用, 但是需要打开 Defold 软件渲染. 可以设置环境变量 LIBGL_ALWAYS_SOFTWARE 值为 1:

```bash
~/bin/Defold$ LIBGL_ALWAYS_SOFTWARE=1 ./Defold
```


#### Q: 在 Ubuntu 20.04 上運行 Defold 報錯 "com.jogamp.opengl.GLException: Graphics configuration failed" ?

A: 這個版本在運行 Defold 時會出現新驅動程序 (Iris) 問題. 可以嘗試使用舊版本驅動程序:

```bash
$ export MESA_LOADER_DRIVER_OVERRIDE=i965
$ ./Defold
```

可能还需要指定载入 libffi 版本 6 才能启动 Defold:

```bash
$ export LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libffi.so.6
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
