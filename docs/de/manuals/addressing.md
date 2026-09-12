---
title: Adressierung in Defold
brief: Dieses Handbuch erklärt, wie Defold das Problem der Adressierung gelöst hat.
---

# Adressierung {#addressing}

Code, der ein laufendes Spiel steuert, muss jedes Spielobjekt (game object) und jede Komponente (component) erreichen können, um das, was Spieler sehen und hören, zu bewegen, zu skalieren, zu animieren, zu löschen und zu verändern. Der Adressierungsmechanismus von Defold macht dies möglich.

## Bezeichner {#identifiers}

Defold verwendet Adressen (oder URLs, aber das lassen wir vorerst außer Acht), um auf Spielobjekte und Komponenten zu verweisen. Diese Adressen bestehen aus Bezeichnern. Im Folgenden siehst du einige Beispiele dafür, wie Defold Adressen verwendet. In diesem Handbuch untersuchen wir im Detail, wie sie funktionieren:

```lua
local id = factory.create("#enemy_factory")
go.set("my_gameobject#my_label", "text", "Hello World!")

local pos = go.get_position("my_gameobject")
go.set_position(pos, "/level/stuff/other_gameobject")

msg.post("#", "hello_there")
local id = go.get_id(".")
```

Beginnen wir mit einem sehr einfachen Beispiel. Angenommen, du hast ein Spielobjekt mit einer einzelnen Sprite-Komponente. Außerdem hast du eine Skriptkomponente, um das Spielobjekt zu steuern. Der Aufbau im Editor würde ungefähr so aussehen:

![bean im Editor](images/addressing/bean_editor.png)

Nun möchtest du das Sprite beim Spielstart deaktivieren, damit du es später erscheinen lassen kannst. Das geht ganz einfach, indem du den folgenden Code in "controller.script" einfügst:

```lua
function init(self)
    msg.post("#body", "disable") -- <1>
end
```
1. Mach dir keine Sorgen, wenn dich das Zeichen '#' verwirrt. Darauf kommen wir gleich zurück.

Das funktioniert wie erwartet. Beim Spielstart *adressiert* die Skriptkomponente die Sprite-Komponente über ihren Bezeichner "body" und verwendet diese Adresse, um ihr eine *Nachricht* namens "disable" zu senden. Diese spezielle Engine-Nachricht bewirkt, dass die Sprite-Komponente die Sprite-Grafik ausblendet. Schematisch sieht der Aufbau so aus:

![bean](images/addressing/bean.png)

Die Bezeichner im Aufbau legst du bei der Entwicklung fest. Sie müssen innerhalb ihres Namenskontexts eindeutig sein. Hier haben wir dem Spielobjekt den Bezeichner "bean" gegeben, seine Sprite-Komponente "body" genannt und die Skriptkomponente, die die Figur steuert, "controller" genannt. Bezeichner, die in URL-Adressen als Zeichenfolgen verwendet werden, sollten weder `:` noch `#` enthalten, da die URL-Syntax `:` als Socket-Trennzeichen und `#` als Trennzeichen zwischen Spielobjekt und Komponente reserviert. Andere Satzzeichen weist der URL-Parser nicht zurück.

::: sidenote
Wenn du keinen Namen wählst, übernimmt das der Editor. Jedes Mal, wenn du im Editor ein neues Spielobjekt oder eine neue Komponente erstellst, wird der Eigenschaft *Id* automatisch ein eindeutiger Wert zugewiesen.

- Spielobjekte erhalten automatisch einen Bezeichner "go" mit fortlaufender Nummer ("go2", "go3" usw.).
- Komponenten erhalten einen Bezeichner, der ihrem Komponententyp entspricht ("sprite", "sprite2" usw.).

Du kannst diese automatisch zugewiesenen Namen beibehalten, wenn du möchtest. Wir empfehlen dir jedoch, die Bezeichner in gute, aussagekräftige Namen zu ändern.
:::

Fügen wir nun eine weitere Sprite-Komponente hinzu und geben bean einen Schild:

![bean](images/addressing/bean_shield_editor.png)

Die neue Komponente muss innerhalb des Spielobjekts eindeutig bezeichnet sein. Wenn du ihr den Namen "body" geben würdest, wäre für den Skriptcode nicht eindeutig, an welches Sprite er die Nachricht "disable" senden soll. Deshalb wählen wir den eindeutigen (und aussagekräftigen) Bezeichner "shield". Jetzt können wir die Sprites "body" und "shield" nach Belieben aktivieren und deaktivieren.

