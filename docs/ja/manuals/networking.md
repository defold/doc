---
title: Defold のネットワーク通信
brief: このマニュアルでは、リモートサーバーへの接続や、その他の種類のネットワーク接続を行う方法を説明します。
---

# ネットワーク通信 {#networking}

ゲームが何らかのバックエンドサービスに接続することは珍しくありません。たとえば、スコアを送信したり、マッチメイキングを処理したり、セーブデータをクラウドに保存したりします。また、多くのゲームでは、中央のサーバーを介さずにゲームクライアント同士が直接通信するピアツーピア接続も使われています。ネットワーク接続やデータのやり取りには、さまざまなプロトコルや規格を使うことができます。Defold でネットワーク接続を利用する各種の方法については、以下を参照してください。

* [HTTP リクエスト](/manuals/http-requests)
* [ソケット接続](/manuals/socket-connections)
* [WebSocket 接続](/manuals/websocket-connections)
* [オンラインサービス](/manuals/online-services)


## 技術的な詳細 {#technical-details}

### IPv4 と IPv6 {#ipv4-and-ipv6}

Defold は、ソケットと HTTP リクエストで IPv4 および IPv6 による接続をサポートしています。

### セキュアな接続 {#secure-connections}

Defold は、ソケットと HTTP リクエストでセキュアな SSL 接続をサポートしています。

Defold は、オプションでセキュアな接続の SSL 証明書を検証することもできます。*game.project* の Network セクションにある [SSL Certificates 設定](/manuals/project-settings/#network)) のフィールドに、CA ルート証明書の公開鍵または自己署名証明書の公開鍵を含む PEM ファイルを指定すると、SSL 検証が有効になります。CA ルート証明書の一覧は `builtins/ca-certificates` に含まれていますが、新しい PEM ファイルを作成し、ゲームの接続先サーバーに応じて必要な CA ルート証明書をコピーして貼り付けることをお勧めします。

