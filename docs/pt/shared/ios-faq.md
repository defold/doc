#### P: Não consigo instalar meu jogo Defold usando uma conta gratuita de Apple Developer.
R: Certifique-se de usar no seu projeto Defold o mesmo bundle identifier que você usou no projeto Xcode ao gerar o perfil de provisionamento móvel.

#### P: Como posso verificar os entitlements de uma aplicação empacotada?
R: De [Inspect the entitlements of a built app](https://developer.apple.com/library/archive/technotes/tn2415/_index.html#//apple_ref/doc/uid/DTS40016427-CH1-APPENTITLEMENTS):

```sh
codesign -d --ent :- /path/to/the.app
```

#### P: Como posso verificar os entitlements de um perfil de provisionamento?
R: De [Inspecting a profile's entitlements](https://developer.apple.com/library/archive/technotes/tn2415/_index.html#//apple_ref/doc/uid/DTS40016427-CH1-PROFILESENTITLEMENTS):

```sh
security cms -D -i /path/to/iOSTeamProfile.mobileprovision
```
