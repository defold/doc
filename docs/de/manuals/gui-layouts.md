---
title: GUI-Layouts in Defold
brief: Defold unterstützt GUIs, die sich automatisch an Änderungen der Bildschirmausrichtung auf Mobilgeräten anpassen. Dieses Dokument erklärt, wie diese Funktion funktioniert.
---

# Layouts

Defold unterstützt GUIs, die sich automatisch an Änderungen der Bildschirmausrichtung auf Mobilgeräten anpassen. Mit dieser Funktion kannst du GUIs gestalten, die sich an die Ausrichtung und das Seitenverhältnis verschiedener Bildschirmgrößen anpassen. Du kannst auch Layouts erstellen, die zu bestimmten Gerätemodellen passen.

## Anzeigeprofile erstellen {#creating-display-profiles}

Standardmäßig ist in den Einstellungen von *game.project* festgelegt, dass eine integrierte Einstellungsdatei für Anzeigeprofile (display profiles) verwendet wird ("builtins/render/default.display_profiles"). Die Standardprofile sind "Landscape" (1280 Pixel breit und 720 Pixel hoch) und "Portrait" (720 Pixel breit und 1280 Pixel hoch). In den Profilen sind keine Gerätemodelle festgelegt, sodass sie auf jedes Gerät passen.

Um eine neue Einstellungsdatei für Profile zu erstellen, kopiere entweder die Datei aus dem Ordner "builtins" oder öffne mit einem <kbd>Rechtsklick</kbd> auf eine geeignete Stelle in der Ansicht *Assets* das Kontextmenü und wähle <kbd>New... ▸ Display Profiles</kbd>. Gib der neuen Datei einen passenden Namen und klicke auf <kbd>Ok</kbd>.

Der Editor öffnet die neue Datei jetzt zum Bearbeiten. Füge neue Profile hinzu, indem du in der Liste *Profiles* auf <kbd>+</kbd> klickst. Füge jedem Profil einen Satz von *Qualifikatoren* (qualifiers) hinzu:

Width
: Die Breite des Qualifikators in Pixeln.

Height
: Die Höhe des Qualifikators in Pixeln.

