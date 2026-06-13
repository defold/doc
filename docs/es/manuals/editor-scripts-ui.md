---
title: "Scripts del editor: UI"
brief: Este manual explica cómo crear elementos de interfaz en el editor usando Lua
---

# Scripts del editor e interfaz

Este manual explica cómo crear elementos interactivos de interfaz en el editor usando scripts del editor escritos en Lua. Para empezar con los scripts del editor, consulta el [manual de scripts del editor](/manuals/editor-scripts). Puedes encontrar la referencia completa de la API del editor [aquí](/ref/stable/editor-lua/). Actualmente solo es posible crear diálogos interactivos, aunque queremos ampliar el soporte de scripting de interfaz al resto del editor en el futuro.

## Hola mundo

Toda la funcionalidad relacionada con la interfaz existe en el módulo `editor.ui`. Este es el ejemplo más simple de un script del editor con una interfaz personalizada para empezar:
```lua
local M = {}

function M.get_commands()
    return {
        {
            label = "Do with confirmation",
            locations = {"View"},
            run = function()
                local result = editor.ui.show_dialog(editor.ui.dialog({
                    title = "Perform action?",
                    buttons = {
                        editor.ui.dialog_button({
                            text = "Cancel",
                            cancel = true,
                            result = false
                        }),
                        editor.ui.dialog_button({
                            text = "Perform",
                            default = true,
                            result = true
                        })
                    }
                }))
                print('Perform action:', result)
            end
        }
    }
end

return M

```

Este fragmento de código define un comando **View → Do with confirmation**. Cuando lo ejecutes, verás el siguiente diálogo:

![Diálogo Hello world](images/editor_scripts/perform_action_dialog.png)

Finalmente, después de presionar <kbd>Enter</kbd> (o hacer click en el botón `Perform`), verás la siguiente línea en la consola del editor:
```
Perform action:	true
```

## Conceptos básicos

### Componentes

El editor proporciona varios **componentes** de interfaz que se pueden componer para crear la interfaz deseada. Por convención, todos los componentes se configuran usando una única tabla llamada **props**. Los componentes en sí no son tablas, sino **userdata inmutable** que usa el editor para crear la interfaz.

### Props

Las **props** son tablas que definen entradas para los componentes. Las props deben tratarse como inmutables: mutar la tabla de props en el lugar no hará que el componente se vuelva a renderizar, pero usar una tabla diferente sí. La interfaz se actualiza cuando la instancia del componente recibe una tabla de props que no es superficialmente igual a la anterior.

### Alineación

Cuando al componente se le asignan algunos límites en la interfaz, ocupará todo el espacio, aunque eso no significa que la parte visible del componente se estire. En su lugar, la parte visible tomará el espacio que necesita y luego se alineará dentro de los límites asignados. Por lo tanto, la mayoría de los componentes integrados definen una prop `alignment`.

Por ejemplo, considera este componente label:
```lua
editor.ui.label({
    text = "Hello",
    alignment = editor.ui.ALIGNMENT.RIGHT
})
```
La parte visible es el texto `Hello`, y está alineada dentro de los límites asignados al componente:

![Alineación](images/editor_scripts/alignment.png)

## Componentes integrados

El editor define varios componentes integrados que se pueden usar juntos para construir la interfaz. Los componentes se pueden agrupar de forma aproximada en 3 categorías: layout, presentación de datos e input.

### Componentes de layout

Los componentes de layout se usan para colocar otros componentes unos junto a otros. Los componentes principales de layout son **`horizontal`**, **`vertical`** y **`grid`**. Estos componentes también definen props como **padding** y **spacing**, donde padding es un espacio vacío desde el borde de los límites asignados hasta el contenido, y spacing es un espacio vacío entre los hijos:

![Padding y Spacing](images/editor_scripts/padding_and_spacing.png)

