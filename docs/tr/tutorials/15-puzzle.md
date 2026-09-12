---
title: Defold'da 15 bulmacası oyunu oluşturma
brief: Defold'a yeni başladıysanız bu kılavuz, Defold'un yapı taşlarından birkaçını denemenize ve betik mantığını çalıştırmanıza yardımcı olacaktır.
---

# Klasik 15 bulmacası

Bu tanınmış bulmaca, 1870'lerde Amerika'da popüler oldu. Bulmacanın amacı, tahtadaki karoları yatay ve dikey olarak kaydırarak sıralamaktır. Bulmaca, karoların karıştırıldığı bir düzenden başlar.

Bulmacanın en yaygın sürümünde karoların üzerinde 1--15 sayıları bulunur. Ancak karoları bir görüntünün parçaları hâline getirerek bulmacayı biraz daha zorlaştırabilirsiniz. Başlamadan önce bulmacayı çözmeyi deneyin. Boş kareye komşu bir karoyu tıklayarak boş konuma kaydırın.

## Projeyi oluşturma

1. Defold'u başlatın.
2. Soldaki *New Project* seçeneğini seçin.
3. *From Template* sekmesini seçin.
4. *Empty Project* seçeneğini seçin
5. Yerel sürücünüzde proje için bir konum seçin.
6. *Create New Project* seçeneğine tıklayın.

*game.project* ayarlar dosyasını açın ve oyunun boyutlarını 512⨉512 olarak ayarlayın. Bu boyutlar, kullanacağınız görüntüyle eşleşecektir.

![ekran ayarları](images/15-puzzle/display_settings.png)

Sonraki adım, bulmacaya uygun bir görüntü indirmektir. Kare biçiminde herhangi bir görüntü seçin, ancak 512'ye 512 piksel olacak şekilde ölçeklendirdiğinizden emin olun. Görüntü aramakla uğraşmak istemiyorsanız şunu kullanabilirsiniz:

![Mona Lisa](images/15-puzzle/monalisa.png)

Görüntüyü indirin, ardından projenizin *main* klasörüne sürükleyin.

## Izgarayı temsil etme

Defold, bulmaca tahtasını görselleştirmek için ideal olan yerleşik bir karo haritası (*Tilemap*) bileşeni (component) içerir. Karo haritaları, tek tek karoları ayarlamanıza ve okumanıza olanak tanır; bu proje için gereken de budur.

Ancak karo haritasını oluşturmadan önce, karo haritasının karo görüntülerini alacağı bir karo kaynağına (*Tilesource*) ihtiyacınız vardır.

*main* klasörüne <kbd>sağ tıklayın</kbd> ve <kbd>New ▸ Tile Source</kbd> seçeneğini seçin. Yeni dosyaya `monalisa.tilesource` adını verin.

Karonun *Width* ve *Height* özelliklerini 128 olarak ayarlayın. Bu işlem, 512⨉512 piksellik görüntüyü 16 karoya böler. Karoları karo haritasına yerleştirdiğinizde 1--16 olarak numaralandırılırlar.

![Karo kaynağı](images/15-puzzle/tilesource.png)

Ardından *main* klasörüne <kbd>sağ tıklayın</kbd> ve <kbd>New ▸ Tile Map</kbd> seçeneğini seçin. Yeni dosyaya "grid.tilemap" adını verin.

Defold, ızgaranın başlangıç durumunu hazırlamanızı gerektirir. Bunun için "layer1" katmanını seçin ve başlangıç noktasının hemen sağ üstüne 4⨉4 boyutunda bir karo ızgarası boyayın. Karolar için hangi değerleri ayarladığınız pek önemli değildir. Birazdan bu karoların içeriğini otomatik olarak ayarlayan kodu yazacaksınız.

![Karo haritası](images/15-puzzle/tilemap.png)

## Parçaları bir araya getirme

*main.collection* koleksiyon (collection) dosyasını açın. *Outline* görünümündeki kök düğüme <kbd>sağ tıklayın</kbd> ve <kbd>Add Game Object</kbd> seçeneğini seçin. Yeni oyun nesnesinin (game object) *Id* özelliğini "game" olarak ayarlayın.

Oyun nesnesine <kbd>sağ tıklayın</kbd> ve <kbd>Add Component File</kbd> seçeneğini seçin. *grid.tilemap* dosyasını seçin. *Id* özelliğini "tilemap" olarak ayarlayın.

Oyun nesnesine <kbd>sağ tıklayın</kbd> ve <kbd>Add Component ▸ Label</kbd> seçeneğini seçin. Etiketin (label) *Id* özelliğini "done", *Text* özelliğini ise "Well done" olarak ayarlayın. Etiketi karo haritasının merkezine taşıyın.

