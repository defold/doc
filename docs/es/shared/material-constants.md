
El material predeterminado de {{ include.component }} tiene las siguientes constantes que se pueden cambiar con [go.set()](/ref/stable/go/#go.set) o [go.animate()](/ref/stable/go/#go.animate) (consulta el [manual de Material para más detalles](/manuals/material/#vertex-and-fragment-constants)). Ejemplos:
```lua
go.set("#{{ include.component }}", "{{ include.variable }}", vmath.vector4(1,0,0,1))
go.animate("#{{ include.component }}", "{{ include.variable }}", go.PLAYBACK_LOOP_PINGPONG, vmath.vector4(1,0,0,1), go.EASING_LINEAR, 2)
```
