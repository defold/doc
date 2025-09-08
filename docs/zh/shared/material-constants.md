
默认的 {{ include.component }} 材质具有以下常量，可以使用 [go.set()](/ref/stable/go/#go.set) 或 [go.animate()](/ref/stable/go/#go.animate) 进行更改（详情请参考[材质手册](/manuals/material/#vertex-and-fragment-constants)）。示例：
```lua
go.set("#{{ include.component }}", "{{ include.variable }}", vmath.vector4(1,0,0,1))
go.animate("#{{ include.component }}", "{{ include.variable }}", go.PLAYBACK_LOOP_PINGPONG, vmath.vector4(1,0,0,1), go.EASING_LINEAR, 2)
```
