#### D: Perché i nodi rettangolari (box) della GUI senza texture sono trasparenti nell'editor, ma appaiono come previsto quando creo la build ed eseguo il gioco? {#q-why-are-gui-box-nodes-without-a-texture-transparent-in-the-editor-but-show-up-as-expected-when-i-build-and-run}

R: Questo errore può verificarsi sui [computer con GPU AMD Radeon](https://github.com/defold/editor2-issues/issues/2723). Assicurati di aggiornare i driver della scheda grafica.

#### D: Perché ricevo l'errore `com.sun.jna.Native.open.class java.lang.Error: Access is denied` quando apro un atlas o la vista di una scena? {#q-why-am-i-getting-comsunjnanativeopenclass-javalangerror-access-is-denied-when-opening-an-atlas-or-a-scene-view}

R: Prova a eseguire Defold come amministratore. Fai clic con il pulsante destro del mouse sull'eseguibile di Defold e seleziona "Run as Administrator".

#### D: Perché il rendering del mio gioco non funziona correttamente su Windows con una GPU integrata Intel UHD (mentre la build HTML5 funziona)? {#q-why-is-my-game-not-rendering-properly-on-windows-using-an-intel-uhd-integrated-gpu-but-my-html5-build-works}

R: Assicurati di aggiornare il driver alla versione 27.20.100.8280 o successiva. Verifica con [Intel Driver Support Assistant](https://www.intel.com/content/www/us/en/search.html?ws=text#t=Downloads&layout=table&cf:Downloads=%5B%7B%22actualLabel%22%3A%22Graphics%22%2C%22displayLabel%22%3A%22Graphics%22%7D%2C%7B%22actualLabel%22%3A%22Intel%C2%AE%20UHD%20Graphics%20Family%22%2C%22displayLabel%22%3A%22Intel%C2%AE%20UHD%20Graphics%20Family%22%7D%2C%7B%22actualLabel%22%3A%22Intel%C2%AE%20UHD%20Graphics%20630%22%2C%22displayLabel%22%3A%22Intel%C2%AE%20UHD%20Graphics%20630%22%7D%5D). Puoi trovare ulteriori informazioni in [questo post sul forum](https://forum.defold.com/t/sprite-game-object-is-not-rendering/69198/35?u=britzl).

#### D: L'editor Defold va in crash e nel log compare `AWTError: Assistive Technology not found` {#q-the-defold-editor-is-crashing-and-the-log-shows-awterror-assistive-technology-not-found}

R: Se l'editor va in crash e nel log compare `Caused by: java.awt.AWTError: Assistive Technology not found: com.sun.java.accessibility.AccessBridge`, segui questi passaggi:

* Vai a `C:\Users\<username>`
* Apri il file `.accessibility.properties` con un normale editor di testo (Notepad va bene)
* Individua le seguenti righe nella configurazione:

```
assistive_technologies=com.sun.java.accessibility.AccessBridge
screen_magnifier_present=true
```

* Aggiungi un cancelletto (`#``) all'inizio di queste righe
* Salva le modifiche al file e riavvia Defold
