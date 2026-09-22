---
title: Magic Link öğreticisi
brief: Bu öğreticide başlangıç ekranı, oyun mekanikleri ve giderek zorlaşan bölümlerle basit bir ilerleme sistemi içeren, eksiksiz küçük bir bulmaca oyunu oluşturacaksınız.
---

# Magic Link öğreticisi

Bu oyun, _Bejeweled_ ve _Candy Crush_ tarzındaki klasik eşleştirme oyununun bir çeşididir. Oyuncu aynı renkteki blokları kaldırmak için sürükleyerek birbirine bağlar. Ancak oyunun amacı aynı renkteki uzun blok dizilerini kaldırmak, tahtayı temizlemek veya puan toplamak değil, tahtanın çeşitli yerlerine dağılmış özel "sihirli blokların" birbirine bağlanmasını sağlamaktır.

Bu öğretici, tamamlanmış bir tasarımdan yola çıkarak oyunu oluşturduğumuz, adım adım ilerleyen bir kılavuz olarak yazılmıştır. Gerçekte işe yarayan bir tasarım bulmak çok zaman ve emek ister. Temel bir fikirle başlayıp ardından bu fikrin neler sunabileceğini daha iyi anlamak için bir prototipini oluşturmanın yolunu bulabilirsiniz. "Magic Link" gibi basit bir oyun bile oldukça fazla tasarım çalışması gerektirir. Bu oyun, son biçimine (hâlâ kusursuz olmaktan çok uzak olsa da) ve oyun kurallarına ulaşana kadar birkaç yinelemeden ve bazı denemelerden geçti. Ancak bu öğreticide o süreci atlayıp son tasarım üzerinden oyunu oluşturmaya başlayacağız.

## Başlarken

Yeni bir proje oluşturup varlık (asset) paketini içe aktararak başlamanız gerekir:

