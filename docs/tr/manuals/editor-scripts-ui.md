---
title: "Düzenleyici betikleri: kullanıcı arayüzü"
brief: Bu kılavuz, Lua kullanarak düzenleyicide kullanıcı arayüzü öğeleri oluşturmayı açıklar
---

# Düzenleyici betikleri ve kullanıcı arayüzü

Bu kılavuz, Lua ile yazılan düzenleyici betiklerini (editor scripts) kullanarak düzenleyicide etkileşimli iletişim kutuları oluşturmayı ve kaynakları (resource) açmayı açıklar. Düzenleyici betiklerine başlamak için [Düzenleyici betikleri kılavuzuna](/manuals/editor-scripts) bakın. Düzenleyicinin tüm API başvuru belgelerini [burada](/ref/stable/editor-lua/) bulabilirsiniz.

## Merhaba dünya

Kullanıcı arayüzüyle (UI) ilgili tüm işlevler `editor.ui` modülünde bulunur. Başlangıç için özel bir arayüze sahip düzenleyici betiğinin en basit örneği şöyledir:
```lua
local M = {}

function M.get_commands()
    return {
        {
            label = "Do with confirmation",
            locations = {"View"},
            run = function()
                local result = editor.ui.show_dialog(editor.ui.dialog({
                    title = "Perform action?",
                    buttons = {
                        editor.ui.dialog_button({
                            text = "Cancel",
                            cancel = true,
                            result = false
                        }),
                        editor.ui.dialog_button({
                            text = "Perform",
                            default = true,
                            result = true
                        })
                    }
                }))
                print('Perform action:', result)
            end
        }
    }
end

return M

```

Bu kod parçası, **View → Do with confirmation** komutunu tanımlar. Komutu yürüttüğünüzde aşağıdaki iletişim kutusunu görürsünüz:

![Merhaba dünya iletişim kutusu](images/editor_scripts/perform_action_dialog.png)

Son olarak, <kbd>Enter</kbd> tuşuna bastıktan (veya `Perform` düğmesine tıkladıktan) sonra düzenleyici konsolunda aşağıdaki satırı görürsünüz:
```
Perform action:	true
```

## Kaynakları açma

Bir proje kaynağını açmak için bir komutun `run` işlevinden `editor.ui.open_resource()` işlevini çağırın. Yol `/` ile başlar. Görünümü belirtmezseniz kaynağın birincil görünümü seçilir:

```lua
editor.ui.open_resource("/main/main.script")
```

`code` ve `text` görünümleri, üçüncü bağımsız değişken olarak bir imleç konumu veya seçim kabul eder. Satır ve sütun numaraları `1` ile başlar; belirtilmeyen sütunun varsayılan değeri `1` olur. Bu bağımsız değişkenleri geçirirken görünümü belirtin:

```lua
editor.ui.open_resource("/main/main.script", "code", { line = 10 })
editor.ui.open_resource("/main/main.script", "code", { line = 10, column = 5 })
```

Bir aralık seçmek için bunun yerine `from` ve `to` imleç konumlarını belirtin:

```lua
editor.ui.open_resource("/main/main.script", "code", {
    from = { line = 10, column = 1 },
    to = { line = 12, column = 1 }
})
```

