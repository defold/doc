---
title: 엔드리스 러너 튜토리얼
brief: 이 튜토리얼에서는 빈 프로젝트에서 시작해 애니메이션 캐릭터, 물리 충돌, 수집 아이템, 점수 기능이 있는 완전한 러너 게임을 만듭니다.
---

# 러너 튜토리얼

이 튜토리얼에서는 빈 프로젝트에서 시작해 애니메이션 캐릭터, 물리 충돌, 수집 아이템, 점수 기능이 있는 완전한 러너 게임을 만듭니다.

새 게임엔진을 배울 때는 받아들여야 할 내용이 많으므로, 시작을 돕기 위해 이 튜토리얼을 만들었습니다. 이 튜토리얼은 엔진과 에디터가 어떻게 동작하는지 단계별로 살펴보는 꽤 완성도 있는 튜토리얼입니다. 프로그래밍에 어느 정도 익숙하다고 가정합니다.

Lua 프로그래밍 입문이 필요하다면 [Defold의 Lua 매뉴얼](/manuals/lua)을 확인하세요.

처음 시작하기에 이 튜토리얼이 조금 어렵게 느껴진다면, 다양한 난이도의 튜토리얼을 모아 둔 [튜토리얼 페이지](//www.defold.com/tutorials)를 확인하세요.

비디오 튜토리얼을 보는 것을 선호한다면 [Youtube의 비디오 버전](https://www.youtube.com/playlist?list=PLXsXu5srjNlxtYPQ_YJQSxJG2AN9OVS5b)을 확인하세요.

약간 수정한 두 개의 다른 튜토리얼 게임 에셋을 사용합니다. 튜토리얼은 여러 단계로 나뉘며, 각 파트는 최종 게임을 향해 중요한 한 걸음씩 진행합니다.

최종 결과물은 환경 속을 달리는 영웅 캐릭터를 조작해 코인을 모으고 장애물을 피하는 게임입니다. 영웅 캐릭터는 고정 속도로 달리며, 플레이어는 버튼 하나를 누르거나 모바일 기기에서 화면을 터치해 영웅 캐릭터의 점프만 제어합니다. 레벨은 점프해서 올라갈 플랫폼과 수집할 코인이 끝없이 이어지는 구조로 구성됩니다.

이 튜토리얼을 진행하거나 게임을 만들다가 막히는 부분이 있으면 언제든 [Defold Forum](//forum.defold.com)에서 도움을 요청하세요. 포럼에서는 Defold에 대해 논의하고, Defold 팀에 도움을 요청하고, 다른 게임 개발자가 문제를 어떻게 해결했는지 살펴보고, 새로운 영감을 얻을 수 있습니다. 지금 시작해 보세요.

::: sidenote
튜토리얼 전체에서 개념과 특정 작업 방법에 대한 자세한 설명은 이 문단처럼 표시됩니다. 이런 섹션이 너무 자세하다고 느껴지면 건너뛰어도 됩니다.
:::

그럼 시작해 보겠습니다. 이 튜토리얼을 따라가며 즐겁게 배우고, Defold를 시작하는 데 도움이 되기를 바랍니다.

> 이 튜토리얼의 에셋은 [여기](https://github.com/defold/sample-runner/tree/main/def-runner)에서 다운로드하세요.

## STEP 1 - 설치와 설정

첫 단계는 [다음 파일을 다운로드](https://github.com/defold/sample-runner/tree/main/def-runner)하는 것입니다.

아직 Defold 에디터를 다운로드하고 설치하지 않았다면 지금 설치하세요.

:[install](../shared/install.md)

에디터를 설치하고 시작했다면 새 프로젝트를 만들고 준비할 차례입니다. "Empty Project" 템플릿에서 [새 프로젝트](/manuals/project-setup/#creating-a-new-project)를 생성합니다.

::: sidenote
이 튜토리얼은 [Spine Extension](https://github.com/defold/extension-spine)의 Spine 기능을 사용합니다. *game.project*의 dependencies 섹션에 익스텐션을 추가하세요.
:::

## 에디터

에디터를 처음 시작하면 열린 프로젝트 없이 빈 상태로 시작하므로 메뉴에서 <kbd>Open Project</kbd>를 선택하고 새로 만든 프로젝트를 선택합니다. 프로젝트의 "branch"를 만들라는 안내도 표시됩니다.

이제 *Assets pane*에서 프로젝트에 포함된 모든 파일을 볼 수 있습니다. "main/main.collection" 파일을 더블 클릭하면 중앙의 에디터 뷰에서 파일이 열립니다.

![에디터 개요](images/runner/1/editor2_overview.png)

에디터는 다음과 같은 주요 영역으로 구성됩니다.

Assets pane
: 프로젝트의 모든 파일을 보여주는 뷰입니다. 파일 타입마다 서로 다른 아이콘이 있습니다. 파일을 더블 클릭하면 해당 파일 타입에 맞는 전용 에디터에서 열립니다. 특별한 읽기 전용 폴더인 *builtins*는 모든 프로젝트에서 공통으로 사용되며, 기본 렌더 스크립트, 폰트, 다양한 컴포넌트를 렌더링하기 위한 메터리얼 등 유용한 항목을 포함합니다.

Main Editor View
: 편집 중인 파일 타입에 따라 이 뷰에는 해당 타입의 에디터가 표시됩니다. 여기에서 보이는 Scene editor가 가장 일반적으로 사용됩니다. 열려 있는 각 파일은 별도 탭에 표시됩니다.

Changed Files
: 마지막 동기화 이후 현재 브랜치에서 만든 모든 편집 목록을 포함합니다. 따라서 이 창에 무언가 보인다면 아직 서버에 없는 변경사항이 있다는 뜻입니다. 이 뷰를 통해 텍스트 전용 diff를 열고 변경사항을 되돌릴 수 있습니다.

Outline
: 현재 편집 중인 파일의 컨텐츠를 계층형 뷰로 보여줍니다. 이 뷰를 통해 오브젝트와 컴포넌트를 추가, 삭제, 수정, 선택할 수 있습니다.

Properties
: 현재 선택한 오브젝트나 컴포넌트에 설정된 프로퍼티입니다.

Console
: 게임을 실행할 때 이 뷰는 게임엔진에서 오는 출력(로깅, 오류, 디버그 정보 등)과 스크립트의 커스텀 `print()` 및 `pprint()` 디버그 메세지를 캡처합니다. 앱이나 게임이 시작되지 않으면 가장 먼저 콘솔을 확인해야 합니다. 콘솔 뒤에는 오류 정보를 표시하는 탭들과 파티클 효과를 만들 때 사용하는 Curve Editor가 있습니다.

## 게임 실행하기

"Empty" 프로젝트 템플릿은 실제로 완전히 비어 있습니다. 그래도 <kbd>Project ▸ Build</kbd>를 선택해 프로젝트를 빌드하고 게임을 실행합니다.

![빌드](images/runner/1/build_and_launch.png)

검은 화면은 그다지 흥미롭지 않을 수 있지만, 실행 중인 Defold 게임 어플리케이션이며 쉽게 더 흥미로운 것으로 바꿀 수 있습니다. 이제 그렇게 해보겠습니다.

::: sidenote
Defold 에디터는 파일을 기준으로 동작합니다. *Assets pane*에서 파일을 더블 클릭하면 적절한 에디터로 열립니다. 그런 다음 파일의 내용을 작업할 수 있습니다.

파일 편집이 끝나면 저장해야 합니다. 메인 메뉴에서 <kbd>File ▸ Save</kbd>를 선택합니다. 에디터는 저장되지 않은 변경사항이 있는 파일의 탭에서 파일명에 별표 '\*'를 추가해 알려줍니다.

![저장되지 않은 변경사항이 있는 파일](images/runner/1/file_changed.png)
:::

## 프로젝트 설정하기

시작하기 전에 프로젝트의 몇 가지 설정을 조정하겠습니다. `Assets Pane`에서 *game.project* 에셋을 열고 Display 섹션까지 아래로 스크롤합니다. 프로젝트의 `width`와 `height`를 각각 `1280`과 `720`으로 설정합니다.

영웅 캐릭터에 애니메이션을 적용할 수 있도록 Spine 익스텐션도 프로젝트에 추가해야 합니다. 설치한 Defold 에디터 버전과 호환되는 Spine 익스텐션 버전을 추가하세요. 사용 가능한 Spine 버전은 여기에서 확인할 수 있습니다.

[https://github.com/defold/extension-spine/releases](https://github.com/defold/extension-spine/releases)

사용하려는 릴리스의 zip 파일 링크를 마우스 오른쪽 버튼으로 클릭합니다.

![Right click and copy link to release](images/runner/extension-spine-releases.png)

릴리스 링크를 [game.project dependencies](/manuals/libraries/#setting-up-library-dependencies) 목록에 추가합니다. Spine 익스텐션을 추가한 뒤에는 Spine 익스텐션에 포함된 에디터 통합을 활성화하기 위해 에디터를 다시 시작해야 합니다.


## STEP 2 - 지면 만들기

첫 작은 단계로 캐릭터를 위한 경기장, 더 정확히는 스크롤되는 지면 조각을 만듭니다. 이 작업은 몇 단계로 진행합니다.

1. 이미지 에셋을 프로젝트로 가져옵니다. 에셋 패키지의 "level-images" 하위 폴더에 있는 "ground01.png"와 "ground02.png" 이미지 파일을 프로젝트의 적절한 위치, 예를 들어 "main" 폴더 안의 "images" 폴더로 드래그합니다.
2. 지면 텍스쳐를 담을 새 *Atlas* 파일을 만듭니다(*Assets pane*에서 적절한 폴더, 예를 들어 *main* 폴더를 마우스 오른쪽 버튼으로 클릭하고 <kbd>New ▸ Atlas File</kbd>을 선택). 아틀라스 파일 이름은 *level.atlas*로 지정합니다.

  ::: sidenote
  *Atlas*는 여러 개의 개별 이미지를 하나의 더 큰 이미지 파일로 결합하는 파일입니다. 이렇게 하는 이유는 공간을 절약하고 성능을 높이기 위해서입니다. 아틀라스와 다른 2D 그래픽 기능에 대해서는 [2D 그래픽 문서](/manuals/2dgraphics)에서 더 자세히 읽을 수 있습니다.
  :::

3. *Outline*에서 아틀라스 루트를 마우스 오른쪽 버튼으로 클릭하고 <kbd>Add Images</kbd>를 선택해 새 아틀라스에 지면 이미지를 추가합니다. 가져온 이미지를 선택하고 *OK*를 클릭합니다. 이제 아틀라스의 각 이미지는 스프라이트, 파티클 효과, 기타 시각 요소에서 사용할 수 있는 1프레임 애니메이션(정지 이미지)으로 접근할 수 있습니다. 파일을 저장합니다.

  ![새 아틀라스 생성](images/runner/1/new_atlas.png)

  ![아틀라스에 이미지 추가](images/runner/1/add_images_to_atlas.png)

  ::: sidenote
  *왜 동작하지 않죠!?* Defold를 처음 시작할 때 사람들이 흔히 겪는 문제는 저장하는 것을 잊는 것입니다! 아틀라스에 이미지를 추가한 뒤에는 그 이미지에 접근하기 전에 파일을 저장해야 합니다.
  :::

4. 지면용 컬렉션 파일 *ground.collection*을 만들고 여기에 게임 오브젝트 7개를 추가합니다(*Outline* 뷰에서 컬렉션의 루트를 마우스 오른쪽 버튼으로 클릭하고 <kbd>Add Game Object</kbd> 선택). *Properties* 뷰에서 *Id* 프로퍼티를 변경해 오브젝트 이름을 "ground0", "ground1", "ground2" 등으로 지정합니다. Defold는 새 게임 오브젝트에 자동으로 유니크한 id를 할당한다는 점에 유의하세요.

5. 각 오브젝트에 스프라이트 컴포넌트를 추가하고(*Outline* 뷰에서 게임 오브젝트를 마우스 오른쪽 버튼으로 클릭한 뒤 <kbd>Add Component</kbd>를 선택하고 *Sprite*를 선택한 다음 *OK* 클릭), 스프라이트 컴포넌트의 *Image* 프로퍼티를 방금 만든 아틀라스로 설정하고 스프라이트의 기본 애니메이션을 두 지면 이미지 중 하나로 설정합니다. _스프라이트 컴포넌트_(게임 오브젝트가 아님)의 X 포지션을 190, Y 포지션을 40으로 설정합니다. 이미지의 너비가 380픽셀이고 옆으로 그 절반만큼 이동했으므로, 게임 오브젝트의 피벗은 스프라이트 이미지의 가장 왼쪽 가장자리에 위치합니다.

  ![지면 컬렉션 생성](images/runner/1/ground_collection.png)

6. 사용 중인 그래픽이 조금 너무 크므로 각 게임 오브젝트를 60%로 스케일합니다(X와 Y에서 0.6 스케일, 결과적으로 너비 228픽셀의 지면 조각).

  ![지면 스케일 조정](images/runner/1/scale_ground.png)

7. 모든 _게임 오브젝트_를 한 줄로 배치합니다. _게임 오브젝트_(스프라이트 컴포넌트가 아님)의 X 포지션을 0, 228, 456, 684, 912, 1140, 1368로 설정합니다(너비 228픽셀의 배수).

  ::: sidenote
  스프라이트 컴포넌트가 있는 완성된 스케일 적용 게임 오브젝트 하나를 만든 뒤 복사하는 것이 아마 가장 쉽습니다. *Outline* 뷰에서 표시한 다음 <kbd>Edit ▸ Copy</kbd>를 선택하고 이어서 <kbd>Edit ▸ Paste</kbd>를 선택합니다.

  더 크거나 작은 타일을 원한다면 스케일만 변경하면 된다는 점도 알아두면 좋습니다. 하지만 그렇게 하면 모든 지면 게임 오브젝트의 X 포지션도 새 너비의 배수로 변경해야 합니다.
  :::

8. 파일을 저장한 다음 *ground.collection*을 *main.collection* 파일에 추가합니다. 먼저 *main.collection* 파일을 더블 클릭하고, *Outline* 뷰에서 루트 오브젝트를 마우스 오른쪽 버튼으로 클릭한 뒤 <kbd>Add Collection From File</kbd>을 선택합니다. 다이얼로그에서 *ground.collection*을 선택하고 *OK*를 클릭합니다. *ground.collection*을 반드시 0, 0, 0 위치에 배치하세요. 그렇지 않으면 화면에서 오프셋되어 보입니다. 저장합니다.

9. 게임을 시작해(<kbd>Project ▸ Build</kbd>) 모든 것이 제자리에 있는지 확인합니다.

  ![정지된 지면](images/runner/1/still_ground.png)

이쯤 되면 지금까지 만든 것들이 실제로 무엇인지 혼란스러울 수 있으니, 잠시 모든 Defold 프로젝트의 가장 기본적인 빌딩 블록을 살펴보겠습니다.

게임 오브젝트
: 실행 중인 게임 안에 존재하는 것들입니다. 각 게임 오브젝트는 3D 공간의 위치, 회전, 스케일을 가집니다. 반드시 보일 필요는 없습니다. 게임 오브젝트는 그래픽(스프라이트, 타일맵, 모델, Spine 모델, 파티클 효과), 사운드, 물리, 팩토리(스폰용) 등의 기능을 추가하는 _컴포넌트_를 원하는 수만큼 가질 수 있습니다. Lua _스크립트 컴포넌트_도 추가해 게임 오브젝트에 동작을 줄 수 있습니다. 게임에 존재하는 각 게임 오브젝트에는 메세지 전달을 통해 통신할 때 필요한 *id*가 있습니다.

컬렉션
: 컬렉션 자체는 실행 중인 게임에 독립적으로 존재하지 않지만, 게임 오브젝트의 정적 이름 지정을 가능하게 하면서 동시에 같은 게임 오브젝트의 여러 인스턴스를 허용하는 데 사용됩니다. 실제로 컬렉션은 게임 오브젝트와 다른 컬렉션을 담는 컨테이너로 사용됩니다. 복잡한 게임 오브젝트와 컬렉션 계층구조의 프로토타입(다른 엔진에서는 "prefabs" 또는 "blueprints"라고도 함)처럼 컬렉션을 사용할 수 있습니다. 시작 시 엔진은 main 컬렉션을 로드하고 그 안에 넣어 둔 모든 것에 생명을 불어넣습니다. 기본적으로 이것은 프로젝트의 *main* 폴더 안에 있는 *main.collection* 파일이지만, 프로젝트 설정에서 변경할 수 있습니다.

지금은 이 설명으로 충분할 것입니다. 하지만 이런 항목을 훨씬 더 포괄적으로 다룬 내용은 [빌딩 블록 매뉴얼](/manuals/building-blocks)에서 확인할 수 있습니다. 나중에 Defold에서 사물이 어떻게 동작하는지 더 깊이 이해하려면 해당 매뉴얼을 살펴보는 것이 좋습니다.

## STEP 3 - 지면 움직이기

이제 모든 지면 조각을 제자리에 배치했으므로 움직이게 만드는 것은 꽤 간단합니다. 아이디어는 이렇습니다. 조각들을 오른쪽에서 왼쪽으로 이동시키고, 조각 하나가 화면 바깥의 가장 왼쪽 가장자리에 도달하면 가장 오른쪽 위치로 옮깁니다. 이 모든 게임 오브젝트를 이동하려면 Lua 스크립트가 필요하므로 하나 만들어 보겠습니다.

1. *Assets pane*에서 *main* 폴더를 마우스 오른쪽 버튼으로 클릭하고 <kbd>New ▸ Script File</kbd>을 선택합니다. 새 파일 이름은 *ground.script*로 지정합니다.
2. 새 파일을 더블 클릭해 Lua 스크립트 에디터를 엽니다.
3. 파일의 기본 내용을 삭제하고 다음 Lua 코드를 복사해 넣은 뒤 파일을 저장합니다.

```lua
-- ground.script
local pieces = { "ground0", "ground1", "ground2", "ground3",
                    "ground4", "ground5", "ground6" } -- <1>

function init(self) -- <2>
    self.speed = 360  -- 픽셀/s 단위 속도
end

function update(self, dt) -- <3>
    for i, p in ipairs(pieces) do -- <4>
        local pos = go.get_position(p)
        if pos.x <= -228 then -- <5>
            pos.x = 1368 + (pos.x + 228)
        end
        pos.x = pos.x - self.speed * dt -- <6>
        go.set_position(pos, p) -- <7>
    end
end
```
1. 지면 게임 오브젝트의 id를 Lua 테이블에 저장해 반복 처리할 수 있게 합니다.
2. `init()` 함수는 게임 오브젝트가 게임 안에서 살아날 때 호출됩니다. 지면의 속도를 담는 오브젝트 로컬 멤버 변수를 초기화합니다.
3. `update()`는 각 프레임마다 한 번, 일반적으로 초당 60번 호출됩니다. `dt`에는 마지막 호출 이후 지난 초 단위 시간이 들어 있습니다.
4. 모든 지면 게임 오브젝트를 반복 처리합니다.
5. 현재 위치를 로컬 변수에 저장한 다음, 현재 오브젝트가 가장 왼쪽 가장자리에 있으면 가장 오른쪽 가장자리로 옮깁니다.
6. 현재 X 포지션을 설정된 속도만큼 감소시킵니다. `dt`를 곱해 프레임레이트와 무관한 픽셀/s 단위 속도를 얻습니다.
7. 새 속도로 오브젝트의 위치를 업데이트합니다.

::: sidenote
Defold는 데이터와 게임 오브젝트를 관리하는 빠른 엔진 코어입니다. 게임에 필요한 모든 로직이나 동작은 Lua 언어로 만듭니다. Lua는 게임 로직을 작성하기에 좋은 빠르고 가벼운 프로그래밍 언어입니다. [Programming in Lua](http://www.lua.org/pil/) 책과 공식 [Lua reference manual](http://www.lua.org/manual/5.3/)처럼 이 언어를 배울 수 있는 좋은 자료가 있습니다.

Defold는 Lua 위에 여러 API를 추가하고, 게임 오브젝트 간 통신을 프로그래밍할 수 있게 해주는 _메세지 전달_ 시스템도 제공합니다. 동작 방식에 대한 자세한 내용은 [메세지 전달 매뉴얼](/manuals/message-passing)을 참고하세요.
:::

::: sidenote
각각 <kbd>F6</kbd>, <kbd>F7</kbd>, <kbd>F8</kbd> 키를 사용해 에디터의 Assets Pane, Console, Outline 섹션을 토글할 수 있습니다.
:::

이제 스크립트 파일이 있으므로 게임 오브젝트의 컴포넌트에 이 파일에 대한 참조를 추가해야 합니다. 그러면 스크립트가 게임 오브젝트 라이프사이클의 일부로 실행됩니다. *ground.collection*에 새 게임 오브젝트를 만들고, 방금 만든 Lua 스크립트 파일을 참조하는 *Script* 컴포넌트를 오브젝트에 추가합니다.

1. 컬렉션의 루트를 마우스 오른쪽 버튼으로 클릭하고 <kbd>Add Game Object</kbd>를 선택합니다. 오브젝트의 *id*를 "controller"로 설정합니다.
2. "controller" 오브젝트를 마우스 오른쪽 버튼으로 클릭하고 <kbd>Add Component from file</kbd>을 선택한 다음 *ground.script* 파일을 선택합니다.

![지면 controller](images/runner/1/ground_controller.png)

이제 게임을 실행하면 "controller" 게임 오브젝트가 *Script* 컴포넌트의 스크립트를 실행해 지면이 화면을 가로질러 부드럽게 스크롤됩니다.

## STEP 4 - 영웅 캐릭터 만들기

영웅 캐릭터는 다음 컴포넌트로 구성된 게임 오브젝트가 됩니다.

*Spine Model*
: 몸의 각 부분을 부드럽고 저렴하게 애니메이션할 수 있는 종이 인형 같은 작은 영웅 캐릭터를 제공합니다.

*Collision Object*
: 영웅 캐릭터와, 레벨에서 영웅이 달릴 수 있는 것, 위험한 것, 주울 수 있는 것 사이의 충돌을 감지합니다.

*Script*
: 사용자 입력을 획득하고 그 입력에 반응하며, 영웅 캐릭터를 점프시키고 애니메이션하고 충돌을 처리합니다.

먼저 몸 부분 이미지를 가져온 다음, *hero.atlas*라고 부를 새 아틀라스에 추가합니다.

1. *Assets pane*에서 마우스 오른쪽 버튼을 클릭하고 <kbd>New ▸ Folder</kbd>를 선택해 새 폴더를 만듭니다. 클릭하기 전에 폴더를 선택하지 않도록 주의하세요. 그렇지 않으면 새 폴더가 선택된 폴더 안에 생성됩니다. 폴더 이름은 "hero"로 지정합니다.
2. *hero* 폴더를 마우스 오른쪽 버튼으로 클릭하고 <kbd>New ▸ Atlas File</kbd>을 선택해 새 아틀라스 파일을 만듭니다. 파일 이름은 *hero.atlas*로 지정합니다.
3. *hero* 폴더 안에 새 하위 폴더 *images*를 만듭니다. *hero* 폴더를 마우스 오른쪽 버튼으로 클릭하고 <kbd>New ▸ Folder</kbd>를 선택합니다.
4. 에셋 패키지의 *hero-images* 폴더에서 몸 부분 이미지를 방금 *Assets pane*에 만든 *images* 폴더로 드래그합니다.
5. *hero.atlas*를 열고 *Outline*의 루트 노드를 마우스 오른쪽 버튼으로 클릭한 다음 <kbd>Add Images</kbd>를 선택합니다. 모든 몸 부분 이미지를 표시하고 *OK*를 클릭합니다.
6. 아틀라스 파일을 저장합니다.

![영웅 아틀라스](images/runner/2/hero_atlas.png)

Spine 애니메이션 데이터도 가져오고 이를 위한 *Spine Scene*을 설정해야 합니다.

1. *hero.spinejson* 파일(에셋 패키지에 포함되어 있음)을 *Assets pane*의 *hero* 폴더로 드래그합니다.
2. *Spine Scene* 파일을 만듭니다. *hero* 폴더를 마우스 오른쪽 버튼으로 클릭하고 <kbd>New ▸ Spine Scene File</kbd>을 선택합니다. 파일 이름은 *hero.spinescene*으로 지정합니다.
3. 새 파일을 더블 클릭해 *Spine Scene*을 열고 편집합니다.
4. *spine_json* 프로퍼티를 가져온 JSON 파일 *hero.spinejson*으로 설정합니다. 프로퍼티를 클릭한 다음 파일 선택 버튼 *...*을 클릭해 리소스 브라우저를 엽니다.
5. *atlas* 프로퍼티가 *hero.atlas* 파일을 참조하도록 설정합니다.
6. 파일을 저장합니다.

![영웅 spinescene](images/runner/2/hero_spinescene.png)

::: sidenote
*hero.spinejson* 파일은 Spine JSON 포멧으로 익스포트되었습니다. 이런 파일을 만들려면 Spine 애니메이션 소프트웨어가 필요합니다. 다른 애니메이션 소프트웨어를 사용하려면 애니메이션을 sprite-sheet로 익스포트하고 *Tile Source* 또는 *Atlas* 리소스에서 플립북 애니메이션으로 사용할 수 있습니다. 자세한 내용은 [Animation](/manuals/animation) 매뉴얼을 참고하세요.
:::

### 게임 오브젝트 구성하기

이제 영웅 게임 오브젝트를 만들기 시작할 수 있습니다.

1. 새 파일 *hero.go*를 만듭니다(*hero* 폴더를 마우스 오른쪽 버튼으로 클릭하고 <kbd>New ▸ Game Object File</kbd> 선택).
2. 게임 오브젝트 파일을 엽니다.
3. 여기에 *Spine Model* 컴포넌트를 추가합니다. (*Outline*에서 루트를 마우스 오른쪽 버튼으로 클릭하고 <kbd>Add Component</kbd>를 선택한 다음 "Spine Model"을 선택합니다.)
4. 컴포넌트의 *Spine Scene* 프로퍼티를 방금 만든 *hero.spinescene* 파일로 설정하고 기본 애니메이션으로 "run_right"를 선택합니다(애니메이션은 나중에 제대로 수정합니다).
5. 파일을 저장합니다.

![Spine Model 프로퍼티](images/runner/2/spinemodel_properties.png)

이제 충돌이 동작하도록 물리를 추가할 차례입니다.

1. 영웅 게임 오브젝트에 *Collision Object* 컴포넌트를 추가합니다. (*Outline*에서 루트를 마우스 오른쪽 버튼으로 클릭하고 <kbd>Add Component</kbd>를 선택한 다음 "Collision Object" 선택)
2. 새 컴포넌트를 마우스 오른쪽 버튼으로 클릭하고 <kbd>Add Shape</kbd>를 선택합니다. 캐릭터의 몸을 덮도록 두 개의 shape를 추가합니다. 구와 박스면 충분합니다.
3. shape를 클릭하고 *Move Tool* (<kbd>Scene ▸ Move Tool</kbd>)을 사용해 shape를 적절한 위치로 이동합니다.
4. *Collision Object* 컴포넌트를 표시하고 *Type* 프로퍼티를 "Kinematic"으로 설정합니다.

::: sidenote
"Kinematic" 충돌은 충돌은 등록하되, 물리 엔진이 충돌을 자동으로 해결하거나 오브젝트를 시뮬레이션하지 않기를 원한다는 뜻입니다. 물리 엔진은 여러 가지 충돌 오브젝트 타입을 지원합니다. 이에 대해서는 [Physics documentation](/manuals/physics)에서 더 자세히 읽을 수 있습니다.
:::

충돌 오브젝트가 무엇과 상호작용해야 하는지 지정하는 것이 중요합니다.

1. *Group* 프로퍼티를 "hero"라는 새 충돌 그룹으로 설정합니다.
2. *Mask* 프로퍼티를 이 충돌 오브젝트가 충돌을 등록해야 하는 다른 그룹 "geometry"로 설정합니다. "geometry" 그룹은 아직 존재하지 않지만 곧 여기에 속한 충돌 오브젝트를 추가할 것입니다.

마지막으로 새 *hero.script* 파일을 만들고 게임 오브젝트에 추가합니다.

1. *Assets pane*에서 *hero* 폴더를 마우스 오른쪽 버튼으로 클릭하고 <kbd>New ▸ Script File</kbd>을 선택합니다. 새 파일 이름은 *hero.script*로 지정합니다.
2. 새 파일을 연 다음, 다음 코드를 스크립트 파일에 복사해 붙여넣고 저장합니다. (코드는 영웅 충돌 shape를 충돌 대상에서 분리하는 solver를 제외하면 꽤 단순합니다. 이 처리는 `handle_geometry_contact()` 함수가 수행합니다.)

![영웅 게임 오브젝트](images/runner/2/hero_game_object.png)

::: sidenote
충돌을 직접 처리하는 이유는 캐릭터의 충돌 오브젝트 타입을 dynamic으로 설정하면 엔진이 관련 body에 대해 뉴턴식 시뮬레이션을 수행하기 때문입니다. 이런 게임에서는 그런 시뮬레이션이 전혀 최적이 아니므로, 다양한 힘으로 물리 엔진과 씨름하는 대신 완전히 직접 제어합니다.

이렇게 하고 충돌을 제대로 처리하려면 약간의 벡터 수학이 필요합니다. kinematic 충돌을 해결하는 방법에 대한 자세한 설명은 [Physics documentation](/manuals/physics-resolving-collisions/)에 있습니다.
:::

```lua
-- 픽셀 단위/sˆ2로 플레이어를 아래로 당기는 중력
local gravity = -20

-- 픽셀 단위/s의 점프 이륙 속도
local jump_takeoff_speed = 900

function init(self)
    -- 이 스크립트의 on_input()으로 입력을 보내도록 엔진에 알립니다
    msg.post(".", "acquire_input_focus")

    -- 시작 위치를 저장합니다
    self.position = go.get_position()

    -- 이동 벡터와 지면 접촉 여부를 추적합니다
    self.velocity = vmath.vector3(0, 0, 0)
    self.ground_contact = false
end

function final(self)
    -- 오브젝트가 삭제될 때 입력 포커스를 반환합니다
    msg.post(".", "release_input_focus")
end

function update(self, dt)
    local gravity = vmath.vector3(0, gravity, 0)

    if not self.ground_contact then
        -- 지면 접촉이 없으면 중력을 적용합니다
        self.velocity = self.velocity + gravity
    end

    -- 플레이어 캐릭터에 velocity를 적용합니다
    go.set_position(go.get_position() + self.velocity * dt)

    -- volatile 상태를 재설정합니다
    self.correction = vmath.vector3()
    self.ground_contact = false
end

local function handle_geometry_contact(self, normal, distance)
    -- correction 벡터를 contact normal에 투영합니다
    -- (첫 contact point에서는 correction 벡터가 0-vector입니다)
    local proj = vmath.dot(self.correction, normal)
    -- 이 contact point에 필요한 보정값을 계산합니다
    local comp = (distance - proj) * normal
    -- correction 벡터에 더합니다
    self.correction = self.correction + comp
    -- 플레이어 캐릭터에 보정을 적용합니다
    go.set_position(go.get_position() + comp)
    -- normal이 충분히 위쪽을 향하는지 확인해 플레이어가 지면에 서 있는 것으로 간주합니다
    -- (0.7은 순수 수직 방향에서 약 45도 벗어난 값과 거의 같습니다)
    if normal.y > 0.7 then
        self.ground_contact = true
    end
    -- velocity를 normal에 투영합니다
    proj = vmath.dot(self.velocity, normal)
    -- 투영값이 음수이면 velocity의 일부가 contact point를 향한다는 뜻입니다
    if proj < 0 then
        -- 그 경우 해당 컴포넌트를 제거합니다
        self.velocity = self.velocity - proj * normal
    end
end

function on_message(self, message_id, message, sender)
    if message_id == hash("contact_point_response") then
        -- contact point 메세지를 받았는지 확인합니다. contact point마다 하나의 메세지가 옵니다
        if message.group == hash("geometry") then
            handle_geometry_contact(self, message.normal, message.distance)
        end
    end
end

local function jump(self)
    -- 지면에서만 점프를 허용합니다
    if self.ground_contact then
        -- 이륙 속도를 설정합니다
        self.velocity.y = jump_takeoff_speed
    end
end

local function abort_jump(self)
    -- 아직 상승 중이면 점프를 짧게 끊습니다
    if self.velocity.y > 0 then
        -- 위쪽 속도를 줄입니다
        self.velocity.y = self.velocity.y * 0.5
    end
end

function on_input(self, action_id, action)
    if action_id == hash("jump") or action_id == hash("touch") then
        if action.pressed then
            jump(self)
        elseif action.released then
            abort_jump(self)
        end
    end
end
```

1. 스크립트를 영웅 오브젝트에 *Script* 컴포넌트로 추가합니다(*Outline*에서 *hero.go*의 루트를 마우스 오른쪽 버튼으로 클릭하고 <kbd>Add Component from File</kbd>을 선택한 다음 *hero.script* 파일 선택).

원한다면 이제 영웅 캐릭터를 main 컬렉션에 임시로 추가하고 게임을 실행해, 캐릭터가 월드 아래로 떨어지는 것을 볼 수 있습니다.

영웅이 기능하려면 마지막으로 입력이 필요합니다. 위 스크립트에는 이미 "jump"와 "touch"(터치 스크린용) 동작에 반응하는 `on_input()` 함수가 들어 있습니다. 이 동작에 대한 입력 바인딩을 추가해 보겠습니다.

1. "input/game.input_bindings"를 엽니다.
2. "KEY_SPACE"에 대한 key trigger를 추가하고 action 이름을 "jump"로 지정합니다.
3. "TOUCH_MULTI"에 대한 touch trigger를 추가하고 action 이름을 "touch"로 지정합니다. (action 이름은 임의이지만 스크립트의 이름과 일치해야 합니다. 여러 트리거에 같은 action 이름을 사용할 수는 없다는 점에 유의하세요.)
4. 파일을 저장합니다.

![입력 바인딩](images/runner/2/input_bindings.png)

## STEP 5 - 레벨 리팩터링

이제 충돌을 포함한 영웅 캐릭터 설정이 끝났으므로, 영웅 캐릭터가 충돌하거나 달릴 대상이 생기도록 지면에도 충돌을 추가해야 합니다. 곧 그렇게 하겠지만, 먼저 약간의 리팩터링을 통해 모든 레벨 관련 항목을 별도 컬렉션에 넣고 파일 구조를 조금 정리하겠습니다.

1. 새 *level.collection* 파일을 만듭니다(*Assets pane*에서 *main*을 마우스 오른쪽 버튼으로 클릭하고 <kbd>New ▸ Collection File</kbd> 선택).
2. 새 파일을 열고 *Outline*에서 루트를 마우스 오른쪽 버튼으로 클릭한 뒤 <kbd>Add Collection from File</kbd>을 선택하고 *ground.collection*을 고릅니다.
3. *level.collection*에서 *Outline*의 루트를 마우스 오른쪽 버튼으로 클릭하고 <kbd>Add Game Object File</kbd>을 선택한 다음 *hero.go*를 고릅니다.
4. 이제 프로젝트 루트에 *level*이라는 새 폴더를 만듭니다(*game.project* 아래의 빈 공간을 마우스 오른쪽 버튼으로 클릭하고 <kbd>New ▸ Folder</kbd> 선택). 그런 다음 지금까지 만든 레벨 에셋을 그곳으로 옮깁니다. *level.collection*, *level.atlas*, 레벨 아틀라스용 이미지를 담은 "images" 폴더, *ground.collection*, *ground.script* 파일입니다.
5. *main.collection*을 열고 *ground.collection*을 삭제한 뒤, 이제 *ground.collection*을 포함하고 있는 *level.collection*을 대신 추가합니다(마우스 오른쪽 버튼 클릭 후 <kbd>Add Collection from File</kbd>). 컬렉션을 0, 0, 0 위치에 배치했는지 확인합니다.

::: sidenote
지금쯤 알아차렸겠지만 *Assets pane*에 보이는 파일 계층구조는 컬렉션에서 만드는 컨텐츠 구조와 분리되어 있습니다. 개별 파일은 컬렉션 파일과 게임 오브젝트 파일에서 참조되지만, 파일의 위치는 완전히 임의입니다.

파일을 새 위치로 옮기고 싶다면 Defold가 해당 파일에 대한 참조를 자동으로 업데이트해 도와줍니다(리팩터링). 게임처럼 복잡한 소프트웨어를 만들 때, 프로젝트가 성장하고 변경됨에 따라 구조를 바꿀 수 있다는 것은 매우 유용합니다. Defold는 이를 권장하며 프로세스를 매끄럽게 만들어 주므로 파일을 옮기는 것을 두려워하지 마세요!
:::

레벨 컬렉션에 스크립트 컴포넌트가 있는 controller 게임 오브젝트도 추가해야 합니다.

1. 새 스크립트 파일을 만듭니다. *Assets pane*에서 *level* 폴더를 마우스 오른쪽 버튼으로 클릭하고 <kbd>New ▸ Script File</kbd>을 선택합니다. 파일 이름은 *controller.script*로 지정합니다.
2. 스크립트 파일을 열고 다음 코드를 복사해 넣은 뒤 파일을 저장합니다.

    ```lua
    -- controller.script
    go.property("speed", 360) -- <1>

    function init(self)
        msg.post("ground/controller#ground", "set_speed", { speed = self.speed })
    end
    ```
    1. 이것은 스크립트 프로퍼티입니다. 기본값으로 설정하지만, 배치된 스크립트 인스턴스는 에디터의 Properties 뷰에서 이 값을 직접 오버라이드할 수 있습니다.

3. *level.collection* 파일을 엽니다.
4. *Outline*에서 루트를 마우스 오른쪽 버튼으로 클릭하고 <kbd>Add Game Object</kbd>를 선택합니다.
5. *Id*를 "controller"로 설정합니다.
6. *Outline*에서 "controller" 게임 오브젝트를 마우스 오른쪽 버튼으로 클릭하고 <kbd>Add Component from File</kbd>을 선택한 다음 *level* 폴더의 *controller.script* 파일을 선택합니다.
7. 파일을 저장합니다.

![스크립트 프로퍼티](images/runner/2/script_property.png)

::: sidenote
"controller" 게임 오브젝트는 파일에 존재하지 않고 레벨 컬렉션 안에 내장(in-place)으로 생성됩니다. 즉, 게임 오브젝트 인스턴스는 내장 데이터에서 생성됩니다. 이런 단일 목적 게임 오브젝트에는 괜찮은 방식입니다. 어떤 게임 오브젝트의 여러 인스턴스가 필요하고 각 인스턴스를 만드는 데 사용되는 프로토타입/템플릿을 수정할 수 있기를 원한다면, 게임 오브젝트 파일을 만들고 그 파일에서 게임 오브젝트를 컬렉션에 추가하면 됩니다. 그러면 파일을 프로토타입/템플릿으로 참조하는 게임 오브젝트가 만들어집니다.

이 "controller" 게임 오브젝트의 목적은 실행 중인 레벨과 관련된 모든 것을 제어하는 것입니다. 곧 이 스크립트가 영웅이 상호작용할 플랫폼과 코인을 스폰하는 역할을 맡겠지만, 지금은 레벨의 속도만 설정합니다.
:::

레벨 controller 스크립트의 `init()` 함수에서는 id로 주소가 지정된 지면 controller 오브젝트의 스크립트 컴포넌트에 메세지를 보냅니다.

```lua
msg.post("ground/controller#controller", "set_speed", { speed = self.speed })
```

controller 게임 오브젝트는 "ground" 컬렉션 안에 있으므로 id는 `"ground/controller"`로 설정됩니다. 그런 다음 오브젝트 id와 컴포넌트 id를 구분하는 해쉬 문자 `"#"` 뒤에 컴포넌트 id `"controller"`를 추가합니다. 지면 스크립트에는 아직 `set_speed` 메세지에 반응하는 코드가 없으므로 *ground.script*에 `on_message()` 함수를 추가하고 이에 대한 로직을 넣어야 합니다.

1. *ground.script*를 엽니다.
2. 다음 코드를 추가하고 파일을 저장합니다.

```lua
-- ground.script
function on_message(self, message_id, message, sender)
    if message_id == hash("set_speed") then -- <1>
        self.speed = message.speed -- <2>
    end
end
```
1. 모든 메세지는 보낼 때 내부적으로 해쉬되며 해쉬된 값과 비교해야 합니다.
2. 메세지 데이터는 메세지와 함께 전송되는 데이터를 담은 Lua 테이블입니다.

![지면 코드 추가](images/runner/insert_ground_code.png)

## STEP 6 - 지면 물리와 플랫폼

이제 지면에 물리 충돌을 추가해야 합니다.

1. *ground.collection* 파일을 엽니다.
2. 적절한 게임 오브젝트에 새 *Collision Object* 컴포넌트를 추가합니다. 지면 스크립트는 충돌에 반응하지 않으므로(그 모든 로직은 영웅 스크립트에 있습니다), 어떤 _정지_ 게임 오브젝트에 넣어도 됩니다(지면 타일 오브젝트는 정지 상태가 아니므로 피하세요). 좋은 후보는 "controller" 게임 오브젝트지만, 원한다면 별도 오브젝트를 만들어도 됩니다. 게임 오브젝트를 마우스 오른쪽 버튼으로 클릭하고 <kbd>Add Component</kbd>를 선택한 다음 *Collision Object*를 선택합니다.
3. *Collision Object* 컴포넌트를 마우스 오른쪽 버튼으로 클릭하고 <kbd>Add Shape</kbd>를 선택한 다음 *Box*를 선택해 box shape를 추가합니다.
4. *Move Tool*과 *Scale Tool* (<kbd>Scene ▸ Move Tool</kbd> 및 <kbd>Scene ▸ Scale Tool</kbd>)을 사용해 박스가 모든 지면 타일을 덮도록 만듭니다.
5. 지면 물리는 움직이지 않을 것이므로 충돌 오브젝트의 *Type* 프로퍼티를 "Static"으로 설정합니다.
6. 충돌 오브젝트의 *Group* 프로퍼티를 "geometry"로, *Mask*를 "hero"로 설정합니다. 이제 영웅의 충돌 오브젝트와 이 오브젝트 사이의 충돌이 등록됩니다.
7. 파일을 저장합니다.

![지면 충돌](images/runner/2/ground_collision.png)

이제 게임을 실행해 볼 수 있습니다(<kbd>Project ▸ Build</kbd>). 영웅 캐릭터가 지면 위를 달려야 하며 <kbd>Space</kbd> 버튼으로 점프할 수 있어야 합니다. 모바일 기기에서 게임을 실행하면 화면을 탭해 점프할 수 있습니다.

게임 월드의 삶을 조금 덜 지루하게 만들기 위해 점프해서 올라갈 플랫폼을 추가하겠습니다.

1. 에셋 패키지에서 *rock_planks.png* 이미지 파일을 *level/images* 하위 폴더로 드래그합니다.
2. *level.atlas*를 열고 새 이미지를 아틀라스에 추가합니다(*Outline*에서 루트를 마우스 오른쪽 버튼으로 클릭하고 <kbd>Add Images</kbd> 선택).
3. 파일을 저장합니다.
4. *level* 폴더에 *platform.go*라는 새 *Game Object* 파일을 만듭니다. (*Assets pane*에서 *level*을 마우스 오른쪽 버튼으로 클릭한 다음 <kbd>New ▸ Game Object File</kbd> 선택.)
5. 게임 오브젝트에 *Sprite* 컴포넌트를 추가합니다(*Outline* 뷰에서 루트를 마우스 오른쪽 버튼으로 클릭하고 <kbd>Add Component</kbd>를 선택한 다음 *Sprite* 선택).
6. *Image* 프로퍼티가 *level.atlas* 파일을 참조하도록 설정하고 *Default Animation*을 "rock_planks"로 설정합니다. 편의를 위해 레벨 오브젝트는 "level/objects" 하위 폴더에 둡니다.
7. 플랫폼 게임 오브젝트에 *Collision Object* 컴포넌트를 추가합니다(*Outline* 뷰에서 루트를 마우스 오른쪽 버튼으로 클릭하고 <kbd>Add Component</kbd> 선택).
8. 컴포넌트의 *Type*을 "Kinematic"으로 설정하고, *Group*과 *Mask*를 각각 "geometry"와 "hero"로 설정합니다.
9. *Collision Object* 컴포넌트에 *Box Shape*를 추가합니다. (*Outline*에서 컴포넌트를 마우스 오른쪽 버튼으로 클릭하고 <kbd>Add Shape</kbd>를 선택한 다음 *Box* 선택).
10. *Move Tool*과 *Scale Tool* (<kbd>Scene ▸ Move Tool</kbd> 및 <kbd>Scene ▸ Scale Tool</kbd>)을 사용해 *Collision Object* 컴포넌트의 shape가 플랫폼을 덮도록 만듭니다.
11. *Script* 파일 *platform.script*를 만들고(*Assets pane*에서 마우스 오른쪽 버튼을 클릭한 다음 <kbd>New ▸ Script File</kbd> 선택), 다음 코드를 파일에 넣은 뒤 저장합니다.

    ```lua
    -- platform.script
    function init(self)
        self.speed = 540      -- 픽셀/s 단위 기본 속도
    end

    function update(self, dt)
        local pos = go.get_position()
        if pos.x < -500 then
            go.delete() -- <1>
        end
        pos.x = pos.x - self.speed * dt
        go.set_position(pos)
    end

    function on_message(self, message_id, message, sender)
        if message_id == hash("set_speed") then
            self.speed = message.speed
        end
    end
    ```
    1. 플랫폼이 화면의 오른쪽 가장자리 밖으로 이동했을 때 그냥 삭제합니다.

12. *platform.go*를 열고 새 스크립트를 컴포넌트로 추가합니다(*Outline* 뷰에서 루트를 마우스 오른쪽 버튼으로 클릭하고 <kbd>Add Component From File</kbd>을 선택한 다음 *platform.script* 선택).
13. *platform.go*를 새 파일로 복사하고(*Assets pane*에서 파일을 마우스 오른쪽 버튼으로 클릭해 <kbd>Copy</kbd>를 선택한 다음 다시 마우스 오른쪽 버튼으로 클릭하고 <kbd>Paste</kbd> 선택), 새 파일 이름을 *platform_long.go*로 지정합니다.
14. *platform_long.go*를 열고 두 번째 *Sprite* 컴포넌트를 추가합니다(*Outline* 뷰에서 루트를 마우스 오른쪽 버튼으로 클릭하고 <kbd>Add Component</kbd> 선택). 또는 기존 *Sprite*를 복사해도 됩니다.
15. *Move Tool* (<kbd>Scene ▸ Move Tool</kbd>)을 사용해 *Sprite* 컴포넌트들을 나란히 배치합니다.
16. *Move Tool*과 *Scale Tool*을 사용해 *Collision Object* 컴포넌트의 shape가 두 플랫폼을 모두 덮도록 만듭니다.

![플랫폼](images/runner/2/platform_long.png)

::: sidenote
*platform.go*와 *platform_long.go* 둘 다 같은 스크립트 파일을 참조하는 *Script* 컴포넌트를 가지고 있다는 점에 유의하세요. 이는 좋은 방식입니다. 스크립트 파일에 대한 모든 변경사항이 일반 플랫폼과 긴 플랫폼 모두의 동작에 영향을 주기 때문입니다.
:::

## 플랫폼 스폰하기

게임의 아이디어는 단순한 엔드리스 러너를 만드는 것입니다. 이는 플랫폼 게임 오브젝트를 에디터의 컬렉션에 배치할 수 없다는 뜻입니다. 대신 동적으로 스폰해야 합니다.

1. *level.collection*을 엽니다.
2. "controller" 게임 오브젝트에 *Factory* 컴포넌트 두 개를 추가합니다(마우스 오른쪽 버튼으로 클릭하고 <kbd>Add Component</kbd>를 선택한 다음 *Factory* 선택).
3. 컴포넌트의 *Id* 프로퍼티를 "platform_factory"와 "platform_long_factory"로 설정합니다.
4. "platform_factory"의 *Prototype* 프로퍼티를 */level/objects/platform.go* 파일로 설정합니다.
5. "platform_long_factory"의 *Prototype* 프로퍼티를 */level/objects/platform_long.go* 파일로 설정합니다.
6. 파일을 저장합니다.
7. 레벨을 관리하는 *controller.script* 파일을 엽니다.
8. 스크립트가 다음 내용을 포함하도록 수정한 다음 파일을 저장합니다.

```lua
-- controller.script
go.property("speed", 360)

local grid = 460
local platform_heights = { 100, 200, 350 } -- <1>

function init(self)
    msg.post("ground/controller#controller", "set_speed", { speed = self.speed })
    self.gridw = 0
end

function update(self, dt) -- <2>
    self.gridw = self.gridw + self.speed * dt

    if self.gridw >= grid then
        self.gridw = 0

        -- 무작위 높이에 플랫폼을 스폰할 수도 있습니다
        if math.random() > 0.2 then
            local h = platform_heights[math.random(#platform_heights)]
            local f = "#platform_factory"
            if math.random() > 0.5 then
                f = "#platform_long_factory"
            end

            local p = factory.create(f, vmath.vector3(1600, h, 0), nil, {}, 0.6)
            msg.post(p, "set_speed", { speed = self.speed })
        end
    end
end
```
1. 플랫폼을 스폰할 Y 포지션의 미리 정의된 값입니다.
2. `update()` 함수는 매 프레임 한 번 호출되며, 이를 사용해 특정 간격(겹침 방지)과 높이에서 일반 플랫폼 또는 긴 플랫폼을 스폰할지 결정합니다. 다양한 스폰 알고리즘을 실험해 서로 다른 게임플레이를 만들기 쉽습니다.

이제 게임을 실행합니다(<kbd>Project ▸ Build</kbd>).

와, 이제 (거의) 플레이 가능한 무언가로 바뀌기 시작했습니다...

![게임 실행](images/runner/2/run_game.png)

## STEP 7 - 애니메이션과 사망

먼저 영웅 캐릭터에 생동감을 불어넣겠습니다. 지금은 불쌍한 캐릭터가 달리기 루프에 갇혀 있고 점프나 다른 동작에 제대로 반응하지 않습니다. 에셋 패키지에서 추가한 Spine 파일에는 바로 이 목적을 위한 애니메이션 세트가 실제로 들어 있습니다.

1. *hero.script* 파일을 열고 기존 `update()` 함수 _앞에_ 다음 함수를 추가합니다.

```lua
    -- hero.script
    local function play_animation(self, anim)
        -- 이미 재생 중이 아닌 애니메이션만 재생합니다
        if self.anim ~= anim then
            -- Spine Model에 애니메이션을 재생하라고 알립니다
            local anim_props = { blend_duration = 0.15 }
            spine.play_anim("#spinemodel", anim, go.PLAYBACK_LOOP_FORWARD, anim_props)
            -- 어떤 애니메이션이 재생 중인지 기억합니다
            self.anim = anim
        end
    end

    local function update_animation(self)
        -- 올바른 애니메이션이 재생되고 있는지 확인합니다
        if self.ground_contact then
            play_animation(self, hash("run"))
        else
            play_animation(self, hash("jump"))

        end
    end
```

2. `update()` 함수를 찾아 `update_animation` 호출을 추가합니다.

```lua
    ...
    -- 플레이어 캐릭터에 적용합니다
    go.set_position(go.get_position() + self.velocity * dt)

    update_animation(self)
    ...
  ```

![영웅 코드 삽입](images/runner/insert_hero_code.png)

::: sidenote
Lua에는 로컬 변수에 대한 "lexical scope"가 있으며 `local` 함수를 배치하는 순서에 민감합니다. `update()` 함수가 로컬 함수 `update_animation()`과 `play_animation()`을 호출하므로, 런타임은 이를 호출할 수 있으려면 먼저 로컬 함수를 보았어야 합니다. 그래서 이 함수들을 `update()` 앞에 둬야 합니다. 함수 순서를 바꾸면 오류가 발생합니다. 이는 `local` 변수에만 적용된다는 점에 유의하세요. Lua의 스코프 규칙과 로컬 함수에 대해서는 http://www.lua.org/pil/6.2.html 에서 더 읽을 수 있습니다.
:::

영웅에 점프와 낙하 애니메이션을 추가하는 데 필요한 것은 이것뿐입니다. 게임을 실행하면 플레이 감각이 훨씬 좋아졌다는 것을 알 수 있습니다. 플랫폼이 안타깝게도 영웅을 화면 밖으로 밀어낼 수 있다는 것도 알아차릴 수 있습니다. 이것은 충돌 처리의 부작용이지만 해결책은 쉽습니다. 폭력을 더하고 플랫폼 가장자리를 위험하게 만들면 됩니다!

1. 에셋 패키지에서 *spikes.png*를 *Assets pane*의 "level/images" 폴더로 드래그합니다.
2. *level.atlas*를 열고 이미지를 추가합니다(마우스 오른쪽 버튼을 클릭하고 <kbd>Add Images</kbd> 선택).
3. *platform.go*를 열고 몇 개의 *Sprite* 컴포넌트를 추가합니다. *Image*를 *level.atlas*로, *Default Animation*을 "spikes"로 설정합니다.
4. *Move Tool*과 *Rotate Tool*을 사용해 플랫폼 가장자리를 따라 가시를 배치합니다.
5. 가시가 플랫폼 뒤에 렌더링되도록 가시 스프라이트의 *Z* 포지션을 -0.1로 설정합니다.
6. 플랫폼에 새 *Collision Object* 컴포넌트를 추가합니다(*Outline*에서 루트를 마우스 오른쪽 버튼으로 클릭하고 <kbd>Add Component</kbd> 선택). *Group* 프로퍼티를 "danger"로 설정합니다. *Mask*도 "hero"로 설정합니다.
7. *Collision Object*에 box shape를 추가하고(마우스 오른쪽 버튼 클릭 후 <kbd>Add Shape</kbd> 선택), *Move Tool* (<kbd>Scene ▸ Move Tool</kbd>)과 *Scale Tool*을 사용해 영웅 캐릭터가 옆이나 아래에서 플랫폼에 부딪힐 때 "danger" 오브젝트와 충돌하도록 shape를 배치합니다.
8. 파일을 저장합니다.

    ![플랫폼 가시](images/runner/3/danger_edges.png)

9. *hero.go*를 열고 *Collision Object*를 표시한 다음 *Mask* 프로퍼티에 "danger" 이름을 추가합니다. 그런 다음 파일을 저장합니다.

    ![영웅 충돌](images/runner/3/hero_collision.png)

10. *hero.script*를 열고, 영웅 캐릭터가 "danger" 가장자리와 충돌하면 반응하도록 `on_message()` 함수를 변경합니다.

    ```lua
    -- hero.script
    function on_message(self, message_id, message, sender)
        if message_id == hash("reset") then
            self.velocity = vmath.vector3(0, 0, 0)
            self.correction = vmath.vector3()
            self.ground_contact = false
            self.anim = nil
            go.set(".", "euler.z", 0)
            go.set_position(self.position)
            msg.post("#collisionobject", "enable")

        elseif message_id == hash("contact_point_response") then
            -- contact point 메세지를 받았는지 확인합니다
            if message.group == hash("danger") then
                -- 죽고 다시 시작합니다
                play_animation(self, hash("death"))
                msg.post("#collisionobject", "disable")
                -- <1>
                go.animate(".", "euler.z", go.PLAYBACK_ONCE_FORWARD, 160, go.EASING_LINEAR, 0.7)
                go.animate(".", "position.y", go.PLAYBACK_ONCE_FORWARD, go.get_position().y - 200, go.EASING_INSINE, 0.5, 0.2,
                    function()
                        msg.post("#", "reset")
                    end)
            elseif message.group == hash("geometry") then
                handle_geometry_contact(self, message.normal, message.distance)
            end
        end
    end
    ```
    1. 영웅이 죽을 때 회전과 낙하 움직임을 추가합니다. 훨씬 더 개선할 수 있습니다!

11. 오브젝트를 초기화하도록 "reset" 메세지를 보내게 `init()` 함수를 변경한 다음 파일을 저장합니다.

    ```lua
    -- hero.script
    function init(self)
        -- 이 스크립트에서 입력을 처리할 수 있게 합니다
        msg.post(".", "acquire_input_focus")
        -- 위치를 저장합니다
        self.position = go.get_position()
        msg.post("#", "reset")
    end
    ```

## STEP 8 - 레벨 재설정

이제 게임을 시도해 보면 reset 메커니즘이 동작하지 않는다는 점이 금방 드러납니다. 영웅 reset 자체는 괜찮지만, reset 직후 플랫폼 가장자리로 곧바로 떨어져 다시 죽는 상황이 쉽게 생깁니다. 원하는 것은 사망 시 전체 레벨을 제대로 reset하는 것입니다. 레벨은 스폰된 플랫폼들의 연속일 뿐이므로, 모든 스폰된 플랫폼을 추적한 다음 reset 때 삭제하기만 하면 됩니다.

1. *controller.script* 파일을 열고 모든 스폰된 플랫폼의 id를 저장하도록 코드를 편집합니다.

    ```lua
    -- controller.script
    go.property("speed", 360)

    local grid = 460
    local platform_heights = { 100, 200, 350 }

    function init(self)
        msg.post("ground/controller#controller", "set_speed", { speed = self.speed })
        self.gridw = 0
        self.spawns = {} -- <1>
    end

    function update(self, dt)
        self.gridw = self.gridw + self.speed * dt

        if self.gridw >= grid then
            self.gridw = 0

            -- 무작위 높이에 플랫폼을 스폰할 수도 있습니다
            if math.random() > 0.2 then
                local h = platform_heights[math.random(#platform_heights)]
                local f = "#platform_factory"
                if math.random() > 0.5 then
                    f = "#platform_long_factory"
                end

                local p = factory.create(f, vmath.vector3(1600, h, 0), nil, {}, 0.6)
                msg.post(p, "set_speed", { speed = self.speed })
                table.insert(self.spawns, p) -- <1>
            end
        end
    end

    function on_message(self, message_id, message, sender)
        if message_id == hash("reset") then -- <2>
            -- 영웅에게 reset하라고 알립니다.
            msg.post("hero#hero", "reset")
            -- 모든 플랫폼을 삭제합니다
            for i,p in ipairs(self.spawns) do
                go.delete(p)
            end
            self.spawns = {}
        elseif message_id == hash("delete_spawn") then -- <3>
            for i,p in ipairs(self.spawns) do
                if p == message.id then
                    table.remove(self.spawns, i)
                    go.delete(p)
                end
            end
        end
    end
    ```
    1. 테이블을 사용해 모든 스폰된 플랫폼을 저장합니다.
    2. "reset" 메세지는 테이블에 저장된 모든 플랫폼을 삭제합니다.
    3. "delete_spawn" 메세지는 특정 플랫폼을 삭제하고 테이블에서 제거합니다.

2. 파일을 저장합니다.
3. *platform.script*를 열고 가장 왼쪽 가장자리에 도달한 플랫폼을 그냥 삭제하는 대신, 레벨 controller에 플랫폼 제거를 요청하는 메세지를 보내도록 수정합니다.

    ```lua
    -- platform.script
    ...
    if pos.x < -500 then
        msg.post("/level/controller#controller", "delete_spawn", { id = go.get_id() })
    end
    ...
    ```

    ![플랫폼 코드 삽입](images/runner/insert_platform_code.png)

4. 파일을 저장합니다.
5. *hero.script*를 엽니다. 이제 마지막으로 해야 할 일은 레벨에 reset을 수행하라고 알리는 것입니다. 영웅에게 reset을 요청하는 메세지를 레벨 controller 스크립트로 옮겼습니다. reset 제어를 이렇게 중앙화하면, 예를 들어 더 긴 시간의 사망 시퀀스를 더 쉽게 도입할 수 있으므로 합리적입니다.

```lua
-- hero.script
...
go.animate(".", "position.y", go.PLAYBACK_ONCE_FORWARD, go.get_position().y - 200, go.EASING_INSINE, 0.5, 0.2,
    function()
        msg.post("controller#controller", "reset")
    end)
...
```

![영웅 코드 삽입](images/runner/insert_hero_code_2.png)

이제 기본적인 restart-die 루프가 준비되었습니다!

다음은 살아갈 이유가 될 무언가, 코인입니다!

## STEP 9 - 수집할 코인

아이디어는 플레이어가 수집할 코인을 레벨에 넣는 것입니다. 먼저 물어볼 질문은 이를 레벨에 어떻게 배치할 것인가입니다. 예를 들어 플랫폼 스폰 알고리즘과 어느 정도 맞물리는 스폰 방식을 개발할 수도 있습니다. 하지만 결국 훨씬 쉬운 접근을 선택해 플랫폼 자체가 코인을 스폰하게 했습니다.

1. 에셋 패키지에서 *coin.png* 이미지를 *Assets pane*의 "level/images"로 드래그합니다.
2. *level.atlas*를 열고 이미지를 추가합니다(마우스 오른쪽 버튼을 클릭하고 <kbd>Add Images</kbd> 선택).
3. *level* 폴더에 *coin.go*라는 *Game Object* 파일을 만듭니다(*Assets pane*에서 *level*을 마우스 오른쪽 버튼으로 클릭하고 <kbd>New ▸ Game Object File</kbd> 선택).
4. *coin.go*를 열고 *Sprite* 컴포넌트를 추가합니다(*Outline*에서 마우스 오른쪽 버튼을 클릭하고 <kbd>Add Component</kbd> 선택). *Image*를 *level.atlas*로, *Default Animation*을 "coin"으로 설정합니다.
5. *Collision Object*를 추가하고(*Outline*에서 마우스 오른쪽 버튼을 클릭하고 <kbd>Add Component</kbd> 선택)
이미지를 덮는 *Sphere* shape를 추가합니다(컴포넌트를 마우스 오른쪽 버튼으로 클릭하고 <kbd>Add Shape</kbd> 선택).
6. *Move Tool* (<kbd>Scene ▸ Move Tool</kbd>)과 *Scale Tool*을 사용해 구가 코인 이미지를 덮도록 만듭니다.
7. 충돌 오브젝트 *Type*을 "Kinematic"으로, *Group*을 "pickup"으로, *Mask*를 "hero"로 설정합니다.
8. *hero.go*를 열고 *Collision Object* 컴포넌트의 *Mask* 프로퍼티에 "pickup"을 추가한 다음 파일을 저장합니다.
9. 새 스크립트 파일 *coin.script*를 만듭니다(*Assets pane*에서 *level*을 마우스 오른쪽 버튼으로 클릭하고 <kbd>New ▸ Script File</kbd> 선택). 템플릿 코드를 다음으로 교체합니다.

    ```lua
    -- coin.script
    function init(self)
        self.collected = false
    end

    function on_message(self, message_id, message, sender)
        if self.collected == false and message_id == hash("collision_response") then
            self.collected = true
            msg.post("#sprite", "disable")
        elseif message_id == hash("start_animation") then
            pos = go.get_position()
            go.animate(go.get_id(), "position.y", go.PLAYBACK_LOOP_PINGPONG, pos.y + 24, go.EASING_INOUTSINE, 0.75, message.delay)
        end
    end
    ```

10. 스크립트 파일을 코인 오브젝트에 *Script* 컴포넌트로 추가합니다(*Outline*의 루트를 마우스 오른쪽 버튼으로 클릭하고 <kbd>Add Component from File</kbd> 선택).

    ![코인 게임 오브젝트](images/runner/3/coin.png)

계획은 플랫폼 오브젝트에서 코인을 스폰하는 것이므로 *platform.go*와 *platform_long.go*에 코인용 팩토리를 넣습니다.

1. *platform.go*를 열고 *Factory* 컴포넌트를 추가합니다(*Outline*에서 마우스 오른쪽 버튼을 클릭하고 <kbd>Add Component</kbd> 선택).
2. *Factory*의 *Id*를 "coin_factory"로 설정하고 *Prototype*을 *coin.go* 파일로 설정합니다.
3. 이제 *platform_long.go*를 열고 동일한 *Factory* 컴포넌트를 만듭니다.
4. 두 파일을 저장합니다.

![코인 팩토리](images/runner/3/coin_factory.png)

이제 코인을 스폰하고 삭제하도록 *platform.script*를 수정해야 합니다.

```lua
-- platform.script
function init(self)
    self.speed = 540     -- 픽셀/s 단위 기본 속도
    self.coins = {}
end

function final(self)
    for i,p in ipairs(self.coins) do
        go.delete(p)
    end
end

function update(self, dt)
    local pos = go.get_position()
    if pos.x < -500 then
        msg.post("/level/controller#controller", "delete_spawn", { id = go.get_id() })
    end
    pos.x = pos.x - self.speed * dt
    go.set_position(pos)
end

function create_coins(self, params)
    local spacing = 56
    local pos = go.get_position()
    local x = pos.x - params.coins * (spacing*0.5) - 24
    for i = 1, params.coins do
        local coin = factory.create("#coin_factory", vmath.vector3(x + i * spacing , pos.y + 64, 1))
        msg.post(coin, "set_parent", { parent_id = go.get_id() }) -- <1>
        msg.post(coin, "start_animation", { delay = i/10 }) -- <2>
        table.insert(self.coins, coin)
    end
end

function on_message(self, message_id, message, sender)
    if message_id == hash("set_speed") then
        self.speed = message.speed
    elseif message_id == hash("create_coins") then
        create_coins(self, message)
    end
end
```
1. 스폰된 코인의 부모를 플랫폼으로 설정하면 코인이 플랫폼과 함께 이동합니다.
2. 애니메이션은 이제 코인의 부모가 된 플랫폼을 기준으로 코인이 위아래로 춤추게 만듭니다.

::: sidenote
부모-자식 관계는 엄밀히 말하면 _씬 그래프_의 수정입니다. 자식은 부모와 함께 변형(이동, 스케일, 회전)됩니다. 게임 오브젝트 사이에 추가적인 "ownership" 관계가 필요하다면 코드에서 그것을 별도로 추적해야 합니다.
:::

이 튜토리얼의 마지막 단계는 *controller.script*에 몇 줄을 추가하는 것입니다.

```lua
-- controller.script
...
local platform_heights = { 100, 200, 350 }
local coins = 3 -- <1>
...
```
1. 일반 플랫폼에 스폰할 코인의 수입니다.

```lua
-- controller.script
...
local coins = coins
if math.random() > 0.5 then
    f = "#platform_long_factory"
    coins = coins * 2 -- 긴 플랫폼에는 코인 수를 두 배로 합니다
end
...
```

```lua
-- controller.script
...
msg.post(p, "set_speed", { speed = self.speed })
msg.post(p, "create_coins", { coins = coins })
table.insert(self.spawns, p)
...
```

![controller 코드 삽입](images/runner/insert_controller_code.png)

이제 단순하지만 동작하는 게임이 완성되었습니다! 여기까지 왔다면 계속해서 직접 다음을 추가해 볼 수 있습니다.

1. 점수와 생명 카운터
2. 수집과 사망을 위한 파티클 효과
3. 멋진 배경 이미지

> 완성된 프로젝트 버전은 [여기](images/runner/sample-runner.zip)에서 다운로드하세요.

이것으로 입문 튜토리얼을 마칩니다. 이제 Defold에 뛰어들어 보세요. 안내를 위해 많은 [매뉴얼과 튜토리얼](//www.defold.com/learn)을 준비해 두었으며, 막히면 [포럼](//forum.defold.com)에 오시면 됩니다.

즐거운 Defolding 되세요!
