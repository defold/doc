---
title: Defold의 폰트 매뉴얼
brief: 이 매뉴얼은 Defold가 폰트를 처리하는 방식과 게임에서 폰트를 화면에 표시하는 방법을 설명합니다.
---

# 폰트 파일

폰트는 Label 컴포넌트와 GUI 텍스트 노드에서 텍스트를 렌더링하는 데 사용됩니다. Defold는 여러 폰트 파일 포멧을 지원합니다.

- TrueType
- OpenType
- BMFont

프로젝트에 추가된 폰트는 Defold가 렌더링할 수 있는 텍스쳐 포멧으로 자동 변환됩니다. 폰트 렌더링 기술은 두 가지가 있으며, 각각 고유한 장점과 단점이 있습니다.

- 비트맵
- 디스턴스 필드

## 오프라인 또는 런타임 폰트

기본적으로 래스터화된 글리프 이미지로 변환하는 작업은 빌드 시점(오프라인)에 이루어집니다. 이 방식은 각 폰트가 빌드 단계에서 가능한 모든 글리프를 래스터화해야 하므로, 메모리를 소비하고 번들 크기도 늘릴 수 있는 매우 큰 텍스쳐가 생성될 수 있다는 단점이 있습니다.

"runtime fonts"를 사용하면 `.ttf` 폰트가 원본 그대로 번들에 포함되고, 래스터화는 런타임에 필요할 때 수행됩니다. 이렇게 하면 런타임 메모리 사용량과 번들 크기를 모두 최소화할 수 있습니다.

## 텍스트 레이아웃 지원(예: 오른쪽에서 왼쪽)

