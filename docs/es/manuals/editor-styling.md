---
title: Estilo del editor
brief: Puedes modificar los colores, la tipografía y otros aspectos visuales del editor usando una hoja de estilos personalizada.
---

# Estilo del editor

Puedes modificar los colores, la tipografía y otros aspectos visuales del editor usando una hoja de estilos personalizada:

* Crea una carpeta llamada `.defold` en tu directorio de usuario.
  * En Windows `C:\Users\**Your Username**\.defold`
  * En macOS `/Users/**Your Username**/.defold`
  * En Linux `~/.defold`
* Crea un archivo `editor.css` en la carpeta `.defold`

Al iniciar, el editor cargará tu hoja de estilos personalizada y la aplicará sobre el estilo predeterminado. El editor usa JavaFX para la interfaz de usuario y las hojas de estilos son casi idénticas a los archivos CSS que se usan en un navegador para aplicar atributos de estilo a los elementos de una página web. Las hojas de estilos predeterminadas del editor están [disponibles para inspección en GitHub](https://github.com/defold/defold/tree/editor-dev/editor/styling/stylesheets/base).

## Cambiar el color

Los colores predeterminados se definen en [`_palette.scss`](https://github.com/defold/defold/blob/editor-dev/editor/styling/stylesheets/base/_palette.scss) y tienen este aspecto:

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

El tema básico se divide en tres grupos de colores (con variantes más oscuras y más claras):

* Color de fondo - color de fondo en paneles, ventanas y diálogos
* Color de componente - botones, controles de barras de desplazamiento y contornos de campos de texto
* Color de texto - texto e iconos

Por ejemplo, si agregas esto a tu hoja de estilos personalizada `editor.css` en la carpeta `.defold` del directorio de usuario:

```
* {
	-df-background-darker:    derive(#0a0a42, -10%);
	-df-background-dark:      derive(#0a0a42, -5%);
	-df-background:           #0a0a42;
	-df-background-light:     derive(#0a0a42, 10%);
	-df-background-lighter:   derive(#0a0a42, 20%);
}
```

Obtendrás el siguiente aspecto en tu editor:

![](images/editor/editor-styling-color.png)


## Cambiar las fuentes

El editor usa dos fuentes: `Dejavu Sans Mono` para código y texto monoespaciado (errores), y `Source Sans Pro` para el resto de la interfaz. Las definiciones de fuentes se encuentran principalmente en [`_typography.scss`](https://github.com/defold/defold/blob/editor-dev/editor/styling/stylesheets/base/_typography.scss) y tienen este aspecto:

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

La fuente principal se define en un elemento raíz, lo que facilita bastante reemplazar la fuente en la mayoría de los lugares. Agrega esto a tu `editor.css`:

```
@import url('https://fonts.googleapis.com/css2?family=Architects+Daughter&display=swap');

.root {
    -fx-font-family: "Architects Daughter";
}
```

Obtendrás el siguiente aspecto en tu editor:

![](images/editor/editor-styling-fonts.png)

También es posible usar una fuente local en lugar de una fuente web:

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
¡La fuente del editor de código se define por separado en las Preferences del editor!
:::
