---
title: Live-Update-Inhalte in Defold
brief: Live Update bietet einen Mechanismus, mit dem die Laufzeitumgebung Ressourcen abrufen und im Anwendungs-Bundle speichern kann, die beim Build absichtlich aus dem Bundle ausgelassen wurden. Dieses Handbuch erklärt, wie das funktioniert.
---

# Live Update

Wenn du ein Bundle für ein Spiel erstellst, packt Defold alle Spielressourcen in das entstehende plattformspezifische Paket. In den meisten Fällen ist dies erwünscht, da die laufende Engine sofort auf alle Ressourcen zugreifen und sie schnell vom Datenträger laden kann. Es gibt jedoch Fälle, in denen du das Laden von Ressourcen auf einen späteren Zeitpunkt verschieben möchtest. Zum Beispiel:

- Dein Spiel besteht aus einer Reihe von Episoden, und du möchtest nur die erste mitliefern, damit die Spieler sie ausprobieren können, bevor sie entscheiden, ob sie mit dem Rest des Spiels fortfahren möchten.
- Dein Spiel ist für HTML5 vorgesehen. Im Browser bedeutet das Laden einer Anwendung vom Datenträger, dass das gesamte Anwendungspaket vor dem Start heruntergeladen werden muss. Auf einer solchen Plattform möchtest du möglicherweise ein minimales Startpaket bereitstellen und die Anwendung schnell starten, bevor du die restlichen Spielressourcen herunterlädst.
- Dein Spiel enthält sehr große Ressourcen (Bilder, Videos usw.), deren Download du aufschieben möchtest, bis sie im Spiel angezeigt werden sollen. So bleibt die Installationsgröße gering.

Live Update erweitert das Konzept des Sammlungs-Proxys (collection proxy) um einen Mechanismus, mit dem die Laufzeitumgebung Ressourcen abrufen und im Anwendungs-Bundle speichern kann, die beim Build absichtlich aus dem Bundle ausgelassen wurden.

Damit kannst du deine Inhalte auf mehrere Archive aufteilen:

* _Basisarchiv_
* Gemeinsame Leveldateien
* Levelpaket 1
* Levelpaket 2
* ...

## Inhalte für Live Update vorbereiten {#preparing-content-for-live-update}

Angenommen, wir erstellen ein Spiel mit großen, hochauflösenden Bildressourcen. Das Spiel hält diese Bilder in Sammlungen (collections) mit jeweils einem Spielobjekt (game object) und einem Sprite mit dem Bild:

![Mona-Lisa-Sammlung](images/live-update/mona-lisa.png)

Damit die Engine eine solche Sammlung dynamisch lädt, können wir einfach eine Komponente (component) vom Typ Sammlungs-Proxy hinzufügen und auf *`monalisa.collection`* verweisen lassen. Das Spiel kann nun entscheiden, wann es die Inhalte der Sammlung vom Datenträger in den Arbeitsspeicher lädt, indem es eine `load`-Nachricht an den Sammlungs-Proxy sendet. Wir möchten jedoch noch weiter gehen und das Laden der in der Sammlung enthaltenen Ressourcen selbst steuern.

Dazu aktivieren wir einfach das Kontrollkästchen *Exclude* in den Eigenschaften des Sammlungs-Proxys. Damit weisen wir Defold an, beim Erstellen eines Anwendungs-Bundles sämtliche Inhalte von *`monalisa.collection`* auszulassen.

::: important
Ressourcen, auf die das Basispaket des Spiels verweist, werden nicht ausgeschlossen.
:::

![Ausgeschlossener Sammlungs-Proxy](images/live-update/proxy-excluded.png)

## Einstellungen für Live Update {#live-update-settings}

Wenn Defold ein Anwendungs-Bundle erstellt, muss es die ausgeschlossenen Ressourcen an einem anderen Ort speichern. Die Projekteinstellungen für Live Update bestimmen den Speicherort dieser Ressourcen. Du findest die Einstellungen unter <kbd>Project ▸ Live update Settings...</kbd>. Dabei wird eine Einstellungsdatei erstellt, falls noch keine vorhanden ist. Wähle in *game.project* aus, welche Einstellungsdatei für Live Update bei der Bundle-Erstellung verwendet werden soll. So kannst du unterschiedliche Einstellungen für verschiedene Umgebungen verwenden, zum Beispiel für den Produktivbetrieb, die Qualitätssicherung (QA), die Entwicklung usw.

