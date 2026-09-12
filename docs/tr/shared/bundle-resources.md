Dağıtım paketine eklenen kaynaklar (bundle resources), [*Bundle Resources* alanı](/manuals/project-settings/#bundle-resources) kullanılarak *game.project* dosyası üzerinden uygulamanızın dağıtım paketine dahil edilen ek dosya ve klasörlerdir.

*Bundle Resources* alanı, paketleme sırasında oluşan pakete olduğu gibi kopyalanması gereken kaynak dosyalarını ve klasörlerini içeren dizinlerin virgülle ayrılmış bir listesini içermelidir. Dizinler, proje kökünden başlayan mutlak bir yolla belirtilmelidir; örneğin `/res`. Kaynak dizini, `platform` veya `architecture-platform` biçiminde adlandırılmış alt klasörler içermelidir.

Desteklenen platformlar `ios`, `android`, `osx`, `win32`, `linux`, `web`, `switch` şeklindedir. Tüm platformlar için ortak kaynak dosyalarını içeren `common` adlı bir alt klasöre de izin verilir. Örnek:

```
res
├── win32
│   └── mywin32file.txt
├── common
│   └── mycommonfile.txt
└── android
    ├── myandroidfile.txt
    └── res
        └── xml
            └── filepaths.xml
```

Uygulamanın depolandığı konumun yolunu almak için [`sys.get_application_path()`](/ref/stable/sys/#sys.get_application_path:) işlevini kullanabilirsiniz. Erişmeniz gereken dosyaların nihai mutlak yolunu oluşturmak için bu uygulama temel yolunu kullanın. Bu dosyaların mutlak yolunu elde ettikten sonra dosyalara erişmek için `io.*` ve `os.*` işlevlerini kullanabilirsiniz.
