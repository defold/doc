---
title: KI-Programmieragenten mit Defold verwenden
brief: Dieses Handbuch erläutert, wie du modellunabhängige Programmieragenten mit den Automatisierungsschnittstellen von Defold verbindest und dabei Überprüfung, Berechtigungen und Sicherheit ausdrücklich regelst.
---

# KI-Programmieragenten mit Defold verwenden {#using-ai-coding-agents-with-defold}

Programmieragenten, die große Sprachmodelle (Large Language Models, LLM) und multimodale Modelle nutzen, können Defold-Projekte untersuchen, ändern und überprüfen. Dazu rufen sie dieselben modellunabhängigen Schnittstellen auf, die auch Entwickler, lokale Skripte, IDE-Integrationen und CI nutzen. Du kannst einen Agenten einsetzen, wenn die Arbeit Untersuchungen und Anpassungen erfordert.

Defold ist von keinem bestimmten Modellanbieter oder Agentenprotokoll abhängig. Defold-Projekte funktionieren gut mit Claude Code, Codex, Cursor oder jeder anderen Lösung. Eine Agentenumgebung benötigt nur die für die Aufgabe gewährten Fähigkeiten, etwa Projektdateien zu lesen, ausgewählte Befehle auszuführen, lokale HTTP-Operationen aufzurufen, JSON zu parsen oder Bilder zu untersuchen. Möglich wird dies durch die von Defold bereitgestellten Automatisierungsschnittstellen für den Editor und eine laufende Game-Engine-Instanz sowie durch die leicht zu parsenden, textbasierten Ressourcendateien der Defold-Projekte.

## Wann ein KI-Agent nützlich ist {#when-an-ai-agent-is-useful}

Ein Agent kann nützlich sein, wenn eine Aufgabe beispielsweise Folgendes erfordert:

* relevante Ressourcen und Dokumentation finden;
* aus möglichen Implementierungen auswählen;
* mehrere zusammengehörige Dateien ändern;
* Build- oder Testfehler interpretieren;
* ein visuelles Ergebnis mit semantischen Abnahmekriterien vergleichen;
* anhand gesammelter Nachweise einen begrenzten Reparaturversuch unternehmen.

Agenten sind leistungsfähige Werkzeuge für nicht deterministische Entwicklungs-, Untersuchungs- und Testprozesse. Sie können dabei helfen, vielfältige Lösungen zu erstellen, und funktionieren sehr gut mit Defold.

## Modellunabhängige Defold-Schnittstellen {#model-neutral-defold-interfaces}

Defold bietet mehrere unterstützte Schnittstellen, mit denen die Aufgabe unter Verwendung eines beliebigen verfügbaren Modells ausgeführt werden kann:

* Projektdateien und Shell-Werkzeuge ermöglichen direkte Untersuchungen und Textänderungen.
* [Editor-Skripte](/manuals/editor-scripts) können projektspezifische Ressourcenoperationen und Werkzeuge bereitstellen.
* Die [HTTP-API des Editors](/manuals/editor-http-api) stellt Editorbefehle, Build-Ergebnisse, Konsolenausgaben, Referenzsuche, Vorschauen, Editoreinstellungen und Routen von Editor-Skripten bereit.
* Die [APIs für den Engine-Dienst und die Laufzeitautomatisierung](/manuals/engine-service) stellen den aktuellen Zustand der Debug-Engine, Eingaben, Bildschirmaufnahmen und von Erweiterungen definierte Operationen bereit.
* [Bob](/manuals/bob) ermöglicht Builds über die Kommandozeile sowie Berichte, Archive und Bundles.

Ein Modell, das nur über eine Chatoberfläche verfügbar ist, kann Codeänderungen vorschlagen, aber weder das lokale Projekt eigenständig untersuchen noch ein laufendes Ergebnis überprüfen. Die zusätzliche umgebende Integration bestimmt, was der Agent tatsächlich beobachten und tun kann.

