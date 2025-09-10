---
title: Defold库项目
brief: 库功能允许您在项目之间共享资源。本手册解释了其工作原理。
---

# 库

库功能允许您在项目之间共享资源。这是一个简单但非常强大的机制，您可以通过多种方式在工作流程中使用它。

库在以下情况下非常有用：

* 将资源从已完成的项目复制到新项目。如果您正在制作早期游戏的续作，这是一种简单的方法。
* 构建一个模板库，您可以将其复制到项目中，然后进行定制或专门化。
* 构建一个或多个包含现成对象或脚本的库，您可以直接引用它们。这对于存储通用脚本模块或构建共享的图形、声音和动画资源库非常方便。

## 设置库共享

假设您想要构建一个包含共享精灵和图块源的库。首先从[设置新项目](/manuals/project-setup/)开始。确定您要从项目中共享哪些文件夹，并将这些文件夹的名称添加到项目设置中的*`include_dirs`*属性中。如果您想列出多个文件夹，请用空格分隔名称：

![Include directories](images/libraries/libraries_include_dirs.png)

在我们能够将此库添加到另一个项目之前，我们需要一种定位库的方法。

## 库URL

库通过标准URL进行引用。对于托管在GitHub上的项目，它将是项目发布的URL：

![GitHub Library URL](images/libraries/libraries_library_url_github.png)

::: important
建议始终依赖库项目的特定版本，而不是主分支。这样，作为开发者，您可以决定何时合并库项目的更改，而不是总是从库项目的主分支获取最新的（可能具有破坏性的）更改。
:::

