---
title: エンジンサービスとランタイム HTTP API
brief: このマニュアルでは、実行中の Defold デバッグエンジンが提供する開発用 HTTP サービスと、ランタイム拡張や外部ツールによるその利用方法を説明します。
---

# エンジンサービスとランタイム HTTP API {#the-engine-service-and-runtime-http-apis}

Debug モードでプロジェクトを実行すると、ゲームと特別なエンジンサービス（engine service）を含む、特定のエンジンのランタイムインスタンス用のプロセスが作成されます。このサービスにアクセスすると、開発とプロファイリングの基盤、実行時のロジックとメッセージ、エンジンの状態、拡張機能を扱えます。

エンジンサービスは、実行中のデバッグエンジンまたはヘッドレスエンジン（`dmengine` または `dmengine_headless`）が提供する開発用 HTTP サービスです。

Defold エディターに属し、開いているプロジェクトを制御する[エディターサーバー（editor server）](/manuals/editor-http-api)とは別のサービスです。

2つのサービスは異なるポートを使います。エディターのポートに接続するツールは、そのポートでランタイム拡張のルートを呼び出せません。逆も同様で、エンジンサービスに接続するツールはエディターの操作を呼び出せません。

エンジンサービスは、デバッグ、開発、プロファイリングの基盤の一部です。リリースエンジンのインスタンスは、このサービスを作成しません。

## 利用条件とポートの検出 {#availability-and-port-discovery}

エディターがデバッグエンジンを起動するときは、動的に割り当てるサービスポートを要求します。選択されたポートは *Console* に表示され、CLI から実行した場合はログに記録されます。

![Defold のデバッグビルドに表示されるエンジンサービスのポート情報](images/automation/engine-service.png)

```text
INFO:ENGINE: Engine service started on port <port>
```

エンジンは、実際のアドレスと割り当てられたポートを使った OpenAPI 検出用の完全な URL も記録します。

```text
INFO:ENGINE: OpenAPI: http://<address>:<port>/openapi.json
```

エディターからゲームを起動した場合、これらの行はエディターのコンソールに表示されます。単純なローカルの制御ツールはこれらを解析できますが、再利用可能な連携では、エディターまたはそのラッパーがエンジンインスタンスと登録されたポートを追跡するようにします。これにより、古いポートを新しく起動したプロセスや再利用されたプロセスと取り違えることを防げます。

エンジンは、対応するプラットフォームではサービス検出を通じて開発ターゲットの存在も通知します。この仕組みは主に Defold のツールが使用するもので、常に固定のポートをハードコードする方法で置き換えることは推奨しません。

サーバーには、localhost（`127.0.0.1`）の指定されたポートでアクセスできます:

![エンジンサーバーへのアクセス](images/automation/engine-server.png)

## OpenAPI による操作の検出 {#discovering-operations-through-openapi}

`GET /openapi.json` は、ランタイム HTTP API を記述した OpenAPI 3.0.3 ドキュメントを返します。ログに表示されたエンジンサービスのポートを使います。ローカルのエンジンでは、以下の `<port>` をそのポートに置き換えてください。

```sh
ENGINE_URL="http://127.0.0.1:<port>"
curl -fsS "$ENGINE_URL/openapi.json" | jq
```

このドキュメントは、現在登録されているハンドラーが提供するパス、メソッド、パラメーター、リクエストボディ、レスポンスを記述します。OpenAPI メタデータを提供するネイティブ拡張も含まれます。ハンドラーを追加または削除すると `paths` オブジェクトが変化します。プロファイラーや拡張のルートは、実行中のエンジンのプラットフォーム、設定、登録済みの拡張に依存するため、使用するインスタンスからドキュメントを取得してください。

OpenAPI メタデータなしで登録したハンドラーも呼び出せますが、ドキュメントには表示されません。記載されたルートでも、機能を利用できないと報告する場合があります。プラットフォームに依存する操作を使う前に、レスポンスの説明と、利用可能な機能を調べるエンドポイントを確認してください。

