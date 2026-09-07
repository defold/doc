#### Q: エディターのシステム要件は何ですか？ {#q-what-are-the-system-requirements-for-the-editor}
A: エディターはシステムで利用可能なメモリの最大75%を使用します。RAM が 4 GB のコンピューターでも、小規模な Defold プロジェクトには十分なはずです。中規模または大規模なプロジェクトでは、6 GB 以上の RAM を推奨します。


#### Q: Defold のベータ版は自動更新されますか？ {#q-are-defold-beta-versions-auto-updating}
A: はい。Defold のベータ版エディターは、安定版と同様に起動時に更新を確認します。


#### Q: エディターの起動時に `java.awt.AWTError: Assistive Technology not found` というエラーが表示されるのはなぜですか？ {#q-why-am-i-getting-an-error-saying-javaawtawterror-assistive-technology-not-found-when-launching-the-editor}
A: このエラーは、[NVDA スクリーンリーダー](https://www.nvaccess.org/download/)などの Java の支援技術の問題に関連しています。おそらくホームフォルダーに `.accessibility.properties` ファイルがあります。そのファイルを削除して、エディターを再度起動してみてください。（注: 支援技術を使用していて、このファイルが必要な場合は、代替の解決策を相談するために info@defold.se までご連絡ください）。

[Defold フォーラムのこちらのトピック](https://forum.defold.com/t/editor-endless-loading-windows-10-1-2-169-solved/65481/3)で議論されています。


#### Q: エディターの起動時に `sun.security.validator.ValidatorException: PKIX path building failed` というエラーが表示されるのはなぜですか？ {#q-why-am-i-getting-an-error-saying-sunsecurityvalidatorvalidatorexception-pkix-path-building-failed-when-launching-the-editor}
A: この例外は、エディターが https 接続を試みたときに、サーバーから提供された証明書チェーンを検証できない場合に発生します。

このエラーの詳細は、[こちらのリンク](https://github.com/defold/defold/blob/master/editor/README_TROUBLESHOOTING_PKIX.md)を参照してください。


#### Q: 特定の操作を行うと `java.lang.OutOfMemoryError: Java heap space` が発生するのはなぜですか？ {#q-why-am-i-am-getting-a-javalangoutofmemoryerror-java-heap-space-when-performing-certain-operations}
A: Defold エディターは Java で作られており、Java の既定のメモリ設定では不十分な場合があります。その場合は、エディターの設定ファイルを編集して、より多くのメモリを割り当てるよう手動で設定できます。`config` という名前の設定ファイルは、macOS では `Defold.app/Contents/Resources/` フォルダーにあります。Windows では実行ファイル `Defold.exe` と同じ場所、Linux では実行ファイル `Defold` と同じ場所にあります。`config` ファイルを開き、`vmargs` で始まる行に `-Xmx6gb` を追加します。`-Xmx6gb` を追加すると、ヒープサイズの上限が6ギガバイトに設定されます（既定値は通常 4Gb です）。次のようになります。

```
vmargs = -Xmx6gb,-Dfile.encoding=UTF-8,-Djna.nosys=true,-Ddefold.launcherpath=${bootstrap.launcherpath},-Ddefold.resourcespath=${bootstrap.resourcespath},-Ddefold.version=${build.version},-Ddefold.editor.sha1=${build.editor_sha1},-Ddefold.engine.sha1=${build.engine_sha1},-Ddefold.buildtime=${build.time},-Ddefold.channel=${build.channel},-Ddefold.archive.domain=${build.archive_domain},-Djava.net.preferIPv4Stack=true,-Dsun.net.client.defaultConnectTimeout=30000,-Dsun.net.client.defaultReadTimeout=30000,-Djogl.texture.notexrect=true,-Dglass.accessible.force=false,--illegal-access=warn,--add-opens=java.base/java.lang=ALL-UNNAMED,--add-opens=java.desktop/sun.awt=ALL-UNNAMED,--add-opens=java.desktop/sun.java2d.opengl=ALL-UNNAMED,--add-opens=java.xml/com.sun.org.apache.xerces.internal.jaxp=ALL-UNNAMED
```
