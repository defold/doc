---
title: Defold GUI 파이 노드
brief: 이 매뉴얼은 Defold GUI 씬에서 파이 노드를 사용하는 방법을 설명합니다.
---

# GUI 파이 노드

파이 노드는 단순한 원부터 파이 모양, 사각 도넛 모양까지 원형 또는 타원형 오브젝트를 만드는 데 사용됩니다.

## 파이 노드 만들기

*Outline*의 *Nodes* 섹션을 <kbd>Right click</kbd>하고 <kbd>Add ▸ Pie</kbd>를 선택합니다. 새 파이 노드가 선택되며 해당 속성을 수정할 수 있습니다.

![Create pie node](images/gui-pie/create.png)

다음 속성은 파이 노드에만 있습니다:

Inner Radius
: X축을 따라 표현되는 노드의 내부 반지름입니다.

Outer Bounds
: 노드의 외부 경계 모양입니다.

  - `Ellipse`는 노드를 외부 반지름까지 확장합니다.
  - `Rectangle`은 노드를 노드의 바운딩 박스까지 확장합니다.

Perimeter Vertices
: 모양을 만드는 데 사용할 세그먼트 수입니다. 노드의 360도 둘레를 완전히 둘러싸는 데 필요한 정점 수로 표현됩니다.

Pie Fill Angle
: 파이가 얼마나 채워져야 하는지입니다. 오른쪽에서 시작하는 반시계 방향 각도로 표현됩니다.

![Properties](images/gui-pie/properties.png)

노드에 텍스처를 설정하면 텍스처 이미지가 평평하게 적용되며, 텍스처의 모서리는 노드 바운딩 박스의 모서리와 대응됩니다.

## 런타임에 파이 노드 수정하기

파이 노드는 크기, 피벗, 색상 등을 설정하는 모든 일반 노드 조작 함수에 응답합니다. 파이 노드 전용 함수와 속성도 몇 가지 있습니다:

```lua
local pienode = gui.get_node("my_pie_node")

-- get the outer bounds
local fill_angle = gui.get_fill_angle(pienode)

-- increase perimeter vertices
local vertices = gui.get_perimeter_vertices(pienode)
gui.set_perimeter_vertices(pienode, vertices + 1)

-- change outer bounds
gui.set_outer_bounds(pienode, gui.PIEBOUNDS_RECTANGLE)

-- animate the inner radius
gui.animate(pienode, "inner_radius", 100, gui.EASING_INOUTSINE, 2, 0, nil, gui.PLAYBACK_LOOP_PINGPONG)
```
