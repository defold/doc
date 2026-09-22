---
title: HTTP を使った Defold エディターの自動化
brief: このマニュアルでは、外部ツールから、開いている Defold エディタープロジェクトのローカル HTTP API を検出して利用する方法を説明します。
---

# Defold エディターの自動化 {#automating-the-defold-editor}

Defold エディターは、自動操作のための専用サーバーを起動します。HTTP API は、開いているプロジェクトを操作します。エディターコマンド、ビルド、プロジェクトのリソース（resource）、プレビュー、環境設定、コンソール出力、ドキュメント検索、エディタースクリプト（editor script）との連携に利用できます。実行中のゲームを調べたり操作したりする場合は、[エンジンサービス（engine service）またはランタイム自動化 API](/manuals/engine-service) を使用してください。

::: important
エディター HTTP API は実験的な機能であり、Defold のバージョン間で変更される可能性があります。利用可能な操作とスキーマについては、実行中のエディターが生成する `/openapi.json` ドキュメントを基準としてください。
:::

## 外部ツールからのエディターの起動 {#starting-the-editor-from-an-external-tool}

外部ツールには、エディターの実行ファイルと、プロジェクトの `game.project` ファイルへの絶対パスが必要です。

インストール済みの Defold の各バージョンは、[エディターマニュアル](/manuals/editor/#editor-installation-metadata) で説明されている `installations.json` を使って見つけることができます。その `launcherPath` フィールドには、起動する実行ファイルが格納されています。`game.project` のパスを最初の位置引数として渡すと、そのプロジェクトを直接開くことができます。

省略可能な引数 `--port` または `-p` は、エディターサーバーのポートを指定します。省略すると Defold が利用可能なポートを選択します。複数のプロジェクトを開く可能性がある場合は、通常、省略することをお勧めします。

```sh
# Linux
/path/to/Defold/Defold --port 8181 /absolute/path/to/project/game.project
```

```sh
# macOS
/path/to/Defold.app/Contents/MacOS/Defold --port 8181 /absolute/path/to/project/game.project
```

```powershell
# Windows
C:\path\to\Defold\Defold.exe --port 8181 C:\absolute\path\to\project\game.project
```

エディターはグラフィカルなデスクトップアプリケーションです。ディスプレイにアクセスできる対話型ユーザーセッションで起動してください。画面表示を伴わずに実行するヘッドレス（headless）CI など、グラフィカルなセッションが利用できない場合や、スタンドアロンのバンドル（bundle）の作成には、[Bob](/manuals/bob) を使用してください。開いているエディターでも、`/command/compile` を通じてコンパイルのみの自動化を行えます。

エディターを起動したら、プロジェクトが開き、`.internal/editor.port` が作成されるまで待ちます。その後、有効なドキュメントが返されるまで `/openapi.json` をポーリングします。プロセスが作成されたからといって、プロジェクトの準備ができたと判断しないでください。

## エディターサーバーの検出 {#locating-the-editor-server}

エディターは、プロジェクトを開いている間、ローカル HTTP サーバーを起動します。<kbd>Help ▸ Open Editor Server</kbd> を選択すると、既定のブラウザーでホームページが開きます。

![ローカルエディターサーバーのホームページ](images/automation/editor_server.png)

選択されたポートは、プロジェクト内の次のファイルに書き込まれます。

```text
.internal/editor.port
```

このマニュアルの以降の例とコマンドでは、次のシェル変数を使用します。

```sh
PORT="$(cat .internal/editor.port)"
BASE_URL="http://127.0.0.1:$PORT"
```

ポートファイルは、現在のエディターセッションに対応しています。エディターを再起動したら、読み直してください。

::: important
エディターサーバーは、信頼できるローカルの操作インターフェースです。公開アドレス、ポート転送、信頼できないトンネルを通して公開しないでください。
:::

## OpenAPI による操作の検出 {#discovering-operations-through-openapi}

外部ツールが処理を開始するために必要な Defold 固有の情報は、エディターのポートと OpenAPI ドキュメントだけです。

```sh
curl -sS "http://127.0.0.1:$(cat .internal/editor.port)/openapi.json"
```

返される OpenAPI 3.0.3 ドキュメントには、実行中のエディターバージョンがサポートする操作が記述されています。パス、メソッド、パラメーター、コマンド名、リクエスト形式、レスポンス、ステータスコード、認証要件が含まれます。

ドキュメントに記載されているパスを一覧表示します。

```sh
curl -sS "$BASE_URL/openapi.json" |
  jq -r '.paths | keys[]'
```

ドキュメントに記載されているエディターコマンドのパスを一覧表示します。

```sh
curl -sS "$BASE_URL/openapi.json" |
  jq -r '.paths | keys[] | select(startswith("/command/"))'
```

Defold 1.13.2 以降では、OpenAPI ドキュメントに各コマンド専用のパスがあります。それより前のバージョンでは、`/command/{command}` パスとコマンド名の列挙値でコマンドを記述しています。

バージョンの違いに対応する連携では、必要な各操作を確認し、返されたスキーマに基づいてリクエストを設定することをお勧めします。エンドポイント名やコマンド名を網羅していると想定した一覧を別に管理することは、内容が古くなる可能性があるため推奨しません。

プロジェクトで定義したルートも、そのエディタースクリプトが OpenAPI の操作の記述を提供していれば、`/openapi.json` に表示されます。

## エディターコマンドの実行 {#executing-editor-commands}

エディターコマンドを呼び出すには、ドキュメントに記載されているコマンドのパスに `POST` リクエストを送信します。例:

```text
POST /command/compile
POST /command/run
```

プロジェクトを実行せずにコンパイルするには、次のようにします。

```sh
curl -sS \
  -X POST \
  "$BASE_URL/command/compile" |
  jq
```

プロジェクトをコンパイルして実行するには、次のようにします。

```sh
curl -sS \
  -X POST \
  "$BASE_URL/command/run" |
  jq
```

これらのパイプラインはレスポンス本文を表示します。自動化スクリプトでは、[HTML5 のビルド](#building-html5)のパターンを使い、HTTP ステータスと `success` も確認してください。

::: sidenote
Defold 1.13.2 以降では、`/command/build` は `/command/run` の非推奨の互換エイリアスで、OpenAPI には記載されません。新しい連携では `/command/run` を使ってください。
:::

コンパイルが成功すると、HTTP ステータス `200` とともに構造化された結果が返されます。

```json
{
  "success": true,
  "issues": []
}
```

ビルドが失敗すると、HTTP ステータス `422` とともに、次のような問題の情報が返されます。

```json
{
  "success": false,
  "issues": [
    {
      "message": "Example compiler message",
      "severity": "error",
      "resource": "/main/player.script",
      "range": {
        "start": {
          "line": 12,
          "character": 4
        },
        "end": {
          "line": 12,
          "character": 17
        }
      }
    }
  ]
}
```

利用可能なフィールドはエラーによって異なります。リソースパスとソース内の範囲がある場合はそれらを利用しつつ、メッセージのみを含む問題にも対応してください。

実行中のエディターの一覧に含まれていれば、次のようなコマンドがよく役立ちます。

`compile`
: プロジェクトを実行せずにコンパイルします。

`run`
: プロジェクトをコンパイルして実行します。

`clean-build`
: ビルドキャッシュを消去してから、コンパイルして実行します。通常のビルドの動作に一貫性がない場合や、変更が反映されていないように見える場合にのみ使用してください。

`build-html5`
: プロジェクトを HTML5 向けにビルドし、エディターサーバーを通じて出力を利用できるようにします。

`fetch-libraries`
: プロジェクトの依存関係をダウンロードして再読み込みします。

`hot-reload`
: 変更されたリソースを実行中のゲームに再読み込みします。

`reload-extensions`
: エディタースクリプトを再読み込みします。

`debugger-start`、`debugger-stop`、およびデバッガーのステップ実行コマンド
: デバッグセッションと実行中のプロジェクトを操作します。

正確な名前と利用可否は、エディターのバージョンと現在の状態によって異なります。`/openapi.json` から確認してください。

プロジェクトのリソースを操作するコマンドは、実行前に外部でのファイル変更を同期します。

### コマンドのレスポンスと非同期処理 {#command-responses-and-asynchronous-work}

レスポンスはコマンドによって異なります。Defold 1.13.2 以降では、`compile`、`run`、`clean-build`、`build-html5`、`debugger-start`、`hot-reload` はコマンドの完了を待ち、上記のように `success` と `issues` を含む構造化された結果を返します。成功した結果では HTTP `200`、ビルドまたは検証の失敗では `422` が返されます。

`debugger-break` など、他のコマンドは引き続き `202` を返す場合があります。現在の OpenAPI スキーマで操作を調べ、実際の HTTP レスポンスステータスを処理してください。

| ステータス | 意味 |
| --- | --- |
| `200` | コマンドが完了し、結果が返されました |
| `202` | コマンドが受け付けられ、非同期で継続しています |
| `403` | コマンドは現在のエディターの状態では有効ではありません |
| `404` | コマンドは利用できません |
| `422` | ビルドまたは検証に失敗しました |
| `500` | エディターの内部エラーが発生しました |

HTTP `202` レスポンスは、要求した結果が存在する証拠にはなりません。関連する出力、リソース、コンソールのマーカー、または配信 URL を待ち、タイムアウトを設けてください。

### HTML5 のビルド {#building-html5}

現在の OpenAPI ドキュメントに `/command/build-html5` が記載されている場合は、そのパスを通じて呼び出します。シェルスクリプトでは、HTTP ステータスをレスポンス本文とは別に取得し、リクエストまたはビルドに失敗したら停止します。

```sh
build_response_file="$(mktemp)" || exit 1
if ! build_http_status="$(curl -sS \
  -X POST \
  -o "$build_response_file" \
  -w '%{http_code}' \
  "$BASE_URL/command/build-html5")"; then
  cat "$build_response_file"
  rm -f "$build_response_file"
  exit 1
fi

cat "$build_response_file"
if [ "$build_http_status" != "200" ] ||
   ! jq -e '.success == true' "$build_response_file" > /dev/null; then
  rm -f "$build_response_file"
  exit 1
fi
rm -f "$build_response_file"
```

Defold 1.13.2 以降では、このリクエストはビルドの完了を待ち、構造化された結果を返します。この例は、ビルドの問題を含むレスポンス本文を出力し、HTTP `200` かつ `success: true` の場合にのみ処理を続けます。ビルドが成功すると、エディターはブラウザーでゲームを開き、次の URL で配信します。

```text
http://127.0.0.1:<editor-port>/html5/
```

ビルドが完了しても、ブラウザーでゲームの読み込みが完了したとは限りません。入力を送信したりゲームプレイを確認したりする前に、キャンバスとアプリケーションの準備が整うまで待ってください。詳細は、[HTML5 のブラウザーテスト](/manuals/automated-testing/#browser-tests-for-html5) を参照してください。

## API ドキュメントの検索 {#searching-api-documentation}

`/openapi.json` に `/ref` 操作がある場合、この操作で、実行中のエディターバージョンに含まれる API ドキュメントを検索できます。そのバージョンに対応する名前とシグネチャを取得できます。

たとえば、関数を検索するには次のようにします。

```sh
curl -sS \
  --get \
  --data-urlencode "q=go.animate" \
  "$BASE_URL/ref" |
  jq
```

環境と言語で絞り込みます。

```sh
curl -sS \
  --get \
  --data-urlencode "environment=runtime" \
  --data-urlencode "language=Lua" \
  --data-urlencode "q=collision message|raycast" \
  "$BASE_URL/ref" |
  jq
```

検索パラメーターは次のとおりです。

`environment`
: `editor`、`runtime`、またはカンマ区切りの値です。

`language`
: `Lua`、`C`、`C++`、またはカンマ区切りの値です。

`q`
: 大文字と小文字を区別しない式です。空白は AND、`|` は OR を表します。

ドキュメントをまとめたリソースもあります。[LLM ドキュメントの索引](https://defold.com/llms.txt) には、公式マニュアル、API 名前空間、サンプルへのリンクがあり、[LLM 向けドキュメント全文](https://defold.com/llms-full.txt) には、オフライン検索とローカルでの索引作成に利用できる完全なドキュメントが掲載されています。

AI エージェントには、API やメッセージが1つだけ必要な場合、リファレンス全体を取得するよりも、対象を絞った検索を優先することをお勧めします。これにより、トークンを節約し、対象タスクに適した整理されたコンテキストを用意できます。

## コンソール出力の読み取り {#reading-console-output}

エディターのコンソールを JSON として読み取ります。

```sh
curl -sS "$BASE_URL/console" | jq
```

レスポンスの `lines` にはコンソールのテキストが、`regions` には意味に基づいて区分された領域が含まれます。この領域には、エラー、評価結果、リソース参照などが含まれます。

コンソール出力を継続的に取得するには、次のようにします。

```sh
curl -N "$BASE_URL/console/stream"
```

ストリームには既存のコンソール行が含まれ、その後も新しい出力を受け取るために接続を維持します。完了マーカーまたはエラーを受け取ったとき、プロセスの終了を検出したとき、あるいはタイムアウトまたは行数の上限に達したときに閉じてください。

テスト結果の区切り方と失敗の分類については、[自動テストと検証](/manuals/automated-testing/#structured-test-results) を参照してください。

## シーンプレビューのレンダリング {#rendering-scene-previews}

Defold エディター（1.13.1 以降）では、コマンド `/preview/{path}` を通じて、対応するシーンリソースの「スクリーンショット」を PNG にレンダリングできます。

```sh
mkdir -p build/automation

curl -sS \
  "$BASE_URL/preview/main/main.collection?width=1280&height=720" \
  --output build/automation/main-preview.png
```

これは、開いている Basic 3D テンプレートプロジェクトのメインコレクション（main collection）を、既定の初期ビューでレンダリングします。

![エディターでレンダリングしたメインコレクションのプレビュー](images/automation/main-preview.png)

ビジュアルシーンエディターを使うリソースのプレビューを、レンダリングで取得できます。たとえば、モデルコンポーネント（model component）も同じ方法でレンダリングでき、見た目やシェーダーの正しさなどを検証できます。

```sh
curl -sS \
  "$BASE_URL/preview/assets/models/cube.model?width=1280&height=720" \
  --output build/automation/cube-preview.png
```

![エディターでレンダリングした立方体モデルのプレビュー](images/automation/cube-preview.png)

`/preview/` に続くパスには、先頭のスラッシュを含めません。省略可能な寸法の既定値はプロジェクトの表示サイズで、`1` から `4096` の範囲である必要があります。

| ステータス | 意味 |
| --- | --- |
| `200` | プレビューがレンダリングされました |
| `400` | 寸法が無効です |
| `404` | リソースが見つかりませんでした |
| `422` | リソースが読み込まれていないか、シーンプレビューに対応していません |

プレビューは、レベルのレイアウト、GUI のレイアウト、シェーダーとライティングの設定、見た目の回帰の確認など、プロジェクトの視覚的な分析や、ドキュメントのサムネイル作成に非常に役立つ可能性があります。

::: important
エディターのプレビューは、実行中のゲームのスクリーンショットではありません。動的に生成されたオブジェクト、実行時のポストプロセス、プラットフォーム固有のレンダリングは検証できません。これらの要素が必要な場合は、[実行時のスクリーンショット](/manuals/automated-testing/#editor-previews-and-runtime-screenshots) を使用してください。
:::

## エディター Lua の実行 {#executing-editor-lua}

認証が必要な `POST /eval` 操作は、エディター拡張環境で Lua を実行します。セッションごとの Bearer トークンは、次のファイルに保存されます。

```text
.internal/editor.token
```

トークンを読み取り、コードを実行します。

```sh
TOKEN="$(cat .internal/editor.token)"

curl -sS \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: text/plain" \
  --data-binary 'print(editor.version) return editor.platform' \
  "$BASE_URL/eval"
```

出力された内容と戻り値は、テキストとして返されます。一般的なレスポンスは次のとおりです。

| ステータス | 意味 |
| --- | --- |
| `200` | コードが実行されました |
| `401` | Bearer トークンがないか、無効です |
| `422` | Lua コードを解析または実行できませんでした |
| `503` | エディター拡張環境の準備ができていません |

クライアントは `503` の後に再試行してもかまいませんが、試行回数には上限を設けることをお勧めします。`422` が返されたリクエストを再度送信する前に、コードを修正してください。

評価するコードでは、[エディター API](https://defold.com/ref/editor-lua/) とエディタースクリプト環境を利用できます。`go.*` などのゲームのランタイム API を使って、実行中のゲームを操作することはできません。ゲームプレイには、ランタイムテスト、デバッガー、ブラウザーテスト、または [ランタイム自動化 API](/manuals/engine-service/#automation-bridge-extension) を使用してください。

### リソースとファイルの変更 {#modifying-resources-and-files}

Defold のソースリソースの多くはテキスト形式を使用しており、任意のテキスト編集ツールで編集できます。Defold プロジェクトの構造化されたリソースを変更する場合は、エディターのトランザクション（editor transaction）を優先してください。

| 変更内容 | 推奨する方法 |
| --- | --- |
| Lua、シェーダー、JSON、またはその他の既知のテキスト形式 | ファイルの直接変更 |
| エディターで開いているタブ内の未保存のテキスト | `editor.get()` と `editor.transact()` |
| コレクション、ゲームオブジェクト（game object）、GUI、アトラス（atlas）、またはその他の構造化されたリソース | エディターのトランザクション |
| 繰り返し生成するコンテンツ | スタンドアロンのジェネレーター |
| 繰り返し実行できるプロジェクト操作 | エディターコマンドまたはカスタム HTTP エンドポイント |
| CI のみで実行する変換 | Bob の前に実行するスタンドアロンのスクリプト |

リソースを変更する前に、その内容を調べます。

```sh
curl -sS \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: text/plain" \
  --data-binary '
    local path = "/game.project"
    pprint(editor.properties(path))
    return editor.get(path, "path")
  ' \
  "$BASE_URL/eval"
```

トランザクションを実行する前に、`editor.can_get()`、`editor.can_set()`、その他の `editor.can_*()` 関数で確認してください。

エディター Lua で `editor.execute()` を使うと、フォーマッター、バリデーター、ジェネレーターを実行できます。

```lua
local output = editor.execute(
  "python3",
  "scripts/generate_levels.py",
  {
    out = "capture"
  }
)

print(output)
```

コマンドがプロジェクトのリソースを変更しない場合は、`reload_resources = false` を設定して不要な再読み込みを避けてください。

::: important
`.internal/` 内のファイルや、`build/` 内の生成されたコンテンツを変更しないでください。
:::

## 環境設定 {#preferences}

エディターの環境設定は、OpenAPI に記載されているパス（現在は `/prefs/{path}`）を通じて読み書きできます。

たとえば、設定されているコードのフォントサイズを読み取ることができます。

```sh
curl -sS "$BASE_URL/prefs/code/font/size" | jq
```

また、たとえば 16 に設定することもできます。

```sh
curl -sS \
  -X POST \
  -H "Content-Type: application/json" \
  --data '16' \
  "$BASE_URL/prefs/code/font/size"
```

エディターは、環境設定のスキーマに照らして値を検証します。パスまたは値が無効な場合は、HTTP `400` が返されます。

環境設定は、ユーザー単位、またはプロジェクトごとのユーザー単位で永続的に保存される設定であり、`game.project` に保存されるプロジェクト設定ではありません。自動化で環境設定を一時的に変更する必要がある場合は、以前の値を保存し、処理後に復元してください。

## プロジェクトで定義するルート {#project-defined-routes}

エディタースクリプトでは、[`get_http_server_routes()`](/manuals/editor-scripts/#http-server) を使ってルートを追加できます。省略可能な OpenAPI 操作テーブルを指定すると、組み込み操作と同じ `/openapi.json` ドキュメントにルートが公開されます。

プロジェクトで定義したルートでは、コンテンツ生成、検証、レポート、ローカライズのチェック、リソース分析、プロジェクト固有のテスト、IDE や外部コントローラー向けのより小さなインターフェースなどを提供できます。

適切なルートにするには、明確な名前の付いた1つの操作を実行し、入力を検証し、構造化された結果を返し、可能な限り冪等にし、負荷の高い処理を制限することをお勧めします。

プロジェクトで定義したルートは、`/eval` のトークンでは自動的に保護されません。機密性の高い操作を実行するルートには、プロジェクト固有の認証と安全性のチェックを追加してください。

## ライフサイクルフック {#lifecycle-hooks}

フック（hook）は、ビルドの前後、バンドル作成の前後、ゲームプロセスの開始時または終了時に実行できる関数です。プロジェクトのルートには、`hooks.editor_script` ファイルを1つ配置できます。ルートのフックファイルだけがこれらのイベントを受け取るため、プロジェクト内の1か所で実行順序を定義できます。

```lua
local M = {}

local function validate_project()
  print(editor.execute(
    "python3",
    "scripts/validate_project.py",
    {
      out = "capture",
      reload_resources = false
    }
  ))
end

function M.on_build_started(opts)
  validate_project()
end

function M.on_build_finished(opts)
  print("Build successful:", opts.success)
end

return M
```

`on_build_started()` でエラーが発生すると、エディターのビルドは停止します。ライフサイクルフックはエディター内でのみ実行されます。共通の検証と生成のロジックは、CI からも呼び出せるスタンドアロンのスクリプトに配置してください。

## セキュリティと互換性 {#security-and-compatibility}

エディターサーバー全体を、信頼できるローカルのインターフェースとして扱ってください。

* ポートへのアクセスを外部に公開しないでください。
* `.internal/editor.token` を保護してください。このファイルは、現在のセッションで `/eval` の使用を認可します。
* 外部に無制限の `/eval` アクセスを与えないでください。
* トークンは、プロンプト、レポート、ログではなく、ローカルの連携レイヤーに保持してください。
* プロジェクトで定義したルートは、`/eval` の認証を継承しないことに注意してください。
* 最新の `/openapi.json` を使用してください。
* 非同期の自動コマンドとエディターの起動を待つ際は、待機時間に上限を設けてください。

## エンジンサーバー {#engine-server}

エディターサーバーは、エディタープロセスに属します。実行中のゲームは別のポートを使用し、役割も異なります。詳細は、[エンジンサービスとランタイム HTTP API のマニュアル](/manuals/engine-service) を参照してください。
