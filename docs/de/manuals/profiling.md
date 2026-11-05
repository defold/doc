---
title: Profiling in Defold
brief: Dieses Handbuch erklärt die in Defold verfügbaren Profiling-Funktionen.
---

# Profiling

Defold enthält Profiling-Werkzeuge, die in die Engine und die Build-Pipeline integriert sind. Sie helfen dabei, Probleme mit der Leistung, dem Speicherverbrauch und der Ressourcennutzung zu finden. Profiling-Daten zur Laufzeit können von verschiedenen Werkzeugen ausgewertet werden:

* Der grundlegende Profiler und der visuelle Profiler im Spiel sind auf allen Plattformen verfügbar.
* Der [Remotery-Profiler](https://github.com/Celtoys/Remotery) und der interaktive Web-Frame-Profiler sind auf Desktop- und Mobilplattformen verfügbar.
* macOS-Debug-Builds mit Metal können [GPU-Traces](#metal-gpu-trace-capture) zur Untersuchung in Xcode speichern.
* HTML5-Builds können Defold-Messbereiche (Scopes) an die Web Performance API des Browsers übergeben.

Die Einstellung **Profiler** im [Anwendungsmanifest](/manuals/app-manifest/#profiler) steuert, ob Profiler-Code in einen Build eingebunden wird. **Debug Only** ist die Standardeinstellung, **None** schließt ihn aus und **Always** bindet ihn sowohl in Debug- als auch in Release-Builds ein. Die Einstellungen unter `profiler` in *game.project* steuern das Verhalten zur Laufzeit, binden ausgeschlossenen Profiler-Code aber nicht wieder in einen Build ein. Insbesondere steuert **Track CPU** die stichprobenartige Erfassung der CPU-Auslastung; diese Einstellung ist von der Auswahl im Anwendungsmanifest unabhängig.

## Der visuelle Profiler zur Laufzeit {#the-runtime-visual-profiler}

Builds mit Profiler-Unterstützung enthalten einen visuellen Profiler für die Laufzeit, der aktuelle Informationen über der laufenden Anwendung einblendet:

```lua
function on_reload(self)
    -- Toggle the visual profiler on hot reload.
    profiler.enable_ui(true)
end
```

![Visueller Profiler](images/profiling/visual_profiler.png)

Der visuelle Profiler stellt verschiedene Funktionen bereit, mit denen du die Darstellung seiner Daten ändern kannst:

```lua

profiler.set_ui_mode()
profiler.set_ui_view_mode()
profiler.view_recorded_frame()
```

Weitere Informationen zu den Profiler-Funktionen findest du in der [API-Referenz für den Profiler](/ref/profiler/).

## Der Web-Profiler {#the-web-profiler}
Während ein Desktop- oder Mobil-Build mit Profiler-Unterstützung läuft, kannst du über einen Browser auf interaktive Frame- und Ressourcen-Profiler zugreifen.

### Remotery-Frame-Profiler
Mit dem Frame-Profiler kannst du Messdaten deines Spiels während der Ausführung erfassen und einzelne Frames im Detail analysieren. So öffnest du den Profiler:

1. Starte dein Spiel auf deinem Zielgerät.
2. Wähle den Menüeintrag <kbd> Debug ▸ Open Web Profiler</kbd>.

Der Frame-Profiler ist in mehrere Bereiche unterteilt, die jeweils unterschiedliche Ansichten des laufenden Spiels zeigen. Klicke oben rechts auf die Schaltfläche Pause, um die Aktualisierung der Ansichten durch den Profiler vorübergehend anzuhalten.

![Web-Profiler](images/profiling/webprofiler_page.png)

::: sidenote
Wenn du mehrere Ziele gleichzeitig verwendest, kannst du manuell zwischen ihnen wechseln. Ändere dazu das Feld Connection Address oben auf der Seite so, dass es der URL des Remotery-Profilers entspricht, die beim Start des Ziels in der Konsole angezeigt wurde:

```
INFO:ENGINE: Defold Engine 1.3.4 (80b1b73)
INFO:DLIB: Initialized Remotery (ws://127.0.0.1:17815/rmt)
INFO:ENGINE: Loading data from: build/default
```
:::

Sample Timeline
: Sample Timeline zeigt die in der Engine erfassten Daten der Frames mit einer horizontalen Zeitleiste pro Thread. Main ist der Hauptthread, in dem die gesamte Spiellogik und der Großteil des Engine-Codes ausgeführt werden. Remotery steht für den Profiler selbst und Sound für den Thread zum Mischen und Wiedergeben von Audio. Du kannst mit dem Mausrad hinein- und herauszoomen und einzelne Frames auswählen, um ihre Details in der Ansicht Frame Data zu sehen.

  ![Zeitleiste der Messdaten](images/profiling/webprofiler_sample_timeline.png)


Frame Data
: Die Ansicht Frame Data ist eine Tabelle, in der alle Daten des aktuell ausgewählten Frames im Detail aufgeschlüsselt sind. Du kannst sehen, wie viele Millisekunden in jedem Messbereich der Engine verbracht werden.

  ![Frame-Daten](images/profiling/webprofiler_frame_data.png)


Global Properties
: Die Ansicht Global Properties zeigt eine Tabelle mit Zählern. Damit kannst du beispielsweise die Anzahl der Zeichenaufrufe (draw calls) oder die Anzahl der Komponenten (components) eines bestimmten Typs leicht verfolgen.

  ![Globale Eigenschaften](images/profiling/webprofiler_global_properties.png)

::: sidenote
Der Wert LuaMem gibt den Speicherverbrauch der Lua-VM in Kilobytes an, wie ihn die automatische Speicherbereinigung von Lua meldet. Memory ist der Speicherverbrauch der Engine in Kilobytes.
:::

::: important
Die [Einstellung Max Sample Count](/manuals/project-settings/#max-sample-count) begrenzt die Anzahl der Profiler-Messwerte, die pro Thread und pro Frame aufgezeichnet werden. Wenn der Profiler meldet, dass der Grenzwert überschritten wurde, prüfe zunächst den Profiling-Code nativer Erweiterungen auf ein unvollständiges Paar aus Beginn und Ende eines Messbereichs. Erhöhe die Obergrenze nur, wenn ein ordnungsgemäßer Frame mehr Messbereiche enthält, als der konfigurierte Grenzwert erlaubt.
:::

### Ressourcen-Profiler {#resource-profiler}
Mit dem Ressourcen-Profiler kannst du dein Spiel während der Ausführung untersuchen und die Ressourcennutzung im Detail analysieren. So öffnest du den Profiler:

1. Starte einen Debug-Build deines Spiels auf dem Zielgerät.
2. Öffne die [Adresse des Engine-Dienstes](/manuals/engine-service/#availability-and-port-discovery) in einem Browser: `http://<address>:<port>/`. Verwende Adresse und Port, die die laufende Engine in der Konsole meldet.

Der Ressourcen-Profiler ist in 2 Bereiche unterteilt: Einer zeigt eine hierarchische Ansicht der Sammlungen (collections), Spielobjekte (game objects) und Komponenten, die aktuell in deinem Spiel instanziiert sind. Der andere zeigt alle aktuell geladenen Ressourcen.

![Ressourcen-Profiler](images/profiling/webprofiler_resources_page.png)

Sammlungsansicht
: Die Sammlungsansicht zeigt eine hierarchische Liste aller Spielobjekte und Komponenten, die aktuell im Spiel instanziiert sind, sowie die Sammlung, aus der sie stammen. Dies ist ein sehr nützliches Werkzeug, um genauer zu untersuchen und zu verstehen, was du zu einem bestimmten Zeitpunkt in deinem Spiel instanziiert hast und woher die Objekte stammen.

Ressourcenansicht
: Die Ressourcenansicht zeigt alle aktuell in den Speicher geladenen Ressourcen, ihre Größe und die Anzahl der Referenzen auf jede Ressource. Das ist bei der Optimierung des Speicherverbrauchs deiner Anwendung nützlich, wenn du verstehen musst, was sich zu einem bestimmten Zeitpunkt im Speicher befindet.

#### Ressourcenladezeiten {#resource-loading-times}

Du kannst auch untersuchen, wie lange einzelne Ressourcen zum Laden benötigen. Aktiviere [Resource → Profile](/manuals/project-settings/#profile) in *game.project*, bevor du das Spiel startest. In der Textansicht lautet diese Einstellung:

```ini
[resource]
profile = 1
```

Die Einstellung ist standardmäßig deaktiviert. Starte das Spiel nach dem Aktivieren neu, um Ladevorgänge beim Start zu messen. Jeder abgeschlossene oder fehlgeschlagene Ladevorgang schreibt einen Protokolleintrag auf INFO-Ebene mit Ressourcenpfad, Gesamtzeit sowie Zeiten für Preload, Read, Create, Post-Create, Queue und Wait. Cache-Treffer erzeugen keine neuen Ladeaufzeichnungen.

Klicke im Ressourcen-Profiler auf **Capture** und anschließend auf **Show load times**, um die Zeitspalten einzublenden. **Capture** aktualisiert die Ansicht gespeicherter Messungen; es aktiviert weder das Profiling noch misst es frühere Ladevorgänge nachträglich.

| Spalte | Bedeutung |
| --- | --- |
| **Load (ms)** | Gesamte verstrichene Zeit des ersten Ladens einschließlich Abhängigkeiten, Post-Create-Arbeit, Einreihen und Warten. |
| **Preload (ms)** | Zeit zur Vorbereitung der Ressource in ihrem Preload-Callback. |
| **Read (ms)** | Zeit zum Lesen der Ressourcendaten. |
| **Create (ms)** | Zeit zum Erzeugen der Laufzeitressource in ihrem Create-Callback. |

Beim Einblenden der Ladezeiten wird die Tabelle nach Gesamtladedauer sortiert, die langsamsten Ressourcen zuerst. Klicke auf die Überschrift einer Zeitspalte, um nach dieser Phase zu sortieren; ein erneuter Klick kehrt die Reihenfolge um. Die Balken in **Load** zeigen die jeweilige Gesamtzeit relativ zur langsamsten sichtbaren Ressource. Mit **Hide load times** blendest du die Spalten wieder aus.

Lade- und Callback-Zeiten enthalten Arbeit an verschachtelten Abhängigkeiten. Addiere die Gesamtzeiten verschiedener Ressourcen nicht zur Berechnung der Startzeit, da dieselbe Arbeit in mehreren Ressourcenmessungen erscheinen kann. Auch die Spalten **Preload**, **Read** und **Create** decken nicht die gesamte Ladezeit ab; die zusätzlichen Phasen stehen im Protokoll.

Ein Gedankenstrich (`—`) bedeutet, dass keine abgeschlossene Messung vorliegt, beispielsweise weil Profiling deaktiviert war oder das erste Laden noch nicht abgeschlossen ist. Eine gemessene Null wird als `0.000` angezeigt. Die Messungen beschreiben das erste Laden: Cache-Treffer und Hot Reload ändern sie nicht; beim Entladen einer Ressource wird ihre gespeicherte Messung entfernt.

## Metal-GPU-Traces aufzeichnen {#metal-gpu-trace-capture}

Der [HTTP-Dienst der Engine](/manuals/engine-service/#metal-gpu-trace-endpoint) kann unter macOS Metal-GPU-Befehle in ein *.gputrace*-Dokument aufzeichnen. Öffne den fertigen Trace in Xcode, um die aufgezeichneten Frames zu untersuchen. Diese Funktion ist in die Debug-Engine integriert.

### Starten und Unterstützung prüfen {#launch-and-check-support}

Erstelle ein macOS-[Debug-Bundle](/manuals/bundling/#release-vs-debug), das das native Metal-Grafik-Backend enthält. Wenn du ein Anwendungsmanifest verwendest, wähle unter **Graphics (macOS)** eine Option mit Metal; siehe [Grafik-Backends](/manuals/app-manifest/#graphics).

Starte die ausführbare Datei des Bundles aus einem Terminal mit `METAL_CAPTURE_ENABLED=1` und wähle den Metal-Adapter. Ersetze in diesem Beispiel den Bundle-Pfad und den Namen der ausführbaren Datei:

```sh
METAL_CAPTURE_ENABLED=1 \
    "/absolute/path/MyGame.app/Contents/MacOS/MyGame" --graphics-adapter=metal
```

Die Umgebungsvariable muss beim Start der Engine gesetzt sein. Sie nur in einem Terminal für HTTP-Anfragen zu setzen, aktiviert die Aufzeichnung nicht in einer bereits laufenden Engine.

Verwende in einem zweiten Terminal den [im Protokoll ausgegebenen Engine-Dienst-Port](/manuals/engine-service/#availability-and-port-discovery). Die folgenden Beispiele nutzen `curl` und `jq`:

```sh
ENGINE_URL="http://127.0.0.1:<port>"
curl -fsS "$ENGINE_URL/openapi.json" | jq '.paths["/profiler/gputrace"]'
curl -sS -i "$ENGINE_URL/profiler/gputrace"
```

Die Route ist nur unter macOS registriert. Ein `null`-Eintrag im OpenAPI-Dokument bedeutet, dass diese Engine sie nicht bereitstellt. Auch bei vorhandener Route hängt die Aufzeichnungsunterstützung von Grafikadapter und Startumgebung ab. `GET /profiler/gputrace` gibt HTTP 501 mit `error.code: "gputrace_unsupported"` zurück, wenn Metal-Aufzeichnung nicht verfügbar ist. Prüfe vor dem Fortfahren, dass die Engine Metal verwendet und mit `METAL_CAPTURE_ENABLED=1` gestartet wurde. Eine unterstützte Anfrage gibt HTTP 200 mit dem Aufzeichnungsstatus zurück.

### Frames aufzeichnen und untersuchen {#capture-and-inspect-frames}

Wähle einen beschreibbaren absoluten Ausgabepfad mit der Endung `.gputrace`, einem vorhandenen übergeordneten Verzeichnis und ohne bereits vorhandenen Trace an diesem Pfad. Der Pfad liegt auf dem Computer, auf dem die Engine läuft. Für eine lokale Engine erstellt dieses Beispiel ein neues temporäres Verzeichnis und fordert einen Frame an:

```sh
GPU_TRACE_DIR=$(mktemp -d /tmp/defold-gputrace.XXXXXX)
GPU_TRACE_PATH="$GPU_TRACE_DIR/frame.gputrace"
GPU_TRACE_REQUEST=$(jq -n --arg path "$GPU_TRACE_PATH" '{path: $path, frames: 1}')
curl -fsS -X POST \
    -H 'Content-Type: application/json' \
    --data "$GPU_TRACE_REQUEST" \
    "$ENGINE_URL/profiler/gputrace" | jq
```

`frames` ist optional, hat den Standardwert `1` und akzeptiert Ganzzahlen von `1` bis `10000`. Die Aufzeichnung beginnt vor dem nächsten gerenderten Frame und endet, nachdem die angeforderte Anzahl vollständiger Frames eingereicht wurde. Lasse das Spiel während des Wartens weiter rendern. Es kann nur eine ausstehende oder aktive Aufzeichnung geben; eine weitere Startanfrage liefert HTTP 409 mit `error.code: "gputrace_active"`.

`POST` gibt HTTP 200 mit `ok: true` und `data.state: "pending"` zurück, wenn die Aufzeichnung eingeplant wurde. Ihr Abschluss wird durch spätere Statusanfragen gemeldet. Wiederhole die Statusanfrage, bis `data.state` den Wert `complete`, `canceled` oder `failed` erreicht:

```sh
curl -fsS "$ENGINE_URL/profiler/gputrace" | jq
```

| `data.state` | Bedeutung |
| --- | --- |
| `idle` | Es wurde keine Aufzeichnung eingeplant. |
| `pending` | Die Aufzeichnung wartet auf den Beginn des Renderns. |
| `capturing` | Die Aufzeichnung ist aktiv; `data.frames_captured` meldet abgeschlossene Frames. |
| `complete` | Die Aufzeichnung ist abgeschlossen, und der Trace kann geöffnet werden. |
| `canceled` | Eine ausstehende Aufzeichnung wurde vor ihrem Start abgebrochen. |
| `failed` | Die Aufzeichnung konnte nicht starten; der native Fehler steht in `data.error`. |

`GET` beschreibt die aktuelle oder letzte Aufzeichnung. Prüfe, ob `data.path` deinem angeforderten Pfad entspricht. Auch eine fehlgeschlagene Aufzeichnung liefert HTTP 200 mit `ok: true`; prüfe `data.state` und `data.error`, um das Ergebnis zu bestimmen. Verwende bei automatisierten Clients ein Abfrageintervall und eine Zeitbegrenzung.

Öffne den Trace nach Erreichen des Zustands `complete` in Xcode auf dem Mac der Engine:

```sh
open -a Xcode "$GPU_TRACE_PATH"
```

Der HTTP-Endpunkt gibt den Status zurück; der Trace wird unter `data.path` auf dem Engine-Host gespeichert. Hole bei einer entfernten Engine das abgeschlossene Dokument von diesem Host, bevor du es lokal öffnest.

### Eine Aufzeichnung abbrechen oder stoppen {#cancel-or-stop-a-capture}

So brichst du eine ausstehende Aufzeichnung ab oder beendest eine aktive Aufzeichnung vorzeitig:

```sh
curl -fsS -X DELETE "$ENGINE_URL/profiler/gputrace" | jq
```

Eine ausstehende Aufzeichnung wechselt zu `canceled`. Bei einer aktiven Aufzeichnung wird `data.stop_requested` zu `true`, und die Aufzeichnung endet nach dem Einreichen des aktuell gerenderten Frames. Frage weiter mit `GET` ab, bis ein Endzustand erreicht ist. `DELETE` lässt bereits auf den Datenträger geschriebene Traces bestehen. Wenn keine Aufzeichnung aussteht oder aktiv ist, liefert es HTTP 409 mit `error.code: "gputrace_inactive"`.

## Leistungszeitleiste im HTML5-Browser {#html5-browser-performance-timeline}

HTML5 verwendet für seine Browserzeitleiste die Web Performance API anstelle von Remotery. So zeichnest du Defold-Messbereiche auf:

1. Stelle sicher, dass der im Anwendungsmanifest ausgewählte Profiler-Modus Profiler-Unterstützung in der von dir ausgeführten Build-Variante einschließt.
2. Aktiviere **Performance Timeline Enabled** (`profiler.performance_timeline_enabled`) in *game.project*.
3. Starte den HTML5-Build und öffne die Entwicklerwerkzeuge des Browsers.
4. Zeichne im Bereich **Performance** des Browsers eine Sitzung auf und untersuche die Defold-Messbereiche in der entstandenen Zeitleiste.

Diese Browserzeitleiste ist sowohl vom visuellen Profiler im Spiel als auch vom interaktiven Remotery-Web-Profiler getrennt.


## Build-Berichte {#build-reports}
Wenn du ein Bundle deines Spiels erstellst, kannst du dabei einen Build-Bericht erzeugen. Damit erhältst du einen sehr nützlichen Überblick über die Größe aller Assets, die zu deinem Spiel-Bundle gehören. Aktiviere bei der Bundle-Erstellung einfach das Kontrollkästchen *Generate build report*.

![Build-Bericht](images/profiling/build_report.png)

Das Build-Werkzeug erzeugt neben dem Spiel-Bundle eine Datei namens `report.html`. Öffne die Datei in einem Webbrowser, um den Bericht zu untersuchen:

![Build-Bericht](images/profiling/build_report_html.png)

*Overview* bietet eine visuelle Gesamtübersicht der Projektgröße, aufgeschlüsselt nach Ressourcentyp.

*Resources* zeigt eine detaillierte Liste der Ressourcen, die du nach Größe, Komprimierungsverhältnis, Verschlüsselung, Typ und Verzeichnisname sortieren kannst. Verwende das Feld „search“, um die angezeigten Ressourceneinträge zu filtern.

Der Bereich *Structure* zeigt die Größen anhand der Anordnung der Ressourcen in der Dateistruktur des Projekts. Die Einträge sind entsprechend der relativen Größe der Datei- und Verzeichnisinhalte farblich von Grün (klein) bis Blau (groß) gekennzeichnet.


## Externe Werkzeuge {#external-tools}
Zusätzlich zu den integrierten Werkzeugen gibt es eine große Auswahl kostenloser, hochwertiger Werkzeuge für Tracing und Profiling. Hier eine Auswahl:

ProFi (Lua)
: Defold enthält keinen integrierten Lua-Profiler, aber es gibt externe Bibliotheken, die sich recht einfach verwenden lassen. Um herauszufinden, wo deine Skripte Zeit benötigen, kannst du entweder selbst Zeitmessungen in deinen Code einfügen oder eine Lua-Profiling-Bibliothek wie [ProFi](https://github.com/jgrahamc/ProFi) verwenden.

  Beachte, dass reine Lua-Profiler mit jedem installierten Hook einen beträchtlichen zusätzlichen Aufwand verursachen. Daher solltest du die mit einem solchen Werkzeug ermittelten Zeitprofile mit etwas Vorsicht betrachten. Profile zur Zählung von Aufrufen sind allerdings ausreichend genau.

Instruments (macOS und iOS)
: Dieses Werkzeug zur Leistungsanalyse und -visualisierung ist Teil von Xcode. Damit kannst du das Verhalten einer oder mehrerer Anwendungen oder Prozesse aufzeichnen und untersuchen, gerätespezifische Funktionen wie WLAN und Bluetooth analysieren und vieles mehr.

  ![Instruments](images/profiling/instruments.png)

OpenGL-Profiler (macOS)
: Teil des Pakets „Additional Tools for Xcode“, das du von Apple herunterladen kannst. Wähle dazu im Xcode-Menü <kbd>Xcode ▸ Open Developer Tool ▸ More Developer Tools...</kbd>.

  Mit diesem Werkzeug kannst du eine laufende Defold-Anwendung untersuchen und sehen, wie sie OpenGL verwendet. Du kannst OpenGL-Funktionsaufrufe aufzeichnen, Haltepunkte für OpenGL-Funktionen setzen, Anwendungsressourcen wie Texturen, Programme und Shader untersuchen, Pufferinhalte ansehen und weitere Aspekte des OpenGL-Zustands prüfen.

  ![OpenGL-Profiler](images/profiling/opengl.png)

Android Profiler (Android)
: https://developer.android.com/studio/profile/android-profiler.html

  Eine Sammlung von Profiling-Werkzeugen, die Echtzeitdaten zur CPU-, Speicher- und Netzwerkaktivität deines Spiels erfasst. Du kannst den Methodenablauf bei der Codeausführung anhand von Stichproben aufzeichnen, Heap-Dumps erfassen, Speicherzuweisungen ansehen und Details zu über das Netzwerk übertragenen Dateien untersuchen. Um das Werkzeug zu verwenden, musst du `android:debuggable="true"` in `AndroidManifest.xml` setzen.

  ![Android Profiler](images/profiling/android_profiler.png)

  Hinweis: Seit Android Studio 4.1 kannst du die [Profiling-Werkzeuge auch ausführen, ohne Android Studio zu starten](https://developer.android.com/studio/profile/android-profiler.html#standalone-profilers).

Graphics API Debugger (Android)
: https://github.com/google/gapid

  Dies ist eine Sammlung von Werkzeugen, mit denen du Aufrufe einer Anwendung an einen Grafiktreiber untersuchen, anpassen und erneut abspielen kannst. Um das Werkzeug zu verwenden, musst du `android:debuggable="true"` in `AndroidManifest.xml` setzen.

  ![Graphics API Debugger](images/profiling/gapid.png)
