---
title: Defold'da kütüphane projeleriyle çalışma
brief: Kütüphaneler özelliği, projeler arasında varlık paylaşmanızı sağlar. Bu kılavuz, özelliğin nasıl çalıştığını açıklar.
---

# Kütüphaneler

Kütüphaneler (Libraries) özelliği, projeler arasında varlık (asset) paylaşmanızı sağlar. İş akışınızda çeşitli biçimlerde kullanabileceğiniz, basit ama çok güçlü bir mekanizmadır.

Kütüphaneler aşağıdaki amaçlar için kullanışlıdır:

* Tamamlanmış bir projedeki varlıkları yeni bir projeye kopyalamak. Önceki bir oyunun devamını yapıyorsanız bu, işe başlamanın kolay bir yoludur.
* Projelerinize kopyalayıp ardından özelleştirebileceğiniz veya belirli bir amaca uyarlayabileceğiniz bir şablon kütüphanesi oluşturmak.
* Doğrudan başvurabileceğiniz hazır nesneler veya betikler içeren bir ya da daha fazla kütüphane oluşturmak. Bu, ortak betik modüllerini saklamak veya grafik, ses ve animasyon varlıklarından oluşan ortak bir kütüphane oluşturmak için çok kullanışlıdır.

## Kütüphane paylaşımını ayarlama {#setting-up-library-sharing}

Paylaşılan sprite bileşenleri ve karo kaynakları (tile source) içeren bir kütüphane oluşturmak istediğinizi varsayalım. Önce [yeni bir proje oluşturun](/manuals/project-setup/). Projeden hangi klasörleri paylaşmak istediğinize karar verin ve bu klasörlerin adlarını proje ayarlarındaki *`include_dirs`* özelliğine ekleyin. Birden fazla klasör listelemek istiyorsanız adları boşluklarla ayırın:

![Dahil edilecek dizinler](images/libraries/libraries_include_dirs.png)

Bu kütüphaneyi başka bir projeye eklemeden önce kütüphanenin konumunu belirlemenin bir yoluna ihtiyacımız var.

## Kütüphane URL adresi

Kütüphanelere standart bir URL aracılığıyla başvurulur. GitHub'da barındırılan bir proje için bu, projenin yayımlanan bir sürümünün URL adresidir:

![GitHub kütüphane URL adresi](images/libraries/libraries_library_url_github.png)

::: important
Bir kütüphane projesinin `master` dalı yerine her zaman belirli bir sürümüne bağımlı olmanız önerilir. Böylece kütüphane projesinin `master` dalından her zaman en son (ve mevcut işleyişi bozabilecek) değişiklikleri almak yerine, kütüphane projesindeki değişiklikleri ne zaman dahil edeceğinize geliştirici olarak siz karar verirsiniz.
:::