런타임 폰트는 전체 텍스트 레이아웃, 예를 들어 오른쪽에서 왼쪽으로 쓰는 텍스트도 지원한다는 장점이 있습니다.
현재 [HarfBuzz](https://github.com/harfbuzz/harfbuzz), [SheenBidi](https://github.com/Tehreer/SheenBidi), [libunibreak](https://github.com/adah1972/libunibreak), [SkriBidi](https://github.com/memononen/Skribidi) 라이브러리를 사용합니다.

[런타임 폰트 활성화](/manuals/font#enabling-runtime-fonts)를 참고하세요.

## 폰트 컬렉션

`.fontc` 파일 포멧은 폰트 컬렉션이라고도 합니다. 오프라인 모드에서는 하나의 폰트만 연결됩니다.
런타임 폰트를 사용할 때는 둘 이상의 폰트 파일(`.ttf`)을 폰트 컬렉션에 연결할 수 있습니다.

이를 통해 여러 언어의 텍스트를 렌더링할 때 하나의 폰트 컬렉션을 사용하면서도 메모리 사용량을 낮게 유지할 수 있습니다.
예를 들어 일본어 폰트가 들어 있는 컬렉션을 로드한 다음, 해당 폰트를 현재 main 폰트에 연결하고, 이후 일본어 폰트 컬렉션을 언로드할 수 있습니다.

## 폰트 만들기

Defold에서 사용할 폰트를 만들려면 메뉴에서 <kbd>File ▸ New...</kbd>를 선택한 다음 <kbd>Font</kbd>를 선택해 새 Font 파일을 만듭니다. *Assets* 브라우저의 원하는 위치를 <kbd>right click</kbd>하고 <kbd>New... ▸ Font</kbd>를 선택할 수도 있습니다.

![New font name](images/font/new_font_name.png)

새 폰트 파일의 이름을 지정하고 <kbd>Ok</kbd>를 클릭합니다. 그러면 새 폰트 파일이 에디터에서 열립니다.

![New font](images/font/new_font.png)

사용할 폰트를 *Assets* 브라우저로 드래그해 적절한 위치에 놓습니다.

*Font* 프로퍼티를 폰트 파일로 설정하고 필요에 따라 폰트 프로퍼티를 설정합니다.

## 프로퍼티 {#properties}

*Font*
: 폰트 데이터를 생성하는 데 사용할 TTF, OTF 또는 *`.fnt`* 파일입니다.

*Material*
: 이 폰트를 렌더링할 때 사용할 메터리얼입니다. 디스턴스 필드와 BMFonts를 사용할 때는 이 값을 변경해야 합니다. 자세한 내용은 아래를 참고하세요.

*Output Format*
: 생성되는 폰트 데이터의 타입입니다.

  - `TYPE_BITMAP`은 임포트한 OTF 또는 TTF 파일을 폰트 시트 텍스쳐로 변환하며, 비트맵 데이터를 사용해 텍스트 노드를 렌더링합니다. 컬러 채널은 글자 면 모양, 외곽선, 드롭 섀도우를 인코딩하는 데 사용됩니다. *`.fnt`* 파일의 경우 소스 텍스쳐 비트맵이 그대로 사용됩니다.
  - `TYPE_DISTANCE_FIELD`는 임포트한 폰트를 폰트 시트 텍스쳐로 변환하며, 픽셀 데이터가 화면 픽셀이 아니라 폰트 가장자리까지의 거리를 나타냅니다. 자세한 내용은 아래를 참고하세요.

*Render Mode*
: 글리프 렌더링에 사용할 렌더 모드입니다.

  - `MODE_SINGLE_LAYER`는 각 문자마다 하나의 쿼드를 생성합니다.
  - `MODE_MULTI_LAYER`는 글리프 모양, 외곽선, 그림자에 대해 각각 별도의 쿼드를 생성합니다. 레이어는 뒤에서 앞으로 순서대로 렌더링되므로, 외곽선이 글리프 사이의 거리보다 넓더라도 문자가 이전에 렌더링된 문자를 가리지 않습니다. 이 렌더 모드는 폰트 리소스의 Shadow X/Y 프로퍼티에 지정된 대로 드롭 섀도우 오프셋도 올바르게 적용합니다.

*Size*
: 글리프의 목표 크기입니다. 단위는 픽셀입니다.

*Antialias*
: 폰트를 타겟 비트맵에 bake할 때 안티알리아싱을 적용할지 여부입니다. 픽셀 퍼펙트 폰트 렌더링을 원한다면 0으로 설정하세요.

*Alpha*
: 글리프의 투명도입니다. 범위는 0.0--1.0이며, 0.0은 투명, 1.0은 불투명을 의미합니다.

*Outline Alpha*
: 생성된 외곽선의 투명도입니다. 범위는 0.0--1.0입니다.

*Outline Width*
: 생성된 외곽선의 너비입니다. 단위는 픽셀입니다. 외곽선을 사용하지 않으려면 0으로 설정하세요.

*Shadow Alpha*
: 생성된 그림자의 투명도입니다. 범위는 0.0--1.0입니다.

::: sidenote
그림자 지원은 내장 폰트 메터리얼 쉐이더에서 활성화되며, 단일 레이어와 다중 레이어 렌더 모드를 모두 처리합니다. 레이어드 폰트 렌더링이나 그림자 지원이 필요하지 않다면 *`builtins/font-singlelayer.fp`* 같은 더 단순한 쉐이더를 사용하는 것이 좋습니다.
:::

*Shadow Blur*
: 비트맵 폰트의 경우 이 설정은 각 폰트 글리프에 작은 블러 커널을 적용하는 횟수를 나타냅니다. 디스턴스 필드 폰트의 경우 이 설정은 실제 블러의 픽셀 너비와 같습니다.

*Shadow X/Y*
: 생성된 그림자의 가로 및 세로 오프셋입니다. 단위는 픽셀입니다. 이 설정은 Render Mode가 `MODE_MULTI_LAYER`로 설정된 경우에만 글리프 그림자에 영향을 줍니다.

*Characters*
: 폰트에 포함할 문자입니다. 기본적으로 이 필드에는 ASCII 출력 가능 문자(문자 코드 32-126)가 포함됩니다. 이 필드에서 문자를 추가하거나 제거해 폰트에 더 많거나 더 적은 문자를 포함할 수 있습니다.

런타임 폰트의 경우 이 텍스트는 올바른 글리프로 캐쉬를 미리 준비하는 역할을 합니다. 이 작업은 로드 시점에 수행됩니다. `font.prewarm_text()`를 참고하세요.

::: sidenote
ASCII 출력 가능 문자는 다음과 같습니다:
space ! " # $ % & ' ( ) * + , - . / 0 1 2 3 4 5 6 7 8 9 : ; < = > ? @ A B C D E F G H I J K L M N O P Q R S T U V W X Y Z [ \ ] ^ _ \` a b c d e f g h i j k l m n o p q r s t u v w x y z { | } ~
:::

*All Chars*
: 이 프로퍼티를 체크하면 소스 파일에서 사용할 수 있는 모든 글리프가 출력에 포함됩니다.

*Cache Width/Height*
: 글리프 캐쉬 비트맵의 크기를 제한합니다. 엔진이 텍스트를 렌더링할 때 캐쉬 비트맵에서 글리프를 찾습니다. 글리프가 캐쉬에 없으면 렌더링 전에 캐쉬에 추가됩니다. 캐쉬 비트맵이 너무 작아서 엔진이 렌더링하라는 모든 글리프를 담을 수 없으면 에러가 발생합니다(`ERROR:RENDER: Out of available cache cells! Consider increasing cache_width or cache_height for the font.`).

  0으로 설정하면 캐쉬 크기가 자동으로 설정되며, 최대 2048x4096까지 커집니다.

## 디스턴스 필드 폰트

디스턴스 필드 폰트는 비트맵 데이터 대신 텍스쳐에 글리프 가장자리까지의 거리를 저장합니다. 엔진이 폰트를 렌더링할 때는 이 거리 데이터를 해석하고 이를 사용해 글리프를 그리는 특수한 쉐이더가 필요합니다. 디스턴스 필드 폰트는 비트맵 폰트보다 리소스를 더 많이 사용하지만, 크기 조절의 유연성이 더 큽니다.

![Distance field font](images/font/df_font.png)

폰트를 만들 때 *Material* 프로퍼티를 *`builtins/fonts/font-df.material`*(또는 디스턴스 필드 데이터를 처리할 수 있는 다른 메터리얼)로 변경해야 합니다. 그렇지 않으면 폰트가 화면에 렌더링될 때 올바른 쉐이더를 사용하지 않습니다.

## 비트맵 BMFonts {#bitmap-bmfonts}

생성된 비트맵 외에도 Defold는 미리 bake된 비트맵 "BMFont" 포멧의 폰트를 지원합니다. 이 폰트는 모든 글리프가 들어 있는 PNG 폰트 시트로 구성됩니다. 또한 *`.fnt`* 파일에는 시트에서 각 글리프가 어디에 있는지에 대한 정보와 크기 및 커닝 정보가 들어 있습니다. Defold는 Phaser와 일부 다른 도구에서 사용하는 *`.fnt`* 포멧의 XML 버전을 지원하지 않는다는 점에 유의하세요.

이런 타입의 폰트는 TrueType 또는 OpenType 폰트 파일에서 생성된 비트맵 폰트에 비해 성능 향상을 제공하지는 않지만, 임의의 그래픽, 색상, 그림자를 이미지에 직접 포함할 수 있습니다.

생성된 *`.fnt`* 및 *`.png`* 파일을 Defold 프로젝트에 추가합니다. 이 파일들은 같은 폴더에 있어야 합니다. 새 폰트 파일을 만들고 *font* 프로퍼티를 *`.fnt`* 파일로 설정합니다. *output_format*이 `TYPE_BITMAP`으로 설정되어 있는지 확인하세요. Defold는 비트맵을 생성하지 않고 PNG에서 제공된 비트맵을 사용합니다.

::: sidenote
BMFont를 만들려면 적절한 파일을 생성할 수 있는 도구를 사용해야 합니다. 여러 선택지가 있습니다.

* [Bitmap Font Generator](http://www.angelcode.com/products/bmfont/), AngelCode에서 제공하는 Windows 전용 도구입니다.
* [Shoebox](http://renderhjs.net/shoebox/), Windows와 macOS용 무료 Adobe Air 기반 앱입니다.
* [Hiero](https://libgdx.com/wiki/tools/hiero), 오픈 소스 Java 기반 도구입니다.
* [Glyph Designer](https://71squared.com/glyphdesigner), 71 Squared의 상용 macOS 도구입니다.
* [bmGlyph](https://www.bmglyph.com), Sovapps의 상용 macOS 도구입니다.
:::

![BMfont](images/font/bm_font.png)

폰트가 올바르게 렌더링되도록 하려면 폰트를 만들 때 material 프로퍼티를 *`builtins/fonts/font-fnt.material`*로 설정하는 것을 잊지 마세요.

## 아티팩트와 모범 사례

일반적으로 비트맵 폰트는 폰트가 스케일링 없이 렌더링될 때 가장 적합합니다. 비트맵 폰트는 디스턴스 필드 폰트보다 화면에 더 빠르게 렌더링됩니다.

디스턴스 필드 폰트는 확대에 매우 잘 대응합니다. 반면 비트맵 폰트는 단순한 픽셀 이미지이므로 폰트가 스케일링될수록 픽셀도 커져 각진 아티팩트가 생깁니다. 다음은 폰트 크기 48픽셀의 샘플을 4배로 확대해 스케일링한 예입니다.

![Fonts scaled up](images/font/scale_up.png)

축소할 때는 비트맵 텍스쳐를 GPU가 깔끔하고 효율적으로 축소하고 안티알리아싱할 수 있습니다. 비트맵 폰트는 디스턴스 필드 폰트보다 색상을 더 잘 유지합니다. 다음은 같은 샘플 폰트를 48픽셀 크기에서 1/5 크기로 축소한 확대 이미지입니다.

![Fonts scaled down](images/font/scale_down.png)

디스턴스 필드 폰트는 폰트 글리프의 곡선을 표현할 수 있는 거리 정보를 담을 만큼 충분히 큰 타겟 크기로 렌더링되어야 합니다. 다음은 위와 같은 폰트이지만 18픽셀 크기에서 10배로 확대해 스케일링한 것입니다. 이 서체의 모양을 인코딩하기에는 너무 작다는 점이 분명합니다.

![Distance field artifacts](images/font/df_artifacts.png)

그림자나 외곽선 지원이 필요하지 않다면 각각의 알파 값을 0으로 설정하세요. 그렇지 않으면 그림자와 외곽선 데이터가 계속 생성되어 불필요한 메모리를 차지합니다.

## 폰트 캐쉬

Defold의 폰트 리소스는 런타임에 텍스쳐와 폰트 데이터, 두 가지로 나타납니다.

* 폰트 데이터는 글리프 항목 목록으로 구성되며, 각 항목에는 기본 커닝 정보와 해당 글리프의 비트맵 데이터가 들어 있습니다.
* 텍스쳐는 내부적으로 "glyph cache texture"라고 불리며, 특정 폰트의 텍스트를 렌더링할 때 사용됩니다.

런타임에 텍스트를 렌더링할 때 엔진은 먼저 렌더링할 글리프를 순회하며 텍스쳐 캐쉬에서 어떤 글리프를 사용할 수 있는지 확인합니다. 글리프 텍스쳐 캐쉬에 없는 각 글리프는 폰트 데이터에 저장된 비트맵 데이터에서 텍스쳐 업로드를 유발합니다.

각 글리프는 폰트 기준선에 따라 내부적으로 캐쉬에 배치됩니다. 이를 통해 쉐이더에서 해당 캐쉬 셀 안의 글리프 로컬 텍스쳐 좌표를 계산할 수 있습니다. 즉, 그라디언트나 텍스쳐 오버레이 같은 특정 텍스트 효과를 동적으로 구현할 수 있습니다. 엔진은 `texture_size_recip`이라는 특수 쉐이더 상수를 통해 캐쉬에 대한 메트릭을 쉐이더에 노출하며, 이 상수는 벡터 컴포넌트에 다음 정보를 포함합니다.

* `texture_size_recip.x`는 캐쉬 너비의 역수입니다.
* `texture_size_recip.y`는 캐쉬 높이의 역수입니다.
* `texture_size_recip.z`는 캐쉬 셀 너비와 캐쉬 너비의 비율입니다.
* `texture_size_recip.w`는 캐쉬 셀 높이와 캐쉬 높이의 비율입니다.

예를 들어 쉐이더 프래그먼트에서 그라디언트를 생성하려면 다음과 같이 작성하면 됩니다.

`float horizontal_gradient = fract(var_texcoord0.y / texture_size_recip.w);`

쉐이더 uniform에 대한 자세한 내용은 [쉐이더 매뉴얼](/manuals/shader)을 참고하세요.

## 런타임 폰트 활성화 {#enabling-runtime-fonts}

TrueType(`.ttf`) 폰트를 사용할 때 SDF 타입 폰트에 런타임 생성을 사용할 수 있습니다.
이 방식은 Defold 게임의 다운로드 크기와 런타임 메모리 사용량을 크게 줄일 수 있습니다.
작은 단점은 각 글리프를 생성하는 작업이 비동기적이라는 점입니다.

* `game.project`에서 `font.runtime_generation`을 설정해 이 기능을 활성화합니다.

* [App Manifest](/manuals/app-manifest)를 추가하고 `Use full text layout system` 옵션을 활성화합니다.
이렇게 하면 이 기능이 활성화된 커스텀 엔진이 빌드됩니다.

::: sidenote
이 기능은 현재 실험적 기능이지만, 앞으로 기본 워크플로우로 사용할 의도로 제공됩니다.
:::

::: important
`font.runtime_generation` 설정은 프로젝트의 모든 `.ttf` 폰트에 영향을 줍니다.
:::


### 폰트 스크립팅

#### 글리프 캐쉬 프리워밍

런타임 폰트를 더 쉽게 사용할 수 있도록, 런타임 폰트는 글리프 캐쉬 프리워밍을 지원합니다.
이는 폰트의 *Characters*에 나열된 글리프를 폰트가 생성한다는 뜻입니다.

::: sidenote
`All Chars`가 선택되어 있으면 모든 글리프를 한 번에 생성하지 않으려는 목적에 어긋나므로 프리워밍이 수행되지 않습니다.
:::

`.fontc` 파일의 `Characters` 필드가 설정되어 있으면, 이 값은 글리프 캐쉬에서 어떤 글리프를 업데이트해야 하는지 알아내기 위한 텍스트로 사용됩니다.

`font.prewarm_text(font_collection, text, callback)`을 호출해 글리프 캐쉬를 수동으로 업데이트할 수도 있습니다. 이 함수는 누락된 모든 글리프가 글리프 캐쉬에 추가되어 텍스트를 화면에 표시해도 안전한 시점을 알려 주는 콜백을 제공합니다.

### 폰트 컬렉션에 폰트 추가/제거

런타임 폰트에서는 폰트 컬렉션에 폰트(`.ttf`)를 추가하거나 제거할 수 있습니다.
이는 큰 폰트를 여러 문자 세트(예: CJK)에 맞춰 여러 파일로 분할한 경우 유용합니다.

::: important
폰트 컬렉션에 폰트를 추가해도 모든 글리프가 자동으로 로드되거나 렌더링되지는 않습니다.
:::

```lua
function init(self)
    -- Get the target font collection.
    self.font_collection = go.get("#label", "font")

    -- Get the first font assigned to the selected language collection.
    local language_collection = go.get("localization_japanese#label", "font")
    local font_info = font.get_info(language_collection)
    self.language_ttf_hash = font_info.fonts[1].path_hash

    -- Associate it with the target collection and increase its reference count.
    font.add_font(self.font_collection, self.language_ttf_hash)
end
```

```lua
function final(self)
    -- Remove the association and release the font reference.
    font.remove_font(self.font_collection, self.language_ttf_hash)
end
```

### 글리프 프리워밍

런타임 폰트로 텍스트를 올바르게 표시하려면 글리프가 해석되어야 합니다. `font.prewarm_text()`가 이 작업을 대신 수행합니다.
이 작업은 비동기 작업이며, 완료되어 콜백을 받으면 해당 글리프가 포함된 모든 메세지를 안전하게 표시할 수 있습니다.

::: important
글리프 캐쉬가 가득 차면 캐쉬에서 가장 오래된 글리프가 제거됩니다.
:::

```lua
font.prewarm_text(self.font_collection, info.text, function (self, request_id, result, err)
    if result then
      print("PREWARMING OK!")
      label.set_text(self.label, info.text)
    else
      print("Error prewarming text:", err)
    end
  end)
```
