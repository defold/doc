
## Apple gizlilik bildirimi

Gizlilik bildirimi (privacy manifest), uygulamanız veya üçüncü taraf SDK tarafından toplanan veri türlerini ve kullanılan, kullanım gerekçesi bildirilmesi zorunlu API'leri kaydeden bir özellik listesidir (property list). Uygulamanız veya üçüncü taraf SDK, topladığı her veri türü ve kullandığı, kullanım gerekçesi bildirilmesi zorunlu her API kategorisi için gerekçeleri, kendi paketine dahil edilen gizlilik bildirimi dosyasına kaydetmelidir.

Defold, *game.project* dosyasındaki Privacy Manifest alanı aracılığıyla varsayılan bir gizlilik bildirimi sağlar. Bir uygulama dağıtım paketi oluşturulurken gizlilik bildirimi, proje bağımlılıklarındaki tüm gizlilik bildirimleriyle birleştirilir ve uygulama dağıtım paketine eklenir.

Gizlilik bildirimleri hakkında daha fazla bilgi için [Apple'ın resmî belgelerini](https://developer.apple.com/documentation/bundleresources/privacy_manifest_files?language=objc) okuyun.
