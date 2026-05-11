---
title: Estilização do editor
brief: Você pode modificar as cores, a tipografia e outros aspectos visuais do editor usando uma stylesheet personalizada.
---

# Estilização do editor

Você pode modificar as cores, a tipografia e outros aspectos visuais do editor usando uma stylesheet personalizada:

* Crie uma pasta chamada `.defold` no diretório home do seu usuário.
  * No Windows `C:\Users\**Your Username**\.defold`
  * No macOS `/Users/**Your Username**/.defold`
  * No Linux `~/.defold`
* Crie um arquivo `editor.css` na pasta `.defold`

Ao iniciar, o editor carregará sua stylesheet personalizada e a aplicará por cima do estilo padrão. O editor usa JavaFX para a interface de usuário, e as stylesheets são quase idênticas aos arquivos CSS usados em um navegador para aplicar atributos de estilo aos elementos de uma página web. As stylesheets padrão do editor estão [disponíveis para inspeção no GitHub](https://github.com/defold/defold/tree/editor-dev/editor/styling/stylesheets/base).

## Alterando cores

As cores padrão são definidas em [`_palette.scss`](https://github.com/defold/defold/blob/editor-dev/editor/styling/stylesheets/base/_palette.scss) e se parecem com isto:

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

  e assim por diante...
```

O tema básico é dividido em três grupos de cores (com variantes mais escuras e mais claras):

* Cor de fundo - cor de fundo em painéis, janelas e diálogos
* Cor de componente - botões, alças de barra de rolagem, contornos de campos de texto
* Cor de texto - texto e ícones

Como exemplo, se você adicionar isto à sua stylesheet personalizada `editor.css` na pasta `.defold` do diretório home do usuário:

```
* {
	-df-background-darker:    derive(#0a0a42, -10%);
	-df-background-dark:      derive(#0a0a42, -5%);
	-df-background:           #0a0a42;
	-df-background-light:     derive(#0a0a42, 10%);
	-df-background-lighter:   derive(#0a0a42, 20%);
}
```

Você terá a seguinte aparência no seu editor:

![](images/editor/editor-styling-color.png)


## Alterando fontes

O editor usa duas fontes: `Dejavu Sans Mono` para código e texto monoespaçado (erros), e `Source Sans Pro` para o restante da UI. As definições de fonte são encontradas principalmente em [`_typography.scss`](https://github.com/defold/defold/blob/editor-dev/editor/styling/stylesheets/base/_typography.scss) e se parecem com isto:

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

e assim por diante...
```

A fonte principal é definida em um elemento root, o que torna bem fácil substituir a fonte na maioria dos lugares. Adicione isto ao seu `editor.css`:

```
@import url('https://fonts.googleapis.com/css2?family=Architects+Daughter&display=swap');

.root {
    -fx-font-family: "Architects Daughter";
}
```

Você terá a seguinte aparência no seu editor:

![](images/editor/editor-styling-fonts.png)

Também é possível usar uma fonte local em vez de uma fonte web:

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
A fonte do editor de código é definida separadamente nas Preferences do editor!
:::
