---
title: "에디터 스크립트: UI"
brief: 이 매뉴얼은 Lua를 사용해 에디터에서 UI 요소를 만드는 방법을 설명합니다
---

# 에디터 스크립트와 UI {#editor-scripts-and-ui}

이 매뉴얼은 Lua로 작성한 에디터 스크립트를 사용해 에디터에서 상호작용형 UI 요소를 만드는 방법을 설명합니다. 에디터 스크립트를 시작하려면 [Editor Scripts 매뉴얼](/manuals/editor-scripts)을 참고하세요. 전체 editor API reference는 [여기](/ref/stable/editor-lua/)에서 볼 수 있습니다. 현재는 상호작용형 dialog만 만들 수 있지만, 앞으로 UI scripting 지원을 에디터의 나머지 영역으로 확장하려고 합니다.

## Hello world {#hello-world}

모든 UI 관련 기능은 `editor.ui` 모듈에 있습니다. 시작을 위한 커스텀 UI가 있는 에디터 스크립트의 가장 간단한 예는 다음과 같습니다.
```lua
local M = {}

function M.get_commands()
    return {
        {
            label = "Do with confirmation",
            locations = {"View"},
            run = function()
                local result = editor.ui.show_dialog(editor.ui.dialog({
                    title = "Perform action?",
                    buttons = {
                        editor.ui.dialog_button({
                            text = "Cancel",
                            cancel = true,
                            result = false
                        }),
                        editor.ui.dialog_button({
                            text = "Perform",
                            default = true,
                            result = true
                        })
                    }
                }))
                print('Perform action:', result)
            end
        }
    }
end

return M

```

이 코드 조각은 **View → Do with confirmation** 명령을 정의합니다. 실행하면 다음 dialog가 표시됩니다.

![Hello world dialog](images/editor_scripts/perform_action_dialog.png)

마지막으로 <kbd>Enter</kbd>를 누르거나 `Perform` 버튼을 클릭하면 에디터 콘솔에 다음 줄이 표시됩니다.
```
Perform action:	true
```

## 기본 개념 {#basic-concepts}

### 컴포넌트 {#components}

에디터는 원하는 UI를 만들기 위해 조합할 수 있는 여러 UI **컴포넌트**를 제공합니다. 관례상 모든 컴포넌트는 **props**라는 단일 테이블을 사용해 설정합니다. 컴포넌트 자체는 테이블이 아니라, 에디터가 UI를 만들 때 사용하는 **불변 userdata**입니다.

### Props {#props}

**Props**는 컴포넌트에 전달되는 입력을 정의하는 테이블입니다. Props는 불변으로 다뤄야 합니다. props 테이블을 제자리에서 변경해도 컴포넌트가 다시 렌더링되지 않지만, 다른 테이블을 사용하면 다시 렌더링됩니다. 컴포넌트 인스턴스가 이전 값과 shallow-equal하지 않은 props 테이블을 받으면 UI가 업데이트됩니다.

### 정렬 {#alignment}

컴포넌트가 UI에서 어떤 bounds를 할당받으면 전체 공간을 소비하지만, 이것이 컴포넌트의 보이는 부분이 늘어난다는 뜻은 아닙니다. 대신 보이는 부분은 필요한 공간만 차지한 다음, 할당된 bounds 안에서 정렬됩니다. 따라서 대부분의 내장 컴포넌트는 `alignment` prop을 정의합니다.

예를 들어 다음 label 컴포넌트를 살펴보겠습니다.
```lua
editor.ui.label({
    text = "Hello",
    alignment = editor.ui.ALIGNMENT.RIGHT
})
```
보이는 부분은 `Hello` 텍스트이며, 할당된 컴포넌트 bounds 안에서 정렬됩니다.

![정렬](images/editor_scripts/alignment.png)

## 내장 컴포넌트 {#built-in-components}

에디터는 UI를 만들 때 함께 사용할 수 있는 다양한 내장 컴포넌트를 정의합니다. 컴포넌트는 대략 레이아웃, 데이터 표시, 입력이라는 3가지 범주로 묶을 수 있습니다.

