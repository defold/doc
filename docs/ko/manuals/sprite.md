---
title: 2D 이미지 표시하기
brief: 이 매뉴얼은 스프라이트 컴포넌트를 사용해 2D 이미지와 애니메이션을 표시하는 방법을 설명합니다.
---

# 스프라이트

스프라이트(Sprite) 컴포넌트는 화면에 표시되는 단순한 이미지 또는 플립북 애니메이션입니다.

![sprite](images/graphics/sprite.png)

스프라이트 컴포넌트는 그래픽에 [아틀라스](/manuals/atlas) 또는 [타일 소스](/manuals/tilesource)를 사용할 수 있습니다.

## 스프라이트 프로퍼티

*Id*, *Position*, *Rotation* 프로퍼티 외에도 다음과 같은 컴포넌트별 프로퍼티가 있습니다:

*Image*
: 쉐이더에 샘플러가 하나만 있으면 이 필드의 이름은 `Image`입니다. 그렇지 않으면 각 슬롯은 메터리얼의 텍스쳐 샘플러 이름을 따릅니다.
각 슬롯은 해당 텍스쳐 샘플러에서 스프라이트에 사용할 아틀라스 또는 타일 소스 리소스를 지정합니다.

*Default Animation*
: 스프라이트에 사용할 애니메이션입니다. 애니메이션 정보는 첫 번째 아틀라스 또는 타일 소스에서 가져옵니다.

*Material*
: 스프라이트 렌더링에 사용할 메터리얼입니다.

*Blend Mode*
: 스프라이트를 렌더링할 때 사용할 블렌드 모드입니다.

*Size Mode*
: `Automatic`으로 설정하면 에디터가 스프라이트의 크기를 설정합니다. `Manual`로 설정하면 직접 크기를 설정할 수 있습니다.

*Slice 9*
: 스프라이트 크기가 조정될 때 가장자리 주변 스프라이트 텍스쳐의 픽셀 크기를 유지하도록 설정합니다.

:[Slice-9](../shared/slice-9-texturing.md)

### 블렌드 모드
:[blend-modes](../shared/blend-modes.md)

## 런타임 조작

여러 함수와 프로퍼티를 통해 런타임에 스프라이트를 조작할 수 있습니다(사용법은 [API 문서](/ref/sprite/)를 참조하세요). 함수:

* `sprite.play_flipbook()` - 스프라이트 컴포넌트에서 애니메이션을 재생합니다.
* `sprite.set_hflip()` 및 `sprite.set_vflip()` - 스프라이트 애니메이션의 가로 및 세로 뒤집기를 설정합니다.

스프라이트에는 `go.get()`과 `go.set()`으로 조작할 수 있는 여러 프로퍼티도 있습니다:

`cursor`
: 정규화된 애니메이션 커서(`number`)입니다.

`image`
: 스프라이트 이미지(`hash`)입니다. 아틀라스 또는 타일 소스 리소스 프로퍼티와 `go.set()`을 사용해 변경할 수 있습니다. 예제는 [API 레퍼런스](/ref/sprite/#image)를 참조하세요.

`material`
: 스프라이트 메터리얼(`hash`)입니다. 메터리얼 리소스 프로퍼티와 `go.set()`을 사용해 변경할 수 있습니다. 예제는 [API 레퍼런스](/ref/sprite/#material)를 참조하세요.

`playback_rate`
: 애니메이션 재생 속도(`number`)입니다.

`scale`
: 스프라이트의 비균일 스케일(`vector3`)입니다.

`size`
: 스프라이트의 크기(`vector3`)입니다. 스프라이트 `Size Mode`가 `Manual`로 설정된 경우에만 변경할 수 있습니다.

## 메터리얼 상수

{% include shared/material-constants.md component='sprite' variable='tint' %}

`tint`
: 스프라이트의 색상 틴트(`vector4`)입니다. `vector4`는 `x`, `y`, `z`, `w`가 각각 빨강, 초록, 파랑, 알파 틴트에 대응하는 방식으로 틴트를 나타내는 데 사용됩니다.

## 메터리얼 attribute

스프라이트는 현재 할당된 메터리얼의 버텍스 attribute를 오버라이드할 수 있으며, 이 attribute들은 컴포넌트에서 버텍스 쉐이더로 전달됩니다(자세한 내용은 [메터리얼 매뉴얼](/manuals/material/#attributes)을 참조하세요).

메터리얼에 지정된 attribute는 인스펙터에 일반 프로퍼티로 표시되며 개별 스프라이트 컴포넌트에 설정할 수 있습니다. attribute 중 하나라도 오버라이드되면 오버라이드된 프로퍼티로 표시되고 디스크의 스프라이트 파일에 저장됩니다:

![sprite-attributes](../images/graphics/sprite-attributes.png)

## 프로젝트 설정

*game.project* 파일에는 스프라이트와 관련된 몇 가지 [프로젝트 설정](/manuals/project-settings#sprite)이 있습니다.

## 다중 텍스쳐 스프라이트 {#multi-textured-sprites}

스프라이트가 여러 텍스쳐를 사용할 때 주의해야 할 몇 가지 사항이 있습니다.

### 애니메이션

애니메이션 데이터(fps, 프레임 이름)는 현재 첫 번째 텍스쳐에서 가져옵니다. 이것을 "구동 애니메이션"이라고 부르겠습니다.

구동 애니메이션의 이미지 id는 다른 텍스쳐에서 이미지를 조회하는 데 사용됩니다.
따라서 텍스쳐 간에 프레임 id가 일치하는지 확인하는 것이 중요합니다.

예를 들어 `diffuse.atlas`에 다음과 같은 `run` 애니메이션이 있는 경우:

```
run:
    /main/images/hero_run_color_1.png
    /main/images/hero_run_color_2.png
    ...
```

그러면 프레임 id는 `run/hero_run_color_1`이 되며, 예를 들어 `normal.atlas`에서는 이 값을 찾기 어려울 수 있습니다:

```
run:
    /main/images/hero_run_normal_1.png
    /main/images/hero_run_normal_2.png
    ...
```

그래서 [아틀라스](/manuals/material/)의 `Rename patterns`를 사용해 이름을 변경합니다.
해당 아틀라스에 `_color=`와 `_normal=`을 설정하면 두 아틀라스 모두에서 다음과 같은 프레임 이름을 얻게 됩니다:

```
run/hero_run_1
run/hero_run_2
...
```

### UV

UV는 첫 번째 텍스쳐에서 가져옵니다. 버텍스 세트가 하나뿐이므로 보조 텍스쳐의 UV 좌표가 더 많거나 모양이 다른 경우에도
어차피 좋은 매칭을 보장할 수 없습니다.

이 점은 중요하므로 이미지들의 모양이 충분히 비슷한지 확인하세요. 그렇지 않으면 텍스쳐 블리딩이 발생할 수 있습니다.

각 텍스쳐에 있는 이미지의 크기는 서로 다를 수 있습니다.
