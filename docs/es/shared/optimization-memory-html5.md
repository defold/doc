## Tamaño del heap (HTML5)
El tamaño del heap de un juego HTML5 de Defold se puede configurar desde el [campo `heap_size`](/manuals/project-settings/#heap-size) en *game.project*. Asegúrate de optimizar el uso de memoria de tu juego y definir un tamaño de heap mínimo.

Para juegos pequeños, 32 MB es un tamaño de heap alcanzable. Para juegos más grandes, apunta a 64–128 MB. Si, por ejemplo, estás en 58 MB y no es viable optimizar más, puedes quedarte en 64 MB sin pensarlo demasiado. No hay un tamaño objetivo estricto: depende del juego. Simplemente apunta a tamaños más pequeños, idealmente en incrementos de potencias de dos.

Para comprobar el uso actual del heap, puedes iniciar tu juego y jugar el nivel o la sección con más carga de recursos, y monitorizar el uso de memoria:

```lua
if html5 then
    local mem = tonumber(html5.run("HEAP8.length") / 1024 / 1024)
    print(mem)
end
```

También puedes abrir las herramientas de desarrollador de tu navegador y escribir lo siguiente en la consola:

```js
HEAP8.length / 1024 / 1024
```

Si el uso de memoria se mantiene en 32 MB, ¡excelente! Si no, sigue los pasos para [optimizar el tamaño del motor en sí y de assets grandes como sonidos y texturas](/manuals/optimization-size).
