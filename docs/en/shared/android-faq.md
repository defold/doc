#### Q: Is it possible to hide the navigation and status bars on Android?
A: Yes, set the *immersive_mode* setting in the *Android* section of your *game.project* file. This lets your app take over the whole screen and capture all touch events on the screen.


#### Q: Why am I'm getting "Failure [INSTALL_PARSE_FAILED_INCONSISTENT_CERTIFICATES]" when installing a Defold game on device?
A: Android detects that you try to install the app with a new certificate. When bundling debug builds, each build will be signed with a temporary certificate. Uninstall the old app before installing the new version:

```
$ adb uninstall com.defold.examples
Success
$ adb install Defold\ examples.apk
4826 KB/s (18774344 bytes in 3.798s)
      pkg: /data/local/tmp/Defold examples.apk
Success
```


#### Q: Why am I getting errors about conflicting properties in AndroidManifest.xml when building with certain extensions?
A: This can happen when two or more extensions provide an Android Manifest stub containing the same property tag but with different values. This has for instance happened with Firebase and AdMob. The build error looks similar to this:

```
SEVERE: /tmp/job4531953598647135356/upload/AndroidManifest.xml:32:13-58 Error: Attribute property#android.adservices.AD_SERVICES_CONFIG@resource value=(@xml/ga_ad_services_config) from AndroidManifest.xml:32:13-58 is also present at AndroidManifest.xml:92:13-59 value=(@xml/gma_ad_services_config). Suggestion: add 'tools:replace="android:resource"' to <property> element at AndroidManifest.xml to override. 
```

You can read more about the issue and the workaround in reported Defold issue [#9453](https://github.com/defold/defold/issues/9453#issuecomment-2367367269) and Google issue [#327696048](https://issuetracker.google.com/issues/327696048?pli=1).