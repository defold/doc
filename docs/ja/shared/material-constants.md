
既定の {{ include.component }} マテリアル（material）には、[go.set()](/ref/stable/go/#go.set) または [go.animate()](/ref/stable/go/#go.animate) を使って変更できる以下の定数があります（詳しくは[マテリアルのマニュアル](/manuals/material/#vertex-and-fragment-constants)を参照してください）。例:
```lua
go.set("#{{ include.component }}", "{{ include.variable }}", vmath.vector4(1,0,0,1))
go.animate("#{{ include.component }}", "{{ include.variable }}", go.PLAYBACK_LOOP_PINGPONG, vmath.vector4(1,0,0,1), go.EASING_LINEAR, 2)
```
