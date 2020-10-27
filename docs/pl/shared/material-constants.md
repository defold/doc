
Domyślny materiał komponentu typu {{ include.component }} posiada stałe, które można zmienić za pomocą funckji [go.set()](/ref/stable/go/#go.set) lub [go.animate()](/ref/stable/go/#go.animate) (więcej szczegółów znajdziesz w [instrukcji do materiałów](/manuals/material/#vertex-and-fragment-constants)). Przykłady:
```lua
go.set("#{{ include.component }}", "{{ include.variable }}", vmath.vector4(1,0,0,1))
go.animate("#{{ include.component }}", "{{ include.variable }}", go.PLAYBACK_LOOP_PINGPONG, vmath.vector4(1,0,0,1), go.EASING_LINEAR, 2)
```
