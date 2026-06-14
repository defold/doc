---
title: iOS/macOS에서 디버깅하기
brief: 이 매뉴얼은 Xcode를 사용해 빌드를 디버깅하는 방법을 설명합니다.
---

# iOS/macOS에서 디버깅하기

여기서는 Apple이 macOS와 iOS 개발에 권장하는 IDE인 [Xcode](https://developer.apple.com/xcode/)를 사용해 빌드를 디버깅하는 방법을 설명합니다.

## Xcode

* `--with-symbols` 옵션을 사용해 bob으로 앱을 번들링합니다([자세한 정보](/manuals/debugging-native-code/#symbolicate-a-callstack)).

```sh
$ cd myproject
$ wget http://d.defold.com/archive/<sha1>/bob/bob.jar
$ java -jar bob.jar --platform armv7-darwin build --with-symbols --variant debug --archive bundle -bo build/ios -mp <app>.mobileprovision --identity "iPhone Developer: Your Name (ID)"
```

* `Xcode`, `iTunes` 또는 [ios-deploy](https://github.com/ios-control/ios-deploy)로 앱을 설치합니다.

```sh
$ ios-deploy -b <AppName>.ipa
```

* `.dSYM` 폴더(debug symbols)를 가져옵니다.

	* 네이티브 익스텐션을 사용하지 않는다면 [d.defold.com](http://d.defold.com)에서 `.dSYM` 파일을 다운로드할 수 있습니다.

	* 네이티브 익스텐션을 사용한다면 [bob.jar](https://www.defold.com/manuals/bob/)로 빌드할 때 `.dSYM` 폴더가 생성됩니다. 빌드만 필요합니다(아카이브나 번들링은 필요하지 않음).

```sh
$ cd myproject
$ unzip .internal/cache/arm64-ios/build.zip
$ mv dmengine.dSYM <AppName>.dSYM
$ mv <AppName>.dSYM/Contents/Resources/DWARF/dmengine <AppName>.dSYM/Contents/Resources/DWARF/<AppName>
```

### 프로젝트 만들기

제대로 디버깅하려면 프로젝트가 필요하며, 소스 코드도 매핑되어 있어야 합니다.
이 프로젝트는 빌드용이 아니라 디버그용으로만 사용합니다.

* 새 Xcode 프로젝트를 만들고 `Game` 템플릿을 선택합니다.

	![project_template](images/extensions/debugging/ios/project_template.png)

* 이름(예: `debug`)과 기본 설정을 선택합니다.

* 프로젝트를 저장할 폴더를 선택합니다.

* 앱에 코드를 추가합니다.

	![add_files](images/extensions/debugging/ios/add_files.png)

* "Copy items if needed"가 체크 해제되어 있는지 확인합니다.

	![add_source](images/extensions/debugging/ios/add_source.png)

* 최종 결과는 다음과 같습니다.

	![added_source](images/extensions/debugging/ios/added_source.png)


* `Build` 단계를 비활성화합니다.

	![edit_scheme](images/extensions/debugging/ios/edit_scheme.png)

	![disable_build](images/extensions/debugging/ios/disable_build.png)

* `Deployment target` 버전을 기기의 iOS 버전보다 크게 설정합니다.

	![deployment_version](images/extensions/debugging/ios/deployment_version.png)

* 타겟 기기를 선택합니다.

	![select_device](images/extensions/debugging/ios/select_device.png)


### 디버거 실행

앱을 디버깅하는 방법은 몇 가지가 있습니다.

1. `Debug` -> `Attach to process...`를 선택하고 거기서 앱을 선택합니다.

2. 또는 `Attach to process by PID or Process name`을 선택합니다.

	![select_device](images/extensions/debugging/ios/attach_to_process_name.png)

3. 기기에서 앱을 시작합니다.

4. `Edit Scheme`에서 <AppName>.app 폴더를 실행 파일로 추가합니다.

### 디버그 심볼

**lldb를 사용하려면 실행이 일시 중지되어 있어야 합니다**

* `.dSYM` 경로를 lldb에 추가합니다.

```
(lldb) add-dsym <PathTo.dSYM>
```

	![add_dsym](images/extensions/debugging/ios/add_dsym.png)

* `lldb`가 심볼을 성공적으로 읽었는지 확인합니다.

```
(lldb) image list <AppName>
```

### 경로 매핑

* 엔진 소스를 추가합니다(필요에 맞게 변경).

```
(lldb) settings set target.source-map /Users/builder/ci/builds/engine-ios-64-master/build /Users/mathiaswesterdahl/work/defold
(lldb) settings append target.source-map /private/var/folders/m5/bcw7ykhd6vq9lwjzq1mkp8j00000gn/T/job4836347589046353012/upload/videoplayer/src /Users/mathiaswesterdahl/work/projects/extension-videoplayer-native/videoplayer/src
```

* 실행 파일에서 job 폴더를 가져올 수 있습니다. jobfolder 이름은 `job1298751322870374150`처럼 지정되며, 매번 무작위 숫자가 붙습니다.

```sh
$ dsymutil -dump-debug-map <executable> 2>&1 >/dev/null | grep /job

```

* 소스 매핑을 확인합니다.

```
(lldb) settings show target.source-map
```

심볼이 어떤 소스 파일에서 왔는지는 다음 명령으로 확인할 수 있습니다.

```
(lldb) image lookup -va <SymbolName>
```

### 중단점

* 프로젝트 뷰에서 파일을 열고 중단점을 설정합니다.

	![breakpoint](images/extensions/debugging/ios/breakpoint.png)

## 참고

### 바이너리의 UUID 확인

디버거가 `.dSYM` 폴더를 받아들이려면 UUID가 디버깅 중인 실행 파일의 UUID와 일치해야 합니다. UUID는 다음과 같이 확인할 수 있습니다.

```sh
$ dwarfdump -u <PathToBinary>
```
