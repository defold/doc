---
title: Gestaltung des Editors
brief: Mit einem benutzerdefinierten Stylesheet kannst du die Farben, die Typografie und andere visuelle Aspekte des Editors ändern.
---

# Gestaltung des Editors {#editor-styling}

Mit einem benutzerdefinierten Stylesheet kannst du die Farben, die Typografie und andere visuelle Aspekte des Editors ändern:

* Erstelle in deinem Benutzerverzeichnis einen Ordner namens `.defold`.
  * Unter Windows `C:\Users\**Your Username**\.defold`
  * Unter macOS `/Users/**Your Username**/.defold`
  * Unter Linux `~/.defold`
* Erstelle eine Datei namens `editor.css` im Ordner `.defold`

Beim Start lädt der Editor dein benutzerdefiniertes Stylesheet und wendet es zusätzlich zum Standardstil an. Der Editor verwendet JavaFX für die Benutzeroberfläche. Die Stylesheets sind nahezu identisch mit den CSS-Dateien, mit denen ein Browser Stilattribute auf die Elemente einer Webseite anwendet. Die Standard-Stylesheets des Editors kannst du [auf GitHub einsehen](https://github.com/defold/defold/tree/editor-dev/editor/styling/stylesheets/base).

## Farben ändern {#changing-color}

Die Standardfarben sind in [`_palette.scss`](https://github.com/defold/defold/blob/editor-dev/editor/styling/stylesheets/base/_palette.scss) definiert und sehen so aus:

```
* {
	// Background
	-df-background-darker:    derive(#212428, -10%);
	-df-background-dark:      derive(#212428, -5%);
	-df-background:           #212428;
	-df-background-light:     derive(#212428, 10%);
	-df-background-lighter:   derive(#212428, 20%);

	// Component
	-df-component-darker:     derive(#464c55, -20%);
	-df-component-dark:       derive(#464c55, -10%);
	-df-component:            #464c55;
	-df-component-light:      derive(#464c55, 10%);
	-df-component-lighter:    derive(#464c55, 20%);

	// Text & icons
	-df-text-dark:            derive(#b4bac1, -10%);
	-df-text:                 #b4bac1;
	-df-text-selected:        derive(#b4bac1, 20%);

  and so on...
```

Das grundlegende Erscheinungsbild ist in drei Farbgruppen unterteilt (mit dunkleren und helleren Varianten):

* Hintergrundfarbe - Hintergrundfarbe in Bereichen, Fenstern und Dialogfeldern
* Farbe der Bedienelemente - Schaltflächen, Schieber von Bildlaufleisten, Umrandungen von Textfeldern
* Textfarbe - Text und Symbole

Wenn du beispielsweise Folgendes zu deinem benutzerdefinierten Stylesheet `editor.css` im Ordner `.defold` in deinem Benutzerverzeichnis hinzufügst:

```
* {
	-df-background-darker:    derive(#0a0a42, -10%);
	-df-background-dark:      derive(#0a0a42, -5%);
	-df-background:           #0a0a42;
	-df-background-light:     derive(#0a0a42, 10%);
	-df-background-lighter:   derive(#0a0a42, 20%);
}
```

Dann sieht dein Editor so aus:

![](images/editor/editor-styling-color.png)


## Schriftarten ändern {#changing-fonts}

Der Editor verwendet zwei Schriftarten: `Dejavu Sans Mono` für Code und Text mit fester Zeichenbreite (Fehlermeldungen) sowie `Source Sans Pro` für den Rest der Benutzeroberfläche. Die Schriftartdefinitionen befinden sich hauptsächlich in [`_typography.scss`](https://github.com/defold/defold/blob/editor-dev/editor/styling/stylesheets/base/_typography.scss) und sehen so aus:

```
@font-face {
  src: url("SourceSansPro-Light.ttf");
}

@font-face {
  src: url("DejaVuSansMono.ttf");
}

$default-font-mono: 'Dejavu Sans Mono';
$default-font: 'Source Sans Pro';
$default-font-bold: 'Source Sans Pro Semibold';
$default-font-italic: 'Source Sans Pro Italic';
$default-font-light: 'Source Sans Pro Light';

.root {
    -fx-font-size: 13px;
    -fx-font-family: $default-font;
}

Text.strong {
  -fx-font-family: $default-font-bold;
}

and so on...
```

Die Hauptschriftart ist in einem Wurzelelement definiert. Dadurch lässt sich die Schriftart an den meisten Stellen recht leicht ersetzen. Füge Folgendes zu deiner `editor.css` hinzu:

```
@import url('https://fonts.googleapis.com/css2?family=Architects+Daughter&display=swap');

.root {
    -fx-font-family: "Architects Daughter";
}
```

Dann sieht dein Editor so aus:

![](images/editor/editor-styling-fonts.png)

Du kannst auch eine lokale Schriftart anstelle einer Webschriftart verwenden:

```
@font-face {
  font-family: 'Comic Sans MS';
  src: local("cs.ttf");
}

.root {
  -fx-font-family: 'Comic Sans MS';
}
```

::: sidenote
Die Schriftart des Code-Editors wird separat unter Preferences in den Editoreinstellungen festgelegt!
:::
