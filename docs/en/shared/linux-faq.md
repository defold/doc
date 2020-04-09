Mouse clicks on Elementary OS go through the editor onto whatever is below.

: Start the editor like this:

```
$ GTK_CSD=0 ./Defold
```

When I try to create a new project, or open an existing one, the editor crashes.

: On certain distributions (like Ubuntu 18) there is an issue with the version of jogamp/jogl Defold uses vs. the version of Mesa on the system.

  See the following reports for more information:

  - https://github.com/defold/editor2-issues/issues/1905
  - https://github.com/defold/editor2-issues/issues/1886

  If this is your problem try the following workaround:

  ```
  $ export MESA_GL_VERSION_OVERRIDE=3.1
  $ ./Defold
  ```

I can't create a new branch for my project on Linux.

: Make sure that you have *libssl 0.9.8* installed on your machine. Some distributions come with a later version, but Defold needs version *0.9.8*.

When I try to run my game on Linux, the engine doesn't start.

: Check the console output in the editor. If you get the following message:

  ```
  dmengine: error while loading shared libraries: libopenal.so.1: cannot open shared object file: No such file or directory
  ```

  then you need to install *libopenal1*. The package name varies between distributions, and in some cases you might have to install the *openal* and *openal-dev* or *openal-devel* packages.