::: important
建议在使用前始终审查第三方库。了解更多关于[保护您对第三方软件的使用](https://defold.com/manuals/application-security/#securing-your-use-of-third-party-software)的信息。
:::

### 基本访问认证

可以在库URL中添加用户名和密码/令牌，以便在使用非公开库时执行基本访问认证：

```
https://username:password@github.com/defold/private/archive/main.zip
```

`username`和`password`字段将被提取并添加为`Authorization`请求头。这适用于任何支持基本访问认证的服务器。

::: important
确保不要共享或意外泄露您生成的个人访问令牌或密码，因为如果它们落入错误的手中，可能会造成严重后果！
:::

为避免在库URL中以明文形式泄露任何凭据，也可以使用字符串替换模式并将凭据存储为环境变量：

```
https://__PRIVATE_USERNAME__:__PRIVATE_TOKEN__@github.com/defold/private/archive/main.zip
```

在上面的示例中，用户名和令牌将从系统环境变量`PRIVATE_USERNAME`和`PRIVATE_TOKEN`中读取。

#### GitHub认证

要从GitHub上的私有仓库获取，您需要[生成个人访问令牌](https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/creating-a-personal-access-token)并将其用作您的密码。

```
https://github-username:personal-access-token@github.com/defold/private/archive/main.zip
```

#### GitLab认证

要从GitLab上的私有仓库获取，您需要[生成个人访问令牌](https://docs.gitlab.com/ee/security/token_overview.html)并将其作为URL参数发送。

```
https://gitlab.com/defold/private/-/archive/main/test-main.zip?private_token=personal-access-token
```

### 高级访问认证

使用基本访问认证时，用户的访问令牌和用户名将在用于项目的任何仓库上共享。对于超过1人的团队，这可能是一个问题。为了解决这个问题，需要使用一个"只读"用户来访问仓库的库，在GitHub上，这需要一个组织、一个团队和一个不需要编辑仓库的用户（因此是只读的）。

GitHub步骤：
* [创建组织](https://docs.github.com/en/github/setting-up-and-managing-organizations-and-teams/creating-a-new-organization-from-scratch)
* [在组织内创建团队](https://docs.github.com/en/github/setting-up-and-managing-organizations-and-teams/creating-a-team)
* [将所需的私有仓库转移到您的组织](https://docs.github.com/en/github/administering-a-repository/transferring-a-repository)
* [授予团队对仓库的"只读"访问权限](https://docs.github.com/en/github/setting-up-and-managing-organizations-and-teams/managing-team-access-to-an-organization-repository)
* [创建或选择一个用户作为此团队的一部分](https://docs.github.com/en/github/setting-up-and-managing-organizations-and-teams/organizing-members-into-teams)
* 使用上面的"基本访问认证"为此用户创建个人访问令牌

此时，新用户的认证详细信息可以提交并推送到仓库。这将允许任何使用您的私有仓库工作的人将其作为库获取，而无需对库本身具有编辑权限。

::: important
只读用户的令牌对于任何可以访问使用该库的游戏仓库的人都是完全可访问的。
:::

此解决方案在Defold论坛上提出并[在此线程中讨论](https://forum.defold.com/t/private-github-for-library-solved/67240)。

## 设置库依赖

打开您想要访问库的项目。在项目设置中，将库URL添加到*dependencies*属性中。如果需要，您可以指定多个依赖项目。只需使用`+`按钮一个一个地添加它们，并使用`-`按钮删除：

![Dependencies](images/libraries/libraries_dependencies.png)

现在，选择<kbd>Project ▸ Fetch Libraries</kbd>来更新库依赖。每当您打开项目时，这都会自动发生，因此只有当依赖项更改而不重新打开项目时，您才需要这样做。如果您添加或删除依赖库，或者如果某个依赖库项目被某人更改并同步，就会发生这种情况。

![Fetch Libraries](images/libraries/libraries_fetch_libraries.png)

现在，您共享的文件夹出现在*Assets*面板中，您可以使用您共享的所有内容。对库项目所做的任何同步更改都将在您的项目中可用。

![Library setup done](images/libraries/libraries_done.png)

## 编辑库依赖中的文件

库中的文件无法保存。您可以进行更改，编辑器将能够使用这些更改进行构建，这对于测试很有用。但是，文件本身保持不变，当文件关闭时，所有修改都将被丢弃。

如果您想要更改库文件，请确保创建您自己的库分支并在那里进行更改。另一个选择是将整个库文件夹复制/粘贴到您的项目目录中并使用本地副本。在这种情况下，您的本地文件夹将遮蔽原始依赖项，并且应该从`game.project`中删除依赖项链接（不要忘记之后选择<kbd>Project ▸ Fetch Libraries</kbd>）。

`builtins`也是引擎提供的一个库。如果您想要编辑那里的文件，请确保将它们复制到您的项目中并使用它们，而不是原始的`builtins`文件。例如，要修改`default.render_script`，将`/builtins/render/default.render`和`/builtins/render/default.render_script`都复制到您的项目文件夹中，作为`my_custom.render`和`my_custom.render_script`。然后，更新您的本地`my_custom.render`以引用`my_custom.render_script`而不是内置的，并在Render设置下的`game.project`中设置您的自定义`my_custom.render`。

如果您复制粘贴材质并希望跨某种类型的所有组件使用它，使用[每个项目的模板](/manuals/editor/#creating-new-project-files)可能很有用。

## 损坏的引用

库共享仅包括位于共享文件夹下的文件。如果您创建的内容引用了位于共享层次结构之外的资源，引用路径将被损坏。

## 名称冲突

由于您可以在*dependencies*项目设置中列出多个项目URL，您可能会遇到名称冲突。如果两个或更多依赖项目在*`include_dirs`*项目设置中共享一个同名的文件夹，就会发生这种情况。

Defold通过简单地忽略除对同名文件夹的最后一个引用之外的所有引用来解决名称冲突，顺序是项目URL在*dependencies*列表中指定的顺序。例如，如果您在依赖项中列出了3个库项目URL，并且它们都共享一个名为*items*的文件夹，则只会显示一个*items*文件夹——属于URL列表中最后一个项目的那个。
