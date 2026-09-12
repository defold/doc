---
title: Defold'da ağ iletişimi
brief: Bu kılavuz, uzak sunuculara nasıl bağlanılacağını ve diğer tür ağ bağlantılarının nasıl kurulacağını açıklar.
---

# Ağ iletişimi

Oyunların puanları göndermek, eşleştirmeyi yönetmek veya oyun kayıtlarını bulutta saklamak gibi amaçlarla bir arka uç hizmetine (backend service) bağlanması yaygındır. Birçok oyunda, oyun istemcilerinin merkezi bir sunucu olmadan doğrudan birbirleriyle iletişim kurduğu eşler arası (peer to peer) bağlantılar da bulunur. Ağ bağlantıları ve veri alışverişi, çeşitli protokoller ve standartlar kullanılarak gerçekleştirilebilir. Defold'da ağ bağlantılarını kullanmanın farklı yolları hakkında daha fazla bilgi edinin:

* [HTTP istekleri](/manuals/http-requests)
* [Soket bağlantıları](/manuals/socket-connections)
* [WebSocket bağlantıları](/manuals/websocket-connections)
* [Çevrimiçi hizmetler](/manuals/online-services)


## Teknik ayrıntılar

### IPv4 ve IPv6

Defold, soketler (socket) ve HTTP istekleri için IPv4 ve IPv6 bağlantılarını destekler.

### Güvenli bağlantılar

Defold, soketler ve HTTP istekleri için güvenli SSL bağlantılarını destekler.

Defold, isteğe bağlı olarak herhangi bir güvenli bağlantının SSL sertifikasını da doğrulayabilir. SSL doğrulaması, kök CA sertifikalarının açık anahtarlarını veya kendinden imzalı bir sertifikanın açık anahtarını içeren bir PEM dosyası [SSL Certificates ayarı](/manuals/project-settings/#network)) alanında belirtildiğinde etkinleştirilir; bu alan *game.project* dosyasının Network bölümündedir. `builtins/ca-certificates` içinde kök CA sertifikalarının bir listesi bulunur, ancak yeni bir PEM dosyası oluşturmanız ve oyunun bağlandığı sunuculara göre gereken kök CA sertifikalarını kopyalayıp yapıştırmanız önerilir.