エディターには、エディターのポートで提供する独自の [OpenAPI ドキュメント](/manuals/editor-http-api/#discovering-operations-through-openapi)があります。実行時の操作には、エンジン側のドキュメントを使います。

## 組み込みエンドポイント {#built-in-endpoints}

現在のデバッグエンジンは、少数の基本ルートを登録します。

| エンドポイント | 用途 |
| --- | --- |
| `GET /openapi.json` | OpenAPI メタデータを提供する、現在登録済みのランタイム HTTP 操作を検出します |
| `GET /ping` | エンジンサービスが応答することを確認します。 |
| `GET /info` | エンジンのバージョン、プラットフォーム、ビルド識別子、ログサービスの情報を読み取ります。 |
| `GET /state` | Defold のツールが使用する開発用の接続状態を読み取ります。 |
| `POST /post/<socket>/<message-type>` | Protobuf でエンコードした Defold メッセージを、エンジンの名前付きソケット（socket）に送信します。 |

例:

```sh
curl -sS "$ENGINE_URL/ping"
curl -sS "$ENGINE_URL/info" | jq
curl -sS "$ENGINE_URL/state" | jq
```

`/post` ルートは、ホットリロード（hot reload）、再起動、サイズ変更、プロセス制御などの開発操作で使用されます。リクエスト本文は、ルートで指定された型のバイナリ Protobuf メッセージです。JSON メッセージ API ではありません。Protobuf メッセージは、シリアライズ後のサイズが 1024 バイト以下である必要があります。これを超えると、`400 Too large message` が返されます。

これらのルートは開発の基盤であり、エンジンの実装にはプロファイラーやリソースの調査用のルートもあります。

## 録画用エンドポイント {#recording-endpoints}

デスクトップのデバッグエンジンでは、次のルートを通じてネイティブ MP4 録画も利用できます。リリース、ヘッドレス、モバイル、Web の各ビルドと、[App Manifest](/manuals/app-manifest/#exclude-record) で **Exclude Record** が有効な場合には含まれません。

| エンドポイント | 用途 |
| --- | --- |
| `GET /recording/capabilities` | 動画・音声の対応状況、バックエンドの要件、録画サービスの `instance_id` を調べます |
| `GET /recording/status` | 現在の操作、非同期の進行状況、確定済みファイルの情報を読み取ります |
| `POST /recording/start` | 録画を要求し、その `operation_id` を受け取ります |
| `POST /recording/stop` | 指定した操作の停止とファイルの確定を要求します |
| `GET /recording/files/{id}` | 確定済みの MP4 をダウンロードします |
| `DELETE /recording/files/{id}` | サービスが保持している完了済みファイルを削除します |

`/openapi.json` でこれらのルートを検出し、`/recording/capabilities` で現在のプラットフォームの対応状況を確認します。録画状態を変更する操作には `X-Recording-Instance` ヘッダーが必要で、停止には受理された `operation_id` も必要です。開始と停止は非同期です。ファイルが確定するまで待ってからダウンロードしてください。一連の手順は[録画マニュアル](/manuals/recording/#recording-through-http)を参照してください。

HTTP サービスは、Lua とレコーダーを共有します。HTTP から開始すると、対応している場合はアプリケーション音声をデフォルトで有効にします。Lua からの開始は、デフォルトでは動画のみです。ダウンロード可能な `file` 情報を持つのは、HTTP から開始した録画のみです。ダウンロード前に `pending: false`、`finalized: true`、`file.state: "complete"` を待ち、[ファイルサイズと SHA-256 を検証](/manuals/recording/#download-and-release-the-file)します。Lua と HTTP クライアントを組み合わせる場合は、[レコーダーの共有](/manuals/recording/#sharing-the-recorder-with-http-clients)を参照してください。

## Metal GPU トレース用エンドポイント {#metal-gpu-trace-endpoint}

macOS では、デバッグエンジンが Metal GPU トレースをキャプチャする `/profiler/gputrace` を公開します。このルートが `/openapi.json` に現れるのは macOS のみです。キャプチャにはネイティブの Metal アダプターと、エンジン起動時の環境変数 `METAL_CAPTURE_ENABLED=1` が必要です。キャプチャを利用できない場合、リクエストには `error.code: "gputrace_unsupported"` を含む HTTP 501 を返します。

| エンドポイント | 用途 |
| --- | --- |
| `POST /profiler/gputrace` | 書き込み可能な絶対パスの `.gputrace` へのキャプチャを予約します。`frames` のデフォルトは `1` で、`1`～`10000` を指定できます。 |
| `GET /profiler/gputrace` | 現在または直近のキャプチャの状態、パス、フレーム数を読み取ります。 |
| `DELETE /profiler/gputrace` | 保留中のキャプチャを取り消すか、実行中なら現在のレンダリングフレーム後に終了します。トレースはディスクに保持します。 |

受理したリクエストには、`ok: true` と `data` オブジェクトを含む HTTP 200 を返します。キャプチャは非同期で進むため、`data.state` が `complete`、`canceled`、`failed` のいずれかになるまで `GET` をポーリングします。ネイティブ側の起動失敗は `data.error` で報告します。トレースはエンジンのホストに書き込みます。起動コマンド、対応状況の検出、キャプチャの例、結果を Xcode で開く方法は、[Metal GPU トレースのキャプチャガイド](/manuals/profiling/#metal-gpu-trace-capture)を参照してください。

## 拡張機能で定義するランタイムルート {#extension-defined-runtime-routes}

デバッグビルドでは、ネイティブ拡張（native extension）SDK からエンジンの Web サーバーにアクセスできます。拡張機能は、そのサーバーにルートプレフィックスを登録し、ランタイムデータに依存する操作を公開できます。

拡張機能は別の HTTP サーバーを開かずに既存のエンジンサービスを共有できるため、開発ツールに役立ちます。

拡張機能で定義するランタイム自動化 API には、次を推奨します:

* 他と区別できる、バージョン付きのルートプレフィックスを使用します。
* サポートする機能を公開します。
* 構造化されたエラーを返します。
* プラットフォームの機能やエンジンの機能が利用できない場合を明示的に処理します。
* 操作を開発とテストのローカル環境に限定します。
* リリースビルドから除外されるかどうかを明記します。

### 拡張の操作を OpenAPI で公開する {#publishing-extension-operations-in-openapi}

ネイティブ拡張のアプリケーション初期化コールバックで、`dmEngine::GetWebServer(app_params)` によりサーバーを取得し、返されたハンドルが非 null の場合にのみハンドラーを登録します。コールバックの設定は、[拡張のライフサイクル](/manuals/extensions/#extension-lifecycle)を参照してください。

引数が4つの `dmWebServer::AddHandler()` オーバーロードは、OpenAPI 3.0.3 の Paths Object を JSON 文字列として受け取ります。このオブジェクトの最上位キーはルートパスです。各パスは登録されたプレフィックスで始まる必要があり、ほかのハンドラーによって記述済みであってはいけません。インラインのスキーマか、生成されるドキュメント内のパスへの参照を使います。

たとえば、次のヘルパーは、コールバックと、そのステータスエンドポイントの説明を登録します。

```cpp
#include <dmsdk/dlib/webserver.h>

static const char STATUS_OPENAPI[] = R"json(
{
  "/example/v1/status": {
    "get": {
      "summary": "Get extension status",
      "responses": {
        "200": {
          "description": "Current extension status",
          "content": {
            "text/plain": {
              "schema": { "type": "string" }
            }
          }
        }
      }
    }
  }
}
)json";

dmWebServer::Result RegisterStatusHandler(dmWebServer::HServer server,
                                        dmWebServer::Handler callback,
                                        void* context)
{
    dmWebServer::HandlerParams params;
    params.m_Handler = callback;
    params.m_Userdata = context;
    return dmWebServer::AddHandler(
        server, "/example/v1", &params, STATUS_OPENAPI);
}
```

`GET /example/v1/status` を実装し、記述した `text/plain` レスポンスを返すコールバックを渡します。リクエストのパスとメソッドの確認やレスポンスの生成は、引き続きコールバックが担います。登録結果を確認してください。メタデータが不正または競合している場合は、`dmWebServer::RESULT_ERROR_INVAL` を返します。

サーバーは文字列をコピーせず、JSON へのポインターを保持します。`dmWebServer::RemoveHandler()` でハンドラーを削除するか、サーバーを破棄するまで、その格納領域を変更せず、有効な状態に保ってください。例の `static const char` 配列は、この要件を満たします。ハンドラーを削除すると、以降の `/openapi.json` レスポンスから、そのパスも削除されます。

引数が3つの `dmWebServer::AddHandler(server, prefix, &params)` オーバーロードも引き続き利用できます。第4引数に `0` を渡すのと同じで、ハンドラーは OpenAPI メタデータなしで登録され、検出対象には含まれません。

## Automation Bridge 拡張 {#automation-bridge-extension}

Defold 公式の [Automation Bridge](https://github.com/defold/extension-automation-bridge) は、エンジンサービスを基盤とした、デバッグビルド専用のネイティブ拡張です。次の URL 以下に、バージョン付きのランタイム自動化 API を登録します:

```text
http://127.0.0.1:<engine-service-port>/automation-bridge/v1
```

ランタイム API は、シーンやノードの調査、入力、画面情報、スクリーンショット、録画、ライフサイクル情報、オプションのアプリケーション定義の同期などの機能を提供します。操作の例を次に示します:

| 操作 | 動作 |
| --- | --- |
| `GET  /automation-bridge/v1/health` | 動作状況のレポート、API の機能と互換性 |
| `POST /automation-bridge/v1/input/click` | 実行時の入力操作 |
| `GET  /automation-bridge/v1/screenshot` | 実行時のスクリーンショット |

プロジェクトにインストールされているバージョンに対応した、拡張機能の[ネイティブ API ドキュメント](https://github.com/defold/extension-automation-bridge/tree/master/automation_bridge)と [Python ヘルパーのドキュメント](https://github.com/defold/extension-automation-bridge/tree/master/automation_bridge/automation-bridge-python)を使用してください。

Automation Bridge は、リリースビルドでは HTTP API も Lua モジュールも公開しません。

### エディターとランタイムのクライアント {#editor-and-runtime-clients}

Automation Bridge の Python ヘルパーは、2つのクライアントからなる構成を示しています。関数 `editor.open_project()` はエディターのプロジェクトクライアントを返し、`project.build_and_run()` は別のエンジンクライアントを返します。

| クライアント | 用途 |
| --- | --- |
| プロジェクト | エディター HTTP API、コマンド、デバッガー、コンソール、環境設定、リファレンス、プレビュー、ビルド、ポートの検出 |
| ゲーム - エンジンサービス | シーン、入力、スクリーンショット、実行時の状態、同期 |

`project` と `game` を分けることで、プロセスの境界が明確になります。エディターの操作はエディターサーバーで行い、実行中のゲームの観察や操作はエンジンサービスで行います。

```python
from automation_bridge import editor

project = editor.open_project(".")
game = project.build_and_run()
```

## 制限事項とセキュリティ {#limitations-and-security}

エンジンサービスと拡張機能で定義するルートは開発ツールであり、そのように扱うことをお勧めします。

::: important
Defold 1.14.1 以降では、実行中のエンジンの `/openapi.json` ドキュメントで操作を検出します。それ以前のエンジンは、このエンドポイントを提供しません。OpenAPI メタデータなしで登録されたハンドラーについては、対象バージョンの拡張の API ドキュメントを参照してください。
:::

実行時のスクリプト、物理演算、入力、動的に作成されたオブジェクト、プラットフォームのレンダリングには、実行中のエンジンが必要です。これらは[ランタイムの自動テスト](/manuals/automated-testing)で検証することをお勧めします。

* ルーター、公開インターフェース、信頼できないトンネルを介してサービスを公開しないでください。
* エンジンサービスのルートが認証を必要とするものと想定しないでください。
* ランタイムルートは、拡張機能のバージョン、プラットフォーム、グラフィックスバックエンド、エンジンの機能によって異なることがあります。
* 拡張機能で定義する最新の API には、バージョンまたは機能のネゴシエーションを使用してください。
