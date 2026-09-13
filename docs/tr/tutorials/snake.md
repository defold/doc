---
brief: Defold'a yeni başladıysanız bu kılavuz, betik mantığına ve Defold'un bazı yapı taşlarına giriş yaparak sıfırdan bir Snake benzeri oyun oluşturmanıza yardımcı olacaktır.
layout: tutorial
title: Defold'da bir yılan oyunu oluşturma
difficulty: Beginner
---

# Yılan

Bu öğretici, yeniden yapmayı deneyebileceğiniz en yaygın klasik oyunlardan birini oluşturma sürecinde size yol gösterir. Bu oyunun birçok çeşidi vardır; burada "yiyecek" yiyen ve yalnızca yediğinde büyüyen bir yılan bulunur. Bu yılan ayrıca engellerin bulunduğu bir oyun alanında sürünür.

![Küçük resim](images/snake/thumbnail.png)

### Neler öğreneceksiniz

Bu öğreticide şunları öğreneceksiniz:
- Defold'da sıfırdan oyun oluşturma
- Girdileri ayarlama ve işleme
- Karo haritaları oluşturma ve bunları çalışma sırasında değiştirme
- Lua dilinde betik yazma

### Yeni başlayanlar için bir not

Bu öğretici yeni başlayanlar için tasarlanmıştır; ancak Defold ve oyun geliştirme konusunda tamamen yeniyseniz önce giriş niteliğindeki bazı kılavuzları, özellikle [Defold'un yapı taşları](/manuals/building-blocks/) ve [Terim sözlüğü](/manuals/glossary/) kılavuzlarını okumanızı öneririz. Henüz Defold'u indirmediyseniz [Kurulum kılavuzuna](/manuals/install/) bakın. Düzenleyiciyi hızla tanımak için [Düzenleyiciye genel bakış](/manuals/editor/) kılavuzuna da göz atmanız önerilir; ayrıca burada her adım için ekran görüntüleri sunuyoruz.

## Projeyi oluşturma

Defold'u başlatın ve:

1. Sol tarafta *Create From* ▸ *Templates* seçeneğini seçin.
2. *Empty Project* seçeneğini seçin.
3. *Title* alanına bir proje adı yazın.
4. Proje için *Location* alanında bir konum seçin.
5. *Create New Project* düğmesine tıklayın.

![Başlangıç](images/snake/1.png)

<input type="checkbox"/> Tamam!

## Proje ayarları

Oyunun çözünürlüğünü belirleyerek başlayacağız.

1. Düzenleyici açıldığında sol taraftaki *Assets* bölmesinde `game.project` dosyasını bulun. Açmak için dosyaya çift tıklayın.
2. `game.project` dosyasının *Display* bölümüne gidin.
3. Oyunun boyutlarını (`Width` ve `Height`) 768⨉768 veya 16'nın başka bir katı olacak şekilde ayarlayın.

![Ekran ayarları](images/snake/2.png)

Bunu yapmanızın nedeni, oyunun her parçası 16x16 piksel olan bir ızgara üzerine çizilecek olmasıdır; böylece oyun ekranı hiçbir parçayı kısmen kesmez. `game.project` dosyası projenin tüm önemli ayarlarını içerir; bunların tamamını [Proje ayarları kılavuzunda](/manuals/project-settings/) okuyabilirsiniz.

<input type="checkbox"/> Tamam!

## Assets bölmesinde yeni klasörler oluşturma

Sade bir Snake benzeri oyun için çok az grafik gerekir. Yılan için 16⨉16 boyutunda bir yeşil parça, engeller için bir beyaz blok ve yiyeceği temsil eden daha küçük bir kırmızı blok.

Önce Defold düzenleyicisinde varlıklar (assets) için bir dizin oluşturun:

1. `main` klasörüne <kbd>sağ tıklayın</kbd>
2. `New Folder` seçeneğini seçin.
3. Ad soran bir açılır pencere görünecektir; `assets` yazın ve `Create Folder` düğmesine tıklayın.

![Yeni klasör](images/snake/3.png)

<input type="checkbox"/> Tamam!

## Oyuna grafik ekleme

Aşağıdaki görüntü, ihtiyacınız olan tek varlıktır:

![Yılan sprite görüntüleri](images/snake/snake.png)

1. Yukarıdaki görüntüye <kbd>sağ tıklayın</kbd> ve yerel diskinize kaydedin. Ardından indirdiğiniz görüntüyü proje klasöründe az önce oluşturduğunuz yeni konuma sürükleyip bırakın (veya kopyalayıp yapıştırın).

![Yeni klasör](images/snake/4.png)

[Varlıkları içe aktarma hakkında daha fazla ayrıntıyı burada](/manuals/importing-graphics/) da okuyabilirsiniz.

<input type="checkbox"/> Tamam!

## Karo kaynağı ekleme

Defold, ızgara üzerinde hizalanmış *karolardan* (tiles) oluşan oyun alanını oluşturmak için kullanacağınız yerleşik bir [karo haritası (Tile Map)](/manuals/tilemap/) bileşeni (component) sunar. Karo haritası, karoları tek tek ayarlamanıza ve okumanıza olanak tanır; bu da bu oyun için çok uygundur. Karo haritaları grafiklerini bir [karo kaynağından (Tile Source)](/manuals/tilesource/) aldığı için bir karo kaynağı oluşturmanız gerekir:

1. `assets` klasörüne <kbd>sağ tıklayın</kbd>.
2. "Resources" bölümünde `New` ▸ `Tile Source` seçeneğini seçin.
3. Yeni dosyaya "snake" adını verin (düzenleyici dosyayı `snake.tilesource` olarak kaydedecektir).

![Yeni karo kaynağı](images/snake/5.png)

Karo kaynağı, bu dosya türüne özel Tile Source Editor içinde açılır ve çalışabilmesi için bir görüntü belirtmeniz istenir. Sağ tarafta `Properties` bölmesini bulabilirsiniz:

4. `Image` özelliğini az önce içe aktardığınız grafik dosyasına ayarlayın.
![Karo kaynağı](images/snake/6.png)

5. `Width` ve `Height` özellikleri 16 (varsayılan değer) olarak bırakılmalıdır. Bu, 32⨉32 piksellik görüntüyü 1–4 olarak numaralandırılmış 4 karoya böler.

![Karo kaynağı özellikleri](images/snake/7.png)

*Extrude Borders* özelliğinin 2 piksel olarak ayarlandığına dikkat edin. Bu, grafikleri kenara kadar uzanan karoların çevresinde görüntü kusurları oluşmasını önler.

Bir dosyada değişiklik yaparsanız sekmesinde adının yanında bir yıldız işareti `*` görünür. Tüm dosyaları kaydetmek için `File` ▸ `Save All` seçeneğini seçin veya <kbd>Ctrl</kbd>+<kbd>S</kbd> (Mac'te <kbd>⌘Cmd</kbd> + <kbd>S</kbd>) kısayolunu kullanın.

<input type="checkbox"/> Tamam!

## Oyun alanının karo haritasını oluşturma

Artık kullanıma hazır bir karo kaynağınız var; şimdi oyun alanının karo haritası bileşenini oluşturma zamanı:

1. `main` klasörüne <kbd>sağ tıklayın</kbd> ve "Components" bölümünde <kbd>New</kbd> ▸ <kbd>Tile Map</kbd> seçeneğini seçin. Yeni dosyaya "grid" adını verin (düzenleyici dosyayı "grid.tilemap" olarak kaydedecektir).
![Karo haritası ekleme](images/snake/8.png)

2. Dosya Tile Map Editor içinde açılır ve bir **Tile Source** gerektiğini belirtir; bu nedenle *Tile Source* özelliğini daha önce oluşturduğunuz "snake.tilesource" dosyasına ayarlayın.
![Karo kaynağını ayarlama](images/snake/9.png)

<input type="checkbox"/> Tamam!

## Karo haritasına karo çizme

Defold, karo haritasının yalnızca kullanılan alanını saklar; bu nedenle ekran sınırlarını dolduracak kadar karo eklemeniz gerekir.

1. Sağ taraftaki `Outline` bölmesinde `layer1` katmanını seçin.
2. Karo paletini göstermek için `Edit` ▸ `Select Tile...` menü seçeneğini veya <kbd>Space</kbd> kısayolunu kullanın, ardından boyarken kullanmak istediğiniz karoya tıklayın.
![Karo haritası](images/snake/10.png)

3. Ekranın kenarlarını çevreleyen bir sınır ve birkaç engel boyayın.
![Tamamlanmış karo haritası](images/snake/11.png)

Oyun ekranını doldurmak için 48x48 karo boyutunda bir karo haritasına ihtiyacınız olacak (çünkü ekran boyutumuz 768 ve karolarımız 16 piksel, dolayısıyla 768/16 = 48).

Bitirdiğinizde karo haritasını kaydedin.

<input type="checkbox"/> Tamam!

## Karo haritasını oyuna ekleme

Şimdi karo haritamızı oyuna eklememiz gerekiyor. Defold'un yapı taşlarını biliyorsanız bileşenlerin oyun nesnelerinin (game objects) bir parçası olduğunu ve oyun nesnelerinin koleksiyonlarda (collections) tanımlanabildiğini de biliyorsunuzdur.

1. `Assets` bölmesinde `main.collection` dosyasına çift tıklayarak açın. Bu dosya, Empty Project şablonunda varsayılan olarak motor başlatıldığında yüklenen başlangıç koleksiyonudur (bootstrap collection).

2. `Outline` görünümünde köke <kbd>sağ tıklayın</kbd> ve `Add Game Object` seçeneğini seçin. Bu işlem, oyun başladığında yüklenen koleksiyonda yeni bir oyun nesnesi oluşturur.
![Oyun nesnesi ekleme](images/snake/12.png)

3. Yeni oyun nesnesine <kbd>sağ tıklayın</kbd> ve `Add Component File` seçeneğini seçin. Az önce oluşturduğunuz "grid.tilemap" dosyasını seçin.
![Bileşen ekleme](images/snake/13.png)

Artık oyun koleksiyonumuzda bir karo haritası var. Oyunu düzenleyiciden çalıştırdığınızda görünür olmalıdır.

1. `Project` ▸ `Build` seçeneğini seçin veya <kbd>Ctrl</kbd> + <kbd>B</kbd> (Mac'te <kbd>⌘Cmd</kbd> + <kbd>B</kbd>) kısayolunu kullanın.

![Oyunu çalıştırma](images/snake/14.png)

<input type="checkbox"/> Tamam!

## Oyuna betik ekleme

1. `Assets` tarayıcısında `main` klasörüne <kbd>sağ tıklayın</kbd> ve Scripts bölümünde `New` ▸ `Script` seçeneğini seçin. Yeni betik (script) dosyasına "snake" adını verin ("snake.script" olarak kaydedilecektir). Bu dosya oyunun tüm mantığını içerecektir.
![Betik ekleme](images/snake/15.png)

2. *main.collection* dosyasına dönün ve karo haritasını barındıran oyun nesnesine <kbd>sağ tıklayın</kbd>. <kbd>Add&nbsp;Component&nbsp;File</kbd> seçeneğini seçin ve "snake.script" dosyasını seçin.

![Ana koleksiyon](images/snake/16.png)

Artık karo haritası bileşeni ve betik hazır.

<input type="checkbox"/> Tamam!

## Oyun betiği

Yazacağınız betik oyunun tamamını yönetecek. Özellikleri tek tek ekleyeceğiz.

### Basit hareket algoritması

Nasıl çalışacağına ilişkin fikir şu:

1. Betik, yılanın o anda kapladığı karo konumlarının bir listesini tutar.
2. Oyuncu bir yön tuşuna basarsa yılanın hareket etmesi gereken yönü saklayın.
3. Düzenli aralıklarla yılanı geçerli hareket yönünde bir adım ilerletin.

### Başlangıç işlemleri

*snake.script* dosyasını açın ve `init()` işlevini bulun. Oyun başladığında betiğin başlangıç işlemleri yapılırken motor bu işlevi çağırır. Kodu aşağıdaki gibi değiştirin:

```lua
function init(self)
    self.segments = { -- <1>
        {x = 7, y = 24},
        {x = 8, y = 24},
        {x = 9, y = 24},
        {x = 10, y = 24}
    }
    self.dir = {x = 1, y = 0} -- <2>
    self.speed = 7.0 -- <3>
    self.time = 0 -- <4>
end
```

Bu kodda şunları yapıyoruz:

1. Yılanın parçalarını `self.segments` adlı bir Lua tablosunda saklıyoruz. Bu tablo, her biri bir parçanın X ve Y konumunu tutan tabloların listesini içerir.
2. Geçerli yönü, X ve Y yönünü tutan `self.dir` adlı bir tabloda saklıyoruz.
3. Geçerli hareket hızını, saniyede geçilen karo sayısı olarak `self.speed` içinde saklıyoruz.
4. Hareket hızını takip etmek için kullanılacak bir zamanlayıcı değerini `self.time` içinde saklıyoruz.

Yukarıdaki betik kodu Lua dilinde yazılmıştır. Kod hakkında dikkat etmeniz gereken birkaç nokta var; ancak aşağıdakileri henüz anlamıyorsanız endişelenmeyin. Adımları izleyin, denemeler yapın ve kendinize zaman tanıyın; sonunda anlayacaksınız. Şimdilik `init()` içinde kullanacağımız değişkenlere yalnızca başlangıç değerlerini verdiğimizi aklınızda tutmanız yeterli.

- Defold, betik bileşeninin yaşam süresi boyunca çağrılan bir dizi yerleşik geri çağırım (callback) *işlevi* ayırır. Bunlar yöntem *değildir*, sıradan işlevlerdir.
- Çalışma zamanı ortamı, `self` parametresi aracılığıyla geçerli betik bileşeni örneğine (instance) bir başvuru geçirir. `self` başvurusu örneğe ait verileri saklamak için kullanılır.
- `self` başvurusu, içinde veri saklayabileceğiniz bir Lua tablosu olarak kullanılabilir. Diğer tablolarda olduğu gibi noktalı gösterimi kullanmanız yeterlidir: `self.data = "value"`. Başvuru, betiğin yaşam süresi boyunca geçerlidir; bu örnekte oyunun başlangıcından siz oyundan çıkana kadar.
- Lua tablo değişmezleri süslü ayraçlar `{}` içine yazılır.
- Tablo girdileri anahtar-değer çiftleri (`{x = 10, y = 20}`), iç içe Lua tabloları (`{ {a = 1}, {b = 2} }`) veya başka veri türleri olabilir.

<input type="checkbox"/> Tamam!

### Güncelleme

`init()` işlevi, betik bileşeninin çalışan oyunda bir örneği oluşturulduğunda tam olarak bir kez çağrılır. Buna karşılık `update()` işlevi **her karede** bir kez çağrılır. Bu da işlevi gerçek zamanlı oyun mantığı için ideal kılar.

Güncellemenin temel fikri şu: belirli aralıklarla aşağıdakileri yapın:

1. Yılanın başının nerede olduğunu bulun, ardından geçerli hareket yönünde bir adım ötesindeki konumda yeni bir baş oluşturun. Yani yılan X=1 ve Y=0 yönünde hareket ediyorsa ve geçerli baş X=0 ve Y=0 konumundaysa yeni baş X=1 ve Y=0 konumunda olmalıdır.
2. Yeni başın konumunu yılanı oluşturan parçaların listesine kaydedin.
3. Kuyruğun konumunu parçalar tablosundan alın.
4. Bu konumdaki kuyruk karosunu temizleyin.
5. Yılanın tüm parçalarını (karoları) tablodaki konumlara çizin.

![Algoritma](images/snake/17.png)

:::sidenote
Yılanın başının tablonun sonunda, kuyruğunun ise başında olduğunu unutmayın.
:::

1. *snake.script* dosyasında `update()` işlevini bulun ve kodu aşağıdaki gibi değiştirin:

```lua
function update(self, dt)
    self.time = self.time + dt -- <1>
    if self.time >= 1.0 / self.speed then -- <2>
        local head = self.segments[#self.segments] -- <3>

        local newhead = {
            x = head.x + self.dir.x,
            y = head.y + self.dir.y
        } -- <4>

        table.insert(self.segments, newhead) -- <5>

        local tail = table.remove(self.segments, 1) -- <6>

        tilemap.set_tile("#grid", "layer1", tail.x, tail.y, 0) -- <7>

        for i, s in ipairs(self.segments) do -- <8>
            tilemap.set_tile("#grid", "layer1", s.x, s.y, 2) -- <9>
        end

        self.time = 0 -- <10>
    end
end
```

Bu kodda şunları yapıyoruz:

1. Zamanlayıcıyı, `update()` işlevinin son çağrılışından bu yana geçen süre (saniye cinsinden), yani "delta time" veya `dt` kadar ilerletiyoruz.
2. Zamanlayıcı yeterince ilerlediyse:
3. Geçerli başın konumunu alıyoruz. `#`, dizi olarak kullanılan bir tablonun uzunluğunu almak için kullanılan işleçtir. Bizim tablomuz da dizi olarak kullanılır; tüm parçalar, anahtar belirtilmeden tanımlanmış tablo değerleridir.
4. Geçerli başın konumuna ve hareket yönüne (`self.dir`) göre yeni bir baş parçası oluşturuyoruz.
5. Yeni başı parçalar tablosunun (sonuna) ekliyoruz.
6. Kuyruğu parçalar tablosunun başından kaldırıyoruz.
7. Kaldırılan kuyruğun konumundaki karoyu temizliyoruz. `#grid` karo haritamızda `layer1` adlı yalnızca 1 katman bulunur.
8. Parçalar tablosundaki öğeler üzerinde döngü kuruyoruz. Her yinelemede `i`, tablodaki konuma (1'den başlayarak), `s` ise geçerli parçaya ayarlanır.
9. Parçanın konumundaki karoyu 2 değerine ayarlıyoruz (bu, yılanın yeşil rengini içeren karodur).
10. İşimiz bittiğinde zamanlayıcıyı sıfırlıyoruz.

Oyunu şimdi çalıştırırsanız 4 parça uzunluğundaki yılanın oyun alanında soldan sağa süründüğünü görmelisiniz.

![Oyunu çalıştırma](images/snake/snake_run_1.png)

<input type="checkbox"/> Tamam!

## Oyuncu girdisi

Oyuncu girdisine tepki verecek kodu eklemeden önce girdi bağlantılarını ayarlamanız gerekir.

### Girdi eşlemeleri

1. `input` klasöründeki `game.input_binding` dosyasını bulun ve açmak için dosyaya <kbd>çift tıklayın</kbd>.
2. Yukarı, aşağı, sola ve sağa hareket için bir dizi *Key Trigger* eşlemesi ekleyin. *Input* sütununda klavye tuşlarını seçin ve *Action* sütunlarına eylem adlarını yazın.

![Girdi](images/snake/18.png)

Girdi eşlemesi (input binding) dosyası, gerçek kullanıcı girdilerini (tuşlar, fare hareketleri vb.) girdi almayı talep etmiş betiklere iletilen eylem *adlarıyla* eşler.

<input type="checkbox"/> Tamam!

### Girdi odağını alma

Eşlemeler hazır olduğunda girdi odağını (input focus) almak için *snake.script* dosyasını açın ve `init()` işlevinin başına aşağıdaki satırı ekleyin:

```lua
function init(self)
    msg.post(".", "acquire_input_focus") -- <1>

    self.segments = {
        {x = 7, y = 24},
        {x = 8, y = 24},
        {x = 9, y = 24},
        {x = 10, y = 24}
    }
    self.dir = {x = 1, y = 0}
    self.speed = 7.0
    self.time = 0
end
```

Eklenen satır:
1. Geçerli oyun nesnesine ("." geçerli oyun nesnesinin kısa yazımıdır) motordan girdi almaya başlamasını söyleyen bir ileti (message) gönderir.

Ardından `on_input` işlevini bulun ve aşağıdaki kodu yazın:

```lua
function on_input(self, action_id, action)
    if action_id == hash("up") and action.pressed then -- <1>
        self.dir.x = 0 -- <2>
        self.dir.y = 1
    elseif action_id == hash("down") and action.pressed then
        self.dir.x = 0
        self.dir.y = -1
    elseif action_id == hash("left") and action.pressed then
        self.dir.x = -1
        self.dir.y = 0
    elseif action_id == hash("right") and action.pressed then
        self.dir.x = 1
        self.dir.y = 0
    end
end
```

Bu `if...elseif...` dalları şunları yapar:
1. Girdi eşlemelerinde ayarlandığı gibi "up" girdi eylemi alınırsa ve `action` tablosunun `pressed` alanı `true` değerindeyse (oyuncu tuşa basmışsa):
2. Hareket yönünü ayarlar.

Oyunu yeniden çalıştırın ve yılanı yönlendirebildiğinizi kontrol edin.

<input type="checkbox"/> Tamam!

### Girdi işlemeyi iyileştirme

İki tuşa aynı anda basarsanız her basış için bir tane olmak üzere `on_input()` işlevinin iki kez çağrılacağına dikkat edin. Yukarıdaki kodda, sonraki `on_input()` çağrıları `self.dir` içindeki değerlerin üzerine yazacağından yalnızca en son çağrı yılanın yönünü etkiler.

Ayrıca yılan sola giderken <kbd>right</kbd> tuşuna basarsanız yılanın kendi üzerine döneceğine dikkat edin. Bu sorunun *görünüşte* bariz çözümü, `on_input()` içindeki `if` koşullarına ek bir koşul koymaktır:

```lua
if action_id == hash("up") and self.dir.y ~= -1 and action.pressed then
    ...
elseif action_id == hash("down") and self.dir.y ~= 1 and action.pressed then
    ...
```

Ancak yılan sola giderken oyuncu bir sonraki hareket adımı gerçekleşmeden önce *hızla* sırasıyla <kbd>up</kbd> ve <kbd>right</kbd> tuşlarına basarsa yalnızca <kbd>right</kbd> tuşuna basılması etkili olur ve yılan kendi üzerine hareket eder. Yukarıda gösterilen `if` ifadelerine koşullar eklendiğinde girdi yok sayılır. *Bu iyi değil!*

Bu sorunu doğru biçimde çözmek için girdiyi bir kuyrukta saklayıp yılan hareket ettikçe bu kuyruktan girdileri almak gerekir:

```lua
function init(self)
    msg.post(".", "acquire_input_focus")

    self.segments = {
        {x = 7, y = 24},
        {x = 8, y = 24},
        {x = 9, y = 24},
        {x = 10, y = 24}
    }
    self.dir = {x = 1, y = 0}
    self.speed = 7.0
    self.time = 0

    self.dirqueue = {} -- <1>
end
```

Bu kez:
1. Boş bir tablo olarak başlatılan `self.dirqueue` değişkenini ekledik.

`update()` işlevine şunları ekleyin:

```lua
function update(self, dt)
    self.time = self.time + dt
    if self.time >= 1.0 / self.speed then
        local newdir = table.remove(self.dirqueue, 1) -- <1>
        if newdir then
            local opposite = newdir.x == -self.dir.x or newdir.y == -self.dir.y -- <2>
            if not opposite then
                self.dir = newdir -- <3>
            end
        end

        local head = self.segments[#self.segments]
        local newhead = {x = head.x + self.dir.x, y = head.y + self.dir.y}

        table.insert(self.segments, newhead)

        local tail = table.remove(self.segments, 1)
        tilemap.set_tile("#grid", "layer1", tail.x, tail.y, 0)

        for i, s in ipairs(self.segments) do
            tilemap.set_tile("#grid", "layer1", s.x, s.y, 2)
        end

        self.time = 0
    end
end
```

1. Yön kuyruğundan ilk öğeyi alın.
2. Bir öğe varsa (`newdir` null değilse) `newdir` yönünün `self.dir` yönünün tersi olup olmadığını kontrol edin.
3. Yeni yönü yalnızca ters yönü göstermiyorsa ayarlayın.

Ayrıca `on_input` işlevini, bunun yerine geçerli girdiyi kuyrukta saklayacak şekilde değiştirin:

```lua
function on_input(self, action_id, action)
    if action_id == hash("up") and action.pressed then
        table.insert(self.dirqueue, {x = 0, y = 1}) -- <1>
    elseif action_id == hash("down") and action.pressed then
        table.insert(self.dirqueue, {x = 0, y = -1})
    elseif action_id == hash("left") and action.pressed then
        table.insert(self.dirqueue, {x = -1, y = 0})
    elseif action_id == hash("right") and action.pressed then
        table.insert(self.dirqueue, {x = 1, y = 0})
    end
end
```

1. `self.dir` değerini doğrudan ayarlamak yerine girdi yönünü yön kuyruğuna ekleyin.

Oyunu başlatın ve beklendiği gibi oynandığını kontrol edin.

<input type="checkbox"/> Tamam!

## Yiyecek ve engellerle çarpışma

Yılanın uzaması ve hızlanması için haritada yiyeceğe ihtiyacı var. Bunu ekleyelim!

### Yiyecek oluşturma

`init()` işlevinin üstüne yeni bir işlev ekleyin:

```lua
local function put_food(self) -- <1>
    self.food = {x = math.random(2, 47), y = math.random(2, 47)} -- <2>
    tilemap.set_tile("#grid", "layer1", self.food.x, self.food.y, 3) -- <3>
end
```

Bu işlevde şunları yapıyoruz:
1. Haritaya bir yiyecek yerleştiren `put_food()` adlı yeni bir işlev tanımlıyoruz.
2. Rastgele bir X ve Y konumunu `self.food` adlı değişkende saklıyoruz.
3. X ve Y konumundaki karoyu, yiyeceğin karo grafiği olan 3 değerine ayarlıyoruz.

Ardından bu işlevi `init()` işlevinin sonunda çağırın:
```lua
function init(self)
    msg.post(".", "acquire_input_focus")

    self.segments = {
        {x = 7, y = 24},
        {x = 8, y = 24},
        {x = 9, y = 24},
        {x = 10, y = 24}
    }
    self.dir = {x = 1, y = 0}
    self.dirqueue = {}
    self.speed = 7.0
    self.time = 0

    math.randomseed(socket.gettime()) -- <1>
    put_food(self) -- <2>
end
```

1. `math.random()` ile rastgele değerler almaya başlamadan önce rastgelelik tohumunu ayarlayın; aksi takdirde aynı rastgele değer dizisi üretilir. Bu tohum yalnızca bir kez ayarlanmalıdır.
2. Oyuncunun haritada bir yiyecekle başlaması için oyun başlangıcında `put_food()` işlevini çağırın.

<input type="checkbox"/> Tamam!

### Yiyeceği yeme

Artık yılanın bir şeye çarpıp çarpmadığını algılamak için karo haritasında yılanın gideceği yerde ne olduğuna bakıp buna tepki vermek yeterli.

Yılanın hayatta olup olmadığını takip eden bir değişken ekleyin:

```lua
function init(self)
    msg.post(".", "acquire_input_focus")

    self.segments = {
        {x = 7, y = 24},
        {x = 8, y = 24},
        {x = 9, y = 24},
        {x = 10, y = 24}
    }
    self.dir = {x = 1, y = 0}
    self.dirqueue = {}
    self.speed = 7.0
    self.time = 0

    self.alive = true -- <1>

    math.randomseed(socket.gettime())
    put_food(self)
end
```

1. Yılanın hayatta olup olmadığını belirten bir bayrak.

Ardından duvar/engel ve yiyecekle çarpışmayı denetleyen mantığı ekleyin:

```lua
function update(self, dt)
    self.time = self.time + dt
    if self.time >= 1.0 / self.speed and self.alive then -- <1>
        local newdir = table.remove(self.dirqueue, 1)

        if newdir then
            local opposite = newdir.x == -self.dir.x or newdir.y == -self.dir.y
            if not opposite then
                self.dir = newdir
            end
        end

        local head = self.segments[#self.segments]
        local newhead = {x = head.x + self.dir.x, y = head.y + self.dir.y}

        table.insert(self.segments, newhead)

        local tile = tilemap.get_tile("#grid", "layer1", newhead.x, newhead.y) -- <2>

        if tile == 2 or tile == 4 then
            self.alive = false -- <3>
        elseif tile == 3 then
            self.speed = self.speed + 1 -- <4>
            put_food(self)
        else
            local tail = table.remove(self.segments, 1) -- <5>
            tilemap.set_tile("#grid", "layer1", tail.x, tail.y, 1)
        end

        for i, s in ipairs(self.segments) do
            tilemap.set_tile("#grid", "layer1", s.x, s.y, 2)            
        end

        self.time = 0
    end
end
```

1. Yılanı yalnızca hayattaysa ilerletin.
2. Karo haritasına çizim yapmadan önce yılanın yeni başının bulunacağı konumda ne olduğunu okuyun.
3. Karo bir engel veya yılanın başka bir parçasıysa oyun biter!
4. Karo yiyecekse hızı artırın, ardından yeni bir yiyecek yerleştirin.
5. Kuyruğun yalnızca çarpışma olmadığında kaldırıldığına dikkat edin. Bu, oyuncu yiyecek yediğinde o hareket sırasında kuyruk kaldırılmadığı için yılanın bir parça uzayacağı anlamına gelir.

Şimdi oyunu deneyin ve oynanışın düzgün olduğundan emin olun!

Öğretici burada sona eriyor; ancak oyun üzerinde denemeler yapmaya devam edin ve aşağıdaki alıştırmalardan bazılarını tamamlayın!

<input type="checkbox"/> Tamam!

## Betiğin tamamı

Başvurmanız için betiğin tüm kodu aşağıdadır:

```lua
local function put_food(self)
    self.food = {x = math.random(2, 47), y = math.random(2, 47)}
    tilemap.set_tile("#grid", "layer1", self.food.x, self.food.y, 3)        
end

function init(self)
    msg.post(".", "acquire_input_focus")

    self.segments = {
        {x = 7, y = 24},
        {x = 8, y = 24},
        {x = 9, y = 24},
        {x = 10, y = 24}
    }
    self.dir = {x = 1, y = 0}
    self.dirqueue = {}
    self.speed = 7.0
    self.time = 0

    self.alive = true

    math.randomseed(socket.gettime())
    put_food(self)
end

function update(self, dt)
    self.time = self.time + dt
    if self.time >= 1.0 / self.speed and self.alive then
        local newdir = table.remove(self.dirqueue, 1)

        if newdir then
            local opposite = newdir.x == -self.dir.x or newdir.y == -self.dir.y
            if not opposite then
                self.dir = newdir
            end
        end

        local head = self.segments[#self.segments]
        local newhead = {x = head.x + self.dir.x, y = head.y + self.dir.y}

        table.insert(self.segments, newhead)

        local tile = tilemap.get_tile("#grid", "layer1", newhead.x, newhead.y)

        if tile == 2 or tile == 4 then
            self.alive = false
        elseif tile == 3 then
            self.speed = self.speed + 1
            put_food(self)
        else
            local tail = table.remove(self.segments, 1)
            tilemap.set_tile("#grid", "layer1", tail.x, tail.y, 1)
        end

        for i, s in ipairs(self.segments) do
            tilemap.set_tile("#grid", "layer1", s.x, s.y, 2)            
        end

        self.time = 0
    end
end

function on_input(self, action_id, action)
    if action_id == hash("up") and action.pressed then
        table.insert(self.dirqueue, {x = 0, y = 1})
    elseif action_id == hash("down") and action.pressed then
        table.insert(self.dirqueue, {x = 0, y = -1})
    elseif action_id == hash("left") and action.pressed then
        table.insert(self.dirqueue, {x = -1, y = 0})
    elseif action_id == hash("right") and action.pressed then
        table.insert(self.dirqueue, {x = 1, y = 0})
    end
end
```

## Alıştırmalar

Şu iyileştirmeleri uygulamayı denemek iyi bir alıştırmadır:

1. Oyun bittiğinde yeniden başlatmak için bir tuş girdisini işleyen kod ekleyin.
2. İster yalnızca bir etiket bileşeni (label component) kullanarak (daha kolay), ister bir GUI oluşturarak puanlama ve puan sayacı ekleyin.
3. put_food() işlevi, yılanın konumunu veya engelleri hesaba katmaz. Yiyeceği yalnızca boş yerlere yerleştirecek şekilde düzeltin.
4. Oyun bittiğinde bir "Game Over" iletisi gösterin ve oyuncunun yeniden denemesine izin verin.
5. Ek alıştırma: oyuncunun kontrol ettiği ikinci bir yılan ekleyin.
