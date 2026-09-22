---
title: ネイティブ拡張にエディターの自動補完を追加する
brief: このマニュアルでは、拡張の利用者に Defold エディターでの自動補完を提供するために、スクリプト API 定義を作成する方法を説明します。
---

# ネイティブ拡張の自動補完 {#auto-complete-for-native-extensions}

Defold エディターは、すべての Defold API 関数の補完候補を提示し、スクリプトで読み込む Lua モジュールの補完候補も生成します。ただし、エディターはネイティブ拡張（native extension）が公開する機能の補完候補を自動的に提示することはできません。ネイティブ拡張では、別のファイルで API 定義を提供することで、その拡張の API についても補完候補を有効にできます。


## スクリプト API 定義の作成 {#creating-a-script-api-definition}

スクリプト API 定義（script API definition）ファイルの拡張子は `.script_api` です。このファイルは [YAML 形式](https://yaml.org/) で記述し、拡張のファイルとともに配置する必要があります。スクリプト API 定義の形式は次のとおりです。

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

型には `table, string , boolean, number, function` のいずれかを指定できます。値が複数の型を取れる場合は、`[type1, type2, type3]` と記述します。
::: sidenote
現在、型はエディターに表示されません。エディターが型情報の表示に対応した際に利用できるよう、型を記述しておくことをお勧めします。
:::

## 例 {#examples}

実際の使用例については、次のプロジェクトを参照してください。

* [Facebook 拡張](https://github.com/defold/extension-facebook/tree/master/facebook/api)
* [WebView 拡張](https://github.com/defold/extension-webview/blob/master/webview/api/webview.script_api)
