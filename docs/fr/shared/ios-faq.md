#### Q : Je n'arrive pas à installer mon jeu Defold avec un compte Apple Developer gratuit. {#q-i-am-unable-to-install-my-defold-game-using-a-free-apple-developer-account}
R : Assurez-vous d'utiliser le même identifiant de bundle dans votre projet Defold que celui que vous avez utilisé dans le projet Xcode lors de la génération du profil de provisionnement mobile.

#### Q : Comment vérifier les droits d'une application générée sous forme de bundle ? {#q-how-can-i-check-the-entitlements-of-a-bundled-application}
R : D'après [Inspection des droits d'une application compilée](https://developer.apple.com/library/archive/technotes/tn2415/_index.html#//apple_ref/doc/uid/DTS40016427-CH1-APPENTITLEMENTS) :

```sh
codesign -d --ent :- /path/to/the.app
```

#### Q : Comment vérifier les droits d'un profil de provisionnement ? {#q-how-can-i-check-the-entitlements-of-a-provisioning-profile}
R : D'après [Inspection des droits d'un profil](https://developer.apple.com/library/archive/technotes/tn2415/_index.html#//apple_ref/doc/uid/DTS40016427-CH1-PROFILESENTITLEMENTS) :

```sh
security cms -D -i /path/to/iOSTeamProfile.mobileprovision
```