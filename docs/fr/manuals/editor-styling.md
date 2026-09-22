---
title: Personnalisation visuelle de l'éditeur
brief: Vous pouvez modifier les couleurs, la typographie et d'autres aspects visuels de l'éditeur à l'aide d'une feuille de style personnalisée.
---

# Personnalisation visuelle de l'éditeur {#editor-styling}

Vous pouvez modifier les couleurs, la typographie et d'autres aspects visuels de l'éditeur à l'aide d'une feuille de style personnalisée :

* Créez un dossier nommé `.defold` dans votre répertoire personnel.
  * Sous Windows `C:\Users\**Your Username**\.defold`
  * Sous macOS `/Users/**Your Username**/.defold`
  * Sous Linux `~/.defold`
* Créez un fichier `editor.css` dans le dossier `.defold`

Au démarrage, l'éditeur charge votre feuille de style personnalisée et l'applique par-dessus le style par défaut. L'éditeur utilise JavaFX pour l'interface utilisateur, et les feuilles de style sont presque identiques aux fichiers CSS utilisés dans un navigateur pour appliquer des attributs de style aux éléments d'une page web. Les feuilles de style par défaut de l'éditeur sont [consultables sur GitHub](https://github.com/defold/defold/tree/editor-dev/editor/styling/stylesheets/base).

## Modification des couleurs {#changing-color}

Les couleurs par défaut sont définies dans [`_palette.scss`](https://github.com/defold/defold/blob/editor-dev/editor/styling/stylesheets/base/_palette.scss) et se présentent comme suit :

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

Le thème de base est divisé en trois groupes de couleurs (avec des variantes plus sombres et plus claires) :

* Couleur de fond - couleur de fond des panneaux, fenêtres et boîtes de dialogue
* Couleur des composants - boutons, poignées des barres de défilement, contours des champs de texte
* Couleur du texte - texte et icônes

Par exemple, si vous ajoutez ceci à votre feuille de style personnalisée `editor.css` dans le dossier `.defold` de votre répertoire personnel :

```
* {
	-df-background-darker:    derive(#0a0a42, -10%);
	-df-background-dark:      derive(#0a0a42, -5%);
	-df-background:           #0a0a42;
	-df-background-light:     derive(#0a0a42, 10%);
	-df-background-lighter:   derive(#0a0a42, 20%);
}
```

Votre éditeur aura alors cette apparence :

![](images/editor/editor-styling-color.png)


## Modification des polices {#changing-fonts}

L'éditeur utilise deux polices : `Dejavu Sans Mono` pour le code et le texte à chasse fixe (erreurs), et `Source Sans Pro` pour le reste de l'interface utilisateur. Les définitions des polices se trouvent principalement dans [`_typography.scss`](https://github.com/defold/defold/blob/editor-dev/editor/styling/stylesheets/base/_typography.scss) et se présentent comme suit :

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

La police principale est définie dans un élément racine, ce qui permet de la remplacer assez facilement à la plupart des endroits. Ajoutez ceci à votre fichier `editor.css` :

```
@import url('https://fonts.googleapis.com/css2?family=Architects+Daughter&display=swap');

.root {
    -fx-font-family: "Architects Daughter";
}
```

Votre éditeur aura alors cette apparence :

![](images/editor/editor-styling-fonts.png)

Il est également possible d'utiliser une police locale à la place d'une police web :

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
La police de l'éditeur de code est définie séparément dans la fenêtre Preferences de l'éditeur !
:::
