## Heap-Größe (HTML5) {#heap-size-html5}
Die Heap-Größe eines HTML5-Spiels von Defold lässt sich über das [Feld `heap_size`](/manuals/project-settings/#heap-size) in *game.project* konfigurieren. Achte darauf, den Speicherverbrauch deines Spiels zu optimieren und eine möglichst kleine Heap-Größe festzulegen.

Für kleine Spiele ist eine Heap-Größe von 32 MB erreichbar. Für größere Spiele solltest du 64–128 MB anstreben. Wenn du beispielsweise bei 58 MB liegst und weitere Optimierungen nicht machbar sind, kannst du dich ohne langes Grübeln für 64 MB entscheiden. Es gibt keine feste Zielgröße — sie hängt vom Spiel ab. Strebe möglichst kleine Größen an, idealerweise in Stufen, die Zweierpotenzen entsprechen. 

Um den aktuellen Heap-Verbrauch zu prüfen, kannst du dein Spiel starten, im „ressourcenintensivsten“ Level oder Abschnitt spielen und dabei den Speicherverbrauch beobachten:

```lua
if html5 then
    local mem = tonumber(html5.run("HEAP8.length") / 1024 / 1024)
    print(mem)
end
```

Du kannst auch die Entwicklerwerkzeuge deines Browsers öffnen und Folgendes in die Konsole eingeben:

```js
HEAP8.length / 1024 / 1024
```

Wenn der Speicherverbrauch bei 32 MB bleibt, ist das großartig! Andernfalls befolge die Schritte, um [die Größe der Engine selbst und großer Assets wie Audiodateien und Texturen zu optimieren](/manuals/optimization-size).
