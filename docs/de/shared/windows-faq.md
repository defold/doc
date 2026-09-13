#### Q: Warum sind GUI-Box-Knoten (GUI box nodes) ohne Textur im Editor transparent, werden aber wie erwartet angezeigt, wenn ich einen Build erstelle und ausführe? {#q-why-are-gui-box-nodes-without-a-texture-transparent-in-the-editor-but-show-up-as-expected-when-i-build-and-run}

A: Dieser Fehler kann auf [Computern mit AMD Radeon-GPUs](https://github.com/defold/editor2-issues/issues/2723) auftreten. Stelle sicher, dass du deine Grafiktreiber aktualisierst.

#### Q: Warum erhalte ich beim Öffnen eines Atlas oder einer Szenenansicht die Fehlermeldung `com.sun.jna.Native.open.class java.lang.Error: Access is denied`? {#q-why-am-i-getting-comsunjnanativeopenclass-javalangerror-access-is-denied-when-opening-an-atlas-or-a-scene-view}

A: Versuche, Defold als Administrator auszuführen. Klicke mit der rechten Maustaste auf die ausführbare Defold-Datei und wähle "Run as Administrator".

#### Q: Warum wird mein Spiel unter Windows mit einer integrierten Intel UHD-GPU nicht richtig gerendert (obwohl mein HTML5-Build funktioniert)? {#q-why-is-my-game-not-rendering-properly-on-windows-using-an-intel-uhd-integrated-gpu-but-my-html5-build-works}

A: Stelle sicher, dass du deinen Treiber auf Version 27.20.100.8280 oder höher aktualisierst. Prüfe dies mit dem [Intel Driver Support Assistant](https://www.intel.com/content/www/us/en/search.html?ws=text#t=Downloads&layout=table&cf:Downloads=%5B%7B%22actualLabel%22%3A%22Graphics%22%2C%22displayLabel%22%3A%22Graphics%22%7D%2C%7B%22actualLabel%22%3A%22Intel%C2%AE%20UHD%20Graphics%20Family%22%2C%22displayLabel%22%3A%22Intel%C2%AE%20UHD%20Graphics%20Family%22%7D%2C%7B%22actualLabel%22%3A%22Intel%C2%AE%20UHD%20Graphics%20630%22%2C%22displayLabel%22%3A%22Intel%C2%AE%20UHD%20Graphics%20630%22%7D%5D). Weitere Informationen findest du in [diesem Forumsbeitrag](https://forum.defold.com/t/sprite-game-object-is-not-rendering/69198/35?u=britzl).

#### Q: Der Defold-Editor stürzt ab und im Protokoll steht `AWTError: Assistive Technology not found` {#q-the-defold-editor-is-crashing-and-the-log-shows-awterror-assistive-technology-not-found}

Wenn der Editor abstürzt und im Protokoll `Caused by: java.awt.AWTError: Assistive Technology not found: com.sun.java.accessibility.AccessBridge` steht, führe die folgenden Schritte aus:

* Navigiere zu `C:\Users\<username>`
* Öffne die Datei `.accessibility.properties` mit einem gewöhnlichen Texteditor (Notepad ist geeignet)
* Suche in der Konfiguration nach den folgenden Zeilen:

```
assistive_technologies=com.sun.java.accessibility.AccessBridge
screen_magnifier_present=true
```

* Füge am Anfang dieser Zeilen ein Rautezeichen (`#``) hinzu
* Speichere deine Änderungen an der Datei und starte Defold neu
