## Hello World

Esta es una forma rápida de hacer algo en Defold: sigue los pasos y luego vuelve para leer el resto del manual.

1. Selecciona un proyecto vacío desde `Templates`, asígnale un nombre en `Title`, elige la ubicación y créalo haciendo click en `Create New Project`. Se abrirá en el editor Defold.
![Hello World Step 1](../manuals/images/unity/helloworld_1.png)
2. En el lado izquierdo, en el panel `Assets`, abre la carpeta `main` y haz doble click en `main.collection` para abrirla.
3. En el lado derecho, en el panel `Outline`, haz click derecho en `Collection` y selecciona `Add Game Object`.
![Hello World Step 2](../manuals/images/unity/helloworld_2.png)
4. Haz click derecho en el objeto de juego `go` creado, selecciona `Add Component` y luego `Label`.
![Hello World Step 3](../manuals/images/unity/helloworld_3.png)
5. Abajo a la izquierda, en el panel `Properties`, escribe algo en la propiedad `Text`.
6. En la vista principal central de la escena, arrastra, mueve y suelta la label para colocarla alrededor de `(480,320,0)`, o cambia su posición en `Properties`: `Position`.
![Hello World Step 4](../manuals/images/unity/helloworld_4.png)
7. Después de cambiar la posición de la label, guarda el proyecto haciendo click en `File` -> `Save All` o con el atajo <kbd>Ctrl</kbd>+<kbd>S</kbd> (<kbd>Cmd</kbd>+<kbd>S</kbd> en Mac).
8. Crea la build del proyecto haciendo click en `Project` -> `Build` o con el atajo <kbd>Ctrl</kbd>+<kbd>B</kbd> (<kbd>Cmd</kbd>+<kbd>B</kbd> en Mac).
![Hello World Step 5](../manuals/images/unity/helloworld_5.png)

Acabas de crear la build de tu primer proyecto en Defold y deberías ver tu texto en la ventana. Los conceptos de objeto de juego y componente deberían resultarte familiares. Las colecciones, Outline, Properties y por qué tuvimos que mover la label un poco hacia arriba a la derecha se explican más abajo.
