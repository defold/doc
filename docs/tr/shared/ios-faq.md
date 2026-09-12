#### Q: Ücretsiz bir Apple Developer hesabıyla Defold oyunumu kuramıyorum.
A: Defold projenizde, mobil sağlama profilini (provisioning profile) oluştururken Xcode projesinde kullandığınız paket tanımlayıcısının (bundle identifier) aynısını kullandığınızdan emin olun.

#### Q: Paketlenmiş bir uygulamanın yetkilerini (entitlements) nasıl kontrol edebilirim?
A: [Derlenmiş bir uygulamanın yetkilerini inceleme](https://developer.apple.com/library/archive/technotes/tn2415/_index.html#//apple_ref/doc/uid/DTS40016427-CH1-APPENTITLEMENTS) bölümünden:

```sh
codesign -d --ent :- /path/to/the.app
```

#### Q: Bir sağlama profilinin yetkilerini nasıl kontrol edebilirim
A: [Bir profilin yetkilerini inceleme](https://developer.apple.com/library/archive/technotes/tn2415/_index.html#//apple_ref/doc/uid/DTS40016427-CH1-PROFILESENTITLEMENTS) bölümünden:

```sh
security cms -D -i /path/to/iOSTeamProfile.mobileprovision
```