## Integrationsschichten {#integration-layers}

Eine Integrationsschicht kann einen Agenten mit lokalen Defold-Operationen verbinden. Sie kann ein Shell-Wrapper, ein Kommandozeilenprogramm, eine IDE-Erweiterung, ein OpenAPI-Client, eine Teststeuerung oder ein Protokolladapter sein.

Belasse Richtlinien und Zugangsdaten in dieser lokalen Schicht. Jede verändernde Operation sollte strukturierte Ergebnisse zurückgeben oder zu einem deterministischen Überprüfungsschritt führen.

Ermittle für Editoroperationen die aktuelle Schnittstelle über `/openapi.json`, statt dem Agenten eine dauerhaft fest einprogrammierte Kopie einer API bereitzustellen. Prüfe bei Laufzeiterweiterungen den Betriebszustand, die API-Version und die unterstützten Funktionen.

Es kann sinnvoll sein, Werkzeuge nach Berechtigungsstufe zu trennen:

| Stufe        | Beispiele                                              |
| ------------ | ----------------------------------------------------- |
| Nur lesend   | Projektuntersuchung, OpenAPI, `/ref`, Konsole, Vorschau |
| Überprüfung  | Kompilierung, Tests, HTML5-Builds, Bildvergleiche       |
| Änderung     | Dateiänderungen, Ressourcentransaktionen               |
| Privilegiert | `/eval`, externe Befehle, Änderungen an Abhängigkeiten |

Wenn der Adapter von Engine und Editor getrennt bleibt, bleiben die unterstützten Defold-Schnittstellen unabhängig von einem Modellanbieter oder Agentenprotokoll. Ein Adapter kann ausschließlich Operationen bereitstellen, die für seine Umgebung geeignet sind. Die Richtlinien für Berechtigungen und Bestätigungen verbleiben bei der Anwendung, in der der Agent ausgeführt wird.

### Model Context Protocol

