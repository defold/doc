---
title: Texturprofile in Defold
brief:  Defold unterstützt die automatische Verarbeitung von Texturen und die Komprimierung von Bilddaten. Dieses Handbuch beschreibt die verfügbaren Funktionen.
---

# Texturprofile {#texture-profiles}

Defold unterstützt die automatische Verarbeitung von Texturen und die Komprimierung von Bilddaten (in *Atlanten (Atlas)*, *Kachelquellen (tile sources)*, *Cubemaps* und eigenständigen Texturen für Modelle, GUI usw.).

Es gibt zwei Arten der Komprimierung: Software-Bildkomprimierung und Hardware-Texturkomprimierung.

1. Software-Komprimierung (wie PNG und JPEG) verringert den Speicherplatzbedarf von Bildressourcen. Dadurch wird das fertige Bundle kleiner. Die Bilddateien müssen jedoch beim Einlesen in den Arbeitsspeicher dekomprimiert werden. Auch wenn ein Bild auf dem Datenträger klein ist, kann es daher viel Arbeitsspeicher belegen.

2. Hardware-Texturkomprimierung verringert ebenfalls den Speicherplatzbedarf von Bildressourcen. Anders als Software-Komprimierung verringert sie jedoch auch den Arbeitsspeicherbedarf von Texturen. Das liegt daran, dass die Grafikhardware komprimierte Texturen direkt verarbeiten kann, ohne sie zuvor dekomprimieren zu müssen.

Die Verarbeitung von Texturen wird über ein bestimmtes Texturprofil (texture profile) konfiguriert. In dieser Datei erstellst du _Profile_, die festlegen, welche Komprimierungsformate und welche Komprimierungsart beim Erstellen von Bundles für eine bestimmte Plattform verwendet werden sollen. _Profile_ werden anschließend mit passenden _Dateipfadmustern_ verknüpft. So kannst du genau steuern, welche Dateien in deinem Projekt komprimiert werden und wie dies geschieht.

Da alle verfügbaren Verfahren zur Hardware-Texturkomprimierung verlustbehaftet sind, entstehen Artefakte in deinen Texturdaten. Diese Artefakte hängen stark davon ab, wie dein Ausgangsmaterial aussieht und welche Komprimierungsmethode verwendet wird. Du solltest dein Ausgangsmaterial testen und experimentieren, um die besten Ergebnisse zu erzielen. Google kann dir dabei helfen.