El editor define constantes de padding y spacing `small`, `medium` y `large`. En cuanto a spacing, `small` está pensado para el espacio entre distintos subelementos de un elemento individual de interfaz, `medium` para el espacio entre elementos individuales de interfaz, y `large` para el espacio entre grupos de elementos. El spacing predeterminado es `medium`. Un valor de padding de `large` significa padding desde los bordes de la ventana hasta el contenido, `medium` es padding desde los bordes de un elemento de interfaz significativo, y `small` es padding desde los bordes de elementos pequeños de interfaz como menús contextuales y tooltips (aún no implementados).

Un contenedor **`horizontal`** coloca sus hijos uno después de otro en horizontal, haciendo siempre que la altura de cada hijo llene el espacio disponible. De forma predeterminada, el ancho de cada hijo se mantiene al mínimo, aunque es posible hacer que tome tanto espacio como sea posible estableciendo la prop `grow` en `true` en un hijo.

Un contenedor **`vertical`** es similar al horizontal, pero con los ejes intercambiados.

Finalmente, **`grid`** es un componente contenedor que distribuye sus hijos en una cuadrícula 2D, como una tabla. La configuración `grow` en una cuadrícula se aplica a filas o columnas, por lo que no se establece en un hijo, sino en la tabla de configuración de una columna. Además, los hijos de una cuadrícula se pueden configurar para ocupar varias filas o columnas con las props `row_span` y `column_span`. Las cuadrículas son útiles para crear formularios con varios inputs:
```lua
editor.ui.grid({
    padding = editor.ui.PADDING.LARGE, -- agrega padding alrededor de los bordes del diálogo
    columns = {{}, {grow = true}}, -- hace crecer la 2.ª columna
    children = {
        {
            editor.ui.label({
                text = "Level Name",
                alignment = editor.ui.ALIGNMENT.RIGHT
            }),
            editor.ui.string_field({})
        },
        {
            editor.ui.label({
                text = "Author",
                alignment = editor.ui.ALIGNMENT.RIGHT
            }),
            editor.ui.string_field({})
        }
    }
})
```
El código anterior producirá el siguiente formulario de diálogo:

![Diálogo New Level](images/editor_scripts/new_level_dialog.png)

### Componentes de presentación de datos

El editor define 4 componentes de presentación de datos:
- **`label`**: etiqueta de texto, pensada para usarse con inputs de formularios.
- **`icon`**: un icono; actualmente solo se puede usar para presentar un conjunto pequeño de iconos predefinidos, pero queremos permitir más iconos en el futuro.
- **`heading`**: elemento de texto pensado para presentar una línea de texto de encabezado en, por ejemplo, un formulario o un diálogo. El enum `editor.ui.HEADING_STYLE` define varios estilos de encabezado que incluyen los encabezados `H1`-`H6` de HTML, así como `DIALOG` y `FORM`, específicos del editor.
- **`paragraph`**: elemento de texto pensado para presentar un párrafo de texto. La principal diferencia con `label` es que paragraph soporta ajuste de línea: si los límites asignados son demasiado pequeños horizontalmente, el texto se ajustará y posiblemente se acortará con `"..."` si no cabe en la vista.

### Componentes de input

Los componentes de input están hechos para que el usuario interactúe con la interfaz. Todos los componentes de input soportan la prop `enabled` para controlar si la interacción está habilitada o no, y definen varias props de callback que notifican al script del editor cuando hay interacción.

