---
title: Modelli dell'editor
brief: Puoi aggiungere i tuoi modelli di progetto personalizzati alla finestra New Project.
---

# Modelli dell'editor {#editor-templates}

Puoi aggiungere i tuoi modelli di progetto personalizzati alla finestra New Project:

![modelli di progetto personalizzati](images/editor/custom_project_templates.png)

Per aggiungere una o più nuove schede con modelli di progetto personalizzati, devi aggiungere un file `welcome.edn` nella cartella `.defold` all'interno della tua cartella personale:

* Crea una cartella chiamata `.defold` nella tua cartella personale.
  * Su Windows `C:\Users\**Your Username**\.defold`
  * Su macOS `/Users/**Your Username**/.defold`
  * Su Linux `~/.defold`
* Crea un file `welcome.edn` nella cartella `.defold`

Il file `welcome.edn` usa il formato Extensible Data Notation. Esempio:

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

Questo crea l'elenco di modelli visibile nella schermata qui sopra.

::: sidenote
Puoi usare soltanto le immagini dei modelli [incluse nell'editor](https://github.com/defold/defold/tree/dev/editor/resources/welcome/images).
:::
