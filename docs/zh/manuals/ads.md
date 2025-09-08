---
title: 在 Defold 中展示广告
brief: 展示各种类型的广告是网页和手机游戏盈利的常见方式。本手册介绍了使用广告为游戏盈利的多种方法。
---

# 广告

广告已成为网页和手机游戏盈利的非常普遍的方式，并已发展成为一个价值数十亿美元的产业。作为开发者，你的收入基于观看游戏中广告的人数。通常情况很简单，观看者越多收入越多，但其他因素也会影响你的收入：

* 广告质量 - 相关广告更容易获得玩家的互动和关注。
* 广告格式 - 横幅广告通常收入较低，而从头到尾观看的全屏广告收入更高。
* 广告网络 - 你获得的收入因广告网络而异。

::: sidenote
CPM = 千人成本。广告商为每千次观看支付的金额。CPM因广告网络和广告格式而异。
:::

## 格式

游戏中可以使用许多不同类型的广告格式。一些更常见的格式是横幅广告、插页广告和奖励广告：

### 横幅广告

横幅广告基于文本、图像或视频，覆盖屏幕的相对较小部分，通常位于屏幕的顶部或底部。横幅广告非常容易实现，并且非常适合休闲单屏游戏，因为很容易为广告预留屏幕区域。横幅广告最大化了曝光率，因为用户可以在不中断游戏的情况下玩你的游戏。

### 插页广告

插页广告是带有动画的大型全屏体验，有时还包含交互式富媒体内容。插页广告通常在关卡之间或游戏会话之间展示，因为这是游戏体验中的自然中断。插页广告通常产生的观看次数少于横幅广告，但其成本（CPM）远高于横幅广告，从而带来可观的总体广告收入。

### 奖励广告

奖励广告（也称为激励广告）是可选的，因此比许多其他形式的广告侵入性更小。奖励广告通常是像插页广告一样的全屏体验。用户可以选择观看广告以换取奖励 - 例如战利品、硬币、生命、时间或其他游戏内货币或福利。奖励广告通常具有最高的成本（CPM），但观看次数直接与用户选择率相关。只有当奖励足够有价值并在适当时机提供时，奖励广告才能产生良好的效果。


## 广告网络

[Defold 资源门户](/tags/stars/ads/)包含几个与广告提供商集成的资源：

* [AdMob](https://defold.com/assets/admob-defold/) - 使用 Google AdMob 网络展示广告。
* [Enhance](https://defold.com/assets/enhance/) - 支持多种不同的广告网络。需要额外的构建后步骤。
* [Facebook Instant Games](https://defold.com/assets/facebookinstantgames/) - 在你的 Facebook Instant Game 中展示广告。
* [IronSource](https://defold.com/assets/ironsource/) - 使用 IronSource 广告网络展示广告。
* [Unity Ads](https://defold.com/assets/defvideoads/) - 使用 Unity Ads 网络展示广告。


# 如何在游戏中整合广告

当你决定要在游戏中整合广告网络后，你需要遵循该特定资源的安装和使用说明。通常你要做的是首先将该扩展添加为[项目依赖](/manuals/libraries/#设置库依赖)。一旦将资源添加到项目中，你就可以继续进行集成，并调用特定于该资源的函数来加载和展示广告。


# 结合广告和应用内购买

在手机游戏中，提供[应用内购买](/manuals/iap)以永久移除广告是相当常见的。


## 了解更多

有许多在线资源可供学习优化广告收入：

* Google AdMob [Monetize mobile games with ads](https://admob.google.com/home/resources/monetize-mobile-game-with-ads/)
* Game Analytics [Popular ad formats and how to use them](https://gameanalytics.com/blog/popular-mobile-game-ad-formats.html)
* deltaDNA [Ad serving in games: 10 expert tips](https://deltadna.com/blog/ad-serving-in-games-10-tips/)