Etiketin ızgaranın üzerine çizildiğinden emin olmak için Z konumunu 1 olarak ayarlayın.

![Ana koleksiyon](images/15-puzzle/main_collection.png)

Ardından bulmaca mantığı için bir Lua betik (script) dosyası oluşturun: *main* klasörüne <kbd>sağ tıklayın</kbd> ve <kbd>New ▸ Script</kbd> seçeneğini seçin. Yeni dosyaya "game.script" adını verin.

Sonra *main.collection* içindeki "game" adlı oyun nesnesine <kbd>sağ tıklayın</kbd> ve <kbd>Add Component File</kbd> seçeneğini seçin. *game.script* dosyasını seçin.

Oyunu çalıştırın. Izgarayı çizdiğiniz hâliyle ve üzerinde "Well done" iletisini gösteren etiketi görmelisiniz.

## Bulmaca mantığı

Artık bütün parçalar yerli yerinde; öğreticinin geri kalanında bulmaca mantığını oluşturacağız.

Betik, tahtadaki karoların karo haritasından ayrı kendi temsilini tutacaktır. Bunun nedeni, üzerinde işlem yapmayı kolaylaştırabilmemizdir. Karoları 2 boyutlu bir dizide saklamak yerine, bir Lua tablosunda tek boyutlu bir liste olarak saklayacağız. Liste, ızgaranın sol üst köşesinden başlayıp sağ alt köşesine kadar sırayla karo numaralarını içerir:

```lua
-- The completed board looks like this:
self.board = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0}
```

Böyle bir karo listesini alıp karo haritamıza çizen kod oldukça basittir, ancak listedeki konumu x ve y konumuna dönüştürmesi gerekir:

```lua
-- Draw a table list of tiles onto a 4x4 tilemap
local function draw(t)
    for i=1, #t do
        local y = 5 - math.ceil(i/4) -- <1>
        local x = i - (math.ceil(i/4) - 1) * 4
        tilemap.set_tile("#tilemap","layer1",x,y,t[i])
    end
end
```
1. Karo haritalarında x değeri 1 ve y değeri 1 olan karo sol alttadır. Bu nedenle y konumunun yönü tersine çevrilmelidir.

Bir test `init()` işlevi oluşturarak işlevin amaçlandığı gibi çalışıp çalışmadığını denetleyebilirsiniz:

```lua
function init(self)
    -- An inverted board, for test
    self.board = {15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0}
    draw(self.board)
end
```

Karolar bir Lua tablosunda liste olarak tutulduğunda sıralarını karıştırmak çok kolaydır. Kod yalnızca listedeki her öğeyi dolaşır ve her karonun yerini rastgele seçilen başka bir karoyla değiştirir:

```lua
-- Swap two items in a table list
local function swap(t, i, j)
    local tmp = t[i]
    t[i] = t[j]
    t[j] = tmp
    return t
end

-- Randomize the order of a the elements in a table list
local function scramble(t)
    local n = #t
    for i = 1, n - 1 do
        t = swap(t, i, math.random(i, n))
    end
    return t
end
```

Devam etmeden önce 15 bulmacası hakkında dikkate almanız gereken bir nokta var: karo sırasını yukarıdaki gibi rastgele belirlerseniz bulmacanın çözülmesinin *imkânsız* olma olasılığı %50'dir.

Bu kötü bir haberdir, çünkü oyuncuya çözülemeyen bir bulmaca sunmayı kesinlikle istemezsiniz.

Neyse ki bir düzenin çözülebilir olup olmadığını belirlemek mümkündür. Bunun nasıl yapıldığına bakalım:

## Çözülebilirlik

4⨉4 boyutundaki bir bulmacada bir düzenin çözülebilir olup olmadığını belirlemek için iki bilgi gerekir:

1. Düzendeki "terslik" (inversion) sayısı. Bir karonun, kendisinden daha küçük numaralı başka bir karodan önce gelmesine terslik denir. Örneğin `{1, 2, 3, 4, 5, 6, 7, 8, 9, 12, 11, 10, 13, 14, 15, 0}` listesinde 3 terslik vardır:

    - 12 sayısının ardından 11 ve 10 gelir; bu da 2 terslik oluşturur.
    - 11 sayısının ardından 10 gelir; bu da 1 terslik daha oluşturur.

    (Çözülmüş bulmaca durumunda terslik sayısının sıfır olduğuna dikkat edin)

2. Boş karenin bulunduğu satır (listede `0` ile gösterilir).

Bu iki sayı, aşağıdaki işlevlerle hesaplanabilir:

```lua
-- Count the number of inversions in a list of tiles
local function inversions(t)
    local inv = 0
    for i=1, #t do
        for j=i+1, #t do
            if t[i] > t[j] and t[j] ~= 0 then -- <1>
                inv = inv + 1
            end
        end
    end
    return inv
end
```
1. Boş karenin hesaba katılmadığına dikkat edin.

