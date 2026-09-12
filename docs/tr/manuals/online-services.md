---
title: Çevrimiçi hizmetler
brief: Bu kılavuz, farklı oyun ve arka uç hizmetlerine nasıl bağlanacağınızı açıklar.
---
# Oyun hizmetleri

HTTP istekleri ve soket bağlantıları kullanarak internetteki binlerce farklı hizmete bağlanabilir ve bu hizmetlerle etkileşim kurabilirsiniz, ancak çoğu durumda yalnızca bir HTTP isteği göndermek yeterli olmaz. Genellikle bir tür kimlik doğrulama (authentication) kullanmanız gerekir; istek verilerinin belirli bir biçime getirilmesi ve yanıtın kullanılmadan önce ayrıştırılması gerekebilir. Elbette bunları kendiniz elle yapabilirsiniz, ancak bu tür işleri sizin yerinize yapan eklentiler (extensions) ve kütüphaneler (libraries) de vardır. Aşağıda, belirli arka uç (backend) hizmetleriyle daha kolay etkileşim kurmak için kullanılabilecek bazı eklentilerin listesini bulabilirsiniz:

## Genel amaçlı
* [Colyseus](https://defold.com/assets/colyseus/) - Çok oyunculu oyun istemcisi
* [Nakama](https://defold.com/assets/nakama/) - Oyununuza kimlik doğrulama, oyuncu eşleştirme (matchmaking), veri analizi, buluta kaydetme, çok oyunculu oyun desteği, sohbet ve daha fazlasını ekleyin
* [Photon Realtime](https://defold.com/assets/photon-realtime/) - Photon Realtime, kimlik doğrulama, oyuncu eşleştirme ve hızlı, güvenilir iletişim gibi temel özellikler için ölçeklenebilir çözümler sunar.
* [PlayFab](https://defold.com/assets/playfabsdk/) - Oyununuza kimlik doğrulama, oyuncu eşleştirme, veri analizi, buluta kaydetme ve daha fazlasını ekleyin
* [AWS SDK](https://github.com/britzl/aws-sdk-lua) - Amazon Web Services hizmetlerini oyununuzun içinden kullanın

## Kimlik doğrulama, skor tabloları, başarımlar
* [Google Play Game Services](https://defold.com/assets/googleplaygameservices/) - Oyununuzda kimlik doğrulama ve buluta kaydetme için Google Play Game Services hizmetlerini kullanın
* [Steamworks](https://defold.com/assets/steamworks/) - Oyununuza Steam desteği ekleyin
* [Apple GameKit Game Center](https://defold.com/assets/gamekit/)

## Veri analizi
* [Firebase Analytics](https://defold.com/assets/googleanalyticsforfirebase/) - Oyununuza Firebase Analytics ekleyin
* [Game Analytics](https://gameanalytics.com/docs/item/defold-sdk) - Oyununuza GameAnalytics ekleyin
* [Google Analytics](https://defold.com/assets/gameanalytics/) - Oyununuza Google Analytics ekleyin

Daha fazla eklenti için [Asset Portal](https://www.defold.com/assets/) sayfasına göz atın!
