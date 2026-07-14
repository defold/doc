---
title: 어플리케이션 메니페스트
brief: 이 매뉴얼은 어플리케이션 메니페스트를 사용해 엔진에서 기능을 제외하는 방법을 설명합니다.
---

# 어플리케이션 메니페스트

어플리케이션 메니페스트는 엔진에 링크할 기능과 백엔드를 제어합니다. 사용하지 않는 기능을 제외하면 게임의 최종 바이너리 크기가 줄어들기 때문에 권장됩니다. 또한 지원되는 최소 HTML5 브라우저 버전과 WebAssembly 메모리 설정 같은 빌드 타임 옵션도 포함합니다.

![](images/app_manifest/create-app-manifest.png)

![](images/app_manifest/app-manifest.png)

# 메니페스트 적용

`game.project`에서 메니페스트를 `Native Extensions` -> `App Manifest`에 지정합니다.

## Physics 2D

포함할 Box2D 구현을 선택합니다.

* **Box2D Version 3** - Box2D 3을 포함합니다. 이 버전은 선택적으로 활성화하며 레거시 구현과 다른 시뮬레이션 결과를 만들 수 있으므로 기존 프로젝트의 물리 설정을 다시 조정해야 할 수 있습니다.
* **Box2D (Legacy Defold version)** - 레거시 Defold Box2D 구현을 포함합니다. 기본값입니다.
* **None** - 2D 물리를 제외합니다.

Box2D solver 설정은 버전마다 다릅니다. 자세한 내용은 [Box2D 프로젝트 설정](/manuals/project-settings/#box2d)을 참고하세요.

## Physics 3D

Bullet 3D 물리 구현을 포함합니다. 기본적으로 포함되며, 3D 물리를 제외하려면 이 설정을 비활성화하세요.

## Rig + Model

리그와 모델 기능을 제어하거나 None을 선택해 모델과 리그를 완전히 제외합니다. ([`Model`](https://defold.com/manuals/model/#model-component) 문서를 참고하세요).


## Exclude Record

엔진에서 비디오 녹화 기능을 제외합니다([`start_record`](https://defold.com/ref/stable/sys/#start_record) 메세지 문서를 참고하세요).


## Profiler

프로파일러 기능을 엔진에 링크할 시점을 제어합니다.

* **Debug Only** - 디버그 빌드에만 프로파일러를 포함합니다. 기본값입니다.
* **None** - 모든 빌드 variant에서 프로파일러 기능을 제외합니다.
* **Always** - 디버그 빌드와 릴리스 빌드 모두에 프로파일러를 포함합니다.

app manifest 설정은 프로파일러 코드를 빌드에 링크할지 제어합니다. *game.project*의 `profiler` 설정은 런타임 프로파일러 동작을 제어합니다. 사용할 수 있는 기능은 [프로파일링 매뉴얼](/manuals/profiling/)을 참고하세요.


## Sound

사운드 설정은 엔진에 링크할 사운드 시스템과 decoder를 제어합니다.

### Exclude Sound

엔진에서 모든 사운드 재생 기능을 제외합니다.

### Exclude Sound Decoder: WAV

WAV 사운드 리소스 지원을 제외합니다.

### Exclude Sound Decoder: OGG

Ogg Vorbis 사운드 리소스 지원을 제외합니다.

### Include Sound Decoder: Opus

Ogg Opus 사운드 리소스 지원을 포함합니다. Opus decoder는 기본적으로 제외되므로 `.opus` 리소스를 재생하려면 이 옵션을 활성화해야 합니다. 지원되는 형식은 [사운드 매뉴얼](/manuals/sound/)을 참고하세요.


## Exclude Input

엔진에서 모든 입력 처리를 제외합니다.


## Exclude Live Update

엔진에서 [Live Update 기능](/manuals/live-update)을 제외합니다.


## Exclude Image

엔진에서 `image` 스크립트 모듈 [link](https://defold.com/ref/stable/image/)를 제외합니다.


## Exclude Types

엔진에서 `types` 스크립트 모듈 [link](https://defold.com/ref/stable/types/)를 제외합니다.


## Exclude Basis Transcoder

엔진에서 Basis Universal [텍스쳐 압축 라이브러리](/manuals/texture-profiles)를 제외합니다.


## Use Android Support Lib

Android X 대신 더 이상 사용되지 않는 Android Support Library를 사용합니다. [자세한 정보](https://defold.com/manuals/android/#using-androidx).


## Graphics

각 플랫폼에 포함할 그래픽 백엔드를 선택합니다. 결합 선택은 두 백엔드를 모두 포함하므로 선호하는 백엔드를 사용할 수 없을 때 폴백할 수 있습니다.

| 필드 | 플랫폼 | 선택 | 기본값 |
|---|---|---|---|
| **Graphics** | Windows 및 Linux | OpenGL, Vulkan, OpenGL & Vulkan | OpenGL |
| **Graphics (macOS)** | macOS | OpenGL, Metal, Vulkan, OpenGL & Metal, OpenGL & Vulkan | Vulkan |
| **Graphics (iOS)** | iOS | OpenGL, Metal, Vulkan, OpenGL & Metal, OpenGL & Vulkan | OpenGL |
| **Graphics (Android)** | Android | OpenGL+Vulkan, OpenGL, Vulkan | OpenGL+Vulkan |
| **Graphics (HTML5)** | HTML5 | WebGL, WebGPU, WebGL & WebGPU | WebGL |

Linux ARM64에서 **OpenGL** 선택은 OpenGL ES 백엔드를 사용합니다. Android의 결합 기본값은 사용할 수 있으면 Vulkan을 우선하고, 그렇지 않으면 OpenGL ES로 폴백합니다.

## Use full text layout system

활성화하면(`true`) 프로젝트에서 True Type Fonts(`.ttf`)를 사용할 때 SDF 타입 폰트의 런타임 생성을 사용할 수 있습니다. [Font Manual](https://defold.com/manuals/font/#enabling-runtime-fonts)에서 자세한 내용을 확인하세요.


## 최소 브라우저 버전

YAML 필드 **`minSafariVersion`**, **`minFirefoxVersion`**, **`minChromeVersion`**은 Emscripten이 대상으로 하는 최소 브라우저 버전을 지정합니다. 현재 기본값과 지원되는 최소 버전은 non-threaded 타겟과 threaded 타겟에서 서로 다릅니다.

| 타겟 | Safari | Firefox | Chrome |
|---|---:|---:|---:|
| `wasm-web` | `101000` | `40` | `45` |
| `wasm_pthread-web` | `150000` | `79` | `75` |

관련 타겟의 context에서 override를 지정하세요. threaded 타겟에는 추가 [호스팅 요구 사항](/manuals/html5/#creating-html5-bundle)도 있습니다. Emscripten 설정 레퍼런스의 [`MIN_SAFARI_VERSION`](https://emscripten.org/docs/tools_reference/settings_reference.html#min-safari-version), [`MIN_FIREFOX_VERSION`](https://emscripten.org/docs/tools_reference/settings_reference.html#min-firefox-version), [`MIN_CHROME_VERSION`](https://emscripten.org/docs/tools_reference/settings_reference.html#min-chrome-version)을 참고하세요.

## Initial memory (HTML5)
YAML 필드 이름: **`initialMemory`**
기본값: **33554432**

웹 어플리케이션에 처음 할당되는 메모리의 바이트 수입니다. 값은 WebAssembly 페이지 크기(64 KiB)의 배수여야 합니다. Emscripten의 [`INITIAL_MEMORY`](https://emscripten.org/docs/tools_reference/settings_reference.html#initial-memory) 설정을 참고하세요.

이 옵션은 컴파일 타임 기본값을 제공합니다. *game.project*의 [`html5.heap_size`](/manuals/html5/#heap-size) 값이 런타임에 이 값을 덮어씁니다.

## Stack size (HTML5)
YAML 필드 이름: **`stackSize`**
기본값: **5242880**

어플리케이션 스택의 바이트 크기입니다. Emscripten의 [`STACK_SIZE`](https://emscripten.org/docs/tools_reference/settings_reference.html#stack-size) 설정을 참고하세요.
