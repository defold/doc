---
title: Ein einfaches Auto in Defold bauen.
brief: Wenn du neu bei Defold bist, hilft dir diese Anleitung dabei, dich im Editor zurechtzufinden. Sie erklärt außerdem die Grundideen und die häufigsten Bausteine von Defold – Spielobjekte, Sammlungen, Skripte und Sprites.
---

# Ein Auto bauen {#building-a-car}

Wenn du neu bei Defold bist, hilft dir diese Anleitung dabei, dich im Editor zurechtzufinden. Sie erklärt außerdem die Grundideen und die häufigsten Bausteine von Defold: Spielobjekte (game objects), Sammlungen (collections), Skripte (scripts) und Sprites.

Wir beginnen mit einem leeren Projekt und arbeiten uns Schritt für Schritt zu einer sehr kleinen, spielbaren Anwendung vor. Am Ende hast du hoffentlich ein Gefühl dafür, wie Defold funktioniert, und bist bereit, ein umfangreicheres Tutorial anzugehen oder direkt in die Handbücher einzusteigen.

::: sidenote
Im gesamten Tutorial sind ausführliche Beschreibungen von Konzepten und einzelnen Arbeitsschritten wie dieser Absatz gekennzeichnet. Wenn dir diese Abschnitte zu sehr ins Detail gehen, kannst du sie überspringen.
:::

## Ein neues Projekt erstellen {#creating-a-new-project}

![Neues Projekt](images/new_empty.png)

1. Starte Defold.
2. Wähle links *New Project*.
3. Wähle die Registerkarte *From Template*.
4. Wähle *Empty Project*
5. Wähle einen Speicherort für das Projekt auf deinem lokalen Laufwerk.
6. Klicke auf *Create New Project*.

## Der Editor {#the-editor}

Erstelle zunächst ein [neues Projekt](/manuals/project-setup/) und öffne es im Editor. Wenn du auf die Datei *main/main.collection* doppelklickst, wird sie geöffnet:

![Übersicht des Editors](../manuals/images/editor/editor2_overview.png)

Der Editor besteht aus den folgenden Hauptbereichen:

Assets pane
: Diese Ansicht zeigt alle Dateien in deinem Projekt. Unterschiedliche Dateitypen haben unterschiedliche Symbole. Doppelklicke auf eine Datei, um sie in dem für diesen Dateityp vorgesehenen Editor zu öffnen. Der besondere, schreibgeschützte Ordner *builtins* ist für alle Projekte gemeinsam verfügbar und enthält nützliche Elemente wie ein Standard-Render-Skript, eine Schriftart, Materialien zum Rendern verschiedener Komponenten (components) und weitere Dinge.

Main Editor View
: Je nachdem, welchen Dateityp du bearbeitest, zeigt diese Ansicht den passenden Editor an. Am häufigsten wird der Szeneneditor verwendet, den du hier siehst. Jede geöffnete Datei wird in einer eigenen Registerkarte angezeigt.

Changed Files
: Enthält Dateien, die im Vergleich zum aktuellen Git-Commit lokal hinzugefügt, geändert, umbenannt oder gelöscht wurden. Hier kannst du Textunterschiede anzeigen und lokale Änderungen rückgängig machen. Verwende einen externen Git-Client oder die Befehlszeile, um mit einem entfernten Repository zu synchronisieren.

Outline
: Der Inhalt der gerade bearbeiteten Datei in einer hierarchischen Ansicht. Über diese Ansicht kannst du Objekte und Komponenten hinzufügen, löschen, ändern und auswählen.

Properties
: Die Eigenschaften, die für das aktuell ausgewählte Objekt oder die ausgewählte Komponente festgelegt sind.

