---
title: Defold 타일 맵 매뉴얼
brief: 이 매뉴얼은 Defold의 타일 맵 지원을 자세히 설명합니다.
---

# 타일 맵

*타일 맵(Tile Map)*은 *타일 소스(Tile Source)*의 타일을 큰 그리드 영역에 조합하거나 칠할 수 있게 해 주는 컴포넌트입니다. 타일 맵은 보통 게임 레벨 환경을 만드는 데 사용됩니다. 충돌 감지와 물리 시뮬레이션을 위해 타일 소스의 *Collision Shapes*를 맵에서 사용할 수도 있습니다([예제](/examples/tilemap/collisions/)).

타일 맵을 만들기 전에 먼저 타일 소스를 만들어야 합니다. 타일 소스를 만드는 방법은 [타일 소스 매뉴얼](/manuals/tilesource)을 참고하세요.

## 타일 맵 만들기

새 타일 맵을 만들려면:

- *Assets* 브라우저의 위치를 <kbd>오른쪽 클릭</kbd>한 다음 <kbd>New... ▸ Tile Map</kbd>을 선택합니다.
- 파일 이름을 지정합니다.
- 새 타일 맵이 타일 맵 에디터에서 자동으로 열립니다.

  ![새 타일맵](images/tilemap/tilemap.png)

- *Tile Source* 프로퍼티를 준비한 타일 소스 파일로 설정합니다.

타일 맵에 타일을 칠하려면:

1. *Outline* 뷰에서 칠할 *Layer*를 선택하거나 만듭니다.
2. 브러시로 사용할 타일을 선택하거나(<kbd>Space</kbd>를 눌러 타일 팔레트를 표시), 팔레트에서 클릭한 채 드래그해 여러 타일이 포함된 직사각형 브러시를 만듭니다.

   ![팔레트](images/tilemap/palette.png)

3. 선택한 브러시로 칠합니다. 타일을 지우려면 빈 타일을 선택해 브러시로 사용하거나 지우개(<kbd>Edit ▸ Select Eraser</kbd>)를 선택합니다.

   ![타일 칠하기](images/tilemap/paint_tiles.png)

레이어에서 타일을 직접 선택하고 선택 영역을 브러시로 사용할 수 있습니다. <kbd>Shift</kbd>를 누른 채 타일을 클릭하면 현재 브러시로 가져옵니다. <kbd>Shift</kbd>를 누른 상태에서 클릭한 채 드래그하면 타일 블록을 선택해 더 큰 브러시로 사용할 수도 있습니다. 또한 <kbd>Shift+Ctrl</kbd>을 누른 채 비슷한 방식으로 타일을 잘라내거나, <kbd>Shift+Alt</kbd>를 누른 채 타일을 지울 수 있습니다.

브러시를 시계 방향으로 회전하려면 <kbd>Z</kbd>를 사용합니다. 브러시를 가로로 반전하려면 <kbd>X</kbd>, 세로로 반전하려면 <kbd>Y</kbd>를 사용합니다.

![타일 가져오기](images/tilemap/pick_tiles.png)

## 게임에 타일 맵 추가하기

게임에 타일 맵을 추가하려면:

1. 타일 맵 컴포넌트를 담을 게임 오브젝트를 만듭니다. 게임 오브젝트는 파일 안에 있을 수도 있고 컬렉션에서 직접 만들 수도 있습니다.
2. 게임 오브젝트의 루트를 오른쪽 클릭하고 <kbd>Add Component File</kbd>을 선택합니다.
3. 타일 맵 파일을 선택합니다.

![타일 맵 사용](images/tilemap/use_tilemap.png)

## 런타임 조작

여러 함수와 프로퍼티를 통해 런타임에 타일맵을 조작할 수 있습니다([사용법은 API 문서 참고](/ref/tilemap/)).

### 스크립트에서 타일 변경하기

게임이 실행 중일 때 타일 맵의 내용을 동적으로 읽고 쓸 수 있습니다. 이렇게 하려면 [`tilemap.get_tile()`](/ref/tilemap/#tilemap.get_tile) 및 [`tilemap.set_tile()`](/ref/tilemap/#tilemap.set_tile) 함수를 사용합니다:

```lua
local tile = tilemap.get_tile("/level#map", "ground", x, y)

if tile == 2 then
    -- 잔디 타일(2)을 위험한 구멍 타일(번호 4)로 교체합니다.
    tilemap.set_tile("/level#map", "ground", x, y, 4)
end
```

## 타일맵 프로퍼티

*Id*, *Position*, *Rotation*, *Scale* 프로퍼티 외에도 다음과 같은 컴포넌트별 프로퍼티가 있습니다:

*Tile Source*
: 타일맵에 사용할 타일 소스 리소스입니다.

*Material*
: 타일맵 렌더링에 사용할 메터리얼입니다.

*Blend Mode*
: 타일맵을 렌더링할 때 사용할 블렌드 모드입니다.

### 블렌드 모드
:[blend-modes](../shared/blend-modes.md)

### 프로퍼티 변경하기

타일맵에는 `go.get()`과 `go.set()`으로 조작할 수 있는 여러 프로퍼티가 있습니다:

`tile_source`
: 타일 맵 타일 소스(`hash`)입니다. 타일 소스 리소스 프로퍼티와 `go.set()`을 사용해 변경할 수 있습니다. 예제는 [API 레퍼런스](/ref/tilemap/#tile_source)를 참고하세요.

`material`
: 타일 맵 메터리얼(`hash`)입니다. 메터리얼 리소스 프로퍼티와 `go.set()`을 사용해 변경할 수 있습니다. 예제는 [API 레퍼런스](/ref/tilemap/#material)를 참고하세요.

### 메터리얼 상수

{% include shared/material-constants.md component='tilemap' variable='tint' %}

`tint`
: 타일 맵의 색조(tint)입니다(`vector4`). `vector4`는 x, y, z, w가 각각 빨강, 초록, 파랑, 알파 색조에 대응하는 tint를 표현하는 데 사용됩니다.

## 프로젝트 설정

*game.project* 파일에는 타일맵과 관련된 몇 가지 [프로젝트 설정](/manuals/project-settings#tilemap)이 있습니다.

## 외부 도구

Defold 타일맵으로 직접 익스포트할 수 있는 외부 맵/레벨 에디터가 있습니다:

### Tiled

[Tiled](https://www.mapeditor.org/)는 직교, 아이소메트릭, 육각형 맵에 널리 사용되는 잘 알려진 맵 에디터입니다. Tiled는 다양한 기능을 지원하며 [Defold로 직접 익스포트](https://doc.mapeditor.org/en/stable/manual/export-defold/)할 수 있습니다. 타일맵 데이터와 추가 메타데이터를 익스포트하는 방법은 [Defold 사용자 "goeshard"의 이 블로그 글](https://goeshard.org/2025/01/01/using-tiled-object-layers-with-defold-tilemaps/)에서 더 알아볼 수 있습니다.


### Tilesetter

[Tilesetter](https://www.tilesetter.org/docs/exporting#defold)는 간단한 기본 타일에서 완전한 타일셋을 자동으로 생성하는 데 사용할 수 있으며, Defold로 직접 익스포트할 수 있는 맵 에디터도 포함합니다.
