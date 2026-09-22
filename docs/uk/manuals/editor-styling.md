---
title: Оформлення редактора
brief: Ви можете змінювати кольори, типографіку та інші візуальні аспекти редактора за допомогою власної таблиці стилів.
---

# Оформлення редактора {#editor-styling}

Ви можете змінювати кольори, типографіку та інші візуальні аспекти редактора за допомогою власної таблиці стилів:

* Створіть папку з назвою `.defold` у домашньому каталозі користувача.
  * У Windows `C:\Users\**Your Username**\.defold`
  * У macOS `/Users/**Your Username**/.defold`
  * У Linux `~/.defold`
* Створіть файл `editor.css` у папці `.defold`

Під час запуску редактор завантажить вашу таблицю стилів і застосує її поверх стандартного стилю. Для інтерфейсу користувача редактор використовує JavaFX, а таблиці стилів майже ідентичні файлам CSS, які браузер використовує для застосування атрибутів стилю до елементів вебсторінки. Стандартні таблиці стилів редактора [можна переглянути на GitHub](https://github.com/defold/defold/tree/editor-dev/editor/styling/stylesheets/base).

## Змінення кольору {#changing-color}

Стандартні кольори визначено у файлі [`_palette.scss`](https://github.com/defold/defold/blob/editor-dev/editor/styling/stylesheets/base/_palette.scss), і вони мають такий вигляд:

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

Базову тему поділено на три групи кольорів (із темнішими та світлішими варіантами):

* Колір тла — колір тла панелей, вікон, діалогових вікон
* Колір компонентів — кнопки, повзунки смуг прокручування, контури текстових полів
* Колір тексту — текст і піктограми

Наприклад, якщо ви додасте цей код до власної таблиці стилів `editor.css` у папці `.defold` у домашньому каталозі користувача:

```
* {
	-df-background-darker:    derive(#0a0a42, -10%);
	-df-background-dark:      derive(#0a0a42, -5%);
	-df-background:           #0a0a42;
	-df-background-light:     derive(#0a0a42, 10%);
	-df-background-lighter:   derive(#0a0a42, 20%);
}
```

Ваш редактор матиме такий вигляд:

![](images/editor/editor-styling-color.png)


## Змінення шрифтів {#changing-fonts}

Редактор використовує два шрифти: `Dejavu Sans Mono` для коду й моноширинного тексту (помилок) та `Source Sans Pro` для решти інтерфейсу. Визначення шрифтів переважно містяться у файлі [`_typography.scss`](https://github.com/defold/defold/blob/editor-dev/editor/styling/stylesheets/base/_typography.scss) і мають такий вигляд:

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

Основний шрифт визначено в кореневому елементі, завдяки чому його досить легко замінити в більшості місць. Додайте цей код до файлу `editor.css`:

```
@import url('https://fonts.googleapis.com/css2?family=Architects+Daughter&display=swap');

.root {
    -fx-font-family: "Architects Daughter";
}
```

Ваш редактор матиме такий вигляд:

![](images/editor/editor-styling-fonts.png)

Також можна використовувати локальний шрифт замість вебшрифту:

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
Шрифт редактора коду визначається окремо в налаштуваннях редактора Preferences!
:::