```lua
-- Find the x and y position of a given tile
local function find(t, tile)
    for i=1, #t do
        if t[i] == tile then
            local y = 5 - math.ceil(i/4) -- <1>
            local x = i - (math.ceil(i/4) - 1) * 4
            return x,y
        end
    end
end
```
1. Alttan itibaren Y konumu.

Bu iki sayıyla artık bir bulmaca durumunun çözülebilir olup olmadığını söylemek mümkündür. 4⨉4 boyutundaki bir tahta durumu şu koşullarda *çözülebilirdir*:

- Boş kare *tek* numaralı bir satırdaysa (alttan sayarak 1 veya 3) ve terslik sayısı *çift* ise.
- Boş kare *çift* numaralı bir satırdaysa (alttan sayarak 2 veya 4) ve terslik sayısı *tek* ise.

## Bu nasıl çalışır?

Kurallara uygun her hamle, bir parçayı boş kareyle yatay veya dikey olarak yer değiştirerek hareket ettirir.

Bir parçayı yatay olarak hareket ettirmek, ne terslik sayısını ne de boş karenin bulunduğu satırın numarasını değiştirir.

Ancak bir parçayı dikey olarak hareket ettirmek, terslik sayısının tek veya çift olma durumunu değiştirir (tekten çifte veya çiftten teke). Aynı şekilde boş karenin bulunduğu satırın numarasının tek veya çift olma durumunu da değiştirir.

Örneğin:

![bir parçayı kaydırma](images/15-puzzle/slide.png)

Bu hamleyle karoların sırası şu durumdan:

`{ ... 0, 11, 2, 13, 6 ... }`

şu duruma değişir:

`{ ... 6, 11, 2, 13, 0 ... }`

Toplam terslik sayısı aşağıdaki şekilde 1 azalır:

- 6 sayısı 1 terslik ekler (2 sayısı artık 6'dan sonradır)
- 11 sayısı 1 terslik kaybeder (6 sayısı artık 11'den öncedir)
- 13 sayısı 1 terslik kaybeder (6 sayısı artık 13'ten öncedir)

Dikey bir kaydırmada terslik sayısı ±1 veya ±3 değişebilir.

Dikey bir kaydırmada boş karenin satır numarası ±1 değişebilir.

Bulmacanın son durumunda boş kare sağ alt köşededir (*tek* numaralı 1. satır) ve terslik sayısı *çift* bir değer olan 0'dır. Kurallara uygun her hamle, bu iki değeri ya olduğu gibi bırakır (yatay hamle) ya da tek veya çift olma durumlarını değiştirir (dikey hamle). Kurallara uygun hiçbir hamle, terslik sayısını ve boş karenin satır numarasını *tek*, *tek* veya *çift*, *çift* hâline getiremez.

Dolayısıyla bu iki sayının ikisinin de tek veya ikisinin de çift olduğu bir bulmaca durumunu çözmek imkânsızdır.

Çözülebilirliği denetleyen kod şöyledir:

```lua
-- Is the given table list of 4x4 tiles solvable?
local function solvable(t)
    local x,y = find(t, 0)
    if y % 2 == 1 and inversions(t) % 2 == 0 then
        return true
    end
    if y % 2 == 0 and inversions(t) % 2 == 1 then
        return true
    end
    return false    
end
```

## Kullanıcı girdisi

Şimdi geriye yalnızca bulmacayı etkileşimli hâle getirmek kaldı.

Yukarıda oluşturulan işlevleri kullanarak çalışma sırasındaki tüm hazırlıkları yapan bir `init()` işlevi oluşturun:

```lua
function init(self)
    msg.post(".", "acquire_input_focus") -- <1>
    math.randomseed(socket.gettime()) -- <2>
    self.board = scramble({1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0}) -- <3>
    while not solvable(self.board) do -- <4>
        self.board = scramble(self.board)
    end
    draw(self.board) -- <5>
    self.done = false -- <6>
    msg.post("#done", "disable") -- <7>
end
```
1. Motora bu oyun nesnesinin girdi alması gerektiğini bildirin.
2. Rastgele sayı üretecinin başlangıç değerini belirleyin.
3. Tahta için rastgele bir başlangıç durumu oluşturun.
4. Durum çözülemiyorsa yeniden karıştırın.
5. Tahtayı çizin.
6. Kazanma durumunu izlemek için bir tamamlanma bayrağı ayarlayın.
7. Tamamlanma iletisini gösteren etiketi devre dışı bırakın.

*/input/game.input_bindings* dosyasını açın ve yeni bir *Mouse Trigger* ekleyin. Eylemin adını "press" olarak ayarlayın:

![girdi](images/15-puzzle/input.png)

Betiğe dönün ve bir `on_input()` işlevi oluşturun.

```lua
-- Deal with user input
function on_input(self, action_id, action)
    if action_id == hash("press") and action.pressed and not self.done then -- <1>
        local x = math.ceil(action.x / 128) -- <2>
        local y = math.ceil(action.y / 128)
        local ex, ey = find(self.board, 0) -- <3>
        if math.abs(x - ex) + math.abs(y - ey) == 1 then -- <4>
            self.board = swap(self.board, (4-ey)*4+ex, (4-y)*4+x) -- <5>
            draw(self.board) -- <6>
        end
        ex, ey = find(self.board, 0)
        if inversions(self.board) == 0 and ex == 4 then -- <7>
            self.done = true
            msg.post("#done", "enable")
        end
    end
end
```
1. Bir fare düğmesine basıldıysa ve oyun hâlâ sürüyorsa aşağıdakileri yapın.
2. Kullanıcının tıkladığı karenin x ve y konumlarını hesaplayın.
3. Boş (0) karenin geçerli konumunu bulun.
4. Tıklanan kare, boş karenin hemen üstünde, altında, solunda veya sağındaysa aşağıdakileri yapın:
5. Tıklanan karedeki karoyla boş karenin yerini değiştirin.
6. Güncellenen tahtayı yeniden çizin.
7. Tahtadaki terslik sayısı 0 ise, yani her şey doğru sıradaysa ve boş kare en sağdaki sütundaysa (terslik sayısının 0 olması için son satırda olmalıdır), bulmaca çözülmüş demektir; bu durumda aşağıdakileri yapın:
8. Tamamlanma bayrağını ayarlayın.
9. Tamamlanma iletisini etkinleştirin/gösterin.

İşte bu kadar! İşiniz bitti, bulmaca oyunu tamamlandı!

## Betiğin tamamı

Başvuru için betik kodunun tamamı aşağıdadır:

```lua
local function inversions(t)
    local inv = 0
    for i=1, #t do
        for j=i+1, #t do
            if t[i] > t[j] and t[j] ~= 0 then
                inv = inv + 1
            end
        end
    end
    return inv
end

local function find(t, tile)
    for i=1, #t do
        if t[i] == tile then
            local y = 5 - math.ceil(i/4)
            local x = i - (math.ceil(i/4) - 1) * 4
            return x,y
        end
    end
end

local function solvable(t)
    local x,y = find(t, 0)
    if y % 2 == 1 and inversions(t) % 2 == 0 then
        return true
    end
    if y % 2 == 0 and inversions(t) % 2 == 1 then
        return true
    end
    return false    
end

local function scramble(t)
    for i=1, #t do
        local tmp = t[i]
        local r = math.random(#t)
        t[i] = t[r]
        t[r] = tmp
    end
    return t
end

local function swap(t, i, j)
    local tmp = t[i]
    t[i] = t[j]
    t[j] = tmp
    return t
end

local function draw(t)
    for i=1, #t do
        local y = 5 - math.ceil(i/4)
        local x = i - (math.ceil(i/4) - 1) * 4
        tilemap.set_tile("#tilemap","layer1",x,y,t[i])
    end
end

function init(self)
    msg.post(".", "acquire_input_focus")
    math.randomseed(socket.gettime())
    self.board = scramble({1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0})   
    while not solvable(self.board) do
        self.board = scramble(self.board)
    end
    draw(self.board)
    self.done = false
    msg.post("#done", "disable")
end

function on_input(self, action_id, action)
    if action_id == hash("press") and action.pressed and not self.done then
        local x = math.ceil(action.x / 128)
        local y = math.ceil(action.y / 128)
        local ex, ey = find(self.board, 0)
        if math.abs(x - ex) + math.abs(y - ey) == 1 then
            self.board = swap(self.board, (4-ey)*4+ex, (4-y)*4+x)
            draw(self.board)
        end
        ex, ey = find(self.board, 0)
        if inversions(self.board) == 0 and ex == 4 then
            self.done = true
            msg.post("#done", "enable")
        end
    end
end

function on_reload(self)
    self.done = false
    msg.post("#done", "disable")
end
```

## Ek alıştırmalar

1. 5⨉5 boyutunda bir bulmaca, ardından 6⨉5 boyutunda bir bulmaca yapın. Çözülebilirlik denetimlerinin genel durumlarda çalıştığından emin olun.
2. Kaydırma animasyonları ekleyin. Karolar, karo haritasından ayrı olarak hareket ettirilemediği için buna bir çözüm bulmanız gerekecektir. Belki de yalnızca kayan parçayı içeren ayrı bir karo haritası kullanabilirsiniz?
