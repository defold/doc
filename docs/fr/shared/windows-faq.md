#### Q : Pourquoi les nœuds box de l'interface graphique sans texture sont-ils transparents dans l'éditeur, mais s'affichent-ils comme prévu après la compilation et l'exécution ? {#q-why-are-gui-box-nodes-without-a-texture-transparent-in-the-editor-but-show-up-as-expected-when-i-build-and-run}

R : Cette erreur peut se produire sur les [ordinateurs équipés de GPU AMD Radeon](https://github.com/defold/editor2-issues/issues/2723). Veillez à mettre à jour vos pilotes graphiques.

#### Q : Pourquoi le message `com.sun.jna.Native.open.class java.lang.Error: Access is denied` s'affiche-t-il à l'ouverture d'un atlas ou d'une vue de scène ? {#q-why-am-i-getting-comsunjnanativeopenclass-javalangerror-access-is-denied-when-opening-an-atlas-or-a-scene-view}

R : Essayez d'exécuter Defold en tant qu'administrateur. Faites un clic droit sur l'exécutable Defold et sélectionnez « Run as Administrator ».

#### Q : Pourquoi mon jeu ne s'affiche-t-il pas correctement sous Windows avec un GPU intégré Intel UHD (alors que mon build HTML5 fonctionne) ? {#q-why-is-my-game-not-rendering-properly-on-windows-using-an-intel-uhd-integrated-gpu-but-my-html5-build-works}

R : Veillez à mettre à jour votre pilote vers une version supérieure ou égale à 27.20.100.8280. Vérifiez-le à l'aide de l'[Intel Driver Support Assistant](https://www.intel.com/content/www/us/en/search.html?ws=text#t=Downloads&layout=table&cf:Downloads=%5B%7B%22actualLabel%22%3A%22Graphics%22%2C%22displayLabel%22%3A%22Graphics%22%7D%2C%7B%22actualLabel%22%3A%22Intel%C2%AE%20UHD%20Graphics%20Family%22%2C%22displayLabel%22%3A%22Intel%C2%AE%20UHD%20Graphics%20Family%22%7D%2C%7B%22actualLabel%22%3A%22Intel%C2%AE%20UHD%20Graphics%20630%22%2C%22displayLabel%22%3A%22Intel%C2%AE%20UHD%20Graphics%20630%22%7D%5D). Vous trouverez des informations supplémentaires dans [ce message du forum](https://forum.defold.com/t/sprite-game-object-is-not-rendering/69198/35?u=britzl).

#### Q : L'éditeur Defold plante et le journal affiche `AWTError: Assistive Technology not found` {#q-the-defold-editor-is-crashing-and-the-log-shows-awterror-assistive-technology-not-found}

Si l'éditeur plante et que le journal mentionne `Caused by: java.awt.AWTError: Assistive Technology not found: com.sun.java.accessibility.AccessBridge`, procédez comme suit :

* Accédez à `C:\Users\<username>`
* Ouvrez le fichier `.accessibility.properties` dans un éditeur de texte standard (Notepad convient)
* Recherchez les lignes suivantes dans la configuration :

```
assistive_technologies=com.sun.java.accessibility.AccessBridge
screen_magnifier_present=true
```

* Ajoutez un dièse (`#``) au début de ces lignes
* Enregistrez les modifications du fichier et redémarrez Defold
