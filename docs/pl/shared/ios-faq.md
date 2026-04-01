#### P: Nie mogę zainstalować mojej gry Defold, korzystając z darmowego konta Apple Developer.
O: Upewnij się, że w projekcie Defold używasz tego samego identyfikatora bundla, którego użyłeś w projekcie Xcode podczas generowania profilu provisioning dla urządzeń mobilnych.

#### P: Jak mogę sprawdzić uprawnienia zbudowanej aplikacji?
O: Zobacz [Sprawdzanie uprawnień zbudowanej aplikacji](https://developer.apple.com/library/archive/technotes/tn2415/_index.html#//apple_ref/doc/uid/DTS40016427-CH1-APPENTITLEMENTS):

```sh
codesign -d --ent :- /path/to/the.app
```

#### P: Jak mogę sprawdzić uprawnienia profilu provisioning?
O: Zobacz [Sprawdzanie uprawnień profilu provisioning](https://developer.apple.com/library/archive/technotes/tn2415/_index.html#//apple_ref/doc/uid/DTS40016427-CH1-PROFILESENTITLEMENTS):

```sh
security cms -D -i /path/to/iOSTeamProfile.mobileprovision
```