Device Models
: Eine durch Kommas getrennte Liste von Gerätemodellen. Der Eintrag für das Gerätemodell wird mit dem Anfang des Gerätemodellnamens abgeglichen. Beispielsweise passt `iPhone10` zu Modellen mit dem Namen "iPhone10,\*". Modellnamen mit Kommas sollten in Anführungszeichen eingeschlossen werden. So passt `"iPhone10,3", "iPhone10,6"` zu iPhone-X-Modellen (siehe [iPhone-Wiki](https://www.theiphonewiki.com/wiki/Models)). Beachte, dass nur Android und iOS beim Aufruf von `sys.get_sys_info()` ein Gerätemodell melden. Andere Plattformen geben eine leere Zeichenfolge zurück und wählen deshalb niemals ein Anzeigeprofil aus, das einen Qualifikator für ein Gerätemodell enthält.

![Neue Anzeigeprofile](images/gui-layouts/new_profiles.png)

Du musst außerdem festlegen, dass die Engine deine neuen Profile verwenden soll. Öffne *game.project* und wähle unter *display* in der Einstellung *Display Profiles* die Datei mit den Anzeigeprofilen aus:

![Einstellungen](images/gui-layouts/settings.png)

Wenn die Engine beim Drehen des Geräts automatisch zwischen Hochformat- und Querformatlayouts wechseln soll, aktiviere das Kontrollkästchen *Dynamic Orientation*. Die Engine wählt dynamisch ein passendes Layout aus und ändert die Auswahl auch, wenn sich die Ausrichtung des Geräts ändert.

### Auto Layout Selection (Display Profiles)

Die Ressource für Anzeigeprofile bietet die Option „Auto Layout Selection“ (standardmäßig ON). Wenn sie auf ON gesetzt ist, wählt die Engine automatisch das am besten passende GUI-Layout aus, sowohl beim Erstellen der Szene als auch bei Änderungen der Fenster- oder Bildschirmgröße. Wenn sie auf OFF gesetzt ist, ändert die Engine die Layouts nicht automatisch. Verwende dann `gui.set_layout()` in deinem GUI-Skript, um Layouts manuell zu wechseln. Diese Einstellung wird in der Datei mit den Anzeigeprofilen gespeichert und wirkt sich auf alle GUI-Szenen (GUI scenes) aus.

## GUI-Layouts

Mit den aktuell vorhandenen Anzeigeprofilen kannst du Layoutvarianten für die Anordnung deiner GUI-Knoten (GUI nodes) erstellen. Um einer GUI-Szene ein neues Layout hinzuzufügen, klicke in der Ansicht *Outline* mit der rechten Maustaste auf das Symbol *Layouts* und wähle <kbd>Add ▸ Layout ▸ ...</kbd>:

![Layout zur Szene hinzufügen](images/gui-layouts/add_layout.png)

Beim Bearbeiten einer GUI-Szene werden alle Knoten in einem bestimmten Layout bearbeitet. Das aktuell ausgewählte Layout wird in der Auswahlliste für das Layout der GUI-Szene in der Werkzeugleiste angezeigt. Wenn kein Layout ausgewählt ist, werden die Knoten im Layout *Default* bearbeitet.

![Werkzeugleiste für Layouts](images/gui-layouts/toolbar.png)

![Bearbeiten im Hochformat](images/gui-layouts/portrait.png)

Jede Änderung an einer Knoteneigenschaft, die du bei ausgewähltem Layout vornimmst, _überschreibt_ die Eigenschaft gegenüber dem Layout *Default*. Überschriebene Eigenschaften sind blau markiert. Knoten mit überschriebenen Eigenschaften sind ebenfalls blau markiert. Du kannst auf die Schaltfläche zum Zurücksetzen neben einer überschriebenen Eigenschaft klicken, um sie auf ihren ursprünglichen Wert zurückzusetzen.

![Bearbeiten im Querformat](images/gui-layouts/landscape.png)

Ein Layout kann keine Knoten löschen oder neu erstellen, sondern nur Eigenschaften überschreiben. Wenn du einen Knoten aus einem Layout entfernen musst, kannst du ihn entweder außerhalb des Bildschirms verschieben oder mithilfe von Skriptlogik löschen. Achte außerdem auf das aktuell ausgewählte Layout. Wenn du deinem Projekt ein Layout hinzufügst, wird das neue Layout anhand des aktuell ausgewählten Layouts eingerichtet. Auch beim Kopieren und Einfügen von Knoten wird das aktuell ausgewählte Layout berücksichtigt, sowohl beim Kopieren *als auch* beim Einfügen.

## Dynamische Profilauswahl {#dynamic-profile-selection}

Wenn Auto Layout Selection aktiviert ist, wählt die Engine automatisch das am besten passende Layout aus. Beim dynamischen Layoutabgleich wird jeder Qualifikator eines Anzeigeprofils nach den folgenden Regeln bewertet:

1. Wenn kein Gerätemodell festgelegt ist oder das Gerätemodell übereinstimmt, wird für den Qualifikator ein Bewertungswert (S) berechnet.

2. Der Bewertungswert (S) wird aus der Fläche des Bildschirms (A), der Fläche des Qualifikators (A_Q), dem Seitenverhältnis des Bildschirms (R) und dem Seitenverhältnis des Qualifikators (R_Q) berechnet:

<img src="https://latex.codecogs.com/svg.latex?\inline&space;S=\left|1&space;-&space;\frac{A}{A_Q}\right|&space;&plus;&space;\left|1&space;-&space;\frac{R}{R_Q}\right|" title="S=\left|1 - \frac{A}{A_Q}\right| + \left|1 - \frac{R}{R_Q}\right|" />

3. Das Profil, dessen Qualifikator den niedrigsten Bewertungswert hat, wird ausgewählt, wenn die Ausrichtung des Qualifikators (Quer- oder Hochformat) mit der des Bildschirms übereinstimmt.

4. Wenn kein Profil mit einem Qualifikator derselben Ausrichtung gefunden wird, wird das Profil mit dem am besten bewerteten Qualifikator der anderen Ausrichtung ausgewählt.

5. Wenn kein Profil ausgewählt werden kann, wird das Ersatzprofil *Default* verwendet.

Da das Layout *Default* zur Laufzeit als Ersatz dient, wenn es kein besser passendes Layout gibt, ist ein hinzugefügtes Layout "Landscape" für *alle* Ausrichtungen die beste Übereinstimmung, bis du auch ein Layout "Portrait" hinzufügst.

## Nachrichten bei Layoutänderungen {#layout-change-messages}

Wenn sich das Layout ändert, wird eine Nachricht `layout_changed` an das Skript der GUI-Komponente (GUI component) gesendet. Das geschieht, wenn die Engine das Layout automatisch ändert (Auto Layout Selection auf ON) oder wenn dein Skript `gui.set_layout()` aufruft und sich das Layout tatsächlich ändert. Die Nachricht enthält den gehashten Bezeichner des Layouts, sodass das Skript abhängig vom ausgewählten Layout Logik ausführen kann:

```lua
function on_message(self, message_id, message, sender)
  if message_id == hash("layout_changed") and message.id == hash("My Landscape") then
    -- switching layout to landscape
  elseif message_id == hash("layout_changed") and message.id == hash("My Portrait") then
    -- switching layout to portrait
  end
end
```

Außerdem erhält das aktuelle Render-Skript bei jeder Änderung des Fensters (der Spielansicht) eine Nachricht. Dazu gehören auch Änderungen der Ausrichtung.

```lua
function on_message(self, message_id, message)
  if message_id == hash("window_resized") then
    -- The window was resized. message.width and message.height contain the
    -- new dimensions of the window.
  end
end
```

Wenn die Ausrichtung wechselt, skaliert der GUI-Layoutmanager die GUI-Knoten automatisch und positioniert sie anhand deines Layouts und der Knoteneigenschaften neu. Spielinhalte werden dagegen standardmäßig in einem separaten Renderdurchlauf mit einer Projektion gerendert, die sie durch Strecken in das aktuelle Fenster einpasst. Um dieses Verhalten zu ändern, verwende entweder ein eigenes angepasstes Render-Skript oder eine Kamera-[Bibliothek](/assets/).

## Manuelle Layoutauswahl (Lua) {#manual-layout-selection-lua}

Wenn Auto Layout Selection für die verwendeten Anzeigeprofile auf OFF gesetzt ist, wechselt die Engine die Layouts nicht automatisch. Verwende die folgenden Funktionen in einem GUI-Skript, um Layouts manuell zu verwalten:

### gui.set_layout(layout)

- Akzeptiert eine Zeichenfolge oder einen Hashwert (Layout-Bezeichner).
- Gibt einen booleschen Wert zurück: `true`, wenn das Layout in der Szene vorhanden ist und angewendet wurde, andernfalls `false`.
- Wenn das Layout in den Anzeigeprofilen vorhanden ist, wird die Szenenauflösung auf die Breite/Höhe des Profils aktualisiert.
- Sendet `layout_changed`, wenn sich das Layout tatsächlich ändert.

Beispiel:

```lua
function init(self)
    -- Manually apply the "Portrait" layout
    local ok = gui.set_layout("Portrait")
    if not ok then
        print("Portrait layout not found in this scene")
    end
end
```

### gui.get_layouts()

- Gibt eine Tabelle zurück, die dem Hashwert jedes Layout-Bezeichners `vmath.vector3(width, height, 0)` zuordnet.
- Gibt für das Standardlayout die aktuelle Szenenauflösung zurück.

Beispiel:

```lua
local layouts = gui.get_layouts()
for id, size in pairs(layouts) do
    print(id, size.x, size.y)
end
```

Hinweis: Wenn ein GUI-Layout in der Szene vorhanden ist, aber in den Anzeigeprofilen fehlt, wendet `gui.set_layout()` weiterhin die layoutspezifischen Überschreibungen der Knoteneigenschaften an, ändert jedoch die Szenenauflösung nicht.
