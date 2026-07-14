---
title: 네이티브 익스텐션 - 메니페스트 병합 도구
brief: 이 매뉴얼은 어플리케이션 메니페스트 병합이 어떻게 동작하는지 설명합니다
---

# 어플리케이션 메니페스트

일부 플랫폼에서는 어플리케이션 메니페스트 조각(또는 스텁)을 제공하는 익스텐션을 지원합니다.
이는 `AndroidManifest.xml`, `Info.plist` 또는 `engine_template.html`의 일부일 수 있습니다.

각 익스텐션 메니페스트 스텁은 어플리케이션 기본 메니페스트부터 시작해 하나씩 차례로 적용됩니다.
기본 메니페스트는 기본 제공 메니페스트(`builtins\manifests\<platforms>\...`)이거나 사용자가 제공한 커스텀 메니페스트입니다.

## 이름 지정과 구조

익스텐션이 의도한 대로 동작하려면 익스텐션 메니페스트를 특정 구조에 배치해야 합니다.

    /myextension
        ext.manifest
        /manifests
            /android
                AndroidManifest.xml
            /ios
                Info.plist
            /osx
                Info.plist
            /web
                engine_template.html


## Android

Android 플랫폼에는 이미 `ManifestMerger2` 기반의 메니페스트 병합 도구가 있으며, Defold는 `bob.jar` 안에서 이 도구를 사용해 메니페스트를 병합합니다.
Android 메니페스트를 수정하는 방법에 대한 전체 지침은 [해당 문서](https://developer.android.com/studio/build/manifest-merge)를 참고하세요.

::: important
익스텐션 메니페스트에서 앱의 `android:targetSdkVersion`을 설정하지 않으면 다음 권한이 자동으로 추가됩니다:  `WRITE_EXTERNAL_STORAGE`, `READ_PHONE_STATE`, `READ_EXTERNAL_STORAGE`. 이에 대한 자세한 내용은 공식 문서 [여기](https://developer.android.com/studio/build/manifest-merge#implicit_system_permissions)에서 읽을 수 있습니다.
다음 사용을 권장합니다: `<uses-sdk android:targetSdkVersion="{{android.target_sdk_version}}" />`
:::
### 예제

기본 메니페스트

```xml
    <?xml version='1.0' encoding='utf-8'?>
    <manifest xmlns:android='http://schemas.android.com/apk/res/android'
            package='com.defold.testmerge'
            android:versionCode='14'
            android:versionName='1.0'
            android:installLocation='auto'>
        <uses-feature android:required='true' android:glEsVersion='0x00020000' />
        <uses-sdk android:minSdkVersion='21' android:targetSdkVersion='26' />
        <application android:label='Test Project' android:hasCode='true'>
        </application>
        <uses-permission android:name='android.permission.VIBRATE' />
    </manifest>
```

익스텐션 메니페스트:

```xml
    <?xml version='1.0' encoding='utf-8'?>
    <manifest xmlns:android='http://schemas.android.com/apk/res/android' package='com.defold.testmerge'>
         <uses-sdk android:targetSdkVersion="{{android.target_sdk_version}}" />
        <uses-feature android:required='true' android:glEsVersion='0x00030000' />
        <application>
            <meta-data android:name='com.facebook.sdk.ApplicationName'
                android:value='Test Project' />
            <activity android:name='com.facebook.FacebookActivity'
              android:theme='@android:style/Theme.Translucent.NoTitleBar'
              android:configChanges='keyboard|keyboardHidden|screenLayout|screenSize|orientation'
              android:label='Test Project' />
        </application>
    </manifest>
```

결과

```xml
    <?xml version='1.0' encoding='utf-8'?>
    <manifest xmlns:android='http://schemas.android.com/apk/res/android'
        package='com.defold.testmerge'
        android:installLocation='auto'
        android:versionCode='14'
        android:versionName='1.0' >
        <uses-sdk
            android:minSdkVersion='21'
            android:targetSdkVersion='26' />
        <uses-permission android:name='android.permission.VIBRATE' />
        <uses-feature
            android:glEsVersion='0x00030000'
            android:required='true' />
        <application
            android:hasCode='true'
            android:label='Test Project' >
            <meta-data
                android:name='com.facebook.sdk.ApplicationName'
                android:value='Test Project' />
            <activity
                android:name='com.facebook.FacebookActivity'
                android:configChanges='keyboard|keyboardHidden|screenLayout|screenSize|orientation'
                android:label='Test Project'
                android:theme='@android:style/Theme.Translucent.NoTitleBar' />
        </application>
    </manifest>
```

## iOS / macOS

`Info.plist`의 경우 목록과 딕셔너리를 병합하기 위해 Defold 자체 구현을 사용합니다. 키에 병합 마커 속성 `merge`, `keep` 또는 `replace`를 지정할 수 있으며, 기본값은 `merge`입니다.

### 예제

기본 메니페스트

```xml
    <?xml version='1.0' encoding='UTF-8'?>
    <!DOCTYPE plist PUBLIC '-//Apple//DTD PLIST 1.0//EN' 'http://www.apple.com/DTDs/PropertyList-1.0.dtd'>
    <plist version='1.0'>
    <dict>
        <key>NSAppTransportSecurity</key>
        <dict>
            <key>NSExceptionDomains</key>
            <dict>
                <key>foobar.net</key>
                <dict>
                    <key>testproperty</key>
                    <true/>
                </dict>
            </dict>
        </dict>
        <key>INT</key>
        <integer>8</integer>

        <key>REAL</key>
        <real>8.0</real>

        <!-- 익스텐션 메니페스트에 같은 키가 포함되어 있더라도 이 값을 유지합니다 -->
        <key merge='keep'>BASE64</key>
        <data>SEVMTE8gV09STEQ=</data>

        <!-- 익스텐션 메니페스트에도 이 키를 가진 배열이 있으면, 모든 딕셔너리 값이 기본 배열의 첫 번째 딕셔너리 값과 병합됩니다 -->
        <key>Array1</key>
        <array>
            <dict>
                <key>Foobar</key>
                <array>
                    <string>a</string>
                </array>
            </dict>
        </array>

        <!-- 이 배열의 값을 병합하려고 시도하지 않고, 대신 익스텐션 메니페스트의 값을 배열 끝에 추가해야 합니다 -->
        <key merge='keep'>Array2</key>
        <array>
            <dict>
                <key>Foobar</key>
                <array>
                    <string>a</string>
                </array>
            </dict>
        </array>
    </dict>
    </plist>
```

익스텐션 메니페스트:

```xml
    <?xml version='1.0' encoding='UTF-8'?>
    <!DOCTYPE plist PUBLIC '-//Apple//DTD PLIST 1.0//EN' 'http://www.apple.com/DTDs/PropertyList-1.0.dtd'>
    <plist version='1.0'>
    <dict>
        <key>NSAppTransportSecurity</key>
        <dict>
            <key>NSExceptionDomains</key>
            <dict>
                <key>facebook.com</key>
                <dict>
                    <key>NSIncludesSubdomains</key>
                    <true/>
                    <key>NSThirdPartyExceptionRequiresForwardSecrecy</key>
                    <false/>
                </dict>
            </dict>
        </dict>
        <key>INT</key>
        <integer>42</integer>

        <!-- 기본 메니페스트의 기존 값을 대체합니다 -->
        <key merge='replace'>REAL</key>
        <integer>16.0</integer>

        <key>BASE64</key>
        <data>Rk9PQkFS</data>

        <key>Array1</key>
        <array>
            <dict>
                <key>Foobar</key>
                <array>
                    <string>b</string>
                </array>
            </dict>
        </array>

        <key>Array2</key>
        <array>
            <dict>
                <key>Foobar</key>
                <array>
                    <string>b</string>
                </array>
            </dict>
        </array>
    </dict>
    </plist>
```

결과:

```xml
    <?xml version='1.0'?>
    <!DOCTYPE plist SYSTEM 'file://localhost/System/Library/DTDs/PropertyList.dtd'>
    <plist version='1.0'>
        <!-- 기본 메니페스트와 익스텐션 메니페스트의 딕셔너리를 중첩 병합합니다 -->
        <dict>
            <key>NSAppTransportSecurity</key>
            <dict>
                <key>NSExceptionDomains</key>
                <dict>
                    <key>foobar.net</key>
                    <dict>
                        <key>testproperty</key>
                        <true/>
                    </dict>
                    <key>facebook.com</key>
                    <dict>
                        <key>NSIncludesSubdomains</key>
                        <true/>
                        <key>NSThirdPartyExceptionRequiresForwardSecrecy</key>
                        <false/>
                    </dict>
                </dict>
            </dict>

            <!-- 기본 메니페스트에서 온 값입니다 -->
            <key>INT</key>
            <integer>8</integer>

            <!-- 익스텐션 메니페스트에서 병합 마커가 "replace"로 설정되어 기본 메니페스트의 값이 대체되었습니다 -->
            <key>REAL</key>
            <real>16.0</real>

            <!-- 기본 메니페스트에서 병합 마커가 "keep"으로 설정되어 기본 메니페스트의 값이 사용되었습니다 -->
            <key>BASE64</key>
            <data>SEVMTE8gV09STEQ=</data>

            <!-- 병합 마커가 지정되지 않았으므로 익스텐션 메니페스트의 값이 추가되었습니다 -->
            <key>INT</key>
            <integer>42</integer>

            <!-- 기본 메니페스트의 기본값이 "merge"이므로 배열의 딕셔너리 값이 병합되었습니다 -->
            <key>Array1</key>
            <array>
                <dict>
                    <key>Foobar</key>
                    <array>
                        <string>a</string>
                        <string>b</string>
                    </array>
                </dict>
            </array>

            <!-- 기본 메니페스트가 "keep"을 사용했으므로 딕셔너리 값이 배열에 추가되었습니다 -->
            <key>Array2</key>
            <array>
                <dict>
                    <key>Foobar</key>
                    <array>
                        <string>a</string>
                    </array>
                </dict>
                <dict>
                    <key>Foobar</key>
                    <array>
                        <string>b</string>
                    </array>
                </dict>
            </array>
        </dict>
    </plist>
```


## HTML5

html 템플릿의 경우 각 섹션에 이름을 붙여 서로 매칭할 수 있게 했습니다(예: "engine-start").
그런 다음 `merge` 또는 `keep` 속성을 지정할 수 있습니다. `merge`가 기본값입니다.

### 예제

기본 메니페스트

```html
    <!DOCTYPE html>
    <html>
    <body>
     <script id='engine-loader' type='text/javascript' src='dmloader.js'></script>
     <script id='engine-setup' type='text/javascript'>
     function load_engine() {
         var engineJS = document.createElement('script');
         engineJS.type = 'text/javascript';
         engineJS.src = '{{exe-name}}_wasm.js';
         document.head.appendChild(engineJS);
     }
     </script>
     <script id='engine-start' type='text/javascript'>
         load_engine();
     </script>
    </body>
    </html>
```

익스텐션 메니페스트

```html
    <html>
    <body>
     <script id='engine-loader' type='text/javascript' src='mydmloader.js'></script>
     <script id='engine-start' type='text/javascript' merge='keep'>
         my_load_engine();
     </script>
    </body>
    </html>
```

결과

```html
    <!doctype html>
    <html>
    <head></head>
    <body>
        <script id='engine-loader' type='text/javascript' src='mydmloader.js'></script>
        <script id='engine-setup' type='text/javascript'>
            function load_engine() {
                var engineJSdocument.createElement('script');
                engineJS.type = 'text/javascript';
                engineJS.src = '{{exe-name}}_wasm.js';
                document.head.appendChild(engineJS);
            }
        </script>
        <script id='engine-start' type='text/javascript' merge='keep'>
            my_load_engine(
        </script>
    </body>
    </html>
```
