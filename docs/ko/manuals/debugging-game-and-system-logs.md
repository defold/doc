---
title: 디버깅 - 게임 및 시스템 로그
brief: 이 매뉴얼은 게임 및 시스템 로그를 읽는 방법을 설명합니다.
---

# 게임 및 시스템 로그

게임 로그는 엔진, 네이티브 익스텐션, 게임 로직의 모든 출력을 보여줍니다. 스크립트와 Lua 모듈에서 [print()](/ref/stable/base/#print:...) 및 [pprint()](/ref/stable/builtins/?q=pprint#pprint:v) 명령을 사용해 게임 로그에 정보를 표시할 수 있습니다. 네이티브 익스텐션에서는 [`dmLog` 네임스페이스](/ref/stable/dmLog/)의 함수를 사용해 게임 로그에 쓸 수 있습니다. 게임 로그는 에디터, 터미널 창, 플랫폼별 도구 또는 로그 파일에서 읽을 수 있습니다.

시스템 로그는 운영체제에서 생성되며, 문제를 정확히 찾아내는 데 도움이 되는 추가 정보를 제공할 수 있습니다. 시스템 로그에는 크래시의 스택 트레이스와 메모리 부족 경고가 포함될 수 있습니다.

::: important
콘솔/화면 로깅은 Debug 빌드에서만 정보를 표시합니다. Release 빌드에서는 콘솔 로그가 비어 있지만, 프로젝트 설정 "Write Log File"을 "Always"로 설정하면 Release에서도 파일 로깅을 활성화할 수 있습니다. 자세한 내용은 아래를 참고하세요.
:::

## 에디터에서 게임 로그 읽기

에디터에서 로컬로 게임을 실행하거나 [모바일 개발용 앱](/manuals/dev-app)에 연결하면 모든 출력이 에디터의 콘솔 창에 표시됩니다.

![Editor 2](images/editor/editor2_overview.png)

## 터미널에서 게임 로그 읽기

터미널에서 Defold 게임을 실행하면 로그가 터미널 창 자체에 표시됩니다. Windows와 Linux에서는 터미널에 실행 파일 이름을 입력해 게임을 시작합니다. macOS에서는 .app 파일 안에서 엔진을 실행해야 합니다.

```
$ > ./mygame.app/Contents/MacOS/mygame
```

## 플랫폼별 도구로 게임 및 시스템 로그 읽기

### HTML5

대부분의 브라우저에서 제공하는 개발자 도구를 사용해 로그를 읽을 수 있습니다.

* [Chrome](https://developers.google.com/web/tools/chrome-devtools/console) - Menu > More Tools > Developer Tools
* [Firefox](https://developer.mozilla.org/en-US/docs/Tools/Browser_Console) - Tools > Web Developer > Web Console
* [Edge](https://docs.microsoft.com/en-us/microsoft-edge/devtools-guide/console)
* [Safari](https://support.apple.com/guide/safari-developer/log-messages-with-the-console-dev4e7dedc90/mac) - Develop > Show JavaScript Console

### Android

Android Debug Bridge (ADB) 도구를 사용해 게임 및 시스템 로그를 볼 수 있습니다.

:[Android ADB](../shared/android-adb.md)

설치하고 설정한 후, USB로 기기를 연결하고 터미널을 열어 다음을 실행하세요.

```txt
$ cd <path_to_android_sdk>/platform-tools/
$ adb logcat
```

그러면 기기가 게임의 print 출력을 포함한 모든 출력을 현재 터미널에 덤프합니다.

Defold 어플리케이션 출력만 보고 싶다면 이 명령을 사용하세요.

```txt
$ cd <path_to_android_sdk>/platform-tools/
$ adb logcat -s defold
--------- beginning of /dev/log/system
--------- beginning of /dev/log/main
I/defold  ( 6210): INFO:ENGINE: Defold Engine 1.2.50 (8d1b912)
I/defold  ( 6210): INFO:ENGINE: Loading data from:
I/defold  ( 6210): INFO:ENGINE: Initialized sound device 'default'
I/defold  ( 6210):
D/defold  ( 6210): DEBUG:SCRIPT: Hello there, log!
...
```

### iOS

iOS에서 게임 및 시스템 로그를 읽는 방법은 여러 가지가 있습니다.

1. [Console tool](https://support.apple.com/guide/console/welcome/mac)을 사용해 게임 및 시스템 로그를 읽을 수 있습니다.
2. LLDB 디버거를 사용해 기기에서 실행 중인 게임에 연결할 수 있습니다. 게임을 디버그하려면 디버그하려는 기기가 포함된 "Apple Developer Provisioning Profile"로 게임이 서명되어 있어야 합니다. 에디터에서 게임을 번들하고 번들 다이얼로그에서 프로비저닝 프로파일을 지정하세요(iOS 번들링은 macOS에서만 사용할 수 있습니다).

게임을 실행하고 디버거를 연결하려면 [ios-deploy](https://github.com/phonegap/ios-deploy)라는 도구가 필요합니다. 터미널에서 다음을 실행해 게임을 설치하고 디버그하세요.

```txt
$ ios-deploy --debug --bundle <path_to_game.app> # 참고: .ipa 파일이 아님
```

그러면 앱이 기기에 설치되고 시작되며 LLDB 디버거가 자동으로 연결됩니다. LLDB를 처음 사용한다면 [Getting Started with LLDB](https://developer.apple.com/library/content/documentation/IDEs/Conceptual/gdb_to_lldb_transition_guide/document/lldb-basics.html)를 읽어보세요.


## 로그 파일에서 게임 로그 읽기

*game.project*의 프로젝트 설정 "Write Log File"을 사용해 파일 로깅을 제어합니다.

- "Never": 로그 파일을 쓰지 않습니다.
- "Debug": Debug 빌드에서만 로그 파일을 씁니다.
- "Always": Debug 및 Release 빌드 모두에서 로그 파일을 씁니다.

활성화하면 모든 게임 출력이 디스크의 "`log.txt`"라는 파일에 기록됩니다. 기기에서 게임을 실행하는 경우 파일을 추출하는 방법은 다음과 같습니다.

iOS
: macOS와 Xcode가 설치된 컴퓨터에 기기를 연결합니다.

  Xcode를 열고 <kbd>Window ▸ Devices and Simulators</kbd>로 이동합니다.

  목록에서 기기를 선택한 다음 *Installed Apps* 목록에서 관련 앱을 선택합니다.

  목록 아래의 톱니바퀴 아이콘을 클릭하고 <kbd>Download Container...</kbd>를 선택합니다.

  ![컨테이너 다운로드](images/debugging/download_container.png)

  컨테이너가 추출되면 *Finder*에 표시됩니다. 컨테이너를 오른쪽 클릭하고 <kbd>Show Package Content</kbd>를 선택합니다. "`AppData/Documents/`"에 위치해야 하는 "`log.txt`" 파일을 찾습니다.

Android(
: "`log.txt`"를 추출할 수 있는지는 OS 버전과 제조사에 따라 다릅니다. 다음은 짧고 간단한 [단계별 가이드](https://stackoverflow.com/a/48077004/129360)입니다.
