---
title: Defold GUI 텍스트 노드
brief: 이 매뉴얼은 GUI 씬에 텍스트를 추가하는 방법을 설명합니다.
---

# GUI 텍스트 노드

Defold는 GUI 씬에서 텍스트를 렌더링할 수 있는 특정한 유형의 GUI 노드를 지원합니다. 프로젝트에 추가된 모든 폰트 리소스는 텍스트 노드 렌더링에 사용할 수 있습니다.

에디터 미리보기는 엔진의 폰트 렌더러를 사용하여 텍스트 셰이핑과 오른쪽에서 왼쪽으로 쓰는 레이아웃을 지원합니다. 필요한 폰트 및 App Manifest 설정은 [텍스트 레이아웃 지원](/manuals/font/#text-layout-support-eg-right-to-left)을 참고하세요.

## 텍스트 노드 추가하기

GUI 텍스트 노드에서 사용하려는 폰트는 GUI 컴포넌트에 추가해야 합니다. *Fonts* 폴더를 오른쪽 클릭하거나, 상단 <kbd>GUI</kbd> 메뉴를 사용하거나, 해당 키보드 단축키를 누르세요.

![Fonts](images/gui-text/fonts.png)

텍스트 노드에는 특수 프로퍼티들이 있습니다:

*Font*
: 생성하는 모든 텍스트 노드는 *Font* 프로퍼티가 설정되어 있어야 합니다.

*Text*
: 이 프로퍼티에는 표시되는 텍스트가 들어 있습니다.

*Line Break*
: 텍스트 정렬은 피벗 설정을 따르며, 이 프로퍼티를 설정하면 텍스트가 여러 줄로 이어질 수 있습니다. 노드의 너비가 텍스트가 줄바꿈되는 위치를 결정합니다.

## 벡터 폰트와 컬러 이모지 {#vector-fonts-and-color-emoji}

[벡터 폰트 설정](/manuals/font/#vector-fonts)에 따라 `.font` 리소스를 GUI 씬의 *Fonts*에 추가하고 텍스트 노드에서 선택합니다. 폰트 리소스의 *Material*을 `/builtins/fonts/font-vector.material`로 설정합니다. 표시 크기는 노드의 *Font Size*로 제어합니다.

컬러 이모지는 [COLRv1 대체 폰트 및 번들 설정](/manuals/font/#color-emoji)도 완료하세요. 아이디가 `text`인 텍스트 노드를 만들고 *Text*를 비운 다음 GUI 씬의 `.gui_script`에 다음을 추가합니다:

```lua
function init(self)
    local node = gui.get_node("text")
    local text = "Hello 😀 🍎 🚀"
    local font_resource = gui.get_font_resource(gui.get_font(node))
    -- 이 공유 폰트 리소스에는 대체 폰트를 한 번만 추가합니다.
    font.add_font(font_resource, "/fonts/NotoColorEmoji-Regular.ttf")
    font.prewarm_text(font_resource, text, function(self, request_id, result, err)
        if result then
            gui.set_text(node, text)
        else
            print("Could not prepare GUI text:", err)
        end
    end)
end
```

[`gui.get_font()`](/ref/gui/#gui.get_font)는 GUI 씬 내부의 폰트 이름을 반환하고, [`gui.get_font_resource()`](/ref/gui/#gui.get_font_resource)는 그 이름을 `font.add_font()`에 사용할 폰트 리소스로 변환합니다. 리소스를 공유하는 다른 노드와 Label에도 대체 폰트가 적용되므로 초기화는 한 번만 합니다. 텍스트는 사전 준비에 성공한 후 설정됩니다.

## 정렬

노드 피벗을 설정하여 텍스트의 정렬 모드를 변경할 수 있습니다.

*Center*
: 피벗이 `Center`, `North` 또는 `South`로 설정되어 있으면 텍스트가 가운데 정렬됩니다.

*Left*
: 피벗이 `West` 모드 중 하나로 설정되어 있으면 텍스트가 왼쪽 정렬됩니다.

*Right*
: 피벗이 `East` 모드 중 하나로 설정되어 있으면 텍스트가 오른쪽 정렬됩니다.

![Text alignment](images/gui-text/align.png)

## 런타임에 텍스트 노드 수정하기

텍스트 노드는 크기, 피벗, 색상 등을 설정하는 모든 일반 노드 조작 함수에 응답합니다. 텍스트 노드에만 적용되는 함수도 몇 가지 있습니다:

* 텍스트 노드의 폰트를 변경하려면 [`gui.set_font()`](/ref/gui/#gui.set_font) 함수를 사용합니다.
* 텍스트 노드의 줄바꿈 동작을 변경하려면 [`gui.set_line_break()`](/ref/gui/#gui.set_line_break) 함수를 사용합니다.
* 텍스트 노드의 내용을 변경하려면 [`gui.set_text()`](/ref/gui/#gui.set_text) 함수를 사용합니다.

```lua
function on_message(self, message_id, message, sender)
    if message_id == hash("set_score") then
        local s = gui.get_node("score")
        gui.set_text(s, message.score)
    end
end
```
