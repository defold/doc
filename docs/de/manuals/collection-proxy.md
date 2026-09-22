---
title: Handbuch zu Sammlungs-Proxys
brief: Dieses Handbuch erklärt, wie du dynamisch neue Spielwelten erstellst und zwischen ihnen wechselst.
---

# Sammlungs-Proxy {#collection-proxy}

Ein Sammlungs-Proxy (collection proxy) ist eine Komponente (component) zum dynamischen Laden und Entladen neuer „Spielwelten“ anhand des Inhalts einer Sammlungsdatei. Du kannst damit den Wechsel zwischen Spiellevels und GUI-Bildschirmen, das Laden und Entladen erzählerischer „Szenen“ im Verlauf eines Levels, das Laden und Entladen von Minispielen und mehr umsetzen.

Defold organisiert alle Spielobjekte (game objects) in Sammlungen (collections). Eine Sammlung kann Spielobjekte und andere Sammlungen (also Untersammlungen) enthalten. Mit Sammlungs-Proxys kannst du deine Inhalte in getrennte Sammlungen aufteilen und das Laden und Entladen dieser Sammlungen dann dynamisch durch Skripte verwalten.

Sammlungs-Proxys unterscheiden sich von [Komponenten vom Typ Sammlungsfabrik (collection factory)](/manuals/collection-factory/). Eine Sammlungsfabrik instanziiert den Inhalt einer Sammlung in der aktuellen Spielwelt. Sammlungs-Proxys erstellen zur Laufzeit eine neue Spielwelt und haben deshalb andere Anwendungsfälle.

## Eine Sammlungs-Proxy-Komponente erstellen {#creating-a-collection-proxy-component}

1. Füge einem Spielobjekt eine Sammlungs-Proxy-Komponente hinzu, indem du einen <kbd>Rechtsklick</kbd> auf ein Spielobjekt ausführst und im Kontextmenü <kbd>Add Component ▸ Collection Proxy</kbd> auswählst.

2. Setze die Eigenschaft *Collection* auf eine Sammlung, die du zu einem späteren Zeitpunkt dynamisch in die Laufzeitumgebung laden möchtest. Dies ist eine statische Abhängigkeit zur Build-Zeit: Die referenzierte Sammlung und ihre Abhängigkeiten werden kompiliert. Wenn *Exclude* nicht angekreuzt ist, werden sie in das Haupt-Bundle aufgenommen. Ist *Exclude* angekreuzt, können Ressourcen, die ausschließlich über ausgeschlossene Proxys referenziert werden, für Live Update aus dem Haupt-Bundle weggelassen werden. Außerdem kann der entladene Proxy zur Laufzeit auf eine andere kompilierte Sammlung umgeleitet werden, wie unten beschrieben.

![Proxy-Komponente hinzufügen](images/collection-proxy/create_proxy.png)

(Du kannst die Inhalte vom Build ausschließen und stattdessen per Code herunterladen, indem du das Kästchen *Exclude* ankreuzt und die [Funktion Live Update](/manuals/live-update/) verwendest.)

## Startsammlung {#bootstrap}

