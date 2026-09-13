#### Q: Android'de gezinme ve durum çubuklarını gizlemek mümkün mü?
A: Evet, *game.project* dosyasının *Android* bölümündeki *immersive_mode* ayarını etkinleştirin. Bu, uygulamanızın ekranın tamamını kaplamasını ve ekrandaki tüm dokunma olaylarını yakalamasını sağlar.


#### Q: Cihaza bir Defold oyunu kurarken neden "Failure [INSTALL_PARSE_FAILED_INCONSISTENT_CERTIFICATES]" hatasını alıyorum?
A: Android, uygulamayı yeni bir sertifikayla kurmaya çalıştığınızı algılar. Hata ayıklama derlemeleri (debug build) paketlenirken her derleme geçici bir sertifikayla imzalanır. Yeni sürümü kurmadan önce eski uygulamayı kaldırın:

```
$ adb uninstall com.defold.examples
Success
$ adb install Defold\ examples.apk
4826 KB/s (18774344 bytes in 3.798s)
      pkg: /data/local/tmp/Defold examples.apk
Success
```


#### Q: Belirli eklentilerle projeyi derlerken neden AndroidManifest.xml dosyasındaki çakışan özelliklerle ilgili hatalar alıyorum?
A: Bu durum, iki veya daha fazla eklentinin (extension) aynı property etiketini farklı değerlerle içeren bir Android bildirim parçası (Android Manifest stub) sağlaması durumunda ortaya çıkabilir. Örneğin Firebase ve AdMob ile bu sorun yaşanmıştır. Derleme hatası şuna benzer:

```
SEVERE: /tmp/job4531953598647135356/upload/AndroidManifest.xml:32:13-58
Error: Attribute property#android.adservices.AD_SERVICES_CONFIG@resource
value=(@xml/ga_ad_services_config) from AndroidManifest.xml:32:13-58 is also
present at AndroidManifest.xml:92:13-59 value=(@xml/gma_ad_services_config).
Suggestion: add 'tools:replace="android:resource"' to <property> element at
AndroidManifest.xml to override. 
```

Sorun ve geçici çözümü hakkında daha fazla bilgi için Defold hata bildirimi [#9453](https://github.com/defold/defold/issues/9453#issuecomment-2367367269) ve Google hata bildirimi [#327696048](https://issuetracker.google.com/issues/327696048?pli=1) sayfalarını okuyabilirsiniz.