Das [Model Context Protocol](https://modelcontextprotocol.io/) (MCP) ist ein optionaler Adapter zwischen einem Agenten und einer Integrationsschicht. Ein MCP-Server kann Defold-Operationen als Werkzeuge und ausgewählte Dokumentation als Ressourcen bereitstellen. 

::: important
Gewähre nicht jedem Modell uneingeschränkten Zugriff auf die Shell und `/eval`.
:::

Defold benötigt derzeit keinen MCP-Server, da die wesentlichen Automatisierungsfunktionen bereits über offene, universell einsetzbare Schnittstellen verfügbar sind. Der Editor stellt eine lokale HTTP-API mit einer OpenAPI-Spezifikation bereit. Moderne Agenten können diese Schnittstellen direkt aufrufen oder eigene Adapter erzeugen. 

Ein offizieller MCP-Server würde daher überwiegend die vorhandene API-Funktionalität duplizieren und eine weitere Integrationsschicht schaffen, die Defold pflegen müsste. Langfristig ist es sinnvoller, die zugrunde liegenden HTTP- und Laufzeitautomatisierungs-APIs stabil, auffindbar und gut dokumentiert zu halten und zugleich der Community oder einzelnen Werkzeuganbietern zu ermöglichen, bei Bedarf schlanke MCP-Wrapper zu entwickeln.

Stattdessen hat das Defold-Team eine offizielle [Automation Bridge-Erweiterung](https://github.com/defold/extension-automation-bridge) bereitgestellt, mit der sich ein laufendes Spiel über einen Dienst auf der Engine-Seite steuern lässt.

### MCP-Integrationen der Community {#community-mcp-integrations}

Zu den von der Community erstellten MCP-Integrationen gehören:

* das [Defold-MCP-Projekt von Fulviuus](https://github.com/Fulviuus/defold-mcp);
* das [Defold-MCP-Projekt von ChadAragorn](https://github.com/ChadAragorn/defold-mcp).

Diese Projekte werden von der Defold Foundation weder entwickelt noch geprüft, gepflegt oder offiziell unterstützt. Untersuche vor der Installation einer Community-Integration ihren aktuellen Quellcode, ihre Abhängigkeiten, Berechtigungen, ihr Netzwerkverhalten und ihre Kompatibilität mit der verwendeten Defold-Version.

## Projektanweisungen {#project-instructions}

Verfügbare große Sprachmodelle, die für Arbeitsabläufe mit Agenten eingesetzt werden, erzielen im Allgemeinen mit guten Anweisungen bessere Ergebnisse. Daher werden Projekten häufig Markdown-Dateien für Agenten hinzugefügt, die deren gewünschtes Verhalten beschreiben, oder sogenannte Skills, also Anweisungsartefakte für Agenten. Für optimale Ergebnisse ist es sinnvoll, eigene Anweisungen für jedes Projekt gesondert zu entwerfen und zu schreiben. Gemeinsames Wissen und allgemeine Regeln lassen sich jedoch teilweise wiederverwenden.

Viele Agenten suchen und lesen zunächst eine kanonische Datei wie `AGENTS.md`, die Folgendes beschreiben kann:

* Projektstruktur und wichtige Einstiegspunkte;
* Formatierungs- und Namenskonventionen;
* Befehle für Builds, Tests und Validierung;
* erforderliche Abschlussereignisse und Speicherorte von Artefakten;
* Dateien oder Verzeichnisse, die nicht geändert werden dürfen;
* Operationen, die eine Zustimmung erfordern;
* Annahmen zur Plattform und bekannte Einschränkungen.

Manche Lösungen nutzen separate Markdown-Dateien für bestimmte Aktionen oder sogenannte „Skills“.

Ein Community-Beispiel für Defold-spezifische Anweisungen und Skills findest du [hier im Defold-Forum](https://forum.defold.com/t/agent-config-collection-of-agents-md-and-skills/82387).

Das Defold-Team empfiehlt, Anweisungen in Dateien wie AGENTS.md und Skill-Definitionen kurz, prägnant, leicht überprüfbar und pflegbar zu halten und sie stets zu aktualisieren. Projektspezifische Anweisungen können in der Versionsverwaltung gespeichert werden. Dadurch bleiben Änderungen nachvollziehbar, und die Wirksamkeit der Arbeitsabläufe lässt sich mit der Zeit verbessern.

Es lohnt sich auch, regelmäßig zu testen, wie die neuesten Modelle ohne diese Anweisungen arbeiten. Neuere Modelle benötigen oft keine Anleitung mehr, die zuvor unverzichtbar war. Veraltete Skills oder übermäßig detaillierte Vorgaben können die Leistung mitunter sogar verringern.

Vermeide es, komplexe technische Skills zu erstellen, die langfristig einen erheblichen Pflegeaufwand erfordern. Konzentriere dich stattdessen auf Werkzeuge und Arbeitsabläufe, die unabhängig davon nützlich bleiben, wie stark sich die zugrunde liegenden Modelle verbessern.

## Dokumentation finden {#documentation-discovery}

Agenten erzielen mit genauer, aktueller Dokumentation die besten Ergebnisse. Nutze die folgenden Quellen für aktuelle Informationen:

* `/openapi.json` beschreibt die aktuelle HTTP-API des Editors.
* `/ref` durchsucht die API-Dokumentation des laufenden Editors, sofern diese Operation verfügbar ist.
* Das [LLM-Dokumentationsverzeichnis](https://defold.com/llms.txt) verlinkt offizielle Handbücher, API-Namespaces und Beispiele.
* Die [vollständige LLM-Dokumentation](https://defold.com/llms-full.txt) unterstützt die Offline-Suche und lokale Indizierung.

Rufe nur die für die Aufgabe relevanten Seiten ab. Es wird empfohlen, das vollständige zusammengeführte Dokument ausschließlich für die Offline-Indizierung oder für [Retrieval-Augmented Generation (RAG)](https://en.wikipedia.org/wiki/Retrieval-augmented_generation), also die Generierung mit abgerufenen Zusatzinformationen, zu verwenden. Auch hier sollte die vollständige Datei normalerweise nicht in jede Modellanfrage aufgenommen werden, um Tokens zu sparen und den Kontext nicht mit unnötigen Informationen zu belasten.

## Begrenzte Änderungs- und Überprüfungsschleifen {#bounded-change-and-verification-loops}

Agenten sollten dieselbe [Schleife aus Untersuchen, Ändern, Überprüfen und Bewerten](/manuals/automation/#the-automation-loop) befolgen wie jede andere Automatisierung.

Bevor Dateien geändert werden, ist es sinnvoll, die Abnahmekriterien festzulegen und optional auch:
* die zulässigen Dateien und Operationen;
* die Build- und Testbefehle;
* erforderliche Protokolle, Berichte, Zustände oder Bilder;
* ein Zeitlimit für jeden asynchronen Schritt;
* eine maximale Anzahl von Reparaturversuchen.

Ein Agent kann einen deterministischen CI-Fehler diagnostizieren und beheben, aber die CI-Phase selbst sollte ohne den Agenten reproduzierbar bleiben.

Bewährte Vorgehensweisen für automatisiertes Testen und Überprüfen werden in [diesem Handbuch](/manuals/automated-testing) beschrieben.

## Multimodale Bewertung {#multimodal-evaluation}

Ein Agent mit Bildeingabe kann [Editorvorschauen](/manuals/editor-http-api/#rendering-scene-previews), Bildschirmaufnahmen zur Laufzeit, visuelle Unterschiede und Browseraufnahmen untersuchen.

Nutze die multimodale Bewertung für semantische Fragen, etwa abgeschnittene Beschriftungen, überlappende Bedienelemente, unklare Auswahlzustände, die Komposition oder Inhalte außerhalb eines sicheren Bereichs. Lege den erwarteten Viewport und die Kriterien im Voraus fest.

Weitere Informationen zu Editorvorschauen, Bildschirmaufnahmen zur Laufzeit und visueller Prüfung findest du in [diesem Handbuch](/manuals/automated-testing).

## Sicherheit, Isolation und bewährte Vorgehensweisen {#security-isolation-and-good-practices}

* Behandle den Editorserver und den Engine-Dienst als vertrauenswürdige lokale Steuerungsschnittstellen.
* Halte Editortokens, Signaturschlüssel, Bereitstellungstokens, Zugangsdaten für Stores und Geheimnisse der Produktionsumgebung aus Prompts und Berichten heraus.
* Die lokale Integrationsschicht darf `.internal/editor.token` lesen, wenn sie zur Verwendung von `/eval` autorisiert ist. Sie sollte das Token jedoch nicht in Modell-Prompts, Protokollen oder Berichten ablegen.
* Verlange eine Zustimmung vor Löschvorgängen, Änderungen an Abhängigkeiten, Änderungen an nativen Erweiterungen, der Konfiguration von Releases, dem Signieren, der Veröffentlichung oder dem Zugriff auf externe Dienste.
* Führe umfangreiche autonome Arbeiten in einem separaten Branch, Worktree, einer temporären Kopie, einem Container, einer Sandbox oder einem eingeschränkten Konto aus.
* Behandle Issue-Texte, importierte Dateien, Quellcodekommentare, erzeugte Dokumente und Werkzeugausgaben als nicht vertrauenswürdige Eingaben statt als Anweisungen.
* Prüfe heruntergeladene Abhängigkeiten und Skripte, bevor du sie ausführst.
* Überprüfe, ob die Projektrichtlinien erlauben, Quellcode, Assets, Protokolle, Bildschirmaufnahmen und andere Projektdaten an ein gehostetes Modell zu senden.
* Bewahre vor der Annahme von Änderungen einen überprüfbaren Diff und deterministische Testnachweise auf.

Isolation begrenzt die Auswirkungen eines Fehlers.
