---
title: Automatisiertes Testen und Überprüfen
brief: Dieses Handbuch erklärt, wie du deterministische Defold-Tests lokal, in einem laufenden Spiel, in Browsern und in der kontinuierlichen Integration entwirfst, ausführst und ihre Ergebnisse protokollierst.
---

# Automatisiertes Testen und Überprüfen {#automated-testing-and-verification}

Automatisiertes Testen überprüft Defold-Code und -Inhalte anhand ausdrücklicher, maschinenlesbarer Nachweise. Nutze dieses Handbuch, um Tests zu entwerfen, die gleichermaßen mit lokalen Skripten, Runnern für CI (kontinuierliche Integration) und Programmieragenten funktionieren. Es behandelt Modultests, laufende Sammlungen (collections), Browsertests, Laufzeitautomatisierung, visuelle Prüfungen und Builds ohne grafische Oberfläche (headless) und gibt nützliche Empfehlungen für die Praxis.

## Überprüfungsebenen {#verification-levels}

Sinnvoll aufgebaute Ebenen für automatisierte Tests folgen dem Modell der Testpyramide, das Tests in drei Hauptebenen unterteilt: Unit-Tests, Integrationstests und Ende-zu-Ende-Tests (E2E). In Defold kannst du Tests in gesonderte Sammlungen aufteilen, die beim Start geladen werden können. Üblicherweise ist es sinnvoll, mit der am engsten gefassten und schnellsten Prüfung zu beginnen, die das Problem erkennen kann, und dann bei Bedarf Laufzeit- oder Plattformtests hinzuzufügen.

| Ebene | Geeignete Nachweise |
| --- | --- |
| Statische Validierung | Parser, Formatierungswerkzeug, Ressourcenvalidator oder Vergleich generierter Dateien |
| Modultest | Assertion-Ergebnisse für wiederverwendbare Lua-Logik mit minimalen Engine-Abhängigkeiten |
| Laufende Sammlung | Nachrichten, Komponenten (components), Eingabe, Physik, Lebenszyklus und Engine-Verhalten |
| Laufzeitautomatisierung | Aktueller Szenenzustand, eingespeiste Eingabe, Anwendungszustand und Bildschirmaufnahmen zur Laufzeit |
| HTML5-Browsertest | Eingabe auf der Zeichenfläche, Browserintegration, Verhalten des Ansichtsbereichs (viewport) und Web-Ausgabe |
| Plattformtest | Verhalten und Rendering auf der tatsächlichen Zielplattform |
| Build und Bundle | Beendigungsstatus von Bob, Build-Bericht, Archiv und Bundle-Artefakte |

Eine erfolgreiche Kompilierung belegt, dass sich das Projekt erstellen lässt, aber nicht, dass sich das Gameplay korrekt verhält. Eine Bildschirmaufnahme belegt keine komplexen Übergänge, Animationen, Interaktionen oder Spielabläufe. Moderne multimodale Lösungen können damit jedoch untersuchen, wie ein einzelner Frame aussah und ob Shader und visuelles Layout korrekt sind. Bevorzuge für automatisierte Tests jedoch deterministische Assertions, wenn sich die Bedingung direkt ausdrücken lässt.

## Wiederverwendbarer und testbarer Lua-Code {#reusable-and-testable-lua-code}

Halte wiederverwendbare Logik in Lua-Modulen mit minimalen Engine-Abhängigkeiten. Reine Datentransformationen, Regeln, Zustandsautomaten und Berechnungen lassen sich dann testen, ohne eine vollständige Spielwelt aufzubauen.

Trenne Code, der mit der Engine interagiert, von der Logik, die er aufruft. Ein Skript kann Nachrichten und Komponentenzustände in Aufrufe eines Moduls übersetzen, während Tests das Modul direkt mit kontrollierten Eingaben aufrufen.

Weitere Einzelheiten findest du im [Handbuch zum Schreiben von Code](/manuals/writing-code).

## Tests in einer laufenden Sammlung {#tests-in-a-running-collection}

Verwende eine eigene Testsammlung, wenn das Verhalten von Spielobjekten (game objects), Komponenten, Nachrichten, Eingabe, Physik oder anderen Engine-Systemen abhängt.

Jeder Test sollte:

