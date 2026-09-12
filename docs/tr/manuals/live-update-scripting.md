---
title: Live Update içeriğini betiklerle kullanma
brief: Live Update içeriğini kullanmak için verileri indirip oyununuza bağlamanız gerekir. Bu kılavuzda Live Update'i betiklerle nasıl kullanacağınızı öğrenin.
---

# Live Update'i betiklerle kullanma

Temel bağlama (mount) iş akışında `liveupdate.add_mount()`, `liveupdate.remove_mount()` ve `liveupdate.get_mounts()` kullanılır. Kullanılabilir tüm işlevler için [`liveupdate` API başvuru belgelerinin tamamına](/ref/liveupdate/) bakın.

Kodun, derleme bildirimi (build manifest) dışarıda bırakılmış Live Update içeriği bekleyen bir dağıtım paketini ayırt etmesi gerektiğinde `liveupdate.is_built_with_excluded_files()` kullanın:

```lua
if liveupdate.is_built_with_excluded_files() then
    print("The bundle expects excluded Live Update content")
end
```

Bu işlev yalnızca derleme bildiriminin üst verilerini bildirir. Bir arşivin şu anda bağlı olduğu veya belirli bir kaynağın (resource) kullanılabilir olduğu anlamına gelmez. Etkin bağlama kayıtlarını incelemek için `liveupdate.get_mounts()`, bir koleksiyon vekilinin (collection proxy) bildirimde kayıtlı kaynak karma değerlerini (hash) incelemek için [`collectionproxy.get_resources()`](/ref/collectionproxy/#collectionproxy.get_resources) kullanın.

Önerilen iş akışı, eksiksiz bir Zip arşivini indirip bir `zip:` URI değeri kullanarak bağlamaktır.

## Bağlama kayıtlarını alma

`liveupdate.get_mounts()`, geçerli oturumda etkin olan bağlama kayıtlarını döndürür. Her kayıtta bir `uri` dizesi, sayısal bir `priority` değeri ve bir `name` karma değeri bulunur. Liste ayrıca motorun öncelikleri sıfırın altında olan ve kaldırılamayan temel bağlama kayıtlarını da içerir.

Motor, yeniden başlatıldıktan sonra bağlamaları geri yüklemez. Uygulamanın daha sonraki bir oturumda önceden indirilmiş içeriğe ihtiyacı varsa paketin URI değerini, adını ve önceliğini kendi kayıt verilerinde kalıcı olarak saklaması ve başlangıçta `liveupdate.add_mount()` işlevini yeniden çağırması gerekir.

Birden fazla paket bağlandığında, bunların uygulama tarafından tanımlanan üst verilerini doğrulamak yararlıdır. `mount.name` bir karma değeri olduğundan onu tablo anahtarı olarak kullanın veya `hash("mount-name")` ile karşılaştırın; bir kaynak yolu oluşturmak için dizelere eklemeyin. Aşağıdaki örnek, her adın karma değerini benzersiz bir üst veri kaynağı yoluna eşler:

```lua
local function remove_old_mounts()
	local mounts = liveupdate.get_mounts() -- table with mounts
	local version_resources = {
		[hash("level-pack")] = "/version_level_pack.json",
		[hash("season-pack")] = "/version_season_pack.json",
	}

	for _, mount in ipairs(mounts) do
		local version_resource = version_resources[mount.name]
		local version_data = version_resource and sys.load_resource(version_resource)

		if version_data then
			version_data = json.decode(version_data)
		elseif mount.priority >= 0 then
			version_data = {version = 0} -- if it has no version file, it's likely an old/invalid archive
		end

		-- Ignore the engine's base mounts, which have negative priorities.
		if version_data and version_data.version < sys.get_config_int("game.minimum_lu_version") then
			liveupdate.remove_mount(mount.name)
		end
	end
end
```

Farklı paketler için benzersiz üst veri yolları kullanın. Kaynak arama işlemi bağlama önceliğine göre yapıldığından, aynı yolun birden fazla pakette kullanılması en yüksek öncelikli bağlamadaki kopyanın okunmasına neden olur.

## Dışarıda bırakılan koleksiyon vekillerini betiklerle kullanma

Paketleme dışında bırakılmış bir koleksiyon vekili, önemli bir farkla normal bir koleksiyon vekili gibi çalışır. Dağıtım paketinin depolama alanında bulunmayan kaynakları varken ona `load` iletisi göndermek, yüklemenin başarısız olmasına neden olur.

Arşiv tabanlı iş akışında, genellikle bir vekilin hangi arşive veya arşivlere ihtiyaç duyduğunu önceden belirler ve bunları vekili yüklemeden önce bağlarsınız. Dışarıda bırakıldığını bildiğiniz bir vekilin bildirimde kayıtlı kaynak karma değerlerini incelemek için `collectionproxy.get_resources()` kullanın.

Bir paket bağlandıktan sonra, dışarıda bırakılmış ve yüklü olmayan bir vekil `collectionproxy.set_collection()` ile derlenmiş farklı bir koleksiyona (collection) da yönlendirilebilir. Kısıtlamalar ve yükleme sırası için [Dışarıda bırakılan bir vekilin koleksiyonunu değiştirme](/manuals/collection-proxy/#changing-an-excluded-proxys-collection) bölümüne bakın.

Live Update içeriği yayımlayan bir arşiv derlemesinde, dağıtım paketine dahil edilen ana bildirim dışarıda bırakılan Live Update kayıtlarını içermez; yayımlanan paketin bildirimi ise bunları korur. `collectionproxy.get_resources()`, bildirimdeki bağımlılık üst verilerini okur; başvurulan her veri bloğunun kullanılabilir olduğunu doğrulamaz:

* Vekilin dışarıda bırakılan kayıtlarını içeren bir paket bildirimi bağlanmadan önce, `collectionproxy.get_resources("#proxy")` boş bir `{}` tablosu döndürür.
* İlgili paket bağlandıktan sonra, o vekilin kaynak karma değerlerini içeren boş olmayan bir tablo döndürür. Örneğin:

```lua
{
    "a1b2c3...",
    "d4e5f6...",
    "7890ab...",
    ...
}
```

 Aşağıdaki örnek kod, kaynakların `game.http_url` ayarında belirtilen URL üzerinden erişilebilir olduğunu varsayar.

```lua

-- You'll need to track which archive contains which content
-- In this example, we only use a single liveupdate archive, containing all missing resource.
-- If you are using multiple archive, you need to structure the downloads accordingly
local lu_infos = {
    liveupdate = {
        name = "liveupdate",
        priority = 10,
    }
}

local function get_lu_info_for_level(level_name)
    if level_name == "level1" then
        return lu_infos['liveupdate']
    end
end

local function mount_zip(self, name, priority, path, callback)
    liveupdate.add_mount(name, "zip:" .. path, priority, function(_self, _name, _uri, _result) -- <1>
        callback(_name, _uri, _result)
    end)
end

local function has_mount(name)
    local name_hash = hash(name)
    for _, mount in ipairs(liveupdate.get_mounts()) do
        if mount.name == name_hash then
            return true
        end
    end
    return false
end

function init(self)
    self.http_url = sys.get_config_string("game.http_url", nil) -- <2>

    local level_name = "level1"

    local info = get_lu_info_for_level(level_name) -- <3>

    msg.post("#", "load_level", {level = "level1", info = info }) -- <4>
end

function on_message(self, message_id, message, sender)
    if message_id == hash("load_level") then
        local proxy_resources = collectionproxy.get_resources("#" .. message.level) -- <5>

        -- A build that publishes Live Update content omits excluded entries from the
        -- bundled manifest, so this table is empty until the relevant package manifest
        -- is mounted. After mounting, it contains the resource hashes for the proxy.
        if message.info and #proxy_resources == 0 and not has_mount(message.info.name) then
            msg.post("#", "download_archive", message) -- <6>
        else
            msg.post("#" .. message.level, "load")
        end

    elseif message_id == hash("download_archive") then
        local zip_filename = message.info.name .. ".zip"
        local download_path = sys.get_save_file("mygame", zip_filename)
        local url = self.http_url .. "/" .. zip_filename

        -- Check if the archive already exists. If it does, try to mount it!
        if sys.exists(download_path) then
            mount_zip(self, message.info.name, message.info.priority, download_path, function(name, uri, result) -- <8>
                if result == liveupdate.LIVEUPDATE_OK then
                    msg.post("#", "load_level", message) -- try to load the level again
                else
                    os.remove(download_path)             -- remove and try to
                    msg.post("#", "load_level", message) -- download again
                end
            end)
        else
            -- Make the request. You can use credentials
            http.request(url, "GET", function(self, id, response) -- <7>
                if response.status == 200 or response.status == 304 then
                    mount_zip(self, message.info.name, message.info.priority, download_path, function(name, uri, result) -- <8>
                        if result == liveupdate.LIVEUPDATE_OK then
                            msg.post("#", "load_level", message) -- try to load the level again
                        else
                            print("Failed to mount archive", download_path, ":", result)
                        end
                    end)
                else
                    print("Failed to download archive", download_path, "from", url, ":", response.status)
                end
            end, nil, nil, {path=download_path})
        end

    elseif message_id == hash("proxy_loaded") then -- the level is loaded, and we can enable it
        msg.post(sender, "init")
        msg.post(sender, "enable")
    end
end
```

1. `liveupdate.add_mount()`, belirtilen bir ad, öncelik ve zip dosyası kullanarak tek bir arşivi bağlar. Veriler hemen yüklenebilir duruma gelir (motoru yeniden başlatmak gerekmez). Bağlama yalnızca geçerli oturum boyunca etkindir. İndirilen paketin yolunu ve istediğiniz bağlama ayarlarını kendi kayıt verilerinizde kalıcı olarak saklayın ve her yeniden başlatmadan sonra `liveupdate.add_mount()` işlevini tekrar çağırın.
2. Arşivi, indirebileceğiniz çevrimiçi bir konumda (örneğin S3 üzerinde) saklamanız gerekir.
3. Bir koleksiyon vekilinin adına göre hangi arşivi veya arşivleri indireceğinizi ve bunları nasıl bağlayacağınızı belirlemeniz gerekir
4. Başlangıçta bölümü yüklemeyi deneriz.
5. Bu arşiv yayımlama iş akışında, vekilin dışarıda bırakılan içeriğine ait üst verileri incelemek için `collectionproxy.get_resources()` kullanın. İlgili paket bildirimi bağlanana kadar `{}`, bağlandıktan sonra ise kaynak karma değerlerini içeren boş olmayan bir tablo döndürür. Bu karma değerleri bağımlılıkları tanımlar; sonuç tek başına her veri bloğunun kullanılabilir olduğunu doğrulamaz.
6. Vekil Live Update içeriği kullanıyorsa ve ilgili arşiv henüz bağlanmamışsa, vekili yüklemeden önce arşivi indirip bağlarız.
7. Bir HTTP isteği yapın ve arşivi `download_path` konumuna indirin
8. Veriler indirildi; artık bunları çalışan motora bağlama zamanı.


Yükleme kodu hazır olduğuna göre uygulamayı test edebiliriz. Ancak uygulamayı düzenleyiciden çalıştırmak hiçbir şey indirmez. Bunun nedeni Live Update'in bir dağıtım paketi özelliği olmasıdır. Düzenleyici ortamında çalıştırılırken hiçbir kaynak dışarıda bırakılmaz. Her şeyin düzgün çalıştığından emin olmak için bir dağıtım paketi oluşturmamız gerekir.
