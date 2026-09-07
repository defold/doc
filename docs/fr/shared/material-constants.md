
Le matériau {{ include.component }} par défaut possède les constantes suivantes, que vous pouvez modifier avec [go.set()](/ref/stable/go/#go.set) ou [go.animate()](/ref/stable/go/#go.animate) (consultez le [manuel des matériaux pour plus de détails](/manuals/material/#vertex-and-fragment-constants)). Exemples :
```lua
go.set("#{{ include.component }}", "{{ include.variable }}", vmath.vector4(1,0,0,1))
go.animate("#{{ include.component }}", "{{ include.variable }}", go.PLAYBACK_LOOP_PINGPONG, vmath.vector4(1,0,0,1), go.EASING_LINEAR, 2)
```
