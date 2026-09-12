---
title: Tasten- und Texteingabe in Defold
brief: Dieses Handbuch erklärt, wie Tasten- und Texteingabe funktionieren.
---

::: sidenote
Es wird empfohlen, dass du dich damit vertraut machst, wie Eingaben in Defold grundsätzlich funktionieren, wie du Eingaben empfängst und in welcher Reihenfolge sie in deinen Skriptdateien empfangen werden. Weitere Informationen zum Eingabesystem findest du im [Handbuch zur Eingabeübersicht](/manuals/input).
:::

# Tastenauslöser {#key-triggers}
Mit Tastenauslösern (key triggers) kannst du einzelne Tasten auf der Tastatur Aktionen im Spiel zuordnen. Jede Taste wird separat einer entsprechenden Aktion zugeordnet. Tastenauslöser verknüpfen bestimmte Tasten mit bestimmten Funktionen, beispielsweise die Bewegung einer Spielfigur mit den Pfeil- oder WASD-Tasten. Wenn du beliebige Tastatureingaben lesen musst, verwende Textauslöser (siehe unten).

![](images/input/key_bindings.png)

```lua
function on_input(self, action_id, action)
    if action_id == hash("left") then
        if action.pressed then
            -- start moving left
        elseif action.released then
            -- stop moving left
        end
    end
end
```

# Textauslöser {#text-triggers}
Textauslöser (text triggers) dienen dazu, beliebige Texteingaben zu lesen. Es gibt zwei Arten von Textauslösern: `text` und `marked-text`.

![](images/input/text_bindings.png)

## Text
Der Auslöser `text` erfasst normale Texteingaben. Er setzt das Feld `text` der Aktionstabelle auf eine Zeichenfolge, die das eingegebene Zeichen enthält. Die Aktion wird nur beim Drücken der Taste ausgelöst; es wird keine Aktion für `release` oder `repeated` gesendet.

```lua
function on_input(self, action_id, action)
    if action_id == hash("text") then
        -- Concatenate the typed character to the "user" node...
        local node = gui.get_node("user")
        local name = gui.get_text(node)
        name = name .. action.text
        gui.set_text(node, name)
    end
end
```

## Markierter Text {#marked-text}
Der Auslöser `marked-text` wird hauptsächlich für asiatische Tastaturen verwendet, bei denen mehrere Tastendrücke einer einzelnen Eingabe entsprechen können. Bei der iOS-Tastatur „Japanese-Kana“ kannst du beispielsweise Kombinationen eingeben. Oben auf der Tastatur werden dann verfügbare Zeichen oder Zeichenfolgen angezeigt, die du eingeben kannst.

![Eingabe von markiertem Text](images/input/marked_text.png)

- Jeder Tastendruck erzeugt eine separate Aktion und setzt das Aktionsfeld `text` auf die aktuell eingegebene Zeichenfolge (den „markierten Text“).
- Wenn du ein Zeichen oder eine Zeichenkombination auswählst, wird eine separate Auslöseraktion vom Typ `text` gesendet (sofern eine solche in der Liste der Eingabebindungen (input bindings) eingerichtet ist). Die separate Aktion setzt das Aktionsfeld `text` auf die endgültige Zeichenfolge.