Console
: Wenn das Spiel läuft, erfasst diese Ansicht Ausgaben der Spiel-Engine (Protokollmeldungen, Fehler, Debug-Informationen usw.) sowie alle eigenen Debug-Meldungen aus deinen Skripten, die mit `print()` und `pprint()` ausgegeben werden. Wenn deine Anwendung oder dein Spiel nicht startet, solltest du zuerst die Konsole prüfen. Hinter der Konsole befinden sich mehrere Registerkarten mit Fehlerinformationen sowie ein Kurveneditor, der beim Erstellen von Partikeleffekten verwendet wird.

## Das Spiel ausführen {#running-the-game}

Die Projektvorlage "Empty" ist tatsächlich vollständig leer. Wähle trotzdem <kbd>Project ▸ Build</kbd>, um einen Build des Projekts zu erstellen und das Spiel zu starten.

![Build erstellen](images/car/start_build_and_launch.png)

Ein schwarzer Bildschirm ist vielleicht nicht besonders aufregend, aber dahinter läuft eine Defold-Spielanwendung, die wir leicht in etwas Interessanteres verwandeln können. Also machen wir das.

::: sidenote
Der Defold-Editor arbeitet mit Dateien. Wenn du im *Assets pane* auf eine Datei doppelklickst, öffnest du sie in einem passenden Editor. Anschließend kannst du den Inhalt der Datei bearbeiten.

Wenn du mit der Bearbeitung einer Datei fertig bist, musst du sie speichern. Wähle im Hauptmenü <kbd>File ▸ Save</kbd>. Der Editor weist auf ungespeicherte Änderungen hin, indem er in der Registerkarte der jeweiligen Datei ein Sternchen '\*' an den Dateinamen anhängt.

![Datei mit ungespeicherten Änderungen](images/car/file_changed.png)
:::

## Das Auto zusammensetzen {#assembling-the-car}

Als Erstes erstellen wir eine neue Sammlung. Eine Sammlung ist ein Behälter für Spielobjekte, die du eingefügt und positioniert hast. Sammlungen werden meist zum Erstellen von Spiellevels verwendet. Sie sind aber immer dann sehr nützlich, wenn du Gruppen und/oder Hierarchien zusammengehöriger Spielobjekte wiederverwenden musst. Es kann hilfreich sein, sich Sammlungen als eine Art Prefab vorzustellen.

Klicke im *Assets pane* auf den Ordner *main*, klicke dann mit der rechten Maustaste und wähle <kbd>New ▸ Collection File</kbd>. Du kannst auch im Hauptmenü <kbd>File ▸ New ▸ Collection File</kbd> auswählen.

![Neue Sammlungsdatei](images/car/start_new_collection.png)

Nenne die neue Sammlungsdatei *car.collection* und öffne sie. Wir verwenden diese neue, leere Sammlung, um aus einigen Spielobjekten ein kleines Auto zu bauen. Ein Spielobjekt ist ein Behälter für Komponenten (wie Sprites, Sounds, Logikskripte usw.), mit denen du dein Spiel aufbaust. Jedes Spielobjekt wird im Spiel durch seine ID eindeutig identifiziert. Spielobjekte können durch den Austausch von Nachrichten miteinander kommunizieren, aber dazu später mehr.

Außerdem ist es möglich, ein Spielobjekt direkt in einer Sammlung zu erstellen, wie wir es hier getan haben. Dadurch entsteht ein eigenständiges Objekt. Du kannst dieses Objekt kopieren, aber jede Kopie ist unabhängig – Änderungen an einer Kopie wirken sich nicht auf die anderen aus. Wenn du also 10 Kopien eines Spielobjekts erstellst und feststellst, dass du sie alle ändern möchtest, musst du alle 10 Instanzen des Objekts bearbeiten. Daher solltest du direkt in der Sammlung erstellte Spielobjekte für Objekte verwenden, von denen du nicht viele Kopien anlegen möchtest.

