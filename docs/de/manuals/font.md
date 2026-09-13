---
title: Handbuch zu Schriftarten in Defold
brief: Dieses Handbuch beschreibt, wie Defold mit Schriftarten umgeht und wie du Text in deinen Spielen auf dem Bildschirm darstellst.
---

# Schriftdateien {#font-files}

Schriftarten werden verwendet, um Text in Beschriftungskomponenten (label components) und GUI-Textknoten zu rendern. Defold unterstützt mehrere Schriftdateiformate:

- TrueType
- OpenType
- BMFont

Seit Defold 1.13.2 unterstützen sowohl die bisherige als auch die vollständige Textlayout-Engine TrueType-Konturen und OpenType-CFF1/CFF2-Konturen, einschließlich der Erzeugung zur Laufzeit aus `.ttf`- und `.otf`-Ressourcen.

Informationen zum Gestalten einzelner Textabschnitte und zum Arbeiten mit Links und eingebetteten Sprites findest du im [Handbuch zur Rich-Text-Auszeichnung](/manuals/font-richtext).

Schriftarten, die du deinem Projekt hinzufügst, werden automatisch in ein Texturformat umgewandelt, das Defold rendern kann. Es stehen zwei Verfahren zum Rendern von Schriftarten zur Verfügung, die jeweils eigene Vor- und Nachteile haben:

- Bitmap
- Distanzfeld

## Offline- oder Laufzeitschriftarten {#offline-or-runtime-fonts}

Standardmäßig erfolgt die Umwandlung in gerasterte Glyphenbilder während des Builds (offline). Das hat den Nachteil, dass für jede Schriftart während des Builds alle möglichen Glyphen gerastert werden müssen. Dabei können sehr große Texturen entstehen, die Speicher belegen und außerdem das Bundle vergrößern.

Bei Verwendung von „Laufzeitschriftarten“ (runtime fonts) werden die `.ttf`- und `.otf`-Schriftarten unverändert in das Bundle aufgenommen, und die Rasterisierung erfolgt bei Bedarf zur Laufzeit. Das minimiert sowohl den Speicherverbrauch zur Laufzeit als auch die Bundle-Größe.

## Unterstützung für Textlayout (z. B. von rechts nach links) {#text-layout-support-eg-right-to-left}

