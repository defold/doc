---
title: 에디터 스타일링
brief: 커스텀 스타일시트를 사용해 에디터의 색상, 타이포그래피 및 기타 시각적 요소를 수정할 수 있습니다.
---

# 에디터 스타일링

커스텀 스타일시트를 사용해 에디터의 색상, 타이포그래피 및 기타 시각적 요소를 수정할 수 있습니다:

* 사용자 홈 디렉토리에 `.defold`라는 폴더를 만듭니다.
  * Windows `C:\Users\**Your Username**\.defold`
  * macOS `/Users/**Your Username**/.defold`
  * Linux `~/.defold`
* `.defold` 폴더에 `editor.css` 파일을 만듭니다.

에디터는 시작 시 커스텀 스타일시트를 로드하고 기본 스타일 위에 적용합니다. 에디터는 유저 인터페이스에 JavaFX를 사용하며, 스타일시트는 브라우저에서 웹페이지 요소에 스타일 속성을 적용하는 데 사용하는 CSS 파일과 거의 같습니다. 에디터의 기본 스타일시트는 [GitHub에서 확인할 수 있습니다](https://github.com/defold/defold/tree/editor-dev/editor/styling/stylesheets/base).

## 색상 변경

기본 색상은 [`_palette.scss`](https://github.com/defold/defold/blob/editor-dev/editor/styling/stylesheets/base/_palette.scss)에 정의되어 있으며 다음과 같습니다:

```
* {
	// 배경
	-df-background-darker:    derive(#212428, -10%);
	-df-background-dark:      derive(#212428, -5%);
	-df-background:           #212428;
	-df-background-light:     derive(#212428, 10%);
	-df-background-lighter:   derive(#212428, 20%);

	// 컴포넌트
	-df-component-darker:     derive(#464c55, -20%);
	-df-component-dark:       derive(#464c55, -10%);
	-df-component:            #464c55;
	-df-component-light:      derive(#464c55, 10%);
	-df-component-lighter:    derive(#464c55, 20%);

	// 텍스트 및 아이콘
	-df-text-dark:            derive(#b4bac1, -10%);
	-df-text:                 #b4bac1;
	-df-text-selected:        derive(#b4bac1, 20%);

  이하 생략...
```

기본 테마는 세 가지 색상 그룹(더 어둡고 더 밝은 변형 포함)으로 나뉩니다:

* 배경색 - 패널, 창, 다이얼로그의 배경색
* 컴포넌트 색상 - 버튼, 스크롤 바 핸들, 텍스트 필드 외곽선
* 텍스트 색상 - 텍스트와 아이콘

예를 들어 사용자 홈의 `.defold` 폴더에 있는 커스텀 `editor.css` 스타일시트에 다음을 추가하면:

```
* {
	-df-background-darker:    derive(#0a0a42, -10%);
	-df-background-dark:      derive(#0a0a42, -5%);
	-df-background:           #0a0a42;
	-df-background-light:     derive(#0a0a42, 10%);
	-df-background-lighter:   derive(#0a0a42, 20%);
}
```

에디터가 다음과 같은 모습으로 표시됩니다:

![](images/editor/editor-styling-color.png)


## 폰트 변경

에디터는 두 가지 폰트를 사용합니다. 코드와 고정폭 텍스트(에러)에는 `Dejavu Sans Mono`, 나머지 UI에는 `Source Sans Pro`를 사용합니다. 폰트 정의는 주로 [`_typography.scss`](https://github.com/defold/defold/blob/editor-dev/editor/styling/stylesheets/base/_typography.scss)에 있으며 다음과 같습니다:

```
@font-face {
  src: url("SourceSansPro-Light.ttf");
}

@font-face {
  src: url("DejaVuSansMono.ttf");
}

$default-font-mono: 'Dejavu Sans Mono';
$default-font: 'Source Sans Pro';
$default-font-bold: 'Source Sans Pro Semibold';
$default-font-italic: 'Source Sans Pro Italic';
$default-font-light: 'Source Sans Pro Light';

.root {
    -fx-font-size: 13px;
    -fx-font-family: $default-font;
}

Text.strong {
  -fx-font-family: $default-font-bold;
}

이하 생략...
```

메인 폰트는 루트 요소에 정의되어 있어 대부분의 위치에서 폰트를 비교적 쉽게 교체할 수 있습니다. `editor.css`에 다음을 추가합니다:

```
@import url('https://fonts.googleapis.com/css2?family=Architects+Daughter&display=swap');

.root {
    -fx-font-family: "Architects Daughter";
}
```

에디터가 다음과 같은 모습으로 표시됩니다:

![](images/editor/editor-styling-fonts.png)

웹 폰트 대신 로컬 폰트를 사용할 수도 있습니다:

```
@font-face {
  font-family: 'Comic Sans MS';
  src: local("cs.ttf");
}

.root {
  -fx-font-family: 'Comic Sans MS';
}
```

::: sidenote
코드 에디터 폰트는 에디터 Preferences에서 별도로 정의됩니다!
:::
