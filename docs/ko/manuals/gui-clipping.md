---
title: Defold manual
---

# Clipping
텍스쳐나 텍스트를 사용한 GUI 노드는 그래픽을 GUI에 추가하지만 때로는 화면의 그래픽 일부분을 제거하거나 특정 부분을 보여주는 마스크 기능이 필요한 경우가 있습니다. 이 메뉴얼은 이를 구현하는 방법을 설명합니다.

예를 들어, 게임에서 플레이어가 자신의 방향을 잡기 위한 미니맵이 있는 HUD 요소를 화면에 생성해야 한다고 칩시다.

![Minimap HUD](images/clipping/clipping_minimap.png)

클리핑(clipping)과 함께 파이 노드(pie node)를 사용하면 미니맵을 매우 쉽게 만들 수 있습니다.

![Making the minimap](images/clipping/clipping_making_minimap.png)

1. pie 노드 추가. 맵을 위한 "열쇠구멍" 역할을 하게됨
2. box 노드를 추가하고 맵 텍스쳐를 반영함
3. box 노드를 pie노드의 자식노드로 지정함
4. pie 노드의 **Clipping** 프로퍼티를 "Stencil"로 설정함

![Clipping preview](images/clipping/clipping_preview.png)

이제 부모 노드는 자식 노드에 대한 "열쇠구멍" 역할을 하게 되어 부모 클리핑 노드에 의해 바인딩 된 그래픽만 표시되므로 부모 노드는 맵의 그래픽 외부 영역을 정의하게 됩니다. 따라서 맵 노드를 자유롭게 움직여도 부모 영역 내에 있는 부분이 표시되게 됩니다.

클리핑은 box노드와 pie 노드에 반영할 수 있으며 Text 노드는 다른 노드와 클리핑 할 수 없습니다. 클리핑에는 두 가지 타입이 있는데 클리퍼의 모양을 그리는 **Visible clipper**와 클리핑 마스크에 미치는 영향을 반전시키는 **Inverted clipper**가 있습니다. (자세한 내용은 아래 참고)

![Clipping properties](images/clipping/clipping_properties.png)

Stencil 클리핑은 box 노드와 pie 노드에 반영할 수 있는데, Stencil에는 몇 가지 제한사항이 있습니다.

1. stencil clippers의 총 수는 256개를 초과할 수 없음
2. stencil 자식 노드의 최대 중첩 깊이(nesting depth)는 8단계임(stencil 클리핑 카운트를 사용한 노드만)
3. stencil 형제 노드의 최대 수는 127개임. stencil 계층구조 아래의 각 레벨의 최대 제한은 절반으로 줄어듬
4. Inverted 노드는 비용이 많이 듬. 8개의 inverted clipping 노드가 한계이고 non-inverted clipping 노드의 최대치의 절반이 됨
5. Stencils은 텍스쳐가 아닌 노드의 지오메트리로부터 stencil 마스크를 렌더링함. **Inverted clipper** 프로퍼티를 설정해서 마스크를 반전 시킬 수 있음

## Stencil mask
스텐실 클리핑이 어떻게 동작하는지 이해하기 위해, 스텐실의 계층이 어떻게 개별 클리핑의 모양을 그 계층구조 하에서 전체 마스크로 반영하는지 상상해 보는 것이 좋습니다. 클리핑 노드의 마스크 세트는 해당 노드의 자식들로 상속되며 자식 노드들은 절대 마스크를 확장하지 않고 오직 클리핑만 합니다. 구체적인 예제를 살펴 봅시다.

![Clipping hierarchy](images/clipping/clipping_hierarchy.png)

hexagon 과 square 모형 둘 다 스텐실 클리퍼를 설정합니다. **Inverted clipper** 프로퍼티를 설정하면 해당 노드로 상속된 마스크를 반전 시킵니다. 위의 계층구조에서 normal clippers와 inverted clippers를 사용하여 4가지의 조합이 가능합니다.

![Stencil masks](images/clipping/clipping_stencil_masks.png)

만약 인버트된 노드 아래에 또 **Inverted clipper**로 설정된 노드가 있다면, 자식 노드에 의해 마스크된 영역이 인버트됩니다. inverted clippers 노드를 각각 자식노드로 엮는 방법으로 노드에 여러개의 구멍을 낼 수도 있습니다.

![Two inverters cutting a node](images/clipping/clipping_two_inverters.png)

## Layers
레이어는 노드의 렌더링 순서(일괄 처리(batch))를 제어할 수 있습니다. 레이어와 클리핑 노드를 사용하면 일반적인 레이어 순서가 무시(override) 됩니다. 클리핑 순서는 레이어 순서보다 우선하게 되는데, 즉 노드가 속한 레이어에 관계 없이, 노드 계층에 따라 클리핑 됩니다. 레이어는 오직 그래픽의 그리기 순서에만 영향을 미치며, 더 나아가서 클리핑 노드에 설정된 레이어는 해당 클리퍼 계층의 그리기 순서에만 영향을 미칩니다.

예를 들어, 안쪽 그림자 텍스쳐(inner shadow texture)가 있는 "window_and_shadow" 라는 클리퍼 노드가 있다고 가정해 봅시다. 이 노드의 **Visible clipper** 프로퍼티를 체크하고 "layer2"로 설정해서 "layer0"의 "map" 노드와 클리핑을 연결합니다. 이 클리퍼 텍스쳐는 "map" 자식노드의 위에서 렌더링됩니다. "map"에 설정된 레이어 혹은 "window_and_shadow" 설정된 레이어는 "blue_box" ("layer2") 와 "orange_box" ("layer1") 에 관련된 렌더링 순서에 영향을 주지 않습니다. 만약 "blue_box" 와 "orange_box" 에 관련해서 "window_and_shadow" 의 렌더링 순서를 변경하려면, 노드 트리의 순서를 변경하면 됩니다.

![Layers and clipping](images/clipping/clipping_layers.png)
