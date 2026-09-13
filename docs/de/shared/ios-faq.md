#### Q: Ich kann mein Defold-Spiel mit einem kostenlosen Konto bei Apple Developer nicht installieren. {#q-i-am-unable-to-install-my-defold-game-using-a-free-apple-developer-account}
A: Stelle sicher, dass die Bundle-ID in deinem Defold-Projekt mit der Bundle-ID übereinstimmt, die du im Xcode-Projekt beim Erstellen des mobilen Bereitstellungsprofils verwendet hast.

#### Q: Wie kann ich die Berechtigungen einer als Bundle erstellten Anwendung prüfen? {#q-how-can-i-check-the-entitlements-of-a-bundled-application}
A: Aus [Berechtigungen einer erstellten App prüfen](https://developer.apple.com/library/archive/technotes/tn2415/_index.html#//apple_ref/doc/uid/DTS40016427-CH1-APPENTITLEMENTS):

```sh
codesign -d --ent :- /path/to/the.app
```

#### Q: Wie kann ich die Berechtigungen eines Bereitstellungsprofils prüfen {#q-how-can-i-check-the-entitlements-of-a-provisioning-profile}
A: Aus [Berechtigungen eines Profils prüfen](https://developer.apple.com/library/archive/technotes/tn2415/_index.html#//apple_ref/doc/uid/DTS40016427-CH1-PROFILESENTITLEMENTS):

```sh
security cms -D -i /path/to/iOSTeamProfile.mobileprovision
```