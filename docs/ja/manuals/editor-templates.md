---
title: エディターのテンプレート
brief: New Project ウィンドウに独自のカスタムプロジェクトテンプレートを追加できます。
---

# エディターのテンプレート {#editor-templates}

New Project ウィンドウに独自のカスタムプロジェクトテンプレート（project template）を追加できます。

![カスタムプロジェクトテンプレート](images/editor/custom_project_templates.png)

カスタムプロジェクトテンプレートを含む新しいタブを1つ以上追加するには、ユーザーのホームディレクトリ内の `.defold` フォルダーに `welcome.edn` ファイルを追加する必要があります。

* ユーザーのホームディレクトリに `.defold` という名前のフォルダーを作成します。
  * Windows では `C:\Users\**Your Username**\.defold`
  * macOS では `/Users/**Your Username**/.defold`
  * Linux では `~/.defold`
* `.defold` フォルダーに `welcome.edn` ファイルを作成します。

`welcome.edn` ファイルは Extensible Data Notation 形式を使用します。次に例を示します。

```
{:new-project
  {:categories [
    {:label "My Templates"
     :templates [
          {:name "My project"
           :description "My template with everything set up the way I want it."
           :image "empty.svg"
           :zip-url "https://github.com/britzl/template-project/archive/master.zip"
           :skip-root? true},
          {:name "My other project"
           :description "My other template with everything set up the way I want it."
           :image "empty.svg"
           :zip-url "https://github.com/britzl/template-other-project/archive/master.zip"
           :skip-root? true}]
    }]
  }
}
```

これにより、上のスクリーンショットに示したテンプレートの一覧が作成されます。

::: sidenote
テンプレートの画像には、[エディターに同梱されている画像](https://github.com/defold/defold/tree/dev/editor/resources/welcome/images)のみ使用できます。
:::
