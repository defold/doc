---
title: 在 Defold 中播放广告
brief: 广告是网页游戏和手机游戏的基本盈利方式. 本教程介绍了在 Defold 中如何通过广告盈利.
---

# 广告

广告作为网页游戏和手机游戏的一种普遍盈利方式日趋壮大. 玩家观看游戏里的广告, 开发者有机会获利. 一般看的越多获利越多, 但是最终受益还要取决于下面几项:

* 广告质量 - 游戏内容相关的广告容易获得玩家点击与关注.
* 广告类型 - 广告条的利润低而从头看到尾的全屏广告利润高.
* 广告商 - 不同广告供应商的广告利润有高有低.

::: 注意
CPM = 千人成本. 广告商为一千个浏览量支付的报酬. 不同广告商不同广告类型费用也不同.
:::

## 类型

游戏中可以放各种广告. 常见的有广告条, 插播广告和奖励广告:

### 广告条

广告条可以是文字的, 图片的或者视频的并且占据一部分屏幕, 一般不是屏幕上边就是底边. 广告条很容易植入, 休闲小游戏也容易空出广告条的位置来. 曝光率高, 玩家反感较少.

### 插播广告

插播广告是一种带动画有的还有多媒体交互的全屏广告. 插播广告通常出现在游戏关与关之间或者游戏暂停等时候. 插播广告曝光不高, 但是付费较高, 可以带来不菲收入.

### 奖励广告

奖励广告 (也叫激励广告) 是一种玩家最不反感的广告. 样子通常跟插播广告类似. 玩家可以通过观看广告获得游戏虚拟奖励 - 比如财产, 金币, 命, 游戏延时等等. 奖励广告通常付费最高, 但是观看率取决于玩家. 在关键时刻给予玩家渴望的奖励才能取得激励的效果.


## 广告商

在 [Defold 资源中心](/tags/stars/ads/) 提供了一些广告商的支持程序:

* [AdMob](https://defold.com/assets/admob/) - 谷歌广告.
* [Enhance](https://defold.com/assets/enhance/) - 广告商大集合. 编译后需要额外的安装步骤.
* [Facebook Instant Games](https://defold.com/assets/facebookinstantgames/) - 脸书广告.
* [IronSource](https://defold.com/assets/ironsource/) - IronSource 广告.
* [Unity Ads](https://defold.com/assets/defvideoads/) - Unity 广告.


# 广告游戏整合

决定好合作广告商就可以按步骤地植入广告资源了. 一般都要首先加入 [项目依赖](/manuals/libraries/#设置库依赖). 之后载入广告资源, 展示广告内容.


# 广告与内支付

手机游戏通常含有 [应用内支付](/manuals/iap) 功能以便获得更大收益.


## 更多资源

网上也有很多关于优化广告的教程:

* Google AdMob [Monetize mobile games with ads](https://admob.google.com/home/resources/monetize-mobile-game-with-ads/)
* Game Analytics [Popular ad formats and how to use them](https://gameanalytics.com/blog/popular-mobile-game-ad-formats.html)
* deltaDNA [Ad serving in games: 10 expert tips](https://deltadna.com/blog/ad-serving-in-games-10-tips/)
