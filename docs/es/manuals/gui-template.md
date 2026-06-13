---
title: Manual de plantillas GUI
brief: Este manual explica el sistema de plantillas GUI de Defold, que se usa para crear componentes GUI visuales reutilizables basados en plantillas compartidas o "prefabs".
---

# Nodos de plantilla GUI

Los nodos de plantilla GUI proporcionan un mecanismo potente para crear componentes GUI reutilizables basados en plantillas compartidas o "prefabs". Este manual explica la funcionalidad y cómo usarla.

Una plantilla GUI es una escena GUI que se instancia, nodo por nodo, en otra escena GUI. Después, cualquier valor de propiedad de los nodos de la plantilla original se puede sobrescribir.

## Crear una plantilla

Una plantilla GUI es una escena GUI común, así que se crea igual que cualquier otra escena GUI. Haz <kbd>click derecho</kbd> en una ubicación del panel *Assets* y selecciona <kbd>New... ▸ Gui</kbd>.

![Crear plantilla](images/gui-templates/create.png)

Crea la plantilla y guárdala. Ten en cuenta que los nodos de la instancia se colocarán relativos al origen, así que es buena idea crear la plantilla en la posición 0, 0, 0.

## Crear instancias desde una plantilla

Puedes crear cualquier cantidad de instancias basadas en la plantilla. Crea o abre la escena GUI donde quieres colocar la plantilla, luego haz <kbd>click derecho</kbd> en la sección *Nodes* de *Outline* y selecciona <kbd>Add ▸ Template</kbd>.

![Crear instancia](images/gui-templates/create_instance.png)

Define la propiedad *Template* con el archivo de escena GUI de la plantilla.

Puedes agregar cualquier cantidad de instancias de plantilla y, para cada instancia, puedes sobrescribir las propiedades de cada nodo y cambiar la posición, el color, el tamaño, la textura, etc. de los nodos de la instancia.

![Instancias](images/gui-templates/instances.png)

Cualquier propiedad que cambies se marca en azul en el editor. Presiona el botón de reinicio junto a la propiedad para definir su valor al valor de la plantilla:

![Propiedades](images/gui-templates/properties.png)

Todo nodo que tenga propiedades sobrescritas también se colorea de azul en *Outline*:

![Outline](images/gui-templates/outline.png)

La instancia de plantilla se muestra como una entrada plegable en la vista *Outline*. Sin embargo, es importante tener en cuenta que este elemento en el outline *no es un nodo*. La instancia de plantilla tampoco existe en runtime, pero todos los nodos que forman parte de la instancia sí existen.

Los nodos que forman parte de una instancia de plantilla reciben automáticamente un nombre con un prefijo y una barra (`"/"`) adjuntos a su *Id*. El prefijo es el *Id* definido en la instancia de plantilla.

## Modificar plantillas en runtime

Los scripts que manipulan o consultan nodos agregados mediante el mecanismo de plantillas solo necesitan tener en cuenta la nomenclatura de los nodos de instancia e incluir el *Id* de la instancia de plantilla como prefijo del nombre de nodo:

```lua
if gui.pick_node(gui.get_node("button_1/button"), x, y) then
    -- Hacer algo...
end
```

No hay ningún nodo correspondiente a la instancia de plantilla en sí. Si necesitas un nodo raíz para una instancia, agrégalo a la plantilla.

Si un script está asociado con una escena GUI de plantilla, el script no forma parte del árbol de nodos de la instancia. Puedes adjuntar un único script a cada escena GUI, así que la lógica de tu script debe estar en la escena GUI donde has instanciado tus plantillas.
