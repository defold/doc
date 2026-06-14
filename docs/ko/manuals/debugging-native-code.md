---
title: Defold에서 네이티브 코드 디버깅하기
brief: 이 매뉴얼은 Defold에서 네이티브 코드를 디버깅하는 방법을 설명합니다.
---

# 네이티브 코드 디버깅

Defold는 충분히 테스트되어 있으며 일반적인 상황에서는 크래시가 매우 드물게 발생합니다. 하지만 특히 게임에서 네이티브 익스텐션을 사용하는 경우, 절대 크래시가 발생하지 않는다고 보장할 수는 없습니다. 크래시나 예상대로 동작하지 않는 네이티브 코드 문제가 발생하면 여러 가지 방법으로 진행할 수 있습니다.

* 디버거를 사용해 코드를 단계별로 실행합니다.
* print 디버깅을 사용합니다.
* 크래시 로그를 분석합니다.
* 콜스택을 심볼리케이트합니다.


## 디버거 사용하기

가장 일반적인 방법은 `debugger`를 통해 코드를 실행하는 것입니다. 디버거를 사용하면 코드를 단계별로 실행하고, `breakpoints`를 설정하고, 크래시가 발생했을 때 실행을 중지할 수 있습니다.

각 플랫폼에는 여러 디버거가 있습니다.

* Visual studio - Windows
* VSCode - Windows, macOS, Linux
* Android Studio - Windows, macOS, Linux
* Xcode - macOS
* WinDBG - Windows
* lldb / gdb - macOS, Linux, (Windows)
* ios-deploy - macOS

각 도구는 특정 플랫폼을 디버깅할 수 있습니다.

* Visual studio - Windows + gdbserver를 지원하는 플랫폼(예: Linux/Android)
* VSCode - Windows, macOS (lldb), Linux (lldb/gdb) + gdbserver를 지원하는 플랫폼
* Xcode -  macOS, iOS ([자세히 알아보기](/manuals/debugging-native-code-ios))
* Android Studio - Android ([자세히 알아보기](/manuals/debugging-native-code-android))
* WinDBG - Windows
* lldb/gdb - macOS, Linux, (iOS)
* ios-deploy - iOS (lldb를 통해)


## print 디버깅 사용하기

