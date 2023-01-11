---
title: 编辑器风格
brief: 您可以使用自定义 stylesheet 修改编辑器配色, 文本及其他可视元素.
---

# 编辑器风格

您可以使用自定义 stylesheet 修改编辑器配色, 文本及其他可视元素:

* 在用户目录下创建文件夹并命名为 `.defold`.
   * Windows 路径 `C:\Users\**Your Username**\.defold`
   * macOS 路径 `/Users/**Your Username**/.defold`
   * Linux 路径 `~/.defold`
 *  在 `.defold` 目录下创建一个 `editor.css` 文件.

编辑器启动时会加载您的自定义 stylesheet 作为优先默认风格. 编辑器使用 JavaFX 编写用户界面所以 stylesheets 几乎等价于浏览器里支持的网页 CSS 文件. 官方默认的 stylesheets 保存于 [GitHub 上](https://github.com/defold/defold/tree/editor-dev/editor/styling/stylesheets/base).

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

基本配色主题分为三大部分 (分为深色浅色两种方案):

* Background color - 面板, 窗口, 对话框的背景颜色
* Component color - 按钮, 卷动条手柄, 文字描边颜色
* Text color - 文字和图标颜色

默认情况下, 如果在系统用户目录下的 `.defold` 文件夹下提供自定义 `editor.css` stylesheet:

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

编辑器使用两种字体: 代码编写和单行距文本(报错文字)用 `Dejavu Sans Mono`, 其他 UI 用 `Source Sans Pro`. 文字定义主要保存在 [`_typography.scss`](https://github.com/defold/defold/blob/editor-dev/editor/styling/stylesheets/base/_typography.scss) 中, 如下所示:

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

主要字体定义在树形结构根部以便于调整修改. 将如下 `editor.css` 应用后:

```
@import url('https://fonts.googleapis.com/css2?family=Architects+Daughter&display=swap');

.root {
    -fx-font-family: "Architects Daughter";
}
```

则您的编辑器文本会如下图所示:

![](images/editor/editor-styling-fonts.png)

使用本地字体代替网络字体也是可以的:

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
