---
title: 아틀라스 매뉴얼
brief: 이 매뉴얼은 Defold에서 Atlas 리소스가 어떻게 동작하는지 설명합니다.
---

# 아틀라스

단일 이미지를 스프라이트의 소스로 사용하는 경우도 많지만, 성능상의 이유로 이미지는 아틀라스(atlas)라고 하는 더 큰 이미지 집합으로 결합해야 합니다. 작은 이미지들의 집합을 아틀라스로 결합하는 작업은 데스크톱 컴퓨터나 전용 게임 콘솔보다 메모리와 처리 성능이 더 부족한 모바일 기기에서 특히 중요합니다.

Defold에서 아틀라스 리소스는 서로 분리된 이미지 파일 목록이며, 이 파일들은 자동으로 더 큰 이미지 하나로 결합됩니다.

## Atlas 생성하기

*Assets* 브라우저의 컨텍스트 메뉴에서 <kbd>New... ▸ Atlas</kbd>를 선택합니다. 새 아틀라스 파일의 이름을 지정합니다. 그러면 에디터가 atlas editor에서 파일을 엽니다. 아틀라스 프로퍼티는 *Properties* 창에 표시되며 여기서 편집할 수 있습니다(자세한 내용은 아래 참고).

Sprites 및 ParticleFX 컴포넌트 같은 오브젝트 컴포넌트의 그래픽 소스로 사용하려면 먼저 아틀라스에 이미지나 애니메이션을 채워야 합니다.

이미지를 프로젝트에 추가했는지 확인하세요(이미지 파일을 *Assets* 브라우저의 올바른 위치로 드래그 앤 드롭합니다).

단일 이미지 추가하기

: *Asset* pane에서 에디터 뷰로 이미지를 드래그 앤 드롭합니다.

  또는 *Outline* 창에서 루트 Atlas 항목을 <kbd>Right click</kbd>합니다.

  팝업 컨텍스트 메뉴에서 <kbd>Add Images</kbd>를 선택해 단일 이미지를 추가합니다.

  대화상자가 열리며, 여기서 Atlas에 추가할 이미지를 찾아 선택할 수 있습니다. 이미지 파일을 필터링하고 여러 파일을 한 번에 선택할 수 있습니다.

  ![아틀라스 생성, 이미지 추가](images/atlas/add.png)

  추가된 이미지는 *Outline*에 나열되고, 전체 아틀라스는 중앙 에디터 뷰에서 볼 수 있습니다. 선택 항목이 화면에 맞게 보이도록 <kbd>F</kbd>(메뉴의 <kbd>View ▸ Frame Selection</kbd>)를 눌러야 할 수 있습니다.

  ![추가된 이미지](images/atlas/single_images.png)

플립북 애니메이션 추가하기
: *Outline* 창에서 루트 Atlas 항목을 <kbd>Right click</kbd>합니다.

  팝업 컨텍스트 메뉴에서 <kbd>Add Animation Group</kbd>을 선택해 플립북 애니메이션 그룹을 만듭니다.

  기본 이름("New Animation")을 가진 비어 있는 새 애니메이션 그룹이 아틀라스에 추가됩니다.

  *Asset* pane에서 에디터 뷰로 이미지를 드래그 앤 드롭해 현재 선택된 그룹에 추가합니다.

  또는 새 그룹을 <kbd>Right click</kbd>하고 컨텍스트 메뉴에서 <kbd>Add Images</kbd>를 선택합니다.

  대화상자가 열리며, 여기서 애니메이션 그룹에 추가할 이미지를 찾아 선택할 수 있습니다.

  ![아틀라스 생성, 이미지 추가](images/atlas/add_animation.png)

  애니메이션 그룹을 선택한 상태에서 <kbd>Space</kbd>를 눌러 미리 보고, <kbd>Ctrl/Cmd+T</kbd>를 눌러 미리보기를 닫습니다. 필요에 따라 애니메이션의 *Properties*를 조정합니다(아래 참고).

  ![애니메이션 그룹](images/atlas/animation_group.png)

이미지를 선택하고 <kbd>Alt + Up/down</kbd>을 누르면 Outline에서 이미지 순서를 바꿀 수 있습니다. 또한 outline에서 이미지를 복사해 붙여 넣으면 쉽게 복제본을 만들 수 있습니다(<kbd>Edit</kbd> 메뉴, 오른쪽 클릭 컨텍스트 메뉴 또는 키보드 단축키 사용).

## Atlas 프로퍼티

각 아틀라스 리소스에는 프로퍼티 집합이 있습니다. 이 프로퍼티들은 *Outline* 뷰에서 루트 항목을 선택하면 *Properties* 창에 표시됩니다.