네이티브 코드를 디버깅하는 가장 간단한 방법은 [print 디버깅](http://en.wikipedia.org/wiki/Debugging#Techniques)을 사용하는 것입니다. 변수를 확인하거나 실행 흐름을 나타내려면 [`dmLog` 네임스페이스](/ref/stable/dmLog/)의 함수를 사용하세요. 로그 함수 중 하나를 사용하면 에디터의 *Console* 뷰와 [게임 로그](/manuals/debugging-game-and-system-logs)에 출력됩니다.


## 크래시 로그 분석하기

Defold 엔진은 하드 크래시가 발생하면 `_crash` 파일을 저장합니다. 크래시 파일에는 크래시뿐 아니라 시스템에 대한 정보도 들어 있습니다. [게임 로그 출력](/manuals/debugging-game-and-system-logs)은 크래시 파일이 있는 위치를 기록합니다(운영체제, 기기, 어플리케이션에 따라 달라집니다).

이후 세션에서 [crash 모듈](https://www.defold.com/ref/crash/)을 사용해 이 파일을 읽을 수 있습니다. 파일을 읽고, 정보를 수집하고, 콘솔에 출력한 다음, 크래시 로그 수집을 지원하는 [분석 서비스](/tags/stars/analytics/)로 보내는 것을 권장합니다.

::: important
Windows에서는 `_crash.dmp` 파일도 생성됩니다. 이 파일은 크래시를 디버깅할 때 유용합니다.
:::

### 기기에서 크래시 로그 가져오기

모바일 기기에서 크래시가 발생하면 크래시 파일을 자신의 컴퓨터로 다운로드하고 로컬에서 파싱할 수 있습니다.

#### Android

앱이 [debuggable](/manuals/project-settings/#android)인 경우, [Android Debug Bridge (ADB) 도구](https://developer.android.com/studio/command-line/adb.html)와 `adb shell` 명령을 사용해 크래시 로그를 가져올 수 있습니다.

```
$ adb shell "run-as com.defold.example sh -c 'cat /data/data/com.defold.example/files/_crash'" > ./_crash
```

#### iOS

iTunes에서 앱 컨테이너를 보거나 다운로드할 수 있습니다.

`Xcode -> Devices` 창에서도 크래시 로그를 선택할 수 있습니다.


## 콜스택 심볼리케이트하기

`_crash` 파일 또는 [로그 파일](/manuals/debugging-game-and-system-logs)에서 콜스택을 얻었다면 이를 심볼리케이트할 수 있습니다. 이는 콜스택의 각 주소를 파일명과 줄 번호로 변환하는 것을 의미하며, 근본 원인을 찾는 데 도움이 됩니다.

올바른 엔진을 콜스택과 매칭하는 것이 중요합니다. 그렇지 않으면 잘못된 대상을 디버깅하게 될 가능성이 매우 높습니다! [bob](https://www.defold.com/manuals/bob/)으로 번들링할 때 [`--with-symbols`](https://www.defold.com/manuals/bob/) 플래그를 사용하거나, 에디터의 번들 다이얼로그에서 "Generate debug symbols" 체크박스를 선택하세요.

* iOS - `build/arm64-ios`의 `dmengine.dSYM.zip` 폴더에는 iOS 빌드용 디버그 심볼이 들어 있습니다.
* macOS - `build/x86_64-macos`의 `dmengine.dSYM.zip` 폴더에는 macOS 빌드용 디버그 심볼이 들어 있습니다.
* Android - `projecttitle.apk.symbols/lib/` 번들 출력 폴더에는 타겟 아키텍처용 디버그 심볼이 들어 있습니다.
* Linux - 실행 파일에는 디버그 심볼이 들어 있습니다.
* Windows - `build/x86_64-win32`의 `dmengine.pdb` 파일에는 Windows 빌드용 디버그 심볼이 들어 있습니다.
* HTML5 - `build/wasm-web`의 `dmengine.js.symbols` 파일에는 HTML5 빌드용 디버그 심볼이 들어 있습니다.

::: important
게임의 각 공개 릴리스마다 디버그 심볼을 어딘가에 저장하고, 해당 디버그 심볼이 어떤 릴리스에 속하는지 알고 있는 것이 매우 중요합니다. 디버그 심볼이 없으면 네이티브 크래시를 디버깅할 수 없습니다! 또한 엔진의 `unstripped` 버전도 보관해야 합니다. 이렇게 하면 콜스택을 가장 잘 심볼리케이트할 수 있습니다.
:::


### Google Play에 심볼 업로드하기
Google Play에 기록된 크래시가 심볼리케이트된 콜스택으로 표시되도록 [디버그 심볼을 Google Play에 업로드](https://developer.android.com/studio/build/shrink-code#android_gradle_plugin_version_40_or_earlier_and_other_build_systems)할 수 있습니다. `projecttitle.apk.symbols/lib/` 번들 출력 폴더의 내용을 zip으로 압축하세요. 이 폴더에는 `arm64-v8a`, `armeabi-v7a` 같은 아키텍처 이름을 가진 하위 폴더가 하나 이상 포함됩니다.


### Android 콜스택 심볼리케이트하기

1. 빌드 폴더에서 엔진을 가져옵니다.

```sh
	$ ls <project>/build/<platform>/[lib]dmengine[.exe|.so]
```

2. 폴더에 압축을 풉니다.

```sh
	$ unzip dmengine.apk -d dmengine_1_2_105
```

3. 콜스택 주소를 찾습니다.

	예를 들어 심볼리케이트되지 않은 콜스택에서는 다음과 같이 보일 수 있습니다.

	`#00 pc 00257224 libmy_game_name.so`

	여기서 *`00257224`*가 주소입니다.

4. 주소를 확인합니다.

```sh
    $ arm-linux-androideabi-addr2line -C -f -e dmengine_1_2_105/lib/armeabi-v7a/libdmengine.so _address_
```

참고: [Android 로그](/manuals/debugging-game-and-system-logs)에서 스택 트레이스를 얻은 경우 [ndk-stack](https://developer.android.com/ndk/guides/ndk-stack.html)을 사용해 심볼리케이트할 수 있습니다.

### iOS 콜스택 심볼리케이트하기

1. 네이티브 익스텐션을 사용하는 경우, 서버가 심볼(.dSYM)을 제공할 수 있습니다(`--with-symbols`를 bob.jar에 전달).

```sh
	$ unzip <project>/build/arm64-darwin/build.zip
	# Contents/Resources/DWARF/dmengine을 생성합니다.
```

2. 네이티브 익스텐션을 사용하지 않는 경우, 기본 심볼을 다운로드합니다.

```sh
	$ wget http://d.defold.com/archive/<sha1>/engine/arm64-darwin/dmengine.dSYM
```

3. 로드 주소를 사용해 심볼리케이트합니다.

	어떤 이유로든 콜스택의 주소를 그대로 넣는 방식은 동작하지 않습니다(즉, 로드 주소 0x0).

```sh
		$ atos -arch arm64 -o Contents/Resources/DWARF/dmengine 0x1492c4
```

	# 로드 주소를 직접 지정해도 동작하지 않습니다.

```sh
		$ atos -arch arm64 -o MyApp.dSYM/Contents/Resources/DWARF/MyApp -l0x100000000 0x1492c4
```

	주소에 로드 주소를 더하면 동작합니다.

```sh
		$ atos -arch arm64 -o MyApp.dSYM/Contents/Resources/DWARF/MyApp 0x1001492c4
		dmCrash::OnCrash(int) (in MyApp) (backtrace_execinfo.cpp:27)
```
