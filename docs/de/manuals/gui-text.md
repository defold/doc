---
title: GUI-Textknoten in Defold
brief: Dieses Handbuch beschreibt, wie du Text zu GUI-Szenen hinzufügst.
---

# GUI-Textknoten {#gui-text-nodes}

Defold unterstützt eine spezielle Art von GUI-Knoten (GUI node), mit der sich Text in einer GUI-Szene rendern lässt. Jede Schriftressource, die einem Projekt hinzugefügt wurde, kann zum Rendern von Textknoten (text nodes) verwendet werden.

Die Editorvorschau unterstützt die Formung von Schriftzeichen (text shaping) und Layouts von rechts nach links mithilfe des Schriftrenderers der Engine. Die erforderlichen Einstellungen für die Schriftart und das Anwendungsmanifest (App Manifest) findest du unter [Unterstützung für Textlayout](/manuals/font/#text-layout-support-eg-right-to-left).

## Textknoten hinzufügen {#adding-text-nodes}

Die Schriftarten, die du in GUI-Textknoten verwenden möchtest, müssen zur GUI-Komponente (GUI component) hinzugefügt werden. Klicke dazu entweder mit der rechten Maustaste auf den Ordner *Fonts*, verwende das Menü <kbd>GUI</kbd> in der Menüleiste oder drücke die entsprechende Tastenkombination.

![Schriftarten](images/gui-text/fonts.png)

Textknoten haben eine Reihe besonderer Eigenschaften:

*Font*
: Bei jedem Textknoten, den du erstellst, muss die Eigenschaft *Font* festgelegt sein.

*Text*
: Diese Eigenschaft enthält den angezeigten Text.

*Line Break*
: Die Textausrichtung richtet sich nach der Einstellung des Bezugspunkts (pivot). Wenn du diese Eigenschaft aktivierst, kann der Text über mehrere Zeilen fließen. Die Breite des Knotens bestimmt, wo der Text umgebrochen wird.

## Vektorschriftarten und farbige Emojis {#vector-fonts-and-color-emoji}

Folge der [Einrichtung für Vektorschriftarten](/manuals/font/#vector-fonts), füge die `.font`-Ressource zu *Fonts* der GUI-Szene hinzu und wähle sie am Textknoten aus. Setze *Material* der Schriftartenressource auf `/builtins/fonts/font-vector.material`. Steuere die angezeigte Größe mit *Font Size* des Knotens.

Führe für farbige Emojis zusätzlich die [Einrichtung der COLRv1-Ausweichschrift und des Bundles](/manuals/font/#color-emoji) durch. Erstelle einen Textknoten mit der ID `text`, lasse *Text* leer und füge Folgendes zur `.gui_script` der GUI-Szene hinzu:

```lua
function init(self)
    local node = gui.get_node("text")
    local text = "Hello 😀 🍎 🚀"
    local font_resource = gui.get_font_resource(gui.get_font(node))
    -- Add the fallback once for this shared font resource.
    font.add_font(font_resource, "/fonts/NotoColorEmoji-Regular.ttf")
    font.prewarm_text(font_resource, text, function(self, request_id, result, err)
        if result then
            gui.set_text(node, text)
        else
            print("Could not prepare GUI text:", err)
        end
    end)
end
```

[`gui.get_font()`](/ref/gui/#gui.get_font) gibt den Schriftartennamen innerhalb der GUI-Szene zurück; [`gui.get_font_resource()`](/ref/gui/#gui.get_font_resource) löst diesen Namen zur Schriftartenressource auf, die `font.add_font()` verwendet. Andere Knoten und Beschriftungen mit derselben Ressource erhalten die Ausweichschrift ebenfalls; initialisiere sie daher nur einmal. Der Text wird nach erfolgreicher Vorbereitung gesetzt.

## Ausrichtung {#alignment}

Indem du den Bezugspunkt des Knotens festlegst, kannst du den Ausrichtungsmodus für den Text ändern.

*Zentriert*
: Wenn der Bezugspunkt auf `Center`, `North` oder `South` eingestellt ist, wird der Text zentriert.

*Linksbündig*
: Wenn der Bezugspunkt auf einen der `West`-Modi eingestellt ist, wird der Text linksbündig ausgerichtet.

*Rechtsbündig*
: Wenn der Bezugspunkt auf einen der `East`-Modi eingestellt ist, wird der Text rechtsbündig ausgerichtet.

![Textausrichtung](images/gui-text/align.png)

## Textknoten zur Laufzeit ändern {#modifying-text-nodes-in-runtime}

Textknoten unterstützen alle allgemeinen Funktionen zur Bearbeitung von Knoten, mit denen sich Größe, Bezugspunkt, Farbe und weitere Eigenschaften festlegen lassen. Einige Funktionen sind ausschließlich für Textknoten vorgesehen:

* Um die Schriftart eines Textknotens zu ändern, verwende die Funktion [`gui.set_font()`](/ref/gui/#gui.set_font).
* Um das Verhalten beim Zeilenumbruch eines Textknotens zu ändern, verwende die Funktion [`gui.set_line_break()`](/ref/gui/#gui.set_line_break).
* Um den Inhalt eines Textknotens zu ändern, verwende die Funktion [`gui.set_text()`](/ref/gui/#gui.set_text).

```lua
function on_message(self, message_id, message, sender)
    if message_id == hash("set_score") then
        local s = gui.get_node("score")
        gui.set_text(s, message.score)
    end
end
```
