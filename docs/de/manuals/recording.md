---
title: Videoaufnahmen in Defold
brief: Dieses Handbuch erklärt, wie du das Spielfenster über Lua oder den HTTP-Dienst der Engine als MP4 aufnimmst.
---

# Videoaufnahmen {#video-recording}

Defold kann das Spielfenster über das [Lua-Modul `recorder`](/ref/recorder/) oder den [HTTP-Dienst der Engine](/manuals/engine-service/#recording-endpoints) als H.264-Video in einer MP4-Datei aufnehmen. Beide Schnittstellen teilen sich einen Recorder, sodass immer nur eine Aufnahme starten, laufen oder finalisiert werden kann.

## Verfügbarkeit {#availability}

Die Aufnahme ist in Desktop-**Debug**-Engines enthalten. Sie fehlt in Release-, Headless-, Mobil- und Web-Builds. Auch das Aktivieren von **Exclude Record** in einem [Anwendungsmanifest](/manuals/app-manifest/#exclude-record) entfernt das Lua-Modul und die HTTP-Routen.

| Plattform | Videoanforderungen | Anwendungsaudio |
| --- | --- | --- |
| macOS | macOS 15 oder neuer, mit ScreenCaptureKit | Unterstützt |
| Windows | Windows 10 Version 1903 oder neuer, mit Windows Graphics Capture und Media Foundation | Ab Windows-Build 20348 unterstützt |
| Linux | OpenGL, OpenGL ES oder Vulkan, mit Framebuffer-Aufnahme | Nicht unterstützt |

Video- und Audiounterstützung werden getrennt geprüft. HTTP-Clients können `/recording/capabilities` abfragen; Lua-Aufrufer erhalten einen Fehler, wenn die angeforderte Aufnahme nicht unterstützt wird. Betriebssystemberechtigungen und Fehler des Aufnahmegeräts können auch nach Annahme einer Startanfrage einen asynchronen Fehler verursachen.

Der Recorder nimmt den Inhalt des Spielfensters in seiner nativen Größe in physischen Pixeln auf. Er kann eine Zeile oder Spalte abschneiden, um gerade Videoabmessungen zu erhalten. Eine Änderung der Fenstergröße oder Pixeldichte stoppt und finalisiert die Aufnahme. Die Aufnahmerate beträgt 1–60 Bilder pro Sekunde, standardmäßig 30.

## Mit Lua aufnehmen {#recording-from-lua}

Verwende [`recorder.start()`](/ref/recorder/#recorder.start) mit einem beschreibbaren Ausgabepfad und einem Callback. Das übergeordnete Verzeichnis muss vorhanden sein; [`sys.get_save_file()`](/ref/sys/#sys.get_save_file) liefert einen geeigneten Anwendungsspeicherpfad. Eine vorhandene Ausgabedatei kann überschrieben werden. Lua-Aufnahmen gehören dem Aufrufer und bleiben nach dem Beenden der Engine auf dem Datenträger.

Pfade verwenden wie Lua-Datei-E/A unter Windows die Windows-ANSI-Codepage und sonst UTF-8. `result.path` des Callbacks erhält den an `recorder.start()` übergebenen Pfad.

Dieses `.script`-Beispiel nimmt nach Beginn der Aufnahme fünf Sekunden lang auf:

```lua
local function on_recording_event(self, event, result)
    if event == recorder.EVENT_STARTED then
        self.recording = true
        timer.delay(5, false, function(self)
            if self.recording then
                local ok, err = recorder.stop()
                if not ok then
                    print("Could not stop recording:", err)
                end
            end
        end)
    elseif event == recorder.EVENT_STOPPED then
        self.recording = false
        print("MP4 ready:", result.path)
    elseif event == recorder.EVENT_ERROR then
        self.recording = false
        print("Recording failed:", result.error)
    end
end

function init(self)
    self.recording = false
    if not recorder then
        print("Recording is not included in this engine build")
        return
    end

    local ok, err = recorder.start({
        path = sys.get_save_file("recording_example", "capture.mp4"),
        fps = 30,
        audio = false,
    }, on_recording_event)
    if not ok then
        print("Could not start recording:", err)
    end
end
```

`recorder.start()` und [`recorder.stop()`](/ref/recorder/#recorder.stop) geben bei Annahme `true` und bei Ablehnung `nil, error` zurück. Die Annahme bedeutet nicht, dass Aufnahme oder Dateifinalisierung abgeschlossen sind. Ungültige Optionen lösen Lua-Fehler aus.

Callbacks werden während der Engine-Aktualisierungen ausgeführt:

| Ereignis | Bedeutung |
| --- | --- |
| `recorder.EVENT_STARTED` | Die Aufnahme ist aktiv und kann jetzt gestoppt werden. |
| `recorder.EVENT_STOPPED` | Die MP4-Datei wurde finalisiert und kann gelesen werden. Dieses Ereignis tritt auch nach einem automatischen Stopp bei Größenänderung auf. |
| `recorder.EVENT_ERROR` | Die Aufnahme ist fehlgeschlagen; prüfe `result.error`. Ein Startfehler kann dieses Ereignis ohne `EVENT_STARTED` auslösen. |

Das Ergebnis enthält außerdem `path`, `width`, `height`, `fps` und `audio`. Lies oder lade die Ausgabe erst nach `EVENT_STOPPED` hoch. Halte das startende Skript aktiv, um den Callback zu erhalten: Wird es gelöscht, werden Callbacks verworfen, ohne die Aufnahme zu stoppen. Beim Herunterfahren der Engine wird die Aufnahme ohne Lua-Callbacks finalisiert.

Audio ist **in Lua standardmäßig deaktiviert**. Setze `audio = true`, um auf einer unterstützten Plattform Anwendungsaudio anzufordern. Nicht unterstütztes Audio anzufordern liefert einen Fehler.

### Den Recorder mit HTTP-Clients gemeinsam nutzen {#sharing-the-recorder-with-http-clients}

`recorder.stop()` richtet sich an die aktuelle gemeinsame Aufnahme, auch wenn sie über HTTP gestartet wurde. Die Funktion gibt einen Fehler zurück, solange eine Operation aussteht oder keine Aufnahme aktiv ist. Stoppt ein HTTP-Client eine Lua-Aufnahme, erhält der ursprüngliche Lua-Callback trotzdem sein Abschlussereignis. Ein Start über HTTP erstellt keinen Lua-Callback; beobachte seinen Abschluss über den HTTP-Status.

Der HTTP-Status kann eine Lua-Aufnahme beschreiben, ihr Feld `file` ist jedoch `null`: Der Dienst bereitet Downloads nur für über HTTP gestartete Aufnahmen vor. Lies eine Lua-Aufnahme nach `EVENT_STOPPED` aus `result.path`.

## Über HTTP aufnehmen {#recording-through-http}

Die Aufnahmerouten verwenden den im Spielprotokoll ausgegebenen Engine-Dienst-Port. Ermittle sie über `/openapi.json`, wie im [Handbuch zum Engine-Dienst](/manuals/engine-service/#discovering-operations-through-openapi) beschrieben. Eine Headless- oder Release-Engine stellt sie nicht bereit.

Die folgenden Befehle verwenden eine POSIX-Shell, `curl` und `jq`; zur Download-Prüfung wird außerdem Python 3 benötigt. Führe sie in derselben Shell aus und ersetze `<port>` durch den Port der laufenden Engine. Frage zunächst die Fähigkeiten ab und speichere die Identität des Dienstes:

```sh
set -eu
ENGINE_URL="http://127.0.0.1:<port>"
CAPABILITIES=$(curl -fsS "$ENGINE_URL/recording/capabilities")
printf '%s\n' "$CAPABILITIES" | jq
INSTANCE_ID=$(printf '%s\n' "$CAPABILITIES" | jq -er 'select(.supported) | .instance_id')
```

Fahre nur fort, wenn `supported` den Wert `true` hat; prüfe andernfalls `unsupported_reason` und `minimum_platform_version`. Das Feld `audio` meldet die Audiounterstützung. Im Unterschied zu Lua **aktiviert die HTTP-Aufnahme Audio standardmäßig, wenn das Backend es unterstützt**. Das folgende Beispiel deaktiviert Audio ausdrücklich.

### Die Aufnahme starten und prüfen {#start-and-inspect-the-recording}

Starte mit einem optionalen JSON-Objekt, das `fps` und/oder `audio` enthält. Der Dienst wählt die Ausgabedatei; Pfad, Breite, Höhe oder Maßstab werden nicht akzeptiert.

```sh
START=$(curl -fsS -X POST \
    -H 'Content-Type: application/json' \
    -H "X-Recording-Instance: $INSTANCE_ID" \
    --data '{"fps":30,"audio":false}' \
    "$ENGINE_URL/recording/start")
OPERATION_ID=$(printf '%s\n' "$START" | jq -er '.operation_id')
printf '%s\n' "$START" | jq
```

HTTP 202 bedeutet, dass die Anfrage angenommen wurde. Führe den folgenden Statusbefehl erneut aus, bis `pending` den Wert `false` und `active` den Wert `true` hat. Die Prüfung verwirft Antworten für andere Operationen und meldet Fehler bei Aufnahme oder Dateivorbereitung. Hat ein automatischer Stopp die Aufnahme bereits finalisiert, fahre vor dem Herunterladen mit der [Finalisierung](#stop-and-wait-for-finalization) fort.

```sh
STATUS=$(curl -fsS \
    -H "X-Recording-Instance: $INSTANCE_ID" \
    "$ENGINE_URL/recording/status")
printf '%s\n' "$STATUS" | jq -e --argjson id "$OPERATION_ID" '
    if .operation_id != $id then error("Recording operation changed")
    elif .state == "failed" then error(.failure)
    elif .file.state == "failed" then error("Recording file preparation failed")
    else . end'
```

Lasse das Spiel für die gewünschte Aufnahmedauer laufen und fordere dann einen Stopp an. Wurde die Fenstergröße geändert und die Aufnahme bereits abgeschlossen, überspringe die Stoppanfrage und fahre unten mit der Finalisierung fort.

### Stoppen und auf die Finalisierung warten {#stop-and-wait-for-finalization}

Stoppe die Operation, deren ID du aus der Startantwort gespeichert hast:

```sh
STOP_BODY=$(jq -n --argjson id "$OPERATION_ID" '{operation_id: $id}')
STOP=$(curl -fsS -X POST \
    -H 'Content-Type: application/json' \
    -H "X-Recording-Instance: $INSTANCE_ID" \
    --data "$STOP_BODY" \
    "$ENGINE_URL/recording/stop")
printf '%s\n' "$STOP" | jq
```

HTTP 202 bestätigt nur die Annahme der Stoppanfrage. Wiederhole den Statusbefehl, bis `pending` den Wert `false`, `finalized` den Wert `true` und `file.state` den Wert `complete` hat. Der Dienst bereitet Dateigröße und SHA-256 nach Abschluss der nativen Aufnahme vor; `state: "complete"` und `finalized: true` allein bedeuten daher nicht, dass der Download bereitsteht. Beende das Warten, wenn `state` oder `file.state` zu `failed` wird; lade keine Datei im Zustand `pending` oder `failed` herunter.

Ein automatisierter Client sollte mit Intervall und Zeitbegrenzung abfragen und bei jeder Antwort die gespeicherte Operations-ID prüfen. Lasse die Engine weiter aktualisieren, während du auf Aufnahme und Finalisierung wartest.

### Die Datei herunterladen und freigeben {#download-and-release-the-file}

Verwende die relative URL der abgeschlossenen Datei aus der Statusantwort. Die folgende Prüfung stellt zusätzlich sicher, dass die Antwort noch zu deiner Operation gehört:

```sh
FILE_URL=$(printf '%s\n' "$STATUS" | jq -er --argjson id "$OPERATION_ID" \
    'select(.operation_id == $id and .pending == false and .finalized == true and .file.state == "complete") | .file.url')
curl -fsS -H "X-Recording-Instance: $INSTANCE_ID" \
    "$ENGINE_URL$FILE_URL" -o capture.mp4
printf '%s\n' "$STATUS" > capture.json
```

Bewahre den abgeschlossenen Statusbeleg in `capture.json` zusammen mit der MP4-Datei auf. `/recording/status` beschreibt die aktuelle Operation; eine spätere Aufnahme ersetzt daher die Statusantwort, auch wenn frühere HTTP-Dateien weiterhin verfügbar sind.

Prüfe Byte-Größe und SHA-256 der heruntergeladenen Datei, bevor du sie verwendest oder die Kopie des Dienstes löschst:

```sh
python3 - <<'PY'
import hashlib
import json
from pathlib import Path

receipt = json.loads(Path("capture.json").read_text(encoding="utf-8"))
capture = Path("capture.mp4")
if capture.stat().st_size != receipt["file"]["size"]:
    raise SystemExit("Recording download size mismatch")

digest = hashlib.sha256()
with capture.open("rb") as stream:
    for chunk in iter(lambda: stream.read(65536), b""):
        digest.update(chunk)
if digest.hexdigest() != receipt["file"]["sha256"]:
    raise SystemExit("Recording download SHA-256 mismatch")
print("Verified capture.mp4")
PY
```

Ein GET ohne Header `Range` lädt die gesamte MP4-Datei herunter. Der Dienst unterstützt auch geschlossene Byte-Bereiche wie `Range: bytes=0-1023`, falls ein Client Teil-Downloads benötigt. Prüfe die zusammengesetzte Datei anhand desselben Belegs.

Nach dem Herunterladen und Prüfen kannst du die vom Dienst aufbewahrte Kopie freigeben:

```sh
curl -fsS -X DELETE -H "X-Recording-Instance: $INSTANCE_ID" \
    "$ENGINE_URL$FILE_URL"
```

HTTP-Aufnahmedateien bleiben verfügbar, bis sie ausdrücklich gelöscht werden oder die Engine herunterfährt oder neu startet. Lade sie vor dem Schließen der Engine herunter. Der Dienst bewahrt höchstens 128 Dateien auf; lösche bereits gespeicherte abgeschlossene Dateien, um Platz für weitere Aufnahmen zu schaffen.

### Operationsidentitäten zusammenhalten {#keeping-operation-identities-together}

Jedes POST und DELETE benötigt `X-Recording-Instance`. Die Beispiele senden den Header auch bei Status- und Download-Anfragen, um Antworten einer ersetzten Engine zurückzuweisen. Halte `instance_id`, `operation_id` und die Dateiinformationen zusammen: Die Dienstidentität ändert sich bei einem Neustart, und ein neuer Prozess kann Operationsnummern wiederverwenden.

Eine fehlende Identität führt zu HTTP 400. Eine veraltete Identität, veraltete Stoppoperation oder gelöschte Datei führt zu HTTP 410. Hole keine neue Identität, um damit eine alte Operation erneut zu versuchen. Ermittle stattdessen den neuen Dienst und starte eine neue Aufnahme.

### HTTP-Fehler behandeln {#handling-http-failures}

Abgelehnte Anfragen geben JSON mit `error.code` und `error.message` zurück. Führe zur Fehlerbehebung die einzelne `curl`-Anfrage mit `-i` und ohne `-f` aus, um HTTP-Status und Fehlerkörper zu sehen.

| HTTP-Status | Zu prüfen |
| --- | --- |
| 409 | Eine andere Aufnahme ist aktiv oder ausstehend, die aktuelle Aufnahme ist noch nicht zum Stoppen bereit, oder die Datei wird noch vorbereitet. Lies vor einem erneuten Versuch den Status. |
| 500 | Aufnahmestart, Speicherinitialisierung oder Dateivorbereitung/-lesen fehlgeschlagen. Prüfe die Fehlermeldung; eine fehlgeschlagene Aufnahme meldet im Status auch `failure`. |
| 501 | Video oder das angeforderte Audio wird nicht unterstützt. Prüfe die Fähigkeiten; verwende `audio: false`, wenn nur Audio nicht verfügbar ist. |
| 507 | Die Grenze der vom Dienst aufbewahrten Dateien wurde erreicht. Lade abgeschlossene Dateien herunter und lösche sie, bevor du eine weitere Aufnahme startest. |
