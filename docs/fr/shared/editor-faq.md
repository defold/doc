#### Q : Quelle est la configuration système requise pour l'éditeur ? {#q-what-are-the-system-requirements-for-the-editor}
R : L'éditeur utilisera jusqu'à 75 % de la mémoire disponible du système. Sur un ordinateur doté de 4 Go de RAM, cela devrait suffire pour les petits projets Defold. Pour les projets de taille moyenne ou les grands projets, il est recommandé de disposer de 6 Go de RAM ou plus.


#### Q : Les versions bêta de Defold se mettent-elles à jour automatiquement ? {#q-are-defold-beta-versions-auto-updating}
R : Oui. L'éditeur Defold en version bêta recherche une mise à jour au démarrage, tout comme la version stable de Defold.


#### Q : Pourquoi l'erreur `java.awt.AWTError: Assistive Technology not found` s'affiche-t-elle au lancement de l'éditeur ? {#q-why-am-i-getting-an-error-saying-javaawtawterror-assistive-technology-not-found-when-launching-the-editor}
R : Cette erreur est liée à des problèmes avec les technologies d'assistance de Java, comme le [lecteur d'écran NVDA](https://www.nvaccess.org/download/). Vous avez probablement un fichier `.accessibility.properties` dans votre dossier personnel. Supprimez ce fichier et essayez de relancer l'éditeur. (Remarque : si vous utilisez une technologie d'assistance et que ce fichier doit être présent, contactez-nous à l'adresse info@defold.se pour discuter d'autres solutions).

Ce problème est abordé [ici sur le forum Defold](https://forum.defold.com/t/editor-endless-loading-windows-10-1-2-169-solved/65481/3).


#### Q : Pourquoi l'erreur `sun.security.validator.ValidatorException: PKIX path building failed` s'affiche-t-elle au lancement de l'éditeur ? {#q-why-am-i-getting-an-error-saying-sunsecurityvalidatorvalidatorexception-pkix-path-building-failed-when-launching-the-editor}
R : Cette exception se produit lorsque l'éditeur tente d'établir une connexion https, mais que la chaîne de certificats fournie par le serveur ne peut pas être vérifiée.

Consultez [ce lien](https://github.com/defold/defold/blob/master/editor/README_TROUBLESHOOTING_PKIX.md) pour obtenir des détails sur cette erreur.


#### Q : Pourquoi l'erreur `java.lang.OutOfMemoryError: Java heap space` s'affiche-t-elle lors de certaines opérations ? {#q-why-am-i-am-getting-a-javalangoutofmemoryerror-java-heap-space-when-performing-certain-operations}
R : L'éditeur Defold est développé en Java et, dans certains cas, la configuration mémoire par défaut de Java peut ne pas suffire. Si cela se produit, vous pouvez configurer manuellement l'éditeur pour lui allouer davantage de mémoire en modifiant son fichier de configuration. Ce fichier, nommé `config`, se trouve dans le dossier `Defold.app/Contents/Resources/` sur macOS. Sous Windows, il se trouve à côté de l'exécutable `Defold.exe` et, sous Linux, à côté de l'exécutable `Defold`. Ouvrez le fichier `config` et ajoutez `-Xmx6gb` à la ligne qui commence par `vmargs`. L'ajout de `-Xmx6gb` définit la taille maximale du tas à 6 gigaoctets (la valeur par défaut est généralement de 4 Go). Le résultat devrait ressembler à ceci :

```
vmargs = -Xmx6gb,-Dfile.encoding=UTF-8,-Djna.nosys=true,-Ddefold.launcherpath=${bootstrap.launcherpath},-Ddefold.resourcespath=${bootstrap.resourcespath},-Ddefold.version=${build.version},-Ddefold.editor.sha1=${build.editor_sha1},-Ddefold.engine.sha1=${build.engine_sha1},-Ddefold.buildtime=${build.time},-Ddefold.channel=${build.channel},-Ddefold.archive.domain=${build.archive_domain},-Djava.net.preferIPv4Stack=true,-Dsun.net.client.defaultConnectTimeout=30000,-Dsun.net.client.defaultReadTimeout=30000,-Djogl.texture.notexrect=true,-Dglass.accessible.force=false,--illegal-access=warn,--add-opens=java.base/java.lang=ALL-UNNAMED,--add-opens=java.desktop/sun.awt=ALL-UNNAMED,--add-opens=java.desktop/sun.java2d.opengl=ALL-UNNAMED,--add-opens=java.xml/com.sun.org.apache.xerces.internal.jaxp=ALL-UNNAMED
```
