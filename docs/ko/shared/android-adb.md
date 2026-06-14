`adb` 커맨드 라인 도구는 Android 기기와 상호작용하는 데 사용하는, 사용하기 쉽고 다용도로 활용할 수 있는 프로그램입니다. Mac, Linux, Windows용 Android SDK Platform-Tools의 일부로 `adb`를 다운로드하고 설치할 수 있습니다.

Android SDK Platform-Tools는 https://developer.android.com/studio/releases/platform-tools 에서 다운로드하세요. *adb* 도구는 */platform-tools/* 안에 있습니다. 또는 플랫폼별 패키지를 각 패키지 매니저를 통해 설치할 수 있습니다.

Ubuntu Linux:

```
$ sudo apt-get install android-tools-adb
```

Fedora 18/19:

```
$ sudo yum install android-tools
```

macOS (Homebrew)

```
$ brew cask install android-platform-tools
```

Android 기기를 USB로 컴퓨터에 연결한 다음 다음 명령을 실행하여 `adb`가 작동하는지 확인할 수 있습니다.

```
$ adb devices
List of devices attached
31002535c90ef000    device
```

기기가 표시되지 않으면 Android 기기에서 *USB debugging*이 활성화되어 있는지 확인하세요. 기기의 *Settings*를 열고 *Developer options*(또는 *Development*)를 찾으세요.

![USB debugging 활성화](images/android/usb_debugging.png)
