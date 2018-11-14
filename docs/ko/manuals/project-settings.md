# Project settings
이 매뉴얼은 Defold 프로젝트를 셋팅하는 방법에 대해 설명합니다.

"game.project" 파일은 프로젝트의 광범위한 설정을 포함하고 있으며 반드시 "game.project" 라는 이름으로 프로젝트의 루트에 위치해야 합니다. 게임이 실행되어 시작할 때 엔진이 수행하는 첫 번째가 바로 이 파일을 찾는 것 입니다.

이 파일의 모든 설정은 카테고리별로 나누어져 있습니다. 파일 포멧은 간단한 텍스트 형식이며 일반적인 텍스트 에디터로 수정할 수 있습니다. 형식은 아래와 같습니다.

```
[category1]
setting1 = value
setting2 = value
[category2]
...
```

실제 예제는 아래와 같습니다.

```
[bootstrap]
main_collection = /main/main.collectionc
```

**main_collection** 설정은 **bootstrap** 카테고리에 속해 있다는 것을 의미합니다. 위의 예제처럼 경로에 'c' 문자를 추가하면 이는 해당 파일의 컴파일 버전을 참조하고 있다는 뜻입니다. 또한 프로젝트의 루트경로가 실제 루트경로로 취급되므로 경로 설정에 '/'를 사용하였습니다.

아래엔 사용가능한 모든 설정값들이 섹션별로 정렬되어 있습니다. 몇몇 셋팅은 에디터상에서 노출되지 않고 있지만("hidden setting"으로 표시됨) "game.project"에서 마우스 오른쪽 버튼을 누르고 **Open With ▸ Text Editor** 메뉴를 선택해서 직접 셋팅을 할 수 있습니다.

## 엔진 시작시에 config 값들 설정하기
엔진이 시작될 때, 커맨드 라인에서 "game.project" 설정을 재정의하는 config 값을 제공할 수 있습니다.

```
# 부트스트랩(bootstrap) 컬렉션 지정하기
$ dmengine --config=bootstrap.main_collection=/my.collectionc

# "test.my_value"에 커스텀 밸류 설정하기
$ dmengine --config=test.my_value=4711
```

