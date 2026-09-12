---
title: Dosyalarla çalışma
brief: Bu kılavuz, dosyaların nasıl kaydedilip yükleneceğini ve diğer dosya işlemlerinin nasıl gerçekleştirileceğini açıklar.
---

# Dosyalarla çalışma
Dosya oluşturmanın ve/veya dosyalara erişmenin birçok farklı yolu vardır. Dosya yolları ve dosyalara erişme yöntemleri, dosyanın türüne ve konumuna göre değişir.

## Dosya ve klasör erişimi için işlevler
Defold, dosyalarla çalışmak için çeşitli işlevler sunar:

* Dosyaları okumak ve yazmak için standart [`io.*` işlevlerini](https://defold.com/ref/stable/io/) kullanabilirsiniz. Bu işlevler, giriş/çıkış (I/O) sürecinin tamamı üzerinde çok ayrıntılı denetim sağlar.

```lua
-- open myfile.txt for writing in binary mode
-- returns nil plus error message on failure
local f, err = io.open("path/to/myfile.txt", "wb")
if not f then
	print("Something went wrong while opening the file", err)
	return
end

-- write to the file, flush it to disk and then close the file
f:write("Foobar")
f:flush()
f:close()

-- open myfile.txt for reading in binary mode
-- returns nil plus error message on failure
local f, err = io.open("path/to/myfile.txt", "rb")
if not f then
	print("Something went wrong while opening the file", err)
	return
end

-- read the entire file as a string
-- returns nil on failure
local s = f:read("*a")
if not s then
	print("Error while reading file")
	return
end

print(s) -- Foobar
```

* Dosyaları yeniden adlandırmak ve silmek için [`os.rename()`](https://defold.com/ref/stable/os/#os.rename:oldname-newname) ve [`os.remove()`](https://defold.com/ref/stable/os/#os.remove:filename) işlevlerini kullanabilirsiniz.

* Lua tablolarını okumak ve yazmak için [`sys.save()`](https://defold.com/ref/stable/sys/#sys.save:filename-table) ve [`sys.load()`](https://defold.com/ref/stable/sys/#sys.load:filename) işlevlerini kullanabilirsiniz. Dosya yollarını platformdan bağımsız olarak çözümlemeye yardımcı olan başka [`sys.*`](https://defold.com/ref/stable/sys/) işlevleri de vardır.

```lua
-- get a platform independent path to the file "highscore" for application "mygame"
local path = sys.get_save_file("mygame", "highscore")

-- save a Lua table with some data
local ok = sys.save(path, { highscore = 100 })
if not ok then
	print("Failed to save", path)
	return
end

-- load the data
local ok, data = pcall(sys.load, path)
if not ok then
	-- The file exists, but is corrupt, foreign, or uses an unsupported format.
	print("Failed to load save data:", data)
	data = {}
end
print(data.highscore) -- 100
```

`sys.load()`, dosya yoksa boş bir tablo döndürür. Dosya varsa ancak `sys.save()` ile oluşturulmamışsa, bozuksa veya desteklenmeyen bir serileştirilmiş tablo biçimi kullanıyorsa `sys.load()` bir Lua hatası oluşturur. Bozulmuş veya dışarıdan değiştirilmiş kayıt verilerinin kurtarılabilmesi gerektiğinde yukarıdaki gibi `pcall()` kullanın.


## Dosya ve klasör konumları
Dosya ve klasör konumları üç kategoriye ayrılabilir:

* Uygulamanızın oluşturduğu uygulamaya özgü dosyalar
* Uygulamanızın dağıtım paketine eklenen dosya ve klasörler
* Uygulamanızın eriştiği sisteme özgü dosyalar

### Uygulamaya özgü dosyaları kaydetme ve yükleme
En yüksek puanlar, kullanıcı ayarları ve oyun durumu gibi uygulamaya özgü dosyaları kaydederken ve yüklerken işletim sisteminin bu amaç için ayırdığı bir konumu kullanmanız önerilir. Bir dosyanın işletim sistemine özgü mutlak yolunu almak için [`sys.get_save_file()`](https://defold.com/ref/stable/sys/#sys.get_save_file:application_id-file_name) işlevini kullanabilirsiniz. Mutlak yolu aldıktan sonra `sys.*`, `io.*` ve `os.*` işlevlerini kullanabilirsiniz (yukarıya bakın).

[`sys.save()` ve `sys.load()` işlevlerinin kullanımını gösteren örneği inceleyin](/examples/file/sys_save_load/).

### Uygulamanın dağıtım paketine eklenen dosyalara erişme {#how-to-access-files-bundled-with-the-application}
Dağıtım paketine eklenen kaynakları (bundle resources) ve özel kaynakları (custom resources) kullanarak uygulamanıza dosya ekleyebilirsiniz.

#### Özel kaynaklar {#custom-resources}
:[Custom Resources](../shared/custom-resources.md)

Eklentiler de `ext.properties` aracılığıyla bu dosyaları ekleyebilir. Bu dosyaların yolları, hem düzenleyici derlemelerinde hem de Bob arşivlerinde projenin özel kaynaklarıyla birleştirilir. [Eklentilerde özel kaynaklar](/manuals/extensions/#custom-resources) bölümüne bakın.

```lua
-- Load level data into a string
local data, error = sys.load_resource("/assets/level_data.json")
-- Decode json string to a Lua table
if data then
  local data_table = json.decode(data)
  pprint(data_table)
else
  print(error)
end
```

#### Dağıtım paketine eklenen kaynaklar
:[Bundle Resources](../shared/bundle-resources.md)

```lua
local path = sys.get_application_path()
local f = io.open(path .. "/mycommonfile.txt", "rb")
local txt, err = f:read("*a")
if not txt then
	print(err)
	return
end
print(txt)
```

::: sidenote
Güvenlik nedeniyle tarayıcıların (ve dolayısıyla tarayıcıda çalışan tüm JavaScript kodlarının) sistem dosyalarına erişmesi engellenir. Defold HTML5 derlemelerinde dosya işlemleri çalışmaya devam eder, ancak yalnızca tarayıcıdaki IndexedDB API üzerinden bir "sanal dosya sistemi" üzerinde çalışır. Bu, dağıtım paketine eklenen kaynaklara `io.*` veya `os.*` işlevleriyle erişilemeyeceği anlamına gelir. Ancak bu kaynaklara `http.request()` ile erişebilirsiniz.
:::


#### Özel kaynaklar ve dağıtım paketine eklenen kaynaklar - karşılaştırma

| Özellik                     | Özel kaynaklar                            | Dağıtım paketine eklenen kaynaklar              |
|-----------------------------|-------------------------------------------|------------------------------------------------|
| Yükleme hızı                | Daha hızlı - dosyalar ikili arşivden yüklenir | Daha yavaş - dosyalar dosya sisteminden yüklenir |
| Dosyanın bir kısmını yükleme | Hayır - yalnızca dosyaların tamamı yüklenir | Evet - dosyadan istediğiniz baytları okuyabilirsiniz |
| Paketlemeden sonra dosyaları değiştirme | Hayır - dosyalar ikili bir arşiv içinde saklanır | Evet - dosyalar yerel dosya sisteminde saklanır |
| HTML5 desteği               | Evet                                      | Evet - ancak erişim dosya I/O işlemleriyle değil, http üzerinden sağlanır |


### Sistem dosyalarına erişim
Sistem dosyalarına erişim, güvenlik nedeniyle işletim sistemi tarafından kısıtlanabilir. Yaygın kullanılan bazı sistem dizinlerinin (örneğin `documents`, `resource`, `temp`) mutlak yolunu almak için [`extension-directories`](https://defold.com/assets/extensiondirectories/) yerel kod eklentisini (native extension) kullanabilirsiniz. Bu dosyaların mutlak yolunu aldıktan sonra dosyalara erişmek için `io.*` ve `os.*` işlevlerini kullanabilirsiniz (yukarıya bakın).

::: sidenote
Güvenlik nedeniyle tarayıcıların (ve dolayısıyla tarayıcıda çalışan tüm JavaScript kodlarının) sistem dosyalarına erişmesi engellenir. Defold HTML5 derlemelerinde dosya işlemleri çalışmaya devam eder, ancak yalnızca tarayıcıdaki IndexedDB API üzerinden bir "sanal dosya sistemi" üzerinde çalışır. Bu, HTML5 derlemelerinde sistem dosyalarına erişmenin mümkün olmadığı anlamına gelir.
:::

## Eklentiler
[Asset Portal](https://defold.com/assets/), dosya ve klasör erişimini kolaylaştıran çeşitli varlıklar içerir. Bazı örnekler:

* [Lua File System (LFS)](https://defold.com/assets/luafilesystemlfs/) - Dizinler, dosya izinleri ve benzeri öğelerle çalışmak için işlevler
* [DefSave](https://defold.com/assets/defsave/) - Oturumlar arasında yapılandırma ve oyuncu verilerini kaydetmenize / yüklemenize yardımcı olan bir modül.
