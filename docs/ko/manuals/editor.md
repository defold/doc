---
title: 에디터 개요
brief: 이 매뉴얼은 Defold 에디터의 모습과 동작 방식, 그리고 에디터 안에서 탐색하는 방법의 개요를 제공합니다.
---

# 에디터 개요

에디터에서는 게임 프로젝트의 모든 파일과 폴더를 효율적으로 찾아보고 조작할 수 있습니다. 파일을 편집하면 적절한 에디터가 열리고, 파일과 관련된 모든 정보가 별도의 뷰에 표시됩니다.

## 에디터 시작하기

Defold Editor를 실행하면 프로젝트 선택 및 생성 화면이 표시됩니다. 원하는 작업을 클릭해서 선택하세요.

MY PROJECTS
: 최근에 열었던 프로젝트가 표시되어 빠르게 액세스할 수 있습니다. 시작 화면의 기본 뷰입니다.

  이전에 프로젝트를 열지 않았거나 모두 제거했다면 두 개의 버튼이 표시됩니다. `Open From Disk…`를 클릭하면 시스템 파일 브라우저로 프로젝트를 찾아 열 수 있고, `Create New Project` 버튼을 클릭하면 `TEMPLATES` 탭으로 전환됩니다.

  ![내 프로젝트](images/editor/start_no_projects.png)


  이전에 연 프로젝트가 있으면 아래 그림처럼 프로젝트 목록이 표시됩니다.

  ![내 프로젝트](images/editor/start_my_projects.png)

TEMPLATES
: 특정 플랫폼용이거나 특정 익스텐션을 사용하는 새 Defold 프로젝트를 빠르게 시작할 수 있도록 만들어진 비어 있거나 거의 비어 있는 기본 프로젝트가 들어 있습니다.


TUTORIALS
: 튜토리얼을 따라가고 싶을 때 배우고, 실행하고, 수정해 볼 수 있는 안내형 튜토리얼 프로젝트가 들어 있습니다.


SAMPLES
: 특정 사용 사례를 보여 주기 위해 준비된 프로젝트가 들어 있습니다.

  ![새 프로젝트](images/editor/start_templates.png)

새 프로젝트를 만들면 로컬 드라이브에 저장되며, 모든 편집 내용도 로컬에 저장됩니다.

