---
title: Defold의 리치 텍스트 마크업
brief: 이 매뉴얼은 리치 텍스트 마크업으로 Label 컴포넌트와 GUI 텍스트 노드에 스타일을 적용하고 Lua에서 링크와 스프라이트를 확인하는 방법을 설명합니다.
---

# 리치 텍스트 마크업 {#rich-text-markup}

Label 컴포넌트와 GUI 텍스트 노드에서 마크업을 사용하여 중첩된 시각적 스타일과 효과를 적용하고, Lua에서 링크와 스프라이트를 확인할 수 있습니다.

```lua
go.set("#label", "text", "Score: <color=#69D2E7>1200</color>")
```

폰트에 재사용할 수 있는 이름 있는 오브젝트 스타일을 정의하고 링크에서 선택할 수도 있습니다.

```lua
local fontpath = "/fonts/ui.fontc"
font.set_style(fontpath, "menu_link", "<color=#69D2E7>")
go.set("#label", "text", "Open <link style=menu_link src=inventory>inventory</link>")
```

## 태그 레퍼런스 {#tag-reference}

| 태그 | 용도 | 예제 |
| --- | --- | --- |
| [`color`](#color) | 글리프 면 색상을 설정합니다. | <img src="/manuals/images/richtext/color_green.webp" alt="초록색 텍스트" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`size`](#size) | 글리프 셰이핑과 레이아웃 크기를 변경합니다. | <img src="/manuals/images/richtext/size_24.webp" alt="24픽셀 크기의 텍스트" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`gradient`](#gradient) | 정적 또는 애니메이션 색상 그라디언트를 적용합니다. | <img src="/manuals/images/richtext/gradient_horizontal.webp" alt="수평 그라디언트가 적용된 텍스트" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`ul`](#ul) | 텍스트에 밑줄을 긋습니다. | <img src="/manuals/images/richtext/underline_solid.webp" alt="밑줄이 있는 텍스트" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`strike`](#strike) | 텍스트에 취소선을 긋습니다. | <img src="/manuals/images/richtext/strike_solid.webp" alt="취소선이 있는 텍스트" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`outline`](#outline) | 글리프 외곽선의 너비와 색상을 설정합니다. | <img src="/manuals/images/richtext/outline.webp" alt="외곽선이 있는 텍스트" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`shadow`](#shadow) | 텍스트에 그림자를 추가합니다. | <img src="/manuals/images/richtext/shadow.webp" alt="그림자가 있는 텍스트" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`shake`](#shake) | 애니메이션 무작위 오프셋을 적용합니다. | <img src="/manuals/images/richtext/shake_glyph.webp" alt="흔들리는 텍스트" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`wave`](#wave) | 사인파 애니메이션으로 텍스트를 움직입니다. | <img src="/manuals/images/richtext/wave_glyph.webp" alt="물결치는 텍스트" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`sprite`](#sprite) | 인라인 스프라이트 오브젝트를 추가합니다. | <img src="/manuals/images/richtext/sprite.webp" alt="인라인 스프라이트" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`link`](#link) | 상호작용할 수 있는 링크 오브젝트를 추가합니다. | <img src="/manuals/images/richtext/link.webp" alt="링크된 텍스트" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |

## 문법 {#syntax}

태그와 속성 이름은 대소문자를 구분합니다. 짝을 이루는 태그는 그 안에 있는 보이는 UTF-32 텍스트에 적용됩니다. 스프라이트 오브젝트는 자체 닫는 태그를 사용합니다.

```text
<color=#69D2E7>colored text</color>
<ul pattern=dashed>underlined text</ul>
<outline size=2 color=#000000>outlined text</outline>
<shadow x=2 y=-2 color=#00000080>shadowed text</shadow>
<sprite src=images/icon.png width=2em/>
```

### 속성 {#attributes}

속성에 공백이 없으면 따옴표 없이 쓸 수 있으며, 작은따옴표나 큰따옴표로 감쌀 수도 있습니다. `color`와 `size`는 이름을 지정하는 `value` 형식과 첫 번째 값을 간단히 쓰는 축약형을 모두 지원합니다.

```text
<color=#FF8800>Orange</color>
<color value="#FF8800">Orange</color>
<size='120%'>Larger</size>
```

### 중첩 {#nesting}

태그는 나중에 연 것을 먼저 닫는 순서로 닫아야 합니다. 안쪽 스타일 값은 바깥쪽 스타일의 같은 프로퍼티를 오버라이드합니다. 서로 다른 프로퍼티는 함께 적용됩니다. 텍스트 구간(span)의 효과는 독립적으로 계속 활성화되므로 중첩된 그라디언트는 색상을 곱하고, 중첩된 위치 효과는 오프셋을 더합니다.

```text
<color=#FFCC00>
    Gold <outline size=2 color=#000000>with a black outline</outline>
</color>
```

### 엔티티 {#entities}

보이는 텍스트의 예약 문자에는 `&amp;`, `&apos;`, `&gt;`, `&lt;`, `&quot;`를 사용합니다. 숫자 엔티티는 현재 지원되지 않습니다.

## 태그 {#tags}

리치 텍스트 태그는 둘러싼 텍스트 구간에 스타일을 적용하거나 Lua에서 확인할 수 있는 오브젝트를 설명합니다. 스타일 태그는 짝이 맞는 닫는 태그를 사용합니다. `sprite` 오브젝트는 자체 닫는 태그를 사용하고, `link`는 연결된 텍스트를 둘러쌉니다.

### `color` {#color}

글리프 면 색상을 설정합니다. 색상에는 `#RRGGBB` 또는 `#RRGGBBAA`를 사용합니다. 해쉬 접두어가 필요하며 `0xFF0000`과 `FF0000`은 유효하지 않습니다. 결과는 라벨 또는 렌더러의 기본 색상과 곱해집니다.

| 속성 | 필수 | 기본값 | 의미 |
| --- | --- | --- | --- |
| `=color` 또는 `value=color` | 예 | 기본값 없음 | RGB 또는 RGBA 16진수 형식의 면 색상입니다. |

```text
<color=#00FF00>Opaque green</color>
<color=#00FF0080>Half-alpha green</color>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*#00FF00*

![불투명한 초록색으로 렌더링한 예제 텍스트](images/richtext/color_green.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*#00FF0080*

![알파값이 절반인 초록색으로 렌더링한 예제 텍스트](images/richtext/color_green_alpha.webp)

</div>
</div>

### `size` {#size}

버텍스 스케일뿐 아니라 글리프 셰이핑과 레이아웃 크기도 변경합니다. 상대값은 항상 레이아웃의 기본 폰트 크기를 사용합니다. 바깥쪽 `size` 태그와 누적되지 않습니다.

| 속성 | 필수 | 기본값 | 의미 |
| --- | --- | --- | --- |
| `=size` 또는 `value=size` | 예 | 기본값 없음 | 아래 형식 중 하나를 사용하는 절대 크기, 백분율, 기본 크기의 배수 또는 부호 있는 기본 크기 오프셋입니다. |

| 형식 | 32 px 기준 예제 | 최종 크기 |
| --- | --- | --- |
| 숫자만 쓰거나 `px` 사용 | `24`, `24px` | 24 px |
| 기본 크기의 백분율 | `120%` | 38.4 px |
| 기본 크기의 배수 | `2em` | 64 px |
| 기본 크기로부터 부호 있는 오프셋 | `+4`, `-4` | 36 px, 28 px |

```text
<size=24px>Exactly 24 pixels</size>
<size=120%>120% of the layout base size</size>
<size=2em>Twice the layout base size</size>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*24px*

![24픽셀 크기로 렌더링한 예제 텍스트](images/richtext/size_24.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*32px의 120%*

![32픽셀의 120퍼센트 크기로 렌더링한 예제 텍스트](images/richtext/size_120.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*32px 기준 2em*

![32픽셀 기본 크기의 두 배로 렌더링한 예제 텍스트](images/richtext/size_2em.webp)

</div>
</div>

### `gradient` {#gradient}

그라디언트에는 정확히 하나의 완전한 속성 집합을 지정해야 합니다. 서로 다른 집합을 섞거나 구성원 하나를 생략하면 유효하지 않습니다.

| 모드 | 필수 속성 | 보간 |
| --- | --- | --- |
| 수평 | `left`, `right` | 가로 방향의 두 색상 사이를 보간합니다. |
| 수직 | `bottom`, `top` | 아래쪽과 위쪽 색상 사이를 보간합니다. |
| 네 모서리 | `tl`, `tr`, `bl`, `br` | 네 버텍스 색상 사이를 보간합니다. |

| 속성 | 필수 | 기본값 | 의미 |
| --- | --- | --- | --- |
| `left`, `right` | 수평 모드에서 필수 | 없음 | `#RRGGBB` 또는 `#RRGGBBAA` 형식의 가로 양 끝 색상입니다. 둘 다 있어야 합니다. |
| `bottom`, `top` | 수직 모드에서 필수 | 없음 | 세로 양 끝 색상입니다. 둘 다 있어야 합니다. |
| `tl`, `tr`, `bl`, `br` | 네 모서리 모드에서 필수 | 없음 | 왼쪽 위, 오른쪽 위, 왼쪽 아래, 오른쪽 아래 색상입니다. 네 개 모두 있어야 합니다. |
| `fit` | 아니요 | `span` | `glyph`는 셰이핑된 각 텍스트 위치를 샘플링합니다. `span`은 태그로 지정한 텍스트 전체에 그라디언트를 분포시킵니다. |
| `hz` | 아니요 | `0` | 초당 완전한 흐름 주기 수이며 범위는 `[0,)`입니다. 0이면 그라디언트가 정적으로 유지됩니다. |
| `direction` | 아니요 | `forward` | `forward` 또는 `reverse`입니다. `hz`가 0이 아닐 때 흐름 방향을 제어합니다. |

`fit`을 생략하면 `fit=span`이 태그로 지정한 텍스트 전체에 그라디언트를 분포시킵니다. `fit=glyph`는 셰이핑된 각 텍스트 위치를 독립적으로 샘플링합니다. 선택적 `hz`는 초당 완전한 흐름 애니메이션 주기 수를 지정하며, 기본값 0은 그라디언트를 정적으로 유지합니다. 거울처럼 반사되어 반복되는 색상 변화가 연속적으로 흐르며 색상이 갑자기 바뀌지 않고 순환합니다. 기본값은 `direction=forward`이며, 흐름을 반대로 바꾸려면 `direction=reverse`를 사용합니다.

```text
<gradient left=#FF00FF right=#FFFFFF>Horizontal Gradient</gradient>

<gradient hz=0.25 fit=glyph bottom=#182848 top=#4B6CB7>Animated vertical glyphs</gradient>

<gradient hz=0.25 direction=reverse left=#FF0000 right=#0000FF>Reverse flow</gradient>

<gradient hz=0.25 direction=reverse fit=span left=#FF0000 right=#0000FF>One animated span color</gradient>

<gradient fit=glyph tl=#FF0000 tr=#00FF00 bl=#0000FF br=#FFFFFF>
    Four corners
</gradient>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*수평*

![수평으로 마젠타에서 흰색으로 변하는 그라디언트가 적용된 예제 텍스트](images/richtext/gradient_horizontal.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*수직*

![수직 파란색 그라디언트가 적용된 예제 텍스트](images/richtext/gradient_vertical.webp)

</div>
</div>

**네 모서리**

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=glyph`*

![각 글리프에 맞춘 네 모서리 그라디언트가 적용된 예제 텍스트](images/richtext/gradient_four_glyph.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=span`*

![텍스트 구간에 맞춘 네 모서리 그라디언트가 적용된 예제 텍스트](images/richtext/gradient_four_text.webp)

</div>
</div>

**애니메이션**

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=glyph`*

![각 글리프에 맞춰 흐르는 애니메이션 그라디언트](images/richtext/gradient_flow_glyph.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=span`*

![텍스트 구간에 맞춰 흐르는 애니메이션 그라디언트](images/richtext/gradient_flow_span.webp)

</div>
</div>

그라디언트 색상은 현재 면 색상과 곱해집니다. 따라서 `color=#808080` 안의 그라디언트는 해당 기본 배율보다 밝은 채널을 만들 수 없습니다.

### `ul` {#ul}

폰트의 밑줄 메트릭을 사용할 수 있으면 이를 사용해 밑줄을 그립니다. 이 태그에는 독립적인 색상이 없습니다. 선은 수평, 수직, 네 모서리 그라디언트를 포함하여 최종적으로 적용된 면 색상을 상속합니다.

| 속성 | 필수 | 기본값 | 의미 |
| --- | --- | --- | --- |
| `pattern` | 아니요 | `solid` | `solid` 또는 `dashed`입니다. |

```text
<ul>Solid underline</ul>
<ul pattern=dashed>Dashed underline</ul>
<ul><gradient left=#FF00FF right=#FFFFFF>Gradient line</gradient></ul>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*실선*

![실선 밑줄이 있는 예제 텍스트](images/richtext/underline_solid.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*파선*

![파선 밑줄이 있는 예제 텍스트](images/richtext/underline_dashed.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*그라디언트*

![그라디언트 밑줄이 있는 예제 텍스트](images/richtext/underline_gradient.webp)

</div>
</div>

### `strike` {#strike}

둘러싼 텍스트를 가로지르는 선을 그립니다. `ul`과 같은 `pattern` 값을 받으며, 마찬가지로 최종적으로 적용된 면 색상을 상속합니다.

| 속성 | 필수 | 기본값 | 의미 |
| --- | --- | --- | --- |
| `pattern` | 아니요 | `solid` | `solid` 또는 `dashed`입니다. |

```text
<strike>No longer available</strike>
<strike pattern=dashed>Dashed strikethrough</strike>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*실선*

![실선 취소선이 있는 예제 텍스트](images/richtext/strike_solid.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*파선*

![파선 취소선이 있는 예제 텍스트](images/richtext/strike_dashed.webp)

</div>
</div>

### `outline` {#outline}

외곽선 너비, 색상 또는 둘 다 설정합니다. 속성을 하나 이상 지정해야 합니다. 너비를 0으로 지정하면 해당 텍스트 구간의 외곽선을 명시적으로 비활성화합니다.

| 속성 | 필수 | 기본값 | 의미 |
| --- | --- | --- | --- |
| `size` | size/color 중 하나 | 상속됨. 기본 폰트에서는 `0` | 레이아웃 단위의 너비이며 범위는 `[0,)`입니다. 단위 접미어는 허용되지 않습니다. |
| `color` | size/color 중 하나 | 상속됨. 기본 라벨에서는 `#000000` | 16진수 RGB(`#RRGGBB`) 또는 RGBA(`#RRGGBBAA`) 형식의 단일 외곽선 색상입니다. 알파 컴포넌트가 불투명도를 제어합니다. |

```text
<outline size=3 color=#000000>Black outline</outline>
<outline color=#FF0000>Keep inherited width, change color</outline>
<outline size=0>Disable inherited outline</outline>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*바깥쪽 검은색 외곽선*

![바깥쪽에 검은색 외곽선이 있는 예제 텍스트](images/richtext/outline.webp)

</div>
</div>

### `shadow` {#shadow}

둘러싼 텍스트에 경계가 뚜렷한 그림자를 추가합니다. 속성을 하나 이상 지정해야 합니다. 중첩된 태그에서 생략한 속성은 바깥쪽 그림자의 값을 유지합니다. 가장 바깥쪽 태그에서 생략한 속성은 폰트의 기본 그림자 값을 유지합니다.

| 속성 | 필수 | 기본값 | 의미 |
| --- | --- | --- | --- |
| `color` | 아니요 | 상속됨. 기본 라벨에서는 `#000000` | `#RRGGBB` 또는 `#RRGGBBAA` 형식의 그림자 색상입니다. |
| `x` | 아니요 | 상속됨. 기본 폰트에서는 `0` | 레이아웃 단위의 수평 그림자 오프셋입니다. 양수이면 오른쪽으로 이동합니다. |
| `y` | 아니요 | 상속됨. 기본 폰트에서는 `0` | 레이아웃 단위의 수직 그림자 오프셋입니다. 양수이면 위로 이동합니다. |
| `blur` | 아니요 | 상속됨. 기본 폰트에서는 `0` | 레이아웃 단위의 블러 반경이며 범위는 `[0,)`입니다. |

```text
<shadow x=6 y=-6 blur=4 color=#000000A0>Shadow</shadow>
<shadow x=-2>Override only the horizontal offset</shadow>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*x=6, y=-6, blur=4*

![오프셋이 적용된 그림자가 있는 예제 텍스트](images/richtext/shadow.webp)

</div>
</div>

::: sidenote
그림자 블러는 글리프 아틀라스에 생성되고 저장됩니다. 텍스트 구간은 폰트에 구워진 블러보다 작은 블러를 요청할 수 있습니다. 더 큰 값도 레이아웃에는 보존되지만, 현재는 아틀라스에서 사용할 수 있는 가장 큰 블러로 렌더링됩니다.
:::

### `shake` {#shake}

줄바꿈이나 레이아웃 경계를 변경하지 않고 결정론적인 무작위 오프셋 애니메이션을 적용합니다. 효과가 내부적으로 시간을 관리하므로 스크립트에서 애니메이션 프레임마다 라벨 텍스트를 수정할 필요가 없습니다.

| 속성 | 필수 | 기본값 | 유효한 값 | 의미 |
| --- | --- | --- | --- | --- |
| `hz` | 아니요 | 20 | `[0,)` | 초당 무작위 목표 전환 횟수입니다. 0이면 효과를 일시 정지합니다. |
| `amplitude` | 아니요 | 0.5 | `[0,)` | 레이아웃 단위의 최대 변위입니다. |
| `fit` | 아니요 | `glyph` | `glyph` 또는 `span` | `glyph`는 셰이핑된 각 글리프 단위에 대해 클러스터를 분리하지 않는 오프셋을 샘플링합니다. `span`은 태그로 지정한 텍스트 구간 전체를 하나의 고정된 단위로 이동합니다. |

```text
<shake>Default shake</shake>
<shake hz=12 amplitude=0.8 fit=glyph>Glyph shake</shake>
<shake hz=12 amplitude=0.8 fit=span>Rigid span shake</shake>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=glyph`*

![글리프별 흔들림 애니메이션이 적용된 예제 텍스트](images/richtext/shake_glyph.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=span`*

![텍스트 구간 전체의 흔들림 애니메이션이 적용된 예제 텍스트](images/richtext/shake_span.webp)

</div>
</div>

### `wave` {#wave}

줄바꿈이나 레이아웃 경계를 변경하지 않고 사인파 애니메이션으로 문자를 위아래로 움직입니다. 레이아웃은 업데이트될 때 애니메이션 시간을 누적합니다.

| 속성 | 필수 | 기본값 | 의미 |
| --- | --- | --- | --- |
| `amplitude` | 아니요 | 1 | 레이아웃 단위의 최대 수직 변위이며 범위는 `[0,)`입니다. |
| `hz` | 아니요 | 1 | 초당 완전한 시간 주기 수이며 범위는 `[0,)`입니다. 0이면 파동을 일시 정지합니다. |
| `wavelength` | 아니요 | 6 | 완전한 공간 주기 하나에 해당하는 보이는 UTF-32 텍스트 위치 수이며 범위는 `[1,)`입니다. 기본 문자와 결합 악센트처럼 폰트가 함께 셰이핑하는 문자들은 하나의 단위로 이동합니다. |
| `fit` | 아니요 | `glyph` | `glyph`는 텍스트 전체에 공간 파동을 적용합니다. `span`은 태그로 지정한 텍스트 구간 전체에 하나의 공통 수직 사인 오프셋을 적용합니다. |
| `direction` | 아니요 | `forward` | `forward`는 일반 방향으로 진행합니다. `reverse`는 파동의 진행 방향을 반대로 바꿉니다. |

```text
<wave>Animated character wave</wave>
<wave amplitude=4 hz=3 wavelength=8 fit=glyph>Travelling wave</wave>
<wave amplitude=4 hz=3 wavelength=8 fit=glyph direction=reverse>Reverse travelling wave</wave>
<wave amplitude=4 hz=1 fit=span>Whole span moves together</wave>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=glyph`*

![글리프별 파동 애니메이션이 적용된 예제 텍스트](images/richtext/wave_glyph.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=span`*

![하나의 텍스트 구간으로 함께 움직이는 예제 텍스트](images/richtext/wave_span.webp)

</div>
</div>

### `sprite` {#sprite}

보이는 텍스트의 현재 위치에 자체 닫는 스프라이트 오브젝트를 추가합니다. 속성은 `label.get_layout_objects()`와 `gui.get_layout_objects()`를 위한 메타데이터로 보존됩니다.

| 속성 | 필수 | 기본값 | 의미 |
| --- | --- | --- | --- |
| `id` | 아니요 | 생성됨 | 반환된 레이아웃 오브젝트의 `id`로 해쉬되는 안정적인 식별자입니다. |
| `src` | 아니요 | 없음 | 이미지나 아틀라스의 프로젝트 경로처럼 어플리케이션에서 정의한 스프라이트 리소스 식별자입니다. |
| `animation` | 아니요 | 없음 | 리소스 안에서 어플리케이션이 정의한 애니메이션 식별자입니다. |
| `width` | 아니요 | `1em` | 계산된 스프라이트 너비입니다. |
| `height` | 아니요 | `1em` | 계산된 스프라이트 높이입니다. |
| 그 밖의 모든 속성 | 아니요 | 없음 | 오브젝트 리졸버와 레이아웃 오브젝트 API를 위해 보존되는 어플리케이션 정의 메타데이터입니다. |

```text
A <sprite src=engine/engine/content/builtins/assets/images/logo/logo_256.png/> logo
<sprite src=images/banner.png width=4em height=2em/>
<sprite src=images/icons.atlas animation=coin width=2em/>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*해석된 인라인 스프라이트*

![텍스트와 같은 줄에 렌더링한 Defold 로고](images/richtext/sprite.webp)

</div>
</div>

크기에는 양수의 단위 없는 레이아웃 값, `px`, `em` 또는 `%`를 사용할 수 있습니다. `em`과 `%` 모두 텍스트 레이아웃의 기본 폰트 크기를 사용합니다.

생략한 각 크기의 기본값은 독립적으로 `1em`입니다. 둘 다 생략하면 `1em × 1em` 오브젝트가 됩니다. 너비만 지정해도 리소스의 종횡비에서 높이를 자동으로 계산하지는 않습니다.

::: important
sprite 태그는 개발자가 해당 위치에 원하는 오브젝트를 배치할 수 있도록 제공하는 자리 표시자입니다!
:::

### `link` {#link}

보이는 텍스트 범위를 링크 오브젝트로 설명합니다. 둘러싼 텍스트는 일반적으로 배치되며 기본적으로 `link`라는 스타일을 적용받습니다. Label 및 GUI 컴포넌트는 입력에 따라 텍스트를 다시 셰이핑하지 않고 `link:hover`와 `link:active`를 선택합니다. 링크 입력이 생성하는 메세지는 [상호작용 메세지](#interaction-messages)를 참고하세요.

| 속성 | 필수 | 기본값 | 의미 |
| --- | --- | --- | --- |
| `src` | 아니요 | 없음 | 어플리케이션에서 정의한 링크 대상입니다. 자동 검증이나 이동 없이 문자열 값으로 반환됩니다. |
| `id` | 아니요 | 생성됨 | 반환된 레이아웃 오브젝트의 `id`로 해쉬되는 안정적인 식별자입니다. |
| `style` | 아니요 | `link` | 링크 텍스트에 사용할 이름 있는 기본 스타일입니다. |
| 그 밖의 모든 속성 | 아니요 | 없음 | 식별자, 동작, 툴팁 또는 분석 값과 같은 어플리케이션 정의 메타데이터입니다. |

```text
<ul><link id=website src=https://www.defold.com>www.defold.com</link></ul>
<link id=inventory style=menu_link action=open_inventory item=sword>Iron sword</link>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`style=link`*

![기본 링크 스타일과 밑줄로 렌더링한 www.defold.com](images/richtext/link.webp)

</div>
</div>

컴포넌트는 각 링크의 포인터 상태를 추적합니다. 포인터가 링크 위에 있으면 `link:hover`를, 포인터를 누르고 있으면 `link:active`를 적용합니다. 어느 상태에도 해당하지 않으면 링크의 `style` 속성이 지정한 스타일을 복원하며, 속성이 없으면 `link`를 복원합니다.

### 상호작용 메세지 {#interaction-messages}

링크 상호작용은 Defold의 일반 입력 시스템을 사용합니다. `MOUSE_BUTTON_LEFT`에 대한 Mouse Trigger 바인딩을 추가하면 단일 터치 입력도 활성화됩니다. 게임 오브젝트의 스크립트나 GUI 스크립트에서 입력 포커스를 획득합니다.

```lua
function init(self)
    msg.post(".", "acquire_input_focus")
end
```

자세한 설정 방법은 [입력 포커스](/manuals/input/#input-focus)와 [마우스 및 터치 입력](/manuals/input-mouse-and-touch)을 참고하세요.

라벨 또는 GUI 컴포넌트가 포인터 입력을 받으면 링크가 다음 메세지를 생성합니다. 라벨 메세지는 소유한 게임 오브젝트로, GUI 메세지는 GUI 스크립트로 전송됩니다.

| 메세지 | 전송 시점 |
| --- | --- |
| `text_object_hovered` | 포인터가 링크 안으로 들어갑니다. |
| `text_object_unhovered` | 포인터가 링크 밖으로 나갑니다. |
| `text_object_clicked` | 같은 링크 위에서 누른 포인터를 놓습니다. |

각 메세지에는 다음 필드가 포함됩니다.

| 필드 | 타입 | 설명 |
| --- | --- | --- |
| `id` | `hash` | 오브젝트의 `id` 속성 또는 생성된 레이아웃 오브젝트 id입니다. |
| `type` | `hash` | 레이아웃 오브젝트 타입이며 현재는 `hash("link")`입니다. |
| `src` | `string` | 어플리케이션에서 정의한 오브젝트의 `src` 속성 값이며, 없으면 빈 문자열입니다. |

```lua
function on_message(self, message_id, message)
    if message_id == hash("text_object_clicked") then
        assert(message.type == hash("link"))
        print(message.id, message.src)
    end
end
```

## 이름 있는 스타일 {#named-styles}

각 폰트 컬렉션에는 렌더링에만 적용되는 이름 있는 오브젝트 스타일이 포함되어 있습니다. 링크는 `style` 속성에서 지정한 이름의 스타일을 사용하며, 속성이 없으면 `link`를 사용합니다. 범용 `<style>` 구간 태그는 없습니다.

Defold는 다음 기본값을 제공합니다.

| 스타일 | 면 색상 배율 | 장식 |
| --- | --- | --- |
| `link` | `(0.10, 0.45, 0.90, 1.0)` | 실선 밑줄 |
| `link:hover` | `(0.30, 0.65, 1.00, 1.0)` | 없음 |
| `link:active` | `(0.05, 0.30, 0.70, 1.0)` | 없음 |

여는 태그를 포함한 텍스트 문자열로 스타일을 정의합니다. 태그는 역순으로 암묵적으로 닫히므로 닫는 태그나 보이는 텍스트는 허용되지 않습니다.

```lua
font.set_style("/fonts/ui.fontc", "link",
    "<color=#2673ff><outline color=#000000 size=1>")

font.set_style("/fonts/ui.fontc", "link:hover",
    "<color=#66b3ff><shake amplitude=0.2 hz=20>")
```

태그는 오브젝트 텍스트를 둘러싸며 중첩된 것처럼 왼쪽에서 오른쪽 순서로 적용됩니다. 호출자가 선택한 오브젝트 스타일은 기본 스타일 다음에 적용됩니다. 여러 태그가 같은 렌더 프로퍼티를 설정하면 나중에 적용된 값이 이전 값을 오버라이드합니다. 효과는 왼쪽에서 오른쪽 순서로 추가됩니다.

::: sidenote
`font.set_style()`을 호출하면 해당 이름의 스타일이 가진 렌더 프로퍼티와 효과를 대체합니다. 리소스에서 정의한 장식은 바뀌지 않으므로 `link`를 다시 정의해도 기본 밑줄은 제거되지 않습니다. 이름 있는 스타일은 `color`, `outline`, `shadow`, `gradient`, `wave`, `shake`처럼 렌더링에만 적용되는 태그를 허용합니다. 레이아웃을 바꾸는 태그, 장식 태그, 오브젝트 태그는 허용되지 않습니다.
:::

## 레이아웃 오브젝트 API {#layout-object-api}

배치된 텍스트에서 `sprite`와 `link` 오브젝트를 가져오려면 `label.get_layout_objects()` 또는 `gui.get_layout_objects()`를 사용합니다.

### `label.get_layout_objects()` {#labelget_layout_objects}

```lua
objects = label.get_layout_objects(url)
```

| 인자 | 타입 | 설명 |
| --- | --- | --- |
| `url` | `string`, `hash` 또는 `url` | 확인할 라벨 컴포넌트입니다. 예: `"#label"`. |

### `gui.get_layout_objects()` {#guiget_layout_objects}

```lua
objects = gui.get_layout_objects(node)
```

| 인자 | 타입 | 설명 |
| --- | --- | --- |
| `node` | `node` | 확인할 GUI 텍스트 노드입니다. 예: `gui.get_node("rich_text")`. |

두 함수는 현재 레이아웃 오브젝트를 소스 순서로 담은 새 배열을 반환합니다. 텍스트에 오브젝트 태그가 없으면 빈 배열을 반환합니다. 호출할 때마다 오브젝트와 속성을 Lua로 복사하므로 결과를 캐쉬하고, 텍스트나 레이아웃을 바꾸는 다른 프로퍼티를 변경한 후 다시 조회하세요.

### 반환된 오브젝트 필드 {#returned-object-fields}

| 필드 | 타입 | 설명 |
| --- | --- | --- |
| `type` | `string` | `"sprite"` 또는 `"link"`입니다. |
| `id` | `hash` | 상호작용 메세지에서 사용하는 오브젝트 식별자입니다. |
| `text_offset` | `number` | 보이는 텍스트에서 0부터 시작하는 위치이며 Unicode 코드 포인트 단위입니다. 마크업은 제외되며 엔티티는 디코딩된 문자로 계산합니다. 스프라이트의 경우 삽입 위치입니다. |
| `text_length` | `number` | 둘러싼 보이는 텍스트의 Unicode 코드 포인트 단위 길이입니다. 스프라이트는 삽입된 U+FFFC 오브젝트 대체 코드 포인트 때문에 길이가 1입니다. |
| `width` | `number` | 텍스트 레이아웃 단위로 계산된 너비입니다. 링크의 너비는 현재 0입니다. |
| `height` | `number` | 텍스트 레이아웃 단위로 계산된 높이입니다. 링크의 높이는 현재 0입니다. |
| `x` | `number` | 텍스트 레이아웃의 왼쪽 위 원점을 기준으로 한 오브젝트 왼쪽 아래 모서리의 수평 위치입니다. |
| `y` | `number` | 텍스트 레이아웃의 왼쪽 위 원점을 기준으로 한 오브젝트 왼쪽 아래 모서리의 수직 위치입니다. |
| `attributes` | `table` | 모든 태그 속성을 문자열 키/값 쌍으로 담습니다. 속성 값은 `"2em"`처럼 소스에서의 표현을 유지합니다. 이름 없는 축약값은 `value` 키에 저장됩니다. |

::: sidenote
`text_offset`과 `text_length`는 UTF-8 바이트 오프셋이 아닙니다. `å`나 `猫` 같은 비ASCII 문자는 위치 하나로 계산합니다.
:::

### Lua 예제 {#lua-example}

```lua
local text = [[
Read the <link src=https://defold.com/manuals/ id=manual>manual</link>
or inspect <sprite src=images/info.png width=2em/> for more information.
]]

go.set("#label", "text", text)

local objects = label.get_layout_objects("#label")
for _, object in ipairs(objects) do
    if object.type == "link" then
        print("link", object.attributes.src)
        print("visible range", object.text_offset, object.text_length)
        print("position", object.x, object.y)
    elseif object.type == "sprite" then
        print("sprite", object.x, object.y, object.width, object.height)
        pprint(object.attributes)
    end
end

local gui_objects = gui.get_layout_objects(gui.get_node("rich_text"))
```

## 유용한 조합 {#useful-combinations}

### 색상 외곽선과 수평 그라디언트 {#colored-outline-with-a-horizontal-gradient}

```text
<outline size=2 color=#101820>
    <gradient left=#FEE715 right=#FF6F61>Gradient title</gradient>
</outline>
```

그라디언트는 면 색상에만 곱해지며 외곽선은 자체 색상을 유지합니다.

### 문장 흔들기와 한 단어에 그라디언트 적용하기 {#shake-a-sentence-gradient-one-word}

```text
<shake hz=20 amplitude=0.5>
    This <gradient left=#FF00FF right=#FFFFFF>whole</gradient> text shakes!
</shake>
```

바깥쪽 위치 효과는 모든 글리프에 적용됩니다. 중첩된 색상 효과는 “whole”에만 적용됩니다.

### 다른 프로퍼티를 유지하면서 하나만 오버라이드하기 {#override-one-property-without-losing-the-others}

```text
<color=#FFFFFF><outline size=2 color=#000000>
    Normal <color=#FF4040>warning</color> normal
</outline></color>
```

안쪽 색상은 상속된 외곽선 너비와 색상을 유지하면서 면 색상을 바꿉니다.
