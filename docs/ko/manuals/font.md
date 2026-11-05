---
title: Defold의 폰트 매뉴얼
brief: 이 매뉴얼은 Defold가 폰트를 처리하는 방식과 게임에서 폰트를 화면에 표시하는 방법을 설명합니다.
---

# 폰트 파일

폰트는 Label 컴포넌트와 GUI 텍스트 노드에서 텍스트를 렌더링하는 데 사용됩니다. Defold는 여러 폰트 파일 포멧을 지원합니다.

- TrueType
- OpenType
- BMFont

레거시 및 전체 텍스트 레이아웃 엔진 모두 TrueType 외곽선과 OpenType CFF1/CFF2 외곽선을 지원하며, `.ttf` 및 `.otf` 리소스의 런타임 생성도 지원합니다.

개별 텍스트 구간에 스타일을 적용하고 링크와 인라인 스프라이트를 사용하는 방법은 [리치 텍스트 마크업 매뉴얼](/manuals/font-richtext)을 참고하세요.

TrueType 및 OpenType 폰트에서는 *Mode* 프로퍼티로 글리프 렌더링 방식을 선택합니다:

- **Bitmap**은 래스터화한 글리프 이미지를 사용합니다.
- **SDF**(signed distance field)는 텍스쳐에 글리프 경계까지의 거리를 저장하여 Bitmap보다 유연하게 크기를 조절할 수 있습니다.
- **Vector**는 곡선 데이터에서 글리프 면을 렌더링하여 크기를 바꿔도 선명함을 유지합니다. 외곽선과 그림자 효과는 여전히 비트맵 데이터를 사용합니다.

새로 만든 폰트 리소스는 **Vector** 모드와 **Dynamic** 글리프 생성을 사용합니다. 기존 폰트 리소스는 Bitmap 또는 SDF 모드를 유지합니다. BMFont 소스는 항상 제공된 비트맵을 사용합니다.

