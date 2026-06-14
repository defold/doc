---
title: ZeroBrane Studio로 디버깅하기
brief: 이 매뉴얼은 ZeroBrane Studio를 사용해 Defold에서 Lua 코드를 디버깅하는 방법을 설명합니다.
---

# ZeroBrane Studio로 Lua 스크립트 디버깅하기

Defold에는 내장 디버거가 포함되어 있지만, 무료 오픈 소스 Lua IDE인 _ZeroBrane Studio_를 외부 디버거로 실행할 수도 있습니다. 디버깅 기능을 사용하려면 ZeroBrane Studio가 설치되어 있어야 합니다. 이 프로그램은 크로스 플랫폼이며 macOS와 Windows에서 모두 실행됩니다.

"ZeroBrane Studio"는 http://studio.zerobrane.com 에서 다운로드하세요.

## ZeroBrane 설정

ZeroBrane이 프로젝트의 파일을 찾을 수 있도록 Defold 프로젝트 디렉토리의 위치를 지정해야 합니다. 이를 확인하는 편리한 방법은 Defold 프로젝트 루트의 파일에서 <kbd>Show in Desktop</kbd> 옵션을 사용하는 것입니다.

1. *game.project*를 오른쪽 클릭합니다.
2. <kbd>Show in Desktop</kbd>을 선택합니다.

![Finder에서 보기](images/zerobrane/show_in_desktop.png)

## ZeroBrane 설정하기

ZeroBrane을 설정하려면 <kbd>Project ▸ Project Directory ▸ Choose...</kbd>를 선택합니다:

![설정](images/zerobrane/setup.png)

현재 Defold 프로젝트 디렉토리와 일치하도록 설정하면 ZeroBrane에서 Defold 프로젝트의 디렉토리 트리를 보고, 파일을 탐색하고 열 수 있습니다.

필수는 아니지만 권장되는 다른 설정 변경 사항은 이 문서 아래에서 확인할 수 있습니다.

## 디버깅 서버 시작하기

디버깅 세션을 시작하기 전에 ZeroBrane 내장 디버깅 서버를 시작해야 합니다. 이를 시작하는 메뉴 옵션은 <kbd>Project</kbd> 메뉴 아래에 있습니다. <kbd>Project ▸ Start Debugger Server</kbd>를 선택하면 됩니다:

![디버거 시작](images/zerobrane/startdebug.png)

## 어플리케이션을 디버거에 연결하기

디버깅은 Defold 어플리케이션의 라이프사이클 중 어느 시점에서든 시작할 수 있지만, Lua 스크립트에서 명시적으로 시작해야 합니다. 디버깅 세션을 시작하는 Lua 코드는 다음과 같습니다:

::: sidenote
`dbg.start()`가 호출될 때 게임이 종료된다면, ZeroBrane이 문제를 감지하고 게임에 종료 명령을 보내기 때문일 수 있습니다. 어떤 이유로든 ZeroBrane은 디버깅 세션을 시작하려면 열린 파일이 필요합니다. 그렇지 않으면 다음을 출력합니다:
"Can't start debugging without an opened file or with the current file not being saved 'untitled.lua')."
ZeroBrane에서 이 오류를 수정하려면 `dbg.start()`를 추가한 파일을 여세요.
:::

```lua
dbg = require "builtins.scripts.mobdebug"
dbg.start()
```

위 코드를 어플리케이션에 삽입하면 ZeroBrane의 디버깅 서버에 연결되고(기본적으로 "localhost"를 통해) 다음에 실행될 문장에서 일시 중지됩니다.

```txt
Debugger server started at localhost:8172.
Mapped remote request for '/' to '/Users/my_user/Documents/Projects/Defold_project/'.
Debugging session started in '/Users/my_user/Documents/Projects/Defold_project'.
```

이제 ZeroBrane에서 사용할 수 있는 디버깅 기능을 사용할 수 있습니다. 단계 실행, 검사, 브레이크포인트 추가 및 제거 등을 할 수 있습니다.

::: sidenote
디버깅은 디버깅이 시작된 Lua 컨텍스트에서만 활성화됩니다. *game.project*에서 "shared_state"를 활성화하면 어디에서 시작했는지와 관계없이 전체 어플리케이션을 디버깅할 수 있습니다.
:::

![단계 실행](images/zerobrane/code.png)

연결 시도가 실패하면(디버깅 서버가 실행 중이지 않은 경우일 수 있음) 연결 시도가 끝난 뒤 어플리케이션은 평소처럼 계속 실행됩니다.

## 원격 디버깅

디버깅은 일반 네트워크 연결(TCP)을 통해 이루어지므로 원격으로 디버깅할 수 있습니다. 즉, 모바일 기기에서 실행 중인 어플리케이션을 디버깅할 수 있습니다.

필요한 변경 사항은 디버깅을 시작하는 명령뿐입니다. 기본적으로 `start()`는 localhost에 연결하려고 시도하지만, 원격 디버깅에서는 다음과 같이 ZeroBrane의 디버깅 서버 주소를 수동으로 지정해야 합니다:

```lua
dbg = require "builtins.scripts.mobdebug"
dbg.start("192.168.5.101")
```

이는 원격 기기에서 네트워크 연결이 가능한지, 방화벽이나 비슷한 소프트웨어가 8172 포트의 TCP 연결을 허용하는지도 반드시 확인해야 한다는 뜻입니다. 그렇지 않으면 어플리케이션이 디버깅 서버에 연결하려고 시도하는 동안 실행 시 멈출 수 있습니다.

## 기타 권장 ZeroBrane 설정

디버깅 중에 ZeroBrane이 Lua 스크립트 파일을 자동으로 열도록 만들 수 있습니다. 이렇게 하면 수동으로 파일을 열지 않아도 다른 소스 파일의 함수 안으로 단계 실행할 수 있습니다.

첫 번째 단계는 에디터 설정 파일에 액세스하는 것입니다. 이 파일의 사용자 버전을 변경하는 것이 좋습니다.

- <kbd>Edit ▸ Preferences ▸ Settings: User</kbd>를 선택합니다.
- 설정 파일에 다음을 추가합니다:

  ```txt
  - 디버깅 중 요청된 파일을 자동으로 열기
  editor.autoactivate = true
  ```

- ZeroBrane을 다시 시작합니다.

![기타 권장 설정](images/zerobrane/otherrecommended.png)