Size
: 결과 텍스쳐 리소스의 계산된 전체 크기를 보여줍니다. 너비와 높이는 가장 가까운 2의 거듭제곱으로 설정됩니다. 텍스쳐 압축을 활성화하면 일부 포멧은 정사각형 텍스쳐를 요구합니다. 이 경우 정사각형이 아닌 텍스쳐는 크기가 조정되고 빈 공간으로 채워져 정사각형 텍스쳐가 됩니다. 자세한 내용은 [텍스쳐 프로파일 매뉴얼](/manuals/texture-profiles/)을 참고하세요.

Margin
: 각 이미지 사이에 추가할 픽셀 수입니다.

Inner Padding
: 각 이미지 주변에 패딩으로 넣을 빈 픽셀 수입니다.

Extrude Borders
: 각 이미지 주변에 반복해서 패딩할 가장자리 픽셀 수입니다. 프래그먼트 쉐이더가 이미지 가장자리의 픽셀을 샘플링할 때, 같은 아틀라스 텍스쳐에 있는 이웃 이미지의 픽셀이 번질 수 있습니다. 가장자리를 extrude하면 이 문제를 해결할 수 있습니다.

Max Page Size
: multi-page atlas에서 페이지의 최대 크기입니다. 이는 단일 드로우 콜만 사용하면서도 아틀라스 크기를 제한하기 위해, 하나의 아틀라스를 같은 아틀라스의 여러 페이지로 나누는 데 사용할 수 있습니다. 이 기능은 `/builtins/materials/*_paged_atlas.material`에 있는 multi-page atlas 활성화 메터리얼과 함께 사용해야 합니다.

![Multi-page atlas](images/atlas/multipage_atlas.png)

Rename Patterns
: 쉼표(´,´)로 구분된 검색 및 치환 패턴 목록이며, 각 패턴은 `search=replace` 형식입니다.
각 이미지의 원래 이름(파일 기본 이름)은 이 패턴을 사용해 변환됩니다. (예: 패턴 `hat=cat,_normal=`은 이름이 `hat_normal`인 이미지를 `cat`으로 바꿉니다). 이는 아틀라스 사이에서 애니메이션을 일치시킬 때 유용합니다.

다음은 크기 64x64인 정사각형 이미지 네 개를 아틀라스에 추가했을 때 서로 다른 프로퍼티 설정을 보여주는 예입니다. 이미지가 128x128 안에 들어가지 않게 되는 순간 아틀라스가 256x256으로 커져 많은 텍스쳐 공간이 낭비되는 것을 확인할 수 있습니다.

![아틀라스 프로퍼티](images/atlas/atlas_properties.png)

## Image 프로퍼티

아틀라스의 각 이미지에는 프로퍼티 집합이 있습니다:

Id
: 이미지의 id입니다(읽기 전용).

Size
: 이미지의 너비와 높이입니다(읽기 전용).

Pivot
: 이미지의 피벗 포인트입니다(단위 기준). 왼쪽 위는 (0,0)이고 오른쪽 아래는 (1,1)입니다. 기본값은 (0.5, 0.5)입니다. 피벗은 0-1 범위 밖에 있을 수도 있습니다. 피벗 포인트는 이미지가 예를 들어 스프라이트에서 사용될 때 이미지가 중앙에 배치되는 위치입니다. 에디터 뷰에서 피벗 핸들을 드래그해 피벗 포인트를 수정할 수 있습니다. 핸들은 단일 이미지만 선택된 경우에만 표시됩니다. 드래그하는 동안 <kbd>Shift</kbd>를 누르고 있으면 스냅을 활성화할 수 있습니다.

Sprite Trim Mode
: 스프라이트가 렌더링되는 방식입니다. 기본값은 스프라이트를 사각형으로 렌더링하는 것입니다(Sprite Trim Mode가 Off로 설정됨). 스프라이트에 투명 픽셀이 많다면 4개에서 8개 사이의 버텍스를 사용해 스프라이트를 사각형이 아닌 형태로 렌더링하는 것이 더 효율적일 수 있습니다. sprite trimming은 slice-9 스프라이트와 함께 동작하지 않는다는 점에 유의하세요.

Image
: 이미지 자체의 경로입니다.

![이미지 프로퍼티](images/atlas/image_properties.png)

## Animation 프로퍼티

애니메이션 그룹에 포함된 이미지 목록 외에도 다음 프로퍼티 집합을 사용할 수 있습니다:

Id
: 애니메이션의 이름입니다.

Fps
: 초당 프레임 수(FPS)로 표현되는 애니메이션 재생 속도입니다.

Flip horizontal
: 애니메이션을 가로로 뒤집습니다.

Flip vertical
: 애니메이션을 세로로 뒤집습니다.

