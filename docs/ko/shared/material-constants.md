기본 {{ include.component }} 메터리얼에는 [go.set()](/ref/stable/go/#go.set) 또는 [go.animate()](/ref/stable/go/#go.animate)로 변경할 수 있는 다음 상수가 있습니다([자세한 내용은 메터리얼 매뉴얼](/manuals/material/#vertex-and-fragment-constants)을 참조하세요). 예:
```lua
go.set("#{{ include.component }}", "{{ include.variable }}", vmath.vector4(1,0,0,1))
go.animate("#{{ include.component }}", "{{ include.variable }}", go.PLAYBACK_LOOP_PINGPONG, vmath.vector4(1,0,0,1), go.EASING_LINEAR, 2)
```