![Einstellungen für Live Update](images/live-update/05-liveupdate-settings-zip.png)

Derzeit gibt es drei Möglichkeiten, wie Defold die Ressourcen speichern kann. Wähle die Methode im Dropdown-Menü *Mode* des Einstellungsfensters:

`Zip`
: Diese Option weist Defold an, eine Zip-Archivdatei mit allen ausgeschlossenen Ressourcen zu erstellen. Das Archiv wird am Speicherort abgelegt, der in der Einstellung *Export path* angegeben ist, und kann zur Laufzeit mit einer `zip:`-URI und `liveupdate.add_mount()` eingebunden werden.

`Folder`  
: Diese Option weist Defold an, einen Ordner mit allen ausgeschlossenen Ressourcen zu erstellen. Das ist nützlich, wenn du Dateien vor dem Hochladen oder Verpacken nachbearbeiten musst. Ein Ordner mit einzelnen kompilierten Dateien, die unter ihren erwarteten Ressourcenpfaden abgelegt sind, kann zur Laufzeit mit einer `file:`-URI eingebunden werden.

`Amazon`
: Diese Option weist Defold an, ausgeschlossene Ressourcen automatisch in einen S3-Bucket von Amazon Web Service (AWS) hochzuladen. Gib den Namen deines AWS-*Credential profile* ein, wähle den passenden *Bucket* aus und gib einen Namen für *Prefix* an.  Mehr zur Einrichtung eines AWS-Kontos erfährst du in dieser [AWS-Anleitung](/manuals/live-update-aws)

## Bundles mit Live Update erstellen {#bundling-with-live-update}

::: important
Das Erstellen eines Builds und dessen Ausführung im Editor (<kbd>Project ▸ Build</kbd>) unterstützt Live Update nicht. Um Live Update zu testen, musst du ein Bundle des Projekts erstellen.
:::

Ein Bundle mit Live Update zu erstellen ist einfach. Wähle <kbd>Project ▸ Bundle ▸ ...</kbd> und anschließend die Plattform aus, für die du ein Anwendungs-Bundle erstellen möchtest. Dadurch öffnet sich der Dialog zur Bundle-Erstellung:

![Anwendungs-Bundle mit Live Update erstellen](images/live-update/bundle-app.png)

Bei der Bundle-Erstellung werden alle ausgeschlossenen Ressourcen aus dem Anwendungs-Bundle ausgelassen. Wenn du das Kontrollkästchen *Publish Live update content* aktivierst, weist du Defold an, die ausgeschlossenen Ressourcen entweder zu Amazon hochzuladen oder ein Zip-Archiv zu erstellen, je nachdem, wie du deine Einstellungen für Live Update festgelegt hast (siehe oben). Die veröffentlichten Live-Update-Inhalte enthalten weiterhin `liveupdate.game.dmanifest`, das die vollständige Ressourcenliste für die Bereitstellung über das Netzwerk enthält.

Beim Veröffentlichen von Live-Update-Inhalten entfernt Defold automatisch die Einträge, die ausschließlich zu Live Update gehören, aus dem im Bundle enthaltenen `game.dmanifest`, während das veröffentlichte `liveupdate.game.dmanifest` die vollständige Ressourcenliste behält. Dadurch werden die Bundle-Größe und der Speicherverbrauch zur Laufzeit verringert. Die frühere Einstellung `liveupdate.exclude_entries_from_main_manifest` wurde entfernt; ein eventuell noch vorhandener Eintrag im Projekt wird ignoriert.

Beim Arbeiten mit Archiven gibt `collectionproxy.get_resources()` so lange `{}` zurück, bis das betreffende Archiv eingebunden wurde. Nach dem Einbinden gibt die Funktion die Ressourcen-Hashes für diesen Proxy zurück.

Klicke auf *Package* und wähle einen Speicherort für das Anwendungs-Bundle aus. Nun kannst du die Anwendung starten und prüfen, ob alles wie erwartet funktioniert.