Du kannst auswählen, welche Software-Bildkomprimierung auf die endgültigen Texturdaten (komprimiert oder unkomprimiert) in den Bundle-Archiven angewendet wird. Defold unterstützt die Komprimierungsformate [Basis Universal](https://github.com/BinomialLLC/basis_universal) und [ASTC](https://www.khronos.org/opengl/wiki/ASTC_Texture_Compression).

::: sidenote
Komprimierung ist ein ressourcenintensiver und zeitaufwendiger Vorgang, der zu _sehr_ langen Build-Zeiten führen kann. Diese hängen von der Anzahl der zu komprimierenden Texturbilder sowie von den gewählten Texturformaten und der Art der Software-Komprimierung ab.
:::

### Basis Universal

Basis Universal (kurz BasisU) komprimiert das Bild in ein Zwischenformat, das zur Laufzeit in ein Hardwareformat transkodiert wird, das für die GPU des aktuellen Geräts geeignet ist. Das Basis-Universal-Format bietet eine hohe Qualität, ist aber verlustbehaftet.
Alle Bilder werden außerdem mit LZ4 komprimiert, um die Dateigröße beim Speichern im Spielarchiv weiter zu verringern.

### ASTC

ASTC ist ein flexibles und effizientes Format zur Texturkomprimierung, das von ARM entwickelt und von der Khronos Group standardisiert wurde. Es bietet eine große Auswahl an Blockgrößen und Bitraten, mit denen du Bildqualität und Speicherbedarf wirksam aufeinander abstimmen kannst. ASTC unterstützt verschiedene Blockgrößen von 4×4 bis 12×12 Texeln. Diese entsprechen Bitraten von 8 Bit pro Texel bis hinunter zu 0,89 Bit pro Texel. Diese Flexibilität ermöglicht eine feine Abstimmung zwischen Texturqualität und Speicherplatzbedarf.

ASTC unterstützt verschiedene Blockgrößen von 4×4 bis 12×12 Texeln. Diese entsprechen Bitraten von 8 Bit pro Texel bis hinunter zu 0,89 Bit pro Texel. Diese Flexibilität ermöglicht eine feine Abstimmung zwischen Texturqualität und Speicherplatzbedarf. Die folgende Tabelle zeigt die unterstützten Blockgrößen und ihre jeweiligen Bitraten:

| Blockgröße (Breite x Höhe) | Bit pro Pixel |
| --------------------------- | -------------- |
| 4x4                         | 8.00           |
| 5x4                         | 6.40           |
| 5x5                         | 5.12           |
| 6x5                         | 4.27           |
| 6x6                         | 3.56           |
| 8x5                         | 3.20           |
| 8x6                         | 2.67           |
| 10x5                        | 2.56           |
| 10x6                        | 2.13           |
| 8x8                         | 2.00           |
| 10x8                        | 1.60           |
| 10x10                       | 1.28           |
| 12x10                       | 1.07           |
| 12x12                       | 0.89           |


#### Unterstützte Geräte {#supported-devices}

ASTC liefert zwar sehr gute Ergebnisse, wird aber nicht von allen Grafikkarten unterstützt. Hier findest du eine kurze Liste unterstützter Geräte nach Hersteller:

| GPU-Hersteller     | Unterstützung                                                          |
| ------------------ | --------------------------------------------------------------------- |
| ARM (Mali)         | Alle ARM-Mali-GPUs, die OpenGL ES 3.2 oder Vulkan unterstützen, unterstützen ASTC. |
| Qualcomm (Adreno)  | Adreno-GPUs, die OpenGL ES 3.2 oder Vulkan unterstützen, unterstützen ASTC. |
| Apple              | Apple-GPUs unterstützen ASTC seit dem A8-Chip.                          |
| NVIDIA             | ASTC wird hauptsächlich von mobilen GPUs unterstützt (z. B. Tegra-basierten Chips). |
| AMD (Radeon)       | AMD-GPUs, die Vulkan unterstützen, unterstützen ASTC in der Regel über Software. |
| Intel (integriert) | Moderne Intel-GPUs unterstützen ASTC über Software.                    |

## Texturprofile {#texture-profiles-1}

Jedes Projekt enthält eine bestimmte Datei mit der Endung *.texture_profiles*, die die Konfiguration für die Texturkomprimierung enthält. Standardmäßig ist dies die Datei *builtins/graphics/default.texture_profiles*. Ihre Konfiguration ordnet jede Texturressource einem Profil zu, das RGBA ohne Hardware-Texturkomprimierung und die standardmäßige ZLib-Dateikomprimierung verwendet.

So fügst du Texturkomprimierung hinzu:

- Wähle <kbd>File ▸ New...</kbd> und anschließend *Texture Profiles*, um eine neue Texturprofildatei zu erstellen. (Alternativ kannst du *default.texture_profiles* an einen Speicherort außerhalb von *builtins* kopieren.)
- Wähle einen Namen und einen Speicherort für die neue Datei.
- Ändere den Eintrag *texture_profiles* in *game.project* so, dass er auf die neue Datei verweist.
- Öffne die Datei mit der Endung *.texture_profiles* und konfiguriere sie nach deinen Anforderungen.

![Neue Profildatei](images/texture_profiles/texture_profiles_new_file.png)

![Texturprofil festlegen](images/texture_profiles/texture_profiles_game_project.png)

Du kannst die Verwendung von Texturprofilen in den Editoreinstellungen ein- und ausschalten. Wähle <kbd>File ▸ Preferences...</kbd>. Die Registerkarte *General* enthält das Kontrollkästchen *Enable texture profiles*.

![Einstellungen für Texturprofile](images/texture_profiles/texture_profiles_preferences.png)

## Pfadeinstellungen {#path-settings}

Der Abschnitt *Path Settings* der Texturprofildatei enthält eine Liste von Pfadmustern und legt fest, welches *Profil* bei der Verarbeitung von Ressourcen verwendet werden soll, die zum Pfad passen. Die Pfade werden als „Ant Glob“-Muster angegeben (Einzelheiten findest du in der [Dokumentation](http://ant.apache.org/manual/dirtasks.html#patterns)). Muster können mit den folgenden Platzhaltern angegeben werden:

`*`
: Entspricht null oder mehr Zeichen. Beispielsweise passt `sprite*.png` auf die Dateien *`sprite.png`*, *`sprite1.png`* und *`sprite_with_a_long_name.png`*.

`?`
: Entspricht genau einem Zeichen. Beispielsweise passt `sprite?.png` auf die Dateien *sprite1.png*, *`spriteA.png`*, aber nicht auf *`sprite.png`* oder *`sprite_with_a_long_name.png`*.

`**`
: Entspricht einem vollständigen Verzeichnisbaum oder---wenn als Name eines Verzeichnisses verwendet---null oder mehr Verzeichnissen. Beispielsweise passt `/gui/**` auf alle Dateien im Verzeichnis */gui* und in allen seinen Unterverzeichnissen.

![Pfade](images/texture_profiles/texture_profiles_paths.png)

Dieses Beispiel enthält zwei Pfadmuster und die zugehörigen Profile.

`/gui/**/*.atlas`
: Alle Dateien mit der Endung *.atlas* im Verzeichnis *`/gui`* oder in einem seiner Unterverzeichnisse werden gemäß dem Profil „gui_atlas“ verarbeitet.

`/**/*.atlas`
: Alle Dateien mit der Endung *.atlas* an beliebiger Stelle im Projekt werden gemäß dem Profil „atlas“ verarbeitet.

Beachte, dass der allgemeinere Pfad am Ende steht. Der Abgleichalgorithmus arbeitet von oben nach unten. Der erste Eintrag, der zum Ressourcenpfad passt, wird verwendet. Ein passender Pfadausdruck weiter unten in der Liste überschreibt niemals den ersten Treffer. Wären die Pfade in umgekehrter Reihenfolge angegeben, würde jeder Atlas mit dem Profil „atlas“ verarbeitet, auch die Atlanten im Verzeichnis *`/gui`*.

Texturressourcen, die auf _keinen_ Pfad in der Profildatei passen, werden kompiliert und auf die nächstgelegene Zweierpotenz skaliert, bleiben ansonsten aber unverändert.

## Profile {#profiles}

Der Abschnitt *profiles* der Texturprofildatei enthält eine Liste benannter Profile. Jedes Profil enthält eine oder mehrere *platforms*, wobei jede Plattform durch eine Liste von Eigenschaften beschrieben wird.

![Profile](images/texture_profiles/texture_profiles_profiles.png)

*Platforms*
: Gibt eine passende Plattform an. `OS_ID_GENERIC` passt auf alle Plattformen, `OS_ID_WINDOWS` auf Bundles für Windows, `OS_ID_IOS` auf iOS-Bundles und so weiter. Beachte, dass `OS_ID_GENERIC`, wenn es angegeben ist, für alle Plattformen einbezogen wird.

::: important
Wenn zwei [Pfadeinstellungen](#path-settings) auf dieselbe Datei passen und die Pfade unterschiedliche Profile mit unterschiedlichen Plattformen verwenden, werden **beide** Profile verwendet und **zwei** Texturen erzeugt.
:::

*Formats*
: Ein oder mehrere zu erzeugende Texturformate. Wenn mehrere Formate angegeben sind, werden für jedes Format Texturen erzeugt und in das Bundle aufgenommen. Die Engine wählt Texturen in einem Format aus, das von der Plattform unterstützt wird, auf der sie ausgeführt wird.

*Mipmaps*
: Wenn aktiviert, werden Mipmaps für die Plattform erzeugt. Standardmäßig deaktiviert.

*Premultiply alpha*
: Wenn aktiviert, wird Alpha in die Texturdaten vormultipliziert. Standardmäßig aktiviert.

*Max Texture Size*
: Wenn ein Wert ungleich null angegeben ist, werden die Pixelabmessungen der Texturen auf die angegebene Zahl begrenzt. Jede Textur, deren Breite oder Höhe den angegebenen Wert überschreitet, wird herunterskaliert.

Jeder einem Profil hinzugefügte Eintrag unter *Formats* hat die folgenden Eigenschaften:

*Format*
: Das Format, das beim Kodieren der Textur verwendet wird. Alle verfügbaren Texturformate findest du weiter unten.

*Compressor*
: Der Kompressor, der beim Kodieren der Textur verwendet wird.

*Compressor Preset*
: Wählt eine Komprimierungsvoreinstellung aus, die beim Kodieren des resultierenden komprimierten Bildes verwendet wird. Jede Komprimierungsvoreinstellung gehört zu einem bestimmten Kompressor, und ihre Einstellungen hängen vom Kompressor selbst ab. Um diese Einstellungen zu vereinfachen, gibt es die aktuellen Komprimierungsvoreinstellungen in vier Stufen:

| Voreinstellung | Hinweis                                      |
| --------- | --------------------------------------------- |
| `LOW`     | Schnellste Komprimierung. Niedrige Bildqualität |
| `MEDIUM`  | Standardkomprimierung. Beste Bildqualität      |
| `HIGH`    | Langsamste Komprimierung. Kleinere Dateigröße   |
| `HIGHEST` | Langsame Komprimierung. Kleinste Dateigröße     |

Beachte, dass der Kompressor `uncompressed` nur eine Voreinstellung namens `uncompressed` hat. Sie bedeutet, dass keine Komprimierung auf die Texturen angewendet wird.
Eine Liste der verfügbaren Kompressoren findest du unter [Kompressoren](#compressors).

## Texturformate {#texture-formats}

Texturen für die Grafikhardware können in unkomprimierte oder *verlustbehaftet* komprimierte Daten mit unterschiedlicher Kanalanzahl und Bittiefe umgewandelt werden. Bei einer festen Hardware-Komprimierung hat das resultierende Bild unabhängig vom Bildinhalt eine feste Größe. Das bedeutet, dass der Qualitätsverlust bei der Komprimierung vom Inhalt der ursprünglichen Textur abhängt.

Da die Transkodierung bei der Basis-Universal-Komprimierung von den Fähigkeiten der GPU des Geräts abhängt, werden für die Verwendung mit Basis Universal generische Formate empfohlen, etwa:
`TEXTURE_FORMAT_RGB`, `TEXTURE_FORMAT_RGBA`, `TEXTURE_FORMAT_RGB_16BPP`, `TEXTURE_FORMAT_RGBA_16BPP`, `TEXTURE_FORMAT_LUMINANCE` und `TEXTURE_FORMAT_LUMINANCE_ALPHA`.

Der Basis-Universal-Transkoder unterstützt viele Ausgabeformate, etwa `ASTC4x4`, `BCx`, `ETC2`, `ETC1` und `PVRTC1`.

Die folgenden verlustbehafteten Komprimierungsformate werden derzeit unterstützt:

| Format                            | Komprimierung | Einzelheiten |
| --------------------------------- | ----------- | -------------------------------- |
| `TEXTURE_FORMAT_RGB`              | keine       | 3 Farbkanäle. Alpha wird verworfen. |
| `TEXTURE_FORMAT_RGBA`             | keine       | 3 Farbkanäle und vollständiger Alphakanal. |
| `TEXTURE_FORMAT_RGB_16BPP`        | keine       | 3 Farbkanäle. 5+6+5 Bit. |
| `TEXTURE_FORMAT_RGBA_16BPP`       | keine       | 3 Farbkanäle und vollständiger Alphakanal. 4+4+4+4 Bit. |
| `TEXTURE_FORMAT_LUMINANCE`        | keine       | 1 Graustufenkanal, kein Alpha. RGB-Kanäle werden zu einem Kanal multipliziert. Alpha wird verworfen. |
| `TEXTURE_FORMAT_LUMINANCE_ALPHA`  | keine       | 1 Graustufenkanal und vollständiger Alphakanal. RGB-Kanäle werden zu einem Kanal multipliziert. |

Bei ASTC beträgt die Anzahl der Kanäle immer 4 (RGB + Alpha), und das Format selbst legt die Blockgröße der Komprimierung fest.
Beachte, dass diese Formate nur mit einem ASTC-Kompressor kompatibel sind - jede andere Kombination führt zu einem Build-Fehler.

`TEXTURE_FORMAT_RGBA_ASTC_4X4`
`TEXTURE_FORMAT_RGBA_ASTC_5X4`
`TEXTURE_FORMAT_RGBA_ASTC_5X5`
`TEXTURE_FORMAT_RGBA_ASTC_6X5`
`TEXTURE_FORMAT_RGBA_ASTC_6X6`
`TEXTURE_FORMAT_RGBA_ASTC_8X5`
`TEXTURE_FORMAT_RGBA_ASTC_8X6`
`TEXTURE_FORMAT_RGBA_ASTC_8X8`
`TEXTURE_FORMAT_RGBA_ASTC_10X5`
`TEXTURE_FORMAT_RGBA_ASTC_10X6`
`TEXTURE_FORMAT_RGBA_ASTC_10X8`
`TEXTURE_FORMAT_RGBA_ASTC_10X10`
`TEXTURE_FORMAT_RGBA_ASTC_12X10`
`TEXTURE_FORMAT_RGBA_ASTC_12X12`


## Kompressoren {#compressors}

Die folgenden Texturkompressoren werden standardmäßig unterstützt. Die Daten werden dekomprimiert, wenn die Texturdatei in den Arbeitsspeicher geladen wird.

| Name                              | Formate                   | Hinweis                                                                                       |
| --------------------------------- | ------------------------- | --------------------------------------------------------------------------------------------- |
| `Uncompressed`                    | Alle Formate              | Es wird keine Komprimierung angewendet. Standard.                                              |
| `BasisU`                          | Alle RGB/RGBA-Formate      | Hochwertige, verlustbehaftete Komprimierung mit Basis Universal. Eine niedrigere Qualitätsstufe ergibt eine geringere Größe. |
| `ASTC`                            | Alle ASTC-Formate          | Verlustbehaftete ASTC-Komprimierung. Eine niedrigere Qualitätsstufe ergibt eine geringere Größe. |

::: sidenote
Defold unterstützt installierbare Kompressoren in der Pipeline zur Texturkomprimierung. Dadurch kannst du einen Algorithmus zur Texturkomprimierung in einer Erweiterung implementieren, etwa WEBP oder einen vollständig eigenen Algorithmus.
:::

## Beispielbild {#example-image}

Das folgende Beispiel soll das Ergebnis veranschaulichen.
Beachte, dass Bildqualität, Komprimierungsdauer und komprimierte Größe immer vom Eingabebild abhängen und variieren können.

Ausgangsbild (1024x512):
![Neue Profildatei](images/texture_profiles/kodim03_pow2.png)

### Komprimierungsdauer {#compression-times}

| Voreinstellung | Komprimierungsdauer | Relative Dauer |
| --------- | ---------------- | ------------- |
| `LOW`     | 0m0.143s         | 0.5x            |
| `MEDIUM`  | 0m0.294s         | 1.0x            |
| `HIGH`    | 0m1.764s         | 6.0x            |
| `HIGHEST` | 0m1.109s         | 3.8x            |

### Signalverlust {#signal-loss}

Der Vergleich wird mit dem Werkzeug `basisu` durchgeführt (Messung des PSNR).
100 dB bedeutet keinen Signalverlust (d. h., das Bild ist mit dem Originalbild identisch).

| Voreinstellung | Signal                                           |
| --------- | ------------------------------------------------ |
| `LOW`     | Max:  34 Mean: 0.470 RMS: 1.088 PSNR: 47.399 dB |
| `MEDIUM`  | Max:  35 Mean: 0.439 RMS: 1.061 PSNR: 47.620 dB |
| `HIGH`    | Max:  37 Mean: 0.898 RMS: 1.606 PSNR: 44.018 dB |
| `HIGHEST` | Max:  51 Mean: 1.298 RMS: 2.478 PSNR: 40.249 dB |

### Dateigrößen nach der Komprimierung {#compression-file-sizes}

Die ursprüngliche Dateigröße beträgt 1572882 Byte.

| Voreinstellung | Dateigrößen | Verhältnis |
| --------- | ---------- | ------- |
| `LOW`     | 357225     | 22.71 %  |
| `MEDIUM`  | 365548     | 23.24 %  |
| `HIGH`    | 277186     | 17.62 %  |
| `HIGHEST` | 254380     | 16.17 %  |


### Bildqualität {#image-quality}

Hier siehst du die resultierenden Bilder (mit dem Werkzeug `basisu` aus der ASTC-Kodierung gewonnen).

`LOW`
![Komprimierungsvoreinstellung LOW](images/texture_profiles/kodim03_pow2.fast.png)

`MEDIUM`
![Komprimierungsvoreinstellung MEDIUM](images/texture_profiles/kodim03_pow2.normal.png)

`HIGH`
![Komprimierungsvoreinstellung HIGH](images/texture_profiles/kodim03_pow2.high.png)

`HIGHEST`
![Beste Komprimierungsvoreinstellung](images/texture_profiles/kodim03_pow2.best.png)
