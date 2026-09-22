#### D: Non riesco a installare il mio gioco Defold usando un account Apple Developer gratuito. {#q-i-am-unable-to-install-my-defold-game-using-a-free-apple-developer-account}
R: Assicurati di usare nel progetto Defold lo stesso identificatore del bundle che hai usato nel progetto Xcode quando hai generato il profilo di provisioning mobile.

#### D: Come posso controllare le autorizzazioni (entitlement) di un'applicazione di cui è stato creato il bundle? {#q-how-can-i-check-the-entitlements-of-a-bundled-application}
R: Da [Controllare le autorizzazioni di un'app compilata](https://developer.apple.com/library/archive/technotes/tn2415/_index.html#//apple_ref/doc/uid/DTS40016427-CH1-APPENTITLEMENTS):

```sh
codesign -d --ent :- /path/to/the.app
```

#### D: Come posso controllare le autorizzazioni di un profilo di provisioning {#q-how-can-i-check-the-entitlements-of-a-provisioning-profile}
R: Da [Controllare le autorizzazioni di un profilo](https://developer.apple.com/library/archive/technotes/tn2415/_index.html#//apple_ref/doc/uid/DTS40016427-CH1-PROFILESENTITLEMENTS):

```sh
security cms -D -i /path/to/iOSTeamProfile.mobileprovision
```