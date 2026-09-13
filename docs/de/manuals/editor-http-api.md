---
title: Den Defold-Editor mit HTTP automatisieren
brief: Dieses Handbuch erklärt, wie externe Werkzeuge die lokale HTTP-API eines im Defold-Editor geöffneten Projekts ermitteln und nutzen können.
---

# Den Defold-Editor automatisieren {#automating-the-defold-editor}

Der Defold-Editor startet einen speziellen Server für automatisierte Aktionen. Die HTTP-API steuert das geöffnete Projekt. Nutze sie für Editorbefehle, Builds, Projektressourcen, Vorschauen, Editoreinstellungen, Konsolenausgaben, die Suche in der Dokumentation oder Integrationen mit Editor-Skripten. Um stattdessen das laufende Spiel zu untersuchen oder zu steuern, verwende den [Engine-Dienst oder eine Automatisierungs-API für die Laufzeit](/manuals/engine-service).

::: important
Die HTTP-API des Editors ist experimentell und kann sich zwischen Defold-Versionen ändern. Das vom laufenden Editor erzeugte Dokument `/openapi.json` ist die maßgebliche Quelle für die verfügbaren Operationen und Schemas.
:::

## Den Editor aus einem externen Werkzeug starten {#starting-the-editor-from-an-external-tool}

Ein externes Werkzeug benötigt die ausführbare Datei des Editors und den absoluten Pfad zur Datei `game.project` des Projekts.

Installierte Defold-Versionen lassen sich über `installations.json` ermitteln, wie im [Editorhandbuch](/manuals/editor/#editor-installation-metadata) beschrieben. Das Feld `launcherPath` enthält die ausführbare Datei, die gestartet werden soll. Übergib den Pfad zu `game.project` als erstes positionsabhängiges Argument, um dieses Projekt direkt zu öffnen.

Das optionale Argument `--port` oder `-p` legt den Port des Editorservers fest. Wenn du es weglässt, wählt Defold einen verfügbaren Port. Das ist in der Regel vorzuziehen, wenn mehrere Projekte geöffnet sein können.

```sh
# Linux
/path/to/Defold/Defold --port 8181 /absolute/path/to/project/game.project
```

```sh
# macOS
/path/to/Defold.app/Contents/MacOS/Defold --port 8181 /absolute/path/to/project/game.project
```

```powershell
# Windows
C:\path\to\Defold\Defold.exe --port 8181 C:\absolute\path\to\project\game.project
```

Der Editor ist eine grafische Desktopanwendung. Starte ihn in einer interaktiven Benutzersitzung mit Zugriff auf die Anzeige. Verwende [Bob](/manuals/bob), wenn keine grafische Sitzung verfügbar ist, etwa in einer CI-Umgebung ohne grafische Oberfläche, oder um eigenständige Bundles zu erstellen. Ein geöffneter Editor unterstützt über `/command/compile` auch die Automatisierung einer reinen Kompilierung.

Warte nach dem Start des Editors, bis das Projekt geöffnet wurde und `.internal/editor.port` vorhanden ist. Frage anschließend `/openapi.json` wiederholt ab, bis ein gültiges Dokument zurückgegeben wird. Gehe nicht davon aus, dass das Projekt bereits bereit ist, sobald der Prozess erstellt wurde.

## Den Editorserver ermitteln {#locating-the-editor-server}

Der Editor startet einen lokalen HTTP-Server, solange ein Projekt geöffnet ist. Wähle <kbd>Help ▸ Open Editor Server</kbd>, um dessen Startseite im Standardbrowser zu öffnen:

![Die Startseite des lokalen Editorservers](images/automation/editor_server.png)

Der gewählte Port wird im Projekt in diese Datei geschrieben:

```text
.internal/editor.port
```

Die Beispiele und Befehle in diesem Handbuch beziehen sich ab hier auf diese Shell-Variablen:

```sh
PORT="$(cat .internal/editor.port)"
BASE_URL="http://127.0.0.1:$PORT"
```

Die Portdatei gehört zur aktuellen Editorsitzung. Lies sie nach einem Neustart des Editors erneut ein.

::: important
Der Editorserver ist eine vertrauenswürdige lokale Steuerschnittstelle. Mache ihn nicht über eine öffentliche Adresse, eine Portweiterleitung oder einen nicht vertrauenswürdigen Tunnel zugänglich.
:::

## Operationen über OpenAPI ermitteln {#discovering-operations-through-openapi}

Die einzigen Defold-spezifischen Informationen, die ein externes Werkzeug zu Beginn benötigen sollte, sind der Editorport und das OpenAPI-Dokument:

```sh
curl -sS "http://127.0.0.1:$(cat .internal/editor.port)/openapi.json"
```

Das zurückgegebene OpenAPI-3.0.3-Dokument beschreibt die Operationen, die von der laufenden Editorversion unterstützt werden, einschließlich Pfaden, Methoden, Parametern, Befehlsnamen, Anfrageformaten, Antworten, Statuscodes und Authentifizierungsanforderungen.

Liste die dokumentierten Pfade auf:

```sh
curl -sS "$BASE_URL/openapi.json" |
  jq -r '.paths | keys[]'
```

Liste die dokumentierten Pfade der Editorbefehle auf:

```sh
curl -sS "$BASE_URL/openapi.json" |
  jq -r '.paths | keys[] | select(startswith("/command/"))'
```

In Defold 1.13.2 und neuer hat jeder Befehl einen eigenen Pfad im OpenAPI-Dokument. Frühere Versionen beschreiben Befehle über einen Pfad `/command/{command}` und eine Aufzählung von Befehlsnamen.

Eine Integration, die Versionsunterschiede berücksichtigt, sollte jede benötigte Operation überprüfen und Anfragen anhand des zurückgegebenen Schemas konfigurieren. Wir raten davon ab, eine vermeintlich vollständige Kopie der Endpunkt- oder Befehlsnamen zu pflegen, da diese veralten kann.

Im Projekt definierte Routen erscheinen ebenfalls in `/openapi.json`, wenn ihre Editor-Skripte eine OpenAPI-Operationsbeschreibung bereitstellen.

## Editorbefehle ausführen {#executing-editor-commands}

Rufe Editorbefehle auf, indem du eine `POST`-Anfrage an den dokumentierten Pfad des Befehls sendest, zum Beispiel:

```text
POST /command/compile
POST /command/run
```

So kompilierst du das Projekt, ohne es auszuführen:

```sh
curl -sS \
  -X POST \
  "$BASE_URL/command/compile" |
  jq
```

So kompilierst du das Projekt und führst es aus:

```sh
curl -sS \
  -X POST \
  "$BASE_URL/command/run" |
  jq
```

Diese Pipelines zeigen den Antwortinhalt an. Prüfe in Automatisierungsskripten zusätzlich den HTTP-Status und `success` nach dem Muster in [Builds für HTML5 erstellen](#building-html5).

::: sidenote
Seit Defold 1.13.2 ist `/command/build` ein veralteter und zur Ablösung vorgesehener Kompatibilitätsalias für `/command/run` und wird nicht in OpenAPI aufgeführt. Verwende `/command/run` in neuen Integrationen.
:::

Eine erfolgreiche Kompilierung gibt den HTTP-Status `200` mit einem strukturierten Ergebnis zurück:

```json
{
  "success": true,
  "issues": []
}
```

Ein fehlgeschlagener Build gibt den HTTP-Status `422` mit Problemmeldungen wie diesen zurück:

```json
{
  "success": false,
  "issues": [
    {
      "message": "Example compiler message",
      "severity": "error",
      "resource": "/main/player.script",
      "range": {
        "start": {
          "line": 12,
          "character": 4
        },
        "end": {
          "line": 12,
          "character": 17
        }
      }
    }
  ]
}
```

Die verfügbaren Felder hängen vom Fehler ab. Verwende den Ressourcenpfad und den Quelltextbereich, wenn sie vorhanden sind, behandle aber auch Probleme, die nur eine Meldung enthalten.

Zu den häufig nützlichen Befehlen gehören, sofern der laufende Editor sie aufführt:

`compile`
: Kompiliert das Projekt, ohne es auszuführen.

`run`
: Kompiliert das Projekt und führt es aus.

`clean-build`
: Leert den Build-Cache, kompiliert anschließend das Projekt und führt es aus. Verwende dies nur, wenn sich ein gewöhnlicher Build inkonsistent verhält oder Änderungen offenbar nicht berücksichtigt.

`build-html5`
: Erstellt einen Build des Projekts für HTML5 und stellt die Ausgabe über den Editorserver bereit.

`fetch-libraries`
: Lädt Projektabhängigkeiten herunter und lädt sie neu.

`hot-reload`
: Lädt geänderte Ressourcen in ein laufendes Spiel nach.

`reload-extensions`
: Lädt Editor-Skripte neu.

`debugger-start`, `debugger-stop` und die Befehle zur schrittweisen Ausführung im Debugger
: Steuern eine Debugsitzung und das laufende Projekt.

Die genauen Namen und die Verfügbarkeit hängen von der Editorversion und dem aktuellen Zustand des Editors ab; ermittle sie über `/openapi.json`.

Befehle, die mit Projektressourcen arbeiten, synchronisieren externe Dateiänderungen vor der Ausführung.

### Befehlsantworten und asynchrone Vorgänge {#command-responses-and-asynchronous-work}

Die Antworten hängen vom jeweiligen Befehl ab. In Defold 1.13.2 und neuer warten `compile`, `run`, `clean-build`, `build-html5`, `debugger-start` und `hot-reload` auf den Abschluss des Befehls und geben ein strukturiertes Ergebnis mit `success` und `issues` zurück, wie oben gezeigt. Ein erfolgreiches Ergebnis gibt HTTP `200` zurück; ein Build- oder Validierungsfehler gibt `422` zurück.

Andere Befehle können weiterhin `202` zurückgeben, zum Beispiel `debugger-break`. Untersuche die Operation im aktuellen OpenAPI-Schema und behandle den tatsächlichen HTTP-Antwortstatus:

| Status | Bedeutung |
| --- | --- |
| `200` | Der Befehl wurde abgeschlossen und hat ein Ergebnis zurückgegeben |
| `202` | Der Befehl wurde angenommen und wird asynchron fortgesetzt |
| `403` | Der Befehl ist im aktuellen Zustand des Editors nicht aktiv |
| `404` | Der Befehl ist nicht verfügbar |
| `422` | Der Build oder die Validierung ist fehlgeschlagen |
| `500` | Ein interner Editorfehler ist aufgetreten |

Eine HTTP-Antwort mit `202` ist kein Nachweis dafür, dass das angeforderte Ergebnis vorhanden ist. Warte auf die relevante Ausgabe, Ressource, Konsolenmarkierung oder bereitgestellte URL und setze eine Zeitbegrenzung durch.

### Builds für HTML5 erstellen {#building-html5}

Wenn das aktuelle OpenAPI-Dokument `/command/build-html5` aufführt, rufe den Befehl über diesen Pfad auf. Erfasse in einem Shell-Skript den HTTP-Status getrennt vom Antwortinhalt und brich bei einer fehlgeschlagenen Anfrage oder einem fehlgeschlagenen Build ab:

```sh
build_response_file="$(mktemp)" || exit 1
if ! build_http_status="$(curl -sS \
  -X POST \
  -o "$build_response_file" \
  -w '%{http_code}' \
  "$BASE_URL/command/build-html5")"; then
  cat "$build_response_file"
  rm -f "$build_response_file"
  exit 1
fi

cat "$build_response_file"
if [ "$build_http_status" != "200" ] ||
   ! jq -e '.success == true' "$build_response_file" > /dev/null; then
  rm -f "$build_response_file"
  exit 1
fi
rm -f "$build_response_file"
```

In Defold 1.13.2 und neuer wartet diese Anfrage auf den Abschluss des Builds und gibt ein strukturiertes Ergebnis zurück. Das Beispiel gibt den Antwortinhalt einschließlich etwaiger Build-Probleme aus und fährt nur bei HTTP `200` mit `success: true` fort. Nach einem erfolgreichen Build öffnet der Editor das Spiel in einem Browser und stellt es unter folgender Adresse bereit:

```text
http://127.0.0.1:<editor-port>/html5/
```

Ein abgeschlossener Build bedeutet nicht, dass das Spiel im Browser vollständig geladen wurde. Warte darauf, dass die Zeichenfläche und die Anwendung bereit sind, bevor du Eingaben sendest oder den Spielablauf prüfst. Weitere Einzelheiten findest du unter [Browsertests für HTML5](/manuals/automated-testing/#browser-tests-for-html5).

## Die API-Dokumentation durchsuchen {#searching-api-documentation}

Sofern in `/openapi.json` vorhanden, durchsucht die Operation `/ref` die API-Dokumentation, die mit der laufenden Editorversion ausgeliefert wird. Sie liefert Namen und Signaturen, die zu dieser Version passen.

Um beispielsweise nach einer Funktion zu suchen, verwende:

```sh
curl -sS \
  --get \
  --data-urlencode "q=go.animate" \
  "$BASE_URL/ref" |
  jq
```

Filtere nach Umgebung und Sprache:

```sh
curl -sS \
  --get \
  --data-urlencode "environment=runtime" \
  --data-urlencode "language=Lua" \
  --data-urlencode "q=collision message|raycast" \
  "$BASE_URL/ref" |
  jq
```

Die Suchparameter sind:

`environment`
: `editor`, `runtime` oder durch Kommas getrennte Werte.

`language`
: `Lua`, `C`, `C++` oder durch Kommas getrennte Werte.

`q`
: Ein Ausdruck ohne Unterscheidung zwischen Groß- und Kleinschreibung. Leerraum steht für UND, während `|` für ODER steht.

Es gibt außerdem zusammengefasste Dokumentationsressourcen: Der [Dokumentationsindex für große Sprachmodelle (Large Language Models, LLM)](https://defold.com/llms.txt) verlinkt auf offizielle Handbücher, API-Namespaces und Beispiele. Die [vollständige LLM-Dokumentation](https://defold.com/llms-full.txt) enthält die gesamte Dokumentation, um die Offline-Suche und lokale Indizierung zu unterstützen.

KI-Agenten sollten jedoch gezielte Suchanfragen bevorzugen, statt eine vollständige Referenz abzurufen, wenn nur eine einzelne API oder Nachricht benötigt wird. So sparen sie Tokens und erhalten einen besser vorbereiteten, übersichtlichen Kontext für die jeweilige Aufgabe.

## Konsolenausgaben lesen {#reading-console-output}

Lies die Editorkonsole als JSON:

```sh
curl -sS "$BASE_URL/console" | jq
```

Die Antwort enthält Konsolentext in `lines` und semantische Bereiche in `regions`, darunter Fehler, Auswertungsergebnisse und Ressourcenreferenzen.

Um die Konsolenausgabe fortlaufend zu verfolgen, verwende:

```sh
curl -N "$BASE_URL/console/stream"
```

Der Datenstrom enthält die vorhandenen Konsolenzeilen und bleibt anschließend für neue Ausgaben offen. Schließe ihn, nachdem du eine Abschlussmarkierung oder einen Fehler empfangen, die Beendigung des Prozesses erkannt oder eine Zeit- oder Zeilenbegrenzung erreicht hast.

Informationen zur Abgrenzung von Testergebnissen und zur Klassifizierung von Fehlern findest du unter [Automatisiertes Testen und Überprüfen](/manuals/automated-testing/#structured-test-results).

## Szenenvorschauen rendern {#rendering-scene-previews}

Der Defold-Editor kann seit Version 1.13.1 über den Befehl `/preview/{path}` eine „Bildschirmaufnahme“ einer unterstützten Szenenressource als PNG rendern:

```sh
mkdir -p build/automation

curl -sS \
  "$BASE_URL/preview/main/main.collection?width=1280&height=720" \
  --output build/automation/main-preview.png
```

Dies rendert die Hauptsammlung (main collection) aus dem geöffneten Vorlagenprojekt Basic 3D in einer standardmäßigen Ausgangsansicht:

![Eine vom Editor gerenderte Vorschau der Hauptsammlung](images/automation/main-preview.png)

Du kannst damit Vorschauen von Ressourcen rendern, die den visuellen Szeneneditor verwenden. Beispielsweise lässt sich eine Modellkomponente (model component) auf dieselbe Weise rendern, um ihr Aussehen oder etwa die korrekte Funktionsweise eines Shaders zu überprüfen:

```sh
curl -sS \
  "$BASE_URL/preview/assets/models/cube.model?width=1280&height=720" \
  --output build/automation/cube-preview.png
```

![Eine vom Editor gerenderte Vorschau des Würfelmodells](images/automation/cube-preview.png)

Der Pfad nach `/preview/` enthält keinen führenden Schrägstrich. Die optionalen Abmessungen entsprechen standardmäßig der Anzeigegröße des Projekts und müssen zwischen `1` und `4096` liegen.

| Status | Bedeutung |
| --- | --- |
| `200` | Die Vorschau wurde gerendert |
| `400` | Die Abmessungen sind ungültig |
| `404` | Die Ressource wurde nicht gefunden |
| `422` | Die Ressource ist nicht geladen oder unterstützt keine Szenenvorschauen |

Vorschauen können für die visuelle Analyse des Projekts sehr nützlich sein: zum Prüfen von Level-Layouts, GUI-Layouts, Shader- und Beleuchtungseinstellungen sowie visuellen Regressionen oder zum Erstellen von Vorschaubildern für die Dokumentation.

::: important
Eine Editorvorschau ist keine Bildschirmaufnahme des laufenden Spiels. Sie überprüft weder dynamisch erstellte Objekte noch Nachbearbeitung zur Laufzeit oder plattformspezifisches Rendering. Verwende eine [Bildschirmaufnahme zur Laufzeit](/manuals/automated-testing/#editor-previews-and-runtime-screenshots), wenn diese Elemente benötigt werden.
:::

## Lua im Editor ausführen {#executing-editor-lua}

Die authentifizierte Operation `POST /eval` führt Lua in der Erweiterungsumgebung des Editors aus. Das Bearer-Token für die jeweilige Sitzung wird hier gespeichert:

```text
.internal/editor.token
```

Lies das Token ein und führe Code aus:

```sh
TOKEN="$(cat .internal/editor.token)"

curl -sS \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: text/plain" \
  --data-binary 'print(editor.version) return editor.platform' \
  "$BASE_URL/eval"
```

Ausgaben und Rückgabewerte werden als Text zurückgegeben. Typische Antworten sind:

| Status | Bedeutung |
| --- | --- |
| `200` | Der Code wurde ausgeführt |
| `401` | Das Bearer-Token fehlt oder ist ungültig |
| `422` | Der Lua-Code konnte nicht geparst oder ausgeführt werden |
| `503` | Die Erweiterungsumgebung des Editors ist nicht bereit |

Ein Client darf nach `503` einen erneuten Versuch unternehmen, sollte jedoch die Anzahl der Versuche begrenzen. Korrigiere den Code, bevor du eine Anfrage wiederholst, die `422` zurückgegeben hat.

Ausgewerteter Code kann die [Editor-API](https://defold.com/ref/editor-lua/) und die Skriptumgebung des Editors nutzen. Er kann keine Laufzeit-APIs des Spiels wie `go.*` verwenden, um ein laufendes Spiel zu verändern. Verwende für den Spielablauf einen Laufzeittest, Debugger, Browsertest oder eine [Automatisierungs-API für die Laufzeit](/manuals/engine-service/#automation-bridge-extension).

### Ressourcen und Dateien ändern {#modifying-resources-and-files}

Viele Defold-Quellressourcen verwenden Textformate und lassen sich mit jedem Textbearbeitungswerkzeug ändern. Bevorzuge Editortransaktionen, um strukturierte Ressourcen eines Defold-Projekts zu ändern.

| Änderung | Bevorzugte Methode |
| --- | --- |
| Lua, Shader, JSON oder ein anderes bekanntes Textformat | Direkte Dateiänderung |
| Nicht gespeicherter Text in einer geöffneten Editorregisterkarte | `editor.get()` und `editor.transact()` |
| Sammlung, Spielobjekt (game object), GUI, Atlas oder eine andere strukturierte Ressource | Editortransaktion |
| Wiederholt erzeugte Inhalte | Eigenständiger Generator |
| Wiederholbarer Projektvorgang | Editorbefehl oder benutzerdefinierter HTTP-Endpunkt |
| Transformation ausschließlich für CI | Eigenständiges Skript, das vor Bob ausgeführt wird |

Untersuche eine Ressource, bevor du sie änderst:

```sh
curl -sS \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: text/plain" \
  --data-binary '
    local path = "/game.project"
    pprint(editor.properties(path))
    return editor.get(path, "path")
  ' \
  "$BASE_URL/eval"
```

Prüfe `editor.can_get()`, `editor.can_set()` und die anderen Funktionen `editor.can_*()`, bevor du eine Transaktion durchführst.

Verwende `editor.execute()` in Editor-Lua, um einen Formatierer, Validator oder Generator auszuführen:

```lua
local output = editor.execute(
  "python3",
  "scripts/generate_levels.py",
  {
    out = "capture"
  }
)

print(output)
```

Wenn der Befehl keine Projektressourcen ändert, setze `reload_resources = false`, um unnötiges Neuladen zu vermeiden.

::: important
Ändere keine Dateien in `.internal/` und keine generierten Inhalte in `build/`.
:::

## Editoreinstellungen {#preferences}

Editoreinstellungen lassen sich über den in OpenAPI dokumentierten Pfad lesen und schreiben, derzeit `/prefs/{path}`.

Du kannst beispielsweise die konfigurierte Schriftgröße für Code auslesen:

```sh
curl -sS "$BASE_URL/prefs/code/font/size" | jq
```

Oder sie beispielsweise auf 16 setzen:

```sh
curl -sS \
  -X POST \
  -H "Content-Type: application/json" \
  --data '16' \
  "$BASE_URL/prefs/code/font/size"
```

Der Editor validiert den Wert anhand seines Einstellungsschemas. Ein ungültiger Pfad oder Wert gibt HTTP `400` zurück.

Editoreinstellungen sind dauerhafte benutzerspezifische oder projektbezogene benutzerspezifische Einstellungen und keine in `game.project` gespeicherte Projektkonfiguration. Wenn eine Automatisierung eine Editoreinstellung vorübergehend ändern muss, speichere den vorherigen Wert und stelle ihn anschließend wieder her.

## Im Projekt definierte Routen {#project-defined-routes}

Editor-Skripte können mit [`get_http_server_routes()`](/manuals/editor-scripts/#http-server) zusätzliche Routen definieren. Eine optionale OpenAPI-Operationstabelle macht eine Route über dasselbe Dokument `/openapi.json` wie die integrierten Operationen zugänglich.

Im Projekt definierte Routen können Inhaltserzeugung, Validierung, Berichte, Lokalisierungsprüfungen, Ressourcenanalysen, projektspezifische Tests oder eine kleinere Schnittstelle für eine IDE oder ein externes Steuerprogramm bereitstellen.

Eine gute Route sollte genau eine klar benannte Operation ausführen, ihre Eingabe validieren, ein strukturiertes Ergebnis zurückgeben, nach Möglichkeit idempotent sein und aufwendige Arbeiten begrenzen.

Im Projekt definierte Routen werden nicht automatisch durch das Token für `/eval` geschützt. Ergänze projektspezifische Authentifizierung und Sicherheitsprüfungen, wenn eine Route sensible Operationen ausführt.

## Lebenszyklus-Hooks {#lifecycle-hooks}

Hooks sind Funktionen, die vor und nach Builds, vor und nach der Bundle-Erstellung sowie beim Start oder bei der Beendigung eines Spielprozesses ausgeführt werden können. Ein Projekt kann eine Datei `hooks.editor_script` in seinem Stammverzeichnis enthalten. Nur die Hook-Datei im Stammverzeichnis empfängt diese Ereignisse, sodass das Projekt einen zentralen Ort hat, um ihre Reihenfolge festzulegen.

```lua
local M = {}

local function validate_project()
  print(editor.execute(
    "python3",
    "scripts/validate_project.py",
    {
      out = "capture",
      reload_resources = false
    }
  ))
end

function M.on_build_started(opts)
  validate_project()
end

function M.on_build_finished(opts)
  print("Build successful:", opts.success)
end

return M
```

Ein von `on_build_started()` ausgelöster Fehler bricht den Build im Editor ab. Lebenszyklus-Hooks werden nur im Editor ausgeführt; lege gemeinsam genutzte Validierungs- und Generierungslogik in eigenständigen Skripten ab, die auch aus CI heraus aufgerufen werden können.

## Sicherheit und Kompatibilität {#security-and-compatibility}

Behandle den gesamten Editorserver als vertrauenswürdige lokale Schnittstelle:

* Mache den Zugriff auf den Port nicht öffentlich zugänglich.
* Schütze `.internal/editor.token`; es autorisiert `/eval` für die aktuelle Sitzung.
* Gewähre externen Stellen keinen uneingeschränkten Zugriff auf `/eval`.
* Bewahre das Token in der lokalen Integrationsschicht auf, nicht in Prompts, Berichten oder Protokollen.
* Denke daran, dass im Projekt definierte Routen die Authentifizierung von `/eval` nicht übernehmen.
* Verwende eine aktuelle `/openapi.json`.
* Begrenze die Wartezeiten für asynchrone automatisierte Befehle und für den Start des Editors.

## Engine-Server

Der Editorserver gehört zum Editorprozess. Ein laufendes Spiel hat einen anderen Port und andere Aufgaben, die im [Handbuch zum Engine-Dienst und zur Laufzeit-HTTP-API](/manuals/engine-service) beschrieben werden.
