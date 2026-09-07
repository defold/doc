---
title: オンラインサービス
brief: このマニュアルでは、さまざまなゲームサービスやバックエンドサービスへの接続方法を説明します。
---
# ゲームサービス {#game-services}

HTTP リクエストやソケット接続を使うと、インターネット上の数千ものサービスに接続してやり取りできますが、多くの場合、単に HTTP リクエストを送信するだけでは済みません。通常は何らかの認証を行う必要があり、リクエストのデータを特定の形式に整えたり、レスポンスを利用する前に解析したりする必要がある場合もあります。もちろん、こうした処理は自分で実装できますが、代わりに処理してくれる拡張（extension）やライブラリ（library）もあります。以下に、特定のバックエンドサービスとのやり取りをより簡単にするために使える拡張の一部を紹介します。

## 汎用 {#general-purpose}
* [Colyseus](https://defold.com/assets/colyseus/) - マルチプレイヤーゲームのクライアントです。
* [Nakama](https://defold.com/assets/nakama/) - 認証、マッチメイキング、分析、クラウドセーブ、マルチプレイヤー、チャットなどの機能をゲームに追加します。
* [Photon Realtime](https://defold.com/assets/photon-realtime/) - Photon Realtime は、認証、マッチメイキング、高速で信頼性の高い通信など、不可欠な機能に対応するスケーラブルなソリューションを提供します。
* [PlayFab](https://defold.com/assets/playfabsdk/) - 認証、マッチメイキング、分析、クラウドセーブなどの機能をゲームに追加します。
* [AWS SDK](https://github.com/britzl/aws-sdk-lua) - ゲーム内から Amazon Web Services を利用します。

## 認証、リーダーボード、実績 {#authentication-leaderboards-achievements}
* [Google Play Game Services](https://defold.com/assets/googleplaygameservices/) - Google Play Game Services を使って、ゲーム内で認証やクラウドセーブを利用します。
* [Steamworks](https://defold.com/assets/steamworks/) - ゲームに Steam 対応を追加します。
* [Apple GameKit Game Center](https://defold.com/assets/gamekit/)

## 分析 {#analytics}
* [Firebase Analytics](https://defold.com/assets/googleanalyticsforfirebase/) - ゲームに Firebase Analytics を追加します。
* [Game Analytics](https://gameanalytics.com/docs/item/defold-sdk) - ゲームに GameAnalytics を追加します。
* [Google Analytics](https://defold.com/assets/gameanalytics/) - ゲームに Google Analytics を追加します。

さらに多くの拡張を探すには、[Asset Portal](https://www.defold.com/assets/) を確認してください！
