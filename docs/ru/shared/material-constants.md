
The default {{ include.component }} material has the following constants that can be changed using [go.set()](/ref/stable/go/#go.set) or [go.animate()](/ref/stable/go/#go.animate) (refer to the [Material manual for more details](/manuals/material/#vertex-and-fragment-constants)). Examples:
```lua
go.set("#{{ include.component }}", "{{ include.variable }}", vmath.vector4(1,0,0,1))
go.animate("#{{ include.component }}", "{{ include.variable }}", go.PLAYBACK_LOOP_PINGPONG, vmath.vector4(1,0,0,1), go.EASING_LINEAR, 2)
```
