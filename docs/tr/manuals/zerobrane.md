---
title: ZeroBrane Studio ile hata ayıklama
brief: Bu kılavuz, Defold'daki Lua kodunda hata ayıklamak için ZeroBrane Studio'nun nasıl kullanılacağını açıklar.
---

# ZeroBrane Studio ile Lua betiklerinde hata ayıklama

Defold yerleşik bir hata ayıklayıcı (debugger) içerir; ancak ücretsiz ve açık kaynaklı Lua tümleşik geliştirme ortamı (IDE) _ZeroBrane Studio_ uygulamasını haricî bir hata ayıklayıcı olarak çalıştırmak da mümkündür. Hata ayıklama özelliklerini kullanmak için ZeroBrane Studio'nun kurulu olması gerekir. Program birden çok platformu destekler ve hem macOS hem de Windows üzerinde çalışır.

"ZeroBrane Studio" uygulamasını http://studio.zerobrane.com adresinden indirin

## ZeroBrane yapılandırması

ZeroBrane'in projenizdeki dosyaları bulabilmesi için Defold proje dizininizin konumunu belirtmeniz gerekir. Bu konumu bulmanın pratik bir yolu, Defold projenizin kök dizinindeki bir dosyada <kbd>Show in Desktop</kbd> seçeneğini kullanmaktır.

1. *game.project* dosyasına sağ tıklayın
2. <kbd>Show in Desktop</kbd> seçeneğini seçin

![Show in Finder](images/zerobrane/show_in_desktop.png)

## ZeroBrane'i ayarlama

ZeroBrane'i ayarlamak için <kbd>Project ▸ Project Directory ▸ Choose...</kbd> seçeneğini seçin:

![Ayarlama](images/zerobrane/setup.png)

Bu ayar geçerli Defold proje diziniyle eşleşecek şekilde yapıldığında, ZeroBrane'de Defold projesinin dizin ağacını görebilmeniz, dosyalar arasında gezinebilmeniz ve dosyaları açabilmeniz gerekir.

Önerilen ancak zorunlu olmayan diğer yapılandırma değişikliklerini belgenin ilerleyen bölümlerinde bulabilirsiniz.

## Hata ayıklama sunucusunu başlatma

Bir hata ayıklama oturumu başlatmadan önce ZeroBrane'in yerleşik hata ayıklama sunucusunun başlatılması gerekir. Sunucuyu başlatan menü seçeneği <kbd>Project</kbd> menüsündedir. <kbd>Project ▸ Start Debugger Server</kbd> seçeneğini seçmeniz yeterlidir:

![Hata ayıklayıcıyı başlatma](images/zerobrane/startdebug.png)

## Uygulamanızı hata ayıklayıcıya bağlama

Hata ayıklama, Defold uygulamasının çalıştığı süre boyunca herhangi bir anda başlatılabilir; ancak işlemin Lua betiğinden (Lua script) açıkça başlatılması gerekir. Bir hata ayıklama oturumu başlatmak için kullanılan Lua kodu şöyledir:

::: sidenote
`dbg.start()` çağrıldığında oyununuz kapanıyorsa bunun nedeni ZeroBrane'in bir sorun algılayıp oyuna çıkış komutu göndermesi olabilir. Nedeni bilinmemekle birlikte, ZeroBrane hata ayıklama oturumunu başlatmak için bir dosyanın açık olmasını gerektirir; aksi takdirde şu çıktıyı verir:
"Can't start debugging without an opened file or with the current file not being saved 'untitled.lua')."
Bu hatayı düzeltmek için ZeroBrane'de `dbg.start()` eklediğiniz dosyayı açın.
:::

```lua
dbg = require "builtins.scripts.mobdebug"
dbg.start()
```

Yukarıdaki kodu uygulamaya eklediğinizde uygulama, ZeroBrane'in hata ayıklama sunucusuna (varsayılan olarak "localhost" üzerinden) bağlanır ve yürütülecek bir sonraki deyimde duraklar.

```txt
Debugger server started at localhost:8172.
Mapped remote request for '/' to '/Users/my_user/Documents/Projects/Defold_project/'.
Debugging session started in '/Users/my_user/Documents/Projects/Defold_project'.
```

Artık ZeroBrane'in hata ayıklama özelliklerini kullanabilirsiniz; kodda adım adım ilerleyebilir, inceleme yapabilir, kesme noktası (breakpoint) ekleyip kaldırabilir ve benzeri işlemler yapabilirsiniz.

::: sidenote
Hata ayıklama yalnızca başlatıldığı Lua bağlamı (Lua context) için etkinleştirilir. *game.project* dosyasında "shared_state" ayarını etkinleştirdiğinizde, hata ayıklamayı nerede başlattığınızdan bağımsız olarak uygulamanızın tamamında hata ayıklayabilirsiniz.
:::

![Adım adım ilerleme](images/zerobrane/code.png)

Bağlantı girişimi başarısız olursa (örneğin hata ayıklama sunucusu çalışmadığı için), uygulamanız bağlantı girişiminin ardından normal şekilde çalışmaya devam eder.

## Uzaktan hata ayıklama

Hata ayıklama standart ağ bağlantıları (TCP) üzerinden gerçekleştiği için uzaktan hata ayıklama da yapılabilir. Bu, uygulamanız bir mobil cihazda çalışırken hata ayıklayabileceğiniz anlamına gelir.

Gereken tek değişiklik, hata ayıklamayı başlatan komuttadır. Varsayılan olarak `start()` localhost adresine bağlanmayı dener; ancak uzaktan hata ayıklama için ZeroBrane'in hata ayıklama sunucusunun adresini aşağıdaki gibi elle belirtmemiz gerekir:

```lua
dbg = require "builtins.scripts.mobdebug"
dbg.start("192.168.5.101")
```

Bu nedenle uzak cihazdan ağ bağlantısı sağlandığından ve güvenlik duvarları veya benzeri yazılımların 8172 bağlantı noktasından TCP bağlantılarına izin verdiğinden emin olmak da önemlidir. Aksi takdirde uygulama, başlatılırken hata ayıklama sunucunuza bağlanmaya çalıştığında takılı kalabilir.

## Önerilen diğer ZeroBrane ayarı

ZeroBrane'in hata ayıklama sırasında Lua betik dosyalarını otomatik olarak açmasını sağlayabilirsiniz. Böylece diğer kaynak dosyalardaki işlevlerin içine, dosyaları elle açmak zorunda kalmadan ilerleyebilirsiniz.

İlk adım, düzenleyicinin yapılandırma dosyasına erişmektir. Dosyanın kullanıcıya özel sürümünü değiştirmeniz önerilir.

- <kbd>Edit ▸ Preferences ▸ Settings: User</kbd> seçeneğini seçin
- Yapılandırma dosyasına şunları ekleyin:

  ```txt
  - to automatically open files requested during debugging
  editor.autoactivate = true
  ```

- ZeroBrane'i yeniden başlatın

![Önerilen diğer ayarlar](images/zerobrane/otherrecommended.png)
