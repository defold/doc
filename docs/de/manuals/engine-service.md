---
title: Der Engine-Dienst und die HTTP-APIs zur Laufzeit
brief: Dieses Handbuch erklärt den HTTP-Dienst für die Entwicklung in einer laufenden Defold-Debug-Engine und wie Laufzeiterweiterungen oder externe Werkzeuge ihn nutzen können.
---

# Der Engine-Dienst und die HTTP-APIs zur Laufzeit {#the-engine-service-and-runtime-http-apis}

Wenn du ein Projekt im Debug-Modus ausführst, wird ein Prozess für eine bestimmte Laufzeitinstanz der Engine erstellt. Er enthält dein Spiel und einen speziellen Engine-Dienst (engine service), über den Entwicklungs- und Profiling-Infrastruktur, Laufzeitlogik und Nachrichten, der Engine-Zustand sowie Erweiterungen zugänglich sind.

Der Engine-Dienst ist ein HTTP-Dienst für die Entwicklung, der zu einer laufenden Debug- oder Headless-Engine (`dmengine` oder `dmengine_headless`) gehört.

Er ist vom [Editorserver](/manuals/editor-http-api) getrennt, der zum Defold-Editor gehört und das geöffnete Projekt steuert.

Die beiden Dienste verwenden unterschiedliche Ports. Ein Werkzeug, das sich mit dem Editorport verbindet, kann dort keine Routen von Laufzeiterweiterungen aufrufen. Umgekehrt kann ein Werkzeug, das sich mit dem Engine-Dienst verbindet, keine Editoroperationen aufrufen.

Der Engine-Dienst ist Teil der Infrastruktur für Debugging, Entwicklung und Profiling. Release-Instanzen der Engine erstellen diesen Dienst nicht.

## Verfügbarkeit und Ermitteln des Ports {#availability-and-port-discovery}

Wenn der Editor eine Debug-Engine startet, fordert er einen dynamisch zugewiesenen Dienst-Port an. Die Engine meldet den ausgewählten Port in der *Console* und bei einem Start über die Kommandozeile in ihrem Protokoll:

![Portinformationen des Engine-Dienstes in einem Defold-Debug-Build](images/automation/engine-service.png)

```text
INFO:ENGINE: Engine service started on port <port>
```

Die Engine protokolliert außerdem die vollständige OpenAPI-Erkennungs-URL mit ihrer tatsächlichen Adresse und dem zugewiesenen Port:

```text
INFO:ENGINE: OpenAPI: http://<address>:<port>/openapi.json
```

Diese Zeilen erscheinen in der Editor-Konsole, wenn das Spiel über den Editor gestartet wurde. Eine einfache lokale Steuerung kann sie auswerten, eine wiederverwendbare Integration sollte die Engine-Instanz und den registrierten Port jedoch vom Editor oder dessen Wrapper verfolgen lassen. Dadurch wird vermieden, einen alten Port mit einem neu gestarteten oder wiederverwendeten Prozess zu verwechseln.

Auf unterstützten Plattformen gibt die Engine Entwicklungsziele außerdem über die Diensterkennung bekannt. Dieser Mechanismus wird hauptsächlich von Defold-Werkzeugen verwendet und sollte nicht durch einen dauerhaft fest einprogrammierten Port ersetzt werden.

Der Server ist unter localhost (`127.0.0.1`) am jeweiligen Port erreichbar:

![Zugriff auf den Engine-Server](images/automation/engine-server.png)

## Operationen über OpenAPI ermitteln {#discovering-operations-through-openapi}

`GET /openapi.json` gibt ein OpenAPI-3.0.3-Dokument zurück, das die HTTP-API zur Laufzeit beschreibt. Verwende den Engine-Dienst-Port aus dem Protokoll. Ersetze bei einer lokalen Engine `<port>` unten durch diesen Port:

```sh
ENGINE_URL="http://127.0.0.1:<port>"
curl -fsS "$ENGINE_URL/openapi.json" | jq
```

Das Dokument beschreibt Pfade, Methoden, Parameter, Anfragekörper und Antworten der aktuell registrierten Handler, einschließlich nativer Erweiterungen, die OpenAPI-Metadaten bereitstellen. Sein Objekt `paths` ändert sich, wenn Handler hinzugefügt oder entfernt werden. Profiler- und Erweiterungsrouten hängen von Plattform, Konfiguration und registrierten Erweiterungen der laufenden Engine ab; rufe das Dokument daher von der Instanz ab, die du verwendest.

Handler ohne registrierte OpenAPI-Metadaten bleiben aufrufbar, erscheinen jedoch nicht im Dokument. Auch eine dokumentierte Route kann eine nicht verfügbare Funktion melden; prüfe vor plattformabhängigen Operationen ihre Antwortbeschreibungen und gegebenenfalls den Endpunkt zur Abfrage der Fähigkeiten.

