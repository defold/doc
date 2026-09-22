---
title: Handbuch zum Anwendungslebenszyklus in Defold
brief: Dieses Handbuch beschreibt den Lebenszyklus von Defold-Spielen und -Anwendungen im Detail.
---

# Anwendungslebenszyklus {#application-lifecycle}

Der Lebenszyklus einer Defold-Anwendung oder eines Defold-Spiels ist im Großen und Ganzen einfach. Die Engine durchläuft drei Ausführungsphasen: die Initialisierung, die Aktualisierungsschleife (in der Anwendungen und Spiele die meiste Zeit verbringen) und die Finalisierung.

::: sidenote
Dieses Handbuch bezieht sich auf Defold-Versionen ab 1.12.0. In Version 1.12.0 wurden Änderungen am Lebenszyklus und die neue Funktion `late_update()` eingeführt.
:::

![Übersicht des Lebenszyklus](images/application_lifecycle/application_lifecycle.png)

In vielen Fällen genügt ein grundlegendes Verständnis der internen Abläufe von Defold. Es können jedoch Sonderfälle auftreten, in denen die genaue Reihenfolge, in der Defold seine Aufgaben ausführt, entscheidend ist. Dieses Dokument beschreibt, wie die Engine eine Anwendung vom Start bis zum Ende ausführt.