## Die .zip-Archive {#the-zip-archives}

Eine .zip-Datei für Live Update enthält Dateien, die aus dem Basispaket des Spiels ausgeschlossen wurden.

Unsere aktuelle Pipeline unterstützt zwar nur das Erstellen einer einzigen .zip-Datei, du kannst diese Zip-Datei jedoch in kleinere .zip-Dateien aufteilen. Dadurch sind kleinere Downloads für ein Spiel möglich: Levelpakete, saisonale Inhalte usw. Jede .zip-Datei enthält außerdem eine Manifestdatei, die die Metadaten jeder im .zip-Archiv enthaltenen Ressource beschreibt.

## .zip-Archive aufteilen {#splitting-zip-archives}

Oft ist es sinnvoll, die ausgeschlossenen Inhalte auf mehrere kleinere Archive aufzuteilen, um die Ressourcennutzung genauer steuern zu können. Ein Beispiel ist die Aufteilung eines Spiels mit mehreren Levels in mehrere Levelpakete. Ein weiteres Beispiel sind Dekorationen der Benutzeroberfläche für verschiedene Feiertage, die du in getrennten Archiven ablegst. So kannst du nur das zum aktuellen Kalenderdatum passende Thema laden und einbinden.

Der Ressourcengraph wird in `build/default/game.graph.json` gespeichert und bei jeder Bundle-Erstellung des Projekts automatisch erzeugt. Die erzeugte Datei enthält eine Liste aller Ressourcen des Projekts und die Abhängigkeiten jeder Ressource. Beispieleintrag:

```json
{
  "path" : "/game/player.goc",
  "hexDigest" : "caa342ec99794de45b63735b203e83ba60d7e5a1",
  "children" : [ "/game/ship.spritec", "/game/player.scriptc" ]
}
```

Jeder Eintrag hat einen `path`, der den eindeutigen Pfad der Ressource innerhalb des Projekts angibt. Der `hexDigest` ist der kryptografische Fingerabdruck der Ressource und wird als Dateiname im .zip-Archiv für Live Update verwendet. Das Feld `children` schließlich ist eine Liste weiterer Abhängigkeiten, von denen diese Ressource abhängt. Im obigen Beispiel hat `/game/player.goc` eine Abhängigkeit von einem Sprite und einer Skriptkomponente.

Du kannst die Datei `game.graph.json` auswerten und diese Informationen nutzen, um Gruppen von Einträgen im Ressourcengraphen zu identifizieren und ihre zugehörigen Ressourcen zusammen mit der ursprünglichen Manifestdatei in separaten Archiven zu speichern (die Manifestdatei wird zur Laufzeit so gekürzt, dass sie nur die Dateien des jeweiligen Archivs enthält).

## Live Update auf Android {#live-update-on-android}

