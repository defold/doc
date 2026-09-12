#### Q: Defold düzenleyicisi 4k veya HiDPI monitörde çalıştırıldığında neden çok küçük görünüyor?

A: GNOME kullanıyorsanız Defold'u çalıştırmadan önce ölçekleme katsayısını değiştirebilirsiniz. [kaynak](https://unix.stackexchange.com/a/552411)

```bash
$ gsettings set org.gnome.desktop.interface scaling-factor 2
$ ./Defold
```

A: Özellikle kesirli bir katsayıyla büyütmek istediğinizde kullanabileceğiniz alternatif bir çözüm, `Defold/config` dosyasını değiştirip `vmargs` satırına `glass.gtk.uiScale` eklemektir: [kaynak](https://forum.defold.com/t/4k-hidpi-monitor-support-solved/64108/12?u=britzl)

```
vmargs = -Dglass.gtk.uiScale=1.5,-Dfile.encoding=UTF-8,...
vmargs = -Dglass.gtk.uiScale=175%,-Dfile.encoding=UTF-8,...
vmargs = -Dglass.gtk.uiScale=192dpi,-Dfile.encoding=UTF-8,...
```

Bu değer hakkında daha fazla bilgi için [Arch Linux HiDPI wiki yazısına](https://wiki.archlinux.org/title/HiDPI#JavaFX) bakın.

A: KDE kullanıyorsanız `GDK_SCALE` değerini ayarlayabilirsiniz:

```bash
$ GDK_SCALE=2 ./Defold
```

#### Q: Elementary OS üzerinde fare tıklamaları neden düzenleyicinin içinden geçip altındaki öğelere ulaşıyor?

A: Düzenleyiciyi şu şekilde başlatın:

```bash
$ GTK_CSD=0 ./Defold
```


#### Q: Defold düzenleyicisi bir koleksiyon veya oyun nesnesi açarken çöküyor ve çökme iletisinde `com.jogamp.opengl` geçiyor

A: Bazı dağıtımlarda (Ubuntu 18 gibi), Defold'un kullandığı `jogamp`/`jogl` sürümü ile sistemdeki [Mesa](https://docs.mesa3d.org/) sürümü arasında bir sorun vardır. `MESA_GL_VERSION_OVERRIDE` değerini 2.1 veya daha yüksek, ancak sürücünüzün sürümünü aşmayan bir değere ayarlayarak `glGetString(GL_VERSION)` çağrıldığında bildirilen GL sürümünü değiştirebilirsiniz. Sürücünüzün desteklediği en yüksek OpenGL sürümünü `glxinfo` kullanarak kontrol edebilirsiniz:

```bash
glxinfo | grep version
```

Örnek çıktı ("OpenGL version string: x.y" satırını arayın):

```
server glx version string: 1.4
client glx version string: 1.4
GLX version: 1.4
Max core profile version: 4.6
Max compat profile version: 4.6
Max GLES1 profile version: 1.1
Max GLES[23] profile version: 3.2
OpenGL core profile version string: 4.6 (Core Profile) Mesa 20.2.6
OpenGL core profile shading language version string: 4.60
OpenGL version string: 4.6 (Compatibility Profile) Mesa 20.2.6
OpenGL shading language version string: 4.60
OpenGL ES profile version string: OpenGL ES 3.2 Mesa 20.2.6
OpenGL ES profile shading language version string: OpenGL ES GLSL ES 3.20
GL_EXT_shader_implicit_conversions, GL_EXT_shader_integer_mix,
```

2.1 sürümünü veya grafik sürücünüzle eşleşen sürümü kullanın:

```bash
$ MESA_GL_VERSION_OVERRIDE=2.1 ./Defold
```

```bash
$ MESA_GL_VERSION_OVERRIDE=4.6 ./Defold
```


#### Q: Defold'u başlatırken neden "`com.jogamp.opengl.GLException: Graphics configuration failed`" hatasını alıyorum?

A: Bazı dağıtımlarda (örneğin Ubuntu 20.04), Defold çalıştırılırken yeni [Mesa](https://docs.mesa3d.org/) sürücüleriyle (Iris) ilgili bir sorun yaşanır. Defold'u çalıştırırken daha eski bir sürücü sürümü kullanmayı deneyebilirsiniz:

```bash
$ MESA_LOADER_DRIVER_OVERRIDE=i965 ./Defold
```


#### Q: Defold düzenleyicisi bir koleksiyon veya oyun nesnesi açarken çöküyor ve çökme iletisinde `libffi.so` geçiyor

A: Dağıtımınızın [libffi](https://sourceware.org/libffi/) sürümü ile Defold'un gerektirdiği sürüm (6 veya 7) eşleşmiyor. `libffi.so.6` veya `libffi.so.7` dosyasının `/usr/lib/x86_64-linux-gnu` altında kurulu olduğundan emin olun. `libffi.so.7` dosyasını şu şekilde indirebilirsiniz:  

```bash
$ wget http://ftp.br.debian.org/debian/pool/main/libf/libffi/libffi7_3.3-6_amd64.deb
$ sudo dpkg -i libffi7_3.3-6_amd64.deb
```

Ardından Defold'u çalıştırırken bu sürümün yolunu `LD_PRELOAD` ortam değişkeninde belirtin:

```bash
$ LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libffi.so.7 ./Defold
```


#### Q: OpenGL sürücülerim güncelliğini yitirmiş. Defold kullanmaya devam edebilir miyim?

A: Evet, yazılımla işlemeyi (software rendering) etkinleştirirseniz Defold'u kullanmanız mümkün olabilir. `LIBGL_ALWAYS_SOFTWARE` ortam değişkenini 1 yaparak yazılımla işlemeyi etkinleştirebilirsiniz:

```bash
$ LIBGL_ALWAYS_SOFTWARE=1 ./Defold
```


#### Q: Linux'ta çalıştırmayı denediğimde Defold oyunum neden başlamıyor?

A: Düzenleyicideki konsol çıktısını kontrol edin. Şu iletiyi alıyorsanız:

```
dmengine: error while loading shared libraries: libopenal.so.1: cannot open shared object file: No such file or directory
```

*`libopenal1`* paketini kurmanız gerekir. Paket adı dağıtımlar arasında farklılık gösterir ve bazı durumlarda *`openal`* ile *`openal-dev`* veya *`openal-devel`* paketlerini kurmanız gerekebilir.

```bash
$ apt-get install libopenal-dev
```

#### Q: Üst menü neden bir şey seçemeden kapanıyor?

A: Bunun nedeni büyük olasılıkla kullanılan pencere yöneticisidir (örneğin `Qtile` veya i3). Bu, [JavaFX'te bilinen bir sorundur](https://bugs.openjdk.org/browse/JDK-8251240?focusedCommentId=14362084&page=com.atlassian.jira.plugin.system.issuetabpanels%3Acomment-tabpanel#comment-14362084) ve `GDK_DISPLAY` ortam değişkenini 1 yaparak çözülebilir:¨

```bash
$ GDK_DISPLAY=1 ./Defold

D=2

```

Veya `Defold/config` dosyasını değiştirip `vmargs` satırına `-Djdk.gtk.version=2` ekleyerek çözebilirsiniz:

```
vmargs = -Djdk.gtk.version=2,-Dfile.encoding=UTF-8,...
```


#### Q: Open From Disk seçeneğini seçtiğimde neden mevcut tüm dosya konumlarına göz atamıyorum?

A: Defold'u [Flatpak kullanan Steam üzerinden](https://flathub.org/apps/com.valvesoftware.Steam) çalıştırıyorsanız Steam'e diğer sürücülerinize erişme izni vermeniz gerekir. Flatpak uygulamalarınızın izinlerini [Flatseal](https://flathub.org/apps/com.github.tchx84.Flatseal) veya benzer bir araçla değiştirebilirsiniz.


#### Q: Web profil çıkarıcısını veya tarayıcı gerektiren diğer menü seçeneklerini neden açamıyorum?

A: Büyük olasılıkla Gnome dışındaki sistemlerde tarayıcı algılanmadığı için dahili `Desktop.getDesktop().browse(new URI(url));` çağrısı başarısız oluyordur. `libgnome` kurmayı deneyin.

```bash
$ apt-get install libgnome
```