### 레이아웃 컴포넌트 {#layout-components}

레이아웃 컴포넌트는 다른 컴포넌트를 서로 나란히 배치하는 데 사용합니다. 주요 레이아웃 컴포넌트는 **`horizontal`**, **`vertical`**, **`grid`**입니다. 이 컴포넌트들은 **padding**과 **spacing** 같은 props도 정의합니다. padding은 할당된 bounds의 가장자리부터 컨텐츠까지의 빈 공간이고, spacing은 자식 사이의 빈 공간입니다.

![Padding과 Spacing](images/editor_scripts/padding_and_spacing.png)

에디터는 `small`, `medium`, `large` padding과 spacing 상수를 정의합니다. spacing의 경우 `small`은 개별 UI 요소의 서로 다른 하위 요소 사이 간격에 사용하고, `medium`은 개별 UI 요소 사이 간격에 사용하며, `large`는 요소 그룹 사이 간격에 사용합니다. 기본 spacing은 `medium`입니다. `large` padding 값은 창 가장자리부터 컨텐츠까지의 padding을 의미하고, `medium`은 중요한 UI 요소의 가장자리부터의 padding, `small`은 컨텍스트 메뉴와 툴팁(아직 구현되지 않음) 같은 작은 UI 요소의 가장자리부터의 padding을 의미합니다.

**`horizontal`** 컨테이너는 자식을 가로로 차례대로 배치하며, 모든 자식의 높이가 항상 사용 가능한 공간을 채우도록 만듭니다. 기본적으로 모든 자식의 너비는 최소로 유지되지만, 자식에 `grow` prop을 `true`로 설정하면 가능한 한 많은 공간을 차지하게 만들 수 있습니다.

**`vertical`** 컨테이너는 horizontal과 비슷하지만 축이 바뀐 형태입니다.

마지막으로 **`grid`**는 table처럼 자식을 2D 그리드에 배치하는 컨테이너 컴포넌트입니다. grid의 `grow` 설정은 행 또는 열에 적용되므로 자식이 아니라 column 설정 테이블에 설정합니다. 또한 grid의 자식은 `row_span`과 `column_span` props로 여러 행 또는 열에 걸치도록 설정할 수 있습니다. Grid는 여러 입력이 있는 form을 만들 때 유용합니다.
```lua
editor.ui.grid({
    padding = editor.ui.PADDING.LARGE, -- dialog 가장자리 주변에 padding을 추가합니다
    columns = {{}, {grow = true}}, -- 두 번째 column을 grow하도록 설정합니다
    children = {
        {
            editor.ui.label({
                text = "Level Name",
                alignment = editor.ui.ALIGNMENT.RIGHT
            }),
            editor.ui.string_field({})
        },
        {
            editor.ui.label({
                text = "Author",
                alignment = editor.ui.ALIGNMENT.RIGHT
            }),
            editor.ui.string_field({})
        }
    }
})
```
위 코드는 다음 dialog form을 생성합니다.

![New Level dialog](images/editor_scripts/new_level_dialog.png)

### 데이터 표시 컴포넌트 {#data-presentation-components}

에디터는 다음 데이터 표시 컴포넌트를 정의합니다.

- **`label`** — 텍스트 라벨이며 form 입력과 함께 사용하기 위한 것입니다.
- **`icon`** — 아이콘입니다. 현재는 미리 정의된 작은 아이콘 집합을 표시하는 데만 사용할 수 있지만, 앞으로 더 많은 아이콘을 허용하려고 합니다.
- **`image`** — `/`로 시작하는 프로젝트 리소스 경로나 외부 URL에서 로드한 이미지입니다. 선택적인 `width`와 `height` prop은 종횡비를 유지하면서 지정된 크기 안에 이미지를 맞춥니다.
- **`heading`** — form이나 dialog 등에서 제목 줄 텍스트를 표시하기 위한 텍스트 요소입니다. `editor.ui.HEADING_STYLE` enum은 HTML의 `H1`-`H6` heading과 에디터 전용 `DIALOG`, `FORM`을 포함하는 다양한 heading 스타일을 정의합니다.
- **`paragraph`** — 텍스트 단락을 표시하기 위한 텍스트 요소입니다. `label`과의 주요 차이는 paragraph가 word wrapping을 지원한다는 점입니다. 할당된 bounds가 가로로 너무 작으면 텍스트가 줄바꿈되고, view에 들어가지 않으면 `"..."`로 줄어들 수도 있습니다.

