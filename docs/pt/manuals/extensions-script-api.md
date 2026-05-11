---
title: Adicionando autocomplete do editor a uma extensão nativa
brief: Este manual explica como criar uma definição de API de script para que o editor Defold possa fornecer autocomplete aos usuários de uma extensão.
---

# Autocomplete para extensões nativas

O editor Defold fornece sugestões de autocomplete para todas as funções da API do Defold e gera sugestões para módulos Lua exigidos pelos seus scripts. No entanto, o editor não consegue fornecer automaticamente sugestões de autocomplete para a funcionalidade exposta por extensões nativas. Uma extensão nativa pode fornecer uma definição de API em um arquivo separado para habilitar sugestões de autocomplete também para a API da extensão.


## Criando uma definição de API de script

Um arquivo de definição de API de script usa a extensão `.script_api`. Ele deve estar em [formato YAML](https://yaml.org/) e localizado junto com os arquivos da extensão. O formato esperado para uma definição de API de script é:

```yml
- name: The name of the extension
  type: table
  desc: Extension description
  members:
  - name: Name of the first member
    type: Member type
    desc: Member description
    # se o tipo do membro for "function"
    parameters:
    - name: Name of the first parameter
      type: Parameter type
      desc: Parameter description
    - name: Name of the second parameter
      type: Parameter type
      desc: Parameter description
    # se o tipo do membro for "function"
    returns:
    - name: Name of first return value
      type: Return value type
      desc: Return value description
    examples:
    - desc: First example of member usage
    - desc: Second example of member usage

  - name: Name of the second member
    ...
```

Os tipos podem ser qualquer um de `table, string , boolean, number, function`. Se um valor puder ter múltiplos tipos, ele é escrito como `[type1, type2, type3]`.
::: sidenote
Atualmente os tipos não são exibidos no editor. Ainda assim, é recomendável fornecê-los para que estejam disponíveis quando o editor passar a dar suporte à exibição de informações de tipo.
:::

## Exemplos

Consulte os projetos a seguir para exemplos reais de uso:

* [Extensão Facebook](https://github.com/defold/extension-facebook/tree/master/facebook/api)
* [Extensão WebView](https://github.com/defold/extension-webview/blob/master/webview/api/webview.script_api)
