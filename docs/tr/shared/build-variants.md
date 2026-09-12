## Derleme çeşitleri

Bir oyunun dağıtım paketini oluştururken kullanmak istediğiniz motor türünü seçmeniz gerekir. Üç temel seçeneğiniz vardır:

  * Debug
  * Release
  * Headless

Bu farklı sürümler derleme çeşitleri (`Build variants`) olarak da adlandırılır.

::: sidenote
<kbd>Project ▸ Build</kbd> seçeneğini seçtiğinizde her zaman hata ayıklama sürümünü elde edersiniz.
:::


### Debug

Bu tür yürütülebilir dosyalar, birkaç yararlı hata ayıklama özelliği içerdiği için genellikle oyun geliştirme sırasında kullanılır:

* Profil çıkarıcı (profiler) - Performans ve kullanım sayaçlarını toplamak için kullanılır. Profil çıkarıcının nasıl kullanılacağını [Profil çıkarma kılavuzundan](/manuals/profiling/) öğrenin.
* Günlüğe kaydetme (logging) - Günlüğe kaydetme etkinleştirildiğinde motor, sistem bilgilerini, uyarıları ve hataları günlüğe kaydeder. Motor ayrıca Lua'nın `print()` işlevinden ve `dmLogInfo()`, `dmLogError()` gibi işlevlerle günlüğe kaydeden yerel kod eklentilerinden (native extension) gelen günlükleri de çıktıya yazar. Bu günlükleri nasıl okuyacağınızı [Oyun ve sistem günlükleri kılavuzundan](https://defold.com/manuals/debugging-game-and-system-logs/) öğrenin.
* Çalışma sırasında yeniden yükleme (hot reload) - Çalışma sırasında yeniden yükleme, geliştiricinin oyun çalışırken bir kaynağı (resource) yeniden yüklemesini sağlayan güçlü bir özelliktir. Bunu nasıl kullanacağınızı [Çalışma sırasında yeniden yükleme kılavuzundan](https://defold.com/manuals/hot-reload/) öğrenin.
* Motor hizmetleri (engine services) - Çeşitli açık TCP bağlantı noktaları ve hizmetler aracılığıyla bir oyunun hata ayıklama sürümüne bağlanmak ve bu sürümle etkileşim kurmak mümkündür. Bu hizmetler, yukarıda sözü edilen çalışma sırasında yeniden yükleme özelliğini, uzaktan günlük erişimini ve profil çıkarıcıyı, ayrıca motorla uzaktan etkileşim kurmaya yönelik başka hizmetleri de içerir. Motor hizmetleri hakkında daha fazla bilgi için [geliştirici belgelerine](https://github.com/defold/defold/blob/dev/engine/docs/DEBUG_PORTS_AND_SERVICES.md) bakın.


### Release

Bu çeşitte hata ayıklama özellikleri devre dışıdır. Oyun, uygulama mağazasında yayımlanmaya veya başka yollarla oyuncularla paylaşılmaya hazır olduğunda bu seçeneğin seçilmesi önerilir. Bir oyunu hata ayıklama özellikleri etkin durumdayken yayımlamak çeşitli nedenlerle önerilmez:

* Hata ayıklama özellikleri ikili dosyada az da olsa yer kaplar ve [yayımlanan bir oyunun ikili dosya boyutunu olabildiğince küçük tutmaya çalışmak iyi bir uygulamadır](https://defold.com/manuals/optimization/#optimize-application-size).
* Hata ayıklama özellikleri az da olsa CPU süresi de kullanır. Kullanıcının donanımı düşük özelliklere sahipse bu durum oyunun performansını etkileyebilir. Cep telefonlarında artan CPU kullanımı, ısınmaya ve pilin tükenmesine de katkıda bulunur.
* Hata ayıklama özellikleri, güvenlik, hile veya dolandırıcılık açısından oyuncuların görmesi amaçlanmayan oyun bilgilerini açığa çıkarabilir.


### Headless

Bu yürütülebilir dosya herhangi bir grafik veya ses olmadan çalışır. Bu, oyunun birim/duman testlerini (unit/smoke tests) bir sürekli tümleştirme (CI) sunucusunda çalıştırabileceğiniz, hatta bu dosyayı bulutta bir oyun sunucusu olarak kullanabileceğiniz anlamına gelir.
