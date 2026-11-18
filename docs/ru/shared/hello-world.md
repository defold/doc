## Hello World

Это быстрый способ быстро сделать что-то в Defold: выполните шаги, а потом вернитесь и дочитайте остальную часть руководства.

1. Выберите пустой проект в `Templates`, задайте имя в `Title`, выберите расположение и создайте его, нажав `Create New Project`. Проект откроется в редакторе Defold.
![Hello World, шаг 1](../shared/images/hello-world/helloworld_1.png)
2. Слева, в панели `Assets`, откройте папку `main` и дважды щелкните по `main.collection`, чтобы открыть ее.
3. Справа, в панели `Outline`, щелкните правой кнопкой мыши по `Collection` и выберите `Add Game Object`.
![Hello World, шаг 2](../shared/images/hello-world/helloworld_2.png)
4. Щелкните правой кнопкой мыши по созданному game object `go`, выберите `Add Component`, а затем `Label`.
![Hello World, шаг 3](../shared/images/hello-world/helloworld_3.png)
5. Ниже, слева, в панели `Properties`, введите что-нибудь в свойство `Text`.
6. В основной центральной сцене перетащите и переместите label в позицию около `(480,320,0)`, либо измените это значение в `Properties`: `Position`.
![Hello World, шаг 4](../shared/images/hello-world/helloworld_4.png)
7. После изменения позиции label сохраните проект через `File` -> `Save All` или сочетанием клавиш <kbd>Ctrl</kbd>+<kbd>S</kbd> (<kbd>Cmd</kbd>+<kbd>S</kbd> на Mac).
8. Соберите проект через `Project` -> `Build` или сочетанием клавиш <kbd>Ctrl</kbd>+<kbd>B</kbd> (<kbd>Cmd</kbd>+<kbd>B</kbd> на Mac).
![Hello World, шаг 5](../shared/images/hello-world/helloworld_5.png)

Вы только что собрали свой первый проект в Defold и должны увидеть свой текст в окне. Концепции game object и component должны быть вам знакомы. Collections, outline, properties и то, почему нам понадобилось немного сместить label в правый верхний угол, объясняются ниже.
