
Il materiale predefinito del componente {{ include.component }} ha le seguenti costanti, che puoi modificare con [go.set()](/ref/stable/go/#go.set) o [go.animate()](/ref/stable/go/#go.animate) (consulta il [manuale sui materiali per maggiori dettagli](/manuals/material/#vertex-and-fragment-constants)). Esempi:
```lua
go.set("#{{ include.component }}", "{{ include.variable }}", vmath.vector4(1,0,0,1))
go.animate("#{{ include.component }}", "{{ include.variable }}", go.PLAYBACK_LOOP_PINGPONG, vmath.vector4(1,0,0,1), go.EASING_LINEAR, 2)
```
