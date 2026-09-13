---
title: Einer nativen Erweiterung Codevervollständigung im Editor hinzufügen
brief: Dieses Handbuch erklärt, wie du eine Skript-API-Definition erstellst, damit der Defold-Editor bei der Verwendung einer Erweiterung Codevervollständigung anbieten kann.
---

# Codevervollständigung für native Erweiterungen {#auto-complete-for-native-extensions}

Der Defold-Editor bietet Vorschläge zur Codevervollständigung für alle Defold-API-Funktionen und erzeugt Vorschläge für Lua-Module, die deine Skripte einbinden. Der Editor kann jedoch nicht automatisch Vorschläge zur Codevervollständigung für die Funktionalität bereitstellen, die native Erweiterungen (native extensions) zugänglich machen. Eine native Erweiterung kann eine API-Definition in einer separaten Datei bereitstellen, um Vorschläge zur Codevervollständigung auch für die API der Erweiterung zu ermöglichen.


## Eine Skript-API-Definition erstellen {#creating-a-script-api-definition}

Eine Datei mit einer Skript-API-Definition hat die Dateierweiterung `.script_api`. Sie muss im [YAML-Format](https://yaml.org/) vorliegen und zusammen mit den Dateien der Erweiterung abgelegt sein. Das erwartete Format einer Skript-API-Definition ist:

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

Als Typen sind `table, string , boolean, number, function` möglich. Wenn ein Wert mehrere Datentypen haben kann, wird dies als `[type1, type2, type3]` geschrieben.
::: sidenote
Typen werden derzeit nicht im Editor angezeigt. Es wird empfohlen, sie trotzdem anzugeben, damit sie verfügbar sind, sobald der Editor die Anzeige von Typinformationen unterstützt.
:::

## Beispiele {#examples}

Konkrete Anwendungsbeispiele findest du in den folgenden Projekten:

* [Facebook-Erweiterung](https://github.com/defold/extension-facebook/tree/master/facebook/api)
* [WebView-Erweiterung](https://github.com/defold/extension-webview/blob/master/webview/api/webview.script_api)
