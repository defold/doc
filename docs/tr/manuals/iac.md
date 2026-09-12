---
title: Defold'da uygulamalar arası iletişim
brief: Uygulamalar arası iletişim (inter-app communication), uygulamanız başlatılırken kullanılan başlatma bağımsız değişkenlerine erişmenizi sağlar. Bu kılavuz, Defold'un bu işlevsellik için sunduğu API'yi açıklar.
---

# Uygulamalar arası iletişim

Çoğu işletim sisteminde uygulamalar çeşitli yollarla başlatılabilir:

* Kurulu uygulamalar listesinden
* Uygulamaya özgü bir bağlantıdan
* Bir anlık bildirimden (push notification)
* Kurulum sürecinin son adımı olarak.

Uygulama bir bağlantıdan veya bildirimden ya da kurulum sırasında başlatıldığında ek bağımsız değişkenler iletilebilir. Örneğin, kurulum sırasında kurulum yönlendirme bilgisi (install referrer), uygulamaya özgü bir bağlantıdan veya bildirimden başlatılırken ise derin bağlantı (deep link) iletilebilir. Defold, bir yerel kod eklentisi (native extension) aracılığıyla uygulamanın nasıl çağrıldığına ilişkin bilgileri almak için ortak bir yöntem sunar.

## Eklentiyi kurma

Uygulamalar arası iletişim eklentisini kullanmaya başlamak için eklentiyi *game.project* dosyanıza bağımlılık olarak eklemeniz gerekir. En son kararlı sürüme şu bağımlılık URL adresinden ulaşabilirsiniz:
```
https://github.com/defold/extension-iac/archive/master.zip
```

[Belirli bir sürümün](https://github.com/defold/extension-iac/releases) zip dosyasına bağlantı kullanmanızı öneririz.

## Eklentiyi kullanma

API'nin kullanımı çok kolaydır. Eklentiye bir dinleyici işlevi (listener function) sağlarsınız ve dinleyicinin geri çağırımlarına (callback) tepki verirsiniz.

```
local function iac_listener(self, payload, type)
     if type == iac.TYPE_INVOCATION then
         -- This was an invocation
         print(payload.origin) -- origin may be empty string if it could not be resolved
         print(payload.url)
     end
end

function init(self)
     iac.set_listener(iac_listener)
end
```

API belgelerinin tamamına [eklentinin GitHub sayfasından](https://defold.github.io/extension-iac/) ulaşabilirsiniz.
