#### Q: Chrome で HTML5 アプリがスプラッシュ画面でフリーズするのはなぜですか？ {#q-why-does-my-html5-app-freeze-at-the-splash-screen-in-chrome}

A: ローカルのファイルシステムからブラウザーでゲームを実行できない場合があります。エディターから実行すると、ローカルの Web サーバーからゲームが配信されます。たとえば、Python の `SimpleHTTPServer` を使用できます。

```sh
$ python -m SimpleHTTPServer [port]
```


#### Q: 読み込み中にゲームが "Unexpected data size" エラーでクラッシュするのはなぜですか？ {#q-why-does-my-game-crash-with-error-unexpected-data-size-while-loading}

A: これは通常、Windows を使用し、ビルドを作成して Git にコミットした場合に発生します。Git の改行コードの設定が正しくないと、Git が改行コードを変更するため、データサイズも変わります。この問題を解決するには、次の手順に従ってください: [Git で改行コードを扱うための設定](https://docs.github.com/en/free-pro-team@latest/github/using-git/configuring-git-to-handle-line-endings)
