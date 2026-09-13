
Das Standardmaterial für {{ include.component }} hat die folgenden Konstanten, die du mit [go.set()](/ref/stable/go/#go.set) oder [go.animate()](/ref/stable/go/#go.animate) ändern kannst (weitere Details findest du im [Handbuch zu Materialien](/manuals/material/#vertex-and-fragment-constants)). Beispiele:
```lua
go.set("#{{ include.component }}", "{{ include.variable }}", vmath.vector4(1,0,0,1))
go.animate("#{{ include.component }}", "{{ include.variable }}", go.PLAYBACK_LOOP_PINGPONG, vmath.vector4(1,0,0,1), go.EASING_LINEAR, 2)
```
