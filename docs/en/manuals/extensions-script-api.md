---
title: Adding editor auto-complete to a native extensions
brief: This manual explains how to create a script API definition so that the Defold editor can provide auto-complete for users of an extension.
---

# Auto-complete for native extensions

The Defold editor will provide auto-complete suggestions for all Defold API functions and it will try to generate suggestions for Lua modules required by your scripts. The editor is however unable to provide auto-complete suggestions for the functionality exposed by native extensions. In the case of native extensions it is up to the extension author to generate a script API definition file that the editor can use to provide auto-complete suggestions.


## Creating a script API definition

A script API definition file has the extension `.script_api` and it is a file in [YAML format](https://yaml.org/). The expected format for a script API definition is:

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


## Examples

Refer to the following projects for actual usage examples:

* [Facebook extension](https://github.com/defold/extension-facebook/tree/master/facebook/api)
* [WebView extension](https://github.com/defold/extension-webview/blob/master/webview/api/webview.script_api)
