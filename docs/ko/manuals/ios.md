---
title: Defold manual
---

# Developing games for iOS
이 매뉴얼은 Defold에서 iOS 장치의 앱과 게임을 개발하는 방법을 설명합니다.

iOS 개발은 개발중에도 iOS 기기에 앱이나 게임을 올릴 수 있도록 개발자 등록을 해야 한다는 점에서 Android 개발과 다릅니다. 또 iOS는 휴대폰이나 타블렛에 있는 모든 앱이 Apple이 발행한 인증서(certificate)와 프로비져닝 프로파일(provisioning profile)에 서명해야 한다고 요구합니다.

## Apple’s code signing process
iOS 앱과 관련된 보안은 여러가지 요소로 구성되어 있습니다. 필요한 도구에 액세스 하려면 우선 [Apple’s iOS Developer Program](https://developer.apple.com/programs/)에 가입해야 합니다. 등록 후에는 [Apple’s Developer Member Center](https://developer.apple.com/membercenter/index.action) 로 이동하기 바랍니다.

![Apple Member Center](images/ios/apple_member_center.png)

**Certificates, Identifiers & Profiles** 섹션은 필요한 모든 도구를 포함하고 있으며 여기에서 생성, 삭제, 수정이 가능합니다.

#### Certificates
Apple은 당신을 개발자로 식별하는 암호화된 인증서를 발행합니다. 당신은 development 또는 production 인증서를 생성할 수 있습니다. Developer 인증서는 샌드박스 테스트 환경에서 인앱결제(in-app purchase) 같은 특정한 기능을 테스트 할 수 있게 해 줍니다. Production 인증서는 App Store에 완성된 앱을 업로드 하기 위해 서명하는데 사용됩니다. 테스트를 하려면 당신의 기기에 앱을 설치하기 전에 인증서 부터 서명해야 합니다.

#### Identifiers
다양한 용도의 식별자. 여러 앱에서 사용할 수 있는 와일드카드 식별자(예를 들어 "some.prefix.\*")를 등록할 수 있습니다. App ID는 Passbook integration과 Game Center 등의 활성화 여부와 같은 Application Service 정보를 포함할 수 있습니다. 이러한 App ID는 와일드카드 식별자가 될 수 없습니다. Application Services가 작동하려면 어플리케이션의 "bundle identifier" 가 App ID 식별자와 일치해야만 합니다.

#### Devices
각 개발 장치는 UDID (Unique Device IDentifier)를 등록해야 합니다. 장치에서 UDID를 알아내는 방법은 아래를 참고 바랍니다.

#### Provisioning Profiles
프로비져닝 프로파일은 특정 장치와 App ID를 사용한 인증서와 관련되어 있습니다. 이는 기본적으로 어떤 개발자가 어떤 장치에서 어떤 앱을 사용할 수 있는지를 알려줍니다.

Defold에서 게임이나 앱에 서명할 때에는 유효한 인증서와 유효한 프로비져닝 프로파일이 필요합니다.

> Member Center 홈페이지에서 할 수 있는 일 중에 일부는 Xcode 개발환경 내에서도 수행할 수 있습니다.

## Device UDID
iOS 장치의 UDID는 와이파이나 케이블로 컴퓨터에 연결해서 알아낼 수 있습니다. iTunes 를 열어서 장치 아이콘을 클릭하고 당신의 장치를 선택하세요.

![iTunes devices](images/ios/itunes_devices.png)

**Summary** 페이지에서 **Serial Number** 를 찾습니다.

![Device UDID step 1](images/ios/udid.png)

**Serial Number**를 클릭해서 이 필드를 **UDID**로 변경합니다. 반복적으로 클릭하면 이 장치에 대한 여러 정보들이 표시되므로 **UDID**가 나올 때 까지 계속 클릭해도 됩니다. 긴 UDID 문자열을 마우스 오른쪽 클릭해서 **Copy** 를 눌러 식별자를 클립보드로 복사합니다. 그러면 Apple’s Developer Member Center에서 장치를 등록할 때 UDID 필드에 쉽게 붙여넣기 할 수 있습니다.

![Device UDID step 2](images/ios/udid_2.png)

## Signing the Defold development app
development app은 와이파이를 통해 컨텐츠를 설치할 수 있는 아주 편리한 버전입니다. 장치에 development app을 설치하고 앱을 시작한 다음 에디터에서 해당 장치를 빌드 대상으로 선택합니다.

현재, 최소한 팀원 한 명은 macOS를 실행하고 다른 팀 멤버를 위해 development app를 서명하려고 Apple Developer에 등록할 필요가 있습니다. 우리는 이 사람을 서명인(signer)이라고 부르도록 하겠습니다.

* 서명인의 컴퓨터에 설치된 인증서가 있어야 합니다.
* 서명인의 컴퓨터에 모바일 프로비져닝 프로파일이 있어야 합니다.
* 서명인은 다른 멤버들로부터 UDID를 수집하고 모바일 프로비져닝 프로파일에 추가해야 합니다.

서명된 development app을 Defold Dashboard에 업로드 하려면, 아래 단계가 필요합니다.

1. 에디터에서, **Project > Sign App…​** 선택
2. 당신의 code signing identity 선택
3. 당신의 mobile provisioning 파일 찾기
4. **Sign and upload** 버튼 누르기

![Signing the app](images/ios/sign.png)

Defold dev app은 Dashboard의 프로젝트 페이지로 업로드 됩니다. 각 프로젝트 멤버는 다음 작업을 할 수 있습니다.

1. iOS 장치에서 Dashboard를 탐색
2. 프로젝트의 목록에서 프로젝트 페이지를 염
3. **Members** 섹션 아래에 있는 **Install the Defold App** 링크를 클릭함

이 비디오는 전체 프로세스를 보여줍니다.
https://www.youtube.com/watch?v=T_igYdHubqA

### Launching the game
iOS 장치에서 게임을 실행하려면 Defold dev app과 에디터가 같은 와이파이 네트워크상에서 연결 가능해야 합니다.

1. 에디터가 실행중인지 확인하기
2. iOS 장치에서 Defold dev app 실행하기
3. 에디터에서  **Project > Targets** 에 있는 당신의 장치 선택
4. 게임을 실행하기 위해 **Project > Build And Launch** 선택하기. 게임 컨텐츠가 네트워크를 통해서 장치로 스트림 되므로 게임이 시작되는데 시간이 걸릴 수 있음.
5. 게임이 실행되는 동안, 평소처럼 [핫 리로드(hot-reload)](/manuals/debugging#hot-reloading)도 할 수 있음

## Creating an iOS application bundle
에디터에서 게임용 독립 어플리케이션 번들(stand alone application bundle)도 쉽게 생성할 수 있습니다. 메뉴에서 **Project > Bundle…​ > iOS Application…​** 를 선택하기만 하면 됩니다.

![Signing iOS bundle](images/ios/sign_bundle.png)

당신의 code signing identity를 선택하고 당신의 mobile provisioning 파일을 탐색합니다. **Package** 버튼을 누르면 컴퓨터에서 번들이 생성될 위치를 지정하라는 창이 뜹니다.

![ipa iOS application bundle](images/ios/ipa_file.png)

에디터는 iOS 어플리케이션 번들로  **.ipa** 파일을 생성합니다. 이 파일은 iTunes로 드래그-앤-드롭 해서 다음 동기화 중에 당신의 장치에 설치하게 됩니다. *game.project* 프로젝트 설정 파일에서 실행 스크린 이미지나 앱에서 사용할 아이콘 등을 지정할 수도 있습니다.

## Troubleshooting
### 어플리케이션을 다운로드 할 수 없을 경우
서명인(signer)이 앱을 서명하는데 사용되는 mobile provisioning에 UDID를 제대로 추가했는지 확인합니다.

### 내 장치가 Targets 메뉴에 나타나지 않을 경우
당신의 장치가 컴퓨터와 동일한 와이파이 네트워크에 연결되어 있는지 확인합니다.

### 버전이 맞지 않는다(mis-matching versions)는 메세지로 게임이 시작되지 않는 경우
이 문제는 에디터를 최신 버전으로 업그레이드 했을 때 발생합니다. **Sign and Upload**를 다시 해서 현재 엔진 버전에서 새 dev app을 생성해야 합니다. 당신의 기기의 dashboard에서 다시 앱을 다운로드 하세요.