Yapılandırılmış kaynak görünümü düzenleyicide veya haricî bir uygulamada açılabilir. Yerleşik Code ve Text görünümleri, imleç ve seçim bağımsız değişkenlerini destekler. Desteklenen görünüm adları için [`editor.ui.open_resource()`](/ref/beta/editor/#editor.ui.open_resource:resource_path-view-args) başvurusuna bakın.

## Temel kavramlar

### Bileşenler

Düzenleyici, istenen arayüzü oluşturmak için bir araya getirilebilen çeşitli arayüz **bileşenleri** (component) sunar. Geleneksel olarak tüm bileşenler, **özellikler** (props) adı verilen tek bir tablo kullanılarak yapılandırılır. Bileşenlerin kendileri tablo değildir; düzenleyicinin arayüzü oluşturmak için kullandığı **değiştirilemez userdata** değerleridir.

### Özellikler

**Özellikler**, bileşenlere verilen girdileri tanımlayan tablolardır. Özellikler değiştirilemez kabul edilmelidir: özellik tablosunu yerinde değiştirmek bileşenin yeniden işlenmesini (re-render) tetiklemez, ancak farklı bir tablo kullanmak tetikler. Bileşen örneği (instance), önceki tabloya sığ eşitlik (shallow equality) ölçütüne göre eşit olmayan bir özellik tablosu aldığında arayüz güncellenir.

### Hizalama

Arayüzde bir bileşene bir alan ayrıldığında bileşen alanın tamamını kullanır; ancak bu, bileşenin görünür kısmının esneyeceği anlamına gelmez. Görünür kısım, ihtiyaç duyduğu kadar yer kaplar ve ardından ayrılan alanın sınırları içinde hizalanır. Bu nedenle, yerleşik bileşenlerin çoğu bir `alignment` özelliği tanımlar.

Örneğin, şu etiket bileşenini ele alalım:
```lua
editor.ui.label({
    text = "Hello",
    alignment = editor.ui.ALIGNMENT.RIGHT
})
```
Görünür kısım `Hello` metnidir ve bileşene ayrılan alanın sınırları içinde hizalanır:

![Hizalama](images/editor_scripts/alignment.png)

## Yerleşik bileşenler

Düzenleyici, arayüzü oluşturmak için birlikte kullanılabilen çeşitli yerleşik bileşenler tanımlar. Bileşenler kabaca 3 kategoride gruplandırılabilir: yerleşim, veri sunumu ve girdi.

### Yerleşim bileşenleri

Yerleşim bileşenleri, diğer bileşenleri yan yana yerleştirmek için kullanılır. Başlıca yerleşim bileşenleri **`horizontal`**, **`vertical`** ve **`grid`** bileşenleridir. Bu bileşenler ayrıca **padding** ve **spacing** gibi özellikler tanımlar. Burada padding, ayrılan alanın kenarından içeriğe kadar olan boşluğu; spacing ise alt bileşenler arasındaki boşluğu ifade eder:

![İç boşluk ve aralık](images/editor_scripts/padding_and_spacing.png)

Düzenleyici, iç boşluk ve aralık için `small`, `medium` ve `large` sabitlerini tanımlar. Aralık söz konusu olduğunda `small`, tek bir arayüz öğesinin farklı alt öğeleri arasındaki boşluk; `medium`, ayrı arayüz öğeleri arasındaki boşluk; `large` ise öğe grupları arasındaki boşluk içindir. Varsayılan aralık `medium` değeridir. İç boşluk değeri olarak `large`, pencerenin kenarlarından içeriğe kadar olan boşluğu; `medium`, belirgin bir arayüz öğesinin kenarlarından itibaren bırakılan boşluğu; `small` ise bağlam menüleri ve araç ipuçları (henüz uygulanmadı) gibi küçük arayüz öğelerinin kenarlarından itibaren bırakılan boşluğu ifade eder.

**`horizontal`** kapsayıcısı, alt bileşenlerini yatay olarak art arda yerleştirir ve her alt bileşenin yüksekliğini her zaman kullanılabilir alanı dolduracak şekilde ayarlar. Varsayılan olarak her alt bileşenin genişliği en az düzeyde tutulur; ancak alt bileşenin `grow` özelliğini `true` olarak ayarlayarak mümkün olduğunca fazla yer kaplamasını sağlayabilirsiniz.

**`vertical`** kapsayıcısı, eksenlerin yer değiştirmesi dışında yatay kapsayıcıya benzer.

Son olarak, **`grid`**, alt bileşenlerini tablo gibi 2B bir ızgaraya yerleştiren bir kapsayıcı bileşenidir. Izgaradaki `grow` ayarı satır veya sütunlara uygulanır; bu nedenle alt bileşen üzerinde değil, sütun yapılandırma tablosunda ayarlanır. Ayrıca, ızgaradaki alt bileşenler `row_span` ve `column_span` özellikleriyle birden fazla satırı veya sütunu kaplayacak şekilde yapılandırılabilir. Izgaralar, birden çok girdi içeren formlar oluşturmak için kullanışlıdır:
```lua
editor.ui.grid({
    padding = editor.ui.PADDING.LARGE, -- add padding around dialog edges
    columns = {{}, {grow = true}}, -- make 2nd column grow
    children = {
        {
            editor.ui.label({ 
                text = "Level Name",
                alignment = editor.ui.ALIGNMENT.RIGHT
            }),
            editor.ui.string_field({})
        },
        {
            editor.ui.label({ 
                text = "Author",
                alignment = editor.ui.ALIGNMENT.RIGHT
            }),
            editor.ui.string_field({})
        }
    }
})
```
Yukarıdaki kod, aşağıdaki iletişim kutusu formunu oluşturur:

![Yeni bölüm iletişim kutusu](images/editor_scripts/new_level_dialog.png)

### Veri sunumu bileşenleri

Düzenleyici, aşağıdaki veri sunumu bileşenlerini tanımlar:

- **`label`** — form girdileriyle birlikte kullanılması amaçlanan metin etiketi.
- **`icon`** — bir simge; şu anda yalnızca önceden tanımlanmış küçük bir simge kümesini göstermek için kullanılabilir, ancak gelecekte daha fazla simgeye izin vermeyi amaçlıyoruz.
- **`image`** — `/` ile başlayan bir proje kaynak yolundan veya haricî bir URL adresinden yüklenen görüntü. İsteğe bağlı `width` ve `height` özellikleri, görüntüyü en boy oranını koruyarak belirtilen boyutların içine sığdırır.
- **`heading`** — örneğin bir formda veya iletişim kutusunda bir başlık satırı göstermek için tasarlanmış metin öğesi. `editor.ui.HEADING_STYLE` numaralandırma türü, HTML'nin `H1`-`H6` başlıklarının yanı sıra düzenleyiciye özgü `DIALOG` ve `FORM` stillerini içeren çeşitli başlık stilleri tanımlar.
- **`paragraph`** — bir metin paragrafı göstermek için tasarlanmış metin öğesi. `label` ile temel farkı, paragrafın sözcük kaydırmayı desteklemesidir: ayrılan alan yatay olarak çok küçükse metin bir alt satıra kaydırılır ve görünüme sığmıyorsa `"..."` ile kısaltılabilir.

Örneğin, bir arayüz hem projedeki bir görüntüyü hem de web üzerinden alınan bir görüntüyü gösterebilir:

```lua
editor.ui.vertical({
    children = {
        editor.ui.image({
            image = "/builtins/assets/images/logo/logo_256.png",
            width = 64,
            height = 64
        }),
        editor.ui.image({
            image = "https://defold.com/images/assets/monarch-hero.jpg"
        })
    }
})
```

### Girdi bileşenleri

Girdi bileşenleri, kullanıcının arayüzle etkileşime girmesi için tasarlanmıştır. Tüm girdi bileşenleri, etkileşimin etkin olup olmadığını denetlemek için `enabled` özelliğini destekler ve etkileşim olduğunda düzenleyici betiğine bildirim gönderen çeşitli geri çağırım (callback) özellikleri tanımlar.

Statik bir arayüz oluşturuyorsanız yalnızca yerel değişkenleri değiştiren geri çağırımlar tanımlamanız yeterlidir. Dinamik arayüzler ve daha gelişmiş etkileşimler için [tepkisellik](#reactivity) bölümüne bakın.

Örneğin, basit bir statik New File iletişim kutusunu şu şekilde oluşturabilirsiniz:
```lua
-- initial file name, will be replaced by the dialog
local file_name = ""
local create_file = editor.ui.show_dialog(editor.ui.dialog({
    title = "Create New File",
    content = editor.ui.horizontal({
        padding = editor.ui.PADDING.LARGE,
        spacing = editor.ui.SPACING.MEDIUM,
        children = {
            editor.ui.label({
                text = "New File Name",
                alignment = editor.ui.ALIGNMENT.CENTER
            }),
            editor.ui.string_field({
                grow = true,
                text = file_name,
                -- Typing callback:
                on_value_changed = function(new_text)
                    file_name = new_text
                end
            })
        }
    }),
    buttons = {
        editor.ui.dialog_button({ text = "Cancel", cancel = true, result = false }),
        editor.ui.dialog_button({ text = "Create File", default = true, result = true })
    }
}))
if create_file then
    print("create", file_name)
end
```
Yerleşik girdi bileşenlerinin listesi şöyledir:
- **`string_field`**, **`integer_field`** ve **`number_field`**, dizeleri, tam sayıları ve sayıları düzenlemeye izin veren tek satırlı metin alanının çeşitleridir.
- **`select_box`**, bir açılır liste denetimiyle önceden tanımlanmış seçenek dizisinden bir seçenek seçmek için kullanılır.
- **`check_box`**, `on_value_changed` geri çağırımına sahip bir mantıksal değer girdi alanıdır
- **`button`**, düğmeye basıldığında çağrılan `on_press` geri çağırımına sahiptir.
- **`external_file_field`**, bilgisayarda bir dosya yolu seçmek için tasarlanmış bir bileşendir. Bir metin alanından ve dosya seçimi iletişim kutusu açan bir düğmeden oluşur.
- **`resource_field`**, projede bir kaynak seçmek için tasarlanmış bir bileşendir.

Düğmeler dışındaki tüm bileşenler, bileşenle ilgili sorunu gösteren bir `issue` özelliğinin ayarlanmasına izin verir (bu sorun `editor.ui.ISSUE_SEVERITY.ERROR` veya `editor.ui.ISSUE_SEVERITY.WARNING` olabilir). Örneğin:
```lua
issue = {severity = editor.ui.ISSUE_SEVERITY.WARNING, message = "This value is deprecated"}
```
Bir sorun belirtildiğinde girdi bileşeninin görünümü değişir ve sorun iletisini içeren bir araç ipucu eklenir.

Tüm girdilerin sorun durumlarıyla birlikte bir gösterimi şöyledir:

![Girdiler](images/editor_scripts/inputs_demo.png)

### İletişim kutusuyla ilgili bileşenler

Bir iletişim kutusu göstermek için `editor.ui.show_dialog` işlevini kullanmanız gerekir. Bu işlev, Defold iletişim kutularının ana yapısını tanımlayan bir **`dialog`** bileşeni bekler: `title`, `header`, `content` ve `buttons`. İletişim kutusu bileşeni biraz özeldir: bir arayüz öğesini değil, bir pencereyi temsil ettiği için başka bir bileşenin alt bileşeni olarak kullanılamaz. Ancak `header` ve `content`, olağan bileşenlerdir.

İletişim kutusu düğmeleri de özeldir: **`dialog_button`** bileşeni kullanılarak oluşturulurlar. Olağan düğmelerin aksine, iletişim kutusu düğmelerinin `on_pressed` geri çağırımı yoktur. Bunun yerine, iletişim kutusu kapatıldığında `editor.ui.show_dialog` işlevinin döndüreceği değeri içeren bir `result` özelliği tanımlarlar. İletişim kutusu düğmeleri ayrıca mantıksal değer alan `cancel` ve `default` özelliklerini tanımlar: `cancel` özelliğine sahip düğme, kullanıcı <kbd>Escape</kbd> tuşuna bastığında veya iletişim kutusunu işletim sisteminin kapatma düğmesiyle kapattığında tetiklenir; `default` düğmesi ise kullanıcı <kbd>Enter</kbd> tuşuna bastığında tetiklenir. Bir iletişim kutusu düğmesinin hem `cancel` hem de `default` özelliği aynı anda `true` olarak ayarlanabilir.

### Yardımcı bileşenler

Düzenleyici ayrıca bazı yardımcı bileşenler tanımlar: 
- **`separator`**, içerik bloklarını ayırmak için kullanılan ince bir çizgidir
- **`scroll`**, sardığı bileşen ayrılan alana sığmadığında kaydırma çubukları gösteren bir sarmalayıcı bileşendir

## Tepkisellik {#reactivity}

Bileşenler **değiştirilemez userdata** değerleri olduğu için oluşturulduktan sonra değiştirilemezler. Peki, arayüzün zaman içinde değişmesi nasıl sağlanır? Yanıt: **tepkisel bileşenler** (reactive components). 

::: sidenote
Düzenleyici betiklerinin arayüz sistemi, [React](https://react.dev/) kütüphanesinden esinlenir; bu nedenle tepkisel arayüzleri ve React kancalarını (hooks) bilmek yardımcı olur. 
:::

En basit anlatımla tepkisel bileşen, veri (özellikler) alan ve görünüm (başka bir bileşen) döndüren bir Lua işlevine sahip bileşendir. Tepkisel bileşen işlevi **kancalar** kullanabilir: bunlar, `editor.ui` modülünde bulunan ve bileşenlerinize tepkisel özellikler ekleyen özel işlevlerdir. Geleneksel olarak tüm kancaların adı `use_` ile başlar.

Tepkisel bir bileşen oluşturmak için `editor.ui.component()` işlevini kullanın. 

Şu örneğe bakalım: yalnızca girilen dosya adı boş olmadığında dosya oluşturmaya izin veren bir New File iletişim kutusu:

```lua
-- 1. dialog is a reactive component
local dialog = editor.ui.component(function(props)
    -- 2. the component defines a local state (file name) that defaults to empty string
    local name, set_name = editor.ui.use_state("")

    return editor.ui.dialog({ 
        title = props.title,
        content = editor.ui.vertical({
            padding = editor.ui.PADDING.LARGE,
            children = { 
                editor.ui.string_field({ 
                    value = name,
                    -- 3. typing + Enter updates the local state
                    on_value_changed = set_name 
                }) 
            }
        }),
        buttons = {
            editor.ui.dialog_button({ 
                text = "Cancel", 
                cancel = true 
            }),
            editor.ui.dialog_button({ 
                text = "Create File",
                -- 4. creation is enabled when the name exists
                enabled = name ~= "",
                default = true,
                -- 5. result is the name
                result = name
            })
        }
    })
end)

-- 6. show_dialog will either return non-empty file name or nil on cancel
local file_name = editor.ui.show_dialog(dialog({ title = "New File Name" }))
if file_name then 
    print("create " .. file_name)
else
    print("cancelled")
end
```

Bu kodu çalıştıran bir menü komutunu yürüttüğünüzde düzenleyici bir iletişim kutusu gösterir. `"Create File"` iletişim kutusu başlangıçta devre dışıdır, ancak bir ad yazıp <kbd>Enter</kbd> tuşuna bastığınızda etkinleşir:

![Yeni dosya iletişim kutusu](images/editor_scripts/reactive_new_file_dialog.png)

Peki, bu nasıl çalışır? İlk işlemede `use_state` kancası, bileşenle ilişkili bir yerel durum oluşturur ve bunu durumun ayarlayıcısıyla (setter) birlikte döndürür. Ayarlayıcı işlev çağrıldığında bileşenin yeniden işlenmesini planlar. Sonraki yeniden işlemelerde bileşen işlevi tekrar çağrılır ve `use_state` güncellenmiş durumu döndürür. Ardından, bileşen işlevinin döndürdüğü yeni görünüm bileşeni eskisiyle karşılaştırılır ve değişikliklerin saptandığı yerlerde arayüz güncellenir.

Bu tepkisel yaklaşım, etkileşimli arayüzler oluşturmayı ve bunları eşzamanlı tutmayı büyük ölçüde basitleştirir: kullanıcı girdisinde etkilenen tüm arayüz bileşenlerini açıkça güncellemek yerine görünüm, girdinin (özellikler ve yerel durum) saf bir işlevi (pure function) olarak tanımlanır ve düzenleyici tüm güncellemeleri kendisi yönetir.

### Tepkisellik kuralları

Düzenleyici, tepkisel işlev bileşenlerinin çalışabilmesi için aşağıdaki kurallara uymasını bekler:

1. Bileşen işlevleri saf olmalıdır. Bileşen işlevinin ne zaman veya ne sıklıkta çağrılacağı garanti edilmez. Tüm yan etkilerin işleme dışında, örneğin geri çağırımlarda gerçekleşmesi önerilir
2. Özellikler ve yerel durum değiştirilemez olmalıdır. Özellikleri değiştirmeyin. Yerel durumunuz bir tabloysa onu yerinde değiştirmeyin; durumun değişmesi gerektiğinde yeni bir tablo oluşturup ayarlayıcıya geçirin.
3. Bileşen işlevleri, her çağrıldıklarında aynı kancaları aynı sırayla çağırmalıdır. Kancaları döngülerin içinde, koşullu bloklarda, erken dönüşlerden sonra vb. çağırmayın. Kancaları bileşen işlevinin başında, diğer tüm kodlardan önce çağırmak iyi bir uygulamadır.
4. Kancaları yalnızca bileşen işlevlerinden çağırın. Kancalar, tepkisel bir bileşenin bağlamında çalışır; bu nedenle yalnızca bileşen işlevinde (veya bileşen işlevinin doğrudan çağırdığı başka bir işlevde) çağrılmalarına izin verilir.

### Kancalar

::: sidenote
[React](https://react.dev/) kütüphanesini biliyorsanız düzenleyicideki kancaların, kanca bağımlılıkları söz konusu olduğunda biraz farklı anlamlara sahip olduğunu fark edersiniz.
:::

Düzenleyici 2 kanca tanımlar: **`use_memo`** ve **`use_state`**.

### **`use_state`**

Yerel durum 2 şekilde oluşturulabilir: varsayılan bir değerle veya bir başlatıcı işlevle:
```lua
-- default value
local enabled, set_enabled = editor.ui.use_state(true)
-- initializer function + args
local id, set_id = editor.ui.use_state(string.lower, props.name)
```
Benzer şekilde, ayarlayıcı yeni bir değerle veya bir güncelleyici işlevle çağrılabilir:
```lua
-- updater function
local function increment_by(n, by)
    return n + by
end

local counter = editor.ui.component(function(props)
    local count, set_count = editor.ui.use_state(0)
    
    return editor.ui.horizontal({
        spacing = editor.ui.SPACING.SMALL,
        children = {
            editor.ui.label({
                text = tostring(count),
                alignment = editor.ui.ALIGNMENT.LEFT,
                grow = true
            }),
            editor.ui.text_button({
                text = "+1",
                on_pressed = function() set_count(increment_by, 1) end
            }),
            editor.ui.text_button({
                text = "+5",
                on_pressed = function() set_count(increment_by, 5) end
            })
        }
    })
end)
```

Son olarak durum **sıfırlanabilir**. `editor.ui.use_state()` işlevinin bağımsız değişkenlerinden herhangi biri değiştiğinde durum sıfırlanır; bu değişiklik `==` ile denetlenir. Bu nedenle `use_state` kancasının bağımsız değişkenleri olarak doğrudan yazılmış tabloları veya doğrudan tanımlanmış başlatıcı işlevleri kullanmayın: bu, her yeniden işlemede durumun sıfırlanmasına neden olur. Örnekle açıklayalım:
```lua
-- ❌ BAD: literal table initializer causes state reset on every re-render
local user, set_user = editor.ui.use_state({ first_name = props.first_name, last_name = props.last_name})

-- ✅ GOOD: use initializer function outside of component function to create table state
local function create_user(first_name, last_name) 
    return { first_name = first_name, last_name = last_name}
end
-- ...later, in component function:
local user, set_user = editor.ui.use_state(create_user, props.first_name, props.last_name)


-- ❌ BAD: literal initializer function causes state reset on every re-render
local id, set_id = editor.ui.use_state(function() return string.lower(props.name) end)

-- ✅ GOOD: use referenced initializer function to create the state
local id, set_id = editor.ui.use_state(string.lower, props.name)
```

### **`use_memo`**

Performansı iyileştirmek için `use_memo` kancasını kullanabilirsiniz. İşleme işlevlerinde, örneğin kullanıcı girdisinin geçerli olup olmadığını denetlemek için bazı hesaplamalar yapmak yaygındır. `use_memo` kancası, hesaplama işlevine verilen bağımsız değişkenlerin değişip değişmediğini denetlemenin hesaplama işlevini çağırmaktan daha düşük maliyetli olduğu durumlarda kullanılabilir. Kanca, hesaplama işlevini ilk işlemede çağırır ve `use_memo` kancasının tüm bağımsız değişkenleri değişmeden kalmışsa sonraki yeniden işlemelerde hesaplanan değeri tekrar kullanır:
```lua
-- validation function outside of component function
local function validate_password(password)
    if #password < 8 then
        return false, "Password must be at least 8 characters long."
    elseif not password:match("%l") then
        return false, "Password must include at least one lowercase letter."
    elseif not password:match("%u") then
        return false, "Password must include at least one uppercase letter."
    elseif not password:match("%d") then
        return false, "Password must include at least one number."
    else
        return true, "Password is valid."
    end
end

-- ...later, in component function
local username, set_username = editor.ui.use_state('')
local password, set_password = editor.ui.use_state('')
local valid, message = editor.ui.use_memo(validate_password, password)
```
Bu örnekte parola doğrulaması, parola her değiştiğinde (örneğin bir parola alanına yazı yazıldığında) çalışır, ancak kullanıcı adı değiştiğinde çalışmaz.

`use_memo` için başka bir kullanım alanı, daha sonra girdi bileşenlerinde kullanılan geri çağırımlar oluşturmaktır. Yerel olarak oluşturulmuş bir işlevin başka bir bileşene özellik değeri olarak verildiği durumlarda da kullanılır; bu, gereksiz yeniden işlemeleri önler.
