---
title: Szablony w Edytorze
brief: Możesz dodać własne niestandardowe szablony projektów do okna Nowy projekt.
---

# Szablony w Edytorze

Możesz dodać własne niestandardowe szablony projektów do okna Nowy projekt (New Project):

![niestandardowe szablony projektów](images/editor/custom_project_templates.png)

Aby dodać jedną lub więcej nowych zakładek z niestandardowymi szablonami projektów, musisz dodać plik `welcome.edn` w folderze `.defold` w katalogu domowym użytkownika:

* Utwórz folder o nazwie `.defold` w katalogu domowym użytkownika.
  * W systemie Windows `C:\Użytkownicy\**Twoja Nazwa Użytkownika**\.defold` (ang: `C:\Users\**Your Username**\.defold`)
  * Na systemie macOS `/Użytkownicy/**Twoja Nazwa Użytkownika**/.defold` (ang: `/Users/**Your Username**/.defold`)
  * Na systemie Linux `~/.defold`
* Utwórz plik `welcome.edn` w folderze `.defold`.

Plik `welcome.edn` używa formatu Extensible Data Notation. Przykład:

```
{:new-project
  {:categories [
    {:label "Mój szablon"
     :templates [
          {:name "Mój projekt"
           :description "Mój szablon z moimi własnymi ustawieniami."
           :image "empty.svg"
           :zip-url "https://github.com/britzl/template-project/archive/master.zip"
           :skip-root? true},
          {:name "Mój inny projekt"
           :description "Mój inny szablon z moimi własnymi ustawieniami."
           :image "empty.svg"
           :zip-url "https://github.com/britzl/template-other-project/archive/master.zip"
           :skip-root? true}]
    }]
  }
}
```

To stworzy listę szablonów widocznych na zrzucie ekranu powyżej (na screenshocie nazwy i opisy są w języku angielskim).

::: sidenote
Obecnie można używać tylko obrazów szablonów [dołączonych do Edytora](https://github.com/defold/defold/tree/dev/editor/resources/welcome/images).
:::
