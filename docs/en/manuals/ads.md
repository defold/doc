---
title: Showing ads in Defold
brief: Showing various kinds of ads is a common way to monetize web and mobile games. This manual shows a number of ways to monetize your game using ads.
---

# Ads

Ads has become a very common way of monetizing web and mobile games and it has turned into a billion dollar industry. As a developer you get paid based on the number of people watching the ads you show in your game. It is usually as simple as more viewers equals more money, but other factors also have an impact on how much you get paid:

* The ad quality - relevant ads are more likely to get interaction and attention from your players.
* The ad format - banner ads usually pay less while full screen ads viewed from start to to finish pays more.
* The ad network - the amount you get paid varies from ad networks to ad network.

::: sidenote
CPM = Cost per mille. The amount an advertiser pays per one thousand views. The CPM varies between ad networks and ad formats.
:::

## Formats

There are many different kinds of ad formats that can be used in games. Some of the more common ones are banner, interstitial and reward ads:

### Banner ads

Banner ads are text, image or video based and cover a relatively small part of the screen, usually at the top or bottom of the screen. Banner ads are very easy to implement and they fit very well with casual single screen games where it is easy to reserve an area of the screen for advertisements. Banner ads maximize exposure as users play your game without interruption.

### Interstitial ads

Interstitial ads are large full screen experiences with animations and sometimes also interactive rich media content. Interstitial ads are typically shown in between levels or game sessions as it is a natural break in the game experience. Interstitial ads typically generate less views than banner ads, but the cost (CPM) is much higher than for banner ads, resulting in significant overall ad revenue.

### Rewarded ads

Rewarded ads (also know as Incentivized ads) are optional and therefore less obtrusive than many other forms of ads. Rewarded ads are usually full screen experiences like interstitial ads. The user can choose a reward in exchange for viewing the ad - for instance loot, coins, lives, time or some other in-game currency or benefit. Rewarded ads usually has the highest cost (CPM), but the number of views is directly related to user opt-in rates. Rewarded ads will only generate great performance if the rewards are valuable enough and offered at the right time.


## Ad networks

The [Defold Asset Portal](/tags/stars/ads/) contains several assets which integrate with ad providers:

* [AdMob](https://defold.com/assets/admob-defold/) - Show ads using the Google AdMob network.
* [Enhance](https://defold.com/assets/enhance/) - Supports a number of different ad networks. Requires an additional post-build step.
* [Facebook Instant Games](https://defold.com/assets/facebookinstantgames/) - Show ads in your Facebook Instant Game.
* [IronSource](https://defold.com/assets/ironsource/) - Show ads using the IronSource Ad network.
* [Unity Ads](https://defold.com/assets/defvideoads/) - Show ads using the Unity Ads network.


# How to integrate ads in your game

When you have decided on an ad network to integrate in your game you need to follow the installation and usage instructions for that particular asset. What you typically do is to first add the extension as a [project dependency](/manuals/libraries/#setting-up-library-dependencies). Once you have the asset added to your project you can proceed with the integration and call the functions specific to the asset to load and show ads.


# Combining ads and in-app purchases

It is quite common in mobile games to offer an [In-app purchase](/manuals/iap) to get rid of ads permanently.


## Learn more

There are many online resources to learn from when it comes to optimizing ad revenue:

* Google AdMob [Monetize mobile games with ads](https://admob.google.com/home/resources/monetize-mobile-game-with-ads/)
* Game Analytics [Popular ad formats and how to use them](https://gameanalytics.com/blog/popular-mobile-game-ad-formats.html)
* deltaDNA [Ad serving in games: 10 expert tips](https://deltadna.com/blog/ad-serving-in-games-10-tips/)
