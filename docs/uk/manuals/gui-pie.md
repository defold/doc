---
title: Вузли Pie у GUI Defold
brief: Цей посібник пояснює, як використовувати вузли Pie у сценах GUI Defold.
---

# Вузли Pie у GUI {#gui-pie-nodes}

Вузли Pie використовують для створення круглих або еліптичних об’єктів: від простих кругів до секторів і квадратних кільцеподібних фігур.

## Створення вузла Pie {#creating-a-pie-node}

<kbd>Клацніть правою кнопкою миші</kbd> розділ *Nodes* у вікні *Outline* та виберіть <kbd>Add ▸ Pie</kbd>. Новий вузол Pie буде вибрано, і ви зможете змінювати його властивості.

![Створення вузла Pie](images/gui-pie/create.png)

Наведені нижче властивості притаманні лише вузлам Pie:

Inner Radius
: Внутрішній радіус вузла, заданий уздовж осі X.

Outer Bounds
: Форма зовнішніх меж вузла.

  - `Ellipse` розширює вузол до зовнішнього радіуса.
  - `Rectangle` розширює вузол до його обмежувального прямокутника.

Perimeter Vertices
: Кількість сегментів, які використовуватимуться для побудови форми, задана як кількість вершин, потрібних для повного обходу периметра вузла на 360 градусів.

Pie Fill Angle
: Визначає, яку частину вузла Pie слід заповнити. Задається як кут проти годинникової стрілки, починаючи справа.

![Властивості](images/gui-pie/properties.png)

Якщо задати текстуру для вузла, її зображення накладається на площину так, що кути текстури відповідають кутам обмежувального прямокутника вузла.

## Змінення вузлів Pie під час виконання {#modify-pie-nodes-at-runtime}

Вузли Pie підтримують усі загальні функції роботи з вузлами для встановлення розміру, опорної точки, кольору тощо. Є кілька функцій і властивостей, доступних лише для вузлів Pie:

```lua
local pienode = gui.get_node("my_pie_node")

-- get the outer bounds
local fill_angle = gui.get_fill_angle(pienode)

-- increase perimeter vertices
local vertices = gui.get_perimeter_vertices(pienode)
gui.set_perimeter_vertices(pienode, vertices + 1)

-- change outer bounds
gui.set_outer_bounds(pienode, gui.PIEBOUNDS_RECTANGLE)

-- animate the inner radius
gui.animate(pienode, "inner_radius", 100, gui.EASING_INOUTSINE, 2, 0, nil, gui.PLAYBACK_LOOP_PINGPONG)
```
