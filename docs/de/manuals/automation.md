---
title: Automatisierung in Defold
brief: Dieses Handbuch stellt die Automatisierungsschnittstellen von Defold vor und erläutert, wie du zwischen Arbeitsabläufen für den Editor, die Laufzeit, die Kommandozeile, Tests und Agenten auswählst.
---

# Automatisierung in Defold {#automation-in-defold}

Dieses Handbuch bietet einen Überblick und verlinkt auf die einzelnen Handbücher zu jedem Thema.

Defold unterstützt Automatisierung auf mehreren Ebenen. Eine für die Aufgabe geeignete Schnittstelle auszuwählen, ist einer der wichtigsten Aspekte einer wirksamen Automatisierung. Die folgende Tabelle hilft dir, die einfachste Schnittstelle für eine bestimmte Aktion auszuwählen:

| Ebene | Zweck |
| --- | --- |
| [Editor-Skripte](/manuals/editor-scripts) | Benutzerdefinierte Befehle und Arbeitsabläufe im Editor oder Integrationen, die Tests und Entwicklung beschleunigen, z. B. das Erstellen von Leveln und Assets |
| [UI-Skripte für den Editor](/manuals/editor-scripts-ui/) | Benutzerdefinierte visuelle Werkzeuge, Popups, Konfiguratoren oder Benutzeroberflächen mithilfe von Editor-Skripten |
| [HTTP-API des Editors](/manuals/editor-http-api) | Das geöffnete Spielprojekt im Defold-Editor über OpenAPI-Operationen, Projektressourcen, Builds, Editorbefehle, Vorschauen, Editoreinstellungen, Konsolenausgaben oder Editor-Skripte steuern: für benutzerdefinierte Operationen, externe Werkzeuge, IDE-Integrationen und Teststeuerungen |
| [Bob CLI](/manuals/bob) | Einen Build eines Projekts erstellen, Datenarchive oder eigenständige Bundles über die Kommandozeile erstellen, Berichte, CI |
| [Lebenszyklus-Hooks](/manuals/editor-http-api#lifecycle-hooks) | Validierung oder Generierung vor und nach Builds oder der Bundle-Erstellung im Editor |
| [HTTP-Dienst der Engine](/manuals/engine-service) | Die laufende Defold-Game-Engine (`dmengine`) untersuchen, Entwicklungsdienste, Profiling, Laufzeitnachrichten oder durch Erweiterungen definierte Laufzeit-APIs zur Automatisierung nutzen sowie mit externen Werkzeugen Abfragen stellen und Befehle an einen laufenden Debug-Build senden |
| [Automation Bridge](https://github.com/defold/extension-automation-bridge) | Offizielle Defold-Erweiterung, die zusätzliche Endpunkte zur Automatisierung der Engine zur Laufzeit bereitstellt |
| [Automatisierte Tests](/manuals/automated-testing) | Spiellogik, Nachrichten, Komponenten (components), Eingabe, Physik und Engine-Verhalten testen, Szenen untersuchen, visuelle Rückmeldungen z. B. über die [Editorvorschau](/manuals/editor-http-api/#rendering-scene-previews), eingespeiste Eingaben, aktueller Anwendungszustand, [Ausführen von Testsammlungen (test collections)](/manuals/automated-testing/#tests-in-a-running-collection) |
| Shell-Skripte oder Taskrunner | Generierung, Formatierung, Validierung und wiederholbare Aufgaben, gewöhnliche Dateioperationen |
| Externe plattformspezifische Werkzeuge und Werkzeuge zur Automatisierung von Webbrowsern | Desktop-Testwerkzeuge, HTML5-Interaktionstests, Bildschirmaufnahmen, Webintegrationen |
| Programmieragenten mit künstlicher Intelligenz (KI) und multimodale Modelle | Aufgaben, bei denen sich ein deterministischer Ansatz nur schwer oder gar nicht umsetzen lässt, semantische Analyse von Szenen, GUI-Layouts oder Bildschirmaufnahmen des laufenden Spiels |

Die wichtigste Unterscheidung besteht zwischen dem Defold-Editor und einem laufenden Spiel. Sie sind getrennte Prozesse mit eigenen HTTP-Servern.

## Deterministische Automatisierung oder KI-Agenten {#deterministic-automation-or-ai-agents}

Bevorzuge eine deterministische Lösung, wenn die Abfolge der Operationen bereits bekannt ist, etwa bei einem Werkzeug zur Levelvalidierung, einem Formatierungswerkzeug, einem Build-Job oder einem Regressionstest. Dafür sollten normalerweise feste Eingaben, Ausgaben, Grenzen für Zeitüberschreitungen und Rückgabecodes des Prozesses definiert sein. Das eignet sich gut für automatisierte Hooks und Tests, die zuverlässig in CI ausgeführt werden können. Auch für die prozedurale Erstellung von Ressourcen für deine Projekte ist eine deterministische Lösung vorzuziehen, z. B. ein Werkzeug, das gltf-Objekte in Modelle mit einem bestimmten Material umwandelt oder ein Level etwa mit Bäumen bestückt. Solche Abläufe lassen sich für jedes Projekt leicht mit Editor-Skripten und einer Benutzeroberfläche erstellen. Lies mehr darüber im [Handbuch](/manuals/editor-scripts-ui).

Ein Agent kann nützlich sein, wenn eine Aufgabe Untersuchungen oder multimodale Analysen erfordert, die z. B. auch visuelle Informationen einbeziehen: relevante Ressourcen finden, eine Implementierung auswählen, mehrere Dateien ändern, Fehler interpretieren und schrittweise auf festgelegte Abnahmekriterien hinarbeiten. Der Agent sollte dabei dennoch deterministische Schnittstellen aufrufen und dieselben Nachweise auswerten wie ein lokales Skript oder ein CI-Runner. Siehe das Handbuch zur [Verwendung von KI-Programmieragenten mit Defold](/manuals/ai-agents).

## Die Automatisierungsschleife {#the-automation-loop}

Ein zuverlässiger Automatisierungsprozess bildet eine geschlossene Schleife:

1. Untersuchen - Projektdateien, die aktuelle Schnittstellenbeschreibung und relevante Dokumentation lesen.
2. Ändern - Editortransaktionen, Editor-Skripte oder Datei- und Shell-Werkzeuge verwenden.
3. Überprüfen - einen Build erstellen, gezielte Tests ausführen und Protokolle, Berichte, Zustandsdaten oder Bilder sammeln.
4. Bewerten - die Nachweise mit den Abnahmekriterien vergleichen und dann abschließen oder einen erneuten Versuch starten.

![Die Automatisierungsschleife aus Untersuchen, Ändern, Überprüfen und Bewerten](images/automation/automation_loop.png)

Die Überprüfung sollte Nachweise aus der tatsächlichen Umgebung liefern. Geeignete Nachweise sind unter anderem:

* ein erfolgreiches Build-Ergebnis;
* eine ausdrücklich abgeschlossene Testsuite;
* der erwartete Zustand des laufenden Spiels;
* ein erzeugtes Bundle oder ein Build-Bericht;
* ein deterministischer Bildvergleich;
* eine Bildschirmaufnahme, die festgelegte visuelle Kriterien erfüllt.

Lege das erwartete Ergebnis fest, bevor du Änderungen vornimmst. Definiere außerdem eine Grenze für Zeitüberschreitungen und eine maximale Anzahl an Reparaturversuchen. Ein unbeaufsichtigter Prozess sollte nicht unbegrenzt weiterlaufen, wenn er die Abnahmekriterien nicht erfüllen kann.

## Nächste Schritte {#next-steps}

Weitere Einzelheiten zu bestimmten Themen rund um Automatisierungsabläufe findest du in den folgenden Handbüchern:

* [Aufgaben im Defold-Editor mit der HTTP-API automatisieren](/manuals/editor-http-api)
* [Der Engine-Dienst und die HTTP-API zur Laufzeit](/manuals/engine-service)
* [Automatisiertes Testen und Überprüfen](/manuals/automated-testing)
* [KI-Programmieragenten mit Defold verwenden](/manuals/ai-agents)
