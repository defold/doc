---
title: Richtlinien für Portierung und Veröffentlichung
brief: Dieses Handbuch beschreibt einige Aspekte, die du bei der Portierung eines Spiels auf eine neue Plattform oder bei der ersten Veröffentlichung deines Spiels berücksichtigen solltest.
---

# Richtlinien für Portierung und Veröffentlichung {#porting-and-release-guidelines}

Diese Seite enthält einen hilfreichen Leitfaden und eine Checkliste mit Aspekten, die du bei der Veröffentlichung eines Spiels oder bei der Portierung auf eine neue Plattform berücksichtigen solltest.

Ein Defold-Spiel auf eine neue Plattform zu portieren oder erstmals zu veröffentlichen, ist normalerweise ein unkomplizierter Vorgang. Theoretisch reicht es aus, die entsprechenden Abschnitte in der Datei *game.project* zu konfigurieren. Um jede Plattform bestmöglich zu nutzen, empfiehlt es sich jedoch, das Spiel an ihre jeweiligen Besonderheiten anzupassen.


## Eingabe {#input}
Passe das Spiel an die Eingabemethoden der Plattform an. Ziehe in Betracht, Unterstützung für [Gamepads](/manuals/input-gamepads) hinzuzufügen, sofern die Plattform sie unterstützt! Stelle außerdem sicher, dass das Spiel ein Pausenmenü bietet - wenn sich die Verbindung zu einem Controller plötzlich trennt, sollte das Spiel pausiert werden!

## Lokalisierung {#localization}
Übersetze sämtliche Texte im Spiel. Für eine Veröffentlichung in Europa sowie Nord- und Südamerika solltest du eine Übersetzung zumindest in die EFIGS-Sprachen (Englisch, Französisch, Italienisch, Deutsch und Spanisch) in Betracht ziehen. Stelle sicher, dass du im Spiel (über das Pausenmenü) leicht zwischen verschiedenen Sprachen wechseln kannst.

