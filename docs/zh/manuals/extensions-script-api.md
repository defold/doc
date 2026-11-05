---
title: 为原生扩展添加编辑器自动补全
brief: 本手册解释了如何创建脚本API定义，以便Defold编辑器能为扩展用户提供自动补全功能。
---

# 原生扩展的自动补全

Defold编辑器会为所有Defold API函数提供自动补全建议，并会为脚本所需的Lua模块生成建议。然而，编辑器无法自动为原生扩展暴露的功能提供自动补全建议。原生扩展可以在单独的文件中提供API定义，以启用扩展API的自动补全建议。


## 创建脚本API定义

脚本API定义文件的扩展名为`.script_api`。它必须采用[YAML格式](https://yaml.org/)并与扩展文件放在一起。脚本API定义的预期格式为：

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

类型可以是`table, string, boolean, number, function`中的任意一种。如果一个值可以有多个类型，则写为`[type1, type2, type3]`。
::: sidenote
目前编辑器中不显示类型。但仍建议提供类型信息，以便编辑器在支持显示类型信息时可以使用。
:::

## 示例

请参考以下项目获取实际使用示例：

* [Facebook 扩展](https://github.com/defold/extension-facebook/tree/master/facebook/api)
* [WebView 扩展](https://github.com/defold/extension-webview/blob/master/webview/api/webview.script_api)