예를 들어 UI에서 프로젝트 이미지와 웹 이미지를 모두 표시할 수 있습니다.

```lua
editor.ui.vertical({
    children = {
        editor.ui.image({
            image = "/builtins/assets/images/logo/logo_256.png",
            width = 64,
            height = 64
        }),
        editor.ui.image({
            image = "https://defold.com/images/assets/monarch-hero.jpg"
        })
    }
})
```

### 입력 컴포넌트 {#input-components}

입력 컴포넌트는 사용자가 UI와 상호작용하도록 만들기 위한 것입니다. 모든 입력 컴포넌트는 상호작용 활성화 여부를 제어하는 `enabled` prop을 지원하며, 상호작용이 발생했을 때 에디터 스크립트에 알려주는 다양한 callback props를 정의합니다.

정적 UI를 만든다면 단순히 로컬 변수를 수정하는 callback을 정의하는 것으로 충분합니다. 동적 UI와 더 고급 상호작용은 [반응성](#reactivity)을 참고하세요.

예를 들어 다음과 같이 간단한 정적 New File dialog를 만들 수 있습니다.
```lua
-- 초기 파일 이름이며 dialog에서 바뀝니다
local file_name = ""
local create_file = editor.ui.show_dialog(editor.ui.dialog({
    title = "Create New File",
    content = editor.ui.horizontal({
        padding = editor.ui.PADDING.LARGE,
        spacing = editor.ui.SPACING.MEDIUM,
        children = {
            editor.ui.label({
                text = "New File Name",
                alignment = editor.ui.ALIGNMENT.CENTER
            }),
            editor.ui.string_field({
                grow = true,
                text = file_name,
                -- 입력 callback:
                on_value_changed = function(new_text)
                    file_name = new_text
                end
            })
        }
    }),
    buttons = {
        editor.ui.dialog_button({ text = "Cancel", cancel = true, result = false }),
        editor.ui.dialog_button({ text = "Create File", default = true, result = true })
    }
}))
if create_file then
    print("create", file_name)
end
```
내장 입력 컴포넌트 목록은 다음과 같습니다.
- **`string_field`**, **`integer_field`**, **`number_field`**는 문자열, 정수, 숫자를 편집할 수 있는 한 줄 텍스트 필드의 변형입니다.
- **`select_box`**는 dropdown control로 미리 정의된 options 배열에서 option을 선택하는 데 사용합니다.
- **`check_box`**는 `on_value_changed` callback이 있는 boolean 입력 필드입니다.
- **`button`**은 버튼을 누를 때 호출되는 `on_press` callback을 가집니다.
- **`external_file_field`**는 컴퓨터에서 파일 경로를 선택하기 위한 컴포넌트입니다. 텍스트 필드와 파일 선택 dialog를 여는 버튼으로 구성됩니다.
- **`resource_field`**는 프로젝트 안의 리소스를 선택하기 위한 컴포넌트입니다.

버튼을 제외한 모든 컴포넌트는 컴포넌트와 관련된 issue(`editor.ui.ISSUE_SEVERITY.ERROR` 또는 `editor.ui.ISSUE_SEVERITY.WARNING`)를 표시하는 `issue` prop을 설정할 수 있습니다. 예:
```lua
issue = {severity = editor.ui.ISSUE_SEVERITY.WARNING, message = "This value is deprecated"}
```
issue를 지정하면 입력 컴포넌트의 표시 방식이 바뀌고, issue 메세지가 있는 툴팁이 추가됩니다.

다음은 모든 입력과 issue 변형의 데모입니다.

![입력](images/editor_scripts/inputs_demo.png)

### Dialog 관련 컴포넌트 {#dialog-related-components}

dialog를 표시하려면 `editor.ui.show_dialog` 함수를 사용해야 합니다. 이 함수는 Defold dialog의 주요 구조인 `title`, `header`, `content`, `buttons`를 정의하는 **`dialog`** 컴포넌트를 기대합니다. Dialog 컴포넌트는 조금 특별합니다. UI 요소가 아니라 창을 나타내므로 다른 컴포넌트의 자식으로 사용할 수 없습니다. 하지만 `header`와 `content`는 일반 컴포넌트입니다.

Dialog 버튼도 특별합니다. **`dialog_button`** 컴포넌트를 사용해 만듭니다. 일반 버튼과 달리 dialog 버튼에는 `on_pressed` callback이 없습니다. 대신 dialog가 닫힐 때 `editor.ui.show_dialog` 함수가 반환할 값을 담는 `result` prop을 정의합니다. Dialog 버튼은 `cancel`과 `default` boolean props도 정의합니다. `cancel` prop이 있는 버튼은 사용자가 <kbd>Escape</kbd>를 누르거나 OS 닫기 버튼으로 dialog를 닫을 때 트리거되고, `default` 버튼은 사용자가 <kbd>Enter</kbd>를 누를 때 트리거됩니다. 하나의 dialog 버튼은 `cancel`과 `default` props를 동시에 `true`로 설정할 수 있습니다.

### 유틸리티 컴포넌트 {#utility-components}

추가로 에디터는 몇 가지 유틸리티 컴포넌트를 정의합니다.
- **`separator`**는 컨텐츠 블록을 구분하는 데 사용하는 얇은 선입니다.
- **`scroll`**은 감싼 컴포넌트가 할당된 공간에 맞지 않을 때 스크롤 바를 보여주는 wrapper 컴포넌트입니다.

## 반응성 {#reactivity}

컴포넌트는 **불변 userdata**이므로 만든 뒤에는 변경할 수 없습니다. 그렇다면 시간이 지나면서 UI가 바뀌도록 만들려면 어떻게 해야 할까요? 답은 **반응형 컴포넌트**입니다.

::: sidenote
에디터 scripting UI는 [React](https://react.dev/) 라이브러리에서 영감을 받았으므로, reactive UI와 React hooks를 알고 있으면 도움이 됩니다.
:::

가장 간단히 말하면, 반응형 컴포넌트는 데이터(props)를 받아 view(다른 컴포넌트)를 반환하는 Lua 함수가 있는 컴포넌트입니다. 반응형 컴포넌트 함수는 **hooks**를 사용할 수 있습니다. hooks는 컴포넌트에 반응형 기능을 추가하는 `editor.ui` 모듈의 특별한 함수입니다. 관례상 모든 hook 이름은 `use_`로 시작합니다.

반응형 컴포넌트를 만들려면 `editor.ui.component()` 함수를 사용합니다.

입력한 파일 이름이 비어 있지 않을 때만 파일 생성을 허용하는 New File dialog 예를 살펴보겠습니다.

```lua
-- 1. dialog는 반응형 컴포넌트입니다
local dialog = editor.ui.component(function(props)
    -- 2. 컴포넌트는 빈 문자열을 기본값으로 하는 로컬 상태(파일 이름)를 정의합니다
    local name, set_name = editor.ui.use_state("")

    return editor.ui.dialog({
        title = props.title,
        content = editor.ui.vertical({
            padding = editor.ui.PADDING.LARGE,
            children = {
                editor.ui.string_field({
                    value = name,
                    -- 3. 입력 + Enter가 로컬 상태를 업데이트합니다
                    on_value_changed = set_name
                })
            }
        }),
        buttons = {
            editor.ui.dialog_button({
                text = "Cancel",
                cancel = true
            }),
            editor.ui.dialog_button({
                text = "Create File",
                -- 4. 이름이 있을 때 생성이 활성화됩니다
                enabled = name ~= "",
                default = true,
                -- 5. result는 이름입니다
                result = name
            })
        }
    })
end)

-- 6. show_dialog는 비어 있지 않은 파일 이름을 반환하거나 취소 시 nil을 반환합니다
local file_name = editor.ui.show_dialog(dialog({ title = "New File Name" }))
if file_name then
    print("create " .. file_name)
else
    print("cancelled")
end
```

이 코드를 실행하는 메뉴 명령을 실행하면 에디터는 처음에 `"Create File"` dialog 버튼이 비활성화된 dialog를 표시합니다. 하지만 이름을 입력하고 <kbd>Enter</kbd>를 누르면 활성화됩니다.

![New File dialog](images/editor_scripts/reactive_new_file_dialog.png)

그렇다면 이것은 어떻게 동작할까요? 최초 렌더링에서 `use_state` hook은 컴포넌트와 연결된 로컬 상태를 만들고, 상태 setter와 함께 반환합니다. setter 함수가 호출되면 컴포넌트 re-render를 예약합니다. 이후 re-render에서 컴포넌트 함수가 다시 호출되고, `use_state`는 업데이트된 상태를 반환합니다. 그러면 컴포넌트 함수가 반환한 새 view 컴포넌트를 이전 컴포넌트와 diff하고, 변경이 감지된 곳의 UI가 업데이트됩니다.

이 반응형 접근 방식은 상호작용형 UI를 만들고 동기화 상태로 유지하는 일을 크게 단순화합니다. 사용자 입력에 따라 영향을 받는 모든 UI 컴포넌트를 명시적으로 업데이트하는 대신, view를 입력(props와 로컬 상태)의 순수 함수로 정의하면 에디터가 모든 업데이트를 직접 처리합니다.

### 반응성 규칙 {#rules-of-reactivity}

에디터는 reactive function components가 제대로 동작하려면 다음 규칙을 지키기를 기대합니다.

1. 컴포넌트 함수는 순수해야 합니다. 컴포넌트 함수가 언제 또는 얼마나 자주 호출될지는 보장되지 않습니다. 모든 side-effect는 callback 등 렌더링 외부에 있어야 합니다.
2. Props와 로컬 상태는 불변이어야 합니다. props를 변경하지 마세요. 로컬 상태가 테이블인 경우 제자리에서 변경하지 말고, 상태를 변경해야 할 때 새 테이블을 만들어 setter에 전달하세요.
3. 컴포넌트 함수는 매 호출마다 같은 hook을 같은 순서로 호출해야 합니다. loop 안, 조건 블록 안, early return 뒤 등에서 hook을 호출하지 마세요. 컴포넌트 함수의 시작 부분에서 다른 코드보다 먼저 hook을 호출하는 것이 좋습니다.
4. Hook은 컴포넌트 함수에서만 호출하세요. Hook은 반응형 컴포넌트의 context에서 동작하므로 컴포넌트 함수(또는 컴포넌트 함수가 직접 호출하는 다른 함수) 안에서만 호출할 수 있습니다.

### Hooks {#hooks}

::: sidenote
[React](https://react.dev/)에 익숙하다면, 에디터의 hooks는 hook dependencies와 관련해 약간 다른 의미 체계를 가진다는 점을 알 수 있습니다.
:::

에디터는 **`use_memo`**와 **`use_state`**라는 2가지 hook을 정의합니다.

### **`use_state`** {#use_state}

로컬 상태는 기본값 또는 초기화 함수라는 2가지 방식으로 만들 수 있습니다.
```lua
-- 기본값
local enabled, set_enabled = editor.ui.use_state(true)
-- 초기화 함수 + 인자
local id, set_id = editor.ui.use_state(string.lower, props.name)
```
마찬가지로 setter는 새 값 또는 updater 함수로 호출할 수 있습니다.
```lua
-- updater 함수
local function increment_by(n, by)
    return n + by
end

local counter = editor.ui.component(function(props)
    local count, set_count = editor.ui.use_state(0)

    return editor.ui.horizontal({
        spacing = editor.ui.SPACING.SMALL,
        children = {
            editor.ui.label({
                text = tostring(count),
                alignment = editor.ui.ALIGNMENT.LEFT,
                grow = true
            }),
            editor.ui.text_button({
                text = "+1",
                on_pressed = function() set_count(increment_by, 1) end
            }),
            editor.ui.text_button({
                text = "+5",
                on_pressed = function() set_count(increment_by, 5) end
            })
        }
    })
end)
```

마지막으로 상태는 **reset**될 수 있습니다. `editor.ui.use_state()`에 전달한 인자 중 하나라도 변경되면 상태가 reset되며, 변경 여부는 `==`로 확인합니다. 이 때문에 `use_state` hook의 인자로 리터럴 테이블이나 리터럴 초기화 함수를 사용하면 안 됩니다. 그러면 re-render마다 상태가 reset됩니다. 예:
```lua
-- ❌ 나쁨: 리터럴 테이블 초기화자는 re-render마다 상태 reset을 일으킵니다
local user, set_user = editor.ui.use_state({ first_name = props.first_name, last_name = props.last_name})

-- ✅ 좋음: 컴포넌트 함수 밖의 초기화 함수를 사용해 테이블 상태를 만듭니다
local function create_user(first_name, last_name)
    return { first_name = first_name, last_name = last_name}
end
-- ...나중에, 컴포넌트 함수에서:
local user, set_user = editor.ui.use_state(create_user, props.first_name, props.last_name)


-- ❌ 나쁨: 리터럴 초기화 함수는 re-render마다 상태 reset을 일으킵니다
local id, set_id = editor.ui.use_state(function() return string.lower(props.name) end)

-- ✅ 좋음: 참조된 초기화 함수를 사용해 상태를 만듭니다
local id, set_id = editor.ui.use_state(string.lower, props.name)
```

### **`use_memo`** {#use_memo}

성능을 개선하려면 `use_memo` hook을 사용할 수 있습니다. 예를 들어 사용자 입력이 유효한지 확인하기 위해 render 함수에서 어떤 계산을 수행하는 일은 흔합니다. 계산 함수의 인자가 변경되었는지 확인하는 비용이 계산 함수를 호출하는 비용보다 더 저렴한 경우 `use_memo` hook을 사용할 수 있습니다. 이 hook은 최초 렌더링에서 계산 함수를 호출하고, 이후 re-render에서는 `use_memo`에 전달한 모든 인자가 변경되지 않았다면 계산된 값을 재사용합니다.
```lua
-- 컴포넌트 함수 밖의 validation 함수
local function validate_password(password)
    if #password < 8 then
        return false, "Password must be at least 8 characters long."
    elseif not password:match("%l") then
        return false, "Password must include at least one lowercase letter."
    elseif not password:match("%u") then
        return false, "Password must include at least one uppercase letter."
    elseif not password:match("%d") then
        return false, "Password must include at least one number."
    else
        return true, "Password is valid."
    end
end

-- ...나중에, 컴포넌트 함수에서
local username, set_username = editor.ui.use_state('')
local password, set_password = editor.ui.use_state('')
local valid, message = editor.ui.use_memo(validate_password, password)
```
이 예에서 password validation은 password가 변경될 때마다(예: password 필드에 입력할 때) 실행되지만, username이 변경될 때는 실행되지 않습니다.

`use_memo`의 또 다른 사용 사례는 입력 컴포넌트에서 사용할 callback을 만들거나, 로컬에서 만든 함수를 다른 컴포넌트의 prop 값으로 사용할 때입니다. 이렇게 하면 불필요한 re-render를 방지할 수 있습니다.
