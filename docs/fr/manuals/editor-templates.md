---
title: Modèles de l'éditeur
brief: Vous pouvez ajouter vos propres modèles de projet personnalisés à la fenêtre New Project.
---

# Modèles de l'éditeur {#editor-templates}

Vous pouvez ajouter vos propres modèles de projet personnalisés à la fenêtre New Project :

![modèles de projet personnalisés](images/editor/custom_project_templates.png)

Pour ajouter un ou plusieurs onglets contenant des modèles de projet personnalisés, vous devez ajouter un fichier `welcome.edn` dans le dossier `.defold` de votre répertoire personnel :

* Créez un dossier nommé `.defold` dans votre répertoire personnel.
  * Sous Windows `C:\Users\**Your Username**\.defold`
  * Sous macOS `/Users/**Your Username**/.defold`
  * Sous Linux `~/.defold`
* Créez un fichier `welcome.edn` dans le dossier `.defold`

Le fichier `welcome.edn` utilise le format Extensible Data Notation. Exemple :

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

Cela créera la liste de modèles visible dans la capture d'écran ci-dessus.

::: sidenote
Vous pouvez uniquement utiliser les images de modèles [fournies avec l'éditeur](https://github.com/defold/defold/tree/dev/editor/resources/welcome/images).
:::
