---
title: 项目模板
brief: 在编辑器新建项目窗口中可以加入自定义模板.
---

# 项目模板

在编辑器新建项目窗口中可以加入自定义模板.:

![custom project templates](images/editor/custom_project_templates.png)

要在窗口中添加自定义项目模板页需要在系统用户目录的 `.defold` 文件夹下加入 `welcome.edn` 文件:

* 找到系统用户目录下 `.defold`文件夹的位置:
  * Windows `C:\Users\**Your Username**\.defold`
  * macOS `/Users/**Your Username**/.defold`
  * Linux `~/.defold`
* 在 `.defold` 文件夹下新建 `welcome.edn` 文件.

`welcome.edn` 文件使用的是可扩展数据注解格式. 例如:

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

这样就建立好了如上图的模板列表.

::: sidenote
模板图片只能使用 [编辑器自带的图片](https://github.com/defold/defold/tree/dev/editor/resources/welcome/images).
:::
