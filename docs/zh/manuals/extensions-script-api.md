---
title: 为原生扩展提供编辑器代码提示
brief: 此手册介绍了如何创建脚本 API 定义，以便 Defold 编辑器能为用户提供代码提示功能.
---

# 原生扩展的代码提示

Defold 编辑器为所有 Defold API 功能以及用户引用的Lua模块提供代码提示. 但是编辑器无法为原生扩展暴露的功能. 原生扩展可以在单独一个文件里提供 API 定义来实现代码提示功能.


## 创建脚本 API 定义文件

脚本 API 定义文件使用扩展名 `.script_api`. 必须以 [YAML 格式](https://yaml.org/) 与扩展文件放在一起. 一般脚本 API 定义像这样:

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

数据类型有 `table, string , boolean, number, function` 几种. 如果一个值有多个类型则这样写 `[type1, type2, type3]`.
:::注意
目前编辑器里不显示类型. 但是还是鼓励输入类型以便以后编辑器可以显示出来.
:::

## 例子

实际使用实例参见下面的扩展:

* [Facebook 扩展](https://github.com/defold/extension-facebook/tree/master/facebook/api)
* [WebView 扩展](https://github.com/defold/extension-webview/blob/master/webview/api/webview.script_api)