Ein Spielobjekt, das in einer _Datei_ gespeichert ist, dient dagegen als Prototyp (in anderen Engines auch als „Prefabs“ oder „Blueprints“ bekannt). Wenn du Instanzen eines in einer Datei gespeicherten Spielobjekts in einer Sammlung platzierst, wird jedes Objekt _als Referenz_ eingefügt – es ist ein Klon, der auf dem Prototyp basiert. Wenn du den Prototyp ändern musst, wird jedes einzelne platzierte Spielobjekt, das auf diesem Prototyp basiert, sofort aktualisiert.

![Auto-Spielobjekt hinzufügen](images/car/start_add_car_gameobject.png)

Wähle in der Ansicht *Outline* den obersten Knoten "Collection", klicke mit der rechten Maustaste und wähle <kbd>Add Game Object</kbd>. Ein neues Spielobjekt mit der ID "go" erscheint in der Sammlung. Wähle es aus und setze seine ID in der Ansicht *Properties* auf "car". Bisher ist "car" noch sehr uninteressant. Es ist leer und hat weder eine visuelle Darstellung noch Logik. Um eine visuelle Darstellung hinzuzufügen, müssen wir eine Sprite-_Komponente_ hinzufügen.

Komponenten erweitern Spielobjekte um wahrnehmbare Inhalte (Grafik, Sound) und Funktionalität (Fabriken (factories) zum dynamischen Erzeugen von Objekten, Kollisionen, skriptgesteuertes Verhalten). Eine Komponente kann nicht allein existieren, sondern muss sich in einem Spielobjekt befinden. Komponenten werden normalerweise direkt in derselben Datei wie das Spielobjekt definiert. Wenn du eine Komponente wiederverwenden möchtest, kannst du sie jedoch in einer separaten Datei speichern (wie auch Spielobjekte) und als Referenz in eine beliebige Spielobjektdatei einbinden. Einige Komponententypen (zum Beispiel Lua-Skripte) müssen in einer separaten Komponentendatei liegen und dann als Referenz in deine Objekte eingebunden werden.

Beachte, dass du Komponenten nicht direkt veränderst – du kannst Spielobjekte, die ihrerseits Komponenten enthalten, verschieben, drehen und skalieren sowie ihre Eigenschaften animieren.

![Komponente zum Auto hinzufügen](images/car/start_add_car_component.png)

Wähle das Spielobjekt "car", klicke mit der rechten Maustaste und wähle <kbd>Add Component</kbd>. Wähle dann *Sprite* und klicke auf *Ok*. Wenn du das Sprite in der Ansicht *Outline* auswählst, siehst du, dass noch einige Eigenschaften festgelegt werden müssen:

Image
: Hier wird eine Bildquelle für das Sprite benötigt. Erstelle eine Atlas-Bilddatei, indem du in der Ansicht *Assets pane* "main" auswählst, mit der rechten Maustaste klickst und <kbd>New ▸ Atlas File</kbd> wählst. Nenne die neue Atlasdatei *sprites.atlas* und doppelklicke darauf, um sie im Atlas-Editor zu öffnen. Speichere die folgenden beiden Bilddateien auf deinem Computer und ziehe sie in der Ansicht *Assets pane* nach *main*. Nun kannst du den obersten Knoten Atlas im Atlas-Editor auswählen, mit der rechten Maustaste klicken und <kbd>Add Images</kbd> wählen. Füge das Auto- und das Reifenbild zum Atlas hinzu und speichere ihn. Jetzt kannst du *sprites.atlas* als Bildquelle für die Sprite-Komponente im Spielobjekt "car" in der Sammlung "car" auswählen.

Bilder für unser Spiel:

![Autobild](images/car/start_car.png)
![Reifenbild](images/car/start_tire.png)

Füge diese Bilder zum Atlas hinzu:

![Sprite-Atlas](images/car/start_sprites_atlas.png)

![Sprite-Eigenschaften](images/car/start_sprite_properties.png)

