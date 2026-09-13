
Varsayılan {{ include.component }} materyalinde (material), [go.set()](/ref/stable/go/#go.set) veya [go.animate()](/ref/stable/go/#go.animate) kullanarak değiştirebileceğiniz aşağıdaki sabitler bulunur (daha fazla ayrıntı için [Materyal kılavuzuna](/manuals/material/#vertex-and-fragment-constants) bakın). Örnekler:
```lua
go.set("#{{ include.component }}", "{{ include.variable }}", vmath.vector4(1,0,0,1))
go.animate("#{{ include.component }}", "{{ include.variable }}", go.PLAYBACK_LOOP_PINGPONG, vmath.vector4(1,0,0,1), go.EASING_LINEAR, 2)
```