여러 옵션에 대한 자세한 내용은 [Project Setup 매뉴얼](https://www.defold.com/manuals/project-setup/)에서 확인할 수 있습니다.

## 에디터 언어

시작 화면의 왼쪽 아래에서 Language 선택 항목을 볼 수 있습니다. 현재 사용 가능한 지역화 중에서 선택하세요. 이 설정은 에디터의 `File ▸ Preferences ▸ General ▸ Editor Language`에서도 사용할 수 있습니다.

![언어](images/editor/languages.png)

## 에디터 창 {#the-editor-views}

Defold Editor는 특정 정보를 표시하는 여러 창 또는 뷰로 나뉩니다.

![에디터 2](images/editor/editor_overview.png)

### 1. Assets pane
프로젝트에 포함된 모든 파일과 폴더를 디스크의 구조와 같은 트리 구조로 나열합니다. 목록을 클릭하고 스크롤해서 탐색합니다. 이 뷰에서 모든 파일 관련 작업을 수행할 수 있습니다.

   - <kbd>Left Mouse Click</kbd>으로 파일이나 폴더를 선택하고, <kbd>⇧ Shift</kbd>를 누른 상태에서는 선택 범위를 확장할 수 있으며, <kbd>Ctrl</kbd>/<kbd>⌘ Cmd</kbd>를 누른 상태에서는 클릭한 항목을 선택하거나 선택 해제할 수 있습니다.
   - 파일을 <kbd>Double Mouse Click</kbd>하면 해당 파일 형식에 맞는 특정 에디터에서 열립니다.
   - <kbd>Drag and Drop</kbd>으로 디스크의 다른 위치에 있는 파일을 프로젝트에 추가하거나, 프로젝트 안에서 파일과 폴더를 새 위치로 이동할 수 있습니다.
   - <kbd>Right Mouse Click</kbd>으로 _Context Menu_를 열 수 있으며, 여기에서 새 파일이나 폴더를 만들고, 이름을 바꾸고, 삭제하고, 파일 종속성을 추적하는 등의 작업을 할 수 있습니다.

### 2. Scene Editor pane {#the-scene-editor}

컬렉션, 게임 오브젝트 또는 시각 컴포넌트 파일을 더블 클릭하면 씬을 만들고 편집하는 시각 에디터인 *Scene Editor*가 열립니다. 스크립트 파일과 기타 비시각 리소스는 대신 각각의 전용 에디터에서 열립니다.

![Scene Editor](images/editor/2d_scene.png)

Scene Editor가 제공하는 핵심 기능은 다음과 같습니다.

- 직교 및 원근 카메라 모드가 있는 [2D 및 3D 씬 탐색](/manuals/scene-editing/#2d-and-3d-scene-orientation)
- 오브젝트를 이동, 회전, 확대/축소하기 위한 [변형 도구](/manuals/scene-editing/#manipulating-objects)
- 1인칭 3D 탐색을 위한 [Free Camera Mode](/manuals/scene-editing/#free-camera-mode)
- 크기, 평면, 모양을 설정할 수 있는 [Grid settings](/manuals/scene-editing/#grid-settings)
- 컴포넌트 타입과 가이드를 토글하는 [Visibility filters](/manuals/scene-editing/#visibility-filters)

자세한 내용은 [Scene Editor 매뉴얼](/manuals/scene-editing/)을 읽어 보세요.

### 3. Outline pane

이 뷰는 현재 편집 중인 파일의 컨텐츠를 계층적 트리 구조로 보여 줍니다. Outline은 에디터 뷰를 반영하며, 항목에 대해 작업을 수행할 수 있게 합니다.

   - <kbd>Left Mouse Click</kbd>으로 항목을 선택하고, <kbd>⇧ Shift</kbd>를 누른 상태에서는 선택 범위를 확장할 수 있으며, <kbd>Ctrl</kbd>/<kbd>⌘ Cmd</kbd>를 누른 상태에서는 클릭한 항목을 선택하거나 선택 해제할 수 있습니다.
   - <kbd>Drag and drop</kbd>으로 항목을 이동합니다. 컬렉션 안에서 게임 오브젝트를 다른 게임 오브젝트 위에 놓으면 부모-자식 관계가 생성됩니다.
   - <kbd>Right Mouse Click</kbd>으로 _Context Menu_를 열 수 있으며, 여기에서 항목을 추가하거나 선택한 항목을 삭제하는 등의 작업을 할 수 있습니다.

목록에서 요소 오른쪽에 있는 작은 `👁` Eye Icon을 클릭하면 게임 오브젝트와 시각 컴포넌트의 표시 여부를 토글할 수 있습니다.

![Outline](images/editor/outline.png)

### 4. Properties pane

이 뷰는 현재 선택된 항목과 연결된 프로퍼티를 보여 줍니다. 예를 들어 Id, URL, Position, Rotation, Scale 및/또는 기타 컴포넌트별 프로퍼티와 스크립트의 커스텀 프로퍼티가 표시됩니다.

또한 `↕` Up-Down Arrow를 <kbd>Drag</kbd>하고 마우스를 움직여 지정된 숫자 프로퍼티의 값을 변경할 수 있습니다.

![Properties](images/editor/properties.png)

### 5. Tools pane

이 뷰에는 여러 탭이 있습니다.

*Console* tab : 게임이 실행되는 동안 발생하는 오류, 경고, 정보 엔진 출력 또는 사용자가 의도적으로 출력한 내용을 보여 줍니다.

*Build Errors* : 빌드 과정의 오류를 보여 줍니다.

*Search Results* : `Keep Results`를 클릭했을 때 전체 프로젝트 검색(<kbd>Ctrl</kbd>/<kbd>⌘ Cmd</kbd> + <kbd>Shift</kbd> + <kbd>F</kbd>) 결과를 보여 줍니다.

*Curve Editor* : [Particle Editor](/manuals/particlefx/)에서 커브를 편집할 때 사용됩니다.

Tools pane은 통합 디버거와 상호작용하는 데에도 사용됩니다. 자세한 내용은 [Debugging 매뉴얼](/manuals/debugging/)에서 확인하세요.

### 6. Changed Files pane

프로젝트가 분산 버전 관리 시스템인 Git을 사용한다면 이 뷰는 프로젝트에서 변경, 추가 또는 삭제된 모든 파일을 나열합니다. 프로젝트를 정기적으로 동기화하면 로컬 복사본을 프로젝트 Git 저장소에 저장된 내용과 맞출 수 있으며, 이를 통해 팀 안에서 공동작업을 할 수 있고 문제가 생겨도 작업을 잃지 않습니다. Git에 대한 자세한 내용은 [Version Control 매뉴얼](/manuals/version-control/)에서 확인할 수 있습니다. 이 뷰에서 일부 파일 관련 작업을 수행할 수 있습니다.

   - <kbd>Left Mouse Click</kbd> - 지정된 파일을 선택하고, <kbd>⇧ Shift</kbd>를 누른 상태에서는 선택 범위를 확장할 수 있으며, <kbd>Ctrl</kbd>/<kbd>⌘ Cmd</kbd>를 누른 상태에서는 클릭한 항목을 선택하거나 선택 해제할 수 있습니다. 변경된 파일 하나를 선택하면 `Diff`를 클릭해서 차이를 볼 수 있습니다. 선택한 모든 파일의 변경 사항을 되돌리려면 `Revert`를 클릭할 수 있습니다.
   - 파일을 <kbd>Double Left Mouse Click</kbd>하면 해당 파일의 뷰가 열립니다. 에디터는 Assets 뷰에서와 마찬가지로 파일을 적절한 에디터에서 엽니다.
   - 파일을 <kbd>Right Mouse Click</kbd>하면 팝업 메뉴가 열리며, 여기에서 diff 뷰를 열고, 파일에 적용된 모든 변경 사항을 되돌리고, 파일 시스템에서 파일을 찾는 등의 작업을 할 수 있습니다.

### Menu Bar

에디터 뷰의 위쪽 또는 Mac의 System Bar에서 `File`, `Edit`, `View`, `Project`, `Debug`, `Help` 6개 메뉴가 있는 Menu Bar를 찾을 수 있습니다. 각 기능은 매뉴얼에서 설명합니다.

### Status Bar

에디터의 아래쪽 바에는 Status가 표시되는 좁은 공간이 있습니다. 예를 들면 다음과 같습니다.
- 새 업데이트가 있으면 클릭할 수 있는 `Update Available` 버튼이 표시됩니다. 아래 이 매뉴얼의 에디터 업데이트 섹션을 확인하세요.
- 빌드 또는 번들링 중에는 진행 상태가 여기에 표시됩니다.

## 창 크기와 표시 여부

창 크기는 위에서 설명한 6개 창 사이의 섹션 경계를 <kbd>Dragging</kbd>해서 에디터 안에서 조정할 수 있습니다.

창 표시 여부는 `View` 메뉴의 옵션이나 지정된 단축키를 사용해서 에디터 안에서 토글할 수 있습니다.
- `Toggle Assets Pane` (<kbd>F6</kbd>)으로 Assets 및 Changed Files 창의 표시 여부를 토글합니다.
- `Toggle Changed Files`로 Changed Files 창만의 표시 여부를 토글합니다.
- `Toggle Tools Pane` (<kbd>F7</kbd>)으로 Tools 창의 표시 여부를 토글합니다.
- `Toggle Properties Pane` (<kbd>F8</kbd>)으로 Outline 및 Properties 창의 표시 여부를 토글합니다.

![창 표시 여부](images/editor/editor_panes.png)

`View` 메뉴에서는 Grid, Guides, Camera 같은 다른 표시 관련 설정을 토글하거나 변경할 수 있습니다. 또한 뷰를 선택 항목에 맞추거나(`Frame Selection` 또는 <kbd>F</kbd> 키), 기본 2D 뷰와 3D 뷰 사이를 전환할 수 있으며(`Realign Camera` 또는 <kbd>.</kbd> 키), 이 중 많은 기능은 Toolbar나 단축키로도 접근할 수 있습니다.

## 탭

여러 파일을 열어 두면 에디터 뷰의 위쪽에 파일마다 별도의 탭이 표시됩니다. 단일 창 안의 탭은 위치를 옮길 수 있습니다. 탭을 <kbd>Drag and Drop</kbd>해서 탭 바 안의 위치를 서로 바꿉니다. 다음 작업도 할 수 있습니다.

- 탭에서 <kbd>Right Mouse Click</kbd>하여 _Context Menu_를 엽니다.
- `Close`(<kbd>Ctrl</kbd>/<kbd>⌘ Cmd</kbd> + <kbd>W</kbd>)를 클릭해서 단일 탭을 닫습니다.
- `Close Others`를 클릭해서 선택한 탭을 제외한 모든 탭을 닫습니다.
- `Close All`(<kbd>Ctrl</kbd>/<kbd>⌘ Cmd</kbd> + <kbd>Shift</kbd>+<kbd>W</kbd>)을 클릭해서 활성 창의 모든 탭을 닫습니다.
- `➝| Open As`를 선택해서 기본 에디터가 아닌 다른 에디터나 `File ▸ Preferences ▸ Code ▸ Custom Editor`에 설정된 연결된 외부 도구를 사용합니다. 자세한 내용은 [Preferences 매뉴얼](/manuals/editor-preferences)에서 확인하세요.

![탭](images/editor/tabs_custom.png)

## 나란히 편집하기

에디터 뷰 2개를 나란히 열 수 있습니다.

- 이동하려는 에디터의 탭을 <kbd>Right Mouse Click</kbd>하고 `Move to Other Tab Pane`을 선택합니다.

![2개 창](images/editor/2-panes.png)

탭 메뉴에서 `Swap with Other Tab Pane`을 사용해 지정된 탭을 창 사이로 이동하거나, `Join Tab Panes`로 단일 창으로 합칠 수도 있습니다.

## 새 프로젝트 파일 만들기 {#creating-new-project-files}

새 리소스 파일을 만들려면 `File ▸ New…`를 선택한 다음 메뉴에서 파일 타입을 선택하거나, 컨텍스트 메뉴를 사용합니다.

`Assets` 브라우저에서 대상 위치를 <kbd>Right Mouse Click</kbd>한 다음 `New… ▸ [file type]`을 선택합니다.

![파일 만들기](images/editor/create_file.png)

새 파일에 적합한 *Name*을 입력하고, 필요하면 *Location*을 변경합니다. 파일 타입 접미사를 포함한 전체 파일 이름이 다이얼로그의 *Preview* 아래에 표시됩니다.

![파일 이름 만들기](images/editor/create_file_name.png)

## 템플릿

각 프로젝트에 커스텀 템플릿을 지정할 수 있습니다. 이렇게 하려면 프로젝트의 루트 디렉토리에 `templates`라는 새 폴더를 만들고, `/templates/default.gui` 또는 `/templates/default.script`처럼 원하는 확장자를 가진 `default.*` 이름의 새 파일을 추가합니다. 또한 이 파일에서 `{{NAME}}` 토큰을 사용하면 파일 생성 창에 지정된 파일 이름으로 대체됩니다.

지정된 파일 타입에 사용할 수 있는 템플릿이 있으면 이 타입의 새 파일을 만들 때마다 `templates`에 있는 파일의 컨텐츠로 초기화됩니다.


![템플릿](images/editor/templates.png)

## 프로젝트로 파일 임포트하기

프로젝트에 에셋 파일(이미지, 사운드, 모델 등)을 추가하려면 *Assets* 브라우저의 올바른 위치로 간단히 드래그-앤-드롭하면 됩니다. 이렇게 하면 프로젝트 파일 구조의 선택한 위치에 파일의 _복사본_이 만들어집니다. 자세한 내용은 [매뉴얼의 에셋 임포트 방법](/manuals/importing-assets/)을 읽어 보세요.

![파일 임포트](images/editor/import.png)

## 에디터 업데이트

에디터는 인터넷에 연결되어 있을 때 자동으로 업데이트를 확인합니다. 업데이트가 감지되면 프로젝트 선택 화면의 왼쪽 아래 또는 에디터 창의 오른쪽 아래에 파란색 클릭 가능 링크 `Update Available`이 표시됩니다.

![프로젝트 선택 화면에서 업데이트](images/editor/update_start.png)
![에디터에서 업데이트](images/editor/update_available.png)

다운로드하고 업데이트하려면 클릭 가능한 `Update Available` 링크를 누릅니다. 정보가 포함된 확인 창이 팝업으로 표시됩니다. 계속하려면 `Download Update`를 클릭하세요.

![에디터 업데이트 팝업](images/editor/update.png)

아래쪽 Status Bar에서 다운로드 진행률을 볼 수 있습니다.

![다운로드 진행률](images/editor/download_status.png)

업데이트가 다운로드되면 파란색 링크가 `Restart to Update`로 변경됩니다. 이를 클릭하면 다시 시작하고 업데이트된 에디터가 열립니다.

![업데이트를 위해 다시 시작](images/editor/restart_to_update.png)

## Preferences

`Preferences` 창에서 에디터 설정을 수정할 수 있습니다. 창을 열려면 `File ▸ Preferences…`를 클릭하거나 단축키 <kbd>Ctrl</kbd>/<kbd>⌘ Cmd</kbd> + <kbd>,</kbd>를 사용하세요.

자세한 내용은 [Preferences 매뉴얼](/manuals/editor-preferences)에서 확인하세요.

![Preferences](images/editor/preferences.png)

## 에디터 로그 {#editor-logs}
에디터에 문제가 발생해 이슈를 보고해야 한다면(`Help  ▸ Report Issue`), 에디터 자체의 로그 파일을 제공하는 것이 좋습니다. 시스템 브라우저에서 로그 위치를 열려면 `Help ▸ Show Logs`를 클릭합니다.

자세한 내용은 [Getting Help 매뉴얼](/manuals/getting-help/#getting-help)을 읽어 보세요.

![Show Logs](images/editor/show_logs.png)

에디터 로그 파일은 다음 위치에서 찾을 수 있습니다.

  * Windows: `C:\Users\ **Your Username** \AppData\Local\Defold`
  * macOS: `/Users/ **Your Username** /Library/Application Support/` 또는 `~/Library/Application Support/Defold`
  * Linux: `$XDG_STATE_HOME/Defold` 또는 `~/.local/state/Defold`

에디터가 터미널/명령 프롬프트에서 시작된 경우 실행 중에도 에디터 로그에 접근할 수 있습니다. 에디터를 실행하려면 다음 명령을 사용합니다.

```shell
# Linux:
$ ./path/to/Defold/Defold

# macOS:
$ > ./path/to/Defold.app/Contents/MacOS/Defold
```

## 에디터 서버

에디터가 프로젝트를 열면 임의의 포트에서 웹 서버를 시작합니다. 서버는 다른 어플리케이션에서 에디터와 상호작용하는 데 사용할 수 있습니다. 포트는 `.internal/editor.port` 파일에 기록됩니다.

서버는 `http://localhost:$(cat .internal/editor.port)/openapi.json`에서 OpenAPI 명세를 제공합니다. 에이전트 기반 워크플로를 시작하기 위한 유용한 최소 출발점입니다.

또한 에디터 실행 파일에는 실행 중 포트를 지정할 수 있는 커맨드 라인 옵션 `--port`(또는 `-p`)가 있습니다. 예:
```shell
# Windows
.\path\to\Defold\Defold.exe --port 8181

# Linux:
./path/to/Defold/Defold --port 8181

# macOS:
./path/to/Defold/Defold.app/Contents/MacOS/Defold --port 8181
```

## 에디터 설치 메타데이터

에디터가 시작되면 런처와 설치 경로 정보를 잘 알려진 위치에 기록합니다. 서드파티 IDE 통합과 다른 도구는 이 정보를 사용해 설치된 Defold 에디터를 찾을 수 있습니다.

| OS      | 위치 |
|---------|------|
| macOS   | `~/Library/Application Support/Defold/installations.json` |
| Linux   | `${XDG_STATE_HOME:-~/.local/state}/Defold/installations.json` |
| Windows | `%LOCALAPPDATA%\Defold\installations.json` |

이 파일은 알려진 설치마다 하나의 객체를 가진 JSON 배열을 포함합니다.

```json
[
  {
    "launcherPath": "/Applications/Defold.app/Contents/MacOS/Defold",
    "installPath": "/Applications/Defold.app",
    "lastLaunchedAt": "2026-07-06T12:34:56.789Z"
  }
]
```

## 에디터 스타일링

에디터의 외형은 커스텀 스타일링으로 변경할 수 있습니다. 자세한 내용은 [Editor Styling 매뉴얼](/manuals/editor-styling)을 읽어 보세요.

## FAQ
:[Editor FAQ](../shared/editor-faq.md)
