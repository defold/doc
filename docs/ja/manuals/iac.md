---
title: Defold のアプリ間通信
brief: アプリ間通信を使うと、アプリケーションの起動時に渡された起動引数を取得できます。このマニュアルでは、この機能を利用するための Defold の API について説明します。
---

# アプリ間通信 {#inter-app-communication}

ほとんどのオペレーティングシステムでは、アプリケーションを次のような方法で起動できます。

* インストール済みアプリケーションの一覧から
* アプリケーション固有のリンクから
* プッシュ通知から
* インストール処理の最後のステップとして

リンクや通知から、またはインストール時にアプリケーションを起動する場合は、追加の引数を渡せます。たとえば、インストール時のインストールリファラー（install referrer）や、アプリケーション固有のリンクまたは通知から起動する際のディープリンク（deep-link）です。Defold では、ネイティブ拡張（native extension）を使って、アプリケーションがどのように起動されたかという情報を統一された方法で取得できます。

## 拡張のインストール {#installing-the-extension}

アプリ間通信（Inter-app communication）拡張を使い始めるには、*game.project* ファイルに依存関係として追加する必要があります。最新の安定版は、次の依存関係 URL で入手できます。
```
https://github.com/defold/extension-iac/archive/master.zip
```

[特定のリリース](https://github.com/defold/extension-iac/releases)の zip ファイルへのリンクを使うことをお勧めします。

## 拡張の使用 {#using-the-extension}

API の使い方はとても簡単です。拡張にリスナー関数を登録し、リスナーのコールバックに応じて処理します。

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

API の完全なドキュメントは、[拡張の GitHub ページ](https://defold.github.io/extension-iac/)で参照できます。
