#### Q: What are the system requirements for the editor?
A: The editor will use up to 75% of the available memory of the system. On a computer with 4 GB of RAM this should be enough for smaller Defold projects. For mid-sized or large projects it is recommended to use 6 GB or more of RAM.


#### Q: Are Defold beta versions auto-updating?
A: Yes. The Defold beta editor checks for an update at startup, just like the Defold stable version does.


#### Q: Why am I getting an error saying "java.awt.AWTError: Assistive Technology not found" when launching the editor?
A: This error is related to problems with Java assistive technology such as the [NVDA screen reader](https://www.nvaccess.org/download/). You probably have an `.accessibility.properties` file in your home folder. Remove the file and try launching the editor again. (Note: If you do use any assistive technology and require that file to be present then please reach out to us at info@defold.se to discuss alternative solutions).

Discussed [here on the Defold forum](https://forum.defold.com/t/editor-endless-loading-windows-10-1-2-169-solved/65481/3).


#### Q: Why doesn't the editor start or open my project?
A: Check if there are spaces in the path leading up to the Defold application. For instance, if you put the folder *Defold-macosx* containing the macOS version of the editor in your *Applications* folder, then you should be ok.  If you rename the folder *Defold macosx* the editor might not start anymore. On Windows, putting Defold under *C:\\Program Files\\* can trigger this problem. This is due to a known bug in the underlying Eclipse framework.


#### Q: Why am I getting an error saying "sun.security.validator.ValidatorException: PKIX path building failed" when launching the editor?
A: This exception occurs when the editor tries to make an https connection but the certificate chain provided by the server cannot be verified.

See [this link](https://github.com/defold/defold/blob/master/editor/README_TROUBLESHOOTING_PKIX.md) for details on this error.


#### Q: Why am I am getting a "java.lang.OutOfMemoryError: Java heap space" when performing certain operations?
A: The Defold editor is built using Java and in some cases the default memory configuration of Java might not be sufficient. If this happens you can manually configure the editor to allocate more memory by editing the editor configuration file. The configuration file, named `config`, is located in the `Defold.app/Contents/Resources/` folder on macOS. On Windows it is located next to `Defold.exe` executable and on Linux next to the `Defold` executable. Open the `config` file and add `-Xmx6gb` to the line starting with `vmargs`. Adding `-Xmx6gb` will set the max heap size to 6 gigabytes (the default is usually 4Gb). It should look something like this:

```
vmargs = -Xmx6gb,-Dfile.encoding=UTF-8,-Djna.nosys=true,-Ddefold.launcherpath=${bootstrap.launcherpath},-Ddefold.resourcespath=${bootstrap.resourcespath},-Ddefold.version=${build.version},-Ddefold.editor.sha1=${build.editor_sha1},-Ddefold.engine.sha1=${build.engine_sha1},-Ddefold.buildtime=${build.time},-Ddefold.channel=${build.channel},-Ddefold.archive.domain=${build.archive_domain},-Djava.net.preferIPv4Stack=true,-Dsun.net.client.defaultConnectTimeout=30000,-Dsun.net.client.defaultReadTimeout=30000,-Djogl.texture.notexrect=true,-Dglass.accessible.force=false,--illegal-access=warn,--add-opens=java.base/java.lang=ALL-UNNAMED,--add-opens=java.desktop/sun.awt=ALL-UNNAMED,--add-opens=java.desktop/sun.java2d.opengl=ALL-UNNAMED,--add-opens=java.xml/com.sun.org.apache.xerces.internal.jaxp=ALL-UNNAMED
```
