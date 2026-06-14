---
title: 게임 오브젝트 컴포넌트
brief: 이 매뉴얼은 컴포넌트 개요와 사용 방법을 설명합니다.
---

# 컴포넌트

:[components](../shared/components.md)

## 컴포넌트 타입

Defold는 다음 컴포넌트 타입을 지원합니다:

* [컬렉션 팩토리](/manuals/collection-factory) - 컬렉션을 스폰합니다
* [컬렉션 프록시](/manuals/collection-proxy) - 컬렉션을 로드하고 언로드합니다
* [충돌 오브젝트](/manuals/physics) - 2D 및 3D 물리
* [Camera](/manuals/camera) - 게임 월드의 뷰포트와 투영을 변경합니다
* [Factory](/manuals/factory) - 게임 오브젝트를 스폰합니다
* [GUI](/manuals/gui) - 그래픽 유저 인터페이스를 렌더링합니다
* [Label](/manuals/label) - 텍스트 조각을 렌더링합니다
* [Mesh](/manuals/mesh) 3D mesh를 표시합니다(런타임 생성 및 조작 포함)
* [Model](/manuals/model) 3D 모델을 표시합니다(선택적 애니메이션 포함)
* [Particle FX](/manuals/particlefx) - 파티클을 스폰합니다
* [Script](/manuals/script) - 게임 로직을 추가합니다
* [Sound](/manuals/sound) - 사운드나 음악을 재생합니다
* [Sprite](/manuals/sprite) - 2D 이미지를 표시합니다(선택적 플립북 애니메이션 포함)
* [Tilemap](/manuals/tilemap) - 타일 그리드를 표시합니다

익스텐션을 통해 추가 컴포넌트를 더할 수 있습니다:

* [Rive 모델](/extension-rive) - Rive 애니메이션을 렌더링합니다
* [Spine 모델](/extension-spine) - Spine 애니메이션을 렌더링합니다


## 컴포넌트 활성화 및 비활성화

