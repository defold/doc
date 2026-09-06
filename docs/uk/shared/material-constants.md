
Стандартний матеріал компонента {{ include.component }} має такі константи, які можна змінювати за допомогою [go.set()](/ref/stable/go/#go.set) або [go.animate()](/ref/stable/go/#go.animate) (докладніше див. у [посібнику з матеріалів](/manuals/material/#vertex-and-fragment-constants)). Приклади:
```lua
go.set("#{{ include.component }}", "{{ include.variable }}", vmath.vector4(1,0,0,1))
go.animate("#{{ include.component }}", "{{ include.variable }}", go.PLAYBACK_LOOP_PINGPONG, vmath.vector4(1,0,0,1), go.EASING_LINEAR, 2)
```
