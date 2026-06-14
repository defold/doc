#### Q: Android에서 navigation bar와 status bar를 숨길 수 있나요?
A: 예, *game.project* 파일의 *Android* 섹션에서 *immersive_mode* 설정값을 설정하세요. 이렇게 하면 앱이 전체 화면을 사용하고 화면의 모든 터치 이벤트를 캡처할 수 있습니다.


#### Q: Defold 게임을 기기에 설치할 때 "Failure [INSTALL_PARSE_FAILED_INCONSISTENT_CERTIFICATES]"가 표시되는 이유는 무엇인가요?
A: Android는 새 인증서로 앱을 설치하려고 하는 것을 감지합니다. 디버그 빌드를 번들링할 때는 각 빌드가 임시 인증서로 서명됩니다. 새 버전을 설치하기 전에 이전 앱을 제거하세요:

```
$ adb uninstall com.defold.examples
Success
$ adb install Defold\ examples.apk
4826 KB/s (18774344 bytes in 3.798s)
      pkg: /data/local/tmp/Defold examples.apk
Success
```


#### Q: 특정 익스텐션으로 빌드할 때 AndroidManifest.xml에서 충돌하는 프로퍼티에 대한 오류가 표시되는 이유는 무엇인가요?
A: 두 개 이상의 익스텐션이 같은 프로퍼티 태그를 포함하지만 서로 다른 값을 가진 Android Manifest stub을 제공할 때 발생할 수 있습니다. 예를 들어 Firebase와 AdMob에서 이런 일이 발생한 적이 있습니다. 빌드 오류는 다음과 비슷합니다:

```
SEVERE: /tmp/job4531953598647135356/upload/AndroidManifest.xml:32:13-58
Error: Attribute property#android.adservices.AD_SERVICES_CONFIG@resource
value=(@xml/ga_ad_services_config) from AndroidManifest.xml:32:13-58 is also
present at AndroidManifest.xml:92:13-59 value=(@xml/gma_ad_services_config).
Suggestion: add 'tools:replace="android:resource"' to <property> element at
AndroidManifest.xml to override.
```

이 문제와 우회 방법에 대한 자세한 내용은 보고된 Defold 이슈 [#9453](https://github.com/defold/defold/issues/9453#issuecomment-2367367269)와 Google 이슈 [#327696048](https://issuetracker.google.com/issues/327696048?pli=1)에서 읽을 수 있습니다.
