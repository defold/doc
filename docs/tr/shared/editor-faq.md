#### Q: Düzenleyicinin sistem gereksinimleri nelerdir?
A: Düzenleyici (editor), sistemde kullanılabilir belleğin %75'ine kadarını kullanır. 4 GB RAM bulunan bir bilgisayarda bunun küçük Defold projeleri için yeterli olması beklenir. Orta büyüklükteki veya büyük projeler için 6 GB veya daha fazla RAM kullanılması önerilir.


#### Q: Defold'un beta sürümleri otomatik olarak güncelleniyor mu?
A: Evet. Defold'un beta düzenleyicisi, kararlı sürümde olduğu gibi başlangıçta güncellemeleri kontrol eder.


#### Q: Düzenleyiciyi başlatırken neden `java.awt.AWTError: Assistive Technology not found` hatasını alıyorum?
A: Bu hata, [NVDA ekran okuyucusu](https://www.nvaccess.org/download/) gibi Java yardımcı teknolojileriyle ilgili sorunlardan kaynaklanır. Muhtemelen kullanıcı klasörünüzde bir `.accessibility.properties` dosyası vardır. Dosyayı kaldırın ve düzenleyiciyi yeniden başlatmayı deneyin. (Not: Herhangi bir yardımcı teknoloji kullanıyorsanız ve bu dosyanın bulunması gerekiyorsa alternatif çözümleri görüşmek için lütfen info@defold.se adresinden bizimle iletişime geçin).

Bu konu [Defold forumunda burada ele alınmıştır](https://forum.defold.com/t/editor-endless-loading-windows-10-1-2-169-solved/65481/3).


#### Q: Düzenleyiciyi başlatırken neden `sun.security.validator.ValidatorException: PKIX path building failed` hatasını alıyorum?
A: Bu istisna, düzenleyici bir https bağlantısı kurmaya çalıştığında sunucunun sağladığı sertifika zinciri doğrulanamıyorsa ortaya çıkar.

Bu hata hakkında ayrıntılı bilgi için [bu bağlantıya](https://github.com/defold/defold/blob/master/editor/README_TROUBLESHOOTING_PKIX.md) bakın.


#### Q: Belirli işlemleri gerçekleştirirken neden `java.lang.OutOfMemoryError: Java heap space` hatasını alıyorum?
A: Defold düzenleyicisi Java kullanılarak geliştirilmiştir ve bazı durumlarda Java'nın varsayılan bellek yapılandırması yeterli olmayabilir. Bu durumda düzenleyicinin yapılandırma dosyasını düzenleyerek daha fazla bellek ayırmasını elle yapılandırabilirsiniz. `config` adlı yapılandırma dosyası, macOS'te `Defold.app/Contents/Resources/` klasöründe bulunur. Windows'ta `Defold.exe` yürütülebilir dosyasının, Linux'ta ise `Defold` yürütülebilir dosyasının yanında bulunur. `config` dosyasını açın ve `-Xmx6gb` seçeneğini `vmargs` ile başlayan satıra ekleyin. `-Xmx6gb` eklemek, en büyük öbek (heap) boyutunu 6 gigabayt olarak ayarlar (varsayılan değer genellikle 4Gb'dir). Şuna benzer bir görünüm elde etmelisiniz:

```
vmargs = -Xmx6gb,-Dfile.encoding=UTF-8,-Djna.nosys=true,-Ddefold.launcherpath=${bootstrap.launcherpath},-Ddefold.resourcespath=${bootstrap.resourcespath},-Ddefold.version=${build.version},-Ddefold.editor.sha1=${build.editor_sha1},-Ddefold.engine.sha1=${build.engine_sha1},-Ddefold.buildtime=${build.time},-Ddefold.channel=${build.channel},-Ddefold.archive.domain=${build.archive_domain},-Djava.net.preferIPv4Stack=true,-Dsun.net.client.defaultConnectTimeout=30000,-Dsun.net.client.defaultReadTimeout=30000,-Djogl.texture.notexrect=true,-Dglass.accessible.force=false,--illegal-access=warn,--add-opens=java.base/java.lang=ALL-UNNAMED,--add-opens=java.desktop/sun.awt=ALL-UNNAMED,--add-opens=java.desktop/sun.java2d.opengl=ALL-UNNAMED,--add-opens=java.xml/com.sun.org.apache.xerces.internal.jaxp=ALL-UNNAMED
```
