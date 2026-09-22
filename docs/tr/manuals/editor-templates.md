---
title: Düzenleyici şablonları
brief: New Project penceresine kendi özel proje şablonlarınızı ekleyebilirsiniz.
---

# Düzenleyici şablonları

New Project penceresine kendi özel proje şablonlarınızı (project templates) ekleyebilirsiniz:

![özel proje şablonları](images/editor/custom_project_templates.png)

Özel proje şablonları içeren bir veya daha fazla yeni sekme eklemek için kullanıcı ana dizininizdeki `.defold` klasörüne bir `welcome.edn` dosyası eklemeniz gerekir:

* Kullanıcı ana dizininizde `.defold` adlı bir klasör oluşturun.
  * Windows'ta `C:\Users\**Your Username**\.defold`
  * macOS'te `/Users/**Your Username**/.defold`
  * Linux'ta `~/.defold`
* `.defold` klasöründe bir `welcome.edn` dosyası oluşturun

`welcome.edn` dosyası Extensible Data Notation biçimini kullanır. Örnek:

```
{:new-project
  {:categories [
    {:label "My Templates"
     :templates [
          {:name "My project"
           :description "My template with everything set up the way I want it."
           :image "empty.svg"
           :zip-url "https://github.com/britzl/template-project/archive/master.zip"
           :skip-root? true},
          {:name "My other project"
           :description "My other template with everything set up the way I want it."
           :image "empty.svg"
           :zip-url "https://github.com/britzl/template-other-project/archive/master.zip"
           :skip-root? true}]
    }]
  }
}
```

Bu, yukarıdaki ekran görüntüsünde görülen şablon listesini oluşturur.

::: sidenote
Yalnızca [düzenleyiciyle birlikte gelen](https://github.com/defold/defold/tree/dev/editor/resources/welcome/images) şablon görsellerini kullanabilirsiniz.
:::