Der Editor hat auf seinem eigenen Port ein separates [OpenAPI-Dokument](/manuals/editor-http-api/#discovering-operations-through-openapi). Verwende für Operationen zur Laufzeit das Dokument der Engine.

## Integrierte Endpunkte {#built-in-endpoints}

Die aktuelle Debug-Engine registriert eine kleine Anzahl von Kernrouten.

| Endpunkt | Zweck |
| --- | --- |
| `GET /openapi.json` | Aktuell registrierte HTTP-Operationen zur Laufzeit mit OpenAPI-Metadaten ermitteln |
| `GET /ping` | Prüfen, ob der Engine-Dienst antwortet |
| `GET /info` | Engine-Version, Plattform, Build-Kennung und Informationen zum Protokolldienst lesen |
| `GET /state` | Den von Defold-Werkzeugen verwendeten Verbindungszustand für die Entwicklung lesen |
| `POST /post/<socket>/<message-type>` | Eine Protobuf-codierte Defold-Nachricht an einen benannten Engine-Socket senden |

Zum Beispiel:

```sh
curl -sS "$ENGINE_URL/ping"
curl -sS "$ENGINE_URL/info" | jq
curl -sS "$ENGINE_URL/state" | jq
```

Die Route `/post` wird für Entwicklungsvorgänge wie Hot Reload, Neustart, Größenänderung und Prozesssteuerung verwendet. Ihr Anfrageinhalt ist eine binäre Protobuf-Nachricht des in der Route genannten Typs; sie ist keine API für JSON-Nachrichten. Die Protobuf-Nachricht darf in serialisierter Form nicht größer als 1024 Bytes sein, andernfalls wird `400 Too large message` zurückgegeben.

Diese Routen gehören zur Entwicklungsinfrastruktur. In der Engine-Implementierung gibt es außerdem weitere Routen für den Profiler und die Untersuchung von Ressourcen.

## Aufnahme-Endpunkte {#recording-endpoints}

Desktop-Debug-Engines stellen über die folgenden Routen auch native MP4-Aufnahmen bereit. Diese fehlen in Release-, Headless-, Mobil- und Web-Builds sowie bei aktiviertem **Exclude Record** im [Anwendungsmanifest](/manuals/app-manifest/#exclude-record).

| Endpunkt | Zweck |
| --- | --- |
| `GET /recording/capabilities` | Video-/Audiounterstützung, Backend-Anforderungen und die `instance_id` des Aufnahmedienstes ermitteln |
| `GET /recording/status` | Aktuelle Operation, asynchronen Fortschritt und Informationen zur finalisierten Datei lesen |
| `POST /recording/start` | Aufnahme anfordern und ihre `operation_id` erhalten |
| `POST /recording/stop` | Stoppen und Finalisieren der angegebenen Operation anfordern |
| `GET /recording/files/{id}` | Eine finalisierte MP4-Datei herunterladen |
| `DELETE /recording/files/{id}` | Eine abgeschlossene, vom Dienst aufbewahrte Datei löschen |

Ermittle diese Routen über `/openapi.json` und prüfe anschließend `/recording/capabilities` auf die Unterstützung der aktuellen Plattform. Aufnahmeänderungen benötigen den Header `X-Recording-Instance`; zum Stoppen ist außerdem die akzeptierte `operation_id` erforderlich. Start und Stopp sind asynchron; warte vor dem Herunterladen der Datei auf ihre Finalisierung. Den vollständigen Ablauf beschreibt das [Aufnahmehandbuch](/manuals/recording/#recording-through-http).

Der HTTP-Dienst teilt sich den Recorder mit Lua. HTTP-Starts aktivieren standardmäßig Anwendungsaudio, sofern unterstützt; Lua-Starts nehmen standardmäßig nur Video auf. Nur über HTTP gestartete Aufnahmen besitzen einen herunterladbaren `file`-Beleg. Warte vor dem Herunterladen auf `pending: false`, `finalized: true` und `file.state: "complete"` und [prüfe anschließend Dateigröße und SHA-256](/manuals/recording/#download-and-release-the-file). Beachte beim Kombinieren von Lua und HTTP-Clients die Hinweise zum [gemeinsam genutzten Recorder](/manuals/recording/#sharing-the-recorder-with-http-clients).

## Endpunkt für Metal-GPU-Traces {#metal-gpu-trace-endpoint}

Unter macOS stellen Debug-Engines `/profiler/gputrace` zur Aufzeichnung von Metal-GPU-Traces bereit. Die Route erscheint nur unter macOS in `/openapi.json`. Die Aufzeichnung benötigt den nativen Metal-Adapter und `METAL_CAPTURE_ENABLED=1` in der Startumgebung der Engine. Ist die Aufzeichnung nicht verfügbar, gibt eine Anfrage HTTP 501 mit `error.code: "gputrace_unsupported"` zurück.

| Endpunkt | Zweck |
| --- | --- |
| `POST /profiler/gputrace` | Aufzeichnung in einen beschreibbaren absoluten `.gputrace`-Pfad planen; `frames` ist standardmäßig `1` und darf `1`–`10000` betragen. |
| `GET /profiler/gputrace` | Zustand, Pfad und Frame-Anzahlen der aktuellen oder letzten Aufzeichnung lesen. |
| `DELETE /profiler/gputrace` | Eine ausstehende Aufzeichnung abbrechen oder eine laufende nach dem aktuellen gerenderten Frame beenden; der Trace bleibt auf dem Datenträger. |

Akzeptierte Anfragen liefern HTTP 200 mit `ok: true` und einem Objekt `data`. Die Aufzeichnung läuft asynchron: Frage mit `GET` ab, bis `data.state` den Wert `complete`, `canceled` oder `failed` hat. Native Startfehler werden in `data.error` gemeldet. Der Trace wird auf dem Engine-Host geschrieben. Die [Anleitung für Metal-GPU-Traces](/manuals/profiling/#metal-gpu-trace-capture) enthält Startbefehle, Abfragen der Unterstützung, Aufzeichnungsbeispiele und Hinweise zum Öffnen des Ergebnisses in Xcode.

## Von Erweiterungen definierte Laufzeitrouten {#extension-defined-runtime-routes}

In Debug-Builds kann das SDK für native Erweiterungen (native extensions) Zugriff auf den Webserver der Engine bereitstellen. Eine Erweiterung kann auf diesem Server ein Routenpräfix registrieren und Operationen verfügbar machen, die von Laufzeitdaten abhängen.

Das ist für Entwicklungswerkzeuge nützlich, da eine Erweiterung den vorhandenen Engine-Dienst mitbenutzen kann, ohne einen weiteren HTTP-Server zu öffnen.

Eine von einer Erweiterung definierte API zur Laufzeitautomatisierung sollte:

* ein eigenes, versioniertes Routenpräfix verwenden;
* unterstützte Funktionen offenlegen;
* strukturierte Fehlerinformationen zurückgeben;
* nicht verfügbare Plattform- oder Engine-Funktionen ausdrücklich behandeln;
* Operationen auf lokale Entwicklung und Tests beschränken;
* dokumentieren, ob sie aus Release-Builds ausgeschlossen wird.

### Operationen von Erweiterungen in OpenAPI veröffentlichen {#publishing-extension-operations-in-openapi}

Rufe im Callback zur Anwendungsinitialisierung einer nativen Erweiterung den Server mit `dmEngine::GetWebServer(app_params)` ab und registriere Handler nur, wenn das zurückgegebene Handle nicht null ist. Die Einrichtung des Callbacks beschreibt der [Lebenszyklus von Erweiterungen](/manuals/extensions/#extension-lifecycle).

Die Überladung von `dmWebServer::AddHandler()` mit vier Argumenten akzeptiert ein OpenAPI-3.0.3-Paths-Objekt als JSON-Zeichenfolge. Die Schlüssel auf oberster Ebene sind Routenpfade. Jeder Pfad muss mit dem registrierten Präfix beginnen und darf noch nicht von einem anderen Handler dokumentiert sein. Verwende eingebettete Schemas oder Referenzen auf Pfade im resultierenden Dokument.

Diese Hilfsfunktion registriert beispielsweise einen Callback und die Beschreibung seines Status-Endpunkts:

```cpp
#include <dmsdk/dlib/webserver.h>

static const char STATUS_OPENAPI[] = R"json(
{
  "/example/v1/status": {
    "get": {
      "summary": "Get extension status",
      "responses": {
        "200": {
          "description": "Current extension status",
          "content": {
            "text/plain": {
              "schema": { "type": "string" }
            }
          }
        }
      }
    }
  }
}
)json";

dmWebServer::Result RegisterStatusHandler(dmWebServer::HServer server,
                                        dmWebServer::Handler callback,
                                        void* context)
{
    dmWebServer::HandlerParams params;
    params.m_Handler = callback;
    params.m_Userdata = context;
    return dmWebServer::AddHandler(
        server, "/example/v1", &params, STATUS_OPENAPI);
}
```

Übergib einen Callback, der `GET /example/v1/status` implementiert und die dokumentierte `text/plain`-Antwort liefert. Der Callback bleibt für die Prüfung von Anfragepfaden und -methoden sowie die Erzeugung von Antworten verantwortlich. Prüfe das Registrierungsergebnis: Ungültige oder widersprüchliche Metadaten ergeben `dmWebServer::RESULT_ERROR_INVAL`.

Der Server behält den JSON-Zeiger, ohne die Zeichenfolge zu kopieren. Halte ihren Speicher unverändert und gültig, bis der Handler mit `dmWebServer::RemoveHandler()` entfernt oder der Server zerstört wird. Das Array `static const char` im Beispiel erfüllt diese Anforderung. Beim Entfernen des Handlers werden seine Pfade auch aus nachfolgenden Antworten von `/openapi.json` entfernt.

Die Überladung `dmWebServer::AddHandler(server, prefix, &params)` mit drei Argumenten wird weiterhin unterstützt. Sie entspricht der Übergabe von `0` als viertem Argument: Der Handler wird ohne OpenAPI-Metadaten registriert und erscheint nicht in der Erkennung.

## Die Erweiterung Automation Bridge {#automation-bridge-extension}

Die offizielle Defold-Erweiterung [Automation Bridge](https://github.com/defold/extension-automation-bridge) ist eine native Erweiterung, die ausschließlich in Debug-Builds verfügbar ist und auf dem Engine-Dienst aufbaut. Sie registriert eine versionierte API zur Laufzeitautomatisierung unter:

```text
http://127.0.0.1:<engine-service-port>/automation-bridge/v1
```

Ihre Laufzeit-API bietet Funktionen wie das Untersuchen von Szenen und Knoten (nodes), Eingaben, Bildschirminformationen, Bildschirmaufnahmen, Aufzeichnungen, Lebenszyklusinformationen und eine optionale, von der Anwendung festgelegte Synchronisierung. Zu den Operationen gehören:

| Operation | Aktion |
| --- | --- |
| `GET  /automation-bridge/v1/health` | Statusbericht, unterstützte API-Funktionen und Kompatibilität |
| `POST /automation-bridge/v1/input/click` | Für Eingabeinteraktionen zur Laufzeit |
| `GET  /automation-bridge/v1/screenshot` | Für Bildschirmaufnahmen zur Laufzeit |

Verwende die [Dokumentation der nativen API](https://github.com/defold/extension-automation-bridge/tree/master/automation_bridge) und die [Dokumentation der Python-Hilfsfunktionen](https://github.com/defold/extension-automation-bridge/tree/master/automation_bridge/automation-bridge-python) der Erweiterung für die im Projekt installierte Version.

Automation Bridge stellt in Release-Builds weder seine HTTP-API noch sein Lua-Modul bereit.

### Editor- und Laufzeitclients {#editor-and-runtime-clients}

Die Python-Hilfsfunktionen von Automation Bridge veranschaulichen die Architektur mit zwei Clients. Die Funktion `editor.open_project()` gibt einen Editor-Projektclient zurück, und `project.build_and_run()` gibt einen separaten Engine-Client zurück.

| Client | Zweck |
| --- | --- |
| Projekt | HTTP-API des Editors, Befehle, Debugger, Konsole, Editoreinstellungen, Referenz, Vorschauen, Build und Ermitteln des Ports |
| Spiel - Engine-Dienst | Szene, Eingabe, Bildschirmaufnahmen, Laufzeitzustand und Synchronisierung |

Die Aufteilung in `project` und `game` macht die Prozessgrenze deutlich. Editoroperationen bleiben auf dem Editorserver, während Beobachtungen und Aktionen am laufenden Spiel auf dem Engine-Dienst bleiben.

```python
from automation_bridge import editor

project = editor.open_project(".")
game = project.build_and_run()
```

## Einschränkungen und Sicherheit {#limitations-and-security}

Der Engine-Dienst und die von Erweiterungen definierten Routen sind Entwicklungswerkzeuge und sollten als solche behandelt werden.

::: important
Verwende ab Defold 1.14.1 das Dokument `/openapi.json` der laufenden Engine zur Erkennung. Frühere Engines stellen diesen Endpunkt nicht bereit. Für Handler ohne registrierte OpenAPI-Metadaten verwende die versionierte API-Dokumentation der Erweiterung.
:::

Laufzeitskripte, Physik, Eingaben, dynamisch erstellte Objekte und plattformspezifisches Rendering benötigen eine laufende Engine und sollten durch [automatisiertes Testen zur Laufzeit](/manuals/automated-testing) überprüft werden.

* Mache den Dienst nicht über einen Router, eine öffentliche Schnittstelle oder einen nicht vertrauenswürdigen Tunnel zugänglich.
* Gehe nicht davon aus, dass die Routen des Engine-Dienstes eine Authentifizierung erfordern.
* Laufzeitrouten können je nach Erweiterungsversion, Plattform, Grafik-Backend und unterstützten Engine-Funktionen variieren.
* Handle bei aktuellen, von Erweiterungen definierten APIs die Version oder die unterstützten Funktionen aus.