* "Empty Project" şablonundan [yeni bir proje](/manuals/project-setup/#creating-a-new-project) oluşturun
* Başvuru olarak kullanmak için "Magic Link" projesinin tamamını [magic-link.zip](https://github.com/defold/defold-examples/releases/latest) dosyası olarak indirin. Projeyi sıfırdan oluşturmak isterseniz gereken tüm varlıklar bu eksiksiz projede bulunur.

## Oyun kuralları

![Oyun kuralları şeması](images/magic-link/linker_rules.png)

Tahta her turda rastgele renkli bloklarla ve bir dizi sihirli blokla doldurulur. Renkli bloklar şu kurallara uyar:

* Oyuncu onları aynı renkteki bloklarla (sürükleyerek) bağlarsa kaybolurlar.
* Bloklar kaybolduğunda alt tarafta boşluklar bırakır. Renkli bloklar, altlarında açılan boşluklara dikey olarak düşer.
* Ekranın alt kenarı tüm blokların daha fazla düşmesini engeller.

Sihirli bloklar ise şu kurallara göre farklı davranır:

* Sihirli bloklar, iki yanlarından birinde bir boşluk açılırsa _yana doğru_ hareket eder.
* Altlarında bir boşluk açılırsa bunun yerine normal renkli bloklar gibi düşerler.

Oyuncu oyunla şu kurallar çerçevesinde etkileşime girer:

* Oyuncu yatay, dikey ve çapraz olarak komşu olan renkli blokları sürükleyerek birbirine bağlayabilir.
* Bağlanan bloklar, oyuncu dokunma girdisini bıraktığı (parmağını kaldırdığı) anda kaybolur.
* Sihirli bloklar sürüklemeye tepki vermez ve elle bağlanamaz.
* Ancak sihirli bloklar yatay veya dikey olarak birbirine temas ettiğinde tepki verir. Yani bu koşullarda otomatik olarak bağlanırlar.
* Oyuncu tahtadaki tüm sihirli blokların otomatik olarak bağlanmasını sağlamayı başarırsa bölüm tamamlanır.

Zorluk düzeyi, tahtaya yerleştirilen sihirli blokların sayısını belirler.

## Genel bakış

Her projede olduğu gibi, uygulamaya genel hatlarıyla nasıl yaklaşacağımızı planlamamız gerekir. Oyunu yapılandırmanın ve oluşturmanın birçok yolu vardır. İsteseydik teknik olarak oyunun tamamını grafik kullanıcı arayüzü (GUI) sistemi içinde geliştirebilirdik. Ancak oyunu oyun nesneleri (game object) ve sprite bileşenleriyle (sprite component) oluşturup ekrandaki GUI ve oyun içi bilgi göstergesi (HUD) öğeleri için GUI API'lerini kullanmak çoğu zaman oyun oluşturmanın doğal yoludur; biz de bu yolu izleyeceğiz.

Dosya sayısının oldukça az kalmasını beklediğimiz için proje klasör yapısını çok basit tutacağız:

![Klasör yapısı](images/magic-link/linker_folders.png)

*main*
: Oyunun tüm mantığı bu klasörde yer alacak. Tüm betikler (script), oyun nesnesi dosyaları, koleksiyon (collection) dosyaları, GUI dosyaları ve benzerleri bu klasörde bulunacak. Bu klasörü birkaç klasöre bölmek veya alt klasörler kullanmak isterseniz bunda hiçbir sakınca yoktur.

*images*
: Tüm görüntü varlıkları bu klasörde bulunacak.

*fonts*
: Metin işleme (rendering) için kullanılan yazı tipleri burada tutulur.

*input*
: Girdi eşlemeleri (input binding) bu klasörde tutulur.

## Projeyi hazırlama

*game.project* dosyasında çoğunlukla varsayılan ayarlar korunur, ancak karar vermemiz gereken bazı ayarlar vardır. Öncelikle oyun için bir çözünürlük seçmemiz gerekir. Çözünürlüğü daha sonra değiştirmek oldukça kolaydır. Oyunun son hâlinde ise hedef cihazın çözünürlüğünden veya en boy oranından bağımsız olarak iyi görünmesini sağlamak için biraz çalışma yapmamız gerekecek.

Çözünürlüğü iPhone 4'ün doğal çözünürlüğü olan 640x960 piksel olarak ayarlamayı seçtik. Bu çözünürlük birçok monitöre de sığdığından bilgisayarda oynanış testi yapmak rahat olur. Farklı bir çözünürlükte çalışmak isterseniz yalnızca birkaç değeri farklı şekilde ayarlamanız gerekir.

![Proje ayarları](images/magic-link/linker_project_settings.png)

Ayrıca işlenebilecek en fazla sprite sayısını artırmamız gerekecek. İsterseniz sonraki bölüme geçebilir ve konsolda sprite sınırına ulaştığınız bildirildiğinde buraya dönebilirsiniz.

![Oyun boyutlarının yerleşimi](images/magic-link/linker_layout.png)

Gereken en fazla sprite sayısını hesaplayabiliriz:

* Oyun tahtasında 7x9 blok bulunacak. Tahtanın kenarlarında biraz boşluk, üst kısmında da bazı GUI öğeleri için yer gerekecek. Bu da blokların boyutunun yaklaşık 90x90 piksel olacağı anlamına gelir. Daha küçük olurlarsa küçük bir telefon ekranında etkileşime girmek için fazla küçük kalırlar.
* Her blok bir sprite bileşenidir. Bloğun rengini ayarlamak için tek karelik animasyonlar kullanacağız.
* Blokların bazıları sihirli blok olacak ve bunların her birinde özel efektler için 4 sprite bileşeni kullanacağız.
* Bağlantı grafikleri için öğe başına bir sprite bileşeni gerekecek. En kötü durumda oyuncu bir şekilde tüm tahtayı (sürükleyerek bağlanamayan 2 sihirli blok dışında) bağlarsa bu, 61 ek sprite bileşeni demektir.

En fazla 30 sihirli bloğumuz olduğunu varsayalım. Tahta 63 bloktan (sprite bileşeninden) oluşur. Bunların içindeki 30 sihirli bloğun her biri özel efektler için 4 sprite bileşeni ekler. Bu, 120 ek sprite bileşeni demektir. Dolayısıyla bağlantı grafikleriyle birlikte (bu durumda en fazla 33) her karede en az 120 + 33 = 153 sprite çizmemiz gerekecek. İkinin en yakın kuvveti 256'dır.

Ancak üst sınırı 256 olarak ayarlamak yeterli değildir. Tahtayı her temizleyip sıfırladığımızda mevcut tüm oyun nesnelerini silip yenilerini oluşturacağız. Sprite sayısının, kare boyunca yaşamını sürdüren tüm nesnelere yetecek kadar olması gerekir. Silinen nesneler de buna dahildir; çünkü bunlar karenin sonunda kaldırılır. Bu nedenle en fazla sprite sayısını 512 olarak ayarlamak yeterli olacaktır.

![En fazla sprite sayısı](images/magic-link/linker_sprite_max_count.png)

## Grafik varlıklarını ekleme

Oyun için gereken tüm varlıklar önceden hazırlandı. Bunları 512x512 piksellik görüntüler olarak ekliyor ve motorun hedef boyuta küçültmesini sağlıyoruz.

::: sidenote
Proje ayarlarında *hidpi* seçeneğini etkinleştirmek arka arabelleğin yüksek çözünürlüklü olmasını sağlar. Büyük görüntüleri küçülterek çizdiğinizde Retina ekranlarda çok net görünürler.
:::

![Görüntü ekleme](images/magic-link/linker_add_images.png)

Bloklara ek olarak bir "connector" (bağlayıcı) görüntüsü ve efekt sprite bileşenleri de bulunur. Ayrıca iki arka plan görüntümüz vardır. Biri oyun tahtasının arka planı, diğeri ana menü için kullanılacak. Tüm görüntüleri *images* klasörüne ekleyin, ardından *sprites.atlas* adlı bir atlas dosyası oluşturun. Atlas dosyasını açıp tüm görüntüleri ekleyin.

![Atlasa görüntü ekleme](images/magic-link/linker_add_to_atlas.png)

Düğmeler ve açılır pencereler gibi GUI öğelerini oluşturmak için kullanılan bir dizi GUI görüntüsü vardır. Bunlar *gui.atlas* adlı ayrı bir atlasa eklenir.

## Tahtayı oluşturma

İlk adım tahta mantığını oluşturmaktır. Tahta, oynanış sırasında ekranda görünen her şeyi içeren kendi koleksiyonunda yer alacak. Şimdilik yalnızca "blockfactory" fabrika (factory) bileşeni ve betik gerekiyor. Daha sonra bağlantılar için bir fabrika, ana menü GUI bileşenleri ve son olarak ana menüden oyunu başlatmak için yükleme mekanikleri ile menüye dönmenin bir yolunu ekleyeceğiz.

1. *`board.collection`* dosyasını *`main`* klasöründe oluşturun. Daha sonra adresleyebilmek için adını "board" olarak ayarladığınızdan emin olun. Arka plan sprite bileşenini eklerseniz Z konumunu -1 olarak ayarladığınızdan emin olun; aksi takdirde daha sonra oluşturacağımız tüm blokların arkasında çizilmez.
2. Kolayca test edebilmek için *game.project* dosyasında (*Bootstrap* altındaki) *Main Collection* ayarını geçici olarak `/main/board.collection` yapın.

![Tahta koleksiyonu](images/magic-link/linker_board_collection.png)

![Başlangıçta tahta koleksiyonunun yüklenmesi](images/magic-link/linker_bootstrap_board.png)

*board.script* betik dosyası, tahtanın kendisi ve tahtadaki bloklar için tüm mantığı içerecek. Tahtayı oluşturan işlevi yazarak başlayın ve onu `init()` içinden (geçici olarak) çağırın. Şu an kullanmayacağımız, ancak daha sonra işimize yarayacak iki işlev daha ekliyoruz:

`filter()`
: Bu işlev, öğe (blok) listelerini filtrelememizi sağlayacak.

`build_blocklist()`
: Tahtadaki tüm blokları tek düzeyli bir liste hâlinde toplar; böylece listeyi filtreleyebiliriz.

Tahta oluşturulduktan sonra tüm blokları içeren iki farklı veri kümesi kullanacağız: `self.blocks` ve `self.board`:

```lua
-- board.script
go.property("timer", 0)     -- Use to time events
local blocksize = 80        -- Distance between block centers
local edge = 40             -- Left and right edge.
local bottom_edge = 50      -- Bottom edge.
local boardwidth = 7        -- Number of columns
local boardheight = 9       -- Number of rows
local centeroff = vmath.vector3(8, -8, 0) -- Center offset for connector gfx since there's shadow below in the block img
local dropamount = 3        -- The number of blocks dropped on a "drop"
local colors = { hash("orange"), hash("pink"), hash("blue"), hash("yellow"), hash("green") }

--
-- filter(function, table)
-- e.g: filter(is_even, {1,2,3,4}) -> {2,4}
--
local function filter(func, tbl)
    local new = {}
    for i, v in pairs(tbl) do
        if func(v) then
            new[i] = v
        end
    end
    return new
end

--
-- Build a list of blocks in 1 dimension for easy filtering
--
local function build_blocklist(self)
    self.blocks = {}
    for x, l in pairs(self.board) do
        for y, b in pairs(self.board[x]) do
            table.insert(self.blocks, { id = b.id, color = b.color, x = b.x, y = b.y })
        end
    end
end

--
-- INIT
--
function init(self)
    self.board = {}             -- Contains the board structure
    self.blocks = {}            -- List of all blocks. Used for easy filtering on selection.
    self.chain = {}             -- Current selection chain
    self.connectors = {}        -- Connector elements to mark the selection chain
    self.num_magic = 3          -- Number of magic blocks on the board
    self.drops = 1              -- Number of drops you have available
    self.magic_blocks = {}      -- Magic blocks that are lined up
    self.dragging = false       -- Drag touch input
    msg.post(".", "acquire_input_focus")
    msg.post("#", "start_level")
end

local function build_board(self)
    math.randomseed(os.time())
    local pos = vmath.vector3()
    local c
    local x = 0
    local y = 0
    for x = 0,boardwidth-1 do
        pos.x = edge + blocksize / 2 + blocksize * x
        self.board[x] = {}
        for y = 0,boardheight-1 do
            pos.y = bottom_edge + blocksize / 2 + blocksize * y
            -- Calc z
            pos.z = x * -0.1 + y * 0.01 -- <1>
            c = colors[math.random(#colors)]    -- Pick a random color
            local id = factory.create("#blockfactory", pos, null, { color = c })
            self.board[x][y] = { id = id, color = c,  x = x, y = y }
        end
    end

    -- Build 1d list that we can easily filter.
    build_blocklist(self)
end

function on_message(self, message_id, message, sender)
    if message_id == hash("start_level") then
        build_board(self)
    end
end
```
1. Blok grafikleri üst üste geldiği için bunları doğru sırada çizmemiz gerektiğine dikkat edin. Bu, her bloğun z koordinatını ayarlayarak yapılır. Değer, arka plan sprite bileşeninin bulunduğu -1'in oldukça üzerinde kalacaktır.

Tahta mantığı, "`blockfactory`" fabrika bileşeni aracılığıyla "`block`" oyun nesneleri oluşturur. Bunun çalışması için blok oyun nesnesini oluşturmamız gerekir. Blokta bir betik ve bir sprite bileşeni bulunur. Sprite bileşeninin varsayılan animasyonunu *`sprites.atlas`* içindeki renkli bloklardan herhangi birine ayarlıyor, ardından blok oluşturulduğunda doğru rengi alması için *`block.script`* dosyasına kod ekliyoruz:

![Blok oyun nesnesi](images/magic-link/linker_block.png)

```lua
-- block.script
go.property("color", hash("none"))

function init(self)
    go.set_scale_xy(0.18)     -- render scaled down without changing Z

    if self.color ~= nil then
        sprite.play_flipbook("#sprite", self.color)
    else
        msg.post("#sprite", "disable")
    end
end
```

"blockfactory" fabrika bileşeninin *Prototype* özelliğini yeni *block.go* oyun nesnesi dosyasına ayarlayın.

![Blok fabrikası](images/magic-link/linker_blockfactory.png)

Artık oyunu çalıştırıp tahtanın rastgele renkli bloklarla dolduğunu görebilmelisiniz:

![İlk ekran görüntüsü](images/magic-link/linker_first_screenshot.png)

## Etkileşimler

Artık bir tahtamız olduğuna göre kullanıcı etkileşimi eklemeliyiz. Önce *input* klasöründeki *game.input_binding* dosyasında girdi eşlemelerini tanımlıyoruz. *game.project* ayarlarının girdi eşlemeleri dosyanızı kullandığından emin olun.

![Girdi eşlemeleri](images/magic-link/linker_input_bindings.png)

Yalnızca bir eşlemeye ihtiyacımız var ve `MOUSE_BUTTON_LEFT` girdisini "touch" eylem adına atıyoruz. Bu oyun çoklu dokunma kullanmaz ve kolaylık sağlamak için Defold tek parmakla dokunma girdisini sol fare tıklamalarına dönüştürür.

Girdiyi işleme görevi tahtaya düştüğünden bunun için *board.script* dosyasına kod eklememiz gerekir:

```lua
-- board.script
function on_input(self, action_id, action)
    if action_id == hash("touch") and action.value == 1 then
        -- What block was touched or dragged over?
        local x = math.floor((action.x - edge) / blocksize)
        local y = math.floor((action.y - bottom_edge) / blocksize)

        if x < 0 or x >= boardwidth or y < 0 or y >= boardheight or self.board[x][y] == nil then
            -- outside board.
            return
        end

        if action.pressed then
            -- Player started touch
            msg.post(self.board[x][y].id, "make_orange")

            self.dragging = true
        elseif self.dragging then
            -- then drag
            msg.post(self.board[x][y].id, "make_green")
        end
    elseif action_id == hash("touch") and action.released then
        -- Player released touch.
        self.dragging = false
    end
end
```

`make_orange` ve `make_green` iletileri (message), kodun çalıştığını görsel olarak doğrulamak için yalnızca geçici olarak kullanılır. Bu iletileri işlemek için *block.script* dosyasına kod eklememiz gerekir:

```lua
-- block.script
function on_message(self, message_id, message, sender)
    if message_id == hash("make_orange") then
        sprite.play_flipbook("#sprite", hash("orange"))
    elseif message_id == hash("make_green") then
        sprite.play_flipbook("#sprite", hash("green"))
    end
end
```

Artık dokunduğunuz (veya fare düğmesini basılı tuttuğunuz) sürece bloklara önce bir `make_orange` iletisi, ardından `make_green` iletileri gönderilecektir. Bu nedenle bloklar yeşile dönmeden önce muhtemelen yalnızca bir anlığına turuncu yanıp söneceklerdir (hatta bu bile olmayabilir). Ancak oyuncunun hangi bloğa dokunduğunu biliyoruz! Girdinin nasıl işlendiğini daha ayrıntılı izlemek isterseniz koda `print()` veya `pprint()` çağrıları ekleyin.

## Bağlantıları işaretleme

Şimdi blokların oyuncu tarafından bağlandığını göstermek için kullanılacak işaretleyicinin varlıklarına ihtiyacımız var. Amaç, her bloğun bağlı olduğunu göstermek için üzerine bir grafik yerleştirmektir.

Bağlayıcının sprite görüntüsünü tutan bir "connector" oyun nesnesi ve "board" oyun nesnesinde bir "connector factory" fabrika bileşeni oluşturmamız gerekir:

![Bağlayıcı oyun nesnesi](images/magic-link/linker_connector.png)

![Bağlayıcı fabrikası](images/magic-link/linker_connector_factory.png)

Bu oyun nesnesinin betiği çok kısadır; yalnızca grafikleri oyunun geri kalanıyla uyumlu olacak şekilde ölçeklemesi ve Z sırasını doğru ayarlaması gerekir.

```lua
-- connector.script
function init(self)
    go.set_scale_xy(0.18)           -- Scale in 2D without changing Z.
    go.set(".", "position.z", 1)    -- Put on top.
end
```

`same_color_neighbors()` işlevi, belirli bir bloğa (x, y konumundaki) komşu olan ve onunla aynı renkteki blokların listesini döndürür. Bu işlev, `self.blocks` içindeki blokların tamamını içeren tek düzeyli listeye uygulanan `filter()` işlevini kullanır.

```lua
-- board.script
--
-- Returns a list of neighbor blocks of the same color as the
-- block on x, y
--
local function same_color_neighbors(self, x, y)
    local f = function (v)
        return (v.id ~= self.board[x][y].id) and
               (v.x == x or v.x == x - 1 or v.x == x + 1) and
               (v.y == y or v.y == y - 1 or v.y == y + 1) and
               (v.color == self.board[x][y].color)
    end
    return filter(f, self.blocks)
end
```

`in_blocklist()` yardımcı işlevi, bir bloğun blok listesinde bulunup bulunmadığını denetler:

```lua
-- board.script
--
-- Does the block exist in the list of blocks?
--
local function in_blocklist(blocks, block)
    for i, b in pairs(blocks) do
        if b.id == block then
            return true
        end
    end
    return false
end
```

Bu işlevleri, dokunarak seçilen blok zincirini oluşturmak için `on_input()` içindeki dokunma ve sürükleme girdileri sırasında kullanıyoruz. Henüz sihirli bloklar bulunmasa da burada onları denetleyip yok sayacağız:

```lua
-- board.script
function on_input(self, action_id, action)

    ...

    -- If trying to manipulate magic blocks, ignore.
    if self.board[x][y].color == hash("magic") then
        return
    end

    if action.pressed then
        -- List of neighbors of the same color as touched block
        self.neighbors = same_color_neighbors(self, x, y)
        self.chain = {}
        table.insert(self.chain, self.board[x][y])

        -- Mark block.
        p = go.get_position(self.board[x][y].id)
        local id = factory.create("#connectorfactory", p + centeroff)
        table.insert(self.connectors, id)

        self.dragging = true
    elseif self.dragging then
        -- then drag
        if in_blocklist(self.neighbors, self.board[x][y].id) and not in_blocklist(self.chain, self.board[x][y].id) then
            -- dragging over a same-colored neighbor
            table.insert(self.chain, self.board[x][y])
            self.neighbors = same_color_neighbors(self, x, y)

            -- Mark block.
            p = go.get_position(self.board[x][y].id)
            local id = factory.create("#connectorfactory", p + centeroff)
            table.insert(self.connectors, id)
        end
    end
```

Son olarak, dokunma bırakıldığında tüm bağlantı işaretlerini görünümden kaldırın.

```lua
-- board.script
function on_input(self, action_id, action)

    ...

    elseif action_id == hash("touch") and action.released then
        -- Player released touch.
        self.dragging = false

        -- Empty chain of connector graphics.
        for i, c in ipairs(self.connectors) do
            go.delete(c)
        end
        self.connectors = {}
    end
end
```

![Oyun içindeki bağlayıcılar](images/magic-link/linker_connector_screen.png)

## Bağlanan blokları kaldırma

Artık aynı renkteki blokların bağlanmasını sağlayan mantık hazır ve bağlanan blokları kaldırmak kolay. Tahtadaki konumu doğrudan `nil` yapmak yerine `hash("removing")` olarak ayarlamamızın nedeni, daha sonra sihirli blok mantığını yazarken sihirli blokların yalnızca yeni kaldırılmış blokların yerine kaymasını sağlamamızın gerekmesidir. Tahtadaki konumu burada `nil` olarak ayarlarsak yeni kaldırılmış bloklarla daha önce kaldırılan blokları ayırt edemeyiz.

```lua
-- board.script
-- Remove the currently selected block-chain
--
local function remove_chain(self)
    -- Delete all chained blocks
    for i, c in ipairs(self.chain) do
        self.board[c.x][c.y] = hash("removing")
        go.delete(c.id)
    end
    self.chain = {}
end
```

Tahtada `hash("removing")` olarak ayarlanmış konumları gerçekten kaldırmak (`nil` yapmak) için de bir işleve ihtiyacımız olacak:

```lua
-- board.script
--
-- Set removed blocks to nil
--
local function nilremoved(self)
    for y = 0,boardheight - 1 do
        for x = 0,boardwidth - 1 do
            if self.board[x][y] == hash("removing") then
                self.board[x][y] = nil
            end
        end
    end
end
```

Ayrıca altlarındaki bloklar kaldırıldığında (`nil` yapıldığında) kalan blokları aşağı kaydıran bir işlev oluşturuyoruz. Tahtayı sütun sütun soldan sağa dolaşıyor ve her sütunu aşağıdan yukarıya inceliyoruz. Boş (`nil`) bir konumla karşılaşırsak bu konumun üzerindeki tüm blokları aşağı kaydırıyoruz.

```lua
-- board.script
--
-- Apply shift-down logic to all blocks.
--
local function slide_board(self)
    -- Slide all remaining blocks down into blank spots.
    -- Going column by column makes this easy.
    local dy = 0
    local pos = vmath.vector3()
    for x = 0,boardwidth - 1 do
        dy = 0
        for y = 0,boardheight - 1 do
            if self.board[x][y] ~= nil then
                if dy > 0 then
                    -- Move down dy steps
                    self.board[x][y - dy] = self.board[x][y]
                    self.board[x][y] = nil
                    -- Calc new position
                    self.board[x][y - dy].y = self.board[x][y - dy].y - dy
                    go.animate(self.board[x][y-dy].id, "position.y", go.PLAYBACK_ONCE_FORWARD, bottom_edge + blocksize / 2 + blocksize * (y - dy), go.EASING_OUTBOUNCE, 0.3)
                    -- Calc new z
                    go.set(self.board[x][y-dy].id, "position.z", x * -0.1 + (y-dy) * 0.01)
                end
            else
                dy = dy + 1
            end
        end
    end
    -- blocklist needs updating
    build_blocklist(self)
end
```

![Blokları aşağı kaydırma](images/magic-link/linker_blocks_slide.png)

Artık dokunma bırakıldığında ve `self.chain` içinde bloklar olduğunda bu işlevleri çağıracak kodu `on_input()` içine ekleyebiliriz.

```lua
-- board.script
function on_input(self, action_id, action)

    ...

    elseif action_id == hash("touch") and action.released then
        -- Player released touch.
        self.dragging = false

        if #self.chain > 1 then
            -- There is a chain of blocks. Remove it from board and slide the remaining blocks down.
            remove_chain(self)
            nilremoved(self)
            slide_board(self)
        end

        -- Empty chain of connector graphics.
        for i, c in ipairs(self.connectors) do
            go.delete(c)
        end
        self.connectors = {}
    end
```

## Sihirli blok mantığı

Şimdi sihirli blokları ekleme zamanı. Öncelikle blokların sihirli bloklara dönüşebilmesini sağlayalım. Böylece doldurulmuş tahtayı ayrı bir geçişte dolaşıp istediğimiz blokları sihirli bloklara dönüştürebiliriz. Sihirli blokları biraz daha ilgi çekici hâle getirmek için önce sihirli bloktan oluşturabileceğimiz *`magic_fx.go`* oyun nesnesi biçiminde animasyonlu bir sihir efekti oluşturalım.

![Magic_fx.go](images/magic-link/linker_magic_fx.png)

Bu oyun nesnesi iki sprite bileşeni içerir. Biri "magic" rengidir (*`magic-sphere_layer2.png`* görüntüsünü kullanan bir sprite bileşeni), diğeri ise "light" adlı bir ışık efektidir (*`magic-sphere_layer3.png`* görüntüsünü kullanan bir sprite bileşeni). Nesne, oluşturulduğunda `direction` özelliğinin değerine bağlı olarak dönecek şekilde ayarlanır. Ayrıca nesnenin, ışık efekti sprite bileşenini denetleyen iki iletiyi dinlemesini sağlarız: `lights_on` ve `lights_off`.

Yeni bir betik oluşturun ve bunu *`magic_fx.go`* nesnesine betik bileşeni olarak ekleyin:

```lua
-- magic_fx.script
go.property("direction", hash("left"))

function init(self)
    msg.post("#", "lights_off")
    if self.direction == hash("left") then
        go.set(".", "euler.z", 0)
        go.animate(".", "euler.z", go.PLAYBACK_LOOP_FORWARD, 360,  go.EASING_LINEAR, 3 + math.random())
    else
        go.set(".", "euler.z", 0)
        go.animate(".", "euler.z", go.PLAYBACK_LOOP_FORWARD, -360,  go.EASING_LINEAR, 2 + math.random())
    end
end

function on_message(self, message_id, message, sender)
    if message_id == hash("lights_on") then
        msg.post("#light", "enable")
    elseif message_id == hash("lights_off") then
        msg.post("#light", "disable")
    end
end
```

Artık sihirli blok, `make_magic` iletisini aldığında iki `magic_fx` oyun nesnesi oluşturacak. Bunların her biri zıt yönde dönerek blokların içinde hoş bir renk dansı yaratacak. Ayrıca *`block.go`* nesnesine *`magic-sphere_layer4.png`* görüntüsünü kullanan ek bir sprite bileşeni ekliyoruz. Bu görüntü, oluşturulan efektinkinden daha yüksek bir Z konumuna yerleştirilir ve sihirli kürenin kabuğunu ya da "cover" adı verilen kapağını çizer.

![Kapak sprite bileşeni](images/magic-link/linker_cover.png)

Blok oyun nesnesine bir *Factory* bileşeni eklememiz ve *Prototype* olarak *`magic_fx.go`* oyun nesnemizi kullanmasını sağlamamız gerektiğine dikkat edin. Blok betiğinin de `lights_on` ve `lights_off` iletilerini dinlemesi ve bunları oluşturulan nesnelere iletmesi gerekir. Blok silindiğinde oluşturulan nesnelerin de silinmesi gerektiğini unutmayın. Bu işlem, bloğun `final()` işlevinde yapılır. Bunların tümü *`block.script`* içinde gerçekleşir.

```lua
-- block.script
function init(self)
    go.set_scale_xy(0.18) -- render scaled down without changing Z

    self.fx1 = nil
    self.fx2 = nil

    msg.post("#cover", "disable")

    if self.color ~= nil then
        sprite.play_flipbook("#sprite", self.color)
    else
        msg.post("#sprite", "disable")
    end
end

function final(self)
    if self.fx1 ~= nil then
        go.delete(self.fx1)
    end

    if self.fx2 ~= nil then
        go.delete(self.fx2)
    end
end

function on_message(self, message_id, message, sender)
    if message_id == hash("make_magic") then
        self.color = hash("magic")
        msg.post("#cover", "enable")
        msg.post("#sprite", "enable")
        sprite.play_flipbook("#sprite", hash("magic-sphere_layer1"))

        self.fx1 = factory.create("#fxfactory", p, nil, { direction = hash("left") })
        self.fx2 = factory.create("#fxfactory", p, nil, { direction = hash("right") })

        go.set_parent(self.fx1, go.get_id())
        go.set_parent(self.fx2, go.get_id())

        go.set(self.fx1, "position.z", 0.01)
        go.set(self.fx1, "scale.xy", 1)
        go.set(self.fx2, "position.z", 0.02)
        go.set(self.fx2, "scale.xy", 1)
    elseif message_id == hash("lights_on") or message_id == hash("lights_off") then
        msg.post(self.fx1, message_id)
        msg.post(self.fx2, message_id)
    end
end
```

Artık sihirli bloklar oluşturabilir ve ışıklarını yakabiliriz. Bu efekti, bir sihirli bloğun başka bir sihirli bloğun yanında bulunduğunu göstermek için kullanacağız.

![Işığı kapalı ve açık sihirli blok](images/magic-link/linker_magic_blocks.png)

Tahtayı bloklarla dolduran kodu, tahtaya bazı sihirli bloklar da ekleyecek şekilde değiştirmemiz gerekiyor:

```lua
-- board.script
local function build_board(self)

    ...

    -- Distribute magic blocks.
    local rand_x = 0
    local rand_y
    for y = 0, boardheight - 1, boardheight / self.num_magic do
        local set = false
        while not set do
            rand_y = math.random(math.floor(y), math.min(boardheight - 1, math.floor(y + boardheight / self.num_magic)))
            rand_x = math.random(0, boardwidth - 1)
            if self.board[rand_x][rand_y].color ~= hash("magic") then
                msg.post(self.board[rand_x][rand_y].id, "make_magic")
                self.board[rand_x][rand_y].color = hash("magic")
                set = true
            end
        end
    end

    -- Build 1d list that we can easily filter.
    build_blocklist(self)
end
```

Sihirli blokların temel mekaniği, yanlarındaki başka bir blok kaybolduğunda yana kayabilmeleridir. Bu mekaniğin tüm ayrıntılarını *board.script* içindeki `slide_magic_blocks()` işlevine yansıtıyoruz. Algoritma basittir:

1. Tahtadaki her satır için sihirli blokları içeren bir `M` listesi oluşturun.
2. `M` listesi küçülmeyi bırakana kadar listedeki her sihirli bloğu dolaşın. Her yinelemede:
    1. Sihirli bloğun altında `hash("removing")` değerine sahip bir blok konumu varsa bloğu yalnızca `M` listesinden kaldırın.
    2. Sihirli bloğun yanında `hash("removing")` olarak işaretlenmiş bir boşluk varsa bloğu oraya kaydırın, eski konumunu `hash("removing")` olarak ayarlayın ve ardından `M` listesinden kaldırın.

```lua
-- board.script
-- Apply the shifting logic to magic blocks. Only slide to positions
-- marked for removal with hash("removing")
--
local function slide_magic_blocks(self)
    -- Slide all magic blocks to the side that should slide first.
    -- This works best going row by row!
    local row_m
    for y = 0,boardheight - 1 do
        row_m = {}
        -- Build list of magic blocks on this row.
        for x = 0,boardwidth - 1 do
            if self.board[x][y] ~= nil and self.board[x][y] ~= hash("removing") and self.board[x][y].color == hash("magic") then
                table.insert(row_m, self.board[x][y])
            end
        end

        local mc = #row_m + 1
        -- Go through list, slide and remove if possible. Reiterate until the list does not shrink.
        while #row_m < mc do
            mc = #row_m
            for i, m in pairs(row_m) do
                local x = m.x
                if y > 0 and self.board[x][y-1] == hash("removing") then
                    -- Hole below, do nothing.
                    row_m[i] = nil
                elseif x > 0 and self.board[x-1][y] == hash("removing") then
                    -- Hole to the left! Slide magic block there
                    self.board[x-1][y] = self.board[x][y]
                    self.board[x-1][y].x = x - 1
                    go.animate(self.board[x][y].id, "position.x", go.PLAYBACK_ONCE_FORWARD, edge + blocksize / 2 + blocksize * (x - 1), go.EASING_OUTBOUNCE, 0.3)
                    -- Calc new z
                    go.set(self.board[x][y].id, "position.z", (x - 1) * -0.1 + y * 0.01)
                    self.board[x][y] = hash("removing") -- Will be nilled later
                    row_m[i] = nil
                elseif x < boardwidth - 1 and self.board[x + 1][y] == hash("removing") then
                    -- Hole to the right. Slide magic block there
                    self.board[x+1][y] = self.board[x][y]
                    self.board[x+1][y].x = x + 1
                    go.animate(self.board[x+1][y].id, "position.x", go.PLAYBACK_ONCE_FORWARD, edge + blocksize / 2 + blocksize * (x + 1), go.EASING_OUTBOUNCE, 0.3)
                    -- Calc new z
                    go.set(self.board[x+1][y].id, "position.z", (x + 1) * -0.1 + y * 0.01)
                    self.board[x][y] = hash("removing") -- Will be nilled later
                    row_m[i] = nil
                end
            end
        end
    end
end
```

`on_input()` içinde bu işlevi çağırarak mekaniği deneyebiliriz:

```lua
-- board.script
function on_input(self, action_id, action)

    ...

    elseif action_id == hash("touch") and action.released then
        -- Player released touch.
        self.dragging = false

        if #self.chain > 1 then
            -- There is a chain of blocks. Remove it from board
            remove_chain(self)
            slide_magic_blocks(self)
            nilremoved(self)
            -- Slide remaining blocks down.
            slide_board(self)
        end
        self.chain = {}
        -- Empty chain clears connector graphics.
        for i, c in ipairs(self.connectors) do
            go.delete(c)
        end
        self.connectors = {}
    end
```

Artık konumları kaldırırken neden ara bir `hash("removing")` "etiketi" kullandığımızı açıkça görüyoruz. Bu etiket olmasaydı sihirli bloklar yanlarındaki herhangi bir boş konuma ileri geri kayardı. Belki ilginç bir mekanik olurdu, ancak bu küçük oyun için amaçladığımız mekanik bu değil.

Şimdi sihirli blokların birbirine bağlı olup olmadığını (birbirlerinin solunda, sağında, üstünde veya altında bulunup bulunmadığını) algılayan bir mantığa ihtiyacımız var. Ayrıca tahtadaki tüm sihirli blokların birbirine bağlı olup olmadığını bilmemiz gerekiyor. Kullanılan algoritma oldukça basittir:

1. Tahtadaki tüm sihirli blokları içeren bir `M` listesi oluşturun.
2. `M` listesindeki her blok için:
    1. Bloğun `region` değeri ayarlanmamışsa ona `R` bölge numarasını atayın (başlangıçta `1`).
    2. Bloğun işaretlenmemiş tüm komşularını aynı `R` bölge numarasıyla işaretleyin ve onların komşularına, o komşuların komşularına ve bu şekilde devam edin.
    3. `R` bölge numarasını `1` artırın.

![Bölgeleri işaretleme](images/magic-link/linker_regions.png)

Algoritmanın uygulaması şöyledir:

```lua
-- board.script
--
-- Build list of all current magic blocks.
--
local function magic_blocks(self)
    local magic = {}
    for x = 0,boardwidth - 1 do
        for y = 0,boardheight - 1 do
            if self.board[x][y] ~= nil and self.board[x][y].color == hash("magic") then
                table.insert(magic, self.board[x][y])
            end
        end
    end
    return magic
end

--
-- Filter out adjacent magic blocks
--
local function adjacent_magic_blocks(blocks, block)
    return filter(function (e)
        return (block.x == e.x and math.abs(block.y - e.y) == 1) or
            (block.y == e.y and math.abs(block.x - e.x) == 1)
    end, blocks)
end

--
-- Spread region to neighbors
--
local function mark_neighbors(blocks, block, region)
    local neighbors = adjacent_magic_blocks(blocks, block)
    for i, m in pairs(neighbors) do
        if m.region == nil then
            m.region = region
            mark_neighbors(blocks, m, region)
        end
    end
end

--
-- Mark all magic block regions
--
local function mark_magic_regions(self)
    local m_blocks = magic_blocks(self)
    -- 1. Clear all region marks and count neighbors
    for i, m in pairs(m_blocks) do
        m.region = nil
        local n = 0
        for _ in pairs(adjacent_magic_blocks(m_blocks, m)) do n = n + 1 end
        m.neighbors = n
    end

    -- 2. Assign regions and spread them
    local region = 1
    for i, m in pairs(m_blocks) do
        if m.region == nil then
            m.region = region
            mark_neighbors(m_blocks, m, region)
            region = region + 1
        end
    end
    return m_blocks
end
```

Sihirli bloklar arasındaki bölgelerin sayısını hesaplamamızı sağlayan işlevler de oluşturuyoruz. Bölge sayısı 1 ise tüm sihirli blokların birbirine bağlı olduğunu biliriz. Ayrıca tüm sihirli blokların ışıklarını kapatan bir işlev ve komşusunda sihirli blok bulunan sihirli blokların ışık efektlerini açan bir işlev ekliyoruz:

```lua
-- board.script
--
-- Count the number of connected regions among the magic blocks.
--
local function count_magic_regions(blocks)
    local maxr = 0
    for i, m in pairs(blocks) do
        if m.region > maxr then
            maxr = m.region
        end
    end
    return maxr
end

--
-- Shut off lights on all listed magic blocks
--
local function shutdown_lined_up_magic(self)
    for i, m in ipairs(self.lined_up_magic) do
        msg.post(m.id, "lights_off")
    end
end

--
-- Set highlight for all magic blocks
--
local function highlight_magic(blocks)
    for i, m in pairs(blocks) do
        if m.neighbors > 0 then
            msg.post(m.id, "lights_on")
        else
            msg.post(m.id, "lights_off")
        end
    end
end
```

Artık bu mantık parçalarını genel akışa ekleyebiliriz. Öncelikle tahta rastgele oluşturulduğu için küçük de olsa kazanılmış durumda başlama olasılığı vardır. Bu olursa tahtayı silip yeniden oluştururuz:

```lua
-- board.script
--
-- Clear the board
--
local function clear_board(self)
    for y = 0,boardheight - 1 do
        for x = 0,boardwidth - 1 do
            if self.board[x][y] ~= nil then
                go.delete(self.board[x][y].id)
                self.board[x][y] = nil
            end
        end
    end
end

local function build_board(self)

    ...

    -- Build 1d list that we can easily filter.
    build_blocklist(self)

    local magic_blocks = mark_magic_regions(self)
    if count_magic_regions(magic_blocks) == 1 then
        -- "Win" from start. Make new board.
        clear_board(self)
        build_board(self)
    end
    highlight_magic(magic_blocks)
end
```

Mantığın geri kalanı `on_input()` içine sığar. `level_completed` iletisini işleyen kod hâlâ yok, ancak şimdilik bu sorun değil:

```lua
-- board.script
function on_input(self, action_id, action)

    ...

    elseif action_id == hash("touch") and action.released then
        -- Player released touch.
        self.dragging = false

        if #self.chain > 1 then
            -- There is a chain of blocks. Remove it from board and refill board.
            remove_chain(self)
            slide_magic_blocks(self)
            nilremoved(self)
            -- Slide remaining blocks down.
            slide_board(self)

            local magic_blocks = mark_magic_regions(self)
            -- Highlight adjacent magic blocks.
            if count_magic_regions(magic_blocks) == 1 then
                -- Win!
                msg.post("#", "level_completed")
            end
            highlight_magic(magic_blocks)
        end
        self.chain = {}
        -- Empty chain clears connector graphics.
        for i, c in ipairs(self.connectors) do
            go.delete(c)
        end
        self.connectors = {}
    end
```

Tüm sihirli blokları bağladığınızda henüz hiçbir şey olmasa da artık oyunu oynamak ve kazanma durumuna ulaşmak mümkün.

![İlk kazanma](images/magic-link/linker_first_win.png)

## Blok bırakma

"Blok bırakma" (drop) fikrinin amacı basit bir ilerleme mekaniği eklemektir. Oyuncu *DROP* düğmesine basarak sınırlı sayıda "blok bırakma" işlemi yapabilir; bu işlem tahtaya yukarıdan birkaç yeni rastgele parça bırakır. Oyuncu bir blok bırakma hakkıyla başlar ve her bölüm tamamlandığında ek bir hak kazanır. Blok bırakma mekaniğinin kodu iki işleve sığar. Biri blokların yerleşebileceği olası konumların listesini döndürür; diğeri ise animasyonu ve diğer ayrıntılarıyla blok bırakma işlemini gerçekleştirir.

```lua
-- board.script
--
-- Find spots for a drop.
--
local function dropspots(self)
    local spots = {}
    for x = 0, boardwidth - 1 do
        for y = 0, boardheight - 1 do
            if self.board[x][y] == nil then
                table.insert(spots, { x = x, y = y })
                break
            end
        end
    end
    -- If more than dropamount, randomly remove a slot until dropamount
    for c = 1, #spots - dropamount do
        table.remove(spots, math.random(#spots))
    end
    return spots
end

--
-- Perform the drop
--
local function drop(self, spots)
    for i, s in pairs(spots) do
        local pos = vmath.vector3()
        pos.x = edge + blocksize / 2 + blocksize * s.x
        pos.y = 1000
        c = colors[math.random(#colors)]    -- Pick a random color
        local id = factory.create("#blockfactory", pos, null, { color = c })
        go.animate(id, "position.y", go.PLAYBACK_ONCE_FORWARD, bottom_edge + blocksize / 2 + blocksize * s.y, go.EASING_OUTBOUNCE, 0.5)
        -- Calc new z
        go.set(id, "position.z", s.x * -0.1 + s.y * 0.01)

        self.board[s.x][s.y] = { id = id, color = c,  x = s.x, y = s.y }
    end

    -- Rebuild blocklist
    build_blocklist(self)
end
```

Aşağıdaki kodu örneğin `on_reload()` içinde çalıştırarak veya geçici bir girdi eylemine bağlayarak blok bırakmayı test edebiliriz:

```lua
s = dropspots(self)
if #s > 0 then
    -- Do the drop
    drop(self, s)
end
```

![Blok bırakma](images/magic-link/linker_drop.png)

## Ana menü

Şimdi her şeyi bir araya getirme zamanı. Öncelikle bir başlangıç ekranı oluşturup bunu tahtadan ayıralım. İlk adım, bir *main_menu.gui* dosyası oluşturup içine bir *Start* düğmesi (bir metin düğümü ve dokulu bir kutu düğümü), bir başlık metni düğümü ve birkaç dekoratif blok (dokulu kutu düğümleri) yerleştirmektir. GUI'ye bağladığımız *main_menu.gui_script* betiği, `init()` içinde dekoratif bloklara animasyon uygular. Ayrıca ana betiğe `start_game` iletisi gönderen bir `on_input()` işlevi içerir. O betiği birazdan oluşturacağız.

![Ana menü GUI'si](images/magic-link/linker_main_menu.png)

```lua
-- main_menu.gui_script
function init(self)
    msg.post(".", "acquire_input_focus")

    local bs = { "brick1", "brick2", "brick3", "brick4", "brick5", "brick6" }
    for i, b in ipairs(bs) do
        local n = gui.get_node(b)
        local rt = (math.random() * 3) + 1
        local a = math.random(-45, 45)
        gui.set_color(n, vmath.vector4(1, 1, 1, 0))

        gui.animate(n, "position.y", -100 - math.random(0, 50), gui.EASING_INSINE, 1 + rt, 0, nil, gui.PLAYBACK_LOOP_FORWARD)
        gui.animate(n, "color.w", 1, gui.EASING_INSINE, 1 + rt, 0, nil, gui.PLAYBACK_LOOP_FORWARD)
        gui.animate(n, "rotation.z", a, gui.EASING_INSINE, 1 + rt, 0, nil, gui.PLAYBACK_LOOP_FORWARD)
    end

    gui.animate(gui.get_node("start"), "color.x", 1, gui.EASING_INOUTSINE, 1, 0, nil, gui.PLAYBACK_LOOP_PINGPONG)
end

function on_input(self, action_id, action)
    if action_id == hash("touch") and action.pressed then
        local start = gui.get_node("start")

        if gui.pick_node(start, action.x, action.y) then
            msg.post("/main#script", "start_game")
        end
    end
end
```

Oyunu başlatma görevini yakında ana menü betiği üstleneceği için *board.script* içindeki `init()` işlevinden geçici tahta hazırlama çağrısını kaldırın:

```lua
-- board.script
--
-- INIT
--
function init(self)
    self.board = {}                -- Contains the board structure
    self.blocks = {}            -- List of all blocks. Used for easy filtering on selection.

    self.chain = {}                -- Current selection chain
    self.connectors = {}        -- Connector elements to mark the selection chain
    self.num_magic = 3            -- Number of magic blocks on the board

    self.drops = 1                -- Number of drops you have available

    self.magic_blocks = {}        -- Magic blocks that are lined up

    self.dragging = false        -- Drag touch input
end
```

Ana betik oyunun genel durumunu tutacak ve istendiğinde oyunu başlatacak. Burada *main.collection* dosyasının, başlangıçta göstermemiz gereken en az miktarda varlığı içermesini istiyoruz. Bunu, *main.collection* içine ana menü GUI'sini, bir betik bileşenini ve en önemlisi bir *Collection Proxy* bileşenini barındıran "main" oyun nesnesini koyarak yapıyoruz.

Koleksiyon vekili (collection proxy), çalışan oyuna koleksiyonları dinamik olarak yüklememizi ve bunları bellekten kaldırmamızı sağlar. Belirtilen bir koleksiyon dosyası adına hareket eder; vekile ileti göndererek dinamik koleksiyonu yükler, başlangıç işlemlerini yapar, etkinleştirir, devre dışı bırakır ve bellekten kaldırırız. Koleksiyon vekillerinin kullanımına ilişkin eksiksiz açıklama için [koleksiyon vekili belgelerine](/manuals/collection-proxy) bakın.

Bu örnekte koleksiyon vekili bileşeninin *Collection* özelliğini, "bölümü" içeren *board.collection* dosyasına ayarlıyoruz.

![Ana koleksiyon](images/magic-link/linker_main_collection.png)

Şimdi *game.project* dosyasını açıp başlangıç koleksiyonunu (bootstrap collection) belirleyen *main_collection* ayarını `/main/main.collectionc` olarak değiştirmeliyiz.

![Başlangıçtaki ana koleksiyon](images/magic-link/linker_bootstrap_main.png)

Artık oyunu başlatmak, tahtayı yüklemesi, başlangıç işlemlerini yapması ve etkinleştirmesi için koleksiyon vekilimize ileti göndermek, ardından ana menüyü (görünmemesi için) devre dışı bırakmak anlamına gelir. Ana menüye dönmek ise bu işlemleri tersine çevirir (vekilin koleksiyonu yüklemiş olması koşuluyla).

```lua
-- main.script
function init(self)
    msg.post("#", "to_main_menu")
    self.state = "MAIN_MENU"
end

function on_message(self, message_id, message, sender)
    if message_id == hash("to_main_menu") then
        if self.state ~= "MAIN_MENU" then
            msg.post("#boardproxy", "unload")
        end
        msg.post("main:/main#menu", "enable") -- <1>
        self.state = "MAIN_MENU"
    elseif message_id == hash("start_game") then
        msg.post("#boardproxy", "load")
        msg.post("#menu", "disable")
    elseif message_id == hash("proxy_loaded") then
        -- Board collection has loaded...
        msg.post(sender, "init")
        msg.post("board:/board#script", "start_level", { difficulty = 1 }) -- <2>
        msg.post(sender, "enable")
        self.state = "GAME_RUNNING"
    end
end
```
1. Sokete (socket) "main" adını verdiğimize dikkat edin; *main.collection* içinde bu adı ayarladığımızdan emin olmamız gerekir. Kök düğümü seçin ve *Name* özelliğinin "main" olduğunu denetleyin.
2. Benzer şekilde, yüklenen koleksiyona iletileri koleksiyonun *Name* özelliği aracılığıyla adlandırılan soketi üzerinden göndeririz.

## Oyun içi GUI

Tahta betiğine mantığın son parçasını eklemeden önce tahtaya bir dizi GUI öğesi eklemeliyiz. Önce tahtanın üst kısmına bir *RESTART* düğmesi ve bir *DROP* düğmesi ekliyoruz.

![Tahta GUI'si](images/magic-link/linker_board_gui.png)

Tahta GUI'sinin betiği, yeniden başlatma düğmesine tıklandığında yeniden başlatma GUI iletişim kutusuna, *DROP* düğmesine tıklandığında ise tahta betiğinin kendisine ileti gönderir:

```lua
-- board.gui_script
function init(self)
    msg.post("#", "show")
    msg.post("/restart#gui", "hide")
    msg.post("/level_complete#gui", "hide")
end

function on_message(self, message_id, message, sender)
    if message_id == hash("hide") then
        msg.post("#", "disable")
    elseif message_id == hash("show") then
        msg.post("#", "enable")
    elseif message_id == hash("set_drop_counter") then
        local n = gui.get_node("drop_counter")
        gui.set_text(n, message.drops .. " x")
    end
end

function on_input(self, action_id, action)
    if action_id == hash("touch") and action.pressed then
        local restart = gui.get_node("restart")
        local drop = gui.get_node("drop")

        if gui.pick_node(restart, action.x, action.y) then
            -- Show the restart dialog box.
            msg.post("/restart#gui", "show")
            msg.post("#", "hide")
        elseif gui.pick_node(drop, action.x, action.y) then
            msg.post("/board#script", "drop")
        end
    end
end
```

*RESTART* iletişim kutusu basittir. Bunu *restart.gui* olarak oluşturup oyuncu *NO* seçeneğine tıkladığında hiçbir şey yapmayan, *YES* seçeneğine tıkladığında tahta betiğine `restart_level` iletisi ve *Quit to main menu* seçeneğine tıkladığında ana betiğe `to_main_menu` iletisi gönderen basit bir betik ekliyoruz:

![Yeniden başlatma GUI'si](images/magic-link/linker_restart_gui.png)

```lua
-- restart.gui_script
function on_message(self, message_id, message, sender)
    if message_id == hash("hide") then
        msg.post("#", "disable")
        msg.post(".", "release_input_focus")
    elseif message_id == hash("show") then
        msg.post("#", "enable")
        msg.post(".", "acquire_input_focus")
    end
end

function on_input(self, action_id, action)
    if action_id == hash("touch") and action.pressed then
        local yes = gui.get_node("yes")
        local no = gui.get_node("no")
        local quit = gui.get_node("quit")

        if gui.pick_node(no, action.x, action.y) then
            msg.post("#", "hide")
            msg.post("/board#gui", "show")
        elseif gui.pick_node(yes, action.x, action.y) then
            msg.post("board:/board#script", "restart_level")
            msg.post("/board#gui", "show")
            msg.post("#", "hide")
        elseif gui.pick_node(quit, action.x, action.y) then
            msg.post("main:/main#script", "to_main_menu")
            msg.post("#", "hide")
        end
    end
    -- Consume all input until we're gone.
    return true
end
```

Ayrıca *level_complete.gui* içinde bölümün tamamlanması için basit bir GUI iletişim kutusu oluşturuyor ve oyuncu *CONTINUE* seçeneğine tıkladığında tahta betiğine `next_level` iletisi gönderen basit bir betik ekliyoruz:

![Bölüm tamamlandı iletişim kutusu](images/magic-link/linker_level_complete_gui.png)

```lua
-- level_complete.gui_script
function init(self)
    msg.post("#", "hide")
end

function on_message(self, message_id, message, sender)
    if message_id == hash("hide") then
        msg.post("#", "disable")
        msg.post(".", "release_input_focus")
    elseif message_id == hash("show") then
        msg.post("#", "enable")
        msg.post(".", "acquire_input_focus")
    end
end

function on_input(self, action_id, action)
    if action_id == hash("touch") and action.pressed then
        local continue = gui.get_node("continue")

        if gui.pick_node(continue, action.x, action.y) then
            msg.post("board#script", "next_level")
            msg.post("#", "hide")
        end
    end
    -- Consume all input until we're gone.
    return true
end
```

Geçerli bölümü tanıtmak için kullanılan bir iletişim kutusu ve yalnızca kutuyu gizleme ile gösterme işlemlerini içeren bir betik oluşturuyoruz. Gösterildiğinde iletişim kutusunun metni, geçerli zorluk düzeyini içerecek şekilde ayarlanır:

![Bölümü tanıtan GUI](images/magic-link/linker_present_level_gui.png)

```lua
-- present_level.gui_script
function init(self)
    msg.post("#", "hide")
end

function on_message(self, message_id, message, sender)
    if message_id == hash("hide") then
        msg.post("#", "disable")
    elseif message_id == hash("show") then
        local n = gui.get_node("message")
        gui.set_text(n, "Level " .. message.level)
        msg.post("#", "enable")
    end
end
```

Oyuncu blok bırakmaya çalıştığında buna yer yoksa gösterilen bir iletişim kutusu da ekliyoruz.

![Blok bırakacak yer olmadığını gösteren GUI](images/magic-link/linker_no_drop_room_gui.png)

```lua
-- no_drop_room.gui_script
function init(self)
    msg.post("#", "hide")
    self.t = 0
end

function update(self, dt)
    if self.t < 0 then
        msg.post("#", "hide")
    else
        self.t = self.t - dt
    end
end

function on_message(self, message_id, message, sender)
    if message_id == hash("hide") then
        msg.post("#", "disable")
    elseif message_id == hash("show") then
        self.t = 1
        msg.post("#", "enable")
    end
end
```

Son olarak bu GUI bileşenlerini *board.collection* içine ve gerekli kodu *board.script* içine ekliyoruz:

![Son tahta koleksiyonu](images/magic-link/linker_board_collection_final.png)

Tahtaya gönderilen ve tahtadan gelen tüm iletiler için `on_message()` içinde kod yazmamız gerekiyor.

`start_level`
: Sihirli blokların sayısını zorluk parametresine göre ayarlayın, tahtayı oluşturun ve ardından oyunu başlatmadan (iletişim kutusunu kaldırıp girdi odağını almadan) önce "present_level" GUI iletişim kutusunu 2 saniye boyunca gösterin. Başka hiçbir amaçla kullanılmayan "timer" değerine animasyon uygulayarak `go.animate()` işlevini zamanlayıcı olarak kullandığımıza dikkat edin.

`restart_level`
: Oyuncu *RESTART* GUI düğmesine basıp onayladığında bu gerçekleşir. Tahtayı temizleyip yeniden oluşturun ve blok bırakma sayacını başlangıç değerine döndürün.

`level_completed`
: Tahta kazanma durumuna ulaşır ulaşmaz gönderilir. Girdiyi kapatın, sihirli bloklara animasyon uygulayın ve "level_complete" GUI iletişim kutusunu gösterin. Oyuncu iletişim kutusundaki *CONTINUE* düğmesine tıkladığında kutu yanıt olarak bir `next_level` iletisi gönderecektir.

`next_level`
: Bu ileti alındığında tahtayı temizleyin, blok bırakma sayacını artırın ve bir sonraki zorluk düzeyi ayarlanmış olarak `start_level` iletisini gönderin.

`drop`
: Blok bırakılabilecek yerleri denetleyin. Uygun konum yoksa "no_drop_room" GUI iletişim kutusunu gösterin. Aksi takdirde blok bırakma işlemini gerçekleştirin (oyuncunun hakkı kaldıysa), blok bırakma sayacını azaltın ve sayacın görsel gösterimini güncelleyin.

```lua
-- board.script
function on_message(self, message_id, message, sender)
    if message_id == hash("start_level") then
        self.num_magic = message.difficulty + 1
        build_board(self)

        msg.post("#gui", "set_drop_counter", { drops = self.drops } )

        msg.post("present_level#gui", "show", { level = message.difficulty } )
        -- Wait some...
        go.animate("#", "timer", go.PLAYBACK_ONCE_FORWARD, 1, go.EASING_LINEAR, 2, 0, function ()
            msg.post("present_level#gui", "hide")
            msg.post(".", "acquire_input_focus")
        end)
    elseif message_id == hash("restart_level") then
        clear_board(self)
        build_board(self)
        self.drops = 1
        msg.post("#gui", "set_drop_counter", { drops = self.drops } )
        msg.post(".", "acquire_input_focus")
    elseif message_id == hash("level_completed") then
        -- turn off input
        msg.post(".", "release_input_focus")

        -- Animate the magic!
        for i, m in ipairs(magic_blocks(self)) do
            go.set_scale_xy(0.17, m.id)
            go.animate(m.id, "scale.xy", go.PLAYBACK_LOOP_PINGPONG, 0.19, go.EASING_INSINE, 0.5, 0)
        end

        -- Show completion screen
        msg.post("level_complete#gui", "show")
    elseif message_id == hash("next_level") then
        clear_board(self)
        self.drops = self.drops + 1
        -- Difficulty level is number of magic blocks - 1
        msg.post("#", "start_level", { difficulty = self.num_magic })
    elseif message_id == hash("drop") then
        s = dropspots(self)
        if #s == 0 then
            -- Can't perform drop
            msg.post("no_drop_room#gui", "show")
        elseif self.drops > 0 then
            -- Do the drop
            drop(self, s)
            self.drops = self.drops - 1
            msg.post("#gui", "set_drop_counter", { drops = self.drops } )
        end
    end
end
```

İşte bu kadar! Oyun ve bu öğretici artık tamamlandı! Oyunun tadını çıkarın!

![Tamamlanan oyun](images/magic-link/linker_game_finished.png)

## Devam etmek için

Bu küçük oyunun bazı ilginç özellikleri var ve üzerinde denemeler yapmanızı öneririz. Defold'a daha fazla alışmak için yapabileceğiniz alıştırmaların listesi şöyledir:

* Etkileşimi daha anlaşılır hâle getirin. Yeni bir oyuncu oyunun nasıl çalıştığını ve nelerle etkileşime girebileceğini anlamakta zorlanabilir. Öğretici öğeler eklemeden oyunu daha anlaşılır kılmaya biraz zaman ayırın.
* Ses ekleyin. Oyun şu anda tamamen sessiz; hoş bir müzik ve etkileşim sesleri oyunu iyileştirebilir.
* Oyunun bittiğini otomatik olarak algılayın.
* En yüksek puan. Kalıcı bir en yüksek puan özelliği ekleyin.
* Oyunu yalnızca GUI API'lerini kullanarak yeniden geliştirin.
* Şu anda oyun, her yeni bölümde bir sihirli blok ekleyerek devam ediyor. Bu sonsuza kadar sürdürülemez. Bu soruna tatmin edici bir çözüm bulun.
* Oyunu optimize edin ve sprite bileşenlerini silip yeniden oluşturmak yerine yeniden kullanarak en fazla sprite sayısını azaltın.
* Oyunun farklı çözünürlüklere ve en boy oranlarına sahip ekranlarda aynı derecede iyi görünmesi için çözünürlükten bağımsız işleme uygulayın.
