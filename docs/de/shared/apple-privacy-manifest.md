
## Datenschutzmanifest von Apple {#apple-privacy-manifest}

Das Datenschutzmanifest ist eine Eigenschaftsliste, die die von deiner App oder einem SDK eines Drittanbieters erfassten Datenarten sowie die von deiner App oder dem SDK verwendeten APIs auflistet, deren Nutzung eine Begründung erfordert. Für jede erfasste Datenart und jede verwendete Kategorie solcher APIs muss deine App oder das SDK eines Drittanbieters die Gründe in der im Bundle enthaltenen Datenschutzmanifestdatei festhalten.

Defold stellt über das Feld Privacy Manifest in der Datei *game.project* ein standardmäßiges Datenschutzmanifest bereit. Beim Erstellen eines Anwendungsbundles wird das Datenschutzmanifest mit allen Datenschutzmanifesten in den Projektabhängigkeiten zusammengeführt und in das Anwendungsbundle aufgenommen.

Weitere Informationen zu Datenschutzmanifesten findest du in der [offiziellen Dokumentation von Apple](https://developer.apple.com/documentation/bundleresources/privacy_manifest_files?language=objc).
