Q: Why is the Defold editor super small when run on a 4k or HiDPI monitor when using GNOME?

A: Change the scaling factor before running Defold. [source](https://unix.stackexchange.com/a/552411)

```bash
$ gsettings set org.gnome.desktop.interface scaling-factor 2
```


Q: Why does mouse clicks on Elementary OS go through the editor onto whatever is below?

A: Start the editor like this:

```bash
$ GTK_CSD=0 ./Defold
```


Q: Why does the Defold editor crash when I try to create a new project, or open an existing one?

A: On certain distributions (like Ubuntu 18) there is an issue with the version of jogamp/jogl Defold uses vs. the version of Mesa on the system.

See the following reports for more information:

  - https://github.com/defold/editor2-issues/issues/1905
  - https://github.com/defold/editor2-issues/issues/1886

 If this is your problem try the following workaround:

```bash
$ export MESA_GL_VERSION_OVERRIDE=3.1
$ ./Defold
```


Q: Why doesn't my Defold game start when I try to run it on Linux?

A: Check the console output in the editor. If you get the following message:

```
dmengine: error while loading shared libraries: libopenal.so.1: cannot open shared object file: No such file or directory
```

Then you need to install *libopenal1*. The package name varies between distributions, and in some cases you might have to install the *openal* and *openal-dev* or *openal-devel* packages.

```bash
$ apt-get install libopenal-dev
```
