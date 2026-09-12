---
title: Der Engine-Dienst und die HTTP-APIs zur Laufzeit
brief: Dieses Handbuch erklärt den HTTP-Dienst für die Entwicklung in einer laufenden Defold-Debug-Engine und wie Laufzeiterweiterungen oder externe Werkzeuge ihn nutzen können.
---

# Der Engine-Dienst und die HTTP-APIs zur Laufzeit {#the-engine-service-and-runtime-http-apis}

Wenn du ein Projekt im Debug-Modus ausführst, wird ein Prozess für eine bestimmte Laufzeitinstanz der Engine erstellt. Er enthält dein Spiel und einen speziellen Engine-Dienst (engine service), über den Entwicklungs- und Profiling-Infrastruktur, Laufzeitlogik und Nachrichten, der Engine-Zustand sowie Erweiterungen zugänglich sind.

Der Engine-Dienst ist ein HTTP-Dienst für die Entwicklung, der zu einer laufenden Debug-Engine (`dmengine`) gehört.

Er ist vom [Editorserver](/manuals/editor-http-api) getrennt, der zum Defold-Editor gehört und das geöffnete Projekt steuert.

Die beiden Dienste verwenden unterschiedliche Ports. Ein Werkzeug, das sich mit dem Editorport verbindet, kann dort keine Routen von Laufzeiterweiterungen aufrufen. Umgekehrt kann ein Werkzeug, das sich mit dem Engine-Dienst verbindet, keine Editoroperationen aufrufen.

Der Engine-Dienst ist Teil der Infrastruktur für Debugging, Entwicklung und Profiling. Release-Instanzen der Engine erstellen diesen Dienst nicht.

## Verfügbarkeit und Ermitteln des Ports {#availability-and-port-discovery}

Wenn der Editor eine Debug-Engine startet, fordert er einen dynamisch zugewiesenen Dienstport an. Die Engine meldet den gewählten Port in `Console` (`und bei einem Start über eine CLI auch in ihrem Protokoll):

![Portinformationen des Engine-Dienstes in einem Defold-Debug-Build](images/automation/engine-service.png)

```text
INFO:ENGINE: Engine service started on port <port>
```

Die Zeile erscheint in der Editorkonsole, wenn das Spiel aus dem Editor gestartet wurde. Eine einfache lokale Steuerung kann diese Zeile auswerten. Bei einer wiederverwendbaren Integration sollte jedoch der Editor oder dessen Wrapper die Engine-Instanz und den registrierten Port nachverfolgen. So wird vermieden, dass ein alter Port mit einem neu gestarteten oder wiederverwendeten Prozess verwechselt wird.

Auf unterstützten Plattformen gibt die Engine Entwicklungsziele außerdem über die Diensterkennung bekannt. Dieser Mechanismus wird hauptsächlich von Defold-Werkzeugen verwendet und sollte nicht durch einen dauerhaft fest einprogrammierten Port ersetzt werden.

Der Server ist unter localhost (`127.0.0.1`) am jeweiligen Port erreichbar:

![Zugriff auf den Engine-Server](images/automation/engine-server.png)

## Integrierte Endpunkte {#built-in-endpoints}

Die aktuelle Debug-Engine registriert eine kleine Anzahl von Kernrouten.

| Endpunkt | Zweck |
| --- | --- |
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
Der Engine-Dienst veröffentlicht derzeit kein OpenAPI-Dokument. Integrationen sollten sich auf dokumentiertes Verhalten oder auf die versionierte API einer Erweiterung beschränken.
:::

Laufzeitskripte, Physik, Eingaben, dynamisch erstellte Objekte und plattformspezifisches Rendering benötigen eine laufende Engine und sollten durch [automatisiertes Testen zur Laufzeit](/manuals/automated-testing) überprüft werden.

* Mache den Dienst nicht über einen Router, eine öffentliche Schnittstelle oder einen nicht vertrauenswürdigen Tunnel zugänglich.
* Gehe nicht davon aus, dass die Routen des Engine-Dienstes eine Authentifizierung erfordern.
* Laufzeitrouten können je nach Erweiterungsversion, Plattform, Grafik-Backend und unterstützten Engine-Funktionen variieren.
* Handle bei aktuellen, von Erweiterungen definierten APIs die Version oder die unterstützten Funktionen aus.