게임 오브젝트의 컴포넌트는 게임 오브젝트가 생성될 때 활성화됩니다. 컴포넌트를 비활성화하려면 해당 컴포넌트로 [`disable`](/ref/go/#disable) 메세지를 보냅니다:

```lua
-- 이 스크립트와 같은 게임 오브젝트에 있는 id 'weapon' 컴포넌트를 비활성화합니다
msg.post("#weapon", "disable")

-- 'enemy' 게임 오브젝트에 있는 id 'shield' 컴포넌트를 비활성화합니다
msg.post("enemy#shield", "disable")

-- 현재 게임 오브젝트의 모든 컴포넌트를 비활성화합니다
msg.post(".", "disable")

-- 'enemy' 게임 오브젝트의 모든 컴포넌트를 비활성화합니다
msg.post("enemy", "disable")
```

컴포넌트를 다시 활성화하려면 해당 컴포넌트로 [`enable`](/ref/go/#enable) 메세지를 보낼 수 있습니다:

```lua
-- id 'weapon' 컴포넌트를 활성화합니다
msg.post("#weapon", "enable")
```

## 컴포넌트 프로퍼티

Defold의 모든 컴포넌트 타입은 서로 다른 프로퍼티를 가집니다. 에디터의 [Properties 창](/manuals/editor/#the-editor-views)은 [Outline 창](/manuals/editor/#the-editor-views)에서 현재 선택한 컴포넌트의 프로퍼티를 표시합니다. 사용할 수 있는 컴포넌트 프로퍼티에 대해 더 알아보려면 각 컴포넌트 타입의 매뉴얼을 참고하세요.

## 컴포넌트 위치, 회전 및 스케일

시각적 컴포넌트는 일반적으로 위치와 회전 프로퍼티를 가지며, 대부분 스케일 프로퍼티도 가집니다. 이러한 프로퍼티는 에디터에서 변경할 수 있지만, 거의 모든 경우 런타임에는 변경할 수 없습니다(런타임에 변경할 수 있는 유일한 예외는 스프라이트 및 라벨 컴포넌트의 스케일입니다).

런타임에 컴포넌트의 위치, 회전 또는 스케일을 변경해야 한다면, 대신 해당 컴포넌트가 속한 게임 오브젝트의 위치, 회전 또는 스케일을 수정합니다. 그러면 그 게임 오브젝트의 모든 컴포넌트가 영향을 받는 부작용이 있습니다. 게임 오브젝트에 연결된 여러 컴포넌트 중 하나만 조작하고 싶다면, 해당 컴포넌트를 별도의 게임 오브젝트로 옮기고 원래 컴포넌트가 속해 있던 게임 오브젝트의 자식 게임 오브젝트로 추가하는 것을 권장합니다.

## 컴포넌트 그리기 순서

시각적 컴포넌트의 그리기 순서는 두 가지에 따라 달라집니다:

### 렌더 스크립트 predicate
각 컴포넌트에는 [메터리얼](/manuals/material/)이 할당되고, 각 메터리얼은 하나 이상의 태그를 가집니다. 렌더 스크립트는 다시 여러 predicate를 정의하며, 각 predicate는 하나 이상의 메터리얼 태그와 매칭됩니다. 렌더 스크립트의 *update()* 함수에서 렌더 스크립트 [predicate가 하나씩 그려지고](/manuals/render/#render-predicates), 각 predicate에 정의된 태그와 매칭되는 컴포넌트가 그려집니다. 기본 렌더 스크립트는 먼저 스프라이트와 타일맵을 하나의 패스에서 그린 다음, 파티클 효과를 다른 패스에서 그리며, 둘 다 월드 공간에서 그립니다. 그런 다음 렌더 스크립트는 GUI 컴포넌트를 별도 패스에서 화면 공간에 그립니다.

### 컴포넌트 z 값
모든 게임 오브젝트와 컴포넌트는 `vector3` 오브젝트로 표현되는 위치를 사용해 3D 공간에 배치됩니다. 게임의 그래픽 컨텐츠를 2D로 볼 때 X와 Y 값은 오브젝트의 "너비"와 "높이" 축 위치를 결정하고, Z 위치는 "깊이" 축 위치를 결정합니다. Z 위치를 사용하면 겹치는 오브젝트의 가시성을 제어할 수 있습니다. Z 값이 1인 스프라이트는 Z 위치가 0인 스프라이트 앞에 나타납니다. 기본적으로 Defold는 -1에서 1 사이의 Z 값을 허용하는 좌표 시스템을 사용합니다:

![model](images/graphics/z-order.png)

[렌더 predicate](/manuals/render/#render-predicates)와 매칭되는 컴포넌트들은 함께 그려지며, 그려지는 순서는 컴포넌트의 최종 z 값에 따라 달라집니다. 컴포넌트의 최종 z 값은 컴포넌트 자체의 z 값, 컴포넌트가 속한 게임 오브젝트의 z 값, 그리고 모든 부모 게임 오브젝트의 z 값을 더한 값입니다.

::: sidenote
여러 GUI 컴포넌트가 그려지는 순서는 GUI 컴포넌트의 z 값으로 결정되지 **않습니다**. GUI 컴포넌트의 그리기 순서는 [gui.set_render_order()](/ref/gui/#gui.set_render_order:order) 함수로 제어합니다.
:::

예: 게임 오브젝트 A와 B가 있습니다. B는 A의 자식입니다. B에는 스프라이트 컴포넌트가 있습니다.

| 항목     | Z 값 |
|----------|------|
| A        | 2    |
| B        | 1    |
| B#sprite | 0.5  |

![](images/graphics/component-hierarchy.png)

위 계층구조에서 B의 스프라이트 컴포넌트의 최종 z 값은 2 + 1 + 0.5 = 3.5입니다.

::: important
두 컴포넌트의 z 값이 정확히 같으면 순서는 정의되지 않으며, 컴포넌트가 앞뒤로 깜빡이거나 한 플랫폼에서는 한 순서로 렌더링되고 다른 플랫폼에서는 다른 순서로 렌더링될 수 있습니다.

렌더 스크립트는 z 값에 대한 near 및 far plane을 정의합니다. 이 범위 밖에 있는 z 값을 가진 컴포넌트는 렌더링되지 않습니다. 기본 범위는 -1부터 1까지이지만 [쉽게 변경할 수 있습니다](/manuals/render/#default-view-projection). near 및 far 한계가 -1과 1일 때 Z 값의 수치 정밀도는 매우 높습니다. 3D 에셋으로 작업할 때는 커스텀 렌더 스크립트에서 기본 투영의 near 및 far 한계를 변경해야 할 수 있습니다. 자세한 내용은 [Render 매뉴얼](/manuals/render/)을 참고하세요.
:::


:[Component max count optimizations](../shared/component-max-count-optimizations.md)
