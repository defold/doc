---
title: Defold 中库的使用
brief: 项目间可以使用库共享资源. 本教程解释了其工作方式.
---

# 库

库实现了项目间共享资源. 在工作流中使用库方便而更有效率.

库在以下情形下很有用:

* 把已完成项目的资源复制到新建项目里使用. 如果要为你的游戏出续集, 很需要这种方法.
* 编译一个模板的库以便导入到项目中再定制使用.
* 编译一些包含做好了的对象和脚本的库以便直接使用. 对于保存通用脚本模块或者创建共享资源非常有用.

## 库共享设置

比如你想创建一个包含共享 sprite 和瓷砖图源的库. 先从 [新建项目设置](/manuals/project-setup/) 开始. 确定项目中你要共享的文件夹然后把它加入到项目设置的 *include_dirs* 属性列表里. 如果需要加入多个, 以空格分隔文件夹名称:

![Include dirs](images/libraries/libraries_include_dirs.png)

我们需要先定位库才能把它导入到项目里.

## 库地址

库使用标准 URL 来引用. 对于托管在 GitHub 上的项目, 就是项目发布的 URL:

![GitHub Library URL](images/libraries/libraries_library_url_github.png)

::: 注意
最好使用库项目的发布地址而不是主分支来引用库. 作为开发者你要决定什么时候该合并更新而不是时刻保持主分支最新代码 (使用主分支最新版可能引入潜在的不稳定性).
:::


### 基本訪問驗證

對於不公開的庫可以通過在 URL 上加入用戶名密碼 / 訪問權token的方法來訪問:

```
https://username:password@github.com/defold/private/archive/main.zip
```

這裏 `username` 和 `password` 項會被提取並轉化爲 `Authorization` 請求頭. 這種方法一般服務器都適用. 包括從 GitHub 上獲取私有庫. GitHub 還支持使用 [生成訪問權token](https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/creating-a-personal-access-token) 的方法來代替密碼.

```
https://github-username:personal-access-token@github.com/defold/private/archive/main.zip
```

::: 注意
不要共享或者不小心泄露你的密碼或訪問權token, 否則可能會落入他人之手造成不良後果.
:::

为避免泄密在库 URL 上的明文用户名密码字符串可以使用环境变量代替:

```
https://__PRIVATE_USERNAME__:__PRIVATE_TOKEN__@github.com/defold/private/archive/main.zip
```

上面的例子里用户名和令牌会被替换为环境变量 `PRIVATE_USERNAME` 和 `PRIVATE_TOKEN` 的值.


### 严格访问权限

基本訪問权限下token和用户名都在项目依赖库上公开. 这对于多人开发团队来说可能会造成麻烦. 解决办法是给库引入一个 "只读" 用户, 在 GitHub 上可以设置一个机构, 一个团队以及一个不需要编辑代码的用户 (也就是只读用户).

GitHub 具体步骤:
* [创建机构](https://docs.github.com/en/github/setting-up-and-managing-organizations-and-teams/creating-a-new-organization-from-scratch)
* [机构之下的团队](https://docs.github.com/en/github/setting-up-and-managing-organizations-and-teams/creating-a-team)
* [把需要的私有库存放到机构之下](https://docs.github.com/en/github/administering-a-repository/transferring-a-repository)
* [将开发团队设置为对库 "只读"](https://docs.github.com/en/github/setting-up-and-managing-organizations-and-teams/managing-team-access-to-an-organization-repository)
* [创建只读团队的只读用户成员](https://docs.github.com/en/github/setting-up-and-managing-organizations-and-teams/organizing-members-into-teams)
* 给只读用户发放 "基本访问权限" token

此时这个只读用户的信息就可以放心公开在依赖库上. 这样就可以将私有库公开化而不用担心被恶意篡改.

::: 注意
使用这种只读用户的 token 可以访问所有依赖私有库的游戏.
:::

上述解决方案于 Defold 论坛提出并 [于此帖子上进行谈论](https://forum.defold.com/t/private-github-for-library-solved/67240).

## 设置库依赖

打开需要引入库的项目. 在项目设置里, 把 URL 加入到 *dependencies* 属性下. 如果需要可以加入多个. 使用 `+` 按钮一个一个加入, 使用 `-` 按钮移除:

![Dependencies](images/libraries/libraries_dependencies.png)

然后, 选择 <kbd>Project ▸ Fetch Libraries</kbd> 来更新库依赖. 这项工作会在打开项目时自动执行所以只有当库需要更新而不想重新打开项目时才会用到这个命令. 比如你修改了库依赖或者库本身被修改和同步了的时候.

![Fetch Libraries](images/libraries/libraries_fetch_libraries.png)

此时你共享的文件夹就会出现在资源面板中等待使用. 库的各种修改都会同步到你的项目之中.

![Library setup done](images/libraries/libraries_done.png)

## 引用破坏

共享库仅限于使用共享文件夹下的文件. 如果你引用了共享文件夹之外的资源, 则共享引用就会被破坏.

## 命名冲突

如果项目设置 *dependencies* 中引用了很多库你可能会遇到命名冲突的情况. 如果两个或者多个项目的项目设置中 *include_dirs* 里包含的共享文件夹名一样就会造成这种情况.

Defold 解决库命名冲突的办法很简单, 除了 *dependencies* 列表中最后一个, 其他都忽略掉. 比如说. 你的项目依赖3个库, 每个库都有一个叫做 *items* 的共享文件夹, 则只有一个 *items* 文件夹会被显示出来---那就是处于 URL 列表里的最后一个.