::: important
Nur iOS - Stelle sicher, dass du [Localizations](/manuals/project-settings/#localizations) in `game.project` angibst, da `sys.get_info()` niemals eine Sprache zurückgibt, die nicht in dieser Liste enthalten ist.
:::

Übersetze den Text auf der Store-Seite, denn das wirkt sich positiv auf die Verkaufszahlen aus! Einige Plattformen verlangen, dass der Text auf der Store-Seite in die Sprache jedes Landes übersetzt wird, in dem das Spiel verfügbar ist.

## Materialien für den Store {#store-materials}

### App-Symbol {#app-icon}
Sorge dafür, dass sich dein Spiel von der Konkurrenz abhebt. Das Symbol ist oft dein erster Kontaktpunkt mit potenziellen Spielern. Es sollte auf einer Seite voller Spielsymbole leicht zu finden sein.

### Banner und Bilder für den Store {#store-banners-and-images}
Verwende eindrucksvolle und spannende Grafiken für dein Spiel. Es lohnt sich wahrscheinlich, etwas Geld in die Zusammenarbeit mit einem Grafiker zu investieren, um Grafiken zu erstellen, die Spieler ansprechen.


## Spielstände {#save-games}

### Spielstände auf Desktop- und Mobilgeräten sowie im Web {#save-games-on-desktop-mobile-and-web}
Spielstände und andere gespeicherte Zustandsdaten können mit der Defold-API-Funktion `sys.save(filename, data)` gespeichert und mit `sys.load(filename)` geladen werden. Mit `sys.get_save_file(application_id, name)` kannst du einen Pfad zu einem betriebssystemspezifischen Speicherort für Dateien ermitteln, der sich üblicherweise im Benutzerordner des angemeldeten Benutzers befindet.

### Spielstände auf Konsolen {#save-games-on-console}
Die Verwendung von `sys.get_save_file()` und `sys.save()` funktioniert auf den meisten Plattformen gut, für Konsolen wird jedoch ein anderer Ansatz empfohlen. Konsolenplattformen ordnen üblicherweise jedem verbundenen Controller einen Benutzer zu. Entsprechend sollten Spielstände, Erfolge und andere Funktionen dem jeweiligen Benutzer zugeordnet werden.

Die Gamepad-Eingabeereignisse enthalten eine Benutzer-ID, mit der die Aktionen eines Controllers einem Benutzer auf der Konsole zugeordnet werden können.

Die Konsolenplattformen und ihre nativen Erweiterungen stellen plattformspezifische API-Funktionen bereit, um Daten für einen bestimmten Benutzer zu speichern und zu laden. Verwende diese APIs beim Speichern und Laden auf Konsolen.

APIs von Konsolenplattformen für Dateivorgänge sind üblicherweise asynchron. Wenn du ein plattformübergreifendes Spiel entwickelst, das auch für Konsolen vorgesehen ist, empfiehlt es sich, das Spiel so zu gestalten, dass alle Dateivorgänge unabhängig von der Plattform asynchron sind. Beispiel:

```lua
local function save_game(data, user_id, cb)
	if console then
		local filename = "savegame"
		consoleapi.save(user_id, filename, data, cb)
	else
		local filename = sys.get_save_file("mygame", "savegame" .. user_id)
		local success = sys.save(filename, data)
		cb(success)
	end
end
```


## Build-Artefakte {#build-artifacts}

Stelle sicher, dass du für jede veröffentlichte Version [Debugsymbole erzeugst](/manuals/debugging-native-code/#symbolicate-a-callstack), damit du Abstürze debuggen kannst. Bewahre diese zusammen mit dem Anwendungs-Bundle auf.

## Optimierung der Anwendung {#application-optimizations}

Im [Handbuch zur Optimierung](/manuals/optimization) erfährst du, wie du deine Anwendung hinsichtlich Leistung, Größe, Speicherverbrauch und Akkuverbrauch optimieren kannst.



## Leistung {#performance}
Teste immer auf der Zielhardware! Prüfe die Leistung des Spiels und optimiere sie bei Bedarf. Verwende den [Profiler](/manuals/profiling), um Engpässe im Code zu finden.


## Bildschirmauflösung und Bildwiederholfrequenz {#screen-resolution-and-refresh-rate}
Für Plattformen mit fester Ausrichtung und Bildschirmauflösung: Prüfe, ob das Spiel mit der Bildschirmauflösung und dem Seitenverhältnis der Zielplattform funktioniert. Für Plattformen mit variabler Bildschirmauflösung und variablem Seitenverhältnis: Prüfe, ob das Spiel mit verschiedenen Bildschirmauflösungen und Seitenverhältnissen funktioniert. Berücksichtige dabei, welche Art von [Ansichtsprojektion](/manuals/render/#default-view-projection) im Render-Skript und in der Kamera verwendet wird.

Lege für mobile Plattformen entweder die Bildschirmausrichtung in *game.project* fest oder stelle sicher, dass das Spiel sowohl im Quer- als auch im Hochformat funktioniert.

* **Bildschirmgrößen** - Sieht alles auf einem Bildschirm gut aus, der größer oder kleiner ist als durch die Standardbreite und -höhe in *game.project* vorgegeben?
  * Dabei spielen die im Render-Skript verwendete Projektion und die in der GUI verwendeten Layouts eine Rolle.
* **Seitenverhältnisse** - Sieht alles auf einem Bildschirm gut aus, dessen Seitenverhältnis vom Standardseitenverhältnis abweicht, das sich aus der Breite und Höhe in *game.project* ergibt?
  * Dabei spielen die im Render-Skript verwendete Projektion und die in der GUI verwendeten Layouts eine Rolle.
* **Bildwiederholfrequenz** - Läuft das Spiel gut auf einem Bildschirm mit einer höheren Bildwiederholfrequenz als 60 Hz?
  * Die Einstellungen vsync und swap interval im Abschnitt Display von *game.project* 


## Mobiltelefone mit Notch oder Hole-Punch-Kamera {#mobile-phones-and-notch-and-hole-punch-cameras}
Es ist immer üblicher geworden, eine kleine Aussparung im Bildschirm für die Frontkamera und Sensoren zu verwenden (auch als Notch oder Hole-Punch-Kamera bekannt). Achte bei der Portierung eines Spiels auf Mobilgeräte darauf, dass wichtige Informationen innerhalb des sicheren Bereichs (safe area) der Plattform bleiben.

Defold unterstützt den sicheren Bereich auf Android und iOS von Haus aus. Lege `gui.safe_area_mode` in *game.project* fest, um zu steuern, welche gegenüberliegenden Randabstände des sicheren Bereichs die GUI-Anpassung beeinflussen. `none` ist der Standardwert und ignoriert die Randabstände; `long` wendet im Querformat die linken/rechten und im Hochformat die oberen/unteren Randabstände an; `short` wendet das jeweils andere Paar an; und `both` berücksichtigt alle vier Ränder. Ein GUI-Skript kann den projektweiten Modus für seine Szene mit [`gui.set_safe_area_mode()`](/ref/gui/#gui.set_safe_area_mode) überschreiben. Für eigene GUI- oder Rendering-Logik gibt [`window.get_safe_area()`](/ref/window/#window.get_safe_area) das sichere Rechteck und die einzelnen Randabstände zurück. Plattformen ohne integrierte Randabstände für den sicheren Bereich geben das gesamte Fenster und Randabstände von null zurück.

Die [Safe Area-Erweiterung](/extension-safearea) bleibt eine Alternative für ältere Projekte oder Arbeitsabläufe, die ein Verhalten benötigen, das über die integrierten APIs hinausgeht; für die normale Behandlung des sicheren Bereichs auf Android und iOS ist sie nicht erforderlich.

### Reservierte Bildschirmbereiche {#reserved-screen-areas}

[`window.get_reserved_areas()`](/ref/window/#window.get_reserved_areas) meldet einzelne Bereiche, die das Spielfenster verdecken, etwa Kameraaussparungen und die Dynamic Island. Verwende diese Rechtecke, um Inhalte um einzelne Hindernisse herum zu platzieren. Verwende `window.get_safe_area()`, wenn du ein einzelnes sicheres Layoutrechteck und dessen Randabstände benötigst.

Das Ergebnis ist ein Array von Tabellen mit den Feldern `x`, `y`, `width` und `height`. Jedes Rechteck wird auf das Spielfenster beschnitten. Der Ursprung liegt unten links: `x` ist der linke und `y` der untere Rand, in Fensterpixeln entsprechend [`window.get_size()`](/ref/window/#window.get_size). Diese Koordinaten sind unabhängig von GUI-Anpassung und logischer Auflösung in *game.project*; berücksichtige daher deine GUI-Transformationen, bevor du sie als Knotenpositionen verwendest.

Die Plattformunterstützung ist:

- **iOS 27.1 und neuer:** von UIKit gemeldete aktive Verdeckungen einschließlich seiner Interaktionsränder.
- **Android 9 (API-Level 28) und neuer:** Rechtecke von Bildschirmaussparungen.

Die Funktion gibt auf nicht unterstützten Plattformen und Betriebssystemversionen oder bei fehlenden gemeldeten Hindernissen im Fenster eine leere Tabelle zurück. Eine leere Tabelle bedeutet nicht, dass das gesamte Fenster für wichtige Inhalte sicher ist: Falten, Systemleisten, Tastaturen und Gestenbereiche liegen außerhalb dieser API. Verwende `window.get_safe_area()` für das sichere Rechteck der Plattform.

### Bereiche nach Fensterereignissen aktualisieren {#refreshing-areas-after-window-events}

Frage reservierte Bereiche bei der Initialisierung und erneut bei jedem Callback für [`window.WINDOW_EVENT_RESIZED`](/ref/window/#window.WINDOW_EVENT_RESIZED) ab. Nach der ersten Abfrage lösen auf unterstützten Plattformen auch Änderungen an der Geometrie reservierter Bereiche dieses Ereignis aus, selbst bei unveränderter Fenstergröße. Jede zurückgegebene Tabelle ist eine Momentaufnahme; gespeicherte Tabellen werden nicht automatisch aktualisiert.

Unter iOS wird dieses Ereignis auch nach Orientierungswechseln und Änderungen der sicheren Randabstände gesendet. Eine Drehung um 180° im Querformat kann eine Kameraaussparung oder die Dynamic Island auf die andere Seite verschieben, obwohl Fensterabmessungen und sichere Randabstände gleich bleiben. Aktualisiere deine Geometrie beim Ereignis auch dann, wenn `data.width` und `data.height` ihren vorherigen Werten entsprechen.

Das folgende Skript hält beide Geometriemengen aktuell:

```lua
local function refresh_screen_areas(self)
    self.safe_area = window.get_safe_area()
    self.reserved_areas = window.get_reserved_areas()
    -- Update your UI using the new safe rectangle and reserved areas.
end

local function on_window_event(self, event, data)
    if event == window.WINDOW_EVENT_RESIZED then
        -- Refresh even when the width and height have not changed.
        refresh_screen_areas(self)
    end
end

function init(self)
    refresh_screen_areas(self)
    window.set_listener(on_window_event)
end

function final(self)
    window.set_listener(nil)
end
```

Es kann immer nur ein Fensterereignis-Listener registriert sein. Wenn dein Spiel bereits einen hat, ergänze diese Aktualisierungslogik dort. Durch Ersetzen des gespeicherten Arrays bei jeder Aktualisierung werden auch veraltete Rechtecke entfernt, wenn das Ergebnis leer wird.


## Plattformspezifische Richtlinien {#platform-specific-guidelines}

### Android
Bewahre deinen [Schlüsselspeicher](/manuals/android/#creating-a-keystore) an einem sicheren Ort auf, damit du dein Spiel aktualisieren kannst.


### Konsolen {#consoles}
Bewahre das vollständige Bundle jeder Version auf. Du benötigst diese Dateien, wenn du einen Patch für das Spiel erstellen möchtest.


### Nintendo Switch
Integriere plattformspezifischen Code - Für Nintendo Switch gibt es eine separate Erweiterung mit einigen Hilfsfunktionen, beispielsweise für die Benutzerauswahl.

Defold für Nintendo Switch verwendet Vulkan als Grafik-Backend - Teste das Spiel unbedingt mit dem [Vulkan-Grafik-Backend](https://github.com/defold/extension-vulkan).


### PlayStation®4
Integriere plattformspezifischen Code - Für PlayStation®4 gibt es eine separate Erweiterung mit einigen Hilfsfunktionen, beispielsweise für die Benutzerauswahl.


### HTML5
Webspiele auf Mobiltelefonen werden immer beliebter - Versuche, das Spiel auch in einem mobilen Browser gut zum Laufen zu bringen! Bedenke außerdem, dass von Webspielen schnelle Ladezeiten erwartet werden! - Optimiere daher unbedingt die Größe des Spiels. Berücksichtige auch das Ladeerlebnis insgesamt, um nicht unnötig Spieler zu verlieren.

Im Jahr 2018 führten Browser eine Richtlinie für die automatische Tonwiedergabe ein, die Spiele und andere Webinhalte daran hindert, Töne abzuspielen, bevor eine Benutzerinteraktion (Berührung, Schaltfläche, Gamepad usw.) stattgefunden hat. Berücksichtige dies bei der Portierung auf HTML5 und starte die Wiedergabe von Tönen und Musik erst bei der ersten Benutzerinteraktion. Versuche, Töne vor einer Benutzerinteraktion abzuspielen, werden als Fehler in der Entwicklerkonsole des Browsers protokolliert, beeinträchtigen das Spiel jedoch nicht.

Achte außerdem darauf, alle gerade abgespielten Töne zu pausieren, wenn das Spiel Werbung anzeigt.