Beim Start lädt und instanziiert die Defold-Engine alle Spielobjekte aus einer *Startsammlung (bootstrap collection)* in der Laufzeitumgebung. Anschließend initialisiert und aktiviert sie die Spielobjekte und ihre Komponenten. Welche Startsammlung die Engine verwenden soll, wird in den [Projekteinstellungen](/manuals/project-settings/#main-collection) festgelegt. Üblicherweise wird diese Sammlungsdatei `main.collection` genannt.

![Startsammlung](images/collection-proxy/bootstrap.png)

Um die Spielobjekte und ihre Komponenten unterzubringen, weist die Engine den Speicher zu, der für die gesamte „Spielwelt“ benötigt wird, in der die Inhalte der Startsammlung instanziiert werden. Für Kollisionsobjekte und die Physiksimulation wird außerdem eine eigene Physikwelt erstellt.

Da Skriptkomponenten alle Objekte im Spiel auch von außerhalb der Startwelt adressieren können müssen, erhält diese einen eindeutigen Namen: die Eigenschaft *Name*, die du in der Sammlungsdatei festlegst:

![Startsammlung](images/collection-proxy/collection_id.png)

Wenn die geladene Sammlung Sammlungs-Proxy-Komponenten enthält, werden die von ihnen referenzierten Sammlungen *nicht* automatisch geladen. Du musst das Laden dieser Ressourcen durch Skripte steuern.

## Eine Sammlung laden {#loading-a-collection}

Um eine Sammlung dynamisch über einen Proxy zu laden, sendest du aus einem Skript eine Nachricht namens `"load"` an die Proxy-Komponente:

```lua
-- Tell the proxy "myproxy" to start loading.
msg.post("#myproxy", "load")
```

![Laden](images/collection-proxy/proxy_load.png)

Die Proxy-Komponente weist die Engine an, Speicherplatz für eine neue Welt zuzuweisen. Außerdem wird eine eigene Physikwelt in der Laufzeitumgebung erstellt, und alle Spielobjekte in der Sammlung „`mylevel.collection`“ werden instanziiert.

Die neue Welt erhält ihren Namen aus der Eigenschaft *Name* in der Sammlungsdatei; in diesem Beispiel ist sie auf „`mylevel`“ gesetzt. Der Name muss eindeutig sein. Wenn der in der Sammlungsdatei festgelegte *Name* bereits für eine geladene Welt verwendet wird, meldet die Engine einen Fehler aufgrund eines Namenskonflikts:

```txt
ERROR:GAMEOBJECT: The collection 'default' could not be created since there is already a socket with the same name.
WARNING:RESOURCE: Unable to create resource: build/default/mylevel.collectionc
ERROR:GAMESYS: The collection /mylevel.collectionc could not be loaded.
```

Wenn die Engine das Laden der Sammlung abgeschlossen hat, sendet die Sammlungs-Proxy-Komponente eine Nachricht namens `"proxy_loaded"` an das Skript zurück, das die Nachricht `"load"` gesendet hat. Als Reaktion auf diese Nachricht kann das Skript die Sammlung dann initialisieren und aktivieren:

```lua
function on_message(self, message_id, message, sender)
    if message_id == hash("proxy_loaded") then
        -- New world is loaded. Init and enable it.
        msg.post(sender, "init")
        msg.post(sender, "enable")
        ...
    end
end
```

`"load"`
: Diese Nachricht weist die Sammlungs-Proxy-Komponente an, mit dem Laden ihrer Sammlung in eine neue Welt zu beginnen. Wenn der Proxy damit fertig ist, sendet er eine Nachricht namens `"proxy_loaded"` zurück.

`"async_load"`
: Diese Nachricht weist die Sammlungs-Proxy-Komponente an, ihre Sammlung im Hintergrund in eine neue Welt zu laden. Wenn der Proxy damit fertig ist, sendet er eine Nachricht namens `"proxy_loaded"` zurück.

`"init"`
: Diese Nachricht teilt der Sammlungs-Proxy-Komponente mit, dass alle instanziierten Spielobjekte und Komponenten initialisiert werden sollen. In dieser Phase werden alle `init()`-Funktionen der Skripte aufgerufen.

`"enable"`
: Diese Nachricht teilt der Sammlungs-Proxy-Komponente mit, dass alle Spielobjekte und Komponenten aktiviert werden sollen. Beispielsweise beginnen alle Sprite-Komponenten nach der Aktivierung mit dem Zeichnen.

## Die Sammlung eines ausgeschlossenen Proxys ändern {#changing-an-excluded-proxys-collection}

Mit [`collectionproxy.set_collection()`](/ref/collectionproxy/#collectionproxy.set_collection) kannst du einen ausgeschlossenen, entladenen Proxy auf eine kompilierte Sammlung umleiten. Das ist nach dem Einbinden eines Live-Update-Pakets nützlich. Beim Proxy muss *Exclude* angekreuzt sein, und er darf weder geladen sein noch gerade geladen werden. Der Pfad muss auf `.collectionc` enden. Die Sammlung und alle ihre Abhängigkeiten müssen dem Ressourcensystem zur Verfügung stehen, wenn der Proxy geladen wird.

Prüfe den Rückgabewert, bevor du den Proxy lädst. Initialisiere und aktiviere die neue Welt erst nach dem Empfang von `proxy_loaded`:

```lua
local function load_mounted_level()
    local ok, result = collectionproxy.set_collection(
        "#level_proxy",
        "/level_pack/level_3.collectionc"
    )

    if ok then
        msg.post("#level_proxy", "load")
    else
        print("Unable to change proxy collection", result)
    end
end

function on_message(self, message_id, message, sender)
    if message_id == hash("proxy_loaded") then
        msg.post(sender, "init")
        msg.post(sender, "enable")
    end
end
```

Rufe `collectionproxy.set_collection("#level_proxy", nil)` auf, während der Proxy weder geladen ist noch gerade geladen wird, um die im Editor zugewiesene Sammlung wiederherzustellen. Informationen zum Herunterladen und Einbinden von Inhalten findest du im [Handbuch zur Skriptsteuerung von Live Update](/manuals/live-update-scripting/); die Fehlercodes `collectionproxy.RESULT_*` sind in der API-Referenz beschrieben.

## Adressierung in der neuen Welt {#addressing-into-the-new-world}

Der in den Eigenschaften der Sammlungsdatei festgelegte *Name* wird verwendet, um Spielobjekte und Komponenten in der geladenen Welt zu adressieren. Wenn du beispielsweise ein Ladeobjekt in der Startsammlung erstellst, musst du möglicherweise von jeder geladenen Sammlung aus mit ihm kommunizieren:

```lua
-- tell the loader to load the next level:
msg.post("main:/loader#script", "load_level", { level_id = 2 })
```

![Laden](images/collection-proxy/message_passing.png)

Wenn du vom Ladeobjekt aus mit einem Spielobjekt in der geladenen Sammlung kommunizieren musst, kannst du über die [vollständige URL des Objekts](/manuals/addressing/#urls) eine Nachricht senden:

```lua
msg.post("mylevel:/myobject", "hello")
```

::: important
Es ist nicht möglich, von außerhalb einer geladenen Sammlung direkt auf Spielobjekte innerhalb dieser Sammlung zuzugreifen:

```lua
local position = go.get_position("mylevel:/myobject")
-- loader.script:42: function called can only access instances within the same collection.
```
:::


## Eine Welt entladen {#unloading-a-world}

Um eine geladene Sammlung zu entladen, sendest du Nachrichten, die den umgekehrten Schritten des Ladevorgangs entsprechen:

```lua
-- unload the level
msg.post("#myproxy", "disable")
msg.post("#myproxy", "final")
msg.post("#myproxy", "unload")
```

`"disable"`
: Diese Nachricht weist die Sammlungs-Proxy-Komponente an, alle Spielobjekte und Komponenten in der Welt zu deaktivieren. In dieser Phase werden Sprites nicht mehr gerendert.

`"final"`
: Diese Nachricht weist die Sammlungs-Proxy-Komponente an, alle Spielobjekte und Komponenten in der Welt zu finalisieren. In dieser Phase werden die `final()`-Funktionen aller Skripte aufgerufen.

`"unload"`
: Diese Nachricht weist den Sammlungs-Proxy an, die Welt vollständig aus dem Speicher zu entfernen.

Wenn du keine so feine Steuerung benötigst, kannst du die Nachricht `"unload"` direkt senden, ohne die Sammlung vorher zu deaktivieren und zu finalisieren. Der Proxy deaktiviert und finalisiert die Sammlung dann automatisch, bevor sie entladen wird.

Wenn der Sammlungs-Proxy das Entladen der Sammlung abgeschlossen hat, sendet er eine Nachricht namens `"proxy_unloaded"` an das Skript zurück, das die Nachricht `"unload"` gesendet hat:

```lua
function on_message(self, message_id, message, sender)
    if message_id == hash("proxy_unloaded") then
        -- Ok, the world is unloaded...
        ...
    end
end
```


## Zeitschritt {#time-step}

Die Aktualisierungen eines Sammlungs-Proxys können durch Ändern des _Zeitschritts_ skaliert werden. Das bedeutet, dass ein Proxy schneller oder langsamer aktualisiert werden kann, obwohl das Spiel mit konstanten 60 Bildern pro Sekunde (FPS) läuft. Das wirkt sich beispielsweise auf Folgendes aus:

* Geschwindigkeit der Physiksimulation
* Der Wert von `dt`, der an `update()` übergeben wird
* [Eigenschaftsanimationen von Spielobjekten und GUI-Knoten](https://defold.com/manuals/animation/#property-animation-1)
* [Flipbook-Animationen](https://defold.com/manuals/animation/#flip-book-animation)
* [Simulationen von Partikeleffekten](https://defold.com/manuals/particlefx/)
* Geschwindigkeit von Timern

Du kannst außerdem den Aktualisierungsmodus festlegen. Damit steuerst du, ob die Skalierung diskret (was nur bei einem Skalierungsfaktor unter 1,0 sinnvoll ist) oder kontinuierlich erfolgt.

Du steuerst den Skalierungsfaktor und den Skalierungsmodus, indem du dem Proxy eine Nachricht namens `set_time_step` sendest:

```lua
-- update loaded world at one-fifth-speed.
msg.post("#myproxy", "set_time_step", {factor = 0.2, mode = 1}
```

Um zu sehen, was beim Ändern des Zeitschritts passiert, können wir ein Objekt mit dem folgenden Code in einer Skriptkomponente erstellen und es in die Sammlung aufnehmen, deren Zeitschritt wir verändern:

```lua
function update(self, dt)
    print("update() with timestep (dt) " .. dt)
end
```

Mit einem Zeitschritt von 0,2 erhalten wir folgendes Ergebnis in der Konsole:

```txt
INFO:ENGINE: Defold Engine 1.2.37 (6b3ae27)
INFO:ENGINE: Loading data from: build/default
DEBUG:SCRIPT: update() with timestep (dt) 0
DEBUG:SCRIPT: update() with timestep (dt) 0
DEBUG:SCRIPT: update() with timestep (dt) 0
DEBUG:SCRIPT: update() with timestep (dt) 0
DEBUG:SCRIPT: update() with timestep (dt) 0.016666667535901
DEBUG:SCRIPT: update() with timestep (dt) 0
DEBUG:SCRIPT: update() with timestep (dt) 0
DEBUG:SCRIPT: update() with timestep (dt) 0
DEBUG:SCRIPT: update() with timestep (dt) 0
DEBUG:SCRIPT: update() with timestep (dt) 0.016666667535901
```

`update()` wird weiterhin 60 Mal pro Sekunde aufgerufen, aber der Wert von `dt` ändert sich. Wir sehen, dass nur 1/5 (0,2) der Aufrufe von `update()` einen Wert von 1/60 (entsprechend 60 FPS) für `dt` haben---bei den übrigen ist er null. Alle Physiksimulationen werden ebenfalls entsprechend diesem `dt` aktualisiert und schreiten nur in einem Fünftel der Frames voran.

::: sidenote
Du kannst die Zeitschrittfunktion der Sammlung verwenden, um dein Spiel zu pausieren, beispielsweise während ein Popup angezeigt wird oder wenn das Fenster den Fokus verloren hat. Verwende `msg.post("#myproxy", "set_time_step", {factor = 0, mode = 0})` zum Pausieren und `msg.post("#myproxy", "set_time_step", {factor = 1, mode = 1})` zum Fortsetzen.
:::

Weitere Einzelheiten findest du unter [`set_time_step`](/ref/collectionproxy#set_time_step).

## Einschränkungen und häufige Probleme {#caveats-and-common-issues}

Physik
: Über Sammlungs-Proxys kannst du mehr als eine Sammlung auf oberster Ebene, also eine *Spielwelt*, in die Engine laden. Dabei musst du beachten, dass jede Sammlung auf oberster Ebene eine eigene Physikwelt ist. Physikalische Wechselwirkungen (Kollisionen, Trigger, Strahlabfragen (raycasts)) finden nur zwischen Objekten statt, die zur selben Welt gehören. Selbst wenn die Kollisionsobjekte zweier Welten optisch direkt übereinanderliegen, kann es daher keine physikalischen Wechselwirkungen zwischen ihnen geben.

Speicher
: Jede geladene Sammlung erstellt eine neue Spielwelt mit einem relativ hohen Speicherbedarf. Wenn du Dutzende von Sammlungen gleichzeitig über Proxys lädst, solltest du deinen Entwurf möglicherweise überdenken. Um viele Instanzen von Spielobjekthierarchien dynamisch zu erzeugen, eignen sich [Sammlungsfabriken](/manuals/collection-factory) besser.

Eingabe
: Wenn Objekte in deiner geladenen Sammlung Eingabeaktionen benötigen, musst du sicherstellen, dass das Spielobjekt, das den Sammlungs-Proxy enthält, den Eingabefokus anfordert. Wenn das Spielobjekt Eingabenachrichten empfängt, werden diese an die Komponenten dieses Objekts weitergegeben, also an die Sammlungs-Proxys. Die Eingabeaktionen werden über den Proxy an die geladene Sammlung gesendet.
