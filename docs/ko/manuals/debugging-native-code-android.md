---
title: Android에서 디버깅하기
brief: 이 매뉴얼은 Android Studio를 사용해 빌드를 디버깅하는 방법을 설명합니다.
---

# Android에서 디버깅하기

여기서는 Google의 Android 운영체제용 공식 IDE인 [Android Studio](https://developer.android.com/studio/)를 사용해 빌드를 디버깅하는 방법을 설명합니다.


## Android Studio

* *game.project*에서 `android.debuggable` 옵션을 설정해 번들을 준비합니다.

	![android.debuggable](images/extensions/debugging/android/game_project_debuggable.png)

* 앱을 디버그 모드로 원하는 폴더에 번들링합니다.

	![bundle_android](images/extensions/debugging/android/bundle_android.png)

* [Android Studio](https://developer.android.com/studio/)를 실행합니다.

* `Profile or debug APK`를 선택합니다.

	![debug_apk](images/extensions/debugging/android/android_profile_or_debug.png)

* 방금 만든 apk 번들을 선택합니다.

	![select_apk](images/extensions/debugging/android/android_select_apk.png)

* 메인 `.so` 파일을 선택하고 debug symbols가 있는지 확인합니다.

	![select_so](images/extensions/debugging/android/android_missing_symbols.png)

* debug symbols가 없다면 unstripped `.so` 파일을 업로드합니다. (크기는 약 20mb입니다)

* Path mappings는 실행 파일이 빌드된 위치(클라우드)의 개별 경로를 로컬 드라이브의 실제 폴더로 다시 매핑하는 데 도움이 됩니다.

* .so 파일을 선택한 다음 로컬 드라이브에 대한 매핑을 추가합니다.

	![path_mapping1](images/extensions/debugging/android/path_mappings_android.png)

	![path_mapping2](images/extensions/debugging/android/path_mappings_android2.png)

* 엔진 소스에 액세스할 수 있다면 그 소스에도 path mapping을 추가합니다.

* 현재 디버깅 중인 버전을 checkout했는지 확인합니다.

	defold$ git checkout 1.2.148

* `Apply changes`를 누릅니다.

* 이제 프로젝트에 매핑된 소스가 표시됩니다.

	![source](images/extensions/debugging/android/source_mappings_android.png)

* breakpoint를 추가합니다.

	![breakpoint](images/extensions/debugging/android/breakpoint_android.png)

* `Run` -> `Debug "Appname"`를 누르고 중단하려는 코드를 호출합니다.

	![breakpoint](images/extensions/debugging/android/callstack_variables_android.png)

* 이제 callstack을 단계별로 실행하고 변수를 검사할 수 있습니다.


## 참고

### 네이티브 익스텐션 job 폴더

현재 개발용 워크플로우는 조금 번거롭습니다. job 폴더 이름이 빌드마다
무작위로 정해져 각 빌드에서 path mapping이 유효하지 않게 되기 때문입니다.

하지만 디버깅 세션에서는 문제없이 작동합니다.

Path mappings는 Android Studio 프로젝트의 프로젝트 `.iml` 파일에 저장됩니다.

실행 파일에서 job 폴더를 가져올 수 있습니다.

```sh
$ arm-linux-androideabi-readelf --string-dump=.debug_str build/armv7-android/libdmengine.so | grep /job
```

jobfolder 이름은 `job1298751322870374150`처럼 지정되며, 매번 무작위 숫자가 붙습니다.