Si creas una interfaz estática, basta con definir callbacks que simplemente modifiquen variables locales. Para interfaces dinámicas e interacciones más avanzadas, consulta [reactividad](#reactivity).

Por ejemplo, es posible crear un diálogo estático sencillo de New File así:
```lua
-- nombre de archivo inicial, será reemplazado por el diálogo
local file_name = ""
local create_file = editor.ui.show_dialog(editor.ui.dialog({
    title = "Create New File",
    content = editor.ui.horizontal({
        padding = editor.ui.PADDING.LARGE,
        spacing = editor.ui.SPACING.MEDIUM,
        children = {
            editor.ui.label({
                text = "New File Name",
                alignment = editor.ui.ALIGNMENT.CENTER
            }),
            editor.ui.string_field({
                grow = true,
                text = file_name,
                -- callback al escribir:
                on_value_changed = function(new_text)
                    file_name = new_text
                end
            })
        }
    }),
    buttons = {
        editor.ui.dialog_button({ text = "Cancel", cancel = true, result = false }),
        editor.ui.dialog_button({ text = "Create File", default = true, result = true })
    }
}))
if create_file then
    print("create", file_name)
end
```
Aquí tienes una lista de componentes de input integrados:
- **`string_field`**, **`integer_field`** y **`number_field`** son variaciones de un campo de texto de una sola línea que permiten editar strings, enteros y números.
- **`select_box`** se usa para seleccionar una opción de un array predefinido de opciones con un control desplegable.
- **`check_box`** es un campo de input booleano con callback `on_value_changed`.
- **`button`** con callback `on_press`, que se invoca al presionar el botón.
- **`external_file_field`** es un componente pensado para seleccionar una ruta de archivo en la computadora. Consiste en un campo de texto y un botón que abre un diálogo de selección de archivo.
- **`resource_field`** es un componente pensado para seleccionar un recurso en el proyecto.

Todos los componentes excepto los botones permiten establecer una prop `issue` que muestra el problema relacionado con el componente (ya sea `editor.ui.ISSUE_SEVERITY.ERROR` o `editor.ui.ISSUE_SEVERITY.WARNING`), por ejemplo:
```lua
issue = {severity = editor.ui.ISSUE_SEVERITY.WARNING, message = "This value is deprecated"}
```
Cuando se especifica issue, cambia el aspecto del componente de input y agrega un tooltip con el mensaje del problema.

Aquí tienes una demo de todos los inputs con sus variantes de issue:

![Inputs](images/editor_scripts/inputs_demo.png)

### Componentes relacionados con diálogos

Para mostrar un diálogo, necesitas usar la función `editor.ui.show_dialog`. Espera un componente **`dialog`** que define la estructura principal de los diálogos de Defold: `title`, `header`, `content` y `buttons`. El componente dialog es un poco especial: no puedes usarlo como hijo de otro componente, porque representa una ventana, no un elemento de interfaz. Sin embargo, `header` y `content` sí son componentes normales.

Los botones de diálogo también son especiales: se crean usando el componente **`dialog_button`**. A diferencia de los botones normales, los botones de diálogo no tienen callback `on_pressed`. En su lugar, definen una prop `result` con un valor que devolverá la función `editor.ui.show_dialog` cuando se cierre el diálogo. Los botones de diálogo también definen las props booleanas `cancel` y `default`: el botón con una prop `cancel` se activa cuando el usuario presiona <kbd>Escape</kbd> o cierra el diálogo con el botón de cerrar del sistema operativo, y el botón `default` se activa cuando el usuario presiona <kbd>Enter</kbd>. Un botón de diálogo puede tener las props `cancel` y `default` establecidas en `true` al mismo tiempo.

### Componentes de utilidad

Además, el editor define algunos componentes de utilidad:
- **`separator`** es una línea fina usada para delimitar bloques de contenido.
- **`scroll`** es un componente envoltorio que muestra barras de desplazamiento cuando el componente envuelto no cabe en el espacio asignado.

## Reactividad {#reactivity}

Como los componentes son **userdata inmutable**, es imposible cambiarlos después de crearlos. Entonces, ¿cómo hacer que la interfaz cambie con el tiempo? La respuesta: **componentes reactivos**.

::: sidenote
La interfaz de scripting del editor se inspira en la biblioteca [React](https://react.dev/), así que saber sobre interfaces reactivas y hooks de React te ayudará.
:::

En los términos más simples, un componente reactivo es un componente con una función Lua que recibe datos (props) y devuelve una vista (otro componente). La función del componente reactivo puede usar **hooks**: funciones especiales en el módulo `editor.ui` que agregan funcionalidades reactivas a tus componentes. Por convención, todos los hooks tienen un nombre que empieza con `use_`.

Para crear un componente reactivo, usa la función `editor.ui.component()`.

Veamos este ejemplo: un diálogo New File que solo permite crear un archivo si el nombre de archivo introducido no está vacío:

```lua
-- 1. dialog es un componente reactivo
local dialog = editor.ui.component(function(props)
    -- 2. el componente define un estado local (nombre de archivo) que por defecto es un string vacío
    local name, set_name = editor.ui.use_state("")

    return editor.ui.dialog({
        title = props.title,
        content = editor.ui.vertical({
            padding = editor.ui.PADDING.LARGE,
            children = {
                editor.ui.string_field({
                    value = name,
                    -- 3. escribir + Enter actualiza el estado local
                    on_value_changed = set_name
                })
            }
        }),
        buttons = {
            editor.ui.dialog_button({
                text = "Cancel",
                cancel = true
            }),
            editor.ui.dialog_button({
                text = "Create File",
                -- 4. la creación se habilita cuando existe el nombre
                enabled = name ~= "",
                default = true,
                -- 5. el resultado es el nombre
                result = name
            })
        }
    })
end)

-- 6. show_dialog devolverá un nombre de archivo no vacío o nil al cancelar
local file_name = editor.ui.show_dialog(dialog({ title = "New File Name" }))
if file_name then
    print("create " .. file_name)
else
    print("cancelled")
end
```

Cuando ejecutes un comando de menú que corra este código, el editor mostrará un diálogo con el botón de diálogo `"Create File"` deshabilitado al inicio, pero cuando escribas un nombre y presiones <kbd>Enter</kbd>, se habilitará:

![Diálogo New File](images/editor_scripts/reactive_new_file_dialog.png)

Entonces, ¿cómo funciona? En el primer renderizado, el hook `use_state` crea un estado local asociado con el componente y lo devuelve con un setter para el estado. Cuando se invoca la función setter, programa un nuevo renderizado del componente. En renderizados posteriores, la función del componente se invoca de nuevo, y `use_state` devuelve el estado actualizado. Luego, el nuevo componente de vista devuelto por la función del componente se compara con el anterior, y la interfaz se actualiza donde se detectaron cambios.

Este enfoque reactivo simplifica mucho la construcción de interfaces interactivas y mantenerlas sincronizadas: en vez de actualizar explícitamente todos los componentes de interfaz afectados por el input del usuario, la vista se define como una función pura del input (props y estado local), y el editor se encarga de todas las actualizaciones.

### Reglas de reactividad

El editor espera que las funciones de componente reactivas se comporten correctamente para poder funcionar:

1. Las funciones de componente deben ser puras. No hay garantía de cuándo ni con qué frecuencia se invocará la función del componente. Todos los efectos secundarios deben estar fuera del renderizado, por ejemplo, en callbacks.
2. Las props y el estado local deben ser inmutables. No mutes las props. Si tu estado local es una tabla, no la mutes en el lugar; crea una nueva y pásala al setter cuando el estado necesite cambiar.
3. Las funciones de componente deben llamar los mismos hooks en el mismo orden en cada invocación. No llames hooks dentro de loops, en bloques condicionales, después de retornos tempranos, etc. Es una buena práctica llamar los hooks al inicio de la función del componente, antes de cualquier otro código.
4. Llama hooks solo desde funciones de componente. Los hooks funcionan en el contexto de un componente reactivo, así que solo se permite llamarlos en la función del componente (o en otra función llamada directamente por la función del componente).

### Hooks

::: sidenote
Si conoces [React](https://react.dev/), notarás que los hooks en el editor tienen una semántica ligeramente distinta en lo relativo a las dependencias de hooks.
:::

El editor define 2 hooks: **`use_memo`** y **`use_state`**.

### **`use_state`**

El estado local se puede crear de 2 formas: con un valor predeterminado o con una función inicializadora:
```lua
-- valor predeterminado
local enabled, set_enabled = editor.ui.use_state(true)
-- función inicializadora + argumentos
local id, set_id = editor.ui.use_state(string.lower, props.name)
```
De forma similar, el setter se puede invocar con un valor nuevo o con una función actualizadora:
```lua
-- función actualizadora
local function increment_by(n, by)
    return n + by
end

local counter = editor.ui.component(function(props)
    local count, set_count = editor.ui.use_state(0)

    return editor.ui.horizontal({
        spacing = editor.ui.SPACING.SMALL,
        children = {
            editor.ui.label({
                text = tostring(count),
                alignment = editor.ui.ALIGNMENT.LEFT,
                grow = true
            }),
            editor.ui.text_button({
                text = "+1",
                on_pressed = function() set_count(increment_by, 1) end
            }),
            editor.ui.text_button({
                text = "+5",
                on_pressed = function() set_count(increment_by, 5) end
            })
        }
    })
end)
```

Finalmente, el estado puede **restablecerse**. El estado se restablece cuando cambia cualquiera de los argumentos de `editor.ui.use_state()`, comprobado con `==`. Debido a esto, no debes usar tablas literales ni funciones inicializadoras literales como argumentos para el hook `use_state`: esto hará que el estado se restablezca en cada nuevo renderizado. Para ilustrarlo:
```lua
-- ❌ MAL: un inicializador de tabla literal causa un restablecimiento de estado en cada nuevo renderizado
local user, set_user = editor.ui.use_state({ first_name = props.first_name, last_name = props.last_name})

-- ✅ BIEN: usa una función inicializadora fuera de la función del componente para crear el estado de tabla
local function create_user(first_name, last_name)
    return { first_name = first_name, last_name = last_name}
end
-- ...más tarde, en la función del componente:
local user, set_user = editor.ui.use_state(create_user, props.first_name, props.last_name)


-- ❌ MAL: una función inicializadora literal causa un restablecimiento de estado en cada nuevo renderizado
local id, set_id = editor.ui.use_state(function() return string.lower(props.name) end)

-- ✅ BIEN: usa una función inicializadora referenciada para crear el estado
local id, set_id = editor.ui.use_state(string.lower, props.name)
```

### **`use_memo`**

Puedes usar el hook `use_memo` para mejorar el rendimiento. Es común realizar algunos cálculos en las funciones de renderizado, por ejemplo, para comprobar si el input del usuario es válido. El hook `use_memo` se puede usar en casos donde comprobar si los argumentos de la función de cálculo han cambiado es más barato que invocar la función de cálculo. El hook llamará a la función de cálculo en el primer renderizado, y reutilizará el valor calculado en renderizados posteriores si todos los argumentos de `use_memo` no han cambiado:
```lua
-- función de validación fuera de la función del componente
local function validate_password(password)
    if #password < 8 then
        return false, "Password must be at least 8 characters long."
    elseif not password:match("%l") then
        return false, "Password must include at least one lowercase letter."
    elseif not password:match("%u") then
        return false, "Password must include at least one uppercase letter."
    elseif not password:match("%d") then
        return false, "Password must include at least one number."
    else
        return true, "Password is valid."
    end
end

-- ...más tarde, en la función del componente
local username, set_username = editor.ui.use_state('')
local password, set_password = editor.ui.use_state('')
local valid, message = editor.ui.use_memo(validate_password, password)
```
En este ejemplo, la validación de la contraseña se ejecutará en cada cambio de contraseña (por ejemplo, al escribir en un campo de contraseña), pero no cuando cambie el nombre de usuario.

Otro caso de uso de `use_memo` es crear callbacks que luego se usan en componentes de input, o cuando una función creada localmente se usa como valor de prop para otro componente: esto evita nuevos renderizados innecesarios.
