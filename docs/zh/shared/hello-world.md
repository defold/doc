## Hello World

这是在 Defold 中快速做出东西的方式。按步骤操作，然后再回来阅读手册其余部分。

1. 从 `Templates` 中选择空项目，在 `Title` 中命名，选择位置，然后点击 `Create New Project` 创建。项目会在 Defold Editor 中打开。
![Hello World Step 1](../shared/images/hello-world/helloworld_1.png)
2. 在左侧 `Assets` 面板中打开 `main` 文件夹，双击 `main.collection` 将其打开。
3. 在右侧 `Outline` 面板中右键点击 `Collection`，选择 `Add Game Object`。
![Hello World Step 2](../shared/images/hello-world/helloworld_2.png)
4. 右键点击创建出的 `go` 游戏对象，选择 `Add Component`，然后选择 `Label`。
![Hello World Step 3](../shared/images/hello-world/helloworld_3.png)
5. 在左下方的 `Properties` 面板中，在 `Text` 属性里输入一些文字。
6. 在中央主场景视图中拖动标签，将它放到大约 `(480,320,0)` 的位置，或在 `Properties` 的 `Position` 中修改。
![Hello World Step 4](../shared/images/hello-world/helloworld_4.png)
7. 修改标签位置后，点击 `File` -> `Save All` 保存项目，或使用快捷键 <kbd>Ctrl</kbd>+<kbd>S</kbd>（Mac 上为 <kbd>Cmd</kbd>+<kbd>S</kbd>）。
8. 点击 `Project` -> `Build` 构建项目，或使用快捷键 <kbd>Ctrl</kbd>+<kbd>B</kbd>（Mac 上为 <kbd>Cmd</kbd>+<kbd>B</kbd>）。
![Hello World Step 5](../shared/images/hello-world/helloworld_5.png)

你刚刚构建了自己的第一个 Defold 项目，并应该能在窗口中看到文字。游戏对象和组件的概念对你应该很熟悉。下面会解释集合、轮廓、属性，以及为什么需要把标签稍微往右上方移动。
