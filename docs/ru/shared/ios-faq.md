#### Q: Я не могу установить свою игру Defold, используя бесплатную учётную запись Apple Developer.
A: Убедитесь, что в вашем проекте Defold используется тот же bundle identifier, что и в проекте Xcode, когда вы генерировали mobile provisioning profile.

#### Q: Как проверить entitlements у собранного приложения?
A: Из [Inspect the entitlements of a built app](https://developer.apple.com/library/archive/technotes/tn2415/_index.html#//apple_ref/doc/uid/DTS40016427-CH1-APPENTITLEMENTS):

```sh
codesign -d --ent :- /path/to/the.app
```

#### Q: Как проверить entitlements у provisioning profile
A: Из [Inspecting a profile's entitlements](https://developer.apple.com/library/archive/technotes/tn2415/_index.html#//apple_ref/doc/uid/DTS40016427-CH1-PROFILESENTITLEMENTS):

```sh
security cms -D -i /path/to/iOSTeamProfile.mobileprovision
```
