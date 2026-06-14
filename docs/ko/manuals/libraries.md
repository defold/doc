---
title: Defold에서 라이브러리 프로젝트 작업하기
brief: 라이브러리 기능은 프로젝트 간에 에셋을 공유할 수 있게 해 줍니다. 이 매뉴얼은 이 기능이 어떻게 동작하는지 설명합니다.
---

# 라이브러리

라이브러리 기능은 프로젝트 간에 에셋을 공유할 수 있게 해 줍니다. 간단하지만 매우 강력한 메커니즘이며 워크플로우에서 여러 방법으로 사용할 수 있습니다.

라이브러리는 다음 용도에 유용합니다.

* 완성된 프로젝트에서 새 프로젝트로 에셋을 복사할 때. 이전 게임의 속편을 만들고 있다면 쉽게 시작할 수 있는 방법입니다.
* 프로젝트로 복사한 뒤 커스터마이징하거나 특화할 수 있는 템플릿 라이브러리를 만들 때.
* 직접 참조할 수 있는 완성된 오브젝트나 스크립트 라이브러리를 하나 이상 만들 때. 공통 스크립트 모듈을 저장하거나 그래픽, 사운드, 애니메이션 에셋의 공유 라이브러리를 만들 때 매우 편리합니다.

## 라이브러리 공유 설정

공유 스프라이트와 타일 소스를 포함하는 라이브러리를 만들고 싶다고 가정해 보겠습니다. 먼저 [새 프로젝트를 설정](/manuals/project-setup/)합니다. 프로젝트에서 공유할 폴더를 정하고 해당 폴더 이름을 Project settings의 *`include_dirs`* 프로퍼티에 추가합니다. 폴더를 둘 이상 나열하려면 이름을 공백으로 구분합니다.

![포함 디렉토리](images/libraries/libraries_include_dirs.png)

이 라이브러리를 다른 프로젝트에 추가하기 전에 라이브러리의 위치를 찾을 방법이 필요합니다.

## 라이브러리 URL

라이브러리는 표준 URL을 통해 참조됩니다. GitHub에 호스팅된 프로젝트라면 프로젝트 릴리스의 URL이 됩니다.

![GitHub 라이브러리 URL](images/libraries/libraries_library_url_github.png)

::: important
라이브러리 프로젝트의 master 브랜치가 아니라 특정 릴리스에 항상 의존하는 것을 권장합니다. 이렇게 하면 라이브러리 프로젝트의 master 브랜치에서 최신 변경사항을 항상 받아 오는 대신, 개발자가 라이브러리 프로젝트의 변경사항을 언제 반영할지 직접 결정할 수 있습니다. 최신 변경사항에는 호환성을 깨는 변경이 포함될 수 있습니다.
:::

