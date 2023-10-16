---
title: Stylizacja Edytora
brief: Ta instrukcja opisuje jak modyifkować kolorystykę, typografię i inne wizualne aspekty Edytora Defold używając własnych stylesheetów.
---

# Stylizacja Edytora

Możesz modyfikować kolorystykę, typografię i inne aspekty wizualne Edytora Defold za pomocą niestandardowego arkusza stylów (stylesheet):

* Utwórz folder o nazwie `.defold` w katalogu domowym użytkownika.
  * W systemie Windows `C:\Users\**Twoja Nazwa Użytkownika**\.defold`
  * W systemie macOS `/Users/**Twoja Nazwa Użytkownika**/.defold`
  * W systemie Linux `~/.defold`
* Utwórz plik `editor.css` w folderze `.defold`.

Podczas uruchamiania Edytor automatycznie wczytuje niestandardowy arkusz stylów i zastosuje go wobec domyślnego stylu. Edytor używa JavaFX do interfejsu użytkownika, a arkusze stylów są prawie identyczne z plikami CSS używanymi w przeglądarce do definiowania atrybutów stylu elementów strony internetowej. Domyślne arkusze stylów edytora są [dostępne do wglądu na GitHubie](https://github.com/defold/defold/tree/editor-dev/editor/styling/stylesheets/base).

## Zmiana kolorystyki

Domyślne kolory są zdefiniowane w pliku [`_palette.scss`](https://github.com/defold/defold/blob/editor-dev/editor/styling/stylesheets/base/_palette.scss) i wyglądają następująco:

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

Podstawowa paleta kolorów jest podzielona na trzy grupy kolorów (z ciemniejszymi i jaśniejszymi wariantami):

* Background color (kolor tła) - kolor tła w panelach, oknach, oknach dialogowych
* Component color (kolor komponentu) - przyciski, uchwyty paska przewijania, obrysy pola tekstowego
* Text color (Kolor tekstu) - tekst i ikony

Jako przykład, jeśli dodasz to do niestandardowego arkusza stylów `editor.css` w folderze `.defold` w katalogu domowym użytkownika:

```
* {
	-df-background-darker:    derive(#0a0a42, -10%);
	-df-background-dark:      derive(#0a0a42, -5%);
	-df-background:           #0a0a42;
	-df-background-light:     derive(#0a0a42, 10%);
	-df-background-lighter:   derive(#0a0a42, 20%);
}
```

Otrzymasz następujący wygląd Edytora:

![](images/editor/editor-styling-color.png)


## Zmiana czcionek

Edytor Defold używa domyślnie dwóch czcionek: `Dejavu Sans Mono` dla kodu i tekstu o stałej szerokości (np. błędów) oraz `Source Sans Pro` dla reszty interfejsu użytkownika. Definicje czcionek znajdują się przeważnie w pliku [`_typography.scss`](https://github.com/defold/defold/blob/editor-dev/editor/styling/stylesheets/base/_typography.scss) i wyglądają tak:

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

Główna czcionka jest zdefiniowana w elemencie głównym (root), co sprawia, że jest dość łatwo zamienić czcionkę w większości miejsc. Dodaj to do swojego arkusza stylów `editor.css`:

```
@import url('https://fonts.googleapis.com/css2?family=Architects+Daughter&display=swap');

.root {
    -fx-font-family: "Architects Daughter";
}
```

Otrzymasz następujący wygląd Edytora:

![](images/editor/editor-styling-fonts.png)

Jest również możliwość użycia lokalnej czcionki zamiast czcionki internetowej:

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
Czcionka edytora kodu jest zdefiniowana osobno w preferencjach edytora!
:::
