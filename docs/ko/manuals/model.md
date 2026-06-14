---
title: Defold의 3D 모델
brief: 이 매뉴얼은 3D 모델, 스켈레톤, 애니메이션을 게임에 가져오는 방법을 설명합니다.
---

# 모델 컴포넌트

Defold는 기본적으로 3D 엔진입니다. 2D 메터리얼만으로 작업하더라도 모든 렌더링은 3D에서 수행되며, 화면에는 직교 투영으로 표시됩니다. Defold에서는 3D 에셋, 즉 _모델_을 컬렉션에 포함해 완전한 3D 컨텐츠를 사용할 수 있습니다. 3D 에셋만 사용해 순수한 3D 게임을 만들 수도 있고, 원하는 대로 3D와 2D 컨텐츠를 섞을 수도 있습니다.

## 모델 컴포넌트 생성하기

모델 컴포넌트는 다른 게임 오브젝트 컴포넌트와 같은 방식으로 생성합니다. 두 가지 방법이 있습니다:

- *Assets* 브라우저의 원하는 위치를 <kbd>마우스 오른쪽 버튼으로 누르고</kbd> <kbd>New... ▸ Model</kbd>을 선택해 *Model file*을 만듭니다.
- *Outline* 뷰에서 게임 오브젝트를 <kbd>마우스 오른쪽 버튼으로 누르고</kbd> <kbd>Add Component ▸ Model</kbd>을 선택해 컴포넌트를 게임 오브젝트에 직접 내장합니다.

![Model in game object](images/model/model_gltf.png)

모델을 만들고 나면 여러 프로퍼티를 지정해야 합니다:

### 모델 프로퍼티

*Id*, *Position*, *Rotation* 프로퍼티 외에 다음 컴포넌트별 프로퍼티가 있습니다:

*Mesh*
: 이 프로퍼티는 사용할 메쉬가 들어 있는 glTF *.gltf* 또는 *.glb* 파일을 참조해야 합니다. 파일에 morph target이 포함되어 있으면 메쉬와 함께 가져옵니다. 파일에 메쉬가 여러 개 있으면 첫 번째 메쉬만 읽습니다.

*Create GO Bones*
: 모델의 각 본(bone)에 대해 게임 오브젝트를 생성하려면 이 값을 체크합니다. 이 게임 오브젝트를 사용해 무기 같은 다른 게임 오브젝트를 손 본 등에 붙일 수 있습니다.

*Skeleton*
: 이 프로퍼티는 애니메이션에 사용할 스켈레톤이 들어 있는 glTF *.gltf* 또는 *.glb* 파일을 참조해야 합니다. Defold는 계층구조에 단일 루트 본이 필요하다는 점에 유의하세요.

*Animations*
: 모델에 사용할 애니메이션이 들어 있는 *Animation Set File*로 설정합니다.

*Default Animation*
: 모델에서 자동으로 재생될 애니메이션입니다(애니메이션 세트에서 가져옴).

위 프로퍼티 외에도 모델의 각 메쉬에 메터리얼을 할당하는 필드가 있습니다:

*Material*
: 이 프로퍼티를 텍스쳐가 있는 3D 오브젝트에 적합하도록 직접 만든 메터리얼로 설정합니다. 시작점으로 사용할 수 있는 내장 메터리얼이 몇 가지 있습니다:

  * 정적 인스턴싱되지 않은 모델에는 *model.material*을 사용합니다
  * 정적 인스턴싱된 모델에는 *model_instances.material*을 사용합니다
  * 스킨드(애니메이션되는) 인스턴싱되지 않은 모델에는 *model_skinned.material*을 사용합니다
  * 스킨드(애니메이션되는) 인스턴싱된 모델에는 *model_skinned_instances.material*을 사용합니다

메터리얼에 따라 하나 이상의 텍스쳐 프로퍼티가 있습니다:

*Texture*
: 이 프로퍼티는 오브젝트에 적용하려는 텍스쳐 이미지 파일을 가리켜야 합니다.


## 에디터 조작

모델 컴포넌트를 배치한 뒤에는 일반 *Scene Editor* 도구로 컴포넌트 및/또는 이를 감싸는 게임 오브젝트를 자유롭게 편집하고 조작하여 원하는 대로 모델을 이동, 회전, 확대/축소할 수 있습니다.

## 런타임 조작

여러 함수와 프로퍼티를 통해 런타임에 모델을 조작할 수 있습니다(사용 방법은 [API 문서](/ref/model/)를 참조하세요).

![Wiggler ingame](images/model/runtime.png)

### 런타임 애니메이션

Defold는 런타임에 애니메이션을 제어하는 강력한 지원을 제공합니다. 자세한 내용은 [모델 애니메이션 매뉴얼](/manuals/model-animation)을 참고하세요:

