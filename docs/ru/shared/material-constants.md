
Стандартный материал {{ include.component }} содержит следующие константы, которые можно изменять с помощью [go.set()](/ref/stable/go/#go.set) или [go.animate()](/ref/stable/go/#go.animate) (подробнее см. в [руководстве по материалам](/manuals/material/#vertex-and-fragment-constants)). Примеры:
```lua
go.set("#{{ include.component }}", "{{ include.variable }}", vmath.vector4(1,0,0,1))
go.animate("#{{ include.component }}", "{{ include.variable }}", go.PLAYBACK_LOOP_PINGPONG, vmath.vector4(1,0,0,1), go.EASING_LINEAR, 2)
```