Playback
: 애니메이션 재생 방식을 지정합니다:

  - `None`은 전혀 재생하지 않고 첫 번째 이미지를 표시합니다.
  - `Once Forward`는 애니메이션을 첫 번째 이미지에서 마지막 이미지까지 한 번 재생합니다.
  - `Once Backward`는 애니메이션을 마지막 이미지에서 첫 번째 이미지까지 한 번 재생합니다.
  - `Once Ping Pong`은 애니메이션을 첫 번째 이미지에서 마지막 이미지까지 한 번 재생한 다음 다시 첫 번째 이미지로 되돌아갑니다.
  - `Loop Forward`는 애니메이션을 첫 번째 이미지에서 마지막 이미지까지 반복 재생합니다.
  - `Loop Backward`는 애니메이션을 마지막 이미지에서 첫 번째 이미지까지 반복 재생합니다.
  - `Loop Ping Pong`은 애니메이션을 첫 번째 이미지에서 마지막 이미지까지 반복 재생한 다음 다시 첫 번째 이미지로 되돌아갑니다.

## 런타임 Texture 및 Atlas 생성

런타임에 텍스쳐와 아틀라스를 생성할 수 있습니다.

### 런타임에 Texture 리소스 생성하기

새 텍스쳐 리소스를 생성하려면 [`resource.create_texture(path, params)`](https://defold.com/ref/stable/resource/#resource.create_texture:path-table)를 사용합니다:

```lua
  local params = {
    width  = 128,
    height = 128,
    type   = graphics.TEXTURE_TYPE_2D,
    format = graphics.TEXTURE_FORMAT_RGBA,
  }
  local my_texture_id = resource.create_texture("/my_custom_texture.texturec", params)
```

텍스쳐가 생성되면 [`resource.set_texture(path, params, buffer)`](https://defold.com/ref/stable/resource/#resource.set_texture:path-table-buffer)를 사용해 텍스쳐의 픽셀을 설정할 수 있습니다:

```lua
  local width = 128
  local height = 128
  local buf = buffer.create(width * height, { { name=hash("rgba"), type=buffer.VALUE_TYPE_UINT8, count=4 } } )
  local stream = buffer.get_stream(buf, hash("rgba"))

  for y=1, height do
      for x=1, width do
          local index = (y-1) * width * 4 + (x-1) * 4 + 1
          stream[index + 0] = 0xff
          stream[index + 1] = 0x80
          stream[index + 2] = 0x10
          stream[index + 3] = 0xFF
      end
  end

  local params = { width=width, height=height, x=0, y=0, type=graphics.TEXTURE_TYPE_2D, format=graphics.TEXTURE_FORMAT_RGBA, num_mip_maps=1 }
  resource.set_texture(my_texture_id, params, buf)
```

::: sidenote
`resource.set_texture()`를 사용하면 텍스쳐 전체 크기보다 작은 buffer 너비와 높이를 사용하고 `resource.set_texture()`의 x 및 y 파라미터를 변경하여 텍스쳐의 하위 영역도 업데이트할 수 있습니다.
:::

텍스쳐는 `go.set()`을 사용해 [모델 컴포넌트](/manuals/model/)에서 직접 사용할 수 있습니다:

```lua
  go.set("#model", "texture0", my_texture_id)
```

### 런타임에 Atlas 생성하기

텍스쳐를 [스프라이트 컴포넌트](/manuals/sprite/)에서 사용하려면 먼저 아틀라스에서 사용해야 합니다. Atlas를 생성하려면 [`resource.create_atlas(path, params)`](https://defold.com/ref/stable/resource/#resource.create_atlas:path-table)를 사용합니다:

```lua
  local params = {
    texture = texture_id,
    animations = {
      {
        id          = "my_animation",
        width       = width,
        height      = height,
        frames      = { 1 },
      }
    },
    geometries = {
      {
        vertices  = {
          0,     0,
          0,     height,
          width, height,
          width, 0
        },
        uvs = {
          0,     0,
          0,     height,
          width, height,
          width, 0
        },
        indices = {0,1,2,0,2,3}
      }
    }
  }
  local my_atlas_id = resource.create_atlas("/my_atlas.texturesetc", params)

  -- 같은 go의 'sprite' 컴포넌트에 아틀라스를 할당합니다
  go.set("#sprite", "image", my_atlas_id)

  -- "animation"을 재생합니다
  sprite.play_flipbook("#sprite", "my_animation")

```

`frames` 항목은 `geometries` 테이블을 참조하는 1부터 시작하는 인덱스입니다. 목록에서 geometry를 재사용하거나, 순서를 바꾸거나, 건너뛸 수 있으며, 이는 더 이상 권장되지 않는 `frame_start`와 `frame_end` 구간 필드로는 표현할 수 없습니다. `resource.get_atlas()`는 `frames`를 반환합니다. atlas 데이터를 `resource.set_atlas()` 또는 `resource.create_atlas()`에 전달할 때도 같은 표현을 사용하세요. setter와 creator는 호환성을 위해 구간 필드를 계속 지원하지만 새 코드에서는 `frames`를 사용해야 합니다.
