#### Q: ¿Cuáles son los requisitos del sistema para el editor?
A: El editor usará hasta el 75% de la memoria disponible del sistema. En una computadora con 4 GB de RAM, esto debería ser suficiente para proyectos Defold pequeños. Para proyectos medianos o grandes, se recomienda usar 6 GB de RAM o más.


#### Q: ¿Las versiones beta de Defold se actualizan automáticamente?
A: Sí. El editor beta de Defold busca actualizaciones al iniciar, igual que la versión estable de Defold.


#### Q: ¿Por qué aparece el error `java.awt.AWTError: Assistive Technology not found` al iniciar el editor?
A: Este error está relacionado con problemas de tecnología de asistencia de Java, como el [lector de pantalla NVDA](https://www.nvaccess.org/download/). Probablemente tienes un archivo `.accessibility.properties` en tu carpeta de inicio. Elimina el archivo e intenta iniciar el editor de nuevo. (Nota: Si usas alguna tecnología de asistencia y necesitas que ese archivo esté presente, escríbenos a info@defold.se para hablar sobre soluciones alternativas).

Se discutió [aquí en el foro de Defold](https://forum.defold.com/t/editor-endless-loading-windows-10-1-2-169-solved/65481/3).


#### Q: ¿Por qué aparece el error `sun.security.validator.ValidatorException: PKIX path building failed` al iniciar el editor?
A: Esta excepción ocurre cuando el editor intenta establecer una conexión https, pero no se puede verificar la cadena de certificados proporcionada por el servidor.

Consulta [este enlace](https://github.com/defold/defold/blob/master/editor/README_TROUBLESHOOTING_PKIX.md) para ver más detalles sobre este error.


#### Q: ¿Por qué aparece un `java.lang.OutOfMemoryError: Java heap space` al realizar ciertas operaciones?
A: El editor Defold está construido con Java y, en algunos casos, la configuración de memoria predeterminada de Java puede no ser suficiente. Si esto ocurre, puedes configurar manualmente el editor para que asigne más memoria editando el archivo de configuración del editor. El archivo de configuración, llamado `config`, se encuentra en la carpeta `Defold.app/Contents/Resources/` en macOS. En Windows se encuentra junto al ejecutable `Defold.exe` y en Linux junto al ejecutable `Defold`. Abre el archivo `config` y agrega `-Xmx6gb` a la línea que empieza con `vmargs`. Agregar `-Xmx6gb` establecerá el tamaño máximo del heap en 6 gigabytes (el valor predeterminado suele ser 4Gb). Debería verse similar a esto:

```
vmargs = -Xmx6gb,-Dfile.encoding=UTF-8,-Djna.nosys=true,-Ddefold.launcherpath=${bootstrap.launcherpath},-Ddefold.resourcespath=${bootstrap.resourcespath},-Ddefold.version=${build.version},-Ddefold.editor.sha1=${build.editor_sha1},-Ddefold.engine.sha1=${build.engine_sha1},-Ddefold.buildtime=${build.time},-Ddefold.channel=${build.channel},-Ddefold.archive.domain=${build.archive_domain},-Djava.net.preferIPv4Stack=true,-Dsun.net.client.defaultConnectTimeout=30000,-Dsun.net.client.defaultReadTimeout=30000,-Djogl.texture.notexrect=true,-Dglass.accessible.force=false,--illegal-access=warn,--add-opens=java.base/java.lang=ALL-UNNAMED,--add-opens=java.desktop/sun.awt=ALL-UNNAMED,--add-opens=java.desktop/sun.java2d.opengl=ALL-UNNAMED,--add-opens=java.xml/com.sun.org.apache.xerces.internal.jaxp=ALL-UNNAMED
```
