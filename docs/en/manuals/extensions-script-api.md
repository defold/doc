---
title: Adding editor auto-complete to a native extensions
brief: This manual explains how to create a script API definition so that the Defold editor can provide auto-complete for users of an extension.
---

# Auto-complete for native extensions

The Defold editor will provide auto-complete suggestions for all Defold API functions and it will generate suggestions for Lua modules required by your scripts. The editor is however unable to automatically provide auto-complete suggestions for the functionality exposed by native extensions. A native extension can provide an API definition in a separate file to enable auto-complete suggestions also for the API of the extension.


## Creating a script API definition

A script API definition file has the extension `.script_api`. It must be in [YAML format](https://yaml.org/) and located together with the extension files. The expected format for a script API definition is:

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

Types can be any of `table, string , boolean, number, function`. If a value can have multiple types it is written as `[type1, type2, type3]`.
:::sidenote
Types are currently not shown in the editor. It is recommended to still provide them so that they are available once the editor has support for showing type information.
:::

## Examples

Refer to the following projects for actual usage examples:

* [Facebook extension](https://github.com/defold/extension-facebook/tree/master/facebook/api)
* [WebView extension](https://github.com/defold/extension-webview/blob/master/webview/api/webview.script_api)
