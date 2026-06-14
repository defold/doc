---
title: 코드 작성
brief: 이 매뉴얼은 Defold에서 코드로 작업하는 방법을 간단히 설명합니다.
---

# 코드 작성

Defold에서는 타일 맵 및 파티클 효과 에디터 같은 시각적 도구를 사용해 게임 컨텐츠의 많은 부분을 만들 수 있지만, 게임 로직은 여전히 코드 에디터를 사용해 만듭니다. 게임 로직은 [Lua 프로그래밍 언어](https://www.lua.org/)로 작성하고, 엔진 자체의 익스텐션은 타겟 플랫폼의 네이티브 언어로 작성합니다.

## Lua 코드 작성

Defold는 타겟 플랫폼에 따라 Lua 5.1과 LuaJIT을 사용하므로, 게임 로직을 작성할 때는 해당 Lua 버전의 언어 명세를 따라야 합니다. Defold에서 Lua로 작업하는 방법에 대한 자세한 내용은 [Defold의 Lua 매뉴얼](/manuals/lua)을 참고하세요.

## Lua로 트랜스파일되는 다른 언어 사용하기

Defold는 Lua 코드를 생성하는 트랜스파일러 사용을 지원합니다. 트랜스파일러 익스텐션을 설치하면 [Teal](https://github.com/defold/extension-teal) 같은 대체 언어를 사용해 정적으로 검사되는 Lua를 작성할 수 있습니다. 이 기능은 제한사항이 있는 preview 기능입니다. 현재 트랜스파일러 지원은 Defold Lua 런타임에 정의된 모듈과 함수에 대한 정보를 노출하지 않습니다. 따라서 `go.animate` 같은 Defold API를 사용하려면 외부 정의를 직접 작성해야 합니다.

## 네이티브 코드 작성

Defold에서는 엔진 자체에서 제공하지 않는 플랫폼별 기능에 액세스하기 위해 네이티브 코드로 게임엔진을 확장할 수 있습니다. Lua의 성능이 충분하지 않은 경우(리소스 집약적인 계산, 이미지 처리 등)에도 네이티브 코드를 사용할 수 있습니다. 자세한 내용은 [네이티브 익스텐션 매뉴얼](/manuals/extensions/)을 참고하세요.

## 내장 코드 에디터 사용하기

Defold에는 Lua 파일(.lua), Defold 스크립트 파일(.script, .gui_script 및 .render_script)은 물론 에디터가 기본적으로 처리하지 않는 파일 확장자를 가진 다른 파일도 열고 편집할 수 있는 내장 코드 에디터가 있습니다. 또한 에디터는 Lua 및 스크립트 파일에 구문 강조를 제공합니다.

![](/images/editor/code-editor.png)


### 코드 자동 완성

내장 코드 에디터는 코드를 작성하는 동안 함수의 코드 자동 완성을 표시합니다.

![](/images/editor/codecompletion.png)

<kbd>CTRL</kbd> + <kbd>Space</kbd>를 누르면 함수, 인자, 반환값에 대한 추가 정보가 표시됩니다.

![](/images/editor/apireference.png)

### 린팅 설정 {#linting-configuration}

내장 코드 에디터는 [Luacheck](https://luacheck.readthedocs.io/en/stable/index.html)과 [Lua language server](https://luals.github.io/wiki/diagnostics/)를 사용해 코드 린팅을 수행합니다. Luacheck을 설정하려면 프로젝트 루트에 `.luacheckrc` 파일을 만듭니다. 사용 가능한 옵션 목록은 [Luacheck 설정 페이지](https://luacheck.readthedocs.io/en/stable/config.html)에서 확인할 수 있습니다. Defold는 Luacheck 설정에 다음 기본값을 사용합니다.

```lua
unused_args = false      -- 사용하지 않는 인자에 대해 경고하지 않음(.script 파일에서 흔함)
max_line_length = false  -- 긴 줄에 대해 경고하지 않음
ignore = {
    "611",               -- 줄에 공백만 포함됨
    "612",               -- 줄 끝에 공백이 포함됨
    "614"                -- 주석에 줄 끝 공백이 포함됨
},
```

## 외부 코드 에디터 사용하기

Defold의 코드 에디터는 코드 작성에 필요한 기본 기능을 제공하지만, 더 고급 사용 사례나 선호하는 코드 에디터가 있는 숙련된 사용자를 위해 Defold가 외부 에디터로 파일을 열도록 설정할 수 있습니다. [Preferences 창의 Code 탭](/manuals/editor-preferences/#code)에서 코드를 편집할 때 사용할 외부 에디터를 정의할 수 있습니다.

### Visual Studio Code - Defold Kit

Defold Kit은 다음 기능을 제공하는 Visual Studio Code 플러그인입니다.

* 권장 익스텐션 설치
* Lua 구문 강조, 자동 완성 및 린팅
* 워크스페이스에 관련 설정 적용
* Defold API용 Lua 어노테이션
* 종속성용 Lua 어노테이션
* 빌드하고 실행하기
* 브레이크포인트를 사용한 디버깅
* 모든 플랫폼용 번들링
* 연결된 모바일 장치에 배포

[Visual Studio Marketplace](https://marketplace.visualstudio.com/items?itemName=astronachos.defold)에서 Defold Kit에 대해 더 알아보고 설치하세요.


## 문서 소프트웨어

커뮤니티에서 만든 API 레퍼런스 패키지는 [Dash and Zeal](https://forum.defold.com/t/defold-docset-for-dash/2417)에서 사용할 수 있습니다.
