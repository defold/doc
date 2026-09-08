---
title: Ajout de l'autocomplétion de l'éditeur à une extension native
brief: Ce manuel explique comment créer une définition d'API de script pour que l'éditeur Defold puisse proposer l'autocomplétion aux utilisateurs d'une extension.
---

# Autocomplétion pour les extensions natives {#auto-complete-for-native-extensions}

L'éditeur Defold propose des suggestions d'autocomplétion pour toutes les fonctions de l'API Defold et génère des suggestions pour les modules Lua requis par vos scripts. L'éditeur ne peut toutefois pas proposer automatiquement des suggestions d'autocomplétion pour les fonctionnalités exposées par les extensions natives. Une extension native peut fournir une définition d'API dans un fichier distinct afin d'activer également les suggestions d'autocomplétion pour son API.


## Création d'une définition d'API de script {#creating-a-script-api-definition}

Un fichier de définition d'API de script porte l'extension `.script_api`. Il doit être au [format YAML](https://yaml.org/) et se trouver avec les fichiers de l'extension. Le format attendu pour une définition d'API de script est le suivant :

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

Les types peuvent être `table, string , boolean, number, function`. Si une valeur peut avoir plusieurs types, ils sont indiqués sous la forme `[type1, type2, type3]`.
::: sidenote
Les types ne sont actuellement pas affichés dans l'éditeur. Il est tout de même recommandé de les fournir afin qu'ils soient disponibles lorsque l'éditeur prendra en charge l'affichage des informations de type.
:::

## Exemples {#examples}

Consultez les projets suivants pour des exemples concrets d'utilisation :

* [Extension Facebook](https://github.com/defold/extension-facebook/tree/master/facebook/api)
* [Extension WebView](https://github.com/defold/extension-webview/blob/master/webview/api/webview.script_api)
