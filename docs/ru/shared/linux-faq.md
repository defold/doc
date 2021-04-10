#### Q: Why is the Defold editor super small when run on a 4k or HiDPI monitor when using GNOME?

A: Change the scaling factor before running Defold. [source](https://unix.stackexchange.com/a/552411)

```bash
$ gsettings set org.gnome.desktop.interface scaling-factor 2
```


#### Q: Why does mouse clicks on Elementary OS go through the editor onto whatever is below?

A: Start the editor like this:

```bash
$ GTK_CSD=0 ./Defold
```


#### Q: Why does the Defold editor crash when I try to create a new project, or open an existing one?

A: On certain distributions (like Ubuntu 18) there is an issue with the version of jogamp/jogl Defold uses vs. the version of Mesa on the system.

See the following reports for more information:

  - https://github.com/defold/editor2-issues/issues/1905
  - https://github.com/defold/editor2-issues/issues/1886

If this is your problem try the following workaround:

```bash
$ export MESA_GL_VERSION_OVERRIDE=2.1
$ ./Defold
```

And if that doesn't work then try (or some other version number matching your driver and larger than or equal to 2.1):

```bash
$ export MESA_GL_VERSION_OVERRIDE=3.1
$ ./Defold
```

You may also need to specifically load libffi version 6 before starting Defold:

```bash
$ export LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libffi.so.6
```


#### Q: Why am I getting "com.jogamp.opengl.GLException: Graphics configuration failed" when launching Defold on Ubuntu 20.04?

A: On certain distributions there is an issue with the new Mesa drivers (Iris) when running Defold. You can try using an older version when running Defold:

```bash
$ export MESA_LOADER_DRIVER_OVERRIDE=i965
$ ./Defold
```


#### Q: Why doesn't my Defold game start when I try to run it on Linux?

A: Check the console output in the editor. If you get the following message:

```
dmengine: error while loading shared libraries: libopenal.so.1: cannot open shared object file: No such file or directory
```

Then you need to install *libopenal1*. The package name varies between distributions, and in some cases you might have to install the *openal* and *openal-dev* or *openal-devel* packages.

```bash
$ apt-get install libopenal-dev
```
