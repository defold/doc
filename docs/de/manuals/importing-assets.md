---
title: Assets importieren und bearbeiten
brief: Dieses Handbuch beschreibt, wie du Assets importierst und bearbeitest.
---

# Assets importieren und bearbeiten {#importing-and-editing-assets}

Ein Spielprojekt besteht in der Regel aus einer großen Anzahl externer Assets, die in verschiedenen spezialisierten Programmen zur Erstellung von Grafiken, 3D-Modellen, Audiodateien, Animationen und anderen Inhalten entstehen. Defold ist auf einen Arbeitsablauf ausgelegt, bei dem du in deinen externen Werkzeugen arbeitest und die Assets nach ihrer Fertigstellung in Defold importierst.


## Assets importieren {#importing-assets}

Alle Assets, die du in deinem Projekt verwendest, müssen sich in der Projekthierarchie befinden. Deshalb musst du alle Assets importieren, bevor du sie verwenden kannst. Ziehe dazu einfach die Dateien aus dem Dateisystem deines Computers an eine geeignete Stelle im Bereich *Assets* des Defold-Editors und lege sie dort ab.

![Dateien importieren](images/graphics/import.png)

::: sidenote
Defold unterstützt Bilder in den Bildformaten PNG und JPEG. PNG-Bilder müssen im RGBA-Format mit 32 Bit vorliegen. Andere Bildformate müssen konvertiert werden, bevor sie verwendet werden können.
:::


## Assets verwenden {#using-assets}

Nach dem Import in Defold können die Assets von den verschiedenen Arten von Komponenten (components) verwendet werden, die Defold unterstützt:

* Mit Bildern kannst du viele Arten visueller Komponenten erstellen, die häufig in 2D-Spielen verwendet werden. Lies hier mehr darüber, [wie du 2D-Grafiken importierst und verwendest](/manuals/importing-graphics).
* Audiodateien können von der [Audiokomponente (Sound component)](/manuals/sound) zur Audiowiedergabe verwendet werden.
* Schriftarten werden von der [Beschriftungskomponente (Label component)](/manuals/label) und von [Textknoten](/manuals/gui-text) in einer GUI verwendet.
* glTF-Modelle (*.gltf* und *.glb*) können von der [Modellkomponente (Model component)](/manuals/model) verwendet werden, um 3D-Modelle mit Animationen anzuzeigen. Importiere alle vom Modell verwendeten Texturbilder als separate Assets und weise sie den Textureigenschaften des Materials der Modellkomponente zu. Lies hier mehr darüber, [wie du 3D-Modelle importierst und verwendest](/manuals/importing-models).


## Externe Assets bearbeiten {#editing-external-assets}

Defold bietet keine Bearbeitungswerkzeuge für Bilder, Audiodateien, Modelle oder Animationen. Solche Assets müssen außerhalb von Defold mit spezialisierten Werkzeugen erstellt und in Defold importiert werden. Defold erkennt automatisch Änderungen an allen Assets in deinen Projektdateien und aktualisiert die Editoransicht entsprechend.


## Defold-Assets bearbeiten {#editing-defold-assets}

Der Editor speichert alle Defold-Assets in textbasierten Dateien, die sich gut zusammenführen lassen. Sie lassen sich auch leicht mit einfachen Skripten erstellen und ändern. Weitere Informationen findest du in [diesem Forenthema](https://forum.defold.com/t/deftree-a-python-module-for-editing-defold-files/15210). Beachte jedoch, dass das Defold-Team die Details seiner Dateiformate nicht veröffentlicht, da sich diese gelegentlich ändern. Du kannst auch [Editor-Skripte](/manuals/editor-scripts/) verwenden, um auf bestimmte Lebenszyklusereignisse im Editor zu reagieren und dabei Skripte auszuführen, die Assets erzeugen oder ändern.

Wenn du Defold-Asset-Dateien mit einem Texteditor oder einem externen Werkzeug bearbeitest, solltest du besonders vorsichtig sein. Falls du dabei Fehler einführst, können diese verhindern, dass sich die Datei im Defold-Editor öffnen lässt.

Einige externe Werkzeuge wie [Tiled](/assets/tiled/) und [Tilesetter](https://www.tilesetter.org/beta) können Defold-Assets automatisch erzeugen.