1. einen bekannten Zustand herstellen;
2. ein einzelnes Verhalten ausführen;
3. das erwartete Ergebnis mit Assertions prüfen und bewerten;
4. erstellte Ressourcen bereinigen;
5. eine strukturierte Ergebnisbeschreibung ausgeben.

Bevorzuge isolierte Testsammlungen für Tests. Ein Projekt kann über eine vorübergehende Projekteinstellung in `game.project` eine Testsammlung als Startsammlung (bootstrap collection) auswählen:

```ini
[bootstrap]
main_collection = /test/test.collectionc
```

Lasse eine vorübergehende Startsammlung für Tests nicht in der normalen Projektkonfiguration stehen. Bevorzuge in CI eine eigene Einstellungsdatei, die du an Bob übergibst. CI kann den Zustand des Repositorys nicht ändern; sie sollte nur bei Bedarf vorübergehende Änderungen vornehmen.

Für komplexe Spiele kannst du kleine Sammlungen als „Entwicklungsräume“ mit vordefinierten Szenarien und einfachen geometrischen Entwürfen erstellen. Sie machen Mechaniken reproduzierbar und erleichtern die Entwicklung, weil du sie testen kannst, ohne durch dafür nicht relevante Spielzustände und Abschnitte navigieren zu müssen.

### Testframeworks {#test-frameworks}

