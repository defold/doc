---
title: Defold 的应用内通信
brief: 应用内通信可以让你获得应用启动时的启动参数信息. 本教程解释了Defold中此功能的API.
---

# 应用内通信

大多数操作系统中应用可以由以下方式启动:

* 从已安装应用表中启动
* 从应用链接启动
* 从推送消息中启动
* 在安装程序最后一步启动.

从链接，通知，安装程序启动应用时可以获得引用，比如安装时的快捷方式或者超级链接，通知里的长链接. Defold 使用一个native extension提供一个统一的方法来获得应用是如何启动的相关信息.

## 安装扩展

要使用应用内通信扩展程序你需要在你的 `game.project` 里添加一个依赖. 此依赖的URL是:
```
https://github.com/defold/extension-iac/archive/master.zip
```

推荐使用zip包的链接来[指定版本](https://github.com/defold/extension-iac/releases).

## 使用扩展

API很简单. 提供给扩展程序一个回调用的监听器函数.

```
local function iac_listener(self, payload, type)
     if type == iac.TYPE_INVOCATION then
         -- This was an invocation
         print(payload.origin) -- origin may be empty string if it could not be resolved
         print(payload.url)
     end
end

function init(self)
     iac.set_listener(iac_listener)
end
```

API完整文档在[此页面](https://defold.github.io/extension-iac/).
