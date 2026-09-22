#### D: Quali sono i requisiti di sistema dell'editor? {#q-what-are-the-system-requirements-for-the-editor}
R: L'editor utilizza fino al 75% della memoria disponibile nel sistema. Su un computer con 4 GB di RAM, questa quantità dovrebbe essere sufficiente per progetti Defold di piccole dimensioni. Per progetti di medie o grandi dimensioni, si consiglia di avere almeno 6 GB di RAM.


#### D: Le versioni beta di Defold si aggiornano automaticamente? {#q-are-defold-beta-versions-auto-updating}
R: Sì. All'avvio, l'editor Defold beta verifica la disponibilità di aggiornamenti, proprio come la versione stabile di Defold.


#### D: Perché ricevo l'errore `java.awt.AWTError: Assistive Technology not found` quando avvio l'editor? {#q-why-am-i-getting-an-error-saying-javaawtawterror-assistive-technology-not-found-when-launching-the-editor}
R: Questo errore è legato a problemi con le tecnologie assistive di Java, come il [lettore di schermo NVDA](https://www.nvaccess.org/download/). Probabilmente nella tua cartella home è presente un file `.accessibility.properties`. Rimuovi il file e prova ad avviare nuovamente l'editor. (Nota: se utilizzi una tecnologia assistiva che richiede la presenza di questo file, contattaci all'indirizzo info@defold.se per discutere soluzioni alternative).

Se ne parla [in questa discussione sul forum Defold](https://forum.defold.com/t/editor-endless-loading-windows-10-1-2-169-solved/65481/3).


#### D: Perché ricevo l'errore `sun.security.validator.ValidatorException: PKIX path building failed` quando avvio l'editor? {#q-why-am-i-getting-an-error-saying-sunsecurityvalidatorvalidatorexception-pkix-path-building-failed-when-launching-the-editor}
R: Questa eccezione si verifica quando l'editor tenta di stabilire una connessione HTTPS, ma non è possibile verificare la catena di certificati fornita dal server.

Consulta [questo link](https://github.com/defold/defold/blob/master/editor/README_TROUBLESHOOTING_PKIX.md) per maggiori dettagli su questo errore.


#### D: Perché ricevo l'errore `java.lang.OutOfMemoryError: Java heap space` quando eseguo determinate operazioni? {#q-why-am-i-am-getting-a-javalangoutofmemoryerror-java-heap-space-when-performing-certain-operations}
R: L'editor Defold è realizzato in Java e, in alcuni casi, la configurazione predefinita della memoria di Java potrebbe non essere sufficiente. In questo caso puoi configurare manualmente l'editor affinché allochi più memoria, modificando il suo file di configurazione. Il file di configurazione, denominato `config`, si trova nella cartella `Defold.app/Contents/Resources/` su macOS. Su Windows si trova accanto all'eseguibile `Defold.exe` e su Linux accanto all'eseguibile `Defold`. Apri il file `config` e aggiungi `-Xmx6gb` alla riga che inizia con `vmargs`. Aggiungendo `-Xmx6gb`, imposti la dimensione massima dell'heap a 6 gigabyte (il valore predefinito è solitamente 4 GB). La riga dovrebbe avere un aspetto simile a questo:

```
vmargs = -Xmx6gb,-Dfile.encoding=UTF-8,-Djna.nosys=true,-Ddefold.launcherpath=${bootstrap.launcherpath},-Ddefold.resourcespath=${bootstrap.resourcespath},-Ddefold.version=${build.version},-Ddefold.editor.sha1=${build.editor_sha1},-Ddefold.engine.sha1=${build.engine_sha1},-Ddefold.buildtime=${build.time},-Ddefold.channel=${build.channel},-Ddefold.archive.domain=${build.archive_domain},-Djava.net.preferIPv4Stack=true,-Dsun.net.client.defaultConnectTimeout=30000,-Dsun.net.client.defaultReadTimeout=30000,-Djogl.texture.notexrect=true,-Dglass.accessible.force=false,--illegal-access=warn,--add-opens=java.base/java.lang=ALL-UNNAMED,--add-opens=java.desktop/sun.awt=ALL-UNNAMED,--add-opens=java.desktop/sun.java2d.opengl=ALL-UNNAMED,--add-opens=java.xml/com.sun.org.apache.xerces.internal.jaxp=ALL-UNNAMED
```
