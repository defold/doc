---
title: 기기에서 개발용 앱 실행하기
brief: 이 매뉴얼은 기기에서 반복 개발을 할 수 있도록 개발용 앱을 기기에 넣는 방법을 설명합니다.
---

# 모바일 개발용 앱

개발용 앱을 사용하면 wifi를 통해 컨텐츠를 앱으로 전송할 수 있습니다. 변경 사항을 테스트할 때마다 매번 번들링하고 설치할 필요가 없으므로 반복 작업 시간을 크게 줄일 수 있습니다. 개발용 앱을 기기에 설치하고 앱을 시작한 다음, 에디터에서 해당 기기를 빌드 타겟으로 선택합니다.

## 개발용 앱 설치하기

Debug 모드로 번들링한 iOS 또는 Android 어플리케이션은 모두 개발용 앱 역할을 할 수 있습니다. 실제로 개발용 앱은 올바른 프로젝트 설정을 가지고 있고 작업 중인 프로젝트와 같은 [네이티브 익스텐션](/manuals/extensions/)을 사용하므로, 이 방식을 권장합니다.

프로젝트를 컨텐츠 없이 Debug variant로 번들링할 수 있습니다. 이 옵션을 사용하면 이 매뉴얼에서 설명하는 반복 개발에 적합하고 네이티브 익스텐션이 포함된 어플리케이션 버전을 만들 수 있습니다.

![컨텐츠 없는 번들](images/dev-app/contentless-bundle.png)

### iOS에 설치하기

iOS용으로 번들링하려면 [iOS 매뉴얼의 안내](/manuals/ios/#creating-an-ios-application-bundle)를 따르세요. variant로 Debug를 선택해야 합니다!

### Android에 설치하기

Android용으로 번들링하려면 [Android 매뉴얼의 안내](https://defold.com/manuals/android/#creating-an-android-application-bundle)를 따르세요.

## 게임 실행하기

기기에서 게임을 실행하려면 개발용 앱과 에디터가 같은 wifi 네트워크 또는 USB(아래 참고)를 통해 연결될 수 있어야 합니다.

1. 에디터가 실행 중인지 확인합니다.
2. 기기에서 개발용 앱을 실행합니다.
3. 에디터에서 <kbd>Project ▸ Targets</kbd> 아래의 기기를 선택합니다.
4. 게임을 실행하려면 <kbd>Project ▸ Build</kbd>를 선택합니다. 게임 컨텐츠가 네트워크를 통해 기기로 스트리밍되므로 게임이 시작되기까지 시간이 걸릴 수 있습니다.
5. 게임이 실행 중인 동안에는 평소처럼 [핫 리로드](/manuals/hot-reload/)를 사용할 수 있습니다.

### Windows에서 USB를 사용해 iOS 기기에 연결하기

Windows에서 USB를 통해 iOS 기기에서 실행 중인 개발용 앱에 연결하려면 먼저 [iTunes를 설치](https://www.apple.com/lae/itunes/download/)해야 합니다. iTunes가 설치되면 iOS 기기의 Settings 메뉴에서 [Personal Hotspot을 활성화](https://support.apple.com/en-us/HT204023)해야 합니다. "Trust This Computer?"를 탭하라는 알림이 표시되면 Trust를 탭하세요. 이제 개발용 앱이 실행 중일 때 기기가 <kbd>Project ▸ Targets</kbd> 아래에 표시되어야 합니다.

### Linux에서 USB를 사용해 iOS 기기에 연결하기

Linux에서는 USB로 연결할 때 기기의 Settings 메뉴에서 Personal Hotspot을 활성화해야 합니다. "Trust This Computer?"를 탭하라는 알림이 표시되면 Trust를 탭하세요. 이제 개발용 앱이 실행 중일 때 기기가 <kbd>Project ▸ Targets</kbd> 아래에 표시되어야 합니다.

### macOS에서 USB를 사용해 iOS 기기에 연결하기

최신 iOS 버전에서는 macOS에서 USB로 연결하면 기기와 컴퓨터 사이에 새 ethernet 인터페이스가 자동으로 열립니다. 개발용 앱이 실행 중일 때 기기가 <kbd>Project ▸ Targets</kbd> 아래에 표시되어야 합니다.

오래된 iOS 버전에서는 macOS에서 USB로 연결할 때 기기의 Settings 메뉴에서 Personal Hotspot을 활성화해야 합니다. "Trust This Computer?"를 탭하라는 알림이 표시되면 Trust를 탭하세요. 이제 개발용 앱이 실행 중일 때 기기가 <kbd>Project ▸ Targets</kbd> 아래에 표시되어야 합니다.

### macOS에서 USB를 사용해 Android 기기에 연결하기

macOS에서는 기기가 USB Tethering Mode인 경우 USB를 통해 Android 기기에서 실행 중인 개발용 앱에 연결할 수 있습니다. macOS에서는 [HoRNDIS](https://joshuawise.com/horndis#available_versions) 같은 타사 드라이버를 설치해야 합니다. HoRNDIS가 설치되면 Security & Privacy 설정에서 실행을 허용해야 합니다. USB Tethering이 활성화되면 개발용 앱이 실행 중일 때 기기가 <kbd>Project ▸ Targets</kbd> 아래에 표시됩니다.

### Windows 또는 Linux에서 USB를 사용해 Android 기기에 연결하기

Windows와 Linux에서는 기기가 USB Tethering Mode인 경우 USB를 통해 Android 기기에서 실행 중인 개발용 앱에 연결할 수 있습니다. USB Tethering이 활성화되면 개발용 앱이 실행 중일 때 기기가 <kbd>Project ▸ Targets</kbd> 아래에 표시됩니다.

## 문제 해결

Unable to download application
: 앱 서명에 사용된 mobile provisioning에 기기의 UDID가 포함되어 있는지 확인하세요.

기기가 Targets 메뉴에 표시되지 않음
: 기기가 컴퓨터와 같은 wifi 네트워크에 연결되어 있는지 확인하세요. 개발용 앱이 Debug 모드로 빌드되었는지 확인하세요.

버전 불일치에 대한 메세지와 함께 게임이 시작되지 않음
: 에디터를 최신 버전으로 업그레이드했을 때 발생합니다. 새 버전을 빌드하고 설치해야 합니다.
