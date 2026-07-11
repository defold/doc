---
title: Defold 프로젝트 설정
brief: 이 매뉴얼은 Defold에서 프로젝트별 설정이 어떻게 작동하는지 설명합니다.
---

# 프로젝트 설정

*game.project* 파일에는 프로젝트 전반의 모든 설정이 들어 있습니다. 이 파일은 프로젝트의 루트 폴더에 있어야 하며, 이름은 반드시 *game.project*여야 합니다. 엔진이 시작되어 게임을 실행할 때 가장 먼저 하는 일은 이 파일을 찾는 것입니다.

파일의 모든 설정은 카테고리에 속합니다. 파일을 열면 Defold는 모든 설정을 카테고리별로 묶어서 표시합니다.

![프로젝트 설정](images/project-settings/settings.jpg)


## 파일 포멧

*game.project*의 설정은 보통 Defold 안에서 변경하지만, 표준 텍스트 에디터로도 파일을 편집할 수 있습니다. 이 파일은 INI 파일 포멧 표준을 따르며 다음과 같은 형태입니다.

```ini
[category1]
setting1 = value
setting2 = value
[category2]
...
```

실제 예제는 다음과 같습니다.

```ini
[bootstrap]
main_collection = /main/main.collectionc
```

이는 *main_collection* 설정이 *bootstrap* 카테고리에 속한다는 뜻입니다. 위 예제처럼 파일 참조를 사용할 때는 경로 끝에 'c' 문자를 붙여야 합니다. 이는 해당 파일의 컴파일된 버전을 참조한다는 의미입니다. 또한 *game.project*가 들어 있는 폴더가 프로젝트 루트가 되므로, 설정 경로 앞에 '/'가 붙어 있습니다.


## 런타임 액세스