커스텀 밸류(custom values)는 (다른 config value와 마찬가지로) [sys.get_config()](http://www.defold.com/ref/sys/#sys.get_config) 로 읽을 수 있습니다.

## Project
#### title
어플리케이션의 타이틀
#### version
어플리케이션의 버전
#### write_log
체크하면 엔진은 프로젝트의 루트에 "log.txt" 로그 파일을 씁니다. iOS에서 실행시에는 로그파일은 iTunes의 **Apps** 탭과 **File Sharing** 섹션에서 액세스 할 수 있습니다. Android에서는 앱의 외부 스토리지(external storage)에 저장되어, 예를 들어 "dmengine" 라는 이름의 개발 앱을 실행중일 때는 아래와 같은 경로에서 로그를 볼 수 있습니다.

```
$ adb shell cat /mnt/sdcard/Android/data/com.defold.dmengine/files/log.txt
```

#### compress_archive
번들을 만들 때 데이터 압축을 활성화 합니다. 모든 플랫폼에 적용되며 압축된 모든 데이터를 이미 포함하고 있는 apk를 사용하는 Android는 제외됩니다.
#### dependencies
이 프로젝트가 사용하는 프로젝트의 **Library URL:s** ([Defold dashboard](https://www.defold.com/dashboard/)에서 찾을 수 있음) 을 쉼표로 구분하여 나열합니다. 종속 프로젝트의 멤버여야 합니다.
#### custom_resources (hidden setting)
프로젝트에 포함될 쉼표로 구분된 리소스 목록입니다. 디렉토리가 지정되면 이 디렉토리의 모든 파일과 디렉토리들이 재귀적으로(recursively) 포함됩니다.
#### bundle_resources (hidden setting)
번들을 만들 때 결과 패키지에 그대로 복사해야하는 리소스 파일과 폴더를 포함하고 있는 디렉토리입니다. 이 디렉토리는 예를 들어 "/res" 같이 프로젝트 루트의 절대 경로(absolute path)로 지정됩니다. 이 리소스 디렉토리에는 platform 이나 architecure-platform 이라는 이름의 하위 폴더를 포함해야 합니다. 지원되는 플랫폼은 ios, android, osx 입니다. 지원되는 arc-platform 계열으로는 armv7-ios, arm64-ios, armv7-android, x86_64-osx 가 있습니다. 또한 common 이라는 이름의 하위 폴더에 모든 플랫폼의 공통적인 리소스 파일을 포함 시킬 수도 있습니다.

## Display
#### width
어플리케이션 윈도우의 넓이 픽셀, 기본값 960
#### height
어플리케이션 윈도우의 높이 픽셀, 기본값 640
#### high_dpi
지원되는 디스플레이에 high dpi back buffer를 생성해서 더 높은 해상도로 게임을 렌더링 하게 함
#### samples
안티알리아싱(anti-aliasing) 샘플링을 위한 샘플 수, 기본값 0 (안티알리아싱을 끔)
#### fullscreen
체크하면 어플리케이션이 풀스크린으로 시작됨. 체크하지 않으면 창 모드로 실행됨
#### update_frequency
프레임 업데이트 주기, 기본값 60. 유효값은 60, 30, 20, 15, 12, 10, 6, 5, 4, 3, 2, 1
#### variable_dt
시간 간격을 실제 시간에 대비하여 측정할지 또는 고정(**update_frequency** 설정에 따라)할지 체크함
#### display_profiles
사용할 디스플레이 프로파일 파일을 지정함, 기본값 /builtins/render/default.display_profilesc
#### dynamic_orientation
체크하면 장치의 회전에 따라 portrait와 landscape가 동적으로 전환됨. 개발중인 앱은 이 설정에 따르지 않음.

## Physics
#### type
어떤 물리 타입인지, 2D (기본값) 또는 3D
#### gravity_y
y-축의 월드 중력, 기본값은 -10 (자연 중력)
#### debug
체크하면 디버깅을 위해 물리 활동을 시각화 해줌
#### debug_alpha
물리 시각화를 위한 0~1 사이의 알파값, 기본값 0.9
#### world_count
동시에 존재할 수 있는 물리 월드의 최대 개수, 기본값 4개 (메모리 낭비 주의)
#### gravity_x
x-축의 월드 중력, 기본값은 0
#### gravity_z
z-축의 월드 중력, 기본값은 0
#### scale
게임 월드와 관련된 물리 월드를 0.01~1 값의 수치 정밀도로 얼마나 스케일 할지 설정, 기본값 0.02
#### debug_scale
triad나 normal과 같은 물리에서의 단위 오브젝트를 얼마나 크게 그릴지 설정, 기본값 30
#### max_collisions
얼마나 많은 충돌(collisions)을 스크립트들에게 보고할지 설정, 기본값 64
#### max_contacts
얼마나 많은 접촉 지점(contact points)을 스크립트들에게 보고할지 설정, 기본값 128
#### contact_impulse_limit
이 설정보다 작은 값은 접촉 충격(contact impulses)을 무시함, 기본값 0

## Bootstrap
#### main_collection
어플리케이션을 시작할 때 사용할 컬렉션의 파일 참조, 기본값 /logic/main.collectionc
#### render
렌더링 파이프라인을 정의한 렌더 파일 참조, 기본값 /builtins/render/default.renderc

## Graphics
#### default_texture_min_filter
최소화 필터링(min filtering)에 사용할 필터링 종류, linear(기본값) 또는 nearest
#### default_texture_mag_filter
최대화 필터링(mag filtering)에 사용할 필터링 종류, linear(기본값) 또는 nearest
#### max_debug_vertices
디버그용 버텍스(vertices)의 최대 개수. 물리 모형(physics shape)을 렌더링 하는데 사용됨, 기본값 10000
#### texture_profiles
이 프로젝트에서 사용할 텍스쳐 프로파일 파일, 기본값 /builtins/graphics/default.texture_profiles

## Sound
#### gain
전역 게인(gain:볼륨), 0~1, 기본값 1
#### max_sound_data
최대 사운드의 수, 기본값 128
#### max_sound_buffers
동시에 사용할 수 있는 최대 사운드 버퍼 수, 기본값 32
#### max_sound_sources
동시에 재생할 수 있는 최대 사운드의 수, 기본값 16
#### max_sound_instances
동시에 사용할 수 있는 최대 사운드 인스턴스 수, 기본값 256

## Resource
#### http_cache
체크하면 HTTP 캐쉬를 활성화 해서 네트워크 데이터를 더 빠르게 로드함
#### uri
URI 포멧으로된 프로젝트 빌드 데이터를 찾을 위치
#### max_resources
동시에 로드할 수 있는 리소스의 최대 개수, 기본값 1024

## Input
#### repeat_delay
버튼을 누르고 있을 때 반복(repeat)이 시작되기 전까지의 대기 시간(초), 기본값 0.5
#### repeat_interval
버튼을 누르고 있을 때 각 반복 사이의 대기 시간(초), 기본값 0.2
#### gamepads
OS의 게임패드 신호와 매핑하는 게임패드 구성 파일의 참조, 기본값 /builtins/input/default.gamepadsc
#### game_binding
액션을 하드웨어 입력과 매핑하는 입력 구성 파일의 참조, 기본값 /input/game.input_bindingc

## Sprite
#### max_count
스프라이트의 최대 수, 기본값 128
#### subpixels
체크하면 스프라이트가 픽셀에 따라 정렬되지 않은 상태(unaligned)로 표시됨, 기본값 체크됨

## Collection proxy
#### max_count
컬렉션 프록시의 최대 수, 기본값 8

## Collection factory
#### max_count
컬렉션 팩토리의 최대 수, 기본값 128

## Factory
#### max_count
게임 오브젝트 팩토리의 최대 수, 기본값 128

## iOS
#### app_icon_WxH
가로 세로 크기 W x H 별로 사용할 어플리케이션 아이콘 이미지 파일
#### launch_image_WxH
해상도 가로 세로 크기 W x H 별로 사용할 어플리케이션 실행(launch) 이미지 파일. iOS는 실행(launch) 이미지에 따라 디스플레이 해상도를 선택함.
#### pre_rendered_icons
(iOS 6 and earlier) Check if your icons are pre-rendered. If this is unchecked the icons will get a glossy highlight added automatically.
#### bundle_identifier
번들 식별자는 iOS가 앱의 업데이트를 인식하도록 해줌. 번들 ID는 반드시 고유(unique)해야하며 Apple에 등록되어야 함. iOS와 OS X 앱에서 동일한 식별자를 사용할 수 없음.
#### infoplist
지정하면 앱을 번들로 만들 때 이 info.plist 파일을 사용함

## Android
#### app_icon_WxH
가로 세로 크기 W x H 별로 사용할 어플리케이션 아이콘 이미지 파일
#### version_code
앱 버전을 나타내는 정수형 숫자. 업데이트 마다 값을 증가 시켜야 함
#### push_icon_NNN
안드로이드에서 커스텀 푸쉬 알림에 사용할 이미지 파일. 이 아이콘은 자동으로 로컬이나 원격 푸쉬알림에서 사용됨. 설정하지 않으면 기본값으로 어플리케이션 아이콘을 사용함
#### push_field_title
알림 타이틀로 사용할 페이로드 JSON 필드를 지정함. 아무 값도 지정하지 않으면 타이틀로 어플리케이션의 이름을 사용함
#### push_field_text
알림 내용에 사용할 페이로드 JSON 필드를 지정함. 아무 값도 지정하지 않으면 iOS와 마찬가지로 alert 필드의 텍스트를 사용함
#### package
패키지 식별자
#### gcm_sender_id
Google Cloud Messaging의 Sender Id. 푸쉬 알림을 사용하도록 Google에서 정해준 문자열로 설정함
#### manifest
설정하면 번들을 만들 때, 지정된 Android manifest XML 파일을 사용함
#### iap_provider
사용할 스토어를 지정함. Amazon과 GooglePlay 사용 가능, 기본값 GooglePlay
#### input_method
Android 장치에서 키보드 입력을 받는데 사용되는 방법을 지정함. 유효한 옵션은 KeyEvent (옛날꺼) 그리고 HiddenInputField (새거) 가 있음. 기본값은 KeyEvent

## OS X
#### app_icon
OS X에서 어플리케이션 아이콘으로 사용할 이미지 파일
#### infoplist
지정하면 앱을 번들로 만들 때 이 info.plist 파일을 사용함
#### bundle_identifier
번들 식별자는 OS X가 앱의 업데이트를 인식하도록 해줌. 번들 ID는 반드시 고유(unique)해야하며 Apple에 등록되어야 함. iOS와 OS X 앱에서 동일한 식별자를 사용할 수 없음.

## Windows
#### app_icon
Windows에서 어플리케이션 아이콘으로 사용할 이미지 파일

## HTML5
#### set_custom_heap_size
설정하면 Emscripten이 어플리케이션 힙(heap)을 **custom_heap_size** 만큼의 바이트 수 만큼 할당함
#### custom_heap_size
**set_custom_heap_size**이 체크되어 있을 경우 Emscripten이 사용할 커스텀 힙 사이즈를 설정함. 설정하지 않으면 어플리케이션 힙으로 256MB를 할당함.
#### include_dev_tool
어플리케이션에 메모리 사용량을 추적할 수 있는 비주얼 개발 도구를 포함시킴
#### htmlfile
번들을 만들때 특정 HTML 템플릿 파일을 사용함
#### cssfile
번들을 만들때 특정 CSS 파일을 사용함
#### splash_image
번들을 만들고 시작할 때 특정 스플래쉬 이미지를 사용함
#### archive_location_prefix
게임 컨텐츠는 실행시 엔진에 의해 요구되는 압축 데이터 파일로 분할됨. 이 설정을 사용해서 데이터의 위치를 지정할 수 있음, 기본값은 archive
#### archive_location_suffix
압축 파일에 추가할 접미사. CDN에서 non-cache를 강제할 경우 유용함 (예를 들어 ?version2 를 붙이는 것 처럼)

## Particle FX
#### max_emitter_count
동시에 존재할 수 있는 emitters 최대 수, 기본값 64
#### max_particle_count
동시에 존재할 수 있는 파티클 최대 수, 기본값 1024

## Facebook
#### appid (hidden setting)
Facebook에서 발행한 application id

## IAP
#### auto_finish_transactions
체크하면 자동으로 iap 트랜잭션을 완료함. 체크하지 않으면 트랜잭션 성공 후에 iap.finish()를 명시적으로 호출해야 함, 기본값 체크됨

## Network
#### http_timeout
HTTP 타임아웃(초). 기본값은 0이며 타임아웃을 비활성화 함

## Library
#### include_dirs
공백값(space)으로 구분되는 디렉토리 목록. 라이브러리 공유를 통해 프로젝트를 공유할 수 있음.

## Script
#### shared_state
체크하면 모든 스크립트 유형간에 단일 LUA state를 공유함, 기본값 체크됨

## Tracking
#### app_id
프로젝트의 고유한 tracking ID. 프로젝트 tracking ID는 프로젝트 대쉬보드에서 찾을 수 있음

