---
title: Handbuch zu Schriftarten in Defold
brief: Dieses Handbuch beschreibt, wie Defold mit Schriftarten umgeht und wie du Text in deinen Spielen auf dem Bildschirm darstellst.
---

# Schriftdateien {#font-files}

Schriftarten werden verwendet, um Text in Beschriftungskomponenten (label components) und GUI-Textknoten zu rendern. Defold unterstützt mehrere Schriftdateiformate:

- TrueType
- OpenType
- BMFont

Sowohl die bisherige als auch die vollständige Textlayout-Engine unterstützen TrueType-Konturen und OpenType-CFF1-/CFF2-Konturen, einschließlich der Erzeugung zur Laufzeit aus `.ttf`- und `.otf`-Ressourcen.

Informationen zum Gestalten einzelner Textabschnitte und zum Arbeiten mit Links und eingebetteten Sprites findest du im [Handbuch zur Rich-Text-Auszeichnung](/manuals/font-richtext).

Bei TrueType- und OpenType-Schriftarten wählt die Eigenschaft *Mode* aus, wie Glyphen gerendert werden:

- **Bitmap** verwendet gerasterte Glyphenbilder.
- **SDF** (signed distance field) speichert Abstände zu Glyphenkanten in einer Textur und ermöglicht dadurch eine flexiblere Skalierung als Bitmap.
- **Vector** rendert die Glyphenflächen aus Kurvendaten, sodass sie beim Skalieren scharf bleiben. Kontur- und Schatteneffekte verwenden weiterhin Bitmap-Daten.

Neu erstellte Schriftartenressourcen verwenden den Modus **Vector** und die Glyphenerzeugung **Dynamic**. Bestehende Schriftartenressourcen behalten ihren Bitmap- oder SDF-Modus. BMFont-Quellen verwenden immer ihre mitgelieferte Bitmap.