Laufzeitschriftarten bieten außerdem den Vorteil, vollständiges Textlayout zu unterstützen, z. B. von rechts nach links.
Das Defold-Team verwendet dafür derzeit die Bibliotheken [HarfBuzz](https://github.com/harfbuzz/harfbuzz), [SheenBidi](https://github.com/Tehreer/SheenBidi), [libunibreak](https://github.com/adah1972/libunibreak) und [SkriBidi](https://github.com/memononen/Skribidi).

Siehe [Laufzeitschriftarten aktivieren](/manuals/font#enabling-runtime-fonts)

Der Editor verwendet den Schrift-Renderer der Engine für die Vorschau von Schriftarten und Text in Szenen. Die Ausformung von Text (text shaping) und das Layout von rechts nach links erfordern [Laufzeitschriftarten](#enabling-runtime-fonts) und die Option **Use full text layout system** im Anwendungsmanifest. Bei Offline-Schriftarten berücksichtigt die Vorschau die Einstellungen **Characters** und **All Chars** der Schriftart.

## Schriftsammlung {#font-collection}

Das Dateiformat `.fontc` wird auch als Schriftsammlung (font collection) bezeichnet. Im Offline-Modus ist ihm nur eine Schriftart zugeordnet.
Wenn du Laufzeitschriftarten verwendest, kannst du einer Schriftsammlung mehr als eine Schriftdatei (`.ttf` oder `.otf`) zuordnen.

So kannst du eine Schriftsammlung zum Rendern mehrerer Texte in unterschiedlichen Sprachen verwenden und gleichzeitig den Speicherbedarf gering halten.
Du kannst beispielsweise eine Sammlung mit der japanischen Schriftart laden, diese Schriftart der aktuellen Hauptschriftart zuordnen und anschließend die japanische Schriftsammlung entladen.

## Eine Schriftressource erstellen {#creating-a-font}

Um eine Schriftressource zur Verwendung in Defold zu erstellen, lege eine neue Font-Datei an. Wähle dazu im Menü <kbd>File ▸ New...</kbd> und anschließend <kbd>Font</kbd>. Du kannst auch an einer Stelle im Browser *Assets* einen <kbd>Rechtsklick</kbd> ausführen und <kbd>New... ▸ Font</kbd> wählen.

![Name der neuen Schriftressource](images/font/new_font_name.png)

Gib der neuen Schriftressource einen Namen und klicke auf <kbd>Ok</kbd>. Die neue Schriftressource wird nun im Editor geöffnet.

![Neue Schriftressource](images/font/new_font.png)

Ziehe die Schriftart, die du verwenden möchtest, in den Browser *Assets* und lege sie an einer geeigneten Stelle ab.

Setze die Eigenschaft *Font* auf die Schriftdatei und passe die Schrifteigenschaften nach Bedarf an.

## Eigenschaften {#properties}

*Font*
: Die TTF-, OTF- oder *`.fnt`*-Datei, aus der die Schriftdaten erzeugt werden.

*Material*
: Das Material, das zum Rendern dieser Schriftart verwendet wird. Achte darauf, es für Distanzfeldschriften und BMFonts zu ändern (Einzelheiten dazu findest du weiter unten).

*Output Format*
: Der Typ der erzeugten Schriftdaten.

  - `TYPE_BITMAP` wandelt die importierte OTF- oder TTF-Datei in eine Schriftbogentextur um, deren Bitmap-Daten zum Rendern von Textknoten verwendet werden. Die Farbkanäle codieren die Zeichenform, den Umriss und den Schlagschatten. Bei *`.fnt`*-Dateien wird die Bitmap der Quelltextur unverändert verwendet.
  - `TYPE_DISTANCE_FIELD` Die importierte Schriftart wird in eine Schriftbogentextur umgewandelt, deren Pixeldaten Abstände zum Rand der Schriftzeichen statt Bildschirmpixel darstellen. Einzelheiten findest du weiter unten.

*Render Mode*
: Der Rendermodus für das Rendern von Glyphen.

  - `MODE_SINGLE_LAYER` erzeugt für jedes Zeichen ein einzelnes Quad.
  - `MODE_MULTI_LAYER` erzeugt separate Quads für die Glyphenform, den Umriss und die Schatten. Die Ebenen werden von hinten nach vorne gerendert. Dadurch verdeckt ein Zeichen keine zuvor gerenderten Zeichen, wenn der Umriss breiter als der Abstand zwischen den Glyphen ist. Dieser Rendermodus ermöglicht außerdem den korrekten Versatz des Schlagschattens entsprechend den Eigenschaften Shadow X/Y in der Schriftressource.

*Size*
: Die Zielgröße der Glyphen in Pixeln.

*Antialias*
: Gibt an, ob die Schriftart beim Übertragen in die Ziel-Bitmap mit Kantenglättung versehen werden soll. Setze den Wert auf 0, wenn du die Schrift pixelgenau rendern möchtest.

*Alpha*
: Die Transparenz der Glyphe. 0.0--1.0, wobei 0.0 transparent und 1.0 undurchsichtig bedeutet.

*Outline Alpha*
: Die Transparenz des erzeugten Umrisses. 0.0--1.0.

*Outline Width*
: Die Breite des erzeugten Umrisses in Pixeln. Setze den Wert auf 0, um keinen Umriss zu erzeugen.

*Shadow Alpha*
: Die Transparenz des erzeugten Schattens. 0.0--1.0.

::: sidenote
Die Shader der integrierten Schriftmaterialien ermöglichen Schatten sowohl im einlagigen als auch im mehrlagigen Rendermodus. Wenn du weder mehrlagiges Schriftrendering noch Schatten benötigst, verwendest du am besten einen einfacheren Shader wie *`builtins/font-singlelayer.fp`*.
:::

*Shadow Blur*
: Bei Bitmap-Schriften gibt diese Einstellung an, wie oft ein kleiner Weichzeichnungskern auf jede Glyphe der Schriftart angewendet wird. Bei Distanzfeldschriften entspricht sie der tatsächlichen Breite der Weichzeichnung in Pixeln.

*Shadow X/Y*
: Der horizontale und vertikale Versatz des erzeugten Schattens in Pixeln. Diese Einstellung wirkt sich nur auf den Glyphenschatten aus, wenn Render Mode auf `MODE_MULTI_LAYER` gesetzt ist.

*Characters*
: Die Zeichen, die in die Schriftart aufgenommen werden sollen. Standardmäßig enthält dieses Feld die druckbaren ASCII-Zeichen (Zeichencodes 32-126). Du kannst in diesem Feld Zeichen hinzufügen oder entfernen, um mehr oder weniger Zeichen in die Schriftart aufzunehmen.

Bei Laufzeitschriftarten dient dieser Text dazu, den Cache mit den passenden Glyphen vorab zu füllen. Dies geschieht beim Laden. Siehe `font.prewarm_text()`.

::: sidenote
Die druckbaren ASCII-Zeichen sind:
Leerzeichen ! " # $ % & ' ( ) * + , - . / 0 1 2 3 4 5 6 7 8 9 : ; < = > ? @ A B C D E F G H I J K L M N O P Q R S T U V W X Y Z [ \ ] ^ _ \` a b c d e f g h i j k l m n o p q r s t u v w x y z { | } ~
:::

*All Chars*
: Wenn du diese Eigenschaft aktivierst, werden alle in der Quelldatei verfügbaren Glyphen in die Ausgabe aufgenommen.

*Cache Width/Height*
: Begrenzt die Größe der Bitmap für den Glyphen-Cache. Wenn die Engine Text rendert, sucht sie die Glyphe in der Cache-Bitmap. Ist sie dort nicht vorhanden, wird sie vor dem Rendern zum Cache hinzugefügt. Wenn die Cache-Bitmap zu klein ist, um alle von der Engine zu rendernden Glyphen aufzunehmen, wird ein Fehler gemeldet (`ERROR:RENDER: Out of available cache cells! Consider increasing cache_width or cache_height for the font.`).

  Bei einem Wert von 0 wird die Cache-Größe automatisch festgelegt und kann auf höchstens 2048x4096 anwachsen.

## Distanzfeldschriften {#distance-field-fonts}

Distanzfeldschriften (distance field fonts) speichern statt Bitmap-Daten den Abstand zum Rand der Glyphe in der Textur. Wenn die Engine die Schriftart rendert, ist ein spezieller Shader erforderlich, der die Abstandsdaten interpretiert und damit die Glyphe zeichnet. Distanzfeldschriften benötigen mehr Ressourcen als Bitmap-Schriften, bieten aber mehr Flexibilität bei der Größenänderung.

![Distanzfeldschrift](images/font/df_font.png)

Achte beim Erstellen der Schriftressource darauf, die Eigenschaft *Material* auf *`builtins/fonts/font-df.material`* (oder ein anderes Material, das Distanzfelddaten verarbeiten kann) zu setzen. Andernfalls verwendet die Schriftart beim Rendern auf den Bildschirm nicht den richtigen Shader.

## Bitmap-Schriften im BMFont-Format {#bitmap-bmfonts}

Neben erzeugten Bitmaps unterstützt Defold vorab gerasterte Bitmap-Schriften im Format „BMFont“. Diese Schriftarten bestehen aus einem PNG-Schriftbogen mit allen Glyphen. Zusätzlich enthält eine *`.fnt`*-Datei Angaben dazu, wo sich jede Glyphe auf dem Bogen befindet, sowie Informationen zu Größe und Unterschneidung. (Beachte, dass Defold die XML-Version des *`.fnt`*-Formats, die Phaser und einige andere Werkzeuge verwenden, nicht unterstützt.)

Diese Schriftarten bieten keinen Leistungsvorteil gegenüber Bitmap-Schriften, die aus TrueType- oder OpenType-Schriftdateien erzeugt werden. Sie können jedoch beliebige Grafiken, Farben und Schatten direkt im Bild enthalten.

Füge die erzeugten Dateien *`.fnt`* und *`.png`* deinem Defold-Projekt hinzu. Diese Dateien sollten sich im selben Ordner befinden. Erstelle eine neue Schriftressource und setze die Eigenschaft *font* auf die *`.fnt`*-Datei. Achte darauf, dass *output_format* auf `TYPE_BITMAP` gesetzt ist. Defold erzeugt keine Bitmap, sondern verwendet die im PNG bereitgestellte.

::: sidenote
Um eine BMFont zu erstellen, benötigst du ein Werkzeug, das die entsprechenden Dateien erzeugen kann. Dafür gibt es mehrere Möglichkeiten:

* [Bitmap Font Generator](http://www.angelcode.com/products/bmfont/), ein nur für Windows verfügbares Werkzeug von AngelCode.
* [Shoebox](http://renderhjs.net/shoebox/), eine kostenlose Anwendung für Windows und macOS auf Basis von Adobe Air.
* [Hiero](https://libgdx.com/wiki/tools/hiero), ein Open-Source-Werkzeug auf Basis von Java.
* [Glyph Designer](https://71squared.com/glyphdesigner), ein kommerzielles macOS-Werkzeug von 71 Squared.
* [bmGlyph](https://www.bmglyph.com), ein kommerzielles macOS-Werkzeug von Sovapps.
:::

![BMFont](images/font/bm_font.png)

Damit die Schriftart korrekt gerendert wird, vergiss beim Erstellen der Schriftressource nicht, die Materialeigenschaft auf *`builtins/fonts/font-fnt.material`* zu setzen.

## Artefakte und bewährte Vorgehensweisen {#artifacts-and-best-practices}

Bitmap-Schriften eignen sich im Allgemeinen am besten, wenn die Schriftart ohne Skalierung gerendert wird. Sie lassen sich schneller auf den Bildschirm rendern als Distanzfeldschriften.

Distanzfeldschriften lassen sich sehr gut vergrößern. Bitmap-Schriften bestehen dagegen nur aus Pixelbildern: Beim Vergrößern der Schriftart wachsen auch die Pixel, wodurch blockartige Artefakte entstehen. Das folgende Beispiel zeigt eine Schriftgröße von 48 Pixeln, die auf das 4-Fache vergrößert wurde.

![Vergrößerte Schriftarten](images/font/scale_up.png)

Beim Verkleinern kann die GPU Bitmap-Texturen ansprechend und effizient skalieren und mit Kantenglättung versehen. Eine Bitmap-Schrift behält ihre Farbe besser bei als eine Distanzfeldschrift. Hier siehst du eine vergrößerte Ansicht derselben Beispielschrift mit einer Größe von 48 Pixeln, verkleinert auf 1/5 ihrer Größe:

![Verkleinerte Schriftarten](images/font/scale_down.png)

Distanzfeldschriften müssen in einer Zielgröße gerendert werden, die groß genug ist, um Abstandsinformationen zur Darstellung der Kurven ihrer Glyphen aufzunehmen. Dies ist dieselbe Schriftart wie oben, jedoch mit einer Größe von 18 Pixeln und auf das 10-Fache vergrößert. Es ist deutlich erkennbar, dass diese Größe zu klein ist, um die Formen dieser Schrift zu codieren:

![Artefakte bei Distanzfeldschriften](images/font/df_artifacts.png)

Wenn du keine Schatten oder Umrisse benötigst, setze deren jeweilige Alphawerte auf null. Andernfalls werden weiterhin Schatten- und Umrissdaten erzeugt, die unnötig Speicher belegen.

## Schrift-Cache {#font-cache}
Eine Schriftressource in Defold führt zur Laufzeit zu zwei Dingen: einer Textur und den Schriftdaten.

* Die Schriftdaten bestehen aus einer Liste von Glypheneinträgen, die jeweils grundlegende Informationen zur Unterschneidung und die Bitmap-Daten der Glyphe enthalten.
* Die Textur wird intern „Glyphen-Cache-Textur“ genannt und beim Rendern von Text mit einer bestimmten Schriftart verwendet.

Zur Laufzeit durchläuft die Engine beim Rendern von Text zunächst die zu rendernden Glyphen, um zu prüfen, welche davon im Textur-Cache verfügbar sind. Für jede Glyphe, die im Glyphen-Textur-Cache fehlt, werden die in den Schriftdaten gespeicherten Bitmap-Daten in die Textur hochgeladen.

Jede Glyphe wird intern entsprechend der Schriftgrundlinie im Cache platziert. Dadurch lassen sich in einem Shader die lokalen Texturkoordinaten der Glyphe innerhalb ihrer zugehörigen Cache-Zelle berechnen. So kannst du bestimmte Texteffekte wie Farbverläufe oder Texturüberlagerungen dynamisch umsetzen. Die Engine stellt dem Shader über die spezielle Shader-Konstante `texture_size_recip` Kennwerte zum Cache bereit. Ihre Vektorkomponenten enthalten folgende Informationen:

* `texture_size_recip.x` ist der Kehrwert der Cache-Breite
* `texture_size_recip.y` ist der Kehrwert der Cache-Höhe
* `texture_size_recip.z` ist das Verhältnis der Cache-Zellenbreite zur Cache-Breite
* `texture_size_recip.w` ist das Verhältnis der Cache-Zellenhöhe zur Cache-Höhe

Um beispielsweise in einem Fragment-Shader einen Farbverlauf zu erzeugen, schreibe einfach:

`float horizontal_gradient = fract(var_texcoord0.y / texture_size_recip.w);`

Weitere Informationen zu Shader-Uniforms findest du im [Shader-Handbuch](/manuals/shader).

## Laufzeitschriftarten aktivieren {#enabling-runtime-fonts}

Für Schriftarten vom Typ SDF ist die Erzeugung zur Laufzeit möglich, wenn du TrueType- (`.ttf`) oder OpenType-Schriftarten (`.otf`) verwendest. Die Erzeugung zur Laufzeit aus `.otf`-Ressourcen wird seit Defold 1.13.2 unterstützt.
Dieser Ansatz kann die Downloadgröße und den Speicherverbrauch eines Defold-Spiels zur Laufzeit erheblich reduzieren.
Der kleine Nachteil besteht darin, dass die Erzeugung jeder Glyphe asynchron erfolgt.

* Aktiviere die Funktion, indem du `font.runtime_generation` in game.project setzt.

* Füge ein [Anwendungsmanifest](/manuals/app-manifest) hinzu und aktiviere die Option `Use full text layout system`.
Dadurch wird eine angepasste Engine erstellt, in der diese Funktion aktiviert ist.

::: sidenote
Diese Funktion ist derzeit experimentell, soll aber in Zukunft zum Standardarbeitsablauf werden.
:::

::: important
Die Einstellung `font.runtime_generation` wirkt sich auf alle `.ttf`- und `.otf`-Schriftarten im Projekt aus.
:::


### Schriftarten per Skript steuern {#font-scripting}

#### Den Glyphen-Cache vorab füllen {#prewarming-glyph-cache}

Um Laufzeitschriftarten leichter verwenden zu können, unterstützen sie das Vorabfüllen des Glyphen-Caches.
Das bedeutet, dass die unter *Characters* in der Schriftressource aufgeführten Glyphen erzeugt werden.

::: sidenote
Wenn `All Chars` ausgewählt ist, wird der Cache nicht vorab gefüllt, da dies dem Zweck widerspricht, nicht alle Glyphen gleichzeitig erzeugen zu müssen.
:::

Wenn das Feld `Characters` der `.fontc`-Datei ausgefüllt ist, wird sein Inhalt als Text verwendet, um zu ermitteln, welche Glyphen im Glyphen-Cache aktualisiert werden müssen.

Du kannst den Glyphen-Cache auch manuell aktualisieren, indem du `font.prewarm_text(font_collection, text, callback)` aufrufst. Ein Callback informiert dich darüber, wann alle fehlenden Glyphen zum Glyphen-Cache hinzugefügt wurden und der Text auf dem Bildschirm angezeigt werden kann.

### Schriftarten zu einer Schriftsammlung hinzufügen oder daraus entfernen {#addingremoving-fonts-to-a-font-collection}

Bei Laufzeitschriftarten kannst du Schriftarten (`.ttf`) zu einer Schriftsammlung hinzufügen oder daraus entfernen.
Das ist nützlich, wenn eine große Schriftart in mehrere Dateien für verschiedene Zeichensätze (z. B. CJK) aufgeteilt wurde.

::: important
Wenn du eine Schriftart zu einer Schriftsammlung hinzufügst, werden dadurch nicht automatisch alle Glyphen geladen oder gerendert.
:::

```lua
function init(self)
    -- Get the target font collection.
    self.font_collection = go.get("#label", "font")

    -- Get the first font assigned to the selected language collection.
    local language_collection = go.get("localization_japanese#label", "font")
    local font_info = font.get_info(language_collection)
    self.language_ttf_hash = font_info.fonts[1].path_hash

    -- Associate it with the target collection and increase its reference count.
    font.add_font(self.font_collection, self.language_ttf_hash)
end
```

```lua
function final(self)
    -- Remove the association and release the font reference.
    font.remove_font(self.font_collection, self.language_ttf_hash)
end
```

### Glyphen vorab erzeugen {#prewarming-glyphs}

Damit ein Text mit einer Laufzeitschriftart korrekt angezeigt werden kann, müssen die Glyphen aufgelöst werden. `font.prewarm_text()` übernimmt das für dich.
Dies ist ein asynchroner Vorgang. Sobald er abgeschlossen ist und der Callback aufgerufen wurde, kannst du mit der Anzeige jeder Meldung fortfahren, die diese Glyphen enthält.

::: important
Wenn der Glyphen-Cache voll wird, wird die älteste Glyphe aus dem Cache entfernt.
:::

```lua
font.prewarm_text(self.font_collection, info.text, function (self, request_id, result, err)
    if result then
      print("PREWARMING OK!")
      go.set(self.label, "text", info.text)
    else
      print("Error prewarming text:", err)
    end
  end)
```
