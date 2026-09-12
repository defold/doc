#### Q: Welche Systemanforderungen hat der Editor? {#q-what-are-the-system-requirements-for-the-editor}
A: Der Editor verwendet bis zu 75 % des verfügbaren Arbeitsspeichers des Systems. Auf einem Computer mit 4 GB RAM sollte dies für kleinere Defold-Projekte ausreichen. Für mittelgroße oder große Projekte werden mindestens 6 GB RAM empfohlen.


#### Q: Werden Defold-Betaversionen automatisch aktualisiert? {#q-are-defold-beta-versions-auto-updating}
A: Ja. Der Defold-Editor in der Betaversion sucht beim Start nach Updates, genau wie die stabile Version von Defold.


#### Q: Warum erhalte ich beim Starten des Editors die Fehlermeldung `java.awt.AWTError: Assistive Technology not found`? {#q-why-am-i-getting-an-error-saying-javaawtawterror-assistive-technology-not-found-when-launching-the-editor}
A: Dieser Fehler hängt mit Problemen mit assistiven Technologien in Java zusammen, etwa mit dem [Screenreader NVDA](https://www.nvaccess.org/download/). Wahrscheinlich befindet sich in deinem Benutzerordner eine Datei namens `.accessibility.properties`. Entferne die Datei und versuche erneut, den Editor zu starten. (Hinweis: Wenn du assistive Technologien verwendest und diese Datei benötigst, wende dich bitte unter info@defold.se an uns, um alternative Lösungen zu besprechen).

Eine Diskussion dazu findest du [hier im Defold-Forum](https://forum.defold.com/t/editor-endless-loading-windows-10-1-2-169-solved/65481/3).


#### Q: Warum erhalte ich beim Starten des Editors die Fehlermeldung `sun.security.validator.ValidatorException: PKIX path building failed`? {#q-why-am-i-getting-an-error-saying-sunsecurityvalidatorvalidatorexception-pkix-path-building-failed-when-launching-the-editor}
A: Diese Ausnahme tritt auf, wenn der Editor versucht, eine HTTPS-Verbindung herzustellen, die vom Server bereitgestellte Zertifikatskette aber nicht überprüft werden kann.

Weitere Informationen zu diesem Fehler findest du unter [diesem Link](https://github.com/defold/defold/blob/master/editor/README_TROUBLESHOOTING_PKIX.md).


#### Q: Warum erhalte ich bei bestimmten Vorgängen die Fehlermeldung `java.lang.OutOfMemoryError: Java heap space`? {#q-why-am-i-am-getting-a-javalangoutofmemoryerror-java-heap-space-when-performing-certain-operations}
A: Der Defold-Editor wurde mit Java entwickelt. In manchen Fällen reicht die standardmäßige Speicherkonfiguration von Java möglicherweise nicht aus. In diesem Fall kannst du den Editor manuell so konfigurieren, dass er mehr Speicher reserviert, indem du seine Konfigurationsdatei bearbeitest. Die Konfigurationsdatei heißt `config` und befindet sich unter macOS im Ordner `Defold.app/Contents/Resources/`. Unter Windows befindet sie sich neben der ausführbaren Datei `Defold.exe` und unter Linux neben der ausführbaren Datei `Defold`. Öffne die Datei `config` und füge `-Xmx6gb` zur Zeile hinzu, die mit `vmargs` beginnt. Mit `-Xmx6gb` setzt du die maximale Heap-Größe auf 6 Gigabyte (der Standardwert ist normalerweise 4Gb). Das sollte ungefähr so aussehen:

```
vmargs = -Xmx6gb,-Dfile.encoding=UTF-8,-Djna.nosys=true,-Ddefold.launcherpath=${bootstrap.launcherpath},-Ddefold.resourcespath=${bootstrap.resourcespath},-Ddefold.version=${build.version},-Ddefold.editor.sha1=${build.editor_sha1},-Ddefold.engine.sha1=${build.engine_sha1},-Ddefold.buildtime=${build.time},-Ddefold.channel=${build.channel},-Ddefold.archive.domain=${build.archive_domain},-Djava.net.preferIPv4Stack=true,-Dsun.net.client.defaultConnectTimeout=30000,-Dsun.net.client.defaultReadTimeout=30000,-Djogl.texture.notexrect=true,-Dglass.accessible.force=false,--illegal-access=warn,--add-opens=java.base/java.lang=ALL-UNNAMED,--add-opens=java.desktop/sun.awt=ALL-UNNAMED,--add-opens=java.desktop/sun.java2d.opengl=ALL-UNNAMED,--add-opens=java.xml/com.sun.org.apache.xerces.internal.jaxp=ALL-UNNAMED
```