Projekte können einen kleinen Testrunner implementieren oder eine [Testbibliothek aus der Community](https://defold.com/assets/?tag=testing) verwenden.

Zum Beispiel ist [DefTest](https://defold.com/assets/deftest/) eine auf Telescope basierende Unit-Test-Bibliothek. Sie unterstützt Testsuites, Funktionen zur Testvorbereitung und -nachbereitung, Assertions, Namensfilter, Mocks für ausgewählte Defold-APIs und optional die Ermittlung der Codeabdeckung mit LuaCov. Tests können aus einer eigenen Startsammlung ausgeführt werden, auch in einem mit Bob erstellten Bundle ohne grafische Oberfläche.

## Strukturierte Testergebnisse {#structured-test-results}

Die Zusammenfassung eines Frameworks in der Konsole oder im Protokoll kann für Entwickler nützlich sein, doch eine unbeaufsichtigte automatische Steuerung benötigt weiterhin ein ausdrückliches Abschlussergebnis. Ergänze bei Bedarf einen kleinen Adapter um den Callback oder die Zusammenfassung des Frameworks, damit die Steuerung die Testergebnisse leicht verarbeiten kann.

Eine einfache Ergebnisbeschreibung kann ein eindeutiges Präfix verwenden, gefolgt von jeweils einem JSON-Objekt pro physischer Konsolenzeile:

```text
TEST {"run":"8f13","event":"suite_start","tests":2}
TEST {"run":"8f13","event":"case","name":"player_moves","status":"pass","duration_ms":3}
TEST {"run":"8f13","event":"case","name":"player_stops","status":"pass","duration_ms":2}
TEST {"run":"8f13","event":"suite_end","status":"pass","passed":2,"failed":0}
```

Ein Erfassungsprogramm sollte jede Zeile unabhängig verarbeiten, das Präfix `TEST` finden, das darauf folgende JSON parsen und nicht dazugehörige Engine-Ausgaben ignorieren.

Gib eine eindeutige Lauf-ID an, damit Ausgaben eines alten oder gleichzeitig laufenden Prozesses den aktuellen Lauf nicht abschließen können. Jede Testsuite sollte genau ein eindeutiges Abschlussereignis ausgeben (etwa `Pass`, `Failure`, `Crash`, `Timeout` usw.).

### Konsolenausgabe erfassen {#collecting-console-output}

Wenn ein Spiel aus dem Editor heraus läuft, stellt es sowohl den aktuellen Konsolenverlauf als auch einen kontinuierlichen Datenstrom bereit. Schließe den Datenstrom nach einem passenden Abschlussereignis der Testsuite, dem Ende des Prozesses, einem Fehler oder dem Erreichen eines konfigurierten Zeitlimits und einer Zeilenbegrenzung.

Weitere Informationen findest du im [Handbuch zur HTTP-API des Editors](/manuals/editor-http-api/#reading-console-output).

### Gespeicherte Protokolle {#persisted-logs}

Defold kann das Spielprotokoll auch speichern, wenn du `Write Log File` in `game.project` aktivierst. Siehe [Spiel- und Systemprotokolle](/manuals/debugging-game-and-system-logs/). Die Protokollierung in einer Datei ist nützlich für paketierte Anwendungen und zum Testen von Zielgeräten, auf denen die Editorkonsole nicht verfügbar ist.

Das Projekt kann die integrierten Funktionen `print()` und `pprint()` oder beispielsweise eine andere [Protokollierungsbibliothek](https://defold.com/assets/?tag=logging) aus unserem Asset Portal verwenden.

## Ein laufendes Spiel über eine Laufzeit-API testen {#testing-a-running-game-through-a-runtime-api}

Eine API für Laufzeitautomatisierung kann eine laufende Debug-Engine untersuchen und steuern. Sie lässt sich verwenden, wenn Tests Objekte zur Laufzeit finden, Eingaben einspeisen, auf einen sichtbaren Zustand warten oder das gerenderte Ergebnis aufnehmen müssen.

Weitere Einzelheiten findest du im [Handbuch zum Engine-Dienst](/manuals/engine-service/#automation-bridge-extension).

Das folgende Beispiel verwendet die Struktur der Python-Hilfsfunktionen von [Automation Bridge](https://github.com/defold/extension-automation-bridge). Das Projekt muss eine kompatible Version der Debug-Erweiterung enthalten, ein Element mit der angegebenen Automatisierungs-ID zugänglich machen und den Anwendungszustand `screen` veröffentlichen:

```python
from automation_bridge import editor

project = editor.open_project(".")
game = project.build_and_run()

try:
    play = game.element(automation_id="play_button")
    game.click(play)
    game.wait_for_state("screen", "gameplay", timeout=5.0)
    screenshot = game.screenshot()
    print(screenshot.path)
finally:
    game.close_engine()
```

Von der Anwendung definierte Zustände und Automatisierungs-IDs verwenden die optionale, nur zum Debuggen verfügbare Lua-API von Automation Bridge, die das Projekt aktivieren und zugänglich machen muss. Eine feste Wartezeit ist anfällig für Unterschiede bei Rechnergeschwindigkeit und Frame-Timing; zeitlich begrenztes wiederholtes Abfragen eines definierten Zustands ist zuverlässiger.

Automation Bridge ist eine Erweiterung und kein Bestandteil der Kern-Engine. In ihrer [Python-API-Referenz](https://github.com/defold/extension-automation-bridge/tree/master/automation_bridge/automation-bridge-python) findest du die für die installierte Version geltenden Informationen zu Selektoren, Wartevorgängen, Zustand, Ereignissen, Bildschirmaufnahmen und Diagnose.

## Browsertests für HTML5 {#browser-tests-for-html5}

Der Editor kann über seinen derzeitigen Befehl `build-html5` einen HTML5-Build erstellen und bereitstellen, wie im [Handbuch zur HTTP-API des Editors](/manuals/editor-http-api/#building-html5) beschrieben. Bob kann auch ohne den Editor ein HTML5-Bundle erstellen.

Externe Werkzeuge zur Browserautomatisierung wie Playwright, Puppeteer, Selenium, WebdriverIO oder Cypress können:

* auf die Defold-Zeichenfläche und die Bereitschaft der Anwendung warten;
* Tastatur-, Maus- und emulierte Berührungseingaben senden;
* die Größe des Ansichtsbereichs ändern;
* Browserkonsolenausgaben und JavaScript-Fehler erfassen;
* Bildschirmaufnahmen erstellen und Artefakte vergleichen.

Eingaben, die an die Zeichenfläche gerichtet sind, werden über die normalen Eingabebindungen (input bindings) und `on_input()`-Callbacks des Projekts verarbeitet. Teste sowohl die Reaktion des Spiels als auch browserspezifische Integrationspunkte.

Der zuverlässigste Ansatz besteht darin, eine ausdrückliche JavaScript-Testbrücke in der angepassten `index.html` bereitzustellen. Auf der Defold-Seite können HTML5-Builds mit `html5.run()` JavaScript ausführen, was die Kommunikation mit einer solchen Brücke auf der Browserseite ermöglicht. Verwende für Befehle, die von JavaScript zurück an Defold gelangen, eine eigene Brücke zwischen JavaScript und Engine.

Begrenze die Ausführung von Browsertests. Unterscheide im Abschlussbericht zwischen einem Fehler beim Laden der Seite, einer fehlenden Zeichenfläche, einem JavaScript-Fehler, einer Zeitüberschreitung des Tests und einer fehlgeschlagenen Assertion im Spiel.

## Editorvorschauen und Bildschirmaufnahmen zur Laufzeit für die visuelle Prüfung {#editor-previews-and-runtime-screenshots}

Du kannst Bildschirmaufnahmen von Ressourcendateien in der standardmäßigen Szenenansicht des geöffneten Editors oder in einem Spiel zur Laufzeit erstellen.

| Methode | Zweck |
| --- | --- |
| [Editorvorschau](/manuals/editor-http-api/#rendering-scene-previews) | Layout geladener Ressourcen, etwa eines Levels oder einer GUI, Atlaszusammenstellung, Prüfung von Kachelkarten (tile maps), statischer Szenenaufbau, Korrektheit von Editor-Rendering und Shadern oder Erstellung von Miniaturbildern für die Dokumentation |
| [Bildschirmaufnahme zur Laufzeit](/manuals/engine-service) | Der gerenderte Zustand eines laufenden Builds in einem kontrollierten Szenario |

Du kannst Bildvergleiche beispielsweise für Regressionstests verwenden. Speichere das Differenzbild und die Vergleichsmetriken, wenn eine Prüfung fehlschlägt.

Ein multimodales Modell kann bei der visuellen Prüfung semantische Bedingungen bewerten, die sich ansonsten schwer ausdrücken lassen, etwa abgeschnittenen Text, überlappende Bedienelemente, unklare Auswahlzustände oder Inhalte außerhalb eines sicheren Bereichs. Es wird empfohlen, diese Bewertung als zusätzliches Signal mit ausdrücklichen Kriterien zu behandeln, jedoch nicht als Ersatz für deterministische Logikprüfungen oder Bildvergleiche.

## Tests ohne grafische Oberfläche und CI {#headless-tests-and-ci}

Verwende das Kommandozeilenwerkzeug Bob the builder für CI unabhängig vom Editor.

Du kannst damit Abhängigkeiten auflösen, ein Spiel, ein Archiv oder ein eigenständiges Bundle erstellen und einen JSON-Bericht erzeugen:

```sh
mkdir -p build/reports

java -jar bob.jar \
  --root . \
  --archive \
  --build-report-json build/reports/build-report.json \
  resolve build
```

Erstelle ein Test-Bundle ohne grafische Oberfläche mit eigenen Einstellungen:

```sh
java -jar bob.jar \
  --root . \
  --settings test/test.settings \
  --platform x86_64-linux \
  --variant headless \
  --archive \
  --bundle-output build/test-bundle \
  resolve build bundle
```

Führe die resultierende ausführbare Datei mit einer für die Plattform geeigneten Prozesssteuerung aus. Erfasse ihren Beendigungsstatus und ihre Protokolle, erzwinge ein Zeitlimit und verlange das strukturierte Abschlussereignis der Testsuite.

Das [Bob-Handbuch](/manuals/bob) beschreibt Plattformen, Einstellungsdateien, Bundles, Caches, native Erweiterungen und Build-Berichte.

## Fehlerberichte und Artefakte {#failure-reports-and-artifacts}

Gute Testergebnisse sollten genügend Nachweise aufbewahren, um einen Fehler nachzustellen und zu diagnostizieren:

* Testname, Lauf-ID und Einzelheiten der Assertion;
* verstrichene Zeit und klassifiziertes Ergebnis;
* vollständiges Konsolen- oder Prozessprotokoll;
* Defold-Version, Zielplattform und relevante Konfiguration;
* Build-Bericht von Bob und Beendigungsstatus des Prozesses;
* Laufzeitzustand oder Momentaufnahme der Szene, sofern verfügbar;
* Bildschirmaufnahmen, Abweichungen von Referenzbildern, Aufzeichnungen oder Browser-Traces;
* Pfade oder Links zu allen erzeugten Artefakten.

Dasselbe Format sollte von einem Entwickler, einem lokalen Skript, einem CI-Dienst oder einem [KI-Programmieragenten](/manuals/ai-agents) genutzt werden können. So bleibt die Überprüfung deterministisch, auch wenn Diagnose oder Fehlerbehebung delegiert werden.