::: important
Üçüncü taraf kütüphaneleri kullanmadan önce her zaman incelemeniz önerilir. [Üçüncü taraf yazılımları güvenli kullanma](https://defold.com/manuals/application-security/#securing-your-use-of-third-party-software) hakkında daha fazla bilgi edinin.
:::

### Temel erişim kimlik doğrulaması

Herkese açık olmayan kütüphaneleri kullanırken temel erişim kimlik doğrulaması yapmak için kütüphane URL adresine kullanıcı adı ve parola/belirteç ekleyebilirsiniz:

```
https://username:password@github.com/defold/private/archive/main.zip
```

`username` ve `password` alanları çıkarılıp `Authorization` istek üstbilgisi olarak eklenir. Bu, temel erişim yetkilendirmesini destekleyen her sunucuda çalışır.

::: important
Oluşturduğunuz kişisel erişim belirtecini veya parolayı paylaşmadığınızdan ya da yanlışlıkla sızdırmadığınızdan emin olun; bunların yanlış ellere geçmesi ciddi sonuçlar doğurabilir!
:::

Kimlik bilgilerinin kütüphane URL adresinde açık metin olarak bulunması nedeniyle yanlışlıkla sızmasını önlemek için bir dize değiştirme kalıbı kullanabilir ve kimlik bilgilerini ortam değişkenlerinde saklayabilirsiniz:

```
https://__PRIVATE_USERNAME__:__PRIVATE_TOKEN__@github.com/defold/private/archive/main.zip
```

Yukarıdaki örnekte kullanıcı adı ve belirteç, sistemin `PRIVATE_USERNAME` ve `PRIVATE_TOKEN` ortam değişkenlerinden okunur.

#### GitHub kimlik doğrulaması

GitHub'daki özel bir depodan veri almak için [kişisel erişim belirteci oluşturmanız](https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/creating-a-personal-access-token) ve bunu parola olarak kullanmanız gerekir.

```
https://github-username:personal-access-token@github.com/defold/private/archive/main.zip
```

#### GitLab kimlik doğrulaması

GitLab'daki özel bir depodan veri almak için [kişisel erişim belirteci oluşturmanız](https://docs.gitlab.com/ee/security/token_overview.html) ve bunu URL parametresi olarak göndermeniz gerekir.

```
https://gitlab.com/defold/private/-/archive/main/test-main.zip?private_token=personal-access-token
```

### Gelişmiş erişim kimlik doğrulaması

Temel erişim kimlik doğrulaması kullanıldığında, bir kullanıcının erişim belirteci ve kullanıcı adı projede kullanılan her depoda paylaşılır. Birden fazla kişiden oluşan bir ekipte bu sorun olabilir. Bu sorunu çözmek için kütüphanenin bulunduğu depoya erişimde "salt okunur" bir kullanıcı kullanılmalıdır. GitHub'da bunun için bir kuruluş, bir ekip ve depoyu düzenlemesi gerekmeyen (bu nedenle salt okunur olan) bir kullanıcı gerekir.

GitHub adımları:
* [Bir kuruluş oluşturun](https://docs.github.com/en/github/setting-up-and-managing-organizations-and-teams/creating-a-new-organization-from-scratch)
* [Kuruluş içinde bir ekip oluşturun](https://docs.github.com/en/github/setting-up-and-managing-organizations-and-teams/creating-a-team)
* [İstediğiniz özel depoyu kuruluşunuza aktarın](https://docs.github.com/en/github/administering-a-repository/transferring-a-repository)
* [Ekibe depoya "salt okunur" erişim verin](https://docs.github.com/en/github/setting-up-and-managing-organizations-and-teams/managing-team-access-to-an-organization-repository)
* [Bu ekibin üyesi olacak bir kullanıcı oluşturun veya seçin](https://docs.github.com/en/github/setting-up-and-managing-organizations-and-teams/organizing-members-into-teams)
* Bu kullanıcı için kişisel erişim belirteci oluşturmak üzere yukarıdaki "temel erişim kimlik doğrulaması" bölümünü kullanın

Bu aşamada yeni kullanıcının kimlik doğrulama bilgileri sürüm kontrolüne kaydedilip depoya gönderilebilir. Bu, özel deponuzla çalışan herkesin, kütüphanenin kendisini düzenleme izni olmadan depoyu kütüphane olarak almasını sağlar.

::: important
Salt okunur kullanıcının belirtecine, kütüphaneyi kullanan oyun depolarına erişebilen herkes tamamen erişebilir.
:::

Bu çözüm Defold forumunda önerilmiş ve [bu başlıkta tartışılmıştır](https://forum.defold.com/t/private-github-for-library-solved/67240).

## Kütüphane bağımlılıklarını ayarlama {#setting-up-library-dependencies}

Kütüphaneye erişmesini istediğiniz projeyi açın. Proje ayarlarında kütüphane URL adresini *dependencies* özelliğine ekleyin. İsterseniz birden fazla bağımlı proje belirtebilirsiniz. Bunları `+` düğmesini kullanarak birer birer ekleyin ve `-` düğmesini kullanarak kaldırın:

![Bağımlılıklar](images/libraries/libraries_dependencies.png)

Şimdi kütüphane bağımlılıklarını güncellemek için <kbd>Project ▸ Fetch Libraries</kbd> seçeneğini seçin. Bu işlem, bir projeyi her açtığınızda otomatik olarak gerçekleşir. Bu nedenle yalnızca projeyi yeniden açmadan bağımlılıklar değişirse bu işlemi yapmanız gerekir. Bağımlılık olarak kullanılan kütüphaneleri eklediğinizde veya kaldırdığınızda ya da bu kütüphane projelerinden biri başka biri tarafından değiştirilip eşitlendiğinde bu durum oluşur.

![Kütüphaneleri alma](images/libraries/libraries_fetch_libraries.png)

Paylaştığınız klasörler artık *Assets bölmesinde* görünür ve paylaştığınız her şeyi kullanabilirsiniz. Kütüphane projesinde yapılan ve eşitlenen tüm değişiklikler projenizde kullanılabilir hale gelir.

![Kütüphane kurulumu tamamlandı](images/libraries/libraries_done.png)

## Kütüphane bağımlılıklarındaki dosyaları düzenleme

Kütüphanelerdeki dosyalar kaydedilemez. Değişiklik yapabilirsiniz ve düzenleyici bu değişikliklerle projeyi derleyebilir; bu, test için kullanışlıdır. Ancak dosyanın kendisi değişmeden kalır ve dosya kapatıldığında tüm değişiklikler atılır.

Kütüphane dosyalarında değişiklik yapmak istiyorsanız kütüphanenin size ait bir çatallanmasını (fork) oluşturun ve değişiklikleri orada yapın. Bir diğer seçenek, kütüphane klasörünün tamamını proje dizininize kopyalayıp yapıştırmak ve yerel kopyayı kullanmaktır. Bu durumda yerel klasörünüz özgün bağımlılığın önüne geçer ve bağımlılık bağlantısının `game.project` dosyasından kaldırılması önerilir (ardından <kbd>Project ▸ Fetch Libraries</kbd> seçeneğini seçmeyi unutmayın).

`builtins` de motor tarafından sağlanan bir kütüphanedir. Oradaki dosyaları düzenlemek istiyorsanız dosyaları projenize kopyalayın ve özgün `builtins` dosyaları yerine bunları kullanın. Örneğin, `default.render_script` dosyasını değiştirmek için hem `/builtins/render/default.render` hem de `/builtins/render/default.render_script` dosyasını proje klasörünüze `my_custom.render` ve `my_custom.render_script` adlarıyla kopyalayın. Ardından yerel `my_custom.render` dosyanızı, yerleşik betik yerine `my_custom.render_script` dosyasına başvuracak şekilde güncelleyin ve özel `my_custom.render` dosyanızı `game.project` içindeki Render ayarında belirtin.

Bir materyali kopyalayıp yapıştırdıysanız ve belirli bir türün tüm bileşenlerinde (component) kullanmak istiyorsanız [projeye özel şablonları](/manuals/editor/#creating-new-project-files) kullanmak yararlı olabilir.

## Bozuk başvurular

Kütüphane paylaşımı yalnızca paylaşılan klasörlerin altında bulunan dosyaları içerir. Paylaşılan hiyerarşinin dışındaki varlıklara başvuran bir şey oluşturursanız başvuru yolları bozulur.

## Ad çakışmaları

*dependencies* proje ayarında birden fazla proje URL adresi listeleyebildiğiniz için ad çakışmasıyla karşılaşabilirsiniz. Bu, bağımlı projelerden iki veya daha fazlasının *`include_dirs`* proje ayarında aynı adlı bir klasörü paylaşması durumunda gerçekleşir.

Defold, aynı adlı klasörlere yapılan başvurulardan *dependencies* listesindeki proje URL sırasına göre sonuncusu dışındaki tümünü yok sayarak ad çakışmalarını çözer. Örneğin, bağımlılıklarda 3 kütüphane projesinin URL adresini listelerseniz ve hepsi *items* adlı bir klasör paylaşıyorsa yalnızca bir *items* klasörü görünür---URL listesinin sonundaki projeye ait olan klasör.