Der Vector-Modus benötigt Grafikunterstützung für Texturen vom Typ `RGBA16F` und `R32UI` und wird unter OpenGL ES 2 und WebGL 1 nicht unterstützt. Verwende für nicht unterstützte Grafikadapter Bitmap- oder SDF-Schriftarten mit passenden Materialien; es gibt keinen automatischen Rückfall von Vector auf SDF. Die Einrichtung beschreibt [Vektorschriftarten](#vector-fonts).

## Offline- oder Laufzeitschriftarten {#offline-or-runtime-fonts}

Die Eigenschaft *Glyph Generation* bestimmt, wann die Glyphendaten der jeweiligen Schriftart erzeugt werden:

- **Static** erzeugt die ausgewählten Glyphen beim Build (offline). *Characters* und *All Chars* bestimmen, welche Glyphen enthalten sind. Die Quelldatei `.ttf` oder `.otf` wird nicht für die Erzeugung zur Laufzeit in das Bundle aufgenommen.
- **Dynamic** nimmt die Quelldatei `.ttf` oder `.otf` in das Bundle auf und erzeugt Glyphen bei Bedarf zur Laufzeit. *Prewarm Text* bereitet Glyphen beim Laden der Schriftart vor. Weitere Glyphen können später bei Bedarf erzeugt werden.

SDF- und Vektorschriftarten unterstützen beide Möglichkeiten. Bitmap-Schriftarten und BMFont-Quellen verwenden Static. Jede Schriftartenressource wird unabhängig konfiguriert, sodass ein Projekt statische und dynamische Schriftarten kombinieren kann.

Die dynamische Erzeugung kann die Bundle-Größe und den Speicherbedarf zur Laufzeit reduzieren, besonders bei Schriftarten mit großen Zeichensätzen. Sie benötigt das vollständige Textlayoutsystem in der Engine; siehe [Laufzeitschriftarten aktivieren](#enabling-runtime-fonts).

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

Ziehe die Schriftart, die du verwenden möchtest, in den Browser *Assets* und lege sie an einer geeigneten Stelle ab.

Setze die Eigenschaft *Font* auf die Schriftartendatei. Wähle für eine `.ttf`- oder `.otf`-Quelle *Mode* und *Glyph Generation* und konfiguriere die übrigen Eigenschaften nach Bedarf. Führe bei dynamischer Erzeugung zusätzlich die [Einrichtung für Laufzeitschriftarten](#enabling-runtime-fonts) durch.

![Schriftarteneigenschaften mit Vector-Modus und dynamischer Glyphenerzeugung](images/font/font_properties.png)

Verwende bei Vektorschriftarten *Font Size* an einer Beschriftungskomponente oder einem GUI-Textknoten, um die angezeigte Textgröße zu ändern. *Outline/Shadow Bitmap Size* steuert die Auflösung der Effekt-Bitmaps unabhängig von der angezeigten Textgröße.

Setze bei Bitmap- und SDF-Schriftarten *Size* in der Schriftartenressource, um die erzeugte Glyphengröße zu wählen. BMFont-Größen stammen aus der Quelldatei `.fnt`. Skaliere die Beschriftungskomponente oder den GUI-Textknoten, um die angezeigte Größe dieser Schriftarten zu ändern.

## Eigenschaften {#properties}

*Font*
: Die TTF-, OTF- oder *`.fnt`*-Datei, aus der die Schriftdaten erzeugt werden.

*Material*
: Das Material zum Rendern dieser Schriftart. Es muss zum Schriftartenmodus passen; siehe [Schriftartenmaterialien](#font-materials).

*Mode*
: Die Rendertechnik für eine `.ttf`- oder `.otf`-Quelle: **Bitmap**, **SDF** oder **Vector**. Sie ersetzt die bisherige Eigenschaft *Output Format*. Bei BMFont-Quellen wird diese Eigenschaft nicht angezeigt.

*Glyph Generation*
: **Static** erzeugt Glyphendaten beim Build. **Dynamic** erzeugt sie zur Laufzeit und benötigt das [vollständige Textlayoutsystem](#enabling-runtime-fonts). Diese Eigenschaft ist für SDF- und Vektorschriftarten verfügbar. Im Bitmap-Modus ist sie auf Static festgelegt; bei BMFont-Quellen wird sie nicht angezeigt.

*Render Mode*
: Die Anordnung der Ebenen für erzeugte Bitmap-Schriftarten. Diese Eigenschaft wird nur im Bitmap-Modus für `.ttf`- und `.otf`-Quellen angezeigt. Für SDF-, Vector- und BMFont-Quellen wählt Defold die Ebenenanordnung automatisch.

  - **Single Layer** erzeugt ein einzelnes Quad für jedes Zeichen.
  - **Multi Layer** erzeugt separate Quads für Glyphenform, Kontur und Schatten. Die Ebenen werden von hinten nach vorn gerendert. Dadurch verdeckt ein Zeichen keine zuvor gerenderten Zeichen, wenn die Kontur breiter als der Abstand zwischen Glyphen ist. Außerdem ermöglicht dies Schattenversätze über die Eigenschaften *Shadow X/Y*.

*Size*
: Die Glyphengröße in Pixeln beim Erzeugen von Bitmap- oder SDF-Schriftartendaten. Bei BMFont-Quellen wird die Größe aus der `.fnt`-Datei gelesen und kann hier nicht bearbeitet werden.

*Outline/Shadow Bitmap Size*
: Ersetzt im Vector-Modus *Size*. Die Eigenschaft steuert die Bitmap-Auflösung aktivierter Kontur- und Schatteneffekte sowohl bei statischer als auch bei dynamischer Erzeugung. Sind beide Effekte deaktiviert, ist sie ebenfalls deaktiviert, da die Glyphenflächen Kurvendaten verwenden. Eine Änderung von *Font Size* an einer Beschriftung oder einem GUI-Textknoten verändert diese gemeinsam genutzte Bitmap-Auflösung nicht.

*Antialias*
: Legt fest, ob beim Erzeugen von Bitmap-Schriftartendaten Kantenglättung angewendet wird. Deaktiviere dies für pixelgenaues Rendering. Diese Eigenschaft wird nur im Bitmap-Modus für `.ttf`- und `.otf`-Quellen angezeigt.

*Alpha*
: Die Transparenz der Glyphe. 0.0--1.0, wobei 0.0 transparent und 1.0 undurchsichtig bedeutet.

*Outline Alpha*
: Die Transparenz des erzeugten Umrisses. 0.0--1.0.

*Outline Width*
: Die Breite des erzeugten Umrisses in Pixeln. Setze den Wert auf 0, um keinen Umriss zu erzeugen.

*Shadow Alpha*
: Die Transparenz des erzeugten Schattens. 0.0--1.0.

::: sidenote
Der integrierte Shader für Bitmap-Schriftarten unterstützt Schatten sowohl im Rendermodus *Single Layer* als auch in *Multi Layer*. Für erzeugte Bitmap-Schriftarten mit *Single Layer*, die keine Schatten benötigen, kann ein benutzerdefiniertes Material `/builtins/fonts/font-singlelayer.fp` verwenden. SDF- und Vektorschriftarten benötigen Shader, die zu ihrem Modus passen; siehe [Schriftartenmaterialien](#font-materials).
:::

*Shadow Blur*
: Die Stärke der Unschärfe des erzeugten Schattens. Setze den Wert für einen scharfen Schatten auf 0.

*Shadow X/Y*
: Der horizontale und vertikale Versatz des erzeugten Schattens in Pixeln. Verwende bei erzeugten Bitmap-Schriftarten den Rendermodus *Multi Layer*, um diese Versätze anzuwenden. Für SDF- und Vektorschriftarten wählt Defold die passenden Ebenen automatisch.

*Characters*
: Bei statischer Erzeugung die Zeichen, die in der erstellten Schriftart enthalten sein sollen. Standardmäßig enthält dieses Feld die druckbaren ASCII-Zeichen (Zeichencodes 32–126). Füge Zeichen hinzu oder entferne sie, um festzulegen, welche Glyphen zur Laufzeit verfügbar sind.

*Prewarm Text*
: Ersetzt bei dynamischer Erzeugung *Characters*. Der Text dient beim Laden der Schriftart zum Erzeugen von Glyphen und Vorbereiten des Caches. Er beschränkt nicht, welche Zeichen später erzeugt werden können. Du kannst Text auch aus einem Skript mit [`font.prewarm_text()`](/ref/font/#font.prewarm_text) vorbereiten.

::: sidenote
Die druckbaren ASCII-Zeichen sind:
Leerzeichen ! " # $ % & ' ( ) * + , - . / 0 1 2 3 4 5 6 7 8 9 : ; < = > ? @ A B C D E F G H I J K L M N O P Q R S T U V W X Y Z [ \ ] ^ _ \` a b c d e f g h i j k l m n o p q r s t u v w x y z { | } ~
:::

*All Chars*
: Nimmt bei statischer Erzeugung jede in der Quelle verfügbare Glyphe auf, statt die Schriftart auf *Characters* zu beschränken. Bei dynamischen Schriftarten ist diese Eigenschaft ausgeblendet.

*Cache Width/Height*
: Begrenzt die Größe der Glyphen-Cache-Bitmap, die Bitmap- und SDF-Schriftarten sowie Kontur- und Schatteneffekte im Vector-Modus verwenden. Beim Rendern von Text sucht die Engine die Glyphe in der Cache-Bitmap. Fehlt sie dort, wird sie vor dem Rendern zum Cache hinzugefügt. Ist die Cache-Bitmap zu klein für alle Glyphen, die die Engine rendern soll, wird ein Fehler gemeldet (`ERROR:RENDER: Out of available cache cells! Consider increasing cache_width or cache_height for the font.`).

  Bei einem Wert von 0 wird die Cache-Größe automatisch festgelegt und kann auf höchstens 2048x4096 anwachsen.

## Schriftartenmaterialien {#font-materials}

Verwende ein Material, das zum Schriftartenmodus passt. GUI-Textknoten verwenden *Material* der Schriftartenressource. Beschriftungskomponenten haben eine separate Eigenschaft *Material*, die ebenfalls zur Schriftart passen muss:

| Schriftartenmodus oder Quelle | Schriftartenmaterial für GUI-Text | Material der Beschriftungskomponente |
| --- | --- | --- |
| Bitmap | `/builtins/fonts/font.material` | `/builtins/fonts/label.material` |
| SDF | `/builtins/fonts/font-df.material` | `/builtins/fonts/label-df.material` |
| Vector | `/builtins/fonts/font-vector.material` | `/builtins/fonts/label-vector.material` |
| BMFont (`.fnt`) | `/builtins/fonts/font-fnt.material` | `/builtins/fonts/label-fnt.material` |

Wenn du *Mode* im Schriftarteneditor änderst, wird zwischen den entsprechenden integrierten Bitmap-, SDF- und Vector-Materialien gewechselt, sofern bereits eines dieser Materialien zugewiesen ist. Benutzerdefinierte Materialien werden nicht automatisch ersetzt. Prüfe auch *Material* aller Beschriftungskomponenten, die diese Schriftart verwenden.

## Vektorschriftarten {#vector-fonts}

Vektorschriftarten rendern Glyphenflächen aus Kurven, sodass sie bei Änderungen der angezeigten Textgröße scharf bleiben. So richtest du eine Schriftart ein, die ihre Glyphen zur Laufzeit erzeugt:

1. Erstelle eine `.font`-Ressource, beispielsweise `/fonts/ui.font`, und wähle in ihrer Eigenschaft *Font* eine TrueType- oder OpenType-Quelle aus. Für gewöhnlichen Text kannst du die integrierte `/builtins/fonts/vera_mo_bd.ttf` verwenden.
2. Setze *Mode* auf **Vector**, *Glyph Generation* auf **Dynamic** und *Material* auf `/builtins/fonts/font-vector.material`. Dies sind die Standardwerte neu erstellter Schriftartenressourcen.
3. Aktiviere **Use full text layout system** in einem dem Projekt zugewiesenen Anwendungsmanifest. Folge [Laufzeitschriftarten aktivieren](#enabling-runtime-fonts), um die benutzerdefinierte Engine zu konfigurieren.
4. Aktiviere [Shader ▸ Exclude GLES 2.0](/manuals/project-settings/#exclude-gles-20) in *game.project*.
5. Weise die Schriftart einer [Beschriftung](/manuals/label/) zu oder füge sie zu *Fonts* einer GUI-Szene hinzu und wähle sie an einem [Textknoten](/manuals/gui-text/) aus. Setze bei einer Beschriftung außerdem *Material* der Komponente auf `/builtins/fonts/label-vector.material`. Setze *Font Size* der Komponente oder des Knotens auf die gewünschte Anzeigegröße.

Vektorglyphenflächen verwenden Kurventexturen; aktivierte Konturen und Schatten erzeugen jedoch weiterhin SDF-Bitmap-Daten und belegen Texturspeicher im Glyphen-Cache. *Outline/Shadow Bitmap Size* legt diese Bitmap-Auflösung unabhängig von *Font Size* der Beschriftung oder des GUI-Textknotens fest. Setze *Outline Alpha* und *Shadow Alpha* auf `0`, wenn du diese Effekte nicht benötigst, um die Erzeugung ihrer Bitmap-Daten zu vermeiden.

### Farbige Emojis {#color-emoji}

Vektorschriftarten können farbige COLRv1-Emojis rendern, einschließlich Palettenfarben sowie linearer und radialer Farbverläufe. Die Modi Bitmap und SDF rendern keine COLRv1-Farben. Verwende die obige Einrichtung mit Dynamic und Vector und ergänze die Schriftartensammlung um eine COLRv1-Emoji-Schriftart als Ausweichschrift. Gewöhnlicher Text verwendet weiterhin die ursprüngliche Schriftart.

Kopiere beispielsweise die COLRv1-[Schriftart Noto Color Emoji](https://github.com/google/fonts/blob/main/ofl/notocoloremoji/NotoColorEmoji-Regular.ttf) als `/fonts/NotoColorEmoji-Regular.ttf` in dein Projekt. Wähle die COLRv1-Version: Andere Emoji-Schriftarten können ein anderes Farbformat verwenden, auch wenn ihr Dateiname auf `.ttf` endet.

Ergänze `/fonts/NotoColorEmoji-Regular.ttf` unter **Project ▸ Custom Resources** in *game.project*. Ohne weitere benutzerdefinierte Ressourcen lautet die Einstellung:

```ini
[project]
custom_resources = /fonts/NotoColorEmoji-Regular.ttf
```

Ein in Lua angegebener Schriftartenpfad bewirkt nicht, dass die Schriftartendatei in das Bundle aufgenommen wird. [Custom Resources](/manuals/project-settings/#custom-resources) macht diese Quellschriftart für [`font.add_font()`](/ref/font/#font.add_font) verfügbar, das sie über das Ressourcensystem lädt. Übergib beim Laden aus dem Bundle den Pfad der Quellschriftart als Zeichenfolge.

Füge die Ausweichschrift pro gemeinsam genutzter Schriftartenressource nur einmal hinzu. Die Änderung betrifft alle Beschriftungen und GUI-Textknoten, die diese Schriftart verwenden; zweimaliges Hinzufügen derselben Ausweichschrift löst einen Fehler aus. Wenn du das [Beschriftungsbeispiel](/manuals/label/#vector-fonts-and-color-emoji) und das [GUI-Beispiel](/manuals/gui-text/#vector-fonts-and-color-emoji) mit derselben `.font` verwendest, stimme die Initialisierung so ab, dass die Ausweichschrift einmal hinzugefügt wird, bevor eines der Beispiele Text vorbereitet oder anzeigt. Die Beispiele bereiten nach dem Hinzufügen der Ausweichschrift den vollständigen Text vor und zeigen ihn an, wenn der Callback Erfolg meldet.

## Distanzfeldschriften {#distance-field-fonts}

Distanzfeldschriften (distance field fonts) speichern statt Bitmap-Daten den Abstand zum Rand der Glyphe in der Textur. Wenn die Engine die Schriftart rendert, ist ein spezieller Shader erforderlich, der die Abstandsdaten interpretiert und damit die Glyphe zeichnet. Distanzfeldschriften benötigen mehr Ressourcen als Bitmap-Schriften, bieten aber mehr Flexibilität bei der Größenänderung.

![Distanzfeldschrift](images/font/df_font.png)

Wähle **SDF** unter *Mode* und **Static** oder **Dynamic** unter *Glyph Generation*. Verwende *`/builtins/fonts/font-df.material`* für die Schriftart und *`/builtins/fonts/label-df.material`* für Beschriftungskomponenten oder benutzerdefinierte Materialien, die Distanzfelddaten verarbeiten.

## Bitmap-Schriften im BMFont-Format {#bitmap-bmfonts}

Neben erzeugten Bitmaps unterstützt Defold vorab gerasterte Bitmap-Schriften im Format „BMFont“. Diese Schriftarten bestehen aus einem PNG-Schriftbogen mit allen Glyphen. Zusätzlich enthält eine *`.fnt`*-Datei Angaben dazu, wo sich jede Glyphe auf dem Bogen befindet, sowie Informationen zu Größe und Unterschneidung. (Beachte, dass Defold die XML-Version des *`.fnt`*-Formats, die Phaser und einige andere Werkzeuge verwenden, nicht unterstützt.)

Diese Schriftarten bieten keinen Leistungsvorteil gegenüber Bitmap-Schriften, die aus TrueType- oder OpenType-Schriftdateien erzeugt werden. Sie können jedoch beliebige Grafiken, Farben und Schatten direkt im Bild enthalten.

Füge die erzeugten Dateien *`.fnt`* und *`.png`* deinem Defold-Projekt hinzu. Sie sollten im selben Ordner liegen. Erstelle eine neue Schriftartendatei und setze *Font* auf die *`.fnt`*-Datei. Defold verwendet die mitgelieferte Bitmap und liest ihre Größe aus der `.fnt`-Datei. *Mode* und *Glyph Generation* werden bei BMFont-Quellen nicht angezeigt.

::: sidenote
Um eine BMFont zu erstellen, benötigst du ein Werkzeug, das die entsprechenden Dateien erzeugen kann. Dafür gibt es mehrere Möglichkeiten:

* [Bitmap Font Generator](http://www.angelcode.com/products/bmfont/), ein nur für Windows verfügbares Werkzeug von AngelCode.
* [Shoebox](http://renderhjs.net/shoebox/), eine kostenlose Anwendung für Windows und macOS auf Basis von Adobe Air.
* [Hiero](https://libgdx.com/wiki/tools/hiero), ein Open-Source-Werkzeug auf Basis von Java.
* [Glyph Designer](https://71squared.com/glyphdesigner), ein kommerzielles macOS-Werkzeug von 71 Squared.
* [bmGlyph](https://www.bmglyph.com), ein kommerzielles macOS-Werkzeug von Sovapps.
:::

![BMFont](images/font/bm_font.png)

Setze *Material* der Schriftart auf *`/builtins/fonts/font-fnt.material`*. Verwende für Beschriftungskomponenten *`/builtins/fonts/label-fnt.material`*.

## Artefakte und bewährte Vorgehensweisen {#artifacts-and-best-practices}

Bitmap-Schriften eignen sich im Allgemeinen am besten, wenn die Schriftart ohne Skalierung gerendert wird. Sie lassen sich schneller auf den Bildschirm rendern als Distanzfeldschriften.

Distanzfeldschriften lassen sich sehr gut vergrößern. Bitmap-Schriften bestehen dagegen nur aus Pixelbildern: Beim Vergrößern der Schriftart wachsen auch die Pixel, wodurch blockartige Artefakte entstehen. Das folgende Beispiel zeigt eine Schriftgröße von 48 Pixeln, die auf das 4-Fache vergrößert wurde.

![Vergrößerte Schriftarten](images/font/scale_up.png)

Beim Verkleinern kann die GPU Bitmap-Texturen ansprechend und effizient skalieren und mit Kantenglättung versehen. Eine Bitmap-Schrift behält ihre Farbe besser bei als eine Distanzfeldschrift. Hier siehst du eine vergrößerte Ansicht derselben Beispielschrift mit einer Größe von 48 Pixeln, verkleinert auf 1/5 ihrer Größe:

![Verkleinerte Schriftarten](images/font/scale_down.png)

Distanzfeldschriften müssen in einer Zielgröße gerendert werden, die groß genug ist, um Abstandsinformationen zur Darstellung der Kurven ihrer Glyphen aufzunehmen. Dies ist dieselbe Schriftart wie oben, jedoch mit einer Größe von 18 Pixeln und auf das 10-Fache vergrößert. Es ist deutlich erkennbar, dass diese Größe zu klein ist, um die Formen dieser Schrift zu codieren:

![Artefakte bei Distanzfeldschriften](images/font/df_artifacts.png)

Wenn du keine Schatten oder Konturen benötigst, setze ihre jeweiligen Alpha-Werte auf null. Andernfalls werden weiterhin Schatten- und Konturdaten erzeugt, die unnötig Speicher belegen. Im Vector-Modus verhindert das Deaktivieren beider Effekte die Erzeugung ihrer Bitmap-Daten; die Glyphenflächen verwenden weiterhin Kurvendaten.

## Schrift-Cache {#font-cache}
Bitmap- und SDF-Schriftartenressourcen verwenden zur Laufzeit eine Glyphen-Cache-Textur und Schriftartendaten. Vektorschriftarten speichern ihre Glyphenflächen als Kurvendaten und verwenden für aktivierte Kontur- und Schatteneffekte einen Bitmap-Cache. Das nachfolgend beschriebene Texturlayout gilt für Bitmap- und SDF-Schriftarten.

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

Die Erzeugung zur Laufzeit wird pro Schriftartenressource konfiguriert:

1. Öffne die `.font`-Ressource und wähle eine TrueType- (`.ttf`) oder OpenType-Quelle (`.otf`).
2. Setze *Mode* auf **SDF** oder **Vector** und *Glyph Generation* auf **Dynamic**.
3. Wähle die passenden [Schriftarten- und Beschriftungsmaterialien](#font-materials).
4. Füge ein [Anwendungsmanifest](/manuals/app-manifest) hinzu, weise es unter *Native Extensions ▸ App Manifest* in *game.project* zu und aktiviere **Use full text layout system**. Dadurch wird eine benutzerdefinierte Engine mit Glyphenerzeugung zur Laufzeit und vollständigem Textlayout erstellt.
5. Setze *Prewarm Text* auf Text, der kurz nach dem Laden der Schriftart angezeigt wird. Verwende für später benötigten Text [`font.prewarm_text()`](/ref/font/#font.prewarm_text) und warte vor der Anzeige auf den Callback.

Neue Schriftartenressourcen verwenden bereits den Vector-Modus und dynamische Erzeugung, benötigen aber trotzdem die obige Konfiguration des Anwendungsmanifests.

### Schriftarten per Skript steuern {#font-scripting}

#### Den Glyphen-Cache vorab füllen {#prewarming-glyph-cache}

Dynamische Schriftarten erzeugen beim Laden die von *Prewarm Text* benötigten Glyphen. Das Feld wird als zu layoutender Text interpretiert, sodass der Cache für die dafür erforderlichen Glyphen vorbereitet wird. *All Chars* ist für dynamische Schriftarten nicht verfügbar.

Du kannst für eine dynamische Schriftart auch `font.prewarm_text(font_collection, text, callback)` aufrufen. Der Callback teilt dir mit, wann alle fehlenden Glyphen zum Cache hinzugefügt wurden und der Text angezeigt werden kann. Diese Funktion kann nicht mit statischen Schriftarten verwendet werden.

### Schriftarten zu einer Schriftsammlung hinzufügen oder daraus entfernen {#addingremoving-fonts-to-a-font-collection}

Bei dynamischen Schriftarten können Quellschriftarten (`.ttf` oder `.otf`) einer Schriftartensammlung hinzugefügt oder daraus entfernt werden.
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
