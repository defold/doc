
# Facebook
Facebook API 는  iOS, Android, HTML5 게임을 위해 규격화된 방법으로 Facebook의 게임 연동 기능과 상호작용 할 수 있게 해 줍니다.

Defold Facebook API 는 다양한 플랫폼에서 돌아가는 Facebook API를 iOS, Android, HTML5 (Facebook Canvas를 통해서)에서 동일하게 동작하게끔 통일된 함수들을 제공합니다. 게임에서 Facebook 연동을 시작하려면 Facebook 계정이 필요합니다.

> Defold 1.2.92 에서 Facebook API가 새로운 방법으로 재설계 되었습니다. 이전 API도 여전이 작동하므로 크리티컬한 변경사항은 없습니다. 하지만 예전 API는 새로운 어플리케이션에는 사용하지 않는 것이 좋습니다.

## Registering as a Facebook developer
Facebook 연동 개발을 하려면 Facebook developer에 가입해야 합니다. 여기서 Defold 게임과 커뮤니케이션 할 수 있는 Facebook 어플리케이션을 생성할 수 있습니다.

* [Facebook for developers](https://developers.facebook.com/)로 이동합니다.
* Facebook 계정으로 로그인 합니다.
* 지침에 따라 개발자 계정을 등록하고 확인합니다.

![Register as a developer](images/facebook/register_dev.png)

![developer](images/facebook/register_verify.png)

## Creating a Facebook app
다음 단계는 Facebook application을 생성하는 것입니다. 구석에 My Apps 메뉴를 열어서 생성한 앱 목록을 볼 수 있습니다. 여기서 Add a New App 을 선택합니다.

![Add new app](images/facebook/add_new_app_menu.png)

타겟 플랫폼 선택화면이 나타나면 **basic setup** 를 클릭해서 마법사(wizards)를 스킵합니다.

> 마법사를 통해 제공되는 대부분의 정보는 Defold의 개발과는 무관합니다. 특히 일반적으로  "Info.plist" 또는 "AndroidManifest.xml" 을 직접 편집할 필요가 없습니다.

![Add new app platform](images/facebook/add_new_app_platform.png)

앱 대쉬보드에서는 플랫폼 설정을 쉽게 추가, 삭제, 변경할 수 있습니다. 이제 앱의 이름을 지정하고 **Display Name**, **Namespace**, **Category** 를 선택할 수 있습니다. 다시 말하지만, 이 모든 값들은 앱 대쉬보드에서 수정해야 합니다. 이 과정을 마치면 Facebook은 고유한 앱 식별자로 앱을 생성합니다. **App ID** 는 특정 앱을 식별한 이후로는 변경하는 것이 불가능합니다.

![New app id](images/facebook/new_app_id.png)

![App dashboard settings](images/facebook/add_platform.png)

**Settings** 탭을 클릭해서 숫자로 된 **App ID**를 확인합니다. 이 식별자는 Defold 게임의 [project settings](/manuals/project-settings)에 필요한 값입니다. 불행히도 이 설정은 에디터에서는 숨겨져 있지만(곧 변경될 예정임), "game.project"에 마우스 오른쪽 클릭해서 **Open With ▸ Text Editor** 메뉴를 선택해서 식별자를 쉽게 추가할 수 있습니다.

![Open project settings with](images/facebook/project_open_with.png)

[facebook] 섹션에 **App ID**에 해당하는 appid=456788687846098 를 추가합니다. 숫자가 맞는지 확인하고 파일을 저장합니다.

![Game project](images/facebook/game_project.png)

이제, Facebook 앱 페이지의 **Settings** 탭으로 돌아와서 **\+ Add Platform** 를 클릭해서 앱에 새 플랫폼을 추가합니다. 각 플랫폼 별로 채워야하는 설정 항목들이 있습니다.

![Select platform](images/facebook/select_platform.png)

## iOS
iOS의 경우 "game.project"에 설정한 **bundle_identifier** 를 Bundle ID에 지정해야 합니다.

![iOS settings](images/facebook/settings_ios.png)

## Android
Android의 경우 **Google Play Package Name**에 "game.project"에서 설정한 **package** 식별자를 지정해야 합니다.  또한 인증서의 해쉬값을 생성해서 **Key Hashes** 필드에 입력해야 합니다. openssl 을 사용하여  "certificate.pem"에서 해쉬를 생성할 수 있습니다.

```
$ cat certificate.pem | openssl x509 -outform der | openssl sha1 -binary | openssl base64
```

(서명 파일을 생성하는 자세한 방법은 Android 매뉴얼의 [Creating certificates and keys](/manuals/android#Creating-certificates-and-keys)에서 참고 바랍니다.)

![Android settings](images/facebook/settings_android.png)

## Facebook Canvas
HTML5 게임의 경우에는 작업과정이 약간 다릅니다. Facebook은 어딘가로부터 게임 컨텐츠를 액세스 할 수 있게 해야합니다. 여기 두 가지 옵션이 있습니다.

![Facebook Canvas settings](images/facebook/settings_canvas.png)

1. Facebook의 **Simple Application Hosting** 를 사용합니다. **Yes**를 클릭해서 페이스북이 관리하는 호스팅을 선택합니다. **uploaded assets** 를 선택해서 hosted asset manager를 엽니다.
![Simple hosting](images/facebook/simple_hosting.png)
"HTML5 Bundle"을 선택합니다:
![HTML5 bundle](images/facebook/html5_bundle.png)
HTML5 bundle을 .7z 또는 .zip 으로 압축해서 Facebook에 업로드 합니다. **Push to production** 를 클릭해서 게임 서비스를 시작합니다.

2. Facebook 호스팅의 대안으로는 HTTPS 를 통해 게임을 서비스하는 특정 서버로 HTML5 bundle 을 업로드 하는 방법이 있습니다. **Secure Canvas URL**를 게임의 URL로 설정합니다.

이제, **Canvas Page**로 제공된 Facebook URL 을 통하여 게임이 작동하게 됩니다.

## Testing the setup
다음의 기본적인 테스트를 사용하여 올바르게 설정되었는지 확인할 수 있습니다.

1. 새 게임 오브젝트를 만들어 새 스크립트 컴포넌트를 추가함
2. 스크립트 파일에 아래 코드를 입력함

```lua
local function get_me_callback(self, id, response)
    -- response 테이블은 모든 응답 데이터를 포함하고 있음
    pprint(response)
end

local function fb_login(self, data)
    if data.status == facebook.STATE_OPEN then
        -- 로그인에 성공하면 HTTP graph API를 통해 "me" 데이터를 읽어보자
        local token = facebook.access_token()
        local url = "https://graph.facebook.com/me/?access_token=" .. token
        http.request(url, "GET", get_me_callback)
    elseif data.status == facebook.STATE_CLOSED_LOGIN_FAILED then
        -- 로그인 실패시 뭔가 처리하자...
    end
    if data.error then
        -- 에러 발생
    else
        -- 에러 없음
    end
end

function init(self)
    -- 읽기 권한으로 로그인하기
    local permissions = { "public_profile", "email" }
    facebook.login_with_read_permissions(permissions, fb_login)
end
```

이 간단한 테스트를 실행하면 콘솔창에 아래와 같은 내용이 표시됩니다.

```
DEBUG:SCRIPT:
{
  status = 200,
  headers = {
    connection = keep-alive,
    date = Fri, 04 Nov 2016 13:54:33 GMT,
    etag = "0725a4f703fe6af27da183cfec0bb22637e331e0",
    access-control-allow-origin = *,
    content-length = 53,
    expires = Sat, 01 Jan 2000 00:00:00 GMT,
    content-type = text/javascript; charset=UTF-8,
    x-fb-debug = Pr1qUssb8Xa3x3r1t913hHMdefh69DSYYV5vcxeOB7O33mcfShIw+r7BoLpn147I2wzLF2CZRTpnR3/VYOtFpA==,
    facebook-api-version = v2.5,
    cache-control = private, no-cache, no-store, must-revalidate,
    pragma = no-cache,
    x-fb-trace-id = F03S5dtsdaS,
    x-fb-rev = 2664414,
  }
  response = {"name":"Max de Fold ","id":"14159265358979323"},
}
```

* 전체 Defold Facebook API 는 [Facebook reference documentation](http://www.defold.com/ref/facebook) 에 문서화 되어 있습니다.
* Facebook Graph API 는 https://developers.facebook.com/docs/graph-api 에 문서화 되어 있습니다.

## Development caveats
개발중에는 dev application으로 사용하는 것이 매우 편리합니다. 불행히도 Facebook API는 번들링 된 "Info.plist" 파일이 구성되어야 하는 방법에 따라 dev 앱에서 아직 동작하지 않습니다. 하지만 모든 디버그 번들은 dev 앱으로 동작하므로, 다른 해결책으로는 적절한 Facebook 프로젝트 설정으로 게임을 빌드하고, 장치에 넣고, 실행중인 게임에 연결하고, 평상시 처럼 데이터를 에디터에서 스트림하면 됩니다.