Vector 모드는 `RGBA16F`와 `R32UI` 텍스쳐를 지원하는 그래픽 기능이 필요하며 OpenGL ES 2나 WebGL 1에서는 지원되지 않습니다. 미지원 그래픽 어댑터를 타겟으로 할 때는 Bitmap 또는 SDF 폰트와 해당 메터리얼을 사용하세요. Vector에서 SDF로 자동 전환되지 않습니다. 설정 방법은 [벡터 폰트](#vector-fonts)를 참고하세요.

## 오프라인 또는 런타임 폰트

*Glyph Generation* 프로퍼티는 각 폰트의 글리프 데이터를 언제 생성할지 선택합니다:

- **Static**은 빌드 시점(오프라인)에 선택한 글리프를 생성합니다. *Characters*와 *All Chars*로 포함할 글리프를 제어합니다. 원본 `.ttf` 또는 `.otf` 파일은 런타임 생성을 위해 번들에 포함되지 않습니다.
- **Dynamic**은 원본 `.ttf` 또는 `.otf` 파일을 번들에 포함하고 런타임에 필요에 따라 글리프를 생성합니다. *Prewarm Text*는 폰트가 로드될 때 글리프를 준비합니다. 다른 글리프는 나중에 필요할 때 생성할 수 있습니다.

SDF와 Vector 폰트는 두 방식을 모두 지원합니다. Bitmap 폰트와 BMFont 소스는 Static 생성을 사용합니다. 각 폰트 리소스를 독립적으로 설정하므로 한 프로젝트에서 Static과 Dynamic 폰트를 함께 사용할 수 있습니다.

동적 생성은 특히 문자 집합이 큰 폰트에서 번들 크기와 런타임 메모리 사용량을 줄일 수 있습니다. 엔진의 전체 텍스트 레이아웃 시스템이 필요합니다. [런타임 폰트 활성화](#enabling-runtime-fonts)를 참고하세요.

<a id="text-layout-support-eg-right-to-left"></a>

## 텍스트 레이아웃 지원(예: 오른쪽에서 왼쪽)

런타임 폰트는 전체 텍스트 레이아웃, 예를 들어 오른쪽에서 왼쪽으로 쓰는 텍스트도 지원한다는 장점이 있습니다.
현재 [HarfBuzz](https://github.com/harfbuzz/harfbuzz), [SheenBidi](https://github.com/Tehreer/SheenBidi), [libunibreak](https://github.com/adah1972/libunibreak), [SkriBidi](https://github.com/memononen/Skribidi) 라이브러리를 사용합니다.

[런타임 폰트 활성화](/manuals/font#enabling-runtime-fonts)를 참고하세요.

에디터는 폰트와 씬 텍스트의 미리보기에 엔진의 폰트 렌더러를 사용합니다. 텍스트 셰이핑과 오른쪽에서 왼쪽으로 쓰는 레이아웃에는 [런타임 폰트](#enabling-runtime-fonts)와 App Manifest의 **Use full text layout system** 옵션이 필요합니다. 오프라인 폰트의 미리보기는 폰트의 **Characters** 및 **All Chars** 설정을 따릅니다.

## 폰트 컬렉션

`.fontc` 파일 포멧은 폰트 컬렉션이라고도 합니다. 오프라인 모드에서는 하나의 폰트만 연결됩니다.
런타임 폰트를 사용할 때는 둘 이상의 폰트 파일(`.ttf` 또는 `.otf`)을 폰트 컬렉션에 연결할 수 있습니다.

이를 통해 여러 언어의 텍스트를 렌더링할 때 하나의 폰트 컬렉션을 사용하면서도 메모리 사용량을 낮게 유지할 수 있습니다.
예를 들어 일본어 폰트가 들어 있는 컬렉션을 로드한 다음, 해당 폰트를 현재 main 폰트에 연결하고, 이후 일본어 폰트 컬렉션을 언로드할 수 있습니다.

## 폰트 만들기

Defold에서 사용할 폰트를 만들려면 메뉴에서 <kbd>File ▸ New...</kbd>를 선택한 다음 <kbd>Font</kbd>를 선택해 새 Font 파일을 만듭니다. *Assets* 브라우저의 원하는 위치를 <kbd>right click</kbd>하고 <kbd>New... ▸ Font</kbd>를 선택할 수도 있습니다.

![New font name](images/font/new_font_name.png)

새 폰트 파일의 이름을 지정하고 <kbd>Ok</kbd>를 클릭합니다. 그러면 새 폰트 파일이 에디터에서 열립니다.

사용할 폰트를 *Assets* 브라우저로 드래그해 적절한 위치에 놓습니다.

*Font* 프로퍼티를 폰트 파일로 설정합니다. `.ttf` 또는 `.otf` 소스는 *Mode*와 *Glyph Generation*을 선택하고 나머지 프로퍼티를 필요에 맞게 설정합니다. Dynamic 생성을 사용할 때는 [런타임 폰트 설정](#enabling-runtime-fonts)도 완료하세요.

![Font properties with Vector mode and Dynamic glyph generation](images/font/font_properties.png)

Vector 폰트의 표시 크기는 Label 컴포넌트나 GUI 텍스트 노드의 *Font Size*로 변경합니다. *Outline/Shadow Bitmap Size*는 표시 크기와 독립적으로 효과 비트맵의 해상도를 제어합니다.

Bitmap과 SDF 폰트에서는 폰트 리소스의 *Size*로 생성할 글리프 크기를 선택합니다. BMFont 크기는 원본 `.fnt` 파일에서 가져옵니다. 이러한 폰트의 표시 크기를 바꾸려면 Label 컴포넌트나 GUI 텍스트 노드를 스케일링합니다.

## 프로퍼티 {#properties}

*Font*
: 폰트 데이터를 생성하는 데 사용할 TTF, OTF 또는 *`.fnt`* 파일입니다.

*Material*
: 폰트 렌더링에 사용할 메터리얼입니다. 폰트 모드와 일치해야 합니다. [폰트 메터리얼](#font-materials)을 참고하세요.

*Mode*
: `.ttf` 또는 `.otf` 소스의 렌더링 기법으로 **Bitmap**, **SDF**, **Vector**를 선택합니다. 이전의 *Output Format* 프로퍼티를 대체합니다. BMFont 소스에는 표시되지 않습니다.

*Glyph Generation*
: **Static**은 빌드 시점에 글리프 데이터를 생성합니다. **Dynamic**은 런타임에 생성하며 [전체 텍스트 레이아웃 시스템](#enabling-runtime-fonts)이 필요합니다. 이 프로퍼티는 SDF와 Vector 폰트에 사용할 수 있습니다. Bitmap 모드에서는 Static으로 고정되며 BMFont 소스에는 표시되지 않습니다.

*Render Mode*
: 생성된 Bitmap 폰트의 레이어 구성입니다. `.ttf`와 `.otf` 소스의 Bitmap 모드에서만 표시됩니다. SDF, Vector, BMFont 소스의 레이어 구성은 Defold가 자동으로 선택합니다.

  - **Single Layer**는 문자마다 하나의 쿼드를 만듭니다.
  - **Multi Layer**는 글리프 모양, 외곽선, 그림자의 쿼드를 각각 만듭니다. 레이어는 뒤에서 앞으로 렌더링하므로 외곽선이 글리프 간격보다 넓어도 앞서 렌더링한 문자를 가리지 않습니다. *Shadow X/Y* 프로퍼티의 그림자 오프셋도 사용할 수 있습니다.

*Size*
: Bitmap 또는 SDF 폰트 데이터 생성에 사용할 글리프 크기(픽셀)입니다. BMFont 소스는 `.fnt` 파일에서 크기를 읽으며 여기에서 수정할 수 없습니다.

*Outline/Shadow Bitmap Size*
: Vector 모드에서 *Size*를 대체합니다. Static과 Dynamic 생성 모두에서 활성화된 외곽선과 그림자 효과의 비트맵 해상도를 제어합니다. 두 효과가 모두 꺼져 있으면 글리프 면은 곡선 데이터를 사용하므로 이 프로퍼티도 비활성화됩니다. Label이나 GUI 텍스트 노드의 *Font Size*를 바꿔도 이 공유 비트맵 해상도는 바뀌지 않습니다.

*Antialias*
: Bitmap 폰트 데이터를 생성할 때 글리프에 안티알리아싱을 적용할지 여부입니다. 픽셀 퍼펙트 렌더링에는 비활성화하세요. `.ttf`와 `.otf` 소스의 Bitmap 모드에서만 표시됩니다.

*Alpha*
: 글리프의 투명도입니다. 범위는 0.0--1.0이며, 0.0은 투명, 1.0은 불투명을 의미합니다.

*Outline Alpha*
: 생성된 외곽선의 투명도입니다. 범위는 0.0--1.0입니다.

*Outline Width*
: 생성된 외곽선의 너비입니다. 단위는 픽셀입니다. 외곽선을 사용하지 않으려면 0으로 설정하세요.

*Shadow Alpha*
: 생성된 그림자의 투명도입니다. 범위는 0.0--1.0입니다.

::: sidenote
내장 Bitmap 폰트 쉐이더는 *Single Layer*와 *Multi Layer* 렌더 모드 모두에서 그림자를 지원합니다. *Single Layer* 렌더링을 사용하고 그림자가 필요 없는 생성형 Bitmap 폰트는 커스텀 메터리얼에서 `/builtins/fonts/font-singlelayer.fp`를 사용할 수 있습니다. SDF와 Vector 폰트는 모드에 맞는 쉐이더가 필요합니다. [폰트 메터리얼](#font-materials)을 참고하세요.
:::

*Shadow Blur*
: 생성된 그림자에 적용할 블러 양입니다. 선명한 그림자는 0으로 설정합니다.

*Shadow X/Y*
: 생성된 그림자의 가로 및 세로 오프셋(픽셀)입니다. 생성형 Bitmap 폰트에서는 *Multi Layer* 렌더 모드를 사용해야 오프셋이 적용됩니다. SDF와 Vector 폰트는 Defold가 적절한 레이어를 자동으로 선택합니다.

*Characters*
: Static 생성에서 빌드된 폰트에 포함할 문자입니다. 기본적으로 ASCII 출력 가능 문자(문자 코드 32-126)가 들어 있습니다. 문자를 추가하거나 제거하여 런타임에 사용할 글리프를 제어합니다.

*Prewarm Text*
: Dynamic 생성에서 *Characters*를 대체합니다. 폰트가 로드될 때 이 텍스트로 글리프를 생성하고 캐쉬를 미리 준비합니다. 이후 생성할 수 있는 문자를 제한하지는 않습니다. 스크립트의 [`font.prewarm_text()`](/ref/font/#font.prewarm_text)로도 텍스트를 미리 준비할 수 있습니다.

::: sidenote
ASCII 출력 가능 문자는 다음과 같습니다:
space ! " # $ % & ' ( ) * + , - . / 0 1 2 3 4 5 6 7 8 9 : ; < = > ? @ A B C D E F G H I J K L M N O P Q R S T U V W X Y Z [ \ ] ^ _ \` a b c d e f g h i j k l m n o p q r s t u v w x y z { | } ~
:::

*All Chars*
: Static 생성에서 *Characters*로 제한하지 않고 소스의 모든 글리프를 포함합니다. Dynamic 폰트에서는 숨겨집니다.

*Cache Width/Height*
: Bitmap 및 SDF 폰트와 Vector 외곽선/그림자 효과가 사용하는 글리프 캐쉬 비트맵의 크기를 제한합니다. 엔진은 텍스트를 렌더링할 때 캐쉬 비트맵에서 글리프를 찾습니다. 없으면 렌더링 전에 캐쉬에 추가합니다. 요청된 모든 글리프를 담기에 캐쉬 비트맵이 너무 작으면 오류가 발생합니다(`ERROR:RENDER: Out of available cache cells! Consider increasing cache_width or cache_height for the font.`).

  0으로 설정하면 캐쉬 크기가 자동으로 설정되며, 최대 2048x4096까지 커집니다.

## 폰트 메터리얼 {#font-materials}

폰트 모드와 일치하는 메터리얼을 사용하세요. GUI 텍스트 노드는 폰트 리소스의 *Material*을 사용합니다. Label 컴포넌트에는 별도의 *Material* 프로퍼티가 있으며 이것도 폰트와 일치해야 합니다:

| 폰트 모드 또는 소스 | GUI 텍스트용 폰트 메터리얼 | Label 컴포넌트 메터리얼 |
| --- | --- | --- |
| Bitmap | `/builtins/fonts/font.material` | `/builtins/fonts/label.material` |
| SDF | `/builtins/fonts/font-df.material` | `/builtins/fonts/label-df.material` |
| Vector | `/builtins/fonts/font-vector.material` | `/builtins/fonts/label-vector.material` |
| BMFont (`.fnt`) | `/builtins/fonts/font-fnt.material` | `/builtins/fonts/label-fnt.material` |

폰트에 내장 Bitmap, SDF, Vector 메터리얼 중 하나가 이미 할당되어 있으면 폰트 에디터에서 *Mode*를 변경할 때 해당 모드의 내장 메터리얼로 전환합니다. 커스텀 메터리얼은 자동으로 교체되지 않습니다. 폰트를 사용하는 Label 컴포넌트의 *Material* 프로퍼티도 확인하세요.

## 벡터 폰트 {#vector-fonts}

벡터 폰트는 곡선으로 글리프 면을 렌더링하므로 텍스트 표시 크기를 바꿔도 선명함을 유지합니다. 런타임에 글리프를 생성하는 폰트를 설정하려면:

1. `/fonts/ui.font` 같은 `.font` 리소스를 만들고 *Font* 프로퍼티에서 TrueType 또는 OpenType 소스를 선택합니다. 일반 텍스트에는 내장 `/builtins/fonts/vera_mo_bd.ttf`를 사용할 수 있습니다.
2. *Mode*를 **Vector**, *Glyph Generation*을 **Dynamic**, *Material*을 `/builtins/fonts/font-vector.material`로 설정합니다. 새 폰트 리소스의 기본값입니다.
3. 프로젝트에 지정한 App Manifest에서 **Use full text layout system**을 활성화합니다. [런타임 폰트 활성화](#enabling-runtime-fonts)에 따라 커스텀 엔진을 설정하세요.
4. *game.project*에서 [Shader ▸ Exclude GLES 2.0](/manuals/project-settings/#exclude-gles-20)을 활성화합니다.
5. 폰트를 [Label](/manuals/label/)에 지정하거나 GUI 씬의 *Fonts*에 추가하고 [텍스트 노드](/manuals/gui-text/)에서 선택합니다. Label은 컴포넌트의 *Material*도 `/builtins/fonts/label-vector.material`로 설정합니다. 컴포넌트나 노드의 *Font Size*를 원하는 표시 크기로 설정합니다.

벡터 글리프의 면은 곡선 텍스쳐를 사용하지만 활성화된 외곽선과 그림자는 여전히 SDF 비트맵 데이터를 생성하고 글리프 캐쉬 텍스쳐 메모리를 사용합니다. *Outline/Shadow Bitmap Size*는 Label이나 GUI 텍스트 노드의 *Font Size*와 독립적으로 비트맵 해상도를 설정합니다. 효과가 필요하지 않으면 *Outline Alpha*와 *Shadow Alpha*를 `0`으로 설정하여 비트맵 데이터 생성을 피하세요.

### 컬러 이모지 {#color-emoji}

벡터 폰트는 팔레트 색상과 선형/방사형 그라디언트를 포함한 COLRv1 컬러 이모지를 렌더링할 수 있습니다. Bitmap과 SDF 모드는 COLRv1 색상을 렌더링하지 않습니다. 위의 Dynamic Vector 설정을 사용한 다음 폰트 컬렉션의 대체 폰트로 COLRv1 이모지 폰트를 추가하세요. 일반 텍스트는 원래 폰트를 계속 사용합니다.

예를 들어 COLRv1 [Noto Color Emoji 폰트](https://github.com/google/fonts/blob/main/ofl/notocoloremoji/NotoColorEmoji-Regular.ttf)를 프로젝트에 `/fonts/NotoColorEmoji-Regular.ttf`로 복사합니다. 반드시 COLRv1 버전을 선택하세요. 다른 이모지 폰트는 파일명이 `.ttf`로 끝나더라도 다른 색상 포멧을 사용할 수 있습니다.

*game.project*의 **Project ▸ Custom Resources**에 `/fonts/NotoColorEmoji-Regular.ttf`를 추가합니다. 다른 커스텀 리소스가 없다면 설정은 다음과 같습니다:

```ini
[project]
custom_resources = /fonts/NotoColorEmoji-Regular.ttf
```

Lua에 폰트 경로를 작성하는 것만으로 폰트 파일이 번들에 포함되지는 않습니다. [Custom Resources](/manuals/project-settings/#custom-resources)는 리소스 시스템을 통해 폰트를 로드하는 [`font.add_font()`](/ref/font/#font.add_font)에서 원본 폰트를 사용할 수 있게 합니다. 번들에서 로드할 때 원본 폰트의 문자열 경로를 전달하세요.

공유 폰트 리소스마다 대체 폰트를 한 번만 추가하세요. 변경은 해당 폰트를 사용하는 모든 Label과 GUI 텍스트 노드에 적용되며, 같은 대체 폰트를 두 번 추가하면 오류가 발생합니다. 같은 `.font`로 [Label 예제](/manuals/label/#vector-fonts-and-color-emoji)와 [GUI 예제](/manuals/gui-text/#vector-fonts-and-color-emoji)를 함께 사용한다면, 어느 예제든 텍스트를 미리 준비하거나 표시하기 전에 대체 폰트를 한 번만 추가하도록 초기화를 조정하세요. 예제는 대체 폰트를 추가한 후 전체 텍스트를 미리 준비하고 콜백이 성공하면 표시합니다.

## 디스턴스 필드 폰트

디스턴스 필드 폰트는 비트맵 데이터 대신 텍스쳐에 글리프 가장자리까지의 거리를 저장합니다. 엔진이 폰트를 렌더링할 때는 이 거리 데이터를 해석하고 이를 사용해 글리프를 그리는 특수한 쉐이더가 필요합니다. 디스턴스 필드 폰트는 비트맵 폰트보다 리소스를 더 많이 사용하지만, 크기 조절의 유연성이 더 큽니다.

![Distance field font](images/font/df_font.png)

*Mode*에서 **SDF**, *Glyph Generation*에서 **Static** 또는 **Dynamic**을 선택합니다. 폰트에는 *`/builtins/fonts/font-df.material`*, Label 컴포넌트에는 *`/builtins/fonts/label-df.material`*을 사용하거나 디스턴스 필드 데이터를 처리하는 커스텀 메터리얼을 사용합니다.

## 비트맵 BMFonts {#bitmap-bmfonts}

생성된 비트맵 외에도 Defold는 미리 bake된 비트맵 "BMFont" 포멧의 폰트를 지원합니다. 이 폰트는 모든 글리프가 들어 있는 PNG 폰트 시트로 구성됩니다. 또한 *`.fnt`* 파일에는 시트에서 각 글리프가 어디에 있는지에 대한 정보와 크기 및 커닝 정보가 들어 있습니다. Defold는 Phaser와 일부 다른 도구에서 사용하는 *`.fnt`* 포멧의 XML 버전을 지원하지 않는다는 점에 유의하세요.

이런 타입의 폰트는 TrueType 또는 OpenType 폰트 파일에서 생성된 비트맵 폰트에 비해 성능 향상을 제공하지는 않지만, 임의의 그래픽, 색상, 그림자를 이미지에 직접 포함할 수 있습니다.

생성된 *`.fnt`*와 *`.png`* 파일을 Defold 프로젝트에 추가합니다. 두 파일은 같은 폴더에 있어야 합니다. 새 폰트 파일을 만들고 *Font* 프로퍼티를 *`.fnt`* 파일로 설정합니다. Defold는 제공된 비트맵을 사용하고 `.fnt` 파일에서 크기를 읽습니다. BMFont 소스에는 *Mode*와 *Glyph Generation*이 표시되지 않습니다.

::: sidenote
BMFont를 만들려면 적절한 파일을 생성할 수 있는 도구를 사용해야 합니다. 여러 선택지가 있습니다.

* [Bitmap Font Generator](http://www.angelcode.com/products/bmfont/), AngelCode에서 제공하는 Windows 전용 도구입니다.
* [Shoebox](http://renderhjs.net/shoebox/), Windows와 macOS용 무료 Adobe Air 기반 앱입니다.
* [Hiero](https://libgdx.com/wiki/tools/hiero), 오픈 소스 Java 기반 도구입니다.
* [Glyph Designer](https://71squared.com/glyphdesigner), 71 Squared의 상용 macOS 도구입니다.
* [bmGlyph](https://www.bmglyph.com), Sovapps의 상용 macOS 도구입니다.
:::

![BMfont](images/font/bm_font.png)

폰트의 *Material*을 *`/builtins/fonts/font-fnt.material`*로 설정합니다. Label 컴포넌트에는 *`/builtins/fonts/label-fnt.material`*을 사용합니다.

## 아티팩트와 모범 사례

일반적으로 비트맵 폰트는 폰트가 스케일링 없이 렌더링될 때 가장 적합합니다. 비트맵 폰트는 디스턴스 필드 폰트보다 화면에 더 빠르게 렌더링됩니다.

디스턴스 필드 폰트는 확대에 매우 잘 대응합니다. 반면 비트맵 폰트는 단순한 픽셀 이미지이므로 폰트가 스케일링될수록 픽셀도 커져 각진 아티팩트가 생깁니다. 다음은 폰트 크기 48픽셀의 샘플을 4배로 확대해 스케일링한 예입니다.

![Fonts scaled up](images/font/scale_up.png)

축소할 때는 비트맵 텍스쳐를 GPU가 깔끔하고 효율적으로 축소하고 안티알리아싱할 수 있습니다. 비트맵 폰트는 디스턴스 필드 폰트보다 색상을 더 잘 유지합니다. 다음은 같은 샘플 폰트를 48픽셀 크기에서 1/5 크기로 축소한 확대 이미지입니다.

![Fonts scaled down](images/font/scale_down.png)

디스턴스 필드 폰트는 폰트 글리프의 곡선을 표현할 수 있는 거리 정보를 담을 만큼 충분히 큰 타겟 크기로 렌더링되어야 합니다. 다음은 위와 같은 폰트이지만 18픽셀 크기에서 10배로 확대해 스케일링한 것입니다. 이 서체의 모양을 인코딩하기에는 너무 작다는 점이 분명합니다.

![Distance field artifacts](images/font/df_artifacts.png)

그림자나 외곽선이 필요하지 않으면 각각의 알파 값을 0으로 설정하세요. 그렇지 않으면 그림자와 외곽선 데이터가 계속 생성되어 불필요한 메모리를 사용합니다. Vector 모드에서 두 효과를 모두 비활성화하면 효과의 비트맵 데이터 생성을 피할 수 있으며 글리프 면은 계속 곡선 데이터를 사용합니다.

## 폰트 캐쉬

Bitmap과 SDF 폰트 리소스는 런타임에 글리프 캐쉬 텍스쳐와 폰트 데이터를 사용합니다. Vector 폰트는 글리프 면을 곡선 데이터로 저장하고, 활성화된 외곽선과 그림자 효과에 비트맵 캐쉬를 사용합니다. 아래의 텍스쳐 레이아웃 설명은 Bitmap과 SDF 폰트에 적용됩니다.

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

런타임 생성은 폰트 리소스마다 설정합니다:

1. `.font` 리소스를 열고 TrueType(`.ttf`) 또는 OpenType(`.otf`) 소스를 선택합니다.
2. *Mode*를 **SDF** 또는 **Vector**, *Glyph Generation*을 **Dynamic**으로 설정합니다.
3. 해당하는 [폰트 및 Label 메터리얼](#font-materials)을 선택합니다.
4. [App Manifest](/manuals/app-manifest)를 추가하여 *game.project*의 *Native Extensions ▸ App Manifest*에 지정하고 **Use full text layout system**을 활성화합니다. 런타임 폰트 생성과 전체 텍스트 레이아웃을 지원하는 커스텀 엔진이 빌드됩니다.
5. 폰트 로드 직후에 표시할 텍스트를 *Prewarm Text*에 지정합니다. 나중에 필요한 텍스트는 [`font.prewarm_text()`](/ref/font/#font.prewarm_text)를 사용하고 콜백을 기다린 후 표시하세요.

새 폰트 리소스는 이미 Vector 모드와 Dynamic 생성을 사용하지만 위의 App Manifest 설정은 여전히 필요합니다.

### 폰트 스크립팅

#### 글리프 캐쉬 프리워밍

Dynamic 폰트는 폰트를 로드할 때 *Prewarm Text*에 필요한 글리프를 생성합니다. 이 필드는 레이아웃할 텍스트로 해석하므로 해당 텍스트에 필요한 글리프가 캐쉬에 준비됩니다. Dynamic 폰트에서는 *All Chars*를 사용할 수 없습니다.

Dynamic 폰트에는 `font.prewarm_text(font_collection, text, callback)`을 호출할 수도 있습니다. 누락된 모든 글리프가 캐쉬에 추가되어 안전하게 텍스트를 표시할 수 있으면 콜백이 알려줍니다. 이 함수는 Static 폰트에 사용할 수 없습니다.

### 폰트 컬렉션에 폰트 추가/제거

Dynamic 폰트에서는 폰트 컬렉션에 원본 폰트(`.ttf` 또는 `.otf`)를 추가하거나 제거할 수 있습니다.
이는 큰 폰트를 여러 문자 세트(예: CJK)에 맞춰 여러 파일로 분할한 경우 유용합니다.

::: important
폰트 컬렉션에 폰트를 추가해도 모든 글리프가 자동으로 로드되거나 렌더링되지는 않습니다.
:::

```lua
function init(self)
    -- 대상 폰트 컬렉션을 가져옵니다.
    self.font_collection = go.get("#label", "font")

    -- 선택한 언어 컬렉션에 지정된 첫 번째 폰트를 가져옵니다.
    local language_collection = go.get("localization_japanese#label", "font")
    local font_info = font.get_info(language_collection)
    self.language_ttf_hash = font_info.fonts[1].path_hash

    -- 대상 컬렉션에 연결하고 참조 횟수를 늘립니다.
    font.add_font(self.font_collection, self.language_ttf_hash)
end
```

```lua
function final(self)
    -- 연결을 제거하고 폰트 참조를 해제합니다.
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
      go.set(self.label, "text", info.text)
    else
      print("Error prewarming text:", err)
    end
  end)
```