Du kannst Play Asset Delivery verwenden, um Live-Update-Inhalte herunterzuladen und einzubinden. Mehr dazu erfährst du [im offiziellen Handbuch](https://defold.com/extension-pad/).

## Inhaltsprüfung {#content-verification}

Eine der wichtigsten Funktionen des Live-Update-Systems ist, dass du nun viele Inhaltsarchive verwenden kannst, möglicherweise aus vielen verschiedenen Defold-Versionen.

Standardmäßig führt `liveupdate.add_mount()` beim Hinzufügen einer Einbindung (mount) eine Prüfung der Engine-Version durch.
Das bedeutet, dass sowohl das Basisarchiv des Spiels als auch die Live-Update-Archive zur selben Zeit mit derselben Engine-Version über die Bundle-Option erstellt werden müssen. Dadurch werden alle zuvor vom Client heruntergeladenen Archive ungültig, sodass die Inhalte erneut heruntergeladen werden müssen.

Dieses Verhalten lässt sich über ein Options-Flag deaktivieren.
Wenn es deaktiviert ist, liegt die Verantwortung für die Inhaltsprüfung vollständig bei dir als Entwickler. Du musst sicherstellen, dass jedes Live-Update-Archiv mit der laufenden Engine funktioniert.

Wir empfehlen, Metadaten für jede Einbindung zu speichern, damit die Anwendung entscheiden kann, ob das Paket eingebunden bleiben soll. Führe die Prüfung nach dem Hinzufügen der Einbindung durch, auch wenn die Anwendung beim Start ihre benötigten Einbindungen erneut hinzufügt.
Eine Möglichkeit dazu ist, nach der Bundle-Erstellung des Spiels eine zusätzliche Datei in das Zip-Archiv einzufügen. Füge beispielsweise eine `metadata.json` mit allen Informationen ein, die das Spiel benötigt, und rufe sie nach dem Einbinden mit `sys.load_resource("/metadata.json")` ab. _Verwende für die benutzerdefinierten Daten jeder Einbindung einen eindeutigen Ressourcenpfad, sonst gibt die Ressourcensuche die Datei aus der Einbindung mit der höchsten Priorität zurück._

Wenn du das nicht tust, kann es passieren, dass die Inhalte überhaupt nicht mit der Engine kompatibel sind und diese sich deshalb beenden muss.

## Einbindungen {#mounts}

Das Live-Update-System kann mehrere Inhaltsarchive gleichzeitig verwenden.
Jedes Archiv wird mit einem Namen und einer Priorität in das Ressourcensystem der Engine „eingebunden“.

Wenn zwei Archive dieselbe Datei `sprite.texturec` enthalten, lädt die Engine die Datei aus der Einbindung mit der höchsten Priorität.

Die Engine hält keine Referenz auf eine Ressource in einer Einbindung. Sobald eine Ressource in den Arbeitsspeicher geladen wurde, kann die Einbindung des Archivs aufgehoben werden. Die Ressource bleibt im Arbeitsspeicher, bis sie entladen wird.

Einbindungen sind nur für die aktuelle Engine-Sitzung aktiv. Nach einem Neustart muss die Anwendung für jedes benötigte Paket erneut `liveupdate.add_mount()` aufrufen. Speichere den Speicherort des Pakets, den Namen der Einbindung und ihre Priorität in persistenten Daten, die von der Anwendung verwaltet werden, wenn diese Angaben zwischen Sitzungen erhalten bleiben müssen.

::: sidenote
Ein Zip-Archiv oder ein Ordner wird beim Einbinden weder kopiert noch verschoben. Die eingebundenen Inhalte müssen so lange am angegebenen Speicherort bleiben, wie die Einbindung verwendet wird.
:::

## Skripting mit Live Update {#scripting-with-live-update}

Um Live-Update-Inhalte tatsächlich zu verwenden, musst du die Daten herunterladen und in dein Spiel einbinden.
Mehr zum [Skripting mit Live Update erfährst du hier](/manuals/live-update-scripting).

## Hinweise für die Entwicklung {#development-caveats}

Debugging
: Wenn du eine als Bundle erstellte Version deines Spiels ausführst, hast du keinen direkten Zugriff auf eine Konsole. Das erschwert die Fehlersuche. Du kannst die Anwendung jedoch über die Befehlszeile oder durch einen direkten Doppelklick auf die ausführbare Datei im Bundle starten:

  ![Eine Anwendung aus einem Bundle ausführen](images/live-update/run-bundle.png)

  Das Spiel startet nun mit einem Shell-Fenster, das die Ausgabe aller `print()`-Anweisungen anzeigt:

  ![Konsolenausgabe](images/live-update/run-bundle-console.png)

Erneuten Download von Ressourcen erzwingen
: Als Entwickler kannst du die Inhalte in eine beliebige Datei oder einen beliebigen Ordner herunterladen. Häufig befinden sie sich jedoch unter dem Anwendungspfad. Der Speicherort des Ordners für Anwendungsdaten hängt vom Betriebssystem ab. Du kannst ihn mit `print(sys.get_save_file("", ""))` ermitteln. Um einen Download zu erzwingen, entferne das heruntergeladene Paket und den zugehörigen Eintrag aus allen von der Anwendung verwalteten Zustandsdaten. Es gibt keine von der Engine verwaltete Liste von Einbindungen, die gelöscht werden müsste; Einbindungen bleiben über Neustarts hinweg nicht erhalten.

  ![Lokaler Speicher](images/live-update/local-storage.png)
