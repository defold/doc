---
title: 原生扩展 - Manifest 混合工具
brief: 本教程介绍了应用的 manifests 混合是如何工作的
---

# Application manifests

一些平台上需要提供 manifests 片段 (或称存根) 来为扩展提供支持.
可以是部分 `AndroidManifest.xml`, `Info.plist` 或者 `engine_template.html`

从应用基础 manifest 开始, 每个扩展 manifest 存根一个一个的被应用.
基础 manifest 可以是默认的 (位于 `builtins\manifests\<platforms>\...`), 也可以是由用户自定义的.

## 命名和结构

扩展 manifests 必须被放置在适当的指定位置才能生效.

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

Android 平台提供了 manifest 混合工具 (基于 `ManifestMerger2`), `bob.jar` 中使用此工具混合 Manifest.
关于 Android manifests 的详细信息, 参见 [官方文档](https://developer.android.com/studio/build/manifest-merge)

::: sidenote
如果扩展 manifest 中没有设置应用的 `android:targetSdkVersion` , 下列权限会被自动加入:  `WRITE_EXTERNAL_STORAGE`, `READ_PHONE_STATE`, `READ_EXTERNAL_STORAGE`. 详情请见 [此文档](https://developer.android.com/studio/build/manifest-merge#implicit_system_permissions).
我们推荐这么设置: `<uses-sdk android:targetSdkVersion=“{{android.target_sdk_version}}” />`
:::
### 示例

基础 manifest

```xml
    <?xml version='1.0' encoding='utf-8'?>
    <manifest xmlns:android='http://schemas.android.com/apk/res/android'
            package='com.defold.testmerge'
            android:versionCode='14'
            android:versionName='1.0'
            android:installLocation='auto'>
        <uses-feature android:required='true' android:glEsVersion='0x00020000' />
        <uses-sdk android:minSdkVersion='9' android:targetSdkVersion='26' />
        <application android:label='Test Project' android:hasCode='true'>
        </application>
        <uses-permission android:name='android.permission.VIBRATE' />
    </manifest>
```

扩展 manifest:

```xml
    <?xml version='1.0' encoding='utf-8'?>
    <manifest xmlns:android='http://schemas.android.com/apk/res/android' package='com.defold.testmerge'>
         <uses-sdk android:targetSdkVersion=“{{android.target_sdk_version}}” />
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

混合结果

```xml
    <?xml version='1.0' encoding='utf-8'?>
    <manifest xmlns:android='http://schemas.android.com/apk/res/android'
        package='com.defold.testmerge'
        android:installLocation='auto'
        android:versionCode='14'
        android:versionName='1.0' >
        <uses-sdk
            android:minSdkVersion='9'
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

对于 `Info.plist` 我们实现了专用的工具混合列表和字典. 可以在键上指定混合属性 `merge`, `keep` 或 `replace`, 默认是 `merge`.

### 示例

基础 Manifest

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

        <!-- 即使扩展清单里有这个键也要保持该键 -->
        <key merge='keep'>BASE64</key>
        <data>SEVMTE8gV09STEQ=</data>

        <!-- 如果扩展清单里也有这个键的数组那么所有字典值会与基本数组第一个字典值合并 -->
        <key>Array1</key>
        <array>
            <dict>
                <key>Foobar</key>
                <array>
                    <string>a</string>
                </array>
            </dict>
        </array>

        <!-- 不要试图合并这个数组的值, 而应该把扩展清单的值添加到这个数组里去 -->
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

扩展 manifest:

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

        <!-- 改写基础清单里已存在的值 -->
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

混合结果:

```xml
    <?xml version='1.0'?>
    <!DOCTYPE plist SYSTEM 'file://localhost/System/Library/DTDs/PropertyList.dtd'>
    <plist version='1.0'>
        <!-- 嵌套合并基础清单和扩展清单的字典 -->
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

            <!-- 来自基础清单 -->
            <key>INT</key>
            <integer>8</integer>

            <!-- 基础清单的值被改写因为扩展清单的合并标志是 "replace" -->
            <key>REAL</key>
            <real>16.0</real>

            <!-- 基础清单的值被使用因为基础清单的合并标志是 "keep" -->
            <key>BASE64</key>
            <data>SEVMTE8gV09STEQ=</data>

            <!-- 扩展清单的值被加入进来因为没有指定合并标志 -->
            <key>INT</key>
            <integer>42</integer>

            <!-- 数组的字典值被合并因为基础清单默认合并标志是 "merge" -->
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

            <!-- 字典值被加入到数组因为基础清单使用了 "keep" -->
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

对于 html 模板, 我们给各部分命名, 以便混合时相匹配 (比如 "engine-start").
标签属性可以是 `merge` 或者 `keep`. `merge` 是默认值.

### 示例

基础 manifest

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

扩展 manifest

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

混合结果

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
            my_load_engine();
        </script>
    </body>
    </html>
```
