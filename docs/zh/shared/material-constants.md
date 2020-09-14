
默认 {{ include.component }} 材质常量可以使用 [go.set()](/ref/stable/go/#go.set) 或 [go.animate()](/ref/stable/go/#go.animate) 来修改 (参考 [材质教程](/manuals/material/#vertex-and-fragment-constants)). 例如:
```lua
go.set("#{{ include.component }}", "{{ include.variable }}", vmath.vector4(1,0,0,1))
go.animate("#{{ include.component }}", "{{ include.variable }}", go.PLAYBACK_LOOP_PINGPONG, vmath.vector4(1,0,0,1), go.EASING_LINEAR, 2)
```