Default Animation
: Setze dies auf "car" (oder den Namen, den du dem Autobild gegeben hast). Jedes Sprite benötigt eine Standardanimation, die abgespielt wird, wenn es im Spiel angezeigt wird. Wenn du Bilder zu einem Atlas hinzufügst, erstellt Defold praktischerweise für jede Bilddatei eine Animation mit einem einzigen Frame (ein Standbild).

## Das Auto vervollständigen {#completing-the-car}

Füge als Nächstes zwei weitere Spielobjekte zur Sammlung hinzu. Nenne sie "left_wheel" und "right_wheel" und füge in jedes eine Sprite-Komponente ein, die das Reifenbild zeigt, das wir zu *sprites.atlas* hinzugefügt haben. Ziehe dann die Spielobjekte der Räder auf "car" und lege sie dort ab, damit sie "car" untergeordnet werden. Spielobjekte, die anderen Spielobjekten untergeordnet sind, bewegen sich mit ihrem übergeordneten Objekt mit. Sie können auch einzeln bewegt werden, aber jede Bewegung erfolgt relativ zum übergeordneten Objekt. Für die Reifen ist das ideal, denn sie sollen am Auto bleiben, und beim Lenken können wir sie einfach leicht nach links und rechts drehen. Eine Sammlung kann beliebig viele Spielobjekte enthalten, die nebeneinander stehen, in komplexen Eltern-Kind-Bäumen angeordnet sind oder beides kombinieren.

Bringe die Reifen-Spielobjekte in Position, indem du sie auswählst und dann <kbd>Scene ▸ Move Tool</kbd> wählst. Ziehe an den Pfeilgriffen oder am grünen Quadrat in der Mitte, um das Objekt an eine passende Stelle zu bewegen. Als Letztes müssen wir sicherstellen, dass die Reifen unter dem Auto gezeichnet werden. Dazu setzen wir die Z-Komponente der Position auf -0.5. Jedes sichtbare Element in einem Spiel wird nach seinem Z-Wert sortiert von hinten nach vorne gezeichnet. Ein Objekt mit dem Z-Wert 0 wird über einem Objekt mit dem Z-Wert -0.5 gezeichnet. Da der Standard-Z-Wert des Auto-Spielobjekts 0 ist, werden die Reifenobjekte durch den neuen Wert unter dem Autobild platziert.

![Fertige Autosammlung](images/car/start_car_collection_complete.png)

## Das Autoskript {#the-car-script}

Das letzte Puzzleteil ist ein _Skript_, das das Auto steuert. Ein Skript ist eine Komponente mit einem Programm, das das Verhalten von Spielobjekten definiert. Mit Skripten kannst du die Regeln deines Spiels festlegen und bestimmen, wie Objekte auf verschiedene Interaktionen reagieren sollen (sowohl mit der spielenden Person als auch mit anderen Objekten). Alle Skripte werden in der Programmiersprache Lua geschrieben. Um mit Defold arbeiten zu können, musst du oder jemand in deinem Team lernen, in Lua zu programmieren.

Wähle im *Assets pane* "main", klicke mit der rechten Maustaste und wähle <kbd>New ▸ Script File</kbd>. Nenne die neue Datei *car.script* und füge sie dann zum Spielobjekt "car" hinzu, indem du "car" in der Ansicht *Outline* auswählst, mit der rechten Maustaste klickst und <kbd>Add Component File</kbd> wählst. Wähle *car.script* und klicke auf *OK*. Speichere die Sammlungsdatei.

Doppelklicke auf *car.script*, um die Datei zu öffnen.

::: sidenote
Defold stellt mehrere Lebenszyklusfunktionen bereit, mit denen du Spiellogik programmieren kannst. Mehr darüber erfährst du im [Skript-Handbuch](/manuals/script).
:::

Entferne zunächst die Funktionen `final`, `on_message` und `on_reload`, da wir sie
für dieses Tutorial nicht benötigen.

Füge als Nächstes die folgenden Codezeilen vor dem Beginn der Funktion `init` ein.

