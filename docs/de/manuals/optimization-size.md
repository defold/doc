---
title: Die Größe eines Defold-Spiels optimieren
brief: Dieses Handbuch beschreibt, wie du die Größe eines Defold-Spiels optimierst.
---

# Die Spielgröße optimieren {#optimizing-game-size}

Die Größe deines Spiels kann auf Plattformen wie dem Web und Mobilgeräten ein entscheidender Erfolgsfaktor sein. Auf Desktopcomputern und Konsolen ist sie dagegen weniger wichtig, da Speicherplatz dort günstig und oft reichlich vorhanden ist.

### iOS und Android {#ios-and-android}
Apple und Google haben Größenbeschränkungen für Anwendungen festgelegt, die über Mobilfunknetze heruntergeladen werden (im Gegensatz zum Download über WLAN). Unter Android liegt diese Grenze bei 200 MB für Apps, die als [App Bundles](https://developer.android.com/guide/app-bundle#size_restrictions) veröffentlicht werden. Unter iOS erhalten Nutzer eine Warnung, wenn die Anwendung größer als 200 MB ist, können den Download aber trotzdem fortsetzen.

::: sidenote
Eine Studie aus dem Jahr 2017 zeigte: „Für jede Zunahme der APK-Größe um 6 MB beobachten wir einen Rückgang der Installationskonversionsrate um 1 %.“ ([Quelle](https://medium.com/googleplaydev/shrinking-apks-growing-installs-5d3fcba23ce2))
:::

### HTML5
Poki und viele andere Plattformen für Webspiele empfehlen, dass der anfängliche Download nicht größer als 5 MB sein sollte.

Facebook empfiehlt, dass ein Facebook Instant Game in weniger als 5 Sekunden und vorzugsweise in weniger als 3 Sekunden starten sollte. Was das für die tatsächliche Anwendungsgröße bedeutet, ist nicht klar definiert, aber gemeint sind Größen im Bereich von bis zu 20 MB.

Spielbare Werbeanzeigen sind je nach Werbenetzwerk üblicherweise auf 2 bis 5 MB begrenzt.

## Strategien zur Größenoptimierung {#size-optimization-strategies}
Du kannst die Anwendungsgröße auf zwei Arten optimieren: indem du die Größe der Engine und/oder die Größe der Spiel-Assets reduzierst.

Um besser zu verstehen, woraus sich die Größe deiner Anwendung zusammensetzt, kannst du bei der Bundle-Erstellung [einen Build-Bericht erzeugen](/manuals/bundling/#build-reports). Häufig machen Audiodateien und Grafiken den größten Teil der Größe eines Spiels aus.

::: important
Defold erstellt beim Erstellen von Builds und Bundles deiner Anwendung einen Abhängigkeitsbaum. Das Build-System beginnt bei der Startsammlung (bootstrap collection), die in der Datei *game.project* angegeben ist, und untersucht jede referenzierte Sammlung (collection), jedes Spielobjekt (game object) und jede Komponente (component), um eine Liste der verwendeten Assets zu erstellen. Nur diese Assets werden in das endgültige Anwendungsbundle aufgenommen. Alles, was nicht direkt referenziert wird, wird ausgeschlossen. Es ist zwar gut zu wissen, dass ungenutzte Assets nicht aufgenommen werden, dennoch musst du bei der Entwicklung berücksichtigen, was in die endgültige Anwendung gelangt, wie groß die einzelnen Assets sind und wie groß das Anwendungsbundle insgesamt ist. 
:::

## Die Größe der Engine optimieren {#optimize-engine-size}
Eine schnelle Möglichkeit, die Größe der Engine zu reduzieren, besteht darin, nicht verwendete Funktionen aus der Engine zu entfernen. Dazu dient die [Anwendungsmanifestdatei](https://defold.com/manuals/app-manifest/), über die du nicht benötigte Engine-Komponenten entfernen kannst. Beispiele:

* Physik - Wenn dein Spiel weder Box2D- noch Bullet3D-Physik verwendet, wird dringend empfohlen, die Physik-Engines zu entfernen.
* GUI, Partikeleffekte und Kachelkarten (tile maps) - Diese Komponenten lassen sich mit den [Komponentenschaltern im Anwendungsmanifest](/manuals/app-manifest/#exclude-gui) einzeln ausschließen. Entferne Komponentenreferenzen und API-Aufrufe für jede Funktion, die du ausschließt. Wenn du Partikeleffekte ausschließt, entfällt auch die Unterstützung für Partikelknoten in GUI-Szenen.
* Formatierter Text (rich text) - Deaktiviere [Use Rich Text](/manuals/app-manifest/#use-rich-text), wenn Beschriftungen (labels) und GUI-Texte nur unformatierten Text benötigen. Dadurch entfallen die Verarbeitung von formatiertem Text und Stileffekte, während das gewöhnliche Rendern von Text erhalten bleibt.
* Live Update - Wenn dein Spiel Live Update nicht verwendet, kannst du es entfernen.
* Laden von Bildern - Wenn dein Spiel Bilder nicht manuell mit `image.load()` lädt und dekodiert.
* BasisU - Wenn dein Spiel nur wenige Texturen enthält, vergleiche die Build-Größe ohne BasisU (über das Anwendungsmanifest entfernt) und ohne Texturkomprimierung mit einem Build mit BasisU und komprimierten Texturen. Bei Spielen mit wenigen Texturen kann es vorteilhafter sein, die Größe der Binärdatei zu reduzieren und auf Texturkomprimierung zu verzichten. Außerdem kann der Verzicht auf den Transcoder den zum Ausführen deines Spiels benötigten Speicher reduzieren.

## Die Größe der Assets optimieren {#optimize-asset-size}
Die größten Einsparungen bei der Größenoptimierung von Assets erreichst du meist, indem du die Größe von Audiodateien und Texturen reduzierst.

### Audiodateien optimieren {#optimize-sounds}
Defold unterstützt diese Formate:
* .wav
* .ogg
* .opus

Defold unterstützt PCM-Wave-Dateien mit 8 Bit und 16 Bit. Ogg Vorbis und Ogg Opus verwenden ihre jeweiligen komprimierten Formate und setzen keine bestimmte PCM-Bittiefe voraus. Der Opus-Decoder ist standardmäßig nicht enthalten. Aktiviere **Include Sound Decoder: Opus** im [Anwendungsmanifest](/manuals/app-manifest/#sound), bevor du `.opus`-Ressourcen verwendest.
Die Audiodecoder von Defold erhöhen oder verringern die Abtastraten nach Bedarf für das aktuelle Audiogerät.

Kürzere Audiodateien wie Soundeffekte werden häufig stärker komprimiert, während Musikdateien weniger stark komprimiert werden.
Defold führt keine Komprimierung durch. Du musst dich daher bei der Entwicklung für jedes Audioformat gesondert darum kümmern.

Du kannst die Audiodateien in einem externen Audiobearbeitungsprogramm bearbeiten (oder über die Kommandozeile, beispielsweise mit [ffmpeg](https://ffmpeg.org)), um die Qualität zu reduzieren oder zwischen Formaten zu konvertieren. Ziehe auch in Betracht, Audiodateien von Stereo in Mono umzuwandeln, um die Größe der Inhalte weiter zu reduzieren.

### Texturen optimieren {#optimize-textures}
Du hast mehrere Möglichkeiten, die von deinem Spiel verwendeten Texturen zu optimieren. Zunächst solltest du jedoch die Größe der Bilder prüfen, die einem Atlas hinzugefügt oder als Kachelquelle (tile source) verwendet werden. Du solltest niemals größere Bilder verwenden, als dein Spiel tatsächlich benötigt. Große Bilder zu importieren und sie dann auf die passende Größe zu verkleinern, verschwendet Texturspeicher und sollte vermieden werden. Passe die Bilder zunächst mit einem externen Bildbearbeitungsprogramm an die tatsächlich im Spiel benötigte Größe an. Für Dinge wie Hintergrundbilder kann es auch ausreichen, ein kleines Bild zu verwenden und es auf die gewünschte Größe zu vergrößern. Sobald deine Bilder die richtige Größe haben und Atlanten hinzugefügt wurden oder in Kachelquellen verwendet werden, musst du auch die Größe der Atlanten selbst berücksichtigen. Die maximal nutzbare Atlasgröße hängt von der Plattform und der Grafikhardware ab.

::: sidenote
[Dieser Forenbeitrag](https://forum.defold.com/t/texture-management-in-defold/8921/17?u=britzl) enthält mehrere Tipps dazu, wie du die Größe mehrerer Bilder mithilfe von Skripten oder Software von Drittanbietern ändern kannst.
:::

* Maximale Texturgröße unter HTML5 laut den Meldungen an das [Web3D-Survey-Projekt](https://web3dsurvey.com/webgl/parameters/MAX_TEXTURE_SIZE)
* Maximale Texturgröße unter iOS:
  * iPad: 2048x2048
  * iPhone 4: 2048x2048
  * iPad 2, 3, Mini, Air, Pro: 4096x4096
  * iPhone 4s, 5, 6+, 6s: 4096x4096
* Die maximale Texturgröße unter Android variiert stark, aber im Allgemeinen unterstützen alle einigermaßen neuen Geräte mindestens 4096x4096.

Wenn ein Atlas zu groß ist, musst du ihn entweder in mehrere kleinere Atlanten aufteilen, mehrseitige Atlanten verwenden oder den gesamten Atlas mithilfe eines Texturprofils skalieren. Das Texturprofilsystem von Defold ermöglicht dir, sowohl ganze Atlanten zu skalieren als auch Komprimierungsalgorithmen anzuwenden, um die Größe des Atlas auf dem Datenträger zu reduzieren. Du kannst [im Handbuch mehr über Texturprofile lesen](/manuals/texture-profiles/). Wenn du nicht weißt, was du verwenden sollst, probiere diese Einstellungen als Ausgangspunkt für weitere Anpassungen aus:

* mipmaps: false
* premultiply_alpha: true
* format: TEXTURE_FORMAT_RGBA
* compression_level: NORMAL
* compression_type: COMPRESSION_TYPE_BASIS_UASTC

::: sidenote
Mehr zum Optimieren und Verwalten von Texturen erfährst du in [diesem Forenbeitrag](https://forum.defold.com/t/texture-management-in-defold/8921).
:::

### Schriftarten optimieren {#optimize-fonts}
Deine Schriftarten werden kleiner, wenn du die verwendeten Zeichen festlegst und sie unter [Characters](/manuals/font/#properties) angibst, anstatt das Kontrollkästchen All Chars zu verwenden.

### Inhalte für den Download bei Bedarf ausschließen {#exclude-content-for-download-on-demand}
Eine weitere Möglichkeit, die anfängliche Anwendungsgröße zu reduzieren, besteht darin, Teile der Spielinhalte aus dem Anwendungsbundle auszuschließen und sie bei Bedarf herunterzuladen. Defold bietet ein System namens Live Update, mit dem sich Inhalte für den Download bei Bedarf ausschließen lassen.

Ausgeschlossene Inhalte können von ganzen Levels bis zu freischaltbaren Charakteren, Skins, Waffen oder Fahrzeugen reichen. Wenn dein Spiel viele Inhalte hat, organisiere den Ladevorgang so, dass die Startsammlung und die Sammlung des ersten Levels nur die für dieses Level unbedingt erforderlichen Ressourcen enthalten. Das erreichst du mit Sammlungs-Proxys (collection proxies) oder Fabriken (factories), bei denen das Kontrollkästchen „Exclude“ aktiviert ist. Teile die Ressourcen entsprechend dem Spielfortschritt auf. Dieser Ansatz sorgt für ein effizientes Laden der Ressourcen und hält den anfänglichen Speicherverbrauch niedrig. Erfahre mehr im [Handbuch zu Live Update](/manuals/live-update/).

## Android-spezifische Größenoptimierungen {#android-specific-size-optimizations}
Android-Builds müssen sowohl 32-Bit- als auch 64-Bit-CPU-Architekturen unterstützen. Wenn du [ein Bundle für Android erstellst](/manuals/android), kannst du angeben, welche CPU-Architekturen enthalten sein sollen:

![Ein Android-Bundle signieren](images/android/sign_bundle.png)

Standardmäßig enthält ein Bundle die Architekturen `armv7-android` und `arm64-android`. Eine dritte Architektur, `x86_64-android`, ist verfügbar, aber standardmäßig nicht enthalten, da sie hauptsächlich für Android-Emulatoren, ChromeOS und Windows Subsystem for Android und weniger für physische Geräte nützlich ist. Lass sie deaktiviert, um die Bundle-Größe gering zu halten, sofern du nicht gezielt eine dieser Umgebungen unterstützen musst.

Google Play unterstützt [mehrere APKs](https://developer.android.com/google/play/publishing/multiple-apks) pro Veröffentlichung eines Spiels. Das bedeutet, dass du die Anwendungsgröße reduzieren kannst, indem du zwei APKs erzeugst, eines pro CPU-Architektur, und beide bei Google Play hochlädst.

Du kannst auch eine Kombination aus [APK Expansion Files](https://developer.android.com/google/play/expansion-files) und [Live-Update-Inhalten](/manuals/live-update) verwenden, die dir die [APKX-Erweiterung im Asset Portal](https://defold.com/assets/apkx/) ermöglicht.
