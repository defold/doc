---
title: 3D-сетки в Defold
brief: Это руководство описывает методы создания 3D-сеток во время выполнения игры.
---

# Компонент Mesh

Defold по сути является 3D движком. Даже когда работа ведется только с 2D-материалом, весь рендеринг выполняется в 3D, но проецируется на экран ортографически. Defold позволяет полноценно использовать 3D-контент, добавляя и создавая 3D-сетки во время выполнения в коллекциях. Игры могут быть созданы исключительно в 3D с использованием только 3D-ассетов, или же 3D и 2D контент может совмещаться в соответствии с целями разработчика.

## Создание компонента Mesh

Компоненты сетки создаются так же, как и любой другой компонент игрового объекта. Это можно сделать двумя способами:

- Создайте *файл Mesh*, <kbd>кликнув ПКМ</kbd> в нужном расположении в браузере *Assets* и выберите <kbd>New... ▸ Mesh</kbd>.
- Создайте компонент, встроенный непосредственно в игровой объект, <kbd>кликнув ПКМ</kbd> по игровому объекту в представлении *Outline* и выберите <kbd>Add Component ▸ Mesh</kbd>.

![Mesh in game object](images/mesh/mesh.png)

После создания сетки необходимо определить ряд свойств.

### Свойства сетки

Помимо свойств *Id*, *Position* и *Rotation* существуют следующие специфичные для компонента свойства:

*Material*
: Материал, используемый для рендеринга сетки.

*Vertices*
: Файл буфера, описывающий данные сетки для каждого потока.

*Primitive Type*
: Lines, Triangles или Triangle Strip.

*Position Stream*
: This property should be the name of the *position* stream. The stream is automatically provided as input to the vertex shader.

*Normal Stream*
: This property should be the name of the *normal* stream. The stream is automatically provided as input to the vertex shader.

*tex0*
: Задает текстуру, используемую для сетки.

## Манипулирование в редакторе

После того, как компонент сетки размещен, можно свободно редактировать и манипулировать компонентом и/или объемлющим игровым объектом с помощью обычных инструментов *Scene Editor*, перемещая, вращая и масштабируя сетку по своему усмотрению.

## Манипулирование во время выполнения

Используя буферы сетками можно манипулировать во время выполнения.

## Константы материала

{% include shared/material-constants.md component='mesh' variable='tint' %}

`tint`
: Цветовой оттенок сетки (`vector4`). Для представления оттенка с компонентами x, y, z и w, соответствующими красному, зеленому, синему и альфа оттенкам, используется тип vector4.

## Локальное vs мировое пространство вершин
Если параметр Vertex Space материала сетки установлен в Local, данные будут предоставлены в шейдере как есть, и придется преобразовывать вершины/нормали, как принято, на GPU.

If the Vertex Space setting of the mesh material is set to World Space you have to either provide a default “position” and “normal”, stream, or you can select it from the dropdown, when editing the mesh. This is so that the engine can transform the data to world space for batching with other objects.

## Примеры
Обращайтесь к [forum announcement post](https://forum.defold.com/t/mesh-component-in-defold-1-2-169-beta/65137), чтобы узнать о том, как использовать компонент Mesh, включая примеры проектов и фрагменты кода.

Пример создания куба из треугольных полос (triangle strips):

```Lua

-- cube
local vertices = {
	0, 0, 0,
	0, 1, 0,
	1, 0, 0,
	1, 1, 0,
	1, 1, 1,
	0, 1, 0,
	0, 1, 1,
	0, 0, 1,
	1, 1, 1,
	1, 0, 1,
	1, 0, 0,
	0, 0, 1,
	0, 0, 0,
	0, 1, 0
}

-- create a buffer with a position stream
local buf = buffer.create(#vertices / 3, {
	{ name = hash("position"), type=buffer.VALUE_TYPE_FLOAT32, count = 3 }
})

-- get the position stream and write the vertices
local positions = buffer.get_stream(buf, "position")
for i, value in ipairs(vertices) do
	positions[i] = vertices[i]
end

-- set the buffer with the vertices on the mesh
local res = go.get("#mesh", "vertices")
resource.set_buffer(res, buf)
```