::: important
서드파티 라이브러리는 사용하기 전에 항상 검토하는 것을 권장합니다. [서드파티 소프트웨어 사용 보안](https://defold.com/manuals/application-security/#securing-your-use-of-third-party-software)에 대해 자세히 알아보세요.
:::

### 기본 액세스 인증

공개되지 않은 라이브러리를 사용할 때 기본 액세스 인증을 수행하려면 라이브러리 URL에 사용자 이름과 암호/토큰을 추가할 수 있습니다.

```
https://username:password@github.com/defold/private/archive/main.zip
```

`username` 및 `password` 필드는 추출되어 `Authorization` 요청 헤더로 추가됩니다. 기본 액세스 인증을 지원하는 모든 서버에서 동작합니다.

::: important
생성한 personal access token이나 암호가 잘못된 사람에게 넘어가면 심각한 결과가 생길 수 있으므로 공유하거나 실수로 유출하지 않도록 주의하세요!
:::

라이브러리 URL에 인증 정보를 일반 텍스트로 넣어 실수로 유출하는 일을 피하려면 문자열 치환 패턴을 사용하고 인증 정보를 환경 변수로 저장할 수도 있습니다.

```
https://__PRIVATE_USERNAME__:__PRIVATE_TOKEN__@github.com/defold/private/archive/main.zip
```

위 예제에서는 사용자 이름과 토큰을 시스템 환경 변수 `PRIVATE_USERNAME` 및 `PRIVATE_TOKEN`에서 읽습니다.

#### GitHub 인증

GitHub의 비공개 저장소에서 가져오려면 [personal access token을 생성](https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/creating-a-personal-access-token)하고 이를 암호로 사용해야 합니다.

```
https://github-username:personal-access-token@github.com/defold/private/archive/main.zip
```

#### GitLab 인증

GitLab의 비공개 저장소에서 가져오려면 [personal access token을 생성](https://docs.gitlab.com/ee/security/token_overview.html)하고 URL 파라미터로 보내야 합니다.

```
https://gitlab.com/defold/private/-/archive/main/test-main.zip?private_token=personal-access-token
```

### 고급 액세스 인증

기본 액세스 인증을 사용하면 사용자의 액세스 토큰과 사용자 이름이 프로젝트에 사용되는 모든 저장소에서 공유됩니다. 팀원이 2명 이상인 팀에서는 문제가 될 수 있습니다. 이 문제를 해결하려면 저장소의 라이브러리 접근에 "read only" 사용자를 사용해야 합니다. GitHub에서는 이를 위해 조직, 팀, 그리고 저장소를 편집할 필요가 없는 사용자, 즉 read only 사용자가 필요합니다.

GitHub 단계:
* [조직 생성](https://docs.github.com/en/github/setting-up-and-managing-organizations-and-teams/creating-a-new-organization-from-scratch)
* [조직 안에 팀 생성](https://docs.github.com/en/github/setting-up-and-managing-organizations-and-teams/creating-a-team)
* [원하는 비공개 저장소를 조직으로 이전](https://docs.github.com/en/github/administering-a-repository/transferring-a-repository)
* [팀에 저장소 "read only" 접근 권한 부여](https://docs.github.com/en/github/setting-up-and-managing-organizations-and-teams/managing-team-access-to-an-organization-repository)
* [이 팀에 포함될 사용자 생성 또는 선택](https://docs.github.com/en/github/setting-up-and-managing-organizations-and-teams/organizing-members-into-teams)
* 위의 "기본 액세스 인증"을 사용해 이 사용자의 personal access token 생성

이 시점에서 새 사용자의 인증 세부 정보를 저장소에 커밋하고 푸시할 수 있습니다. 이렇게 하면 비공개 저장소로 작업하는 누구나 라이브러리 자체에 대한 편집 권한 없이도 해당 저장소를 라이브러리로 가져올 수 있습니다.

::: important
read only 사용자의 토큰은 해당 라이브러리를 사용하는 게임 저장소에 접근할 수 있는 누구에게나 완전히 노출됩니다.
:::

이 해결책은 Defold 포럼에서 제안되었으며 [이 스레드에서 논의되었습니다](https://forum.defold.com/t/private-github-for-library-solved/67240).

## 라이브러리 종속성 설정 {#setting-up-library-dependencies}

라이브러리에 접근하려는 프로젝트를 엽니다. 프로젝트 설정에서 Library URL을 *dependencies* 프로퍼티에 추가합니다. 원하는 경우 여러 종속 프로젝트를 지정할 수 있습니다. `+` 버튼으로 하나씩 추가하고 `-` 버튼으로 제거하면 됩니다.

![종속성](images/libraries/libraries_dependencies.png)

이제 라이브러리 종속성을 업데이트하려면 <kbd>Project ▸ Fetch Libraries</kbd>를 선택합니다. 프로젝트를 열 때마다 자동으로 수행되므로, 프로젝트를 다시 열지 않은 상태에서 종속성이 변경된 경우에만 이 작업이 필요합니다. 종속 라이브러리를 추가하거나 제거한 경우, 또는 종속 라이브러리 프로젝트 중 하나가 다른 사람에 의해 변경되고 동기화된 경우가 이에 해당합니다.

![Fetch Libraries](images/libraries/libraries_fetch_libraries.png)

이제 공유한 폴더가 *Assets pane*에 표시되며 공유한 모든 항목을 사용할 수 있습니다. 라이브러리 프로젝트에 동기화된 모든 변경사항은 프로젝트에서 사용할 수 있습니다.

![라이브러리 설정 완료](images/libraries/libraries_done.png)

## 라이브러리 종속성의 파일 편집

라이브러리의 파일은 저장할 수 없습니다. 변경할 수는 있으며, 에디터는 테스트에 유용하도록 그 변경사항으로 빌드할 수 있습니다. 하지만 파일 자체는 변경되지 않고, 파일을 닫으면 모든 수정사항이 폐기됩니다.

라이브러리 파일을 변경하려면 라이브러리를 포크(fork)하고 그곳에서 변경해야 합니다. 또 다른 방법은 전체 라이브러리 폴더를 프로젝트 디렉토리에 복사하여 로컬 사본을 사용하는 것입니다. 이 경우 로컬 폴더가 원래 종속성을 가리게 되며, `game.project`에서 종속성 링크를 제거해야 합니다. 이후 <kbd>Project ▸ Fetch Libraries</kbd>를 선택하는 것을 잊지 마세요.

`builtins`도 엔진에서 제공하는 라이브러리입니다. 이곳의 파일을 편집하려면 원래 `builtins` 파일 대신 사용할 수 있도록 프로젝트로 복사해야 합니다. 예를 들어 `default.render_script`를 수정하려면 `/builtins/render/default.render`와 `/builtins/render/default.render_script`를 둘 다 프로젝트 폴더에 `my_custom.render` 및 `my_custom.render_script`로 복사합니다. 그런 다음 로컬 `my_custom.render`가 빌트인 스크립트 대신 `my_custom.render_script`를 참조하도록 업데이트하고, `game.project`의 Render 설정에서 커스텀 `my_custom.render`를 설정합니다.

메터리얼을 복사 붙여넣기한 뒤 특정 타입의 모든 컴포넌트에서 사용하고 싶다면 [프로젝트별 템플릿](/manuals/editor/#creating-new-project-files)을 사용하는 것이 유용할 수 있습니다.

## 깨진 참조

라이브러리 공유에는 공유된 폴더 아래에 위치한 파일만 포함됩니다. 공유 계층구조 밖에 있는 에셋을 참조하는 항목을 만들면 참조 경로가 깨집니다.

## 이름 충돌

*dependencies* 프로젝트 설정에 여러 프로젝트 URL을 나열할 수 있으므로 이름 충돌이 발생할 수 있습니다. 두 개 이상의 종속 프로젝트가 *`include_dirs`* 프로젝트 설정에서 같은 이름의 폴더를 공유하면 이런 일이 발생합니다.

Defold는 *dependencies* 목록에 지정된 프로젝트 URL 순서에서 같은 이름의 폴더에 대한 마지막 참조를 제외하고 모두 무시하는 방식으로 이름 충돌을 해결합니다. 예를 들어 dependencies에 3개의 라이브러리 프로젝트 URL을 나열했고 모두 *items*라는 폴더를 공유한다면, URL 목록에서 가장 마지막에 있는 프로젝트의 *items* 폴더 하나만 표시됩니다.