```lua
-- Constants
local turn_speed = 0.1                           									  -- Slerp factor
local max_steer_angle_left = vmath.quat_rotation_z(math.pi / 6)     -- 30 degrees
local max_steer_angle_right = vmath.quat_rotation_z(-math.pi / 6)   -- -30 degrees
local steer_angle_zero = vmath.quat_rotation_z(0)									  -- Zero degrees
local wheels_vector = vmath.vector3(0, 72, 0)         		        	-- Vector from center of back and front wheel pairs

local acceleration = 100 																						-- The acceleration of the car

-- prehash the inputs
local left = hash("left")
local right = hash("right")
local accelerate = hash("accelerate")
local brake = hash("brake")
```

Die Änderungen hier sind recht einfach: Wir haben unserem Skript nur eine Reihe von Konstanten (`constants`) hinzugefügt, die wir später verwenden werden, um unser Auto zu programmieren.

::: sidenote
Beachte, wie wir die Hashwerte vorab in Variablen speichern. Das ist eine gute Vorgehensweise, da sie deinen Code lesbarer und leistungsfähiger macht.
:::

Bearbeite als Nächstes die Funktion `init` so, dass sie Folgendes enthält:

```lua
function init(self)
	-- Send a message to the render script (see builtins/render/default.render_script) to set the clear color.
	-- This changes the background color of the game. The vector4 contains color information
	-- by channel from 0-1: Red = 0.2. Green = 0.2, Blue = 0.2 and Alpha = 1.0
	msg.post("@render:", "clear_color", { color = vmath.vector4(0.2, 0.2, 0.2, 1.0) } )		--<1>

	-- Acquire input focus so we can react to input
	msg.post(".", "acquire_input_focus")		-- <2>

	-- Some variables
	self.steer_angle = vmath.quat()				 -- <3>
	self.direction = vmath.quat()

	-- Velocity and acceleration are car relative (not rotated)
	self.velocity = vmath.vector3()
	self.acceleration = vmath.vector3()

	-- Input vector. This is modified later in the on_input function
	-- to store the input.
	self.input = vmath.vector3()
end
```

Fragst du dich, was wir gerade geändert haben? Hier ist die Erklärung.

1. Wir senden eine Nachricht an unser Render-Skript mit der Aufforderung, die Hintergrundfarbe auf Grau zu setzen. Render-Skripte sind spezielle Skripte in Defold, die steuern, wie Objekte auf dem Bildschirm angezeigt werden.
2. Um in einer Skriptkomponente oder einem GUI-Skript auf Eingabeaktionen zu reagieren, muss die Nachricht `acquire_input_focus` an das Spielobjekt gesendet werden, das die Komponente enthält. In unserem Fall senden wir diese Nachricht an das Spielobjekt mit dem Autoskript.
3. Dann deklarieren wir einige Variablen, mit denen wir den aktuellen Zustand unseres Autos festhalten.

Das war doch einfach, oder? Nun bearbeiten wir die Funktion `update` so, dass sie Folgendes enthält:

```lua
function update(self, dt)
	-- Set acceleration to the y input
	self.acceleration.y = self.input.y * acceleration				-- <1>

	-- Calculate the new positions of front and back wheels
	local front_vel = vmath.rotate(self.steer_angle, self.velocity)
	local new_front_pos = vmath.rotate(self.direction, wheels_vector + front_vel)
	local new_back_pos = vmath.rotate(self.direction, self.velocity)								-- <2>

	-- Calculate the car's new direction
	local new_dir = vmath.normalize(new_front_pos - new_back_pos)
	self.direction = vmath.quat_rotation_z(math.atan2(new_dir.y, new_dir.x) - math.pi / 2)			-- <3>

	-- Calculate new velocity based on current acceleration
	self.velocity = self.velocity + self.acceleration * dt			-- <4>

	-- Update position based on current velocity and direction
	local pos = go.get_position()
	pos = pos + vmath.rotate(self.direction, self.velocity)
	go.set_position(pos)																			-- <5>

	-- Interpolate the wheels using vmath.slerp
	if self.input.x > 0 then																		-- <6>
		self.steer_angle = vmath.slerp(turn_speed, self.steer_angle, max_steer_angle_right)
	elseif self.input.x < 0 then
		self.steer_angle = vmath.slerp(turn_speed, self.steer_angle, max_steer_angle_left)
	else
		self.steer_angle = vmath.slerp(turn_speed, self.steer_angle, steer_angle_zero)
	end

	-- Update the wheel rotation
	go.set_rotation(self.steer_angle, "left_wheel")					-- <7>
	go.set_rotation(self.steer_angle, "right_wheel")

	-- Set the game object's rotation to the direction
	go.set_rotation(self.direction)

	-- reset acceleration and input
	self.acceleration = vmath.vector3()								-- <8>
	self.input = vmath.vector3()
end
```

Das war eine riesige Funktion! Aber keine Sorge, so funktioniert das Ganze:

1. Zuerst legen wir unseren Beschleunigungsvektor anhand unseres Eingabevektors fest. Dadurch wird sichergestellt, dass das Auto in Richtung der Eingabe beschleunigt.
2. Als Nächstes wird die Verschiebung beider Räder berechnet. Dabei gilt die einfache Überlegung, dass sich die Hinterräder des Autos immer vorwärts bewegen, während sich die Vorderräder in die Richtung bewegen, in die sie eingeschlagen sind.
3. Anhand der Verschiebung beider Räder wird die neue Bewegungsrichtung unseres Autos berechnet.
4. Hier addieren wir die berechnete Beschleunigung zur Geschwindigkeit.
5. Schließlich aktualisieren wir die Position des Autos anhand unserer aktuellen Geschwindigkeit.
6. Wir interpolieren den Lenkwinkel mit Slerp anhand unserer Eingabe nach links oder rechts. Dadurch springen die Räder bei einer Änderung der Eingabe nicht sofort in die neue Stellung.
7. Die Drehung der Räder wird dann anhand des aktuellen Lenkwinkels des Autos festgelegt. Ebenso wird die Drehung des Autos anhand seiner aktuellen Bewegungsrichtung festgelegt.
8. Abschließend setzen wir die Beschleunigungs- und Eingabevektoren zurück.

Zum Schluss bringen wir unser Auto dazu, auf Eingaben zu reagieren. Aktualisiere die Funktion `on_input` wie folgt:

```lua
function on_input(self, action_id, action)
	-- set the input vector to correspond to the key press
	if action_id == left then
		self.input.x = -1
	elseif action_id == right then
		self.input.x = 1
	elseif action_id == accelerate then
		self.input.y = 1
	elseif action_id == brake then
		self.input.y = -1
	end
end
```

Diese Funktion ist recht einfach: Wir nehmen lediglich die Eingabe entgegen und setzen unseren Eingabevektor.

Vergiss nicht, deine Änderungen zu speichern.

## Eingabe {#input}

Es sind noch keine Eingabeaktionen eingerichtet, also holen wir das nach. Öffne die Datei */input/game.input_bindings* und füge Eingabebindungen (input bindings) vom Typ *key_trigger* für "accelerate", "brake", "left" und "right" hinzu. Wir legen sie auf die Pfeiltasten (KEY_LEFT, KEY_RIGHT, KEY_UP und KEY_DOWN):

![Eingabebindungen](images/car/start_input_bindings.png)

## Das Auto zum Spiel hinzufügen {#adding-the-car-to-the-game}

