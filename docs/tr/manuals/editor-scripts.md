---
title: Düzenleyici betikleri
brief: Bu kılavuz, Lua kullanarak düzenleyiciyi nasıl genişleteceğinizi açıklar
---

# Düzenleyici betikleri

`.editor_script` özel uzantısına sahip Lua dosyalarını kullanarak özel menü öğeleri ve düzenleyici yaşam döngüsü kancaları (lifecycle hooks) oluşturabilirsiniz. Bu düzenleyici betiği (editor script) sistemiyle geliştirme iş akışınızı iyileştirmek için düzenleyiciyi özelleştirebilirsiniz.

## Düzenleyici betiklerinin çalışma zamanı ortamı

Düzenleyici betikleri, düzenleyicinin içinde, Java sanal makinesinin öykündüğü bir Lua sanal makinesinde çalışır. Tüm betikler tek bir ortak ortamı paylaşır; yani birbirleriyle etkileşim kurabilirler. Tıpkı `.script` dosyalarında olduğu gibi Lua modüllerini `require` ile yükleyebilirsiniz, ancak düzenleyicinin içinde çalışan Lua sürümü farklıdır; bu nedenle ortak kodunuzun uyumlu olduğundan emin olun. Düzenleyici Lua 5.2.x sürümünü, daha özel olarak da şu anda JVM üzerinde Lua çalıştırmak için uygulanabilir tek çözüm olan [luaj](https://github.com/luaj/luaj) çalışma zamanı ortamını kullanır. Bunun yanında bazı kısıtlamalar vardır:
- `debug` paketi yoktur;
- `os.execute` yoktur, ancak benzer bir işlev olan `editor.execute()` sunulur;
- `os.tmpname` ve `io.tmpfile` yoktur — düzenleyici betikleri şu anda yalnızca proje dizininin içindeki dosyalara erişebilir;
- eklemek istesek de şu anda `os.rename` yoktur;
- `os.exit` ve `os.setlocale` yoktur.
- düzenleyicinin betikten anında yanıt alması gereken bağlamlarda uzun süren bazı işlevlerin kullanılmasına izin verilmez; ayrıntılar için [Yürütme modları](#execution-modes) bölümüne bakın.

Bir projeyi açtığınızda düzenleyici betiklerinde tanımlanan tüm düzenleyici uzantıları yüklenir. Kütüphaneleri getirdiğinizde uzantılar yeniden yüklenir; çünkü bağımlı olduğunuz kütüphanelerde yeni düzenleyici betikleri bulunabilir. Bu yeniden yükleme sırasında kendi düzenleyici betiklerinizdeki değişiklikler alınmaz; çünkü bunları değiştirmeyi henüz bitirmemiş olabilirsiniz. Bunları da yeniden yüklemek için **Project → Reload Editor Scripts** komutunu çalıştırmanız önerilir.

## `.editor_script` dosyasının yapısı

Her düzenleyici betiği aşağıdaki gibi bir modül döndürmelidir:
```lua
local M = {}

function M.get_commands()
  -- TODO - define editor commands
end

function M.get_language_servers()
  -- TODO - define language servers
end

function M.get_prefs_schema()
  -- TODO - define preferences
end

return M
```
Düzenleyici daha sonra projede ve kütüphanelerde tanımlanan tüm düzenleyici betiklerini toplar, bunları tek bir Lua sanal makinesine yükler ve gerektiğinde çağırır (bu konuda daha fazla bilgi [komutlar](#commands) ve [yaşam döngüsü kancaları](#lifecycle-hooks) bölümlerindedir).

## Düzenleyici API'si

Aşağıdaki API'yi tanımlayan `editor` paketini kullanarak düzenleyiciyle etkileşim kurabilirsiniz:
- `editor.platform` — Windows için `"x86_64-win32"`, macOS için `"x86_64-macos"` veya Linux için `"x86_64-linux"` değerini alan bir dize.
- `editor.version` — Defold sürüm adını içeren bir dize; örneğin `"1.4.8"`
- `editor.engine_sha1` — Defold motorunun SHA1 değerini içeren bir dize
- `editor.editor_sha1` — Defold düzenleyicisinin SHA1 değerini içeren bir dize
- `editor.get(node_id, property)` — düzenleyicideki bir düğümün (node) değerini alır. Düzenleyicideki düğümler; betik veya koleksiyon (collection) dosyaları, koleksiyonların içindeki oyun nesneleri (game objects), kaynak (resource) olarak yüklenen JSON dosyaları gibi çeşitli öğelerdir. `node_id`, düzenleyici tarafından düzenleyici betiğine iletilen bir userdata değeridir. Alternatif olarak düğüm kimliği yerine bir kaynak yolu, örneğin `"/main/game.script"`, iletebilirsiniz. `property` bir dizedir. Şu anda aşağıdaki özellikler desteklenir:
  - `"path"` — dosya veya dizin olarak var olan öğeler, yani *kaynaklar* için proje klasörüne göre dosya yolu. Döndürülen değere örnek: `"/main/game.script"`
  - `"children"` — dizin kaynakları için alt kaynak yollarının listesi
  - `"parent"` — üst düğümü olan bir Outline düğümünün üst düzenleyici düğümü
  - `"text"` — metin olarak düzenlenebilen bir kaynağın (betik veya JSON dosyaları gibi) metin içeriği. Döndürülen değere örnek: `"function init(self)\nend"`. Bunun dosyayı `io.open()` ile okumakla aynı olmadığını unutmayın; çünkü bir dosyayı kaydetmeden düzenleyebilirsiniz ve bu düzenlemelere yalnızca `"text"` özelliğine erişildiğinde ulaşılabilir.
  - atlaslar için: `images` (atlastaki görüntülere ait düzenleyici düğümlerinin listesi) ve `animations` (animasyon düğümlerinin listesi)
  - atlas animasyonları için: `images` (atlastaki `images` ile aynı)
  - karo haritaları (tilemaps) için: `layers` (karo haritasındaki katmanlara ait düzenleyici düğümlerinin listesi)
  - karo haritası katmanları için: `tiles` (sınırsız bir 2B karo ızgarası); daha fazla bilgi için `tilemap.tiles.*` bölümüne bakın
  - parçacık efektleri için: `emitters` (yayıcı düzenleyici düğümlerinin listesi) ve `modifiers` (değiştirici düzenleyici düğümlerinin listesi)
  - parçacık efekti yayıcıları için: `modifiers` (değiştirici düzenleyici düğümlerinin listesi)
  - çarpışma nesneleri için: `shapes` (çarpışma şekli düzenleyici düğümlerinin listesi)
  - GUI dosyaları için: `layers`, `fonts`, `materials`, `textures`, `particlefxs`, `nodes` ve `layouts` gibi düğüm listeleri
  - Outline görünümünde bir şey seçtiğinizde Properties görünümünde gösterilen bazı özellikler. Şu türdeki Outline özellikleri desteklenir:
    - `strings`
    - `booleans`
    - `numbers`
    - `vec2`/`vec3`/`vec4`
    - `resources`
    - `curves`
    Bu özelliklerden bazılarının salt okunur olabileceğini ve bazılarının farklı bağlamlarda kullanılamayabileceğini unutmayın. Bu nedenle bunları okumadan önce `editor.can_get`, düzenleyicide ayarlamadan önce de `editor.can_set` kullanmanız önerilir. Özelliğin düzenleyici betiklerindeki adını açıklayan araç ipucunu görmek için Properties görünümünde özellik adının üzerine gelin. `""` değerini vererek kaynak özelliklerini `nil` olarak ayarlayabilirsiniz.
- `editor.properties(node_id)` — bir düğümden okunabilen özellik adlarının sıralanmış, bağlama duyarlı bir listesini döndürür; örneğin `pprint(editor.properties("/game.project"))`. Listelenen bir özelliğin ayrıca değiştirilip değiştirilemeyeceğini, sıfırlanıp sıfırlanamayacağını, ona öğe eklenip eklenemeyeceğini veya öğelerinin yeniden sıralanıp sıralanamayacağını denetlemek için `editor.can_*` işlevlerini kullanın.
- `editor.can_get(node_id, property)` — `editor.get()` işlevinin hata vermemesi için bu özelliği alıp alamayacağınızı denetler.
- `editor.can_set(node_id, property)` — bu özellik ile kullanılan `editor.tx.set()` düzenleyici işlemi (transaction) adımının hata vermeyeceğini denetler.
- `editor.create_directory(resource_path)` — bir dizin yoksa onu ve var olmayan tüm üst dizinlerini oluşturur.
- `editor.create_resources(resources)` — şablonlardan veya özel içerikle 1 ya da daha fazla kaynak oluşturur
- `editor.delete_directory(resource_path)` — bir dizin varsa onu ve var olan tüm alt dizinlerini ve dosyalarını siler.
- `editor.execute(cmd, [...args], [options])` — bir kabuk komutu çalıştırır; isteğe bağlı olarak çıktısını yakalar.
- `editor.save()` — kaydedilmemiş tüm değişiklikleri diske kaydeder.
- `editor.transact(txs)` — `editor.tx.*` işlevleriyle oluşturulan 1 veya daha fazla işlem adımını kullanarak düzenleyicinin bellekteki durumunu değiştirir.
- `editor.ui.*` — kullanıcı arayüzüyle ilgili çeşitli işlevler; [Kullanıcı arayüzü kılavuzuna](/manuals/editor-scripts-ui) bakın.
- `editor.prefs.*` — düzenleyici tercihleriyle etkileşim kurma işlevleri; [tercihler](#preferences) bölümüne bakın.

Düzenleyici API'sinin tüm başvuru belgelerini [burada](/ref/stable/editor/) bulabilirsiniz.

## Komutlar {#commands}

Bir düzenleyici betiği modülü `get_commands()` tanımlıyorsa uzantılar yeniden yüklendiğinde bu işlev çağrılır. Döndürülen komutlar, `locations` değerlerine bağlı olarak menü çubuğu menülerinde ve Assets, Outline, Scene ve Code bağlam menülerinde görünebilir. Örnek:

```lua
local M = {}

function M.get_commands()
  return {
    {
      label = "Remove Comments",
      locations = {"Edit", "Assets"},
      query = {
        selection = {type = "resource", cardinality = "one"}
      },
      active = function(opts)
        local path = editor.get(opts.selection, "path")
        return ends_with(path, ".lua") or ends_with(path, ".script")
      end,
      run = function(opts)
        local text = editor.get(opts.selection, "text")
        editor.transact({
          editor.tx.set(opts.selection, "text", strip_comments(text))
        })
      end
    },
    {
      label = "Minify JSON",
      locations = {"Assets"},
      query = {
        selection = {type = "resource", cardinality = "one"}
      },
      active = function(opts)
        return ends_with(editor.get(opts.selection, "path"), ".json")
      end,
      run = function(opts)
        local path = editor.get(opts.selection, "path")
        editor.execute("./scripts/minify-json.sh", path:sub(2))
      end
    }
  }
end

return M
```
Düzenleyici, `get_commands()` işlevinin her biri ayrı bir komutu açıklayan tablolardan oluşan bir dizi döndürmesini bekler. Komut açıklaması şunlardan oluşur:

- `label` (zorunlu) — kullanıcıya gösterilecek menü öğesinin metni
- `locations` (zorunlu) — bu komutun nerelerde kullanılabilmesi gerektiğini açıklayan bir dizi. Desteklenen değerler; ilgili menü çubuğu menüleri için `"Edit"`, `"View"`, `"Project"`, `"Debug"` ve `"Help"`; **Project → Bundle** alt menüsü için `"Bundle"`; ilgili bağlam menüleri için de `"Assets"`, `"Outline"`, `"Scene"` ve `"Code"` değerleridir.
- `query` — komutun düzenleyiciden ilgili bilgileri istemesini ve hangi veriler üzerinde çalıştığını tanımlamasını sağlar. `query` tablosundaki her anahtar için `active` ve `run` geri çağırımlarının (callbacks) bağımsız değişken olarak aldığı `opts` tablosunda karşılık gelen bir anahtar bulunur. Desteklenen anahtarlar:
  - `selection`, bu komutun bir şey seçili olduğunda geçerli olduğunu ve bu seçim üzerinde çalıştığını belirtir.
    - `type`, komutun ilgilendiği seçili düğümlerin türüdür; şu anda aşağıdaki türlere izin verilir:
      - `"resource"` — Assets ve Outline görünümlerinde kaynak, karşılık gelen bir dosyası olan seçili öğedir. Menü çubuğunda (Edit veya View) kaynak, o anda açık olan dosyadır;
      - `"outline"` — Outline görünümünde gösterilebilen bir öğe. Outline görünümünde seçili öğedir; menü çubuğunda ise o anda açık olan dosyadır;
      - `"scene"` — Scene görünümünde görüntüsü oluşturulabilen bir öğe.
    - `cardinality`, kaç öğenin seçili olması gerektiğini tanımlar. `"one"` ise komut geri çağırımına iletilen seçim tek bir düğüm kimliği olur. `"many"` ise komut geri çağırımına iletilen seçim, bir veya daha fazla düğüm kimliğinden oluşan bir dizi olur.
  - `active_view`, etkin düzenleyici görünümü istenen türle eşleştiğinde bu komutun geçerli olduğunu belirtir. Etkin görünüm, komut geri çağırımına `opts.active_view` olarak iletilir.
    - `type`, komutun ilgilendiği etkin görünüm türüdür: `"code"`, `"scene"`, `"html"` veya `"form"`.
    - Etkin görünüm `"type"`, `"resource"` ve `"dirty"` özelliklerini destekler. Görünümde gösterilen kaynağı almak için `editor.get(view, "resource")`, kaydedilmemiş değişiklikleri olup olmadığını denetlemek için de `editor.get(view, "dirty")` kullanın.
  - `argument` — komut bağımsız değişkeni. Şu anda yalnızca `"Bundle"` konumundaki komutlar bir bağımsız değişken alır. Bu değer, paketleme komutu açıkça seçildiğinde `true`, yeniden paketleme sırasında ise `false` olur.
- `id` - komut tanımlayıcısı dizesi; örneğin son kullanılan paketleme komutunu `prefs` içinde kalıcı olarak saklamak için kullanılır
- `active` - komutun etkin olup olmadığını denetlemek için yürütülen ve mantıksal değer döndürmesi beklenen bir geri çağırım. `locations` içinde `"Assets"`, `"Scene"` veya `"Outline"` varsa `active`, bağlam menüsü gösterilirken çağrılır. Konumlar arasında `"Edit"` veya `"View"` varsa active, klavyede yazma veya fareyle tıklama gibi her kullanıcı etkileşiminde çağrılır; bu nedenle `active` geri çağırımının nispeten hızlı olduğundan emin olun.
- `run` - kullanıcı menü öğesini seçtiğinde yürütülen bir geri çağırım.

### Düzenleyicinin bellekteki durumunu değiştirmek için komutları kullanma

`run` işleyicisinin içinde, düzenleyicinin bellekteki durumunu sorgulayabilir ve değiştirebilirsiniz. Sorgulama, `editor.get()` işleviyle yapılır; bu işlevle düzenleyiciye dosyaların ve seçimin (`query = {selection = ...}` kullanıyorsanız) geçerli durumunu sorabilirsiniz. Metin olarak düzenlenebilen kaynakların `"text"` özelliğini ve Properties görünümünde gösterilen bazı özellikleri alabilirsiniz — özelliğin düzenleyici betiklerindeki adını açıklayan araç ipucunu görmek için özellik adının üzerine gelin. Düzenleyicinin durumunu değiştirmek için `editor.transact()` kullanılır; bu işlevle 1 veya daha fazla değişikliği geri alınabilen tek bir adımda birleştirirsiniz. Örneğin bir oyun nesnesinin dönüşümünü sıfırlayabilmek istiyorsanız şöyle bir komut yazabilirsiniz:
```lua
{
  label = "Reset transform",
  locations = {"Outline"},
  query = {selection = {type = "outline", cardinality = "one"}},
  active = function(opts)
    local node = opts.selection
    return editor.can_set(node, "position") 
       and editor.can_set(node, "rotation") 
       and editor.can_set(node, "scale")
  end,
  run = function(opts)
    local node = opts.selection
    editor.transact({
      editor.tx.set(node, "position", {0, 0, 0}),
      editor.tx.set(node, "rotation", {0, 0, 0}),
      editor.tx.set(node, "scale", {1, 1, 1})
    })
  end
}
```

### Etkin düzenleyici görünümüyle komutları kullanma

`"View"` gibi menü konumlarındaki komutlar, o anda etkin olan düzenleyici görünümünü sorgulayabilir. Bu, bir komutun kullanıcının o anda baktığı dosya veya sahne üzerinde çalışması gerektiğinde yararlıdır:

```lua
editor.command({
  label = "Print Active View",
  locations = {"View"},
  query = {active_view = {type = "code"}},
  run = function(opts)
    local view = opts.active_view
    local resource = editor.get(view, "resource")
    print(editor.get(view, "type"))
    print(editor.get(resource, "path"))
    print(editor.get(view, "dirty"))
  end
})
```

#### Atlasları düzenleme

Bir atlasın özelliklerini okuyup yazmanın yanı sıra atlas görüntülerini ve animasyonlarını da okuyabilir ve değiştirebilirsiniz. Atlaslar `images` ve `animations` düğüm listesi özelliklerini, animasyonlar ise `images` düğüm listesi özelliğini tanımlar: bu özelliklerle `editor.tx.add`, `editor.tx.remove` ve `editor.tx.clear` işlem adımlarını kullanabilirsiniz.

Örneğin bir atlasa görüntü eklemek için komutun `run` işleyicisinde aşağıdaki kodu yürütün:
```lua
editor.transact({
    editor.tx.add("/main.atlas", "images", {image="/assets/hero.png"})
})
```
Bir atlastaki tüm görüntülerin kümesini bulmak için aşağıdaki kodu yürütün:
```lua
local all_images = {} ---@type table<string, true>
-- first, collect all "bare" images
local image_nodes = editor.get("/main.atlas", "images")
for i = 1, #image_nodes do
    all_images[editor.get(image_nodes[i], "image")] = true
end
-- second, collect all images used in animations
local animation_nodes = editor.get("/main.atlas", "animations")
for i = 1, #animation_nodes do
    local animation_image_nodes = editor.get(animation_nodes[i], "images")
    for j = 1, #animation_image_nodes do
        all_images[editor.get(animation_image_nodes[j], "image")] = true
    end
end
pprint(all_images)
-- {
--     ["/assets/hero.png"] = true,
--     ["/assets/enemy.png"] = true,
-- }}
```
Bir atlastaki tüm animasyonları değiştirmek için:
```lua
editor.transact({
    editor.tx.clear("/main.atlas", "animations"),
    editor.tx.add("/main.atlas", "animations", {
        id = "hero_run",
        images = {
            {image = "/assets/hero_run_1.png"},
            {image = "/assets/hero_run_2.png"},
            {image = "/assets/hero_run_3.png"},
            {image = "/assets/hero_run_4.png"}
        }
    })
})
```

#### Karo kaynaklarını düzenleme

Karo kaynakları (tile sources), Outline özelliklerine ek olarak aşağıdaki özellikleri tanımlar:
- `animations` - karo kaynağının animasyon düğümlerinin listesi
- `collision_groups` - karo kaynağının çarpışma grubu düğümlerinin listesi
- `tile_collision_groups` - karo kaynağındaki karoların çarpışma grubu atamalarını içeren tablo

Örneğin bir karo kaynağını şöyle yapılandırabilirsiniz:
```lua
local tilesource = "/game/world.tilesource"
editor.transact({
    editor.tx.add(tilesource, "animations", {id = "idle", start_tile = 1, end_tile = 1}),
    editor.tx.add(tilesource, "animations", {id = "walk", start_tile = 2, end_tile = 6, fps = 10}),
    editor.tx.add(tilesource, "collision_groups", {id = "player"}),
    editor.tx.add(tilesource, "collision_groups", {id = "obstacle"}),
    editor.tx.set(tilesource, "tile_collision_groups", {
        [1] = "player",
        [7] = "obstacle",
        [8] = "obstacle"
    })
})
```

#### Karo haritalarını düzenleme

Karo haritaları, karo haritası katmanlarının düğüm listesi olan `layers` özelliğini tanımlar. Her katman ayrıca, bu katmandaki sınırsız bir 2B karo ızgarasını tutan `tiles` özelliğini tanımlar. Bu, motordan farklıdır: karoların sınırları yoktur ve negatif koordinatlar dahil her yere eklenebilirler. Düzenleyici betiği API'si, karoları düzenlemek için aşağıdaki işlevleri içeren `tilemap.tiles` modülünü tanımlar:
- `tilemap.tiles.new()`, sınırsız bir 2B karo ızgarasını tutan yeni bir veri yapısı oluşturur (motorun aksine, düzenleyicide karo haritası sınırsızdır ve koordinatlar negatif olabilir)
- `tilemap.tiles.get_tile(tiles, x, y)`, belirli bir koordinattaki karo indeksini alır
- `tilemap.tiles.get_info(tiles, x, y)`, belirli bir koordinattaki karo bilgilerinin tamamını alır (veri yapısı, motorun `tilemap.get_tile_info` işlevindekiyle aynıdır)
- `tilemap.tiles.iterator(tiles)`, karo haritasındaki tüm karoları dolaşan bir yineleyici oluşturur
- `tilemap.tiles.clear(tiles)`, karo haritasındaki tüm karoları kaldırır
- `tilemap.tiles.set(tiles, x, y, tile_or_info)`, belirli bir koordinattaki karoyu ayarlar
- `tilemap.tiles.remove(tiles, x, y)`, belirli bir koordinattaki karoyu kaldırır

Örneğin tüm karo haritasının içeriğini şöyle yazdırabilirsiniz:
```lua
local layers = editor.get("/level.tilemap", "layers")
for i = 1, #layers do
    local layer = layers[i]
    local id = editor.get(layer, "id")
    local tiles = editor.get(layer, "tiles")
    print("layer " .. id .. ": {")
    for x, y, tile in tilemap.tiles.iterator(tiles) do
        print("  [" .. x .. ", " .. y .. "] = " .. tile)
    end
    print("}")
end
```

Aşağıdaki örnek, bir karo haritasına karolar içeren bir katmanın nasıl eklendiğini gösterir:
```lua
local tiles = tilemap.tiles.new()
tilemap.tiles.set(tiles, 1, 1, 2)
editor.transact({
    editor.tx.add("/level.tilemap", "layers", {
        id = "new_layer",
        tiles = tiles
    })
})
```

#### Parçacık efektlerini düzenleme

Parçacık efektlerini `modifiers` ve `emitters` özelliklerini kullanarak düzenleyebilirsiniz. Örneğin ivme değiştiricisi içeren bir daire yayıcı şöyle eklenir:
```lua
editor.transact({
    editor.tx.add("/fire.particlefx", "emitters", {
        type = "emitter-type-circle",
        modifiers = {
          {type = "modifier-type-acceleration"}
        }
    })
})
```
Birçok parçacık efekti özelliği, eğri veya yayılımlı eğri (curve spread; yani eğri + bir rastgelelik değeri) biçimindedir. Eğriler, boş olmayan bir `points` listesi içeren tablo olarak gösterilir; listedeki her nokta, aşağıdaki özellikleri içeren bir tablodur:
- `x` - noktanın x koordinatı; 0 ile başlayıp 1 ile bitmesi önerilir
- `y` - noktanın değeri
- `tx` (0 ile 1 arasında) ve `ty` (-1 ile 1 arasında) - noktanın teğetleri. Örneğin 80 derecelik bir açı için `tx` değerinin `math.cos(math.rad(80))`, `ty` değerinin ise `math.sin(math.rad(80))` olması önerilir.
Yayılımlı eğriler ayrıca sayısal bir `spread` özelliğine sahiptir. 

Örneğin mevcut bir yayıcı için parçacığın yaşam süresi boyunca alfa değerini belirleyen eğriyi ayarlamak şöyle görünebilir:
```lua
local emitter = editor.get("/fire.particlefx", "emitters")[1]
editor.transact({
    editor.tx.set(emitter, "particle_key_alpha", { points = {
        {x = 0,   y = 0, tx = 0.1, ty = 1}, -- start at 0, go up quickly
        {x = 0.2, y = 1, tx = 1,   ty = 0}, -- reach 1 at 20% of a lifetime
        {x = 1,   y = 0, tx = 1,   ty = 0}  -- slowly go down to 0
    }})
})
```
Elbette, bir yayıcı oluştururken tablodaki `particle_key_alpha` anahtarını kullanmak da mümkündür. Ayrıca "statik" bir eğriyi göstermek için bunun yerine tek bir sayı kullanabilirsiniz.

#### Çarpışma nesnelerini düzenleme

Çarpışma nesneleri, varsayılan Outline özelliklerine ek olarak `shapes` düğüm listesi özelliğini tanımlar. Yeni çarpışma şekilleri şöyle eklenir:
```lua
editor.transact({
    editor.tx.add("/hero.collisionobject", "shapes", {
        type = "shape-type-box" -- or "shape-type-sphere", "shape-type-capsule"
    })
})
```
Şeklin `type` özelliği oluşturma sırasında zorunludur ve şekil eklendikten sonra değiştirilemez. 3 şekil türü vardır:
- `shape-type-box` - `dimensions` özelliği olan kutu şekli
- `shape-type-sphere` - `diameter` özelliği olan küre şekli
- `shape-type-capsule` - `diameter` ve `height` özellikleri olan kapsül şekli

#### GUI dosyalarını düzenleme

GUI dosyaları, Outline özelliklerine ek olarak birkaç düğüm listesi özelliği tanımlar:

- `layers` — katman düzenleyici düğümlerinin listesi (yeniden sıralanabilir)
- `fonts` — yazı tipi düzenleyici düğümlerinin listesi
- `materials` — materyal düzenleyici düğümlerinin listesi
- `textures` — doku düzenleyici düğümlerinin listesi
- `particlefxs` — Particle FX düzenleyici düğümlerinin listesi
- `nodes` — GUI düğümlerine ait düzenleyici düğümlerinin listesi
- `layouts` — GUI yerleşimi düzenleyici düğümlerinin listesi

Düzenleyicinin `layers` özelliğini kullanarak GUI katmanlarını düzenleyebilirsiniz; örneğin:
```lua
editor.transact({
    editor.tx.add("/main.gui", "layers", {name = "foreground"}),
    editor.tx.add("/main.gui", "layers", {name = "background"})
})
```
Ayrıca katmanları yeniden sıralamak da mümkündür:
```lua
local fg, bg = table.unpack(editor.get("/main.gui", "layers"))
editor.transact({
    editor.tx.reorder("/main.gui", "layers", {bg, fg})
})
```
Benzer şekilde yazı tipleri, materyaller, dokular ve parçacık efektleri; `fonts`, `materials`, `textures` ve `particlefxs` özellikleri kullanılarak düzenlenir:
```lua
editor.transact({
    editor.tx.add("/main.gui", "fonts", {font = "/main.font"}),
    editor.tx.add("/main.gui", "materials", {name = "shine", material = "/shine.material"}),
    editor.tx.add("/main.gui", "particlefxs", {particlefx = "/confetti.particlefx"}),
    editor.tx.add("/main.gui", "textures", {texture = "/ui.atlas"})
})
```
Bu özellikler yeniden sıralamayı desteklemez.

Son olarak `nodes` liste özelliğini kullanarak GUI düğümlerini düzenleyebilirsiniz; örneğin:
```lua
editor.transact({
    editor.tx.add("/main.gui", "nodes", {
        type = "gui-node-type-box",
        position = {20, 20, 20}
    }),
    editor.tx.add("/main.gui", "nodes", {
        type = "gui-node-type-template",
        template = "/button.gui"
    }),
})
```
Yerleşik düğüm türleri şunlardır:
- `gui-node-type-box`
- `gui-node-type-particlefx`
- `gui-node-type-pie`
- `gui-node-type-template`
- `gui-node-type-text`

Spine uzantısını kullanıyorsanız `gui-node-type-spine` düğüm türünü de kullanabilirsiniz.

GUI dosyası yerleşimler tanımlıyorsa `layout:property` sözdizimini kullanarak yerleşimlerdeki değerleri alabilir ve ayarlayabilirsiniz; örneğin:
```lua
local node = editor.get("/main.gui", "nodes")[1]

-- GET:
local position = editor.get(node, "position")
pprint(position) -- {20, 20, 20}
local landscape_position = editor.get(node, "Landscape:position")
pprint(landscape_position) -- {20, 20, 20}

-- SET:
editor.transact({
    editor.tx.set(node, "Landscape:position", {30, 30, 30})
})
pprint(editor.get(node, "Landscape:position")) -- {30, 30, 30}
```

Ayarlanmış yerleşim özellikleri, `editor.tx.reset` kullanılarak varsayılan değerlerine sıfırlanabilir:
```lua
print(editor.can_reset(node, "Landscape:position")) -- true
editor.transact({
    editor.tx.reset(node, "Landscape:position")
})
```
Şablon düğüm ağaçları okunabilir, ancak düzenlenemez — yalnızca şablon düğüm ağacındaki düğümlerin özelliklerini ayarlayabilirsiniz:
```lua
local template = editor.get("/main.gui", "nodes")[2]
print(editor.can_add(template, "nodes")) -- false
local node_in_template = editor.get(template, "nodes")[1]
editor.transact({
    editor.tx.set(node_in_template, "text", "Button text")
})
print(editor.can_reset(node_in_template, "text")) -- true (overrides a value in the template)
```

#### Oyun nesnelerini düzenleme

Düzenleyici betiklerini kullanarak bir oyun nesnesi dosyasının bileşenlerini (components) düzenleyebilirsiniz. Bileşenler 2 çeşittir: başvuru yoluyla eklenen (referenced) ve gömülü (embedded). Başvuru yoluyla eklenen bileşenler `component-reference` türünü kullanır ve diğer kaynaklara başvuru görevi görür; yalnızca betiklerde tanımlanan oyun nesnesi özelliklerinin geçersiz kılınmasına izin verir. Gömülü bileşenler `sprite`, `label` vb. türleri kullanır. Bileşen türünde tanımlanan tüm özelliklerin düzenlenmesine ve çarpışma nesnelerinin şekilleri gibi alt bileşenlerin eklenmesine izin verir. Örneğin bir oyun nesnesini yapılandırmak için aşağıdaki kodu kullanabilirsiniz:
```lua
editor.transact({
    editor.tx.add("/npc.go", "components", {
        type = "sprite",
        id = "view"
    }),
    editor.tx.add("/npc.go", "components", {
        type = "collisionobject",
        id = "collision",
        shapes = {
            {
                type = "shape-type-box",
                dimensions = {32, 32, 32}
            }
        }
    }),
    editor.tx.add("/npc.go", "components", {
        type = "component-reference",
        path = "/npc.script",
        id = "controller",
        __hp = 100 -- set a go property defined in the script
    })
})
```

#### Koleksiyonları düzenleme
Düzenleyici betiklerini kullanarak koleksiyonları düzenleyebilirsiniz. Oyun nesneleri (gömülü veya başvuru yoluyla) ve koleksiyonlar (başvuru yoluyla) ekleyebilirsiniz. Örneğin:
```lua
local coll = "/char.collection"
editor.transact({
    editor.tx.add(coll, "children", {
        -- embbedded game object
        type = "go",
        id = "root",
        children = {
            {
                -- referenced game object
                type = "go-reference",
                path = "/char-view.go",
                id = "view"
            },
            {
                -- referenced collection
                type = "collection-reference",
                path = "/body-attachments.collection",
                id = "attachments"
            }
        },
        -- embedded gos can also have components
        components = {
            {
                type = "collisionobject",
                id = "collision",
                shapes = {
                    {type = "shape-type-box", dimensions = {2.5, 2.5, 2.5}}
                }
            },
            {
                type = "component-reference",
                id = "controller",
                path = "/char.script",
                __hp = 100 -- set a go property defined in the script
            }
        }
    })
})
```

Düzenleyicide olduğu gibi, başvuru yoluyla eklenen koleksiyonlar yalnızca düzenlenen koleksiyonun köküne eklenebilir. Oyun nesneleri ise yalnızca gömülü veya başvuru yoluyla eklenen oyun nesnelerine eklenebilir; başvuru yoluyla eklenen koleksiyonlara ya da bu koleksiyonların içindeki oyun nesnelerine eklenemez.

### Kabuk komutlarını kullanma

`run` işleyicisinin içinde dosyalara yazabilir (`io` modülünü kullanarak) ve kabuk komutları yürütebilirsiniz (`editor.execute()` komutunu kullanarak). Kabuk komutları yürütülürken bir kabuk komutunun çıktısını dize olarak yakalayıp kodda kullanmak mümkündür. Örneğin sistem genelinde kurulu [`jq`](https://jqlang.github.io/jq/) programını kabuk üzerinden çağırarak JSON biçimlendiren bir komut oluşturmak istiyorsanız aşağıdaki komutu yazabilirsiniz:
```lua
{
  label = "Format JSON",
  locations = {"Assets"},
  query = {selection = {type = "resource", cardinality = "one"}},
  action = function(opts)
    local path = editor.get(opts.selection, "path")
    return path:match(".json$") ~= nil
  end,
  run = function(opts)
    local text = editor.get(opts.selection, "text")
    local new_text = editor.execute("jq", "-n", "--argjson", "data", text, "$data", {
      reload_resources = false, -- don't reload resources since jq does not touch disk
      out = "capture" -- return text output instead of nothing
    })
    editor.transact({ editor.tx.set(opts.selection, "text", new_text) })
  end
}
```
Bu komut kabuk programını salt okunur biçimde çağırdığı (ve `reload_resources = false` kullanarak düzenleyiciye bunu bildirdiği) için bu eylemi geri alınabilir hale getirmenin avantajından yararlanırsınız.

::: sidenote
Düzenleyici betiğinizi kütüphane olarak dağıtmak istiyorsanız düzenleyicinin çalıştığı platformlar için ikili programı bağımlılığın içinde paketlemek isteyebilirsiniz. Bunun nasıl yapılacağına ilişkin ayrıntılar için [Kütüphanelerdeki düzenleyici betikleri](#editor-scripts-in-libraries) bölümüne bakın.
:::

## Yaşam döngüsü kancaları {#lifecycle-hooks}

Özel olarak ele alınan bir düzenleyici betiği dosyası vardır: projenizin kökünde, *game.project* ile aynı dizinde bulunan `hooks.editor_script`. Düzenleyiciden yaşam döngüsü olaylarını yalnızca bu düzenleyici betiği alır. Böyle bir dosyaya örnek:
```lua
local M = {}

function M.on_build_started(opts)
  local file = io.open("assets/build.json", "w")
  file:write('{"build_time": "' .. os.date() .. '"}')
  file:close()
end

return M
```
Yaşam döngüsü kancalarını tek bir düzenleyici betiği dosyasıyla sınırlamaya karar verdik; çünkü derleme kancalarının gerçekleşme sırası, yeni bir derleme adımı eklemenin kolaylığından daha önemlidir. Komutlar birbirinden bağımsızdır, bu nedenle menüde hangi sırayla gösterildiklerinin pek önemi yoktur; sonuçta kullanıcı seçtiği belirli bir komutu yürütür. Farklı düzenleyici betiklerinde derleme kancaları belirtmek mümkün olsaydı şu sorun ortaya çıkardı: kancalar hangi sırayla yürütülür? Büyük olasılıkla içeriğin sağlama toplamlarını onu sıkıştırdıktan sonra oluşturmak istersiniz... Her adımın işlevini açıkça çağırarak derleme adımlarının sırasını belirleyen tek bir dosyaya sahip olmak, bu sorunu çözmenin bir yoludur.

`/hooks.editor_script` dosyasının belirtebileceği mevcut yaşam döngüsü kancaları:
- `on_build_started(opts)` — oyun, Project Build veya Debug Start seçeneklerinden biri kullanılarak yerel olarak ya da uzak bir hedefte çalıştırılmak üzere derlendiğinde yürütülür. Değişiklikleriniz derlenen oyuna yansır. Bu kancanın hata vermesi derlemeyi durdurur. `opts`, aşağıdaki anahtarları içeren bir tablodur:
  - `platform` — hangi platform için derlendiğini açıklayan, `%arch%-%os%` biçiminde bir dize; şu anda her zaman `editor.platform` ile aynı değerdir.
- `on_build_finished(opts)` — başarılı veya başarısız olmasına bakılmaksızın derleme bittiğinde yürütülür. `opts`, aşağıdaki anahtarları içeren bir tablodur:
  - `platform` — `on_build_started` içindekiyle aynı
  - `success` — derlemenin başarılı olup olmadığı; `true` veya `false`
- `on_bundle_started(opts)` — bir dağıtım paketi (bundle) oluşturduğunuzda veya oyunun HTML5 sürümünü derlediğinizde yürütülür. `on_build_started` için olduğu gibi, bu kancanın tetiklediği değişiklikler dağıtım paketine yansır ve hatalar paketlemeyi durdurur. `opts` şu anahtarlara sahip olur:
  - `output_directory` — dağıtım paketi çıktısını içeren dizini gösteren bir dosya yolu. **Project ▸ Build HTML5**, `build/default` altındaki normal Build çıktısından ayrı olarak kendi çıktı ağacını, örneğin `"/path/to/project/build/default_html5/__htmlLaunchDir"` yolunu kullanır.
  - `platform` — oyunun hangi platform için paketlendiği. Olası platform değerlerinin listesi için [Bob kılavuzuna](/manuals/bob) bakın.
  - `variant` — dağıtım paketi çeşidi; `"debug"`, `"release"` veya `"headless"`
- `on_bundle_finished(opts)` — başarılı olup olmamasına bakılmaksızın paketleme bittiğinde yürütülür. `opts`, `on_bundle_started` içindeki `opts` ile aynı verileri ve ayrıca derlemenin başarılı olup olmadığını belirten `success` anahtarını içeren bir tablodur.
- `on_target_launched(opts)` — kullanıcı bir oyunu başlattığında ve oyun başarıyla çalışmaya başladığında yürütülür. `opts`, başlatılmış motor hizmetini gösteren bir `url` anahtarı içerir; örneğin `"http://127.0.0.1:35405"`
- `on_target_terminated(opts)` — başlatılmış oyun kapatıldığında yürütülür; `on_target_launched` ile aynı opts değerine sahiptir

Yaşam döngüsü kancalarının şu anda yalnızca düzenleyicide kullanılabilen bir özellik olduğunu ve komut satırından paketleme yapılırken Bob tarafından yürütülmediğini unutmayın.

## Dil sunucuları

Düzenleyici, [Dil Sunucusu Protokolü'nün](https://microsoft.github.io/language-server-protocol/) (Language Server Protocol) bir alt kümesini destekler: tanılama (statik kod denetimleri), tamamlama, üzerine gelindiğinde gösterilen bilgiler, Structure bölmesinde belge simgeleri, tanıma gitme, başvuruları bulma, simgeyi yeniden adlandırma ve belgeyi/aralığı biçimlendirme. Dil sunucusundan gelen bilgileri görmek için bir simgenin üzerine gelin. İmleç bir simgenin üzerindeyken simgeyi yeniden adlandırmak için <kbd>F2</kbd>, tanımına gitmek için <kbd>F12</kbd> veya başvurularını bulmak için <kbd>Shift+F12</kbd> kullanın. Bu eylemlere <kbd>Edit</kbd> menüsünden de erişebilirsiniz. Biçimlendirme komutu ve kaydederken biçimlendirme tercihi için [kod biçimlendirme](/manuals/writing-code/#formatting-code) bölümüne bakın.

Birlikte gelen Lua dil sunucusu, çalışma zamanı ve düzenleyici betiği API'leri için Defold tür ek açıklamalarını içerir. `.editor_script` dosyalarında tamamlama ve tanılama, `editor.*` işlevlerini ve bunların bağımsız değişken ve dönüş türlerini tanır. [Kod tamamlama](/manuals/writing-code/#code-completion) bölümüne bakın.

Ek bir dil sunucusu kaydetmek için düzenleyici betiğinizin `get_language_servers` işlevini şöyle tanımlayın:

```lua
function M.get_language_servers()
  local command = 'build/plugins/my-ext/plugins/bin/' .. editor.platform .. '/lua-lsp'
  if editor.platform == 'x86_64-win32' then
    command = command .. '.exe'
  end
  return {
    {
      languages = {'lua'},
      watched_files = {
        { pattern = '**/.luacheckrc' }
      },
      command = {command, '--stdio'}
    }
  }
end
```
Düzenleyici, belirtilen `command` değerini kullanarak dil sunucusunu başlatır ve iletişim için sunucu sürecinin standart girdisini ve çıktısını kullanır.

Dil sunucusu tanım tablosunda şunlar belirtilebilir:
- `languages` (zorunlu) — sunucunun ilgilendiği, [burada](https://code.visualstudio.com/docs/languages/identifiers#_known-language-identifiers) tanımlanan dillerin listesi (dosya uzantıları da kullanılabilir);
- `command` (zorunlu) - komuttan ve bağımsız değişkenlerinden oluşan bir dizi
- `watched_files` - sunucunun [izlenen dosyalar değişti](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#workspace_didChangeWatchedFiles) bildirimini tetikleyecek `pattern` anahtarlarını (glob kalıbı) içeren tablolardan oluşan bir dizi.

## HTTP sunucusu {#http-server}

Düzenleyicinin çalışan her örneğinde (instance) bir HTTP sunucusu çalışır. Sunucu, düzenleyici betikleri kullanılarak genişletilebilir. Düzenleyici HTTP sunucusunu genişletmek için `get_http_server_routes` düzenleyici betiği işlevini eklemeniz gerekir — bu işlev ek rotaları döndürmelidir:
```lua
print("My route: " .. http.server.url .. "/my-extension")

function M.get_http_server_routes()
  return {
    http.server.route("/my-extension", "GET", function(request)
      return http.server.response(200, "Hello world!")
    end)
  }
end
```
Düzenleyici betiklerini yeniden yükledikten sonra konsolda şu çıktıyı görürsünüz: `My route: http://0.0.0.0:12345/my-extension`. Bu bağlantıyı tarayıcıda açarsanız `"Hello world!"` iletinizi görürsünüz.

Girdi olarak alınan `request` bağımsız değişkeni, istek hakkında bilgi içeren basit bir Lua tablosudur. `path` (`/` ile başlayan URL yol bölümü), isteğin `method` değeri (örneğin `"GET"`), `headers` (küçük harfli üstbilgi adlarını içeren bir tablo) ve isteğe bağlı olarak `query` (sorgu dizesi) ve `body` (rota, gövdenin nasıl yorumlanacağını tanımlıyorsa) gibi anahtarlar içerir. Örneğin JSON gövdesi kabul eden bir rota oluşturmak istiyorsanız bunu `"json"` dönüştürücü parametresiyle tanımlarsınız:
```lua
http.server.route("/my-extension/echo-request", "POST", "json", function(request)
  return http.server.json_response(request)
end)
```
Bu uç noktayı komut satırında `curl` ve `jq` kullanarak test edebilirsiniz:
```sh
curl 'http://0.0.0.0:12345/my-extension/echo-request?q=1' -X POST --data '{"input": "json"}' | jq
{
  "path": "/my-extension/echo-request",
  "method": "POST",
  "query": "q=1",
  "headers": {
    "host": "0.0.0.0:12345",
    "content-type": "application/x-www-form-urlencoded",
    "accept": "*/*",
    "user-agent": "curl/8.7.1",
    "content-length": "17"
  },
  "body": {
    "input": "json"
  }
}
```
Rota yolu, istek yolundan çıkarılıp isteğin bir parçası olarak işleyici işlevine iletilebilen kalıpları destekler; örneğin:
```lua
http.server.route("/my-extension/setting/{category}.{key}", function(request)
  return http.server.response(200, tostring(editor.get("/game.project", request.category .. "." .. request.key)))
end)
```
Şimdi örneğin `http://0.0.0.0:12345/my-extension/setting/project.title` adresini açarsanız `/game.project` dosyasından alınan oyununuzun başlığını görürsünüz.

Tek bir yol bölümünü eşleştiren kalıba ek olarak, `{*name}` sözdizimini kullanarak URL yolunun geri kalanını da eşleştirebilirsiniz. Örneğin proje kökündeki dosyaları sunan basit bir dosya sunucusu uç noktası şöyledir:
```lua
http.server.route("/my-extension/files/{*file}", function(request)
  local attrs = editor.external_file_attributes(request.file)
  if attrs.is_file then
    return http.server.external_file_response(request.file)
  else
    return 404
  end
end)
```
Şimdi örneğin `http://0.0.0.0:12345/my-extension/files/main/main.collection` adresini tarayıcıda açarsanız `main/main.collection` dosyasının içeriği görüntülenir.

## Kütüphanelerdeki düzenleyici betikleri {#editor-scripts-in-libraries}

Başkalarının kullanması için komutlar içeren kütüphaneler yayımlayabilirsiniz; bu komutlar düzenleyici tarafından otomatik olarak alınır. Ancak kancalar otomatik olarak alınamaz; çünkü proje kök klasöründeki bir dosyada tanımlanmaları gerekir, kütüphaneler ise yalnızca alt klasörleri sunar. Bunun amacı derleme süreci üzerinde daha fazla denetim sağlamaktır: yaşam döngüsü kancalarını yine de `.lua` dosyalarında basit işlevler olarak oluşturabilirsiniz; böylece kütüphanenizin kullanıcıları bunları kendi `/hooks.editor_script` dosyalarında yükleyip kullanabilir.

Ayrıca, bağımlılıklar Assets görünümünde gösterilseler de dosya olarak mevcut olmadıklarını (bir zip arşivinin içindeki girdiler olduklarını) unutmayın. Düzenleyicinin bağımlılıklardaki bazı dosyaları `build/plugins/` klasörüne çıkarmasını sağlamak mümkündür. Bunun için kütüphane klasörünüzde bir `ext.manifest` dosyası oluşturmanız, ardından bu `ext.manifest` dosyasının bulunduğu klasörde bir `plugins/bin/${platform}` klasörü oluşturmanız gerekir. Bu klasördeki dosyalar otomatik olarak `/build/plugins/${extension-path}/plugins/bin/${platform}` klasörüne çıkarılır; böylece düzenleyici betikleriniz bunlara başvurabilir.

## Tercihler {#preferences}

Düzenleyici betikleri, kullanıcının bilgisayarında saklanan kalıcı ve sürüm kontrolüne kaydedilmeyen veri parçaları olan tercihleri tanımlayabilir ve kullanabilir. Bu tercihlerin üç temel özelliği vardır:
- tür belirtilir: her tercih, veri türünü ve varsayılan değer gibi diğer üst verileri içeren bir şema tanımına sahiptir
- kapsam belirtilir: tercihler proje veya kullanıcı bazında kapsama sahiptir
- iç içedir: her tercih anahtarı, noktalarla ayrılmış bir dizedir; ilk yol bölümü bir düzenleyici betiğini, kalan bölümler ise bu betik içindeki grupları ve tek tek tercihleri tanımlar

Tüm tercihler, şemaları tanımlanarak kaydedilmelidir:
```lua
function M.get_prefs_schema()
  return {
    ["my_json_formatter.jq_path"] = editor.prefs.schema.string(),
    ["my_json_formatter.indent.size"] = editor.prefs.schema.integer({default = 2, scope = editor.prefs.SCOPE.PROJECT}),
    ["my_json_formatter.indent.type"] = editor.prefs.schema.enum({values = {"spaces", "tabs"}, scope = editor.prefs.SCOPE.PROJECT}),
  }
end
```
Böyle bir düzenleyici betiği yeniden yüklendikten sonra düzenleyici bu şemayı kaydeder. Ardından düzenleyici betiği tercihleri alabilir ve ayarlayabilir; örneğin:
```lua
-- Get a specific preference
editor.prefs.get("my_json_formatter.indent.type")
-- Returns: "spaces"

-- Get an entire preference group
editor.prefs.get("my_json_formatter")
-- Returns:
-- {
--   jq_path = "",
--   indent = {
--     size = 2,
--     type = "spaces"
--   }
-- }

-- Set multiple nested preferences at once
editor.prefs.set("my_json_formatter.indent", {
    type = "tabs",
    size = 1
})
```

## Yürütme modları {#execution-modes}

Düzenleyici betiklerinin çalışma zamanı ortamı, düzenleyici betiklerinin çoğunlukla ayrıca ele alması gerekmeyen 2 yürütme modu kullanır: **anında (immediate)** ve **uzun süren (long-running)**. 

**Anında** modu, düzenleyicinin betikten mümkün olan en hızlı şekilde yanıt alması gerektiğinde kullanılır. Örneğin menü komutlarının `active` geri çağırımları anında modunda yürütülür; çünkü bu denetimler, kullanıcının düzenleyiciyle etkileşimine yanıt olarak düzenleyicinin kullanıcı arayüzü iş parçacığında yapılır ve kullanıcı arayüzünü aynı kare içinde güncellemelidir. 

**Uzun süren** modu, düzenleyicinin betikten anında yanıt alması gerekmediğinde kullanılır. Örneğin menü komutlarının `run` geri çağırımları **uzun süren** modunda yürütülür; böylece betik, işini tamamlamak için daha fazla zaman kullanabilir.

Düzenleyici betiklerinin kullanabildiği bazı işlevlerin çalışması uzun sürebilir. Örneğin `editor.execute("git", "status", {reload_resources=false, out="capture"})` yeterince büyük projelerde bir saniyeye kadar sürebilir. Düzenleyicinin hızlı yanıt vermesini ve performansını korumak için zaman alabilecek işlevlere, düzenleyicinin anında yanıt gerektirdiği bağlamlarda izin verilmez. Böyle bir işlevi anında yanıt gerektiren bir bağlamda kullanmaya çalışmak bir hatayla sonuçlanır: `Cannot use long-running editor function in immediate context`. Bu hatayı gidermek için bu tür işlevleri anında yanıt gerektiren bağlamlarda kullanmaktan kaçının.

Aşağıdaki işlevler uzun süren olarak kabul edilir ve anında modunda kullanılamaz:
- `editor.create_directory()`, `editor.create_resources()`, `editor.delete_directory()`, `editor.save()`, `os.remove()` ve `file:write()`: bu işlevler diskteki dosyaları değiştirir; bunun sonucunda düzenleyici, bellekteki kaynak ağacını diskteki durumla eşitler ve bu işlem büyük projelerde saniyeler sürebilir.
- `editor.execute()`: kabuk komutlarının yürütülmesi öngörülemeyen bir süre alabilir.
- `editor.transact()`: birçok yerden başvurulan düğümlerdeki büyük işlemler yüzlerce milisaniye sürebilir; bu da kullanıcı arayüzünün hızlı yanıt vermesi için çok yavaştır.

Aşağıdaki kod yürütme bağlamları anında modunu kullanır:
- Menü komutlarının `active` geri çağırımları: düzenleyicinin aynı kullanıcı arayüzü karesi içinde betikten yanıt alması gerekir.
- Düzenleyici betiklerinin üst düzeyi: düzenleyici betiklerini yeniden yükleme işleminin herhangi bir yan etkisi olmasını beklemiyoruz.

## Eylemler

::: sidenote
Önceden düzenleyici, Lua sanal makinesiyle engelleyici bir şekilde etkileşim kuruyordu. Bazı etkileşimlerin düzenleyicinin kullanıcı arayüzü iş parçacığından yapılması gerektiği için düzenleyici betiklerinin yürütmeyi engellememesi kesin bir gereklilikti. Bu nedenle örneğin `editor.execute()` ve `editor.transact()` yoktu. Betiklerin yürütülmesi ve düzenleyici durumunun değiştirilmesi, bunların yerine kancalardan ve komutların `run` işleyicilerinden bir "eylemler" dizisi döndürülerek tetikleniyordu.

Artık düzenleyici, Lua sanal makinesiyle engelleyici olmayan bir şekilde etkileşim kuruyor; bu nedenle bu eylemlere artık gerek yok: `editor.execute()` gibi işlevleri kullanmak daha kullanışlı, kısa ve güçlüdür. Bu eylemlerin **KULLANIMI ARTIK ÖNERİLMİYOR**, ancak bunları kaldırma planımız yok.
:::

Düzenleyici betikleri, bir komutun `run` işlevinden veya `/hooks.editor_script` dosyasının kanca işlevlerinden bir eylem dizisi döndürebilir. Bu eylemler daha sonra düzenleyici tarafından gerçekleştirilir.

Eylem, düzenleyicinin ne yapması gerektiğini açıklayan bir tablodur. Her eylemin bir `action` anahtarı vardır. Eylemler 2 çeşittir: geri alınabilir ve geri alınamaz.

### Geri alınabilir eylemler

::: sidenote
`editor.transact()` kullanmayı tercih edin.
:::

Geri alınabilir bir eylem, yürütüldükten sonra geri alınabilir. Bir komut birden fazla geri alınabilir eylem döndürürse bunlar birlikte gerçekleştirilir ve birlikte geri alınır. Mümkünse geri alınabilir eylemler kullanmanız önerilir. Dezavantajları, daha sınırlı olmalarıdır.

Mevcut geri alınabilir eylemler:
- `"set"` — düzenleyicideki bir düğümün özelliğini belirli bir değere ayarlar. Örnek:
  ```lua
  {
    action = "set",
    node_id = opts.selection,
    property = "text",
    value = "current time is " .. os.date()
  }
  ```
  `"set"` eylemi şu anahtarları gerektirir:
  - `node_id` — düğüm kimliğini içeren userdata değeri. Alternatif olarak burada düzenleyiciden aldığınız düğüm kimliği yerine bir kaynak yolu, örneğin `"/main/game.script"`, kullanabilirsiniz;
  - `property` — düğümün ayarlanacak özelliği; örneğin `"text"`;
  - `value` — özelliğin yeni değeri. `"text"` özelliği için bir dize olması önerilir.

### Geri alınamaz eylemler

::: sidenote
`editor.execute()` kullanmayı tercih edin.
:::

Geri alınamaz bir eylem geri alma geçmişini temizler; bu nedenle böyle bir eylemi geri almak istiyorsanız sürüm kontrolü gibi başka yöntemler kullanmanız gerekir.

Mevcut geri alınamaz eylemler:
- `"shell"` — bir kabuk betiği yürütür. Örnek:
  ```lua
  {
    action = "shell",
    command = {
      "./scripts/minify-json.sh",
      editor.get(opts.selection, "path"):sub(2) -- trim leading "/"
    }
  }
  ```
  `"shell"` eylemi, komuttan ve bağımsız değişkenlerinden oluşan bir dizi olan `command` anahtarını gerektirir.

### Eylemleri ve yan etkileri birleştirme

Geri alınabilir ve geri alınamaz eylemleri bir arada kullanabilirsiniz. Eylemler sırayla yürütülür; dolayısıyla eylemlerin sırasına bağlı olarak komutun bazı bölümlerini geri alma olanağını kaybedersiniz.

Eylem bekleyen işlevlerden eylem döndürmek yerine, doğrudan `io.open()` kullanarak dosyaları okuyabilir ve onlara yazabilirsiniz. Bu, geri alma geçmişini temizleyecek bir kaynak yeniden yüklemesini tetikler.
