---
title: 编辑器风格
brief: 您可以使用自定义样式表修改编辑器的颜色、字体排版及其他视觉元素。
---

# 编辑器风格

您可以使用自定义样式表修改编辑器的颜色、字体排版及其他视觉元素：

* 在用户目录下创建文件夹并命名为 `.defold`.
   * Windows 路径 `C:\Users\**Your Username**\.defold`
   * macOS 路径 `/Users/**Your Username**/.defold`
   * Linux 路径 `~/.defold`
 *  在 `.defold` 目录下创建一个 `editor.css` 文件.

编辑器启动时会加载您的自定义样式表并将其应用在默认样式之上。编辑器使用 JavaFX 编写用户界面，所以样式表几乎等价于浏览器中用于网页的 CSS 文件。官方默认的样式表保存于 [GitHub 上](https://github.com/defold/defold/tree/editor-dev/editor/styling/stylesheets/base)。

## 修改颜色

默认颜色在 [`_palette.scss`](https://github.com/defold/defold/blob/editor-dev/editor/styling/stylesheets/base/_palette.scss) 中定义, 类似如下设置:

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

基本配色主题分为三大部分（分为深色和浅色两种方案）：

* Background color - 面板、窗口、对话框的背景颜色
* Component color - 按钮、滚动条手柄、文本框边框颜色
* Text color - 文本和图标颜色

作为一个例子，如果您在用户主目录下的`.defold`文件夹中的自定义`editor.css`样式表中添加以下内容：

```
* {
	-df-background-darker:    derive(#0a0a42, -10%);
	-df-background-dark:      derive(#0a0a42, -5%);
	-df-background:           #0a0a42;
	-df-background-light:     derive(#0a0a42, 10%);
	-df-background-lighter:   derive(#0a0a42, 20%);
}
```

则您的编辑器配色会如下图所示:

![](images/editor/editor-styling-color.png)


## 修改字体

编辑器使用两种字体：代码编写和等宽文本（错误信息）使用`Dejavu Sans Mono`，其他UI使用`Source Sans Pro`。字体定义主要保存在[`_typography.scss`](https://github.com/defold/defold/blob/editor-dev/editor/styling/stylesheets/base/_typography.scss)中，如下所示：

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

主要字体定义在根元素中，这使得在大多数地方替换字体变得相当容易。将以下内容添加到您的`editor.css`中：

```
@import url('https://fonts.googleapis.com/css2?family=Architects+Daughter&display=swap');

.root {
    -fx-font-family: "Architects Daughter";
}
```

您的编辑器字体将会如下图所示：

![](images/editor/editor-styling-fonts.png)

也可以使用本地字体而不是网络字体：

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
代码编辑器所用字体是在编辑器设置中定义的!
:::
