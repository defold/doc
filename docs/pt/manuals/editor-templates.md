---
title: Modelos do editor
brief: Você pode adicionar seus próprios modelos de projeto personalizados à janela Novo Projeto.
---

# Modelos do editor

Você pode adicionar seus próprios modelos de projeto personalizados à janela Novo Projeto:

![custom project templates](images/editor/custom_project_templates.png)

Para adicionar uma ou mais novas abas com modelos de projeto personalizados, você precisa adicionar um arquivo `welcome.edn` na pasta `.defold` no seu diretório de usuário:

* Crie uma pasta chamada `.defold` no seu diretório de usuário.
  * No Windows `C:\Users\**Seu Nome de Usuário**\.defold`
  * No macOS `/Users/**Seu Nome de Usuário**/.defold`
  * No Linux `~/.defold`
* Crie um arquivo `welcome.edn` na pasta `.defold`

O arquivo `welcome.edn` usa o formato Extensible Data Notation. Exemplo:

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

Isso criará a lista de modelos vista na captura de tela acima.

::: sidenote
Você só pode usar as imagens de modelo [incluídas com o editor](https://github.com/defold/defold/tree/dev/editor/resources/welcome/images).
:::
