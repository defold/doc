---
title: Personalizzazione dell'aspetto dell'editor
brief: Puoi modificare i colori, la tipografia e altri aspetti visivi dell'editor usando un foglio di stile personalizzato.
---

# Personalizzazione dell'aspetto dell'editor {#editor-styling}

Puoi modificare i colori, la tipografia e altri aspetti visivi dell'editor usando un foglio di stile personalizzato:

* Crea una cartella chiamata `.defold` nella tua directory home.
  * Su Windows `C:\Users\**Your Username**\.defold`
  * Su macOS `/Users/**Your Username**/.defold`
  * Su Linux `~/.defold`
* Crea un file `editor.css` nella cartella `.defold`

All'avvio, l'editor carica il tuo foglio di stile personalizzato e lo applica allo stile predefinito, sovrascrivendone le proprietà corrispondenti. L'editor usa JavaFX per l'interfaccia utente e i fogli di stile sono quasi identici ai file CSS usati dai browser per applicare attributi di stile agli elementi di una pagina web. Puoi [consultare i fogli di stile predefiniti dell'editor su GitHub](https://github.com/defold/defold/tree/editor-dev/editor/styling/stylesheets/base).

## Modifica dei colori {#changing-color}

I colori predefiniti sono definiti in [`_palette.scss`](https://github.com/defold/defold/blob/editor-dev/editor/styling/stylesheets/base/_palette.scss) in questo modo:

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

Il tema di base è suddiviso in tre gruppi di colori (con varianti più scure e più chiare):

* Colore di sfondo - colore di sfondo di pannelli, finestre e finestre di dialogo
* Colore dei componenti - pulsanti, cursori delle barre di scorrimento, contorni dei campi di testo
* Colore del testo - testo e icone

Per esempio, se aggiungi quanto segue al tuo foglio di stile personalizzato `editor.css` nella cartella `.defold` della tua directory home:

```
* {
	-df-background-darker:    derive(#0a0a42, -10%);
	-df-background-dark:      derive(#0a0a42, -5%);
	-df-background:           #0a0a42;
	-df-background-light:     derive(#0a0a42, 10%);
	-df-background-lighter:   derive(#0a0a42, 20%);
}
```

L'editor avrà questo aspetto:

![](images/editor/editor-styling-color.png)


## Modifica dei caratteri {#changing-fonts}

L'editor usa due caratteri: `Dejavu Sans Mono` per il codice e il testo a spaziatura fissa (errori) e `Source Sans Pro` per il resto dell'interfaccia utente. Le definizioni dei caratteri si trovano principalmente in [`_typography.scss`](https://github.com/defold/defold/blob/editor-dev/editor/styling/stylesheets/base/_typography.scss) e hanno questa forma:

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

Il carattere principale è definito in un elemento radice, quindi è piuttosto semplice sostituirlo nella maggior parte dell'interfaccia. Aggiungi quanto segue al tuo file `editor.css`:

```
@import url('https://fonts.googleapis.com/css2?family=Architects+Daughter&display=swap');

.root {
    -fx-font-family: "Architects Daughter";
}
```

L'editor avrà questo aspetto:

![](images/editor/editor-styling-fonts.png)

Puoi anche usare un carattere locale al posto di un carattere web:

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
Il carattere dell'editor di codice si imposta separatamente in Preferences nell'editor!
:::
