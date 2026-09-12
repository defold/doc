#### Q: Dokusu olmayan GUI kutu düğümleri (box node) neden düzenleyicide saydam görünüyor, ancak projeyi derleyip çalıştırdığımda beklendiği gibi görüntüleniyor?

A: Bu hata [AMD Radeon GPU kullanan bilgisayarlarda](https://github.com/defold/editor2-issues/issues/2723) meydana gelebilir. Grafik sürücülerinizi güncellediğinizden emin olun.

#### Q: Bir atlası veya sahne görünümünü açarken neden `com.sun.jna.Native.open.class java.lang.Error: Access is denied` hatasını alıyorum?

A: Defold'u yönetici olarak çalıştırmayı deneyin. Defold'un yürütülebilir dosyasına sağ tıklayın ve "Run as Administrator" seçeneğini seçin.

#### Q: Windows'ta Intel UHD tümleşik GPU kullanırken oyunumda neden görüntü işleme (rendering) düzgün çalışmıyor (oysa HTML5 derleme çıktım çalışıyor)?

A: Sürücünüzü 27.20.100.8280 veya daha yeni bir sürüme güncellediğinizden emin olun. Kontrol etmek için [Intel Driver Support Assistant](https://www.intel.com/content/www/us/en/search.html?ws=text#t=Downloads&layout=table&cf:Downloads=%5B%7B%22actualLabel%22%3A%22Graphics%22%2C%22displayLabel%22%3A%22Graphics%22%7D%2C%7B%22actualLabel%22%3A%22Intel%C2%AE%20UHD%20Graphics%20Family%22%2C%22displayLabel%22%3A%22Intel%C2%AE%20UHD%20Graphics%20Family%22%7D%2C%7B%22actualLabel%22%3A%22Intel%C2%AE%20UHD%20Graphics%20630%22%2C%22displayLabel%22%3A%22Intel%C2%AE%20UHD%20Graphics%20630%22%7D%5D) aracını kullanın. Ek bilgi için [bu forum gönderisine](https://forum.defold.com/t/sprite-game-object-is-not-rendering/69198/35?u=britzl) bakabilirsiniz.

#### Q: Defold düzenleyicisi çöküyor ve günlükte `AWTError: Assistive Technology not found` görünüyor

Düzenleyici çöktüğünde günlükte `Caused by: java.awt.AWTError: Assistive Technology not found: com.sun.java.accessibility.AccessBridge` ifadesi yer alıyorsa şu adımları izleyin:

* `C:\Users\<username>` klasörüne gidin
* `.accessibility.properties` adlı dosyayı standart bir metin düzenleyicisiyle açın (Notepad uygundur)
* Yapılandırmada aşağıdaki satırları bulun:

```
assistive_technologies=com.sun.java.accessibility.AccessBridge
screen_magnifier_present=true
```

* Bu satırların başına bir kare işareti (`#``) ekleyin
* Dosyada yaptığınız değişiklikleri kaydedin ve Defold'u yeniden başlatın