[`sys.get_config_string(key)`](/ref/sys/#sys.get_config_string), [`sys.get_config_number(key)`](/ref/sys/#sys.get_config_number), [`sys.get_config_int(key)`](/ref/sys/#sys.get_config_int)를 사용하면 런타임에 *game.project*의 모든 값을 읽을 수 있습니다. 예:

```lua
local title = sys.get_config_string("project.title")
local gravity_y = sys.get_config_number("physics.gravity_y")
```

::: sidenote
키는 카테고리와 설정 이름을 점으로 연결한 조합이며, 소문자로 작성하고 공백 문자는 밑줄로 바꿉니다. 예: "Project" 카테고리의 "Title" 필드는 `project.title`이 되고, "Physics" 카테고리의 "Gravity Y" 필드는 `physics.gravity_y`가 됩니다.
:::


## 섹션과 설정

아래에는 사용 가능한 모든 설정이 카테고리별로 정리되어 있습니다.

### Project

#### Title
어플리케이션의 타이틀입니다.

#### Version
어플리케이션의 버전입니다.

#### Publisher
퍼블리셔 이름입니다.

#### Developer
개발자 이름입니다.

#### Write Log File
엔진이 로그 파일을 기록하는 시점을 제어합니다. 옵션:

- "Never": 로그 파일을 기록하지 않습니다.
- "Debug": Debug 빌드에서만 로그 파일을 기록합니다.
- "Always": Debug 빌드와 Release 빌드 모두에서 로그 파일을 기록합니다.

에디터에서 인스턴스를 둘 이상 실행하면 파일 이름은 *instance_2_log.txt*가 되며, 여기서 `2`는 인스턴스 인덱스입니다. 단일 인스턴스를 실행하거나 번들에서 실행하면 파일 이름은 *log.txt*가 됩니다. 로그 파일 위치는 다음 경로 중 하나입니다(순서대로 시도).

1. *project.log_dir*에 지정된 경로(hidden setting)
2. 시스템 로그 경로:
  * macOS/iOS: `NSDocumentDirectory`
  * Android: `Context.getExternalFilesDir()`
  * Others: 어플리케이션 루트
3. 어플리케이션 지원 경로
  * macOS/iOS: `NSApplicationSupportDirectory`
  * Windows: `CSIDL_APPDATA` (예: `C:\Users\<username>\AppData\Roaming`)
  * Android: `Context.getFilesDir()`
  * Linux: `HOME` 환경 변수

#### Minimum Log Level
로깅 시스템의 최소 로그 레벨을 지정합니다. 이 레벨 이상인 로그만 표시됩니다.

#### Compress Archive
번들링할 때 아카이브 압축을 활성화합니다. 현재 이 설정은 Android를 제외한 모든 플랫폼에 적용됩니다. Android에서는 apk가 이미 모든 데이터를 압축된 상태로 포함합니다.

#### Dependencies
프로젝트 *Library URL*들의 URL 목록입니다. 자세한 내용은 [Libraries 매뉴얼](/manuals/libraries/)을 참고하세요.

#### Custom Resources
`custom_resources`
:[Custom Resources](../shared/custom-resources.md)

커스텀 리소스를 로드하는 방법은 [File Access 매뉴얼](/manuals/file-access/#how-to-access-files-bundled-with-the-application)에서 더 자세히 다룹니다.

#### Bundle Resources
`bundle_resources`
:[Bundle Resources](../shared/bundle-resources.md)

번들 리소스를 로드하는 방법은 [File Access 매뉴얼](/manuals/file-access/#how-to-access-files-bundled-with-the-application)에서 더 자세히 다룹니다.

#### Bundle Exclude Resources
`bundle_exclude_resources`
번들에 포함하지 않아야 하는 리소스를 쉼표로 구분한 목록입니다. 즉, `bundle_resources` 단계의 수집 결과에서 제거됩니다.

---

### Bootstrap

#### Main Collection
어플리케이션을 시작할 때 사용할 컬렉션의 파일 참조입니다. 기본값은 `/logic/main.collection`입니다.

#### Render
렌더링 파이프라인을 정의하는 렌더 설정 파일입니다. 기본값은 `/builtins/render/default.render`입니다.

---

### Library

#### Include Dirs
라이브러리 공유를 통해 프로젝트에서 공유할 디렉토리를 공백으로 구분한 목록입니다. 자세한 내용은 [Libraries 매뉴얼](/manuals/libraries/)을 참고하세요.

---

### Script

#### Shared State
체크하면 모든 스크립트 타입이 하나의 Lua state를 공유합니다.

---

### Engine

#### Run While Iconified
어플리케이션 창이 아이콘화된 동안에도 엔진이 계속 실행되도록 허용합니다(데스크톱 플랫폼만).

#### Fixed Update Frequency
`fixed_update(self, dt)` 라이프사이클 함수의 업데이트 주기입니다. 단위는 Hertz입니다.

#### Max Time Step
단일 프레임 동안 time step이 너무 커지면 이 최대값으로 제한됩니다. 단위는 초입니다.

---

### Display

#### Width
어플리케이션 창의 너비입니다. 단위는 픽셀입니다.

#### Height
어플리케이션 창의 높이입니다. 단위는 픽셀입니다.

#### High Dpi
지원되는 디스플레이에서 high dpi 백 버퍼를 생성합니다. 일반적으로 게임은 *Width* 및 *Height* 설정에 지정된 값보다 두 배 높은 해상도로 렌더링되지만, 스크립트와 프로퍼티에서 사용하는 논리 해상도는 여전히 해당 설정값입니다.

#### Samples
슈퍼 샘플링 안티앨리어싱에 사용할 샘플 수입니다. 이 값은 `GLFW_FSAA_SAMPLES` window hint를 설정합니다. 값이 `0`이면 안티앨리어싱이 꺼집니다.

#### Fullscreen
어플리케이션을 전체 화면으로 시작할지 체크합니다. 체크하지 않으면 어플리케이션은 창 모드로 실행됩니다.

#### Update Frequency
원하는 프레임레이트입니다. 단위는 Hertz입니다. 가변 프레임레이트를 사용하려면 0으로 설정합니다. 0보다 큰 값은 런타임에 실제 프레임레이트를 기준으로 제한되는 고정 프레임레이트를 사용하게 합니다. 즉, 하나의 엔진 프레임 안에서 게임 루프를 두 번 업데이트할 수는 없습니다. 런타임에 이 값을 변경하려면 [`sys.set_update_frequency(hz)`](https://defold.com/ref/stable/sys/?q=set_update_frequency#sys.set_update_frequency:frequency)를 사용하세요. 이 설정은 headless 빌드에서도 작동합니다.

#### Swap interval
이 정수 값은 어플리케이션이 vsync를 처리하는 방식을 제어합니다. 0은 vsync를 비활성화하며, 기본값은 1입니다. OpenGL 어댑터를 사용할 때 이 값은 창이 [buffer swap 사이에 업데이트](https://www.khronos.org/opengl/wiki/Swap_Interval)해야 하는 프레임 수를 설정합니다. Vulkan에는 swap interval이라는 내장 개념이 없으므로, 이 값은 대신 vsync 활성화 여부를 제어합니다.

#### Vsync
프레임 타이밍을 하드웨어 vsync에 의존합니다. 그래픽 드라이버와 플랫폼 세부 사항에 따라 재정의될 수 있습니다. 더 이상 권장되지 않는 'variable_dt' 동작을 사용하려면 이 설정을 체크 해제하고 frame cap을 0으로 설정합니다.

#### Display Profiles
사용할 display profiles 파일을 지정합니다. 기본값은 `/builtins/render/default.display_profilesc`입니다. 자세한 내용은 [GUI Layouts 매뉴얼](/manuals/gui-layouts/#creating-display-profiles)을 참고하세요.

#### Dynamic Orientation
장치 회전에 따라 앱이 portrait와 landscape 사이를 동적으로 전환할지 체크합니다. 개발용 앱은 현재 이 설정을 따르지 않습니다.

#### Display Device Info
시작할 때 GPU 정보를 콘솔에 출력합니다.

---

### Render

#### Clear Color Red
렌더 스크립트와 창 생성 시 사용하는 clear color의 red 채널입니다.

#### Clear Color Green
렌더 스크립트와 창 생성 시 사용하는 clear color의 green 채널입니다.

#### Clear Color Blue
렌더 스크립트와 창 생성 시 사용하는 clear color의 blue 채널입니다.

#### Clear Color Alpha
렌더 스크립트와 창 생성 시 사용하는 clear color의 alpha 채널입니다.

---

### Font

#### Runtime Generation
런타임 폰트 생성을 사용합니다.

---

### Physics

#### Max Collision Object Count
충돌 오브젝트의 최대 수입니다.

#### Type
사용할 물리 타입입니다. `2D` 또는 `3D`입니다.

#### Gravity X
x축 방향의 월드 중력입니다. 단위는 초당 미터입니다.

#### Gravity Y
y축 방향의 월드 중력입니다. 단위는 초당 미터입니다.

#### Gravity Z
z축 방향의 월드 중력입니다. 단위는 초당 미터입니다.

#### Debug
디버깅을 위해 물리를 시각화할지 체크합니다.

#### Debug Alpha
시각화된 물리에 사용할 alpha 컴포넌트 값입니다. `0`--`1`입니다.

#### World Count
동시에 존재할 수 있는 물리 월드의 최대 수입니다. 기본값은 `4`입니다. 컬렉션 프록시를 통해 동시에 4개보다 많은 월드를 로드한다면 이 값을 늘려야 합니다. 각 물리 월드는 꽤 많은 메모리를 할당한다는 점에 유의하세요.

#### Scale
수치 정밀도를 위해 게임 월드와 관련하여 물리 엔진이 물리 월드를 어떻게 스케일할지 알려줍니다. 값은 `0.01`--`1.0`입니다. 값이 `0.02`로 설정되면 물리 엔진은 50 유닛을 1미터로 봅니다($1 / 0.02$).

#### Allow Dynamic Transforms
물리 엔진이 게임 오브젝트의 변형(transform)을 연결된 충돌 오브젝트 컴포넌트에 적용할지 체크합니다. 이를 사용하면 dynamic인 충돌 모형까지도 이동, 스케일, 회전할 수 있습니다.

#### Use Fixed Timestep
물리 엔진이 고정되고 프레임레이트와 독립적인 업데이트를 사용할지 체크합니다. 이 설정을 `fixed_update(self, dt)` 라이프사이클 함수 및 `engine.fixed_update_frequency` 프로젝트 설정과 함께 사용하면 일정한 간격으로 물리 엔진과 상호작용할 수 있습니다. 새 프로젝트의 권장 설정은 `true`입니다.

#### Debug Scale
triad와 normal 같은 물리의 단위 오브젝트를 얼마나 크게 그릴지 지정합니다.

#### Max Collisions
스크립트로 보고할 충돌 수입니다.

#### Max Contacts
스크립트로 보고할 접촉 지점 수입니다.

#### Contact Impulse Limit
이 설정보다 작은 값을 가진 contact impulse를 무시합니다.

#### Ray Cast Limit 2d
프레임당 2d ray cast 요청의 최대 수입니다.

#### Ray Cast Limit 3d
프레임당 3d ray cast 요청의 최대 수입니다.

#### Trigger Overlap Capacity
겹쳐질 수 있는 물리 트리거의 최대 수입니다.

#### Velocity Threshold
탄성 충돌을 발생시키는 최소 속도입니다.

#### Max Fixed Timesteps
fixed timestep을 사용할 때 시뮬레이션의 최대 step 수입니다(3D만).

---

### Graphics

#### Default Texture Min Filter
축소 필터링에 사용할 필터링을 지정합니다.

#### Default Texture Mag Filter
확대 필터링에 사용할 필터링을 지정합니다.

#### Max Draw Calls
렌더 호출의 최대 수입니다.

#### Max Characters:
텍스트 렌더링 버퍼에 미리 할당되는 문자 수입니다. 즉, 각 프레임에 표시할 수 있는 문자 수입니다.

#### Max Font Batches
각 프레임에 표시할 수 있는 텍스트 배치의 최대 수입니다.

#### Max Debug Vertices
디버그 버텍스의 최대 수입니다. 물리 모형 렌더링 등에 사용됩니다.

#### Texture Profiles
이 프로젝트에서 사용할 텍스쳐 프로파일 파일입니다. 기본값은 `/builtins/graphics/default.texture_profiles`입니다.

#### Verify Graphics Calls
각 그래픽 호출 후 반환값을 확인하고 오류가 있으면 로그에 보고합니다.

#### OpenGL Version Hint
OpenGL 컨텍스트 버전 hint입니다. 특정 버전을 선택하면 이 버전이 필요한 최소 버전으로 사용됩니다(OpenGL ES에는 적용되지 않음).

#### OpenGL Core Profile Hint
컨텍스트를 생성할 때 'core' OpenGL profile hint를 설정합니다. core profile은 즉시 모드 렌더링 같은 모든 deprecated 기능을 OpenGL에서 제거합니다. OpenGL ES에는 적용되지 않습니다.

---

### Shader

#### Exclude GLES 2.0
OpenGLES 2.0 / WebGL 1.0을 실행하는 장치용 쉐이더를 컴파일하지 않습니다.

---

### Input

#### Repeat Delay
누르고 있는 입력이 반복을 시작하기 전까지 기다릴 시간입니다. 단위는 초입니다.

#### Repeat Interval
누르고 있는 입력의 각 반복 사이에 기다릴 시간입니다. 단위는 초입니다.

#### Gamepads
게임패드 신호를 OS에 매핑하는 gamepads config 파일의 파일 참조입니다. 기본값은 `/builtins/input/default.gamepads`입니다.

#### Game Binding
하드웨어 입력을 액션에 매핑하는 입력 config 파일의 파일 참조입니다. 기본값은 `/input/game.input_binding`입니다.

#### Use Accelerometer
엔진이 매 프레임 가속도계 입력 이벤트를 받도록 체크합니다. 가속도계 입력을 비활성화하면 일부 성능 이점이 있을 수 있습니다.

---

### Resource

#### Http Cache
체크하면 장치에서 실행 중인 엔진으로 네트워크를 통해 리소스를 더 빠르게 로드하기 위해 HTTP 캐쉬가 활성화됩니다.

#### Uri
프로젝트 빌드 데이터를 찾을 위치입니다. URI 포멧입니다.

#### Max Resources
동시에 로드할 수 있는 리소스의 최대 수입니다.

---

### Network

#### Http Timeout
HTTP 타임아웃입니다. 단위는 초입니다. 타임아웃을 비활성화하려면 `0`으로 설정합니다.

#### Http Thread Count
HTTP 서비스의 worker thread 수입니다.

#### Http Cache Enabled
체크하면 네트워크 요청에 대한 HTTP 캐쉬가 활성화됩니다(`http.request()` 사용). HTTP 캐쉬는 요청과 연결된 응답을 저장하고 이후 요청에서 저장된 응답을 다시 사용합니다. HTTP 캐쉬는 `ETag` 및 `Cache-Control: max-age` HTTP 응답 헤더를 지원합니다.

#### SSL Certificates
SSL handshake 중 인증서 체인을 검증할 때 사용할 SSL 루트 인증서가 들어 있는 파일입니다.

---

### Collection

#### Max Instances
컬렉션 안의 게임 오브젝트 인스턴스 최대 수입니다. 기본값은 `1024`입니다. [(component max count optimizations 정보 보기)](#component-max-count-optimizations).

#### Max Input Stack Entries
인풋 스택에 들어갈 수 있는 게임 오브젝트의 최대 수입니다.

---

### Sound

#### Gain
전역 게인(볼륨)입니다. `0`--`1`입니다.

#### Use Linear Gain
활성화하면 gain이 linear입니다. 비활성화하면 exponential curve를 사용합니다.

#### Max Sound Data
사운드 리소스의 최대 수입니다. 즉, 런타임의 유니크한 사운드 파일 수입니다.

#### Max Sound Buffers
(현재 사용되지 않음) 동시에 존재할 수 있는 사운드 버퍼의 최대 수입니다.

#### Max Sound Sources
(현재 사용되지 않음) 동시에 재생할 수 있는 사운드의 최대 수입니다.

#### Max Sound Instances
동시에 존재할 수 있는 사운드 인스턴스의 최대 수입니다. 즉, 같은 시간에 실제로 재생되는 사운드 수입니다.

#### Max Component Count
컬렉션당 사운드 컴포넌트의 최대 수입니다.

#### Sample Frame Count
각 오디오 업데이트에 사용하는 샘플 수입니다. 0은 자동을 의미합니다(48 kHz에서는 1024, 44.1 kHz에서는 768).

#### Use Thread
체크하면 메인 thread 부하가 높을 때 끊김 위험을 줄이기 위해 사운드 시스템이 thread를 사용하여 사운드를 재생합니다.

#### Stream Enabled
체크하면 사운드 시스템이 소스 파일을 로드할 때 스트리밍을 사용합니다.

#### Stream Cache Size
_모든_ 청크를 포함하는 사운드 청크 캐쉬의 최대 크기입니다. 기본값은 `2097152` bytes입니다.
이 수는 로드된 사운드 파일 수에 stream chunk size를 곱한 값보다 커야 합니다.
그렇지 않으면 매 프레임 새 청크가 제거될 위험이 있습니다.

#### Stream Chunk Size
각 스트리밍 청크의 크기입니다. 단위는 bytes입니다.

#### Stream Preload Size
아카이브에서 읽는 사운드 파일의 초기 청크 크기를 bytes 단위로 결정합니다.

---

### Sprite

#### Max Count
컬렉션당 스프라이트의 최대 수입니다. [(component max count optimizations 정보 보기)](#component-max-count-optimizations).

#### Subpixels
스프라이트가 픽셀에 맞춰 정렬되지 않은 상태로 표시되도록 허용하려면 체크합니다.

---

### Tilemap

#### Max Count
컬렉션당 타일 맵의 최대 수입니다. [(component max count optimizations 정보 보기)](#component-max-count-optimizations).

#### Max Tile Count
컬렉션당 동시에 보일 수 있는 타일의 최대 수입니다.

---

### Spine

#### Max Count
spine 모델 컴포넌트의 최대 수입니다. [(component max count optimizations 정보 보기)](#component-max-count-optimizations).

---

### Mesh

#### Max Count
컬렉션당 mesh 컴포넌트의 최대 수입니다. [(component max count optimizations 정보 보기)](#component-max-count-optimizations).

---

### Model

#### Max Count
컬렉션당 모델 컴포넌트의 최대 수입니다. [(component max count optimizations 정보 보기)](#component-max-count-optimizations).

#### Split Meshes
65536개보다 많은 버텍스를 가진 mesh를 새 mesh로 분할합니다.

#### Max Bone Matrix Texture Width
bone matrix 텍스쳐의 최대 너비입니다. 애니메이션에 필요한 크기만 사용하며, 가장 가까운 power-of-two로 올림합니다.

#### Max Bone Matrix Texture Height
bone matrix 텍스쳐의 최대 높이입니다. 애니메이션에 필요한 크기만 사용하며, 가장 가까운 power-of-two로 올림합니다.

---

### GUI

#### Max Count
GUI 컴포넌트의 최대 수입니다. [(component max count optimizations 정보 보기)](#component-max-count-optimizations).

#### Max Particle Count
GUI에서 동시에 존재할 수 있는 파티클의 최대 수입니다.

#### Max Animation Count
GUI에서 활성화될 수 있는 애니메이션의 최대 수입니다.

---

### Label

#### Max Count
라벨의 최대 수입니다. [(component max count optimizations 정보 보기)](#component-max-count-optimizations).

#### Subpixels
라벨이 픽셀에 맞춰 정렬되지 않은 상태로 표시되도록 허용하려면 체크합니다.

---

### Particle FX

#### Max Count
동시에 존재할 수 있는 emitter의 최대 수입니다. [(component max count optimizations 정보 보기)](#component-max-count-optimizations).

#### Max Particle Count
동시에 존재할 수 있는 파티클의 최대 수입니다.

---

### Box2D

#### Velocity Iterations
Box2D 2.2 물리 solver의 velocity iteration 수입니다.

#### Position Iterations
Box2D 2.2 물리 solver의 position iteration 수입니다.

#### Sub Step Count
Box2D 3.x 물리 solver의 sub-step 수입니다.

---

### Collection proxy

#### Max Count
컬렉션 프록시의 최대 수입니다. [(component max count optimizations 정보 보기)](#component-max-count-optimizations).

---

### Collection factory

#### Max Count
컬렉션 팩토리의 최대 수입니다. [(component max count optimizations 정보 보기)](#component-max-count-optimizations).

---

### Factory

#### Max Count
게임 오브젝트 팩토리의 최대 수입니다. [(component max count optimizations 정보 보기)](#component-max-count-optimizations).

---

### iOS

#### App Icon 57x57--180x180
지정한 너비와 높이 `W` &times; `H` 크기의 어플리케이션 아이콘으로 사용할 이미지 파일(.png)입니다.

#### Launch Screen
Storyboard 파일(.storyboard)입니다. 만드는 방법에 대한 자세한 내용은 [iOS 매뉴얼](/manuals/ios/#creating-a-storyboard)을 참고하세요.

#### Icons Asset
앱 아이콘이 들어 있는 icons asset 파일(.car)입니다.

#### Prerendered Icons
(iOS 6 및 이전 버전) 아이콘이 미리 렌더링되었는지 체크합니다. 체크하지 않으면 아이콘에 광택 하이라이트가 자동으로 추가됩니다.

#### Bundle Identifier
번들 식별자는 iOS가 앱 업데이트를 인식할 수 있게 합니다. 번들 ID는 Apple에 등록되어야 하며 앱마다 고유해야 합니다. iOS 앱과 macOS 앱에 같은 식별자를 사용할 수 없습니다. 점으로 구분된 둘 이상의 segment로 구성되어야 합니다. 각 segment는 문자로 시작해야 합니다. 각 segment는 영숫자 문자, 밑줄 또는 하이픈(-) 문자로만 구성되어야 합니다([`CFBundleIdentifier`](https://developer.apple.com/library/archive/documentation/General/Reference/InfoPlistKeyReference/Articles/CoreFoundationKeys.html#//apple_ref/doc/uid/20001431-130430) 참고).

#### Bundle Name
번들 짧은 이름(15자)입니다([`CFBundleName`](https://developer.apple.com/library/archive/documentation/General/Reference/InfoPlistKeyReference/Articles/CoreFoundationKeys.html#//apple_ref/doc/uid/20001431-130430) 참고).

#### Bundle Version
번들 버전입니다. 숫자 또는 x.y.z입니다([`CFBundleVersion`](https://developer.apple.com/library/archive/documentation/General/Reference/InfoPlistKeyReference/Articles/CoreFoundationKeys.html#//apple_ref/doc/uid/20001431-130430) 참고).

#### Info.plist
지정하면 앱을 번들링할 때 이 *`info.plist`* 파일을 사용합니다.

#### Privacy Manifest
어플리케이션의 Apple Privacy Manifest입니다. 이 필드는 기본적으로 `/builtins/manifests/ios/PrivacyInfo.xcprivacy`를 사용합니다.

#### Custom Entitlements
지정하면 제공된 provisioning profile(`.entitlements`, `.xcent`, `.plist`)의 entitlement가 어플리케이션을 번들링할 때 제공된 provisioning profile의 entitlement와 병합됩니다.

#### Default Language
어플리케이션의 `Localizations` 목록에 사용자가 선호하는 언어가 없을 때 사용할 언어입니다([`CFBundleDevelopmentRegion`](https://developer.apple.com/library/archive/documentation/General/Reference/InfoPlistKeyReference/Articles/CoreFoundationKeys.html#//apple_ref/doc/uid/20001431-130430) 참고). 선호 언어가 있으면 두 글자 ISO 639-1 표준을 사용하고, 그렇지 않으면 세 글자 ISO 639-2를 사용합니다.

#### Localizations
이 필드에는 지원되는 localization의 언어 이름 또는 ISO 언어 지정자를 식별하는 쉼표로 구분된 문자열이 들어 있습니다([`CFBundleLocalizations`](https://developer.apple.com/library/archive/documentation/General/Reference/InfoPlistKeyReference/Articles/CoreFoundationKeys.html#//apple_ref/doc/uid/20001431-109552) 참고).

---

### Android

#### App Icon 36x36--192x192
지정한 너비와 높이 `W` &times; `H` 크기의 어플리케이션 아이콘으로 사용할 이미지 파일(.png)입니다.

#### Push Icon Small--LargeXxxhdpi
Android에서 커스텀 푸쉬 알림 아이콘으로 사용할 이미지 파일(.png)입니다. 이 아이콘은 로컬 또는 원격 푸쉬 알림 모두에 자동으로 사용됩니다. 설정하지 않으면 기본적으로 어플리케이션 아이콘이 사용됩니다.

#### Push Field Title
알림 타이틀로 사용할 payload JSON 필드를 지정합니다. 이 설정을 비워 두면 푸쉬 알림은 기본적으로 어플리케이션 이름을 타이틀로 사용합니다.

#### Push Field Text
알림 텍스트로 사용할 payload JSON 필드를 지정합니다. 비워 두면 iOS와 마찬가지로 `alert` 필드의 텍스트가 사용됩니다.

#### Version Code
앱 버전을 나타내는 정수 값입니다. 이후 업데이트마다 값을 증가시켜야 합니다.

#### Minimum SDK Version
어플리케이션 실행에 필요한 최소 API Level입니다(`android:minSdkVersion`).

#### Target SDK Version
어플리케이션이 타겟으로 하는 API Level입니다(`android:targetSdkVersion`).

#### Package
패키지 식별자입니다. 점으로 구분된 둘 이상의 segment로 구성되어야 합니다. 각 segment는 문자로 시작해야 합니다. 각 segment는 영숫자 문자 또는 밑줄 문자로만 구성되어야 합니다.

#### GCM Sender Id
Google Cloud Messaging Sender Id입니다. 푸쉬 알림을 활성화하려면 Google에서 할당한 문자열로 설정합니다.

#### FCM Application Id
Firebase Cloud Messaging Application Id입니다.

#### Manifest
설정하면 번들링할 때 지정한 Android manifest XML 파일을 사용합니다.

#### Iap Provider
사용할 스토어를 지정합니다. 유효한 옵션은 `Amazon`과 `GooglePlay`입니다. 자세한 내용은 [extension-iap](/extension-iap/)을 참고하세요.

#### Input Method
Android 장치에서 키보드 입력을 받는 데 사용할 방법을 지정합니다. 유효한 옵션은 `KeyEvent`(old method)와 `HiddenInputField`(new)입니다.

#### Immersive Mode
설정하면 navigation bar와 status bar를 숨기고 앱이 화면의 모든 터치 이벤트를 캡처할 수 있게 합니다.

#### Display Cutout
display cutout 영역까지 확장합니다.

#### Debuggable
어플리케이션을 [GAPID](https://github.com/google/gapid) 또는 [Android Studio](https://developer.android.com/studio/profile/android-profiler) 같은 도구로 디버깅할 수 있는지 여부입니다. 이 설정은 Android manifest의 `android:debuggable` flag를 설정합니다([공식 문서](https://developer.android.com/guide/topics/manifest/application-element#debug)).

#### ProGuard config
최종 APK에서 중복 Java 클래스를 제거하는 데 도움이 되는 커스텀 ProGuard 파일입니다.

#### Extract Native Libraries
패키지 installer가 APK에서 네이티브 라이브러리를 파일 시스템으로 추출할지 지정합니다. `false`로 설정하면 네이티브 라이브러리는 APK 안에 압축되지 않은 상태로 저장됩니다. APK가 더 커질 수는 있지만, 런타임에 라이브러리가 APK에서 직접 로드되므로 어플리케이션 로드가 더 빨라집니다. 이 설정은 Android Manifest의 `android:extractNativeLibs` flag를 설정합니다([공식 문서](https://developer.android.com/guide/topics/manifest/application-element#extractNativeLibs)).

---

### macOS

#### App Icon
macOS에서 어플리케이션 아이콘으로 사용할 번들 아이콘 파일(.icns)입니다.

#### Info.plist
설정하면 번들링할 때 지정한 info.plist 파일을 사용합니다.

#### Privacy Manifest
어플리케이션의 Apple Privacy Manifest입니다. 이 필드는 기본적으로 `/builtins/manifests/osx/PrivacyInfo.xcprivacy`를 사용합니다.

#### Bundle Identifier
번들 식별자는 macOS가 앱 업데이트를 인식할 수 있게 합니다. 번들 ID는 Apple에 등록되어야 하며 앱마다 고유해야 합니다. iOS 앱과 macOS 앱에 같은 식별자를 사용할 수 없습니다. 점으로 구분된 둘 이상의 segment로 구성되어야 합니다. 각 segment는 문자로 시작해야 합니다. 각 segment는 영숫자 문자, 밑줄 또는 하이픈(-) 문자로만 구성되어야 합니다.

#### Default Language
어플리케이션의 `Localizations` 목록에 사용자가 선호하는 언어가 없을 때 사용할 언어입니다([`CFBundleDevelopmentRegion`](https://developer.apple.com/library/archive/documentation/General/Reference/InfoPlistKeyReference/Articles/CoreFoundationKeys.html#//apple_ref/doc/uid/20001431-130430) 참고). 선호 언어가 있으면 두 글자 ISO 639-1 표준을 사용하고, 그렇지 않으면 세 글자 ISO 639-2를 사용합니다.

#### Localizations
이 필드에는 지원되는 localization의 언어 이름 또는 ISO 언어 지정자를 식별하는 쉼표로 구분된 문자열이 들어 있습니다([`CFBundleLocalizations`](https://developer.apple.com/library/archive/documentation/General/Reference/InfoPlistKeyReference/Articles/CoreFoundationKeys.html#//apple_ref/doc/uid/20001431-109552) 참고).

---

### Windows

#### App Icon
Windows에서 어플리케이션 아이콘으로 사용할 이미지 파일(.ico)입니다. .ico 파일을 만드는 방법은 [Windows 매뉴얼](/manuals/windows)에서 더 자세히 확인할 수 있습니다.

---

### HTML5

이 옵션들 중 다수에 대한 자세한 내용은 [HTML5 platform 매뉴얼](/manuals/html5/)을 참고하세요.

#### Heap Size
Emscripten이 사용할 heap 크기입니다. 단위는 megabytes입니다.

#### .html Shell
번들링할 때 지정한 템플릿 HTML 파일을 사용합니다. 기본값은 `/builtins/manifests/web/engine_template.html`입니다.

#### Custom .css
번들링할 때 지정한 theme CSS 파일을 사용합니다. 기본값은 `/builtins/manifests/web/light_theme.css`입니다.

#### Splash Image
설정하면 번들링 후 시작할 때 Defold 로고 대신 지정한 splash image를 사용합니다.

#### Archive Location Prefix
HTML5로 번들링할 때 게임 데이터는 하나 이상의 archive data file로 분할됩니다. 엔진이 게임을 시작하면 이 archive file들이 메모리로 읽힙니다. 데이터 위치를 지정하려면 이 설정을 사용합니다.

#### Archive Location Suffix
아카이브 파일에 붙일 suffix입니다. 예를 들어 CDN에서 캐쉬되지 않은 컨텐츠를 강제로 가져오게 할 때 유용합니다(예: `?version2`).

#### Engine Arguments
엔진에 전달할 인자 목록입니다.

#### Wasm Streaming
wasm 파일의 스트리밍을 활성화합니다(더 빠르고 메모리를 덜 사용하지만 `application/wasm` MIME type이 필요합니다).

#### Show Fullscreen Button
`index.html` 파일에서 Fullscreen Button을 활성화합니다.

#### Show Made With Defold
`index.html` 파일에서 Made With Defold 링크를 활성화합니다.

#### Show Console Banner
활성화하면 엔진이 시작될 때 이 옵션이 브라우저 콘솔에 엔진 및 엔진 버전에 대한 정보를 출력합니다(`console.log()` 사용).

#### Scale Mode
게임 canvas를 스케일하는 데 사용할 방법을 지정합니다.

#### Retry Count
엔진이 시작될 때 파일 다운로드를 시도할 횟수입니다(`Retry Time` 참고).

#### Retry Time
다운로드가 실패했을 때 파일 다운로드를 다시 시도하기 전까지 기다릴 시간입니다. 단위는 초입니다(`Retry Count` 참고).

#### Transparent Graphics Context
그래픽 컨텍스트에 투명한 배경을 사용하려면 체크합니다.

---

### IAP

#### Auto Finish Transactions
IAP 트랜잭션을 자동으로 완료하려면 체크합니다. 체크하지 않으면 트랜잭션이 성공한 뒤 `iap.finish()`를 명시적으로 호출해야 합니다.

---

### Live update

#### Settings
번들링 중 사용할 Liveupdate 설정 리소스 파일입니다.

---

### Native extension

#### _App Manifest_
설정하면 app manifest를 사용하여 엔진 빌드를 커스터마이즈합니다. 이를 통해 엔진에서 사용하지 않는 부분을 제거하여 최종 바이너리 크기를 줄일 수 있습니다. 사용하지 않는 기능을 제외하는 방법은 [application manifest 매뉴얼](/manuals/app-manifest)에서 확인하세요.

---

### Profiler

#### Enabled
게임 내 profiler를 활성화합니다.

#### Track Cpu
체크하면 release 버전 빌드에서 CPU profiling을 활성화합니다. 일반적으로 profiling 정보는 debug 빌드에서만 액세스할 수 있습니다.

#### Sleep Between Server Updates
서버 업데이트 사이에 sleep할 시간입니다. 단위는 milliseconds입니다.

#### Performance Timeline Enabled
브라우저 내 performance timeline을 활성화합니다(HTML5만).

---

## 엔진 시작 시 config 값 설정하기

엔진이 시작될 때 *game.project* 설정을 재정의하는 config 값을 커맨드 라인에서 제공할 수 있습니다.

```bash
# 부트스트랩 컬렉션 지정
$ dmengine --config=bootstrap.main_collection=/my.collectionc

# 두 개의 커스텀 config 값 설정
$ dmengine --config=test.my_value=4711 --config=test2.my_value2=foobar
```

커스텀 값은 다른 config 값과 마찬가지로 [`sys.get_config_string()`](/ref/sys/#sys.get_config_string) 또는 [`sys.get_config_number()`](/ref/sys/#sys.get_config_number)로 읽을 수 있습니다.

```lua
local my_value = sys.get_config_number("test.my_value")
local my_value2 = sys.get_config_string("test.my_value2")
```


:[Component max count optimizations](../shared/component-max-count-optimizations.md)


## 커스텀 프로젝트 설정

메인 프로젝트 또는 [네이티브 익스텐션](/manuals/extensions/)에 커스텀 설정을 정의할 수 있습니다. 메인 프로젝트의 커스텀 설정은 프로젝트 루트의 `game.properties` 파일에 정의해야 합니다. 네이티브 익스텐션의 경우 `ext.manifest` 파일 옆의 `ext.properties` 파일에 정의해야 합니다.

설정 파일은 *game.project*와 같은 INI 포멧을 사용하며, 프로퍼티 속성은 suffix가 붙은 점 표기법(dot notation)으로 정의됩니다.

```
[my_category]
my_property.private = 1
...
```

항상 적용되는 기본 meta 파일은 [여기](https://github.com/defold/defold/blob/dev/com.dynamo.cr/com.dynamo.cr.bob/src/com/dynamo/bob/meta.properties)에서 확인할 수 있습니다.

현재 사용할 수 있는 속성은 다음과 같습니다.

```
[my_extension]
// `type` - 값 문자열 파싱에 사용
my_property.type = string // 다음 값 중 하나: bool, string, number, integer, string_array, resource

// `help` - 에디터에서 help tip으로 사용(현재는 사용되지 않음)
my_property.help = string

// `default` - 사용자가 값을 직접 설정하지 않았을 때 기본값으로 사용되는 값
my_property.default = string

// `private` - 번들 과정에서 사용되지만 번들 자체에서는 제거되는 private 값
my_property.private = 1 // boolean 값 1 또는 0

// `label` - 에디터 input label
my_property.label = My Awesome Property

// `minimum` 및/또는 `maximum` - numeric 프로퍼티의 유효 범위, 에디터 UI에서 검증됨
my_property.minimum = 0
my_property.maximum = 255

// `options` - 에디터 UI의 drop-down 선택지, 쉼표로 구분된 value[:label] 쌍
my_property.options = android: Android, ios: iOS

// `resource` 타입만:
my_property.filter = jpg,png // resource selector dialog에서 허용되는 파일 확장자
my_property.preserve-extension = 1 // 빌드된 확장자 대신 원래 리소스 확장자를 사용

// deprecation
my_property.deprecated = 1 // 프로퍼티를 deprecated로 표시
my_property.severity-default = warning // deprecated 프로퍼티가 지정되었지만 기본값으로 설정된 경우
my_property.severity-override = error  // deprecated 프로퍼티가 지정되고 기본값이 아닌 값으로 설정된 경우

```
추가로 설정 카테고리에 다음 속성을 설정할 수 있습니다.
```
[my_extension]
// `group` - game.project 카테고리 그룹. 예: Main, Platforms, Components, Runtime, Distribution
group = Runtime
// `title` - 표시될 카테고리 title
title = My Awesome Extension
// `help` - 표시될 카테고리 help
help = Settings for My Awesome Extension
```


현재 meta 프로퍼티는 어플리케이션 번들링 시 `bob.jar`에서만 사용되지만, 나중에는 에디터가 이를 파싱하여 *game.project* viewer에 표시할 예정입니다.
