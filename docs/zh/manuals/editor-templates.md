---
title: 编辑器模板
brief: 您可以在新建项目窗口中添加自己的自定义项目模板。
---

# 编辑器模板

您可以在新建项目窗口中添加自己的自定义项目模板：

![custom project templates](images/editor/custom_project_templates.png)

为了添加一个或多个带有自定义项目模板的新标签页，您需要在用户主目录的 `.defold` 文件夹中添加一个 `welcome.edn` 文件：

* 在您的用户主目录中创建一个名为 `.defold` 的文件夹。
  * 在 Windows 上：`C:\Users\**您的用户名**\.defold`
  * 在 macOS 上：`/Users/**您的用户名**/.defold`
  * 在 Linux 上：`~/.defold`
* 在 `.defold` 文件夹中创建一个 `welcome.edn` 文件。

`welcome.edn` 文件使用可扩展数据表示法（Extensible Data Notation）格式。示例：

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

这将创建如上截图所示的模板列表。

::: sidenote
您只能使用[随编辑器一起提供的模板图片](https://github.com/defold/defold/tree/dev/editor/resources/welcome/images)。
:::
