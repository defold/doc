---
title: 为原生扩展添加编辑器自动补全
brief: 本手册解释了如何创建脚本API定义，以便Defold编辑器能为扩展用户提供自动补全功能。
---

# 原生扩展的自动补全

Defold编辑器会为所有Defold API函数提供自动补全建议，并会为脚本所需的Lua模块生成建议。然而，编辑器无法自动为原生扩展暴露的功能提供自动补全建议。原生扩展可以在单独的文件中提供API定义，以启用扩展API的自动补全建议。


## 创建脚本API定义

脚本API定义文件的扩展名为`.script_api`。它必须采用[YAML格式](https://yaml.org/)并与扩展文件放在一起。脚本API定义的预期格式为：

```yml
- name: 扩展名
  type: table
  desc: 扩展描述
  members:
  - name: 成员名1
    type: 成员类型
    desc: 成员描述
    # 如果成员是 "function"
    parameters:
    - name: 参数名1
      type: 参数类型
      desc: 参数描述
    - name: 参数名2
      type: 参数类型
      desc: 参数描述
    # 如果成员是 "function"
    returns:
    - name: 返回值名
      type: 返回值类型
      desc: 返回值描述
    examples:
    - desc: 成员使用示例1
    - desc: 成员使用示例2

  - name: 成员名2
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