Zu Beginn initialisiert die Anwendung alles, was für den Betrieb der Engine erforderlich ist. Sie lädt die als Hauptsammlung verwendete Sammlung (collection) und ruft [`init()`](/ref/go#init) für alle geladenen Komponenten (components) auf, die eine Lua-Funktion namens `init()` besitzen (Skriptkomponenten und GUI-Komponenten mit GUI-Skripten). So kannst du eigene Initialisierungsschritte ausführen.

Die Anwendung tritt dann in die Aktualisierungsschleife ein, in der sie den größten Teil ihrer Lebensdauer verbringt. In jedem Frame werden Spielobjekte (game objects) und die darin enthaltenen Komponenten aktualisiert. Alle [`update()`](/ref/go#update)-Funktionen in Skripten und GUI-Skripten werden aufgerufen. Während der Aktualisierungsschleife werden Nachrichten an ihre Empfänger zugestellt, Klänge abgespielt und sämtliche Grafiken gerendert.

Irgendwann endet der Lebenszyklus der Anwendung. Bevor die Anwendung beendet wird, verlässt die Engine die Aktualisierungsschleife und tritt in die Finalisierungsphase ein. Sie bereitet alle geladenen Spielobjekte auf das Löschen vor. Die [`final()`](/ref/go#final)-Funktionen aller Objektkomponenten werden aufgerufen, sodass du eigene Aufräumarbeiten ausführen kannst. Anschließend werden die Objekte gelöscht und die Hauptsammlung wird entladen.

Die Schritte des Durchlaufs [„Nachrichten zustellen“](#dispatching-messages) werden der Übersichtlichkeit halber in einem eigenen Diagramm am Ende dieses Handbuchs gezeigt. In den Diagrammen sind sie mit einem kleinen Symbol für einen „Briefumschlag mit Pfeil“ 📩 gekennzeichnet.

## Initialisierung {#initialization}

Hier beginnt dein Spiel; dies ist der erste Schritt seiner Ausführung. Er lässt sich in 3 Phasen unterteilen:

![Initialisierung](images/application_lifecycle/initialization.png)

### Vorinitialisierung {#preinitialization}

Während der Phase `Preinitialization` führt die Engine viele Schritte aus, bevor die Hauptsammlung, also die Startsammlung (bootstrap collection), geladen wird. Der Speicherprofiler, Sockets, Grafik, HID (Eingabegeräte), Audio, Physik und vieles mehr werden eingerichtet. Auch die Anwendungskonfiguration (*game.project*) wird geladen und eingerichtet.

![Vorinitialisierung](images/application_lifecycle/pre_init.png)

Der erste von dir steuerbare Einstiegspunkt ist am Ende der Engine-Initialisierung der Aufruf der Funktion `init()` des aktuellen Render-Skripts.

Danach wird die Hauptsammlung geladen und initialisiert.

### Initialisierung der Sammlung {#collection-init}

Während der Phase `Collection Init` wenden alle Spielobjekte in der Sammlung ihre Transformationen auf ihre untergeordneten Objekte an: Verschiebung (Änderung der Position), Drehung und Skalierung. Anschließend werden alle vorhandenen `init()`-Funktionen der Komponenten aufgerufen.

![Initialisierung der Sammlung](images/application_lifecycle/collection_init.png)

::: sidenote
Die Reihenfolge, in der die `init()`-Funktionen der Spielobjektkomponenten aufgerufen werden, ist nicht festgelegt. Du solltest nicht davon ausgehen, dass die Engine Objekte derselben Sammlung in einer bestimmten Reihenfolge initialisiert.
:::

### Phase nach der Aktualisierung während der Initialisierung {#post-update-in-initialization}

Die Engine führt dann einen vollständigen `Post Update`-Durchlauf aus – denselben Durchlauf, der später nach jedem Schritt der `Update Loop` ausgeführt wird. Er erfolgt am Ende der Initialisierung, weil dein `init()`-Code neue Nachrichten senden, Fabriken (factories) zum dynamischen Erzeugen neuer Objekte anweisen, Objekte zum Löschen vormerken und andere Aktionen ausführen kann.

![Phase nach der Aktualisierung](images/application_lifecycle/post_init.png)

Dieser Durchlauf stellt Nachrichten zu, erzeugt die Spielobjekte über Fabriken tatsächlich und löscht Objekte. Beachte, dass der `Post Update`-Durchlauf eine Sequenz zum „Zustellen von Nachrichten“ enthält, die sowohl wartende Nachrichten zustellt als auch Nachrichten an Sammlungs-Proxys (collection proxies) verarbeitet. Alle daraus folgenden Aktualisierungen der Proxys (Aktivieren, Deaktivieren, Initialisieren, Finalisieren, Laden und Vormerken zum Entladen) werden während dieser Schritte ausgeführt.

Es ist durchaus möglich, während `init()` einen [Sammlungs-Proxy](/manuals/collection-proxy) zu laden, sicherzustellen, dass alle darin enthaltenen Objekte initialisiert sind, und die Sammlung anschließend über den Proxy wieder zu entladen. All das kann geschehen, bevor die erste `update()`-Funktion einer Komponente aufgerufen wird, also bevor die Engine die Initialisierungsphase verlassen hat und in die Aktualisierungsschleife eingetreten ist:

```lua
function init(self)
    print("init()")
    msg.post("#collectionproxy", "load")
end

function update(self, dt)
    -- The proxy collection is unloaded before this code is reached.
    print("update()")
end

function on_message(self, message_id, message, sender)
    if message_id == hash("proxy_loaded") then
        print("proxy_loaded. Init, enable and then unload.")
        msg.post("#collectionproxy", "init")
        msg.post("#collectionproxy", "enable")
        msg.post("#collectionproxy", "unload")
        -- The proxy collection objects’ init() and final() functions
        -- are called before we reach this object’s update()
    end
end
```

## Aktualisierungsschleife {#update-loop}

Die `Update Loop` durchläuft einmal pro Frame eine bestimmte Sequenz. Diese Sequenz lässt sich in 5 Hauptphasen unterteilen:

![Aktualisierungsschleife](images/application_lifecycle/update_loop.png)

1. Eingabe (Verarbeitung und Behandlung)
2. Aktualisierung (einschließlich der Aktualisierungen mit festem Zeitschritt, der regulären und späten Aktualisierungen sowie der Aktualisierungen der Engine-Komponenten)
3. Aktualisierung des Renderings
4. Phase nach der Aktualisierung (Entladen von Sammlungs-Proxys, dynamisches Erzeugen und Löschen von Spielobjekten)
5. Rendern des Frames (die endgültige Grafik wird gerendert)

### Eingabephase {#input-phase}

Eingaben werden von verfügbaren Geräten gelesen, anhand der [Eingabebindungen (input bindings)](/manuals/input) zugeordnet und dann weitergeleitet. Jedes Spielobjekt, das den Eingabefokus erhalten hat, erhält Eingaben in den `on_input()`-Funktionen all seiner Komponenten. Bei einem Spielobjekt mit einer Skriptkomponente und einer GUI-Komponente mit GUI-Skript erhalten die `on_input()`-Funktionen beider Komponenten Eingaben – vorausgesetzt, sie sind definiert und haben den Eingabefokus erhalten.

![Eingabephase](images/application_lifecycle/input_phase.png)

Jedes Spielobjekt, das den Eingabefokus erhalten hat und Sammlungs-Proxy-Komponenten enthält, leitet Eingaben an die Komponenten innerhalb der vom Proxy geladenen Sammlung weiter. Dieser Vorgang setzt sich rekursiv über aktivierte Sammlungs-Proxys innerhalb aktivierter Sammlungs-Proxys fort.

### Aktualisierungsphase {#update-phase}

Die Phase `Update` ist Teil der `Update Loop`. Sie wird einmal für die Sammlung auf oberster Ebene gestartet und läuft dann rekursiv für jeden aktivierten Sammlungs-Proxy.

Innerhalb einer Sammlung verarbeitet Defold Callbacks nach Komponententyp: Die Engine durchläuft alle Instanzen eines Komponententyps, der die entsprechende Phase implementiert, ruft den Lua-Callback für jede Instanz auf, stellt die Nachrichten zu und geht dann zum nächsten Komponententyp über.

Die grundsätzliche Reihenfolge der Lua-Callback-Phasen von *Skriptkomponenten* ist:

1. `fixed_update()` – wird 0..N Mal pro Frame aufgerufen (bei Verwendung eines festen Zeitschritts)
2. `update()` – wird 1 Mal pro Frame aufgerufen
3. `late_update()` – wird 1 Mal pro Frame aufgerufen

![Aktualisierungsphase](images/application_lifecycle/update_phase.png)


Jede Spielobjektkomponente in der Hauptsammlung wird durchlaufen. Wenn eine dieser Komponenten ein Skript mit einer Funktion `fixed_update()`/`update()`/`late_update()` besitzt, wird diese aufgerufen. Ist die Komponente ein Sammlungs-Proxy, wird jede Komponente in der vom Proxy geladenen Sammlung rekursiv mit allen Schritten der Phase `Update` aktualisiert.

::: sidenote
Die Reihenfolge, in der die `update()`-Funktionen der Spielobjektkomponenten aufgerufen werden, ist nicht festgelegt. Du solltest nicht davon ausgehen, dass die Engine Objekte derselben Sammlung in einer bestimmten Reihenfolge aktualisiert. Dasselbe gilt für `fixed_update()` und `late_update()` (seit 1.12.0).
:::

#### Physik {#physics}

Bei Kollisionsobjektkomponenten werden Physiknachrichten (Kollisionen, Trigger, Antworten auf Strahlabfragen (raycasts) usw.) innerhalb des zugehörigen Spielobjekts an alle Komponenten zugestellt, die ein Skript mit der Funktion `on_message()` enthalten.

Wenn für die Physiksimulation ein [fester Zeitschritt](/manuals/physics/#physics-updates) verwendet wird, kann außerdem die Funktion `fixed_update()` in allen Skriptkomponenten aufgerufen werden. Diese Funktion ist in physikbasierten Spielen nützlich, wenn du Physikobjekte in regelmäßigen Abständen verändern möchtest, um eine stabile Physiksimulation zu erzielen.

#### Transformationen {#transforms}

Vor **jeder** Aktualisierung eines Komponententyps werden bei Bedarf die Transformationen aktualisiert, also mehrmals während der `Update Loop`. Dabei werden alle Bewegungen, Drehungen und Skalierungen der Spielobjekte auf jede Spielobjektkomponente und alle Komponenten untergeordneter Spielobjekte angewendet.

Am Ende der `Update Loop` werden die Transformationen bei Bedarf ein weiteres, abschließendes Mal aktualisiert.

#### Aktualisierungsphase der Engine (ohne Aktualisierungen mit festem Zeitschritt) {#engine-update-phase-no-fixed-updates}

Die folgenden Tabellen beschreiben die Aktualisierungsdurchläufe auf *Engine-Ebene*. Sie lassen die genaue interne Prioritätsreihenfolge der Komponenten bewusst aus (sie ist ein Implementierungsdetail der Engine), geben aber die für Skripte relevanten Zusicherungen zur Reihenfolge wieder:

- `fixed_update()` wird vor `update()` ausgeführt
- `late_update()` wird nach `update()` ausgeführt
- gesendete Nachrichten werden zwischen den Aktualisierungen der Komponententypen sowie zwischen den Skript-Callback-Phasen zugestellt

Wenn `Use Fixed Timestep` auf `false` gesetzt ist und/oder Fixed Update Frequency den Wert `0` hat, wird zu Beginn der Phase `dt` vorbereitet. Danach ist der Ablauf wie in der folgenden Tabelle dargestellt:

:::sidenote
Beachte, dass nach der Aktualisierung **jedes** Komponententyps alle Nachrichten zugestellt werden. Damit die folgende Tabelle übersichtlich bleibt, ist dies dort nicht eingezeichnet.
:::

| Schritt | Engine-Phase | Lua-Callback | Kommentar |
|-|-|-|-|
| 1 | **Aktualisierung** | `update()` | Wird einmal pro Frame für jeden Komponententyp, der die Aktualisierung implementiert, in der internen Prioritätsreihenfolge aufgerufen. Außerdem werden hier mit `go.animate()` gestartete Animationen von Spielobjekteigenschaften als eigener Komponententyp aktualisiert. **Physikkomponenten** werden hier aktualisiert. Für jeden aktivierten Sammlungs-Proxy wird die gesamte Phase `Update` rekursiv ab Schritt 1 aufgerufen. |
| 2 | **Späte Aktualisierung** | `late_update()` | Wird einmal pro Frame für jeden Komponententyp, der die späte Aktualisierung implementiert, in der internen Prioritätsreihenfolge aufgerufen. |
| 3 | **Transformationen** | | Am Ende wird bei Bedarf für jede Komponente eine zusätzliche abschließende Aktualisierung der Transformationen ausgeführt. |

#### Aktualisierungsphase der Engine mit festem Zeitschritt {#engine-update-phase-with-fixed-timestep}

Wenn `Use Fixed Timestep` auf `true` gesetzt ist und Fixed Update Frequency ungleich null ist, werden zu Beginn der Phase `dt` (Zeitdifferenz), `fixed_dt` und `num_fixed_steps` (`0..N`) vorbereitet. Letzteres gibt an, wie oft die Aktualisierung mit festem Zeitschritt aufgerufen wird. Die Anzahl wird anhand der Zeit seit der letzten Aktualisierung bestimmt, um eine feste Anzahl von Aktualisierungen sicherzustellen.

:::sidenote
Beachte, dass nach der Aktualisierung **jedes** Komponententyps alle Nachrichten zugestellt werden. Damit die folgende Tabelle übersichtlich bleibt, ist dies dort nicht eingezeichnet.
:::

Dann folgt die Schleife:

| Schritt | Engine-Phase | Lua-Callback | Kommentar |
|-|-|-|-|
| 1 | **Aktualisierung mit festem Zeitschritt** | `fixed_update()` | Wird je nach Zeitverlauf `0..N` Mal pro Frame für jeden Komponententyp, der die Aktualisierung mit festem Zeitschritt implementiert, in der internen Prioritätsreihenfolge aufgerufen. Dies umfasst die Aktualisierungsschritte mit festem Zeitschritt der *Physikkomponenten*. |
| 2 | **Aktualisierung** | `update()` | Wird einmal pro Frame für jeden Komponententyp, der die Aktualisierung implementiert, in der internen Prioritätsreihenfolge aufgerufen. Außerdem werden hier mit `go.animate()` gestartete Animationen von Spielobjekteigenschaften als eigener Komponententyp aktualisiert. Für jeden aktivierten Sammlungs-Proxy wird die Phase `Update` rekursiv ab Schritt 1 aufgerufen. |
| 3 | **Späte Aktualisierung** | `late_update()` | Wird einmal pro Frame für jeden Komponententyp, der die späte Aktualisierung implementiert, in der internen Prioritätsreihenfolge aufgerufen. |
| 4 | **Transformationen** | | Am Ende wird bei Bedarf für jede Komponente eine zusätzliche abschließende Aktualisierung der Transformationen ausgeführt. |

Wenn du mehr darüber erfahren möchtest, wie Defold während der Aktualisierungsphase intern arbeitet, lohnt sich ein Blick direkt in den Code von [`gameobject.cpp`](https://github.com/defold/defold/blob/dev/engine/gameobject/src/gameobject/gameobject.cpp).

### Aktualisierungsphase des Renderings {#render-update-phase}

Der Block zur Aktualisierung des Renderings stellt zuerst alle Nachrichten zu, die an den Socket `@render` gesendet wurden (z. B. `set_view_projection`-Nachrichten von Kamerakomponenten, `set_clear_color`-Nachrichten usw.). Anschließend wird `update()` im Render-Skript aufgerufen.

![Aktualisierungsphase des Renderings](images/application_lifecycle/render_update_phase.png)

### Phase nach der Aktualisierung {#post-update-phase}

Nach den Aktualisierungen wird eine Sequenz für die Phase nach der Aktualisierung ausgeführt. Sie entlädt Sammlungs-Proxys aus dem Speicher, die zum Entladen vorgemerkt sind (dies geschieht während der Sequenz zum „Zustellen von Nachrichten“). Für jedes zum Löschen vorgemerkte Spielobjekt werden alle `final()`-Funktionen seiner Komponenten aufgerufen, sofern welche vorhanden sind. Der Code in den `final()`-Funktionen sendet häufig neue Nachrichten an die Warteschlange, daher folgt danach der Durchlauf zum „Zustellen von Nachrichten“.

![Phase nach der Aktualisierung](images/application_lifecycle/post_update_phase.png)

Als Nächstes erzeugt jede Fabrikkomponente, die zum dynamischen Erzeugen eines Spielobjekts angewiesen wurde, dieses Spielobjekt. Zum Schluss werden die zum Löschen vorgemerkten Spielobjekte tatsächlich gelöscht.

### Renderphase {#render-phase}

Im letzten Schritt der Aktualisierungsschleife werden `@system`-Nachrichten zugestellt (`exit`- und `reboot`-Nachrichten, Umschalten des Profilers, Starten und Stoppen der Videoaufnahme usw.).

![Renderphase](images/application_lifecycle/render_phase.png)

Danach werden die Grafiken sowie gegebenenfalls die Darstellung des visuellen Profilers gerendert (siehe die [Debugging-Dokumentation](/manuals/debugging)). Nach dem Rendern der Grafiken erfolgt die Videoaufnahme.

#### Bildrate und Zeitschritt der Sammlung {#frame-rate-and-collection-time-step}

Die Anzahl der Frame-Aktualisierungen pro Sekunde (die der Anzahl der Durchläufe der Aktualisierungsschleife pro Sekunde entspricht) lässt sich in den Projekteinstellungen festlegen oder per Programm, indem eine `set_update_frequency`-Nachricht an den Socket `@system` gesendet wird. Außerdem kannst du den _Zeitschritt_ für Sammlungs-Proxys einzeln festlegen, indem du eine `set_time_step`-Nachricht an den jeweiligen Proxy sendest. Eine Änderung des Zeitschritts einer Sammlung beeinflusst die Bildrate nicht. Sie wirkt sich auf den Zeitschritt der Physikaktualisierung sowie auf die Variable `dt` aus, die an `update().` übergeben wird. Beachte auch, dass eine Änderung des Zeitschritts die Anzahl der Aufrufe von `update()` pro Frame nicht verändert – es ist immer genau ein Aufruf.

(Weitere Informationen findest du im [Handbuch zu Sammlungs-Proxys](/manuals/collection-proxy) und unter [`set_time_step`](/ref/collectionproxy#set-time-step))

#### Drosselung der Engine {#engine-throttling}

Defold 1.12.0 führte eine API zum Drosseln der Engine ein, mit der sich Engine-Aktualisierungen und Rendering vollständig überspringen lassen, während Eingaben weiterhin erkannt werden. Jede Eingabe weckt die Engine wieder auf. Nach einer Wartezeit kann die Engine erneut in den gedrosselten Zustand wechseln.

Weitere Informationen und Anwendungsbeispiele findest du in der API zu `sys.set_engine_throttle()`.

## Finalisierung {#finalization}

Wenn die Anwendung beendet wird, schließt sie zunächst die letzte Sequenz der Aktualisierungsschleife ab. Dabei werden alle Sammlungs-Proxys entladen: Alle Spielobjekte in jeder vom Proxy geladenen Sammlung werden finalisiert und gelöscht.

Anschließend tritt die Engine in eine Finalisierungssequenz ein, die die Hauptsammlung und ihre Objekte behandelt:

![Finalisierung](images/application_lifecycle/finalization.png)

Zuerst werden die `final()`-Funktionen der Komponenten aufgerufen. Darauf folgt das Zustellen von Nachrichten. Schließlich werden alle Spielobjekte gelöscht und die Hauptsammlung wird entladen.

Die Engine fährt dann im Hintergrund die Subsysteme herunter: Die Projektkonfiguration wird gelöscht, der Speicherprofiler wird beendet und so weiter.

Die Anwendung ist jetzt vollständig beendet.

## Nachrichten zustellen {#dispatching-messages}

Das **Zustellen von Nachrichten** ist ein besonderer Durchlauf, der nach der Aktualisierung **jedes** Komponententyps ausgeführt wird, also beispielsweise nach der Aktualisierung von Sprites und Skripten, sowie nach jeder anderen Aktion, die Nachrichten senden kann. Dabei werden alle gesendeten Nachrichten zugestellt, die in einer Warteschlange gesammelt wurden. Diese Durchläufe sind in den Diagrammen mit kleinen Symbolen für einen „Briefumschlag mit Pfeil“ 📩 gekennzeichnet.

![Nachrichten zustellen](images/application_lifecycle/dispatch_messages.png)

Nachdem alle **benutzerdefinierten Nachrichten** durch Aufrufe von `on_message()` für die jeweiligen Komponenten zugestellt wurden, werden die speziellen Defold-Nachrichten für jeden Sammlungs-Proxy in der folgenden Reihenfolge verarbeitet (die auch im Diagramm dargestellt ist):

1. `load`-Nachrichten – laden zum Laden vorgemerkte Sammlungs-Proxys und senden die Nachricht `proxy_loaded` zurück.
2. `unload`-Nachrichten – entladen zum Entladen vorgemerkte Sammlungs-Proxys und senden die Nachricht `proxy_unloaded` zurück.
3. `init`-Nachrichten – lösen die Phase `Collection Init` für alle zu initialisierenden Sammlungs-Proxys aus.
4. `final`-Nachrichten – lösen `final()` für alle Komponenten des zur Finalisierung vorgemerkten Proxys aus.
5. `enable`-Nachrichten – aktivieren den Sammlungs-Proxy, sodass die `Update Loop` im nächsten Frame für ihn ausgeführt wird; dabei wird implizit `init()` für jede Komponente der Sammlung ausgelöst.
6. `disable`-Nachrichten – deaktivieren den Sammlungs-Proxy, sodass die `Update Loop` im nächsten Frame **nicht** für ihn ausgeführt wird; die Ausführung der `Update Loop` für ihn wird vollständig angehalten.

Da der `on_message()`-Code jeder empfangenden Komponente weitere Nachrichten senden kann, stellt die Nachrichtenverarbeitung gesendete Nachrichten rekursiv weiter zu, bis die Nachrichtenwarteschlange leer ist. Die Anzahl der Durchläufe durch die Nachrichtenwarteschlange ist jedoch begrenzt. Weitere Informationen findest du unter [Nachrichtenketten](/manuals/message-passing).
