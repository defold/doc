---
title: 충돌 모양
brief: 충돌 오브젝트 컴포넌트는 여러 기본 모양 또는 하나의 복잡한 모양을 사용할 수 있습니다.
---

# 충돌 모양

충돌 오브젝트 컴포넌트는 여러 기본 모양 또는 하나의 복잡한 모양을 사용할 수 있습니다.

### 기본 모양
기본 모양은 *box*, *sphere*, *capsule*입니다. 충돌 오브젝트를 <kbd>오른쪽 클릭</kbd>하고 <kbd>Add Shape</kbd>를 선택하여 기본 모양을 추가합니다:

![기본 모양 추가](images/physics/add_shape.png)

## Box 모양
box에는 위치, 회전, 크기(너비, 높이, 깊이)가 있습니다:

![Box 모양](images/physics/box.png)

## Sphere 모양
sphere에는 위치, 회전, 지름이 있습니다:

![Sphere 모양](images/physics/sphere.png)

## Capsule 모양
capsule에는 위치, 회전, 지름, 높이가 있습니다:

![Sphere 모양](images/physics/capsule.png)

::: important
Capsule 모양은 3D 물리를 사용할 때만 지원됩니다. 3D 물리는 *game.project* 파일의 Physics 섹션에서 설정합니다.
:::

### 복잡한 모양
복잡한 모양은 타일맵 컴포넌트 또는 convex hull 모양에서 만들 수 있습니다.

## 타일맵 충돌 모양
Defold에는 타일 맵에서 사용하는 타일 소스에 대한 물리 모형을 쉽게 생성할 수 있는 기능이 있습니다. [Tilesource 매뉴얼](/manuals/tilesource/#tile-source-collision-shapes)에서는 타일 소스에 충돌 그룹을 추가하고 타일을 충돌 그룹에 할당하는 방법을 설명합니다([예제](/examples/tilemap/collisions/)).

타일 맵에 충돌을 추가하려면:

1. 게임 오브젝트를 <kbd>오른쪽 클릭</kbd>하고 <kbd>Add Component File</kbd>을 선택하여 게임 오브젝트에 타일맵을 추가합니다. 타일 맵 파일을 선택합니다.
2. 게임 오브젝트를 <kbd>오른쪽 클릭</kbd>하고 <kbd>Add Component ▸ Collision Object</kbd>를 선택하여 게임 오브젝트에 충돌 오브젝트 컴포넌트를 추가합니다.
3. 컴포넌트에 모양을 추가하는 대신 *Collision Shape* 프로퍼티를 *tilemap* 파일로 설정합니다.
4. 평소처럼 충돌 오브젝트 컴포넌트의 *Properties*를 설정합니다.

![Tilesource 충돌](images/physics/collision_tilemap.png)

::: important
충돌 그룹이 타일 맵의 타일 소스에 정의되므로 여기서는 *Group* 프로퍼티가 **사용되지 않는다**는 점에 유의하세요.
:::

## Convex hull 모양
Defold에는 세 개 이상의 점으로 convex hull 모양을 만들 수 있는 기능이 있습니다.

1. 외부 에디터를 사용해 convex hull shape 파일(파일 확장자 `.convexshape`)을 생성합니다.
2. 텍스트 에디터 또는 외부 도구로 파일을 직접 편집합니다(아래 참조).
3. 충돌 오브젝트 컴포넌트에 모양을 추가하는 대신 *Collision Shape* 프로퍼티를 *convex shape* 파일로 설정합니다.

### 파일 포멧
convex hull 파일 포멧은 다른 모든 Defold 파일과 동일한 데이터 포멧, 즉 protobuf text format을 사용합니다. convex hull 모양은 hull의 점들을 정의합니다. 2D 물리에서는 점을 반시계 방향 순서로 제공해야 합니다. 3D 물리 모드에서는 추상적인 point cloud가 사용됩니다. 2D 예제:

```
shape_type: TYPE_HULL
data: 200.000
data: 100.000
data: 0.0
data: 400.000
data: 100.000
data: 0.0
data: 400.000
data: 300.000
data: 0.0
data: 200.000
data: 300.000
data: 0.0
```

위 예제는 사각형의 네 모서리를 정의합니다:

```
 200x300   400x300
    4---------3
    |         |
    |         |
    |         |
    |         |
    1---------2
 200x100   400x100
```

## 외부 도구

충돌 모양을 만드는 데 사용할 수 있는 다양한 외부 도구가 있습니다:

* CodeAndWeb의 [Physics Editor](https://www.codeandweb.com/physicseditor/tutorials/how-to-create-physics-shapes-for-defold)는 스프라이트와 이에 맞는 충돌 모양이 있는 게임 오브젝트를 만드는 데 사용할 수 있습니다.
* [Defold Polygon Editor](https://rossgrams.itch.io/defold-polygon-editor)는 convex hull 모양을 만드는 데 사용할 수 있습니다.
* [Physics Body Editor](https://selimanac.github.io/physics-body-editor/)는 convex hull 모양을 만드는 데 사용할 수 있습니다.


# 충돌 모양 스케일링
충돌 오브젝트와 그 모양은 게임 오브젝트의 스케일을 상속합니다. 이 동작을 비활성화하려면 *game.project*의 Physics 섹션에서 [Allow Dynamic Transforms](/manuals/project-settings/#allow-dynamic-transforms) 체크박스를 해제합니다. 균일 스케일링만 지원되며, 스케일이 균일하지 않으면 가장 작은 스케일 값이 사용된다는 점에 유의하세요.

# 충돌 모양 크기 변경
충돌 오브젝트의 모양은 런타임에 `physics.set_shape()`를 사용해 크기를 변경할 수 있습니다. 예:

```lua
-- capsule shape 데이터 설정
local capsule_data = {
  type = physics.SHAPE_TYPE_CAPSULE,
  diameter = 10,
  height = 20,
}
physics.set_shape("#collisionobject", "my_capsule_shape", capsule_data)

-- sphere shape 데이터 설정
local sphere_data = {
  type = physics.SHAPE_TYPE_SPHERE,
  diameter = 10,
}
physics.set_shape("#collisionobject", "my_sphere_shape", sphere_data)

-- box shape 데이터 설정
local box_data = {
  type = physics.SHAPE_TYPE_BOX,
  dimensions = vmath.vector3(10, 10, 5),
}
physics.set_shape("#collisionobject", "my_box_shape", box_data)
```

::: sidenote
지정된 id를 가진 올바른 타입의 모양이 충돌 오브젝트에 이미 있어야 합니다.
:::

# 충돌 모양 회전

## 3D 물리에서 충돌 모양 회전
3D 물리의 충돌 모양은 모든 축을 중심으로 회전할 수 있습니다.


## 2D 물리에서 충돌 모양 회전
2D 물리의 충돌 모양은 z축을 중심으로만 회전할 수 있습니다. x축 또는 y축을 중심으로 회전하면 잘못된 결과가 발생하므로 피해야 합니다. 이는 모양을 x축 또는 y축을 따라 사실상 뒤집기 위해 180도 회전하는 경우에도 마찬가지입니다. 물리 모형을 뒤집으려면 [`physics.set_hlip(url, flip)`](/ref/stable/physics/?#physics.set_hflip:url-flip) 및 [`physics.set_vlip(url, flip)`](/ref/stable/physics/?#physics.set_vflip:url-flip)을 사용하는 것이 권장됩니다.


# 디버깅
런타임에 충돌 모양을 보려면 [물리 디버깅을 활성화](/manuals/debugging-game-logic/#debugging-problems-with-physics)할 수 있습니다.
