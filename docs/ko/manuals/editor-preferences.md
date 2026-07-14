---
title: 에디터 환경설정
brief: Preferences 창에서 에디터 설정을 수정할 수 있습니다.
---

# 에디터 환경설정

Preferences 창에서 에디터 설정을 수정할 수 있습니다. Preferences 창은 <kbd>File -> Preferences</kbd> 메뉴에서 열 수 있습니다.

## General

![](images/editor/preferences_general.png)

Load External Changes on App Focus
: 에디터가 포커스를 받을 때 외부 변경사항 스캔을 활성화합니다.

Open Bundle Target Folder
: 번들링 프로세스가 완료된 후 타겟 번들 폴더 열기를 활성화합니다.

Enable Texture Compression
: 에디터에서 만든 모든 빌드에 대해 [텍스쳐 압축](/manuals/texture-profiles)을 활성화합니다.

Escape Quits Game
: <kbd>Esc</kbd> 키를 사용해 실행 중인 게임 빌드를 종료합니다.

Track Active Tab in Asset Browser
: *Editor* pane에서 선택된 탭으로 편집 중인 파일이 Asset Browser(*Asset* pane이라고도 함)에서 선택됩니다.

Lint Code on Build
: 프로젝트가 빌드될 때 [코드 린팅](/manuals/writing-code/#linting-configuration)을 활성화합니다. 이 옵션은 기본으로 활성화되어 있지만, 대규모 프로젝트에서 린팅에 시간이 너무 오래 걸리면 비활성화할 수 있습니다.

Engine Arguments
: 에디터가 빌드하고 실행할 때 dmengine 실행 파일에 전달할 인자입니다.
 한 줄에 하나의 인자를 사용하세요. 예:
 ```
--config=bootstrap.main_collection=/my dir/1.collectionc
--verbose
--graphics-adapter=vulkan
```


## Code

![](images/editor/preferences_code.png)

Custom Editor
: 외부 에디터의 절대 경로입니다. macOS에서는 .app 내부 실행 파일의 경로여야 합니다(예: `/Applications/Atom.app/Contents/MacOS/Atom`).

Open File
: 커스텀 에디터가 열 파일을 지정하는 데 사용하는 패턴입니다. `{file}` 패턴은 열 파일명으로 대체됩니다.

Open File at Line
: 커스텀 에디터가 열 파일과 줄 번호를 지정하는 데 사용하는 패턴입니다. `{file}` 패턴은 열 파일명으로 대체되고, `{line}`은 줄 번호로 대체됩니다.

Code editor font
: 코드 에디터에서 사용할 시스템 설치 폰트의 이름입니다.

Zoom on Scroll
: Cmd/Ctrl 버튼을 누른 상태로 코드 에디터에서 스크롤할 때 폰트 크기를 변경할지 여부입니다.

Auto-insert closing parens
: 코드를 편집할 때 짝이 되는 닫는 문자를 자동으로 삽입합니다. 이 옵션은 기본적으로 활성화되어 있습니다.


### Visual Studio Code에서 스크립트 파일 열기

![](images/editor/preferences_vscode.png)

Defold Editor에서 Visual Studio Code로 스크립트 파일을 직접 열려면 실행 파일 경로를 지정하여 다음 설정을 구성해야 합니다:

- MacOS: `/Applications/Visual Studio Code.app/Contents/MacOS/Electron`
- Linux: `/usr/bin/code`
- Windows: `C:\Program Files\Microsoft VS Code\Code.exe`

 특정 파일과 줄을 열려면 다음 파라미터를 설정합니다:

- Open File: `. {file}`
- Open File at Line: `. -g {file}:{line}`

여기서 `.` 문자는 개별 파일이 아니라 전체 워크스페이스를 열기 위해 필요합니다.


## Extensions

![](images/editor/preferences_extensions.png)

Build Server
: [네이티브 익스텐션](/manuals/extensions)이 포함된 프로젝트를 빌드할 때 사용하는 빌드 서버의 URL입니다. 빌드 서버에 인증된 액세스를 하려면 URL에 사용자 이름과 액세스 토큰을 추가할 수 있습니다. 사용자 이름과 액세스 토큰을 지정하려면 다음 표기법을 사용합니다: `username:token@build.defold.com`. Nintendo Switch 빌드 및 인증이 활성화된 자체 빌드 서버 인스턴스를 실행하는 경우 인증된 액세스가 필요합니다(자세한 내용은 [빌드 서버 문서](https://github.com/defold/extender/blob/dev/README_SECURITY.md)를 참고하세요). 사용자 이름과 비밀번호는 시스템 환경 변수 `DM_EXTENDER_USERNAME` 및 `DM_EXTENDER_PASSWORD`로 설정할 수도 있습니다.

Build Server Username
: 인증에 사용할 사용자 이름입니다.

Build Server Password
: 인증에 사용할 비밀번호이며, preferences 파일에 암호화되어 저장됩니다.

Build Server Headers
: 네이티브 익스텐션을 빌드할 때 빌드 서버에 전달할 추가 헤더입니다. extender와 함께 CloudFlare 서비스 또는 유사한 서비스를 사용할 때 중요합니다.

## Tools

![](images/editor/preferences_tools.png)

ADB path
: 이 시스템에 설치된 [ADB](https://developer.android.com/tools/adb) 커맨드 라인 도구의 경로입니다. 시스템에 ADB가 설치되어 있으면 Defold 에디터는 연결된 Android 기기에 번들된 Android APK를 설치하고 실행하는 데 이를 사용합니다. 기본적으로 에디터는 잘 알려진 위치에 ADB가 설치되어 있는지 확인하므로, 커스텀 위치에 ADB를 설치한 경우에만 경로를 지정하면 됩니다.

ios-deploy path
: 이 시스템에 설치된 [ios-deploy](https://github.com/ios-control/ios-deploy) 커맨드 라인 도구의 경로입니다(macOS에만 관련). ADB path와 마찬가지로, Defold 에디터는 연결된 iPhone에 번들된 iOS 어플리케이션을 설치하고 실행하는 데 이 도구를 사용합니다. 기본적으로 에디터는 잘 알려진 위치에 ios-deploy가 설치되어 있는지 확인하므로, ios-deploy의 커스텀 설치를 사용하는 경우에만 경로를 지정하면 됩니다.

## Keymap

![](images/editor/preferences_keymap.png)

Keymap 탭에서 에디터의 키보드 단축키와 마우스 컨트롤을 구성할 수 있습니다. 명령을 변경하려면 더블 클릭하거나, <kbd>Enter</kbd> 또는 <kbd>Space</kbd>를 누르거나, 행 컨텍스트 메뉴를 사용합니다.

키보드 단축키는 *Shortcuts* 열에 키 조합으로 표시됩니다. 마우스 컨트롤은 같은 목록에 배지와 함께 표시됩니다:

- <kbd>MB</kbd>는 마우스 버튼 바인딩을 의미하며, 선택적으로 <kbd>Shift</kbd>, <kbd>Ctrl</kbd>/<kbd>Control</kbd>, 또는 <kbd>Alt</kbd>와 조합될 수 있습니다.
- <kbd>MM</kbd>은 마우스 액션에서 사용하는 수정자 키를 의미합니다.

일부 마우스 컨트롤은 기본 Scene 2D Camera의 바인딩을 재사용하므로, 사용자가 커스터마이즈하기 전에도 행에 바인딩이 표시될 수 있습니다. 이러한 바인딩은 보통 더 어두운 색으로 표시됩니다. 해당 행에 커스텀 바인딩을 설정하면 Defold는 대신 사용자의 바인딩을 사용합니다. 변경 사항을 제거하고 내장 또는 상속된 동작으로 돌아가려면 *Reset to Defaults*를 사용합니다.

경고는 주황색으로 표시됩니다. 자세한 내용을 보려면 경고 위에 마우스를 올립니다. 일반적으로 경고는 다음을 의미합니다:
- 단축키가 텍스트를 입력할 수 있어 텍스트 필드와 충돌할 수 있습니다.
- 같은 단축키 또는 마우스 바인딩이 이미 다른 명령에서 사용되고 있습니다.