![bean](images/addressing/bean_shield.png)

::: sidenote
Wenn du versuchst, einen Bezeichner mehr als einmal zu verwenden, meldet der Editor einen Fehler. In der Praxis stellt dies daher kein Problem dar:

![bean](images/addressing/name_collision.png)
:::

Sehen wir uns nun an, was passiert, wenn du weitere Spielobjekte hinzufügst. Angenommen, du möchtest zwei „Bohnen“ zu einem kleinen Team zusammenstellen. Du beschließt, eines der Bohnen-Spielobjekte "bean" und das andere "buddy" zu nennen. Außerdem soll "bean", nachdem es eine Weile untätig war, "buddy" mitteilen, dass es anfangen soll zu tanzen. Dazu wird eine benutzerdefinierte Nachricht namens "dance" von der Skriptkomponente "controller" in "bean" an das Skript "controller" in "buddy" gesendet:

![bean](images/addressing/bean_buddy.png)

::: sidenote
Es gibt zwei getrennte Komponenten namens "controller", eine in jedem Spielobjekt. Das ist völlig zulässig, da jedes Spielobjekt einen neuen Namenskontext schafft.
:::

Da sich der Empfänger der Nachricht außerhalb des sendenden Spielobjekts ("bean") befindet, muss der Code angeben, welcher "controller" die Nachricht empfangen soll. Er muss sowohl den Bezeichner des Zielspielobjekts als auch den Bezeichner der Komponente angeben. Die vollständige Adresse der Komponente lautet `"buddy#controller"` und besteht aus zwei getrennten Teilen.

- Zuerst kommt der Bezeichner des Zielspielobjekts ("buddy"),
- dann folgt das Trennzeichen zwischen Spielobjekt und Komponente ("#"),
- und schließlich schreibst du den Bezeichner der Zielkomponente ("controller").

Wenn wir zum vorherigen Beispiel mit einem einzelnen Spielobjekt zurückkehren, sehen wir: Lässt der Code den Spielobjektbezeichner in der Zieladresse weg, kann er Komponenten im *aktuellen Spielobjekt* adressieren.

Zum Beispiel bezeichnet `"#body"` die Adresse der Komponente "body" im aktuellen Spielobjekt. Das ist sehr nützlich, weil dieser Code in *jedem* Spielobjekt funktioniert, solange eine Komponente "body" vorhanden ist.

## Sammlungen {#collections}

Sammlungen (collections) ermöglichen es, Gruppen oder Hierarchien von Spielobjekten zu erstellen und kontrolliert wiederzuverwenden. Du verwendest Sammlungsdateien als Vorlagen (oder „Prototypen“ oder „Prefabs“) im Editor, wenn du dein Spiel mit Inhalten füllst.

Angenommen, du möchtest eine große Anzahl von bean/buddy-Teams erstellen. Eine gute Möglichkeit dafür ist, eine Vorlage in einer neuen *Sammlungsdatei* zu erstellen (nenne sie "team.collection"). Erstelle die Spielobjekte des Teams in der Sammlungsdatei und speichere sie. Füge dann eine Instanz des Inhalts dieser Sammlungsdatei in deine primäre Startsammlung (bootstrap collection) ein und gib der Instanz einen Bezeichner (nenne sie "team_1"):

![bean](images/addressing/team_editor.png)

Mit dieser Struktur kann das Spielobjekt "bean" weiterhin über die Adresse `"buddy#controller"` auf die Komponente "controller" in "buddy" verweisen.

![bean](images/addressing/collection_team.png)

Wenn du eine zweite Instanz von "team.collection" hinzufügst (nenne sie "team_2"), funktioniert der Code in den Skriptkomponenten von "team_2" genauso gut. Die Spielobjektinstanz "bean" aus der Sammlung "team_2" kann die Komponente "controller" in "buddy" weiterhin über die Adresse `"buddy#controller"` adressieren.

![bean](images/addressing/teams_editor.png)

## Relative Adressierung {#relative-addressing}

Die Adresse `"buddy#controller"` funktioniert für die Spielobjekte in beiden Sammlungen, weil es sich um eine *relative* Adresse handelt. Jede der Sammlungen "team_1" und "team_2" schafft einen neuen Namenskontext, oder, wenn du so willst, einen „Namensraum“. Defold vermeidet Namenskonflikte, indem es bei der Adressierung den Namenskontext berücksichtigt, den eine Sammlung schafft:

