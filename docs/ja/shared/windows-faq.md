#### Q: テクスチャのない GUI のボックスノード（box node）が、エディターでは透明なのに、ビルドして実行すると想定どおり表示されるのはなぜですか？ {#q-why-are-gui-box-nodes-without-a-texture-transparent-in-the-editor-but-show-up-as-expected-when-i-build-and-run}

A: この問題は、[AMD Radeon GPU を使用するコンピューター](https://github.com/defold/editor2-issues/issues/2723)で発生することがあります。グラフィックスドライバーを更新してください。

#### Q: アトラス（atlas）やシーンビューを開くと `com.sun.jna.Native.open.class java.lang.Error: Access is denied` が表示されるのはなぜですか？ {#q-why-am-i-getting-comsunjnanativeopenclass-javalangerror-access-is-denied-when-opening-an-atlas-or-a-scene-view}

A: Defold を管理者として実行してみてください。Defold の実行ファイルを右クリックして、"Run as Administrator" を選択します。

#### Q: Intel UHD 内蔵 GPU を使用する Windows で、ゲームが正しく描画されないのはなぜですか（HTML5 ビルドは動作します）？ {#q-why-is-my-game-not-rendering-properly-on-windows-using-an-intel-uhd-integrated-gpu-but-my-html5-build-works}

A: ドライバーをバージョン 27.20.100.8280 以降に更新してください。[Intel Driver Support Assistant](https://www.intel.com/content/www/us/en/search.html?ws=text#t=Downloads&layout=table&cf:Downloads=%5B%7B%22actualLabel%22%3A%22Graphics%22%2C%22displayLabel%22%3A%22Graphics%22%7D%2C%7B%22actualLabel%22%3A%22Intel%C2%AE%20UHD%20Graphics%20Family%22%2C%22displayLabel%22%3A%22Intel%C2%AE%20UHD%20Graphics%20Family%22%7D%2C%7B%22actualLabel%22%3A%22Intel%C2%AE%20UHD%20Graphics%20630%22%2C%22displayLabel%22%3A%22Intel%C2%AE%20UHD%20Graphics%20630%22%7D%5D)で確認します。詳しくは、[こちらのフォーラム投稿](https://forum.defold.com/t/sprite-game-object-is-not-rendering/69198/35?u=britzl)を参照してください。

#### Q: Defold エディターがクラッシュし、ログに `AWTError: Assistive Technology not found` と表示されます {#q-the-defold-editor-is-crashing-and-the-log-shows-awterror-assistive-technology-not-found}

エディターがクラッシュし、ログに `Caused by: java.awt.AWTError: Assistive Technology not found: com.sun.java.accessibility.AccessBridge` と記録されている場合は、次の手順に従います。

* `C:\Users\<username>` に移動します
* 標準的なテキストエディター（Notepad でかまいません）で `.accessibility.properties` というファイルを開きます
* 設定ファイル内で次の行を探します。

```
assistive_technologies=com.sun.java.accessibility.AccessBridge
screen_magnifier_present=true
```

* これらの行の先頭にハッシュ記号（`#``）を追加します
* ファイルへの変更を保存し、Defold を再起動します
