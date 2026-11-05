#### Q: Soy incapaz de instalar mi juego Defold utilizando una cuenta gratuita de Apple Developer.
A: Asegúrate de que utilizas el mismo identificador de bundle en tu proyecto Defold así como el que usaste en el proyecto Xcode cuando generaste el perfil provisional del móvil.

#### Q: ¿cómo puedo verificar los derechos de una aplicación empaquetada??
A: Desde [Inspect the entitlements of a built app](https://developer.apple.com/library/archive/technotes/tn2415/_index.html#//apple_ref/doc/uid/DTS40016427-CH1-APPENTITLEMENTS):

```sh
codesign -d --ent :- /path/to/the.app
```

#### Q: ¿Cómo puedo verificar los derechos de un perfil provisional?
A: Desde [Inspecting a profile's entitlements](https://developer.apple.com/library/archive/technotes/tn2415/_index.html#//apple_ref/doc/uid/DTS40016427-CH1-PROFILESENTITLEMENTS):

```sh
security cms -D -i /path/to/iOSTeamProfile.mobileprovision
```