```lua
local play_properties = { blend_duration = 0.1 }
model.play_anim("#model", "jump", go.PLAYBACK_ONCE_FORWARD, play_properties)
```

애니메이션 재생 커서는 직접 조작하거나 프로퍼티 애니메이션 시스템을 통해 애니메이션할 수 있습니다:

```lua
-- run 애니메이션 설정
model.play_anim("#model", "run", go.PLAYBACK_NONE)
-- 커서 애니메이션
go.animate("#model", "cursor", go.PLAYBACK_LOOP_PINGPONG, 1, go.EASING_LINEAR, 10)
```

모델은 glTF morph target 애니메이션도 사용할 수 있습니다. morph target weight는 다른 모델 애니메이션처럼 `model.play_anim()`으로 애니메이션되며, 런타임에 [`model.get_blend_weights()`](/ref/model#model.get_blend_weights)와 [`model.set_blend_weights()`](/ref/model#model.set_blend_weights)를 사용해 읽거나 오버라이드할 수 있습니다. 자세한 내용은 모델 애니메이션 매뉴얼의 [morph target 섹션](/manuals/model-animation#morph-targets)을 참고하세요.

### 프로퍼티 변경

모델에는 `go.get()` 및 `go.set()`으로 조작할 수 있는 여러 프로퍼티도 있습니다:

`animation`
: 현재 모델 애니메이션입니다(`hash`). 읽기 전용입니다. 애니메이션은 `model.play_anim()`으로 변경합니다(위 참조).

`cursor`
: 정규화된 애니메이션 커서입니다(`number`).

`material`
: 모델 메터리얼입니다(`hash`). 메터리얼 리소스 프로퍼티와 `go.set()`을 사용해 변경할 수 있습니다. 예제는 [API 레퍼런스](/ref/model/#material)를 참고하세요.

`playback_rate`
: 애니메이션 재생 속도입니다(`number`).

`textureN`
: N이 0-7인 모델 텍스쳐입니다(`hash`). 텍스쳐 리소스 프로퍼티와 `go.set()`을 사용해 변경할 수 있습니다. 예제는 [API 레퍼런스](/ref/model/#textureN)를 참고하세요.


## 메터리얼

3D 소프트웨어에서는 보통 색상이나 텍스쳐 같은 프로퍼티를 오브젝트 버텍스에 설정할 수 있습니다. 이 정보는 3D 소프트웨어에서 익스포트하는 glTF *.gltf* 또는 *.glb* 파일에 들어갑니다. 게임의 요구사항에 따라 오브젝트에 적합하고 _성능이 좋은_ 메터리얼을 선택하거나 만들어야 합니다. 메터리얼은 오브젝트 렌더링을 위한 _쉐이더 프로그램_ 과 파라미터 집합을 결합합니다.

시작점으로 사용할 수 있는 내장 메터리얼이 몇 가지 있습니다:

  * 정적 인스턴싱되지 않은 모델에는 *model.material*을 사용합니다
  * 정적 인스턴싱된 모델에는 *model_instances.material*을 사용합니다
  * 스킨드(애니메이션되는) 인스턴싱되지 않은 모델에는 *model_skinned.material*을 사용합니다
  * 스킨드(애니메이션되는) 인스턴싱된 모델에는 *model_skinned_instances.material*을 사용합니다

모델용 커스텀 메터리얼을 만들어야 한다면 [메터리얼 문서](/manuals/material)를 참고하세요. [쉐이더 매뉴얼](/manuals/shader)에는 쉐이더 프로그램이 어떻게 동작하는지에 대한 정보가 있습니다.


### 메터리얼 상수

{% include shared/material-constants.md component='model' variable='tint' %}

`tint`
: 모델의 색조(tint)입니다(`vector4`). `vector4`는 x, y, z, w가 각각 빨강, 초록, 파랑, 알파 색조에 대응하는 tint를 표현하는 데 사용됩니다.


## 렌더링

기본 렌더 스크립트는 2D 게임에 맞춰 만들어졌기 때문에 3D 모델에는 동작하지 않습니다. 하지만 기본 렌더 스크립트를 복사하고 렌더 스크립트에 몇 줄의 코드를 추가하면 모델 렌더링을 활성화할 수 있습니다. 예를 들면:

  ```lua

  function init(self)
    self.model_pred = render.predicate({"model"})
    ...
  end

  function update()
    ...
    render.set_depth_mask(true)
    render.enable_state(graphics.STATE_DEPTH_TEST)
    render.set_projection(stretch_projection(-1000, 1000))  -- 직교
    render.draw(self.model_pred)
    render.set_depth_mask(false)
    ...
  end
  ```

렌더 스크립트가 어떻게 동작하는지에 대한 자세한 내용은 [렌더 문서](/manuals/render)를 참고하세요.