Jetzt ist das Auto fahrbereit. Wir haben es in "car.collection" erstellt, aber im Spiel existiert es noch nicht. Das liegt daran, dass die Engine beim Start derzeit "main.collection" lädt. Um das zu ändern, müssen wir einfach *car.collection* zu *main.collection* hinzufügen. Öffne *main.collection*, wähle den obersten Knoten "Collection" in der Ansicht *Outline*, klicke mit der rechten Maustaste und wähle <kbd>Add Collection From File</kbd>. Wähle *car.collection* und klicke auf *OK*. Nun werden die Inhalte von *car.collection* als neue Instanzen in *main.collection* platziert. Wenn du den Inhalt von *car.collection* änderst, wird jede Instanz der Sammlung beim Erstellen des Spiel-Builds automatisch aktualisiert.

![Die Autosammlung hinzufügen](images/car/start_adding_car_collection.png)

Wähle nun <kbd>Project ▸ Build</kbd> und drehe eine Runde mit deinem neuen Auto!
Du wirst feststellen, dass du das Auto jetzt nach Belieben bewegen kannst. Aber etwas stimmt noch nicht. Wenn du die Steuerung loslässt, hält das Auto nicht an, obwohl es das sollte. Zeit, das einzubauen!

## Der Widerstand hilft {#drag-to-the-rescue}

Immer wenn sich ein Objekt in der realen Welt bewegt, wirkt ihm eine Widerstandskraft entgegen, die es abbremst. Diese Kraft ist annähernd proportional zum Quadrat der Geschwindigkeit des bewegten Objekts und kann daher als `D = k * |V| * V` beschrieben werden. Dabei ist `k` eine Konstante, `V` die Geschwindigkeit und `|V|` ihr Betrag (das Tempo). Fügen wir das hinzu.

Füge im Abschnitt mit den Konstanten am Anfang des Skripts die folgende Konstante hinzu

```lua
local drag = 1.1	        --the drag constant <1>
```

Füge dann in der Funktion `update` direkt über dieser Zeile die folgenden Zeilen ein und speichere die Datei.

```lua
function update(self, dt)
	...
  -- Calculate new velocity based on current acceleration
	self.velocity = self.velocity + self.acceleration * dt
	...
end
```

```lua
function update(self, dt)
	...
	-- Speed is the magnitude of the velocity
	local speed = vmath.length_sqr(self.velocity)

	-- Apply drag
	self.acceleration = self.acceleration - speed * self.velocity * drag

	-- Stop if we are already slow enough
	if speed < 0.5 then self.velocity = vmath.vector3(0) end
	...
end
```

1. Deklariere den Widerstandswert als Konstante.
2. Berechne das Tempo, mit dem wir uns bewegen.
3. Wende den Widerstand anhand der Formel auf die aktuelle Beschleunigung an
4. Halte an, wenn das Auto bereits langsam genug ist.

## Das vollständige Autoskript {#the-complete-car-script}

Nachdem du die obigen Schritte ausgeführt hast, sollte deine Datei *car.script* so aussehen:

```lua
local turn_speed = 0.1                           				          	-- Slerp factor
local max_steer_angle_left = vmath.quat_rotation_z(math.pi / 6)	    -- 30 degrees
local max_steer_angle_right = vmath.quat_rotation_z(-math.pi / 6)   -- -30 degrees
local steer_angle_zero = vmath.quat_rotation_z(0)				          	-- Zero degrees
local wheels_vector = vmath.vector3(0, 72, 0)         				      -- Vector from center of back and front wheel pairs

local acceleration = 100 		                      									-- The acceleration of the car
local drag = 1.1                                                  	-- the drag constant

function init(self)
	-- Send a message to the render script (see builtins/render/default.render_script) to set the clear color.
	-- This changes the background color of the game. The vector4 contains color information
	-- by channel from 0-1: Red = 0.2. Green = 0.2, Blue = 0.2 and Alpha = 1.0
	msg.post("@render:", "clear_color", { color = vmath.vector4(0.2, 0.2, 0.2, 1.0) } )

	-- Acquire input focus so we can react to input
	msg.post(".", "acquire_input_focus")

	-- Some variables
	self.steer_angle = vmath.quat()
	self.direction = vmath.quat()

	-- Velocity and acceleration are car relative (not rotated)
	self.velocity = vmath.vector3()
	self.acceleration = vmath.vector3()

	-- Input vector. This is modified later in the on_input function
	-- to store the input.
	self.input = vmath.vector3()
end

function update(self, dt)
	-- Set acceleration to the y input
	self.acceleration.y = self.input.y * acceleration

	-- Calculate the new positions of front and back wheels
	local front_vel = vmath.rotate(self.steer_angle, self.velocity)
	local new_front_pos = vmath.rotate(self.direction, wheels_vector + front_vel)
	local new_back_pos = vmath.rotate(self.direction, self.velocity)

	-- Calculate the car's new direction
	local new_dir = vmath.normalize(new_front_pos - new_back_pos)
	self.direction = vmath.quat_rotation_z(math.atan2(new_dir.y, new_dir.x) - math.pi / 2)

	-- Speed is the magnitude of the velocity
	local speed = vmath.length(self.velocity)

	-- Apply drag
	self.acceleration = self.acceleration - speed * self.velocity * drag

	-- Stop if we are already slow enough
	if speed < 0.5 then self.velocity = vmath.vector3() end

	-- Calculate new velocity based on current acceleration
	self.velocity = self.velocity + self.acceleration * dt

	-- Update position based on current velocity and direction
	local pos = go.get_position()
	pos = pos + vmath.rotate(self.direction, self.velocity)
	go.set_position(pos)

	-- Interpolate the wheels using vmath.slerp
	if self.input.x > 0 then
		self.steer_angle = vmath.slerp(turn_speed, self.steer_angle, max_steer_angle_right)
	elseif self.input.x < 0 then
		self.steer_angle = vmath.slerp(turn_speed, self.steer_angle, max_steer_angle_left)
	else
		self.steer_angle = vmath.slerp(turn_speed, self.steer_angle, steer_angle_zero)
	end

	-- Update the wheel rotation
	go.set_rotation(self.steer_angle, "left_wheel")
	go.set_rotation(self.steer_angle, "right_wheel")

	-- Set the game object's rotation to the direction
	go.set_rotation(self.direction)

	-- reset acceleration and input
	self.acceleration = vmath.vector3()
	self.input = vmath.vector3()
end

function on_input(self, action_id, action)
	-- set the input vector to correspond to the key press
	if action_id == hash("left") then
		self.input.x = -1
	elseif action_id == hash("right") then
		self.input.x = 1
	elseif action_id == hash("accelerate") then
		self.input.y = 1
	elseif action_id == hash("brake") then
		self.input.y = -1
	end
end
```

## Das fertige Spiel ausprobieren {#trying-the-final-game}

Wähle nun im Hauptmenü <kbd>Project ▸ Build</kbd> und drehe eine Runde mit deinem neuen Auto!

Damit ist dieses Einführungstutorial abgeschlossen. Hier sind einige Herausforderungen, die du vielleicht selbstständig angehen möchtest:

1. Derzeit bewegt sich das Auto vorwärts und rückwärts mit derselben Beschleunigung. Du könntest dies so ändern, dass das Auto beim Rückwärtsfahren langsamer fährt.
2. Mache einige der Konstanten (wie die Beschleunigung) zu Eigenschaften (`properties`), damit sie für verschiedene Instanzen des Autos geändert werden können.
3. Füge deinem Auto Sounds hinzu und lass es brummen! ([Tipp](/manuals/sound/))

Jetzt kannst du dich weiter mit Defold beschäftigen. Wir haben viele [Handbücher und Tutorials](/learn) vorbereitet, die dich dabei begleiten. Und wenn du nicht weiterkommst, bist du im [Forum](//forum.defold.com) herzlich willkommen.

Viel Spaß mit Defold!