![Relativer Bezeichner](images/addressing/relative_same.png)

- Innerhalb des Namenskontexts "team_1" sind die Spielobjekte "bean" und "buddy" eindeutig bezeichnet.
- Ebenso sind innerhalb des Namenskontexts "team_2" die Spielobjekte "bean" und "buddy" eindeutig bezeichnet.

Die relative Adressierung funktioniert, indem beim Auflösen einer Zieladresse automatisch der aktuelle Namenskontext vorangestellt wird. Auch das ist äußerst nützlich und leistungsfähig, weil du Gruppen von Spielobjekten mit Code erstellen und sie im gesamten Spiel effizient wiederverwenden kannst.

### Kurzformen {#shorthands}

Defold bietet zwei praktische Kurzformen, mit denen du Nachrichten senden kannst, ohne eine vollständige URL anzugeben:

:[Shorthands](../shared/url-shorthands.md)

## Spielobjektpfade {#game-object-paths}

Um den Mechanismus der Namensvergabe richtig zu verstehen, sehen wir uns an, was passiert, wenn du das Projekt erstellst und ausführst:

1. Der Editor liest die Startsammlung ("main.collection") und ihren gesamten Inhalt (Spielobjekte und andere Sammlungen).
2. Für jedes statische Spielobjekt erstellt der Compiler einen Bezeichner. Diese Bezeichner werden als „Pfade“ aufgebaut, die an der Wurzel der Startsammlung beginnen und entlang der Sammlungshierarchie bis zum Objekt führen. Auf jeder Ebene wird ein Zeichen '/' hinzugefügt.

In unserem obigen Beispiel läuft das Spiel mit den folgenden 4 Spielobjekten:

- /team_1/bean
- /team_1/buddy
- /team_2/bean
- /team_2/buddy

::: sidenote
Bezeichner werden als Hashwerte gespeichert. Die Laufzeitumgebung speichert außerdem den Hashzustand für jeden Sammlungsbezeichner. Dieser wird verwendet, um den Hashvorgang mit einer relativen Zeichenfolge fortzusetzen und so einen absoluten Bezeichner zu erhalten.
:::

Zur Laufzeit existiert die Gruppierung in Sammlungen nicht. Es gibt keine Möglichkeit herauszufinden, zu welcher Sammlung ein bestimmtes Spielobjekt vor der Kompilierung gehörte. Ebenso wenig ist es möglich, alle Objekte einer Sammlung auf einmal zu verändern. Wenn du solche Operationen benötigst, kannst du die Zuordnung leicht selbst im Code verwalten. Der Bezeichner jedes Objekts ist statisch und bleibt garantiert während der gesamten Lebensdauer des Objekts unverändert. Das bedeutet, dass du den Bezeichner eines Objekts bedenkenlos speichern und später verwenden kannst.

## Absolute Adressierung {#absolute-addressing}

Bei der Adressierung kannst du die oben beschriebenen vollständigen Bezeichner verwenden. In den meisten Fällen wird die relative Adressierung bevorzugt, da sie die Wiederverwendung von Inhalten ermöglicht. Es gibt jedoch Fälle, in denen die absolute Adressierung notwendig wird.

Angenommen, du möchtest einen Manager für künstliche Intelligenz (KI), der den Zustand jedes Bohnenobjekts verfolgt. Die Bohnen sollen dem Manager ihren aktiven Status melden, und der Manager soll anhand ihres Status taktische Entscheidungen treffen und ihnen Befehle geben. In diesem Fall wäre es sinnvoll, ein einzelnes Manager-Spielobjekt mit einer Skriptkomponente zu erstellen und es neben den Team-Sammlungen in der Startsammlung zu platzieren.

![Manager-Objekt](images/addressing/manager_editor.png)

Jede Bohne ist dann dafür verantwortlich, Statusnachrichten an den Manager zu senden: "contact", wenn sie einen Feind entdeckt, oder "ouch!", wenn sie getroffen wird und Schaden nimmt. Damit das funktioniert, verwendet das Controller-Skript der Bohne die absolute Adressierung, um Nachrichten an die Komponente "controller" in "manager" zu senden.

Jede Adresse, die mit '/' beginnt, wird von der Wurzel der Spielwelt aus aufgelöst. Diese entspricht der Wurzel der *Startsammlung*, die beim Spielstart geladen wird.

Die absolute Adresse des Manager-Skripts lautet `"/manager#controller"`. Diese absolute Adresse wird zur richtigen Komponente aufgelöst, unabhängig davon, wo sie verwendet wird.

