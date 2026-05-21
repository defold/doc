
O material padrão {{ include.component }} tem as seguintes constantes, que podem ser alteradas usando [go.set()](/ref/stable/go/#go.set) ou [go.animate()](/ref/stable/go/#go.animate) (consulte o [manual de Material para mais detalhes](/manuals/material/#vertex-and-fragment-constants)). Exemplos:
```lua
go.set("#{{ include.component }}", "{{ include.variable }}", vmath.vector4(1,0,0,1))
go.animate("#{{ include.component }}", "{{ include.variable }}", go.PLAYBACK_LOOP_PINGPONG, vmath.vector4(1,0,0,1), go.EASING_LINEAR, 2)
```
