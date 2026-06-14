---
title: Defold GUI 파이 노드
brief: 이 매뉴얼은 Defold GUI 씬에서 파이 노드를 사용하는 방법을 설명합니다.
---

# GUI 파이 노드

파이 노드는 단순한 원부터 파이 모양과 사각 도넛 모양까지, 원형이나 타원형 오브젝트를 만드는 데 사용됩니다.

## 파이 노드 만들기

*Outline*의 *Nodes* 섹션에서 <kbd>마우스 오른쪽 버튼</kbd>을 누르고 <kbd>Add ▸ Pie</kbd>를 선택합니다. 새 파이 노드가 선택되며 해당 프로퍼티를 수정할 수 있습니다.

![파이 노드 만들기](images/gui-pie/create.png)

다음 프로퍼티는 파이 노드에만 있습니다:

Inner Radius
: X축을 기준으로 표현되는 노드의 내부 반지름입니다.

Outer Bounds
: 노드의 외부 경계 모양입니다.

  - `Ellipse`는 노드를 외부 반지름까지 확장합니다.
  - `Rectangle`은 노드를 노드의 바운딩 박스까지 확장합니다.

Perimeter Vertices
: 모양을 만드는 데 사용할 세그먼트 수입니다. 노드의 360도 둘레를 완전히 감싸는 데 필요한 정점 수로 표현됩니다.

Pie Fill Angle
: 파이에서 채워질 양입니다. 오른쪽에서 시작해 반시계 방향으로 잰 각도로 표현됩니다.

![Properties](images/gui-pie/properties.png)

노드에 텍스쳐를 설정하면 텍스쳐 이미지가 평면으로 적용되며, 텍스쳐의 모서리는 노드 바운딩 박스의 모서리와 대응됩니다.

## 런타임에 파이 노드 수정하기

파이 노드는 크기, 피벗, 색상 등을 설정하는 모든 일반 노드 조작 함수로 다룰 수 있습니다. 파이 노드 전용 함수와 프로퍼티도 몇 가지 있습니다:

```lua
local pienode = gui.get_node("my_pie_node")

-- 외부 경계 가져오기
local fill_angle = gui.get_fill_angle(pienode)

-- 둘레 정점 수 늘리기
local vertices = gui.get_perimeter_vertices(pienode)
gui.set_perimeter_vertices(pienode, vertices + 1)

-- 외부 경계 변경하기
gui.set_outer_bounds(pienode, gui.PIEBOUNDS_RECTANGLE)

-- 내부 반지름 애니메이션하기
gui.animate(pienode, "inner_radius", 100, gui.EASING_INOUTSINE, 2, 0, nil, gui.PLAYBACK_LOOP_PINGPONG)
```