![Teams und Manager](images/addressing/teams_manager.png)

![Absolute Adressierung](images/addressing/absolute.png)

## Gehashte Bezeichner {#hashed-identifiers}

Die Engine speichert alle Bezeichner als Hashwerte. Alle Funktionen, die eine Komponente oder ein Spielobjekt als Argument entgegennehmen, akzeptieren eine Zeichenfolge, einen Hashwert oder ein URL-Objekt. Oben haben wir gesehen, wie Zeichenfolgen zur Adressierung verwendet werden.

Wenn du den Bezeichner eines Spielobjekts abfragst, gibt die Engine immer einen gehashten Bezeichner mit absolutem Pfad zurück:

```lua
local my_id = go.get_id()
print(my_id) --> hash: [/path/to/the/object]

local spawned_id = factory.create("#some_factory")
print(spawned_id) --> hash: [/instance42]
```

Du kannst einen solchen Bezeichner anstelle eines Bezeichners als Zeichenfolge verwenden oder selbst einen erstellen. Beachte jedoch, dass ein gehashter Bezeichner dem Pfad des Objekts entspricht, also einer absoluten Adresse:

::: sidenote
Relative Adressen müssen als Zeichenfolgen angegeben werden, weil die Engine einen neuen Hash-Bezeichner auf Grundlage des Hashzustands des aktuellen Namenskontexts (der Sammlung) berechnet. Dabei wird die angegebene Zeichenfolge zum Hash hinzugefügt.
:::

```lua
local spawned_id = factory.create("#some_factory")
local pos = vmath.vector3(100, 100, 0)
go.set_position(pos, spawned_id)

local other_id = hash("/path/to/the/object")
go.set_position(pos, other_id)

-- This will not work! Relative addresses must be given as strings.
local relative_id = hash("my_object")
go.set_position(pos, relative_id)
```

## URLs

Um das Bild zu vervollständigen, sehen wir uns das vollständige Format von Defold-Adressen an: die URL.

Eine URL ist ein Objekt, das üblicherweise als speziell formatierte Zeichenfolge geschrieben wird. Eine allgemeine URL besteht aus drei Teilen:

`[socket:][path][#fragment]`

socket
: Bezeichnet die Spielwelt des Ziels. Das ist bei der Arbeit mit [Sammlungs-Proxys (collection proxies)](/manuals/collection-proxy) wichtig. Der Socket wird dann verwendet, um die _dynamisch geladene Sammlung_ zu bezeichnen.

path
: Dieser Teil der URL enthält den vollständigen Bezeichner des Zielspielobjekts.

fragment
: Der Bezeichner der Zielkomponente innerhalb des angegebenen Spielobjekts.

Wie wir oben gesehen haben, kannst du in den meisten Fällen einige oder den Großteil dieser Angaben weglassen. Du musst fast nie den Socket angeben. Den Pfad musst du häufig, aber nicht immer angeben. Wenn du Dinge in einer anderen Spielwelt adressieren musst, musst du den Socket-Teil der URL angeben. Die vollständige URL-Zeichenfolge für das Skript "controller" im Spielobjekt "manager" aus dem obigen Beispiel lautet zum Beispiel:

`"main:/manager#controller"`

und für den Controller von buddy in team_2 lautet sie:

`"main:/team_2/buddy#controller"`

Wir können Nachrichten an sie senden:

```lua
-- Send "hello" to the manager script and team buddy bean
msg.post("main:/manager#controller", "hello_manager")
msg.post("main:/team_2/buddy#controller", "hello_buddy")
```

## URL-Objekte erstellen {#constructing-url-objects}

URL-Objekte lassen sich auch programmgesteuert in Lua-Code erstellen:

```lua
-- Construct URL object from a string:
local my_url = msg.url("main:/manager#controller")
print(my_url) --> url: [main:/manager#controller]
print(my_url.socket) --> 786443 (internal numeric value)
print(my_url.path) --> hash: [/manager]
print(my_url.fragment) --> hash: [controller]

-- Construct URL from parameters:
local my_url = msg.url("main", "/manager", "controller")
print(my_url) --> url: [main:/manager#controller]

-- Build from empty URL object:
local my_url = msg.url()
my_url.socket = "main" -- specify by valid name
my_url.path = hash("/manager") -- specify as string or hash
my_url.fragment = "controller" -- specify as string or hash

-- Post to target specified by URL
msg.post(my_url, "hello_manager!")
```
