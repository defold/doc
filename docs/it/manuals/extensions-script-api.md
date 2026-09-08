---
title: Aggiungere il completamento automatico dell'editor a un'estensione nativa
brief: Questo manuale spiega come creare una definizione dell'API per gli script, in modo che l'editor Defold possa fornire il completamento automatico a chi usa un'estensione.
---

# Completamento automatico per le estensioni native {#auto-complete-for-native-extensions}

L'editor Defold fornisce suggerimenti di completamento automatico per tutte le funzioni dell'API di Defold e genera suggerimenti per i moduli Lua richiesti dai tuoi script. L'editor non è però in grado di fornire automaticamente suggerimenti di completamento per le funzionalità esposte dalle estensioni native. Un'estensione nativa può fornire una definizione dell'API in un file separato per abilitare i suggerimenti di completamento automatico anche per la propria API.


## Creare una definizione dell'API per gli script {#creating-a-script-api-definition}

Un file di definizione dell'API per gli script ha l'estensione `.script_api`. Deve essere in [formato YAML](https://yaml.org/) e trovarsi insieme ai file dell'estensione. Il formato previsto per una definizione dell'API per gli script è:

```yml
- name: The name of the extension
  type: table
  desc: Extension description
  members:
  - name: Name of the first member
    type: Member type
    desc: Member description
    # if member type is "function"
    parameters:
    - name: Name of the first parameter
      type: Parameter type
      desc: Parameter description
    - name: Name of the second parameter
      type: Parameter type
      desc: Parameter description
    # if member type is "function"
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

I tipi possono essere uno qualsiasi tra `table, string , boolean, number, function`. Se un valore può avere più tipi, questi si scrivono come `[type1, type2, type3]`.
::: sidenote
Al momento i tipi non vengono mostrati nell'editor. Si consiglia comunque di specificarli, in modo che siano disponibili quando l'editor supporterà la visualizzazione delle informazioni sui tipi.
:::

## Esempi {#examples}

Consulta i seguenti progetti per esempi di utilizzo concreti:

* [Estensione Facebook](https://github.com/defold/extension-facebook/tree/master/facebook/api)
* [Estensione WebView](https://github.com/defold/extension-webview/blob/master/webview/api/webview.script_api)
