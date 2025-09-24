---
title: Defold应用间通信
brief: 应用间通信允许您获取启动应用程序时使用的启动参数。本手册解释了Defold中用于此功能的API。
---

# 应用间通信

应用程序在大多数操作系统上可以通过多种方式启动：

* 从已安装应用程序列表
* 从应用程序特定链接
* 从推送通知
* 作为安装过程的最后一步。

在应用程序从链接、通知或安装启动的情况下，可以传递额外的参数，例如安装时的安装来源或从应用程序特定链接或通知启动时的深度链接。Defold提供了一种统一的方式来获取有关应用程序如何被调用的信息，使用原生扩展。

## 安装扩展

要开始使用应用间通信扩展，您需要将其作为依赖项添加到您的*game.project*文件中。最新稳定版本的依赖URL是：
```
https://github.com/defold/extension-iac/archive/master.zip
```

我们建议使用[特定版本](https://github.com/defold/extension-iac/releases)的zip文件链接。

## 使用扩展

API非常易于使用。您为扩展提供一个监听器函数并对监听器回调做出反应。

```
local function iac_listener(self, payload, type)
     if type == iac.TYPE_INVOCATION then
         -- 这是一个调用
         print(payload.origin) -- 如果无法解析，origin可能是空字符串
         print(payload.url)
     end
end

function init(self)
     iac.set_listener(iac_listener)
end
```

API的完整文档可在[扩展GitHub页面](https://defold.github.io/extension-iac/)上找到。
