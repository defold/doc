#### Q: Android でナビゲーションバーとステータスバーを非表示にできますか？ {#q-is-it-possible-to-hide-the-navigation-and-status-bars-on-android}
A: はい。*game.project* ファイルの *Android* セクションで *immersive_mode* を設定します。これにより、アプリが画面全体を使用し、画面上のすべてのタッチイベントを取得できます。


#### Q: デバイスに Defold のゲームをインストールすると、「Failure [INSTALL_PARSE_FAILED_INCONSISTENT_CERTIFICATES]」と表示されるのはなぜですか？ {#q-why-am-im-getting-failure-install_parse_failed_inconsistent_certificates-when-installing-a-defold-game-on-device}
A: Android が、新しい証明書を使ってアプリをインストールしようとしていることを検出したためです。デバッグビルドのバンドル（bundle）を作成する際は、各ビルドが一時的な証明書で署名されます。新しいバージョンをインストールする前に、古いアプリをアンインストールします。

```
$ adb uninstall com.defold.examples
Success
$ adb install Defold\ examples.apk
4826 KB/s (18774344 bytes in 3.798s)
      pkg: /data/local/tmp/Defold examples.apk
Success
```


#### Q: 特定の拡張を使用してビルドすると、AndroidManifest.xml のプロパティの競合に関するエラーが発生するのはなぜですか？ {#q-why-am-i-getting-errors-about-conflicting-properties-in-androidmanifestxml-when-building-with-certain-extensions}
A: 同じプロパティタグに異なる値を指定した Android マニフェストのスタブを、2つ以上の拡張（extension）が提供すると、このエラーが発生することがあります。たとえば、Firebase と AdMob でこの問題が発生しています。ビルドエラーは次のように表示されます。

```
SEVERE: /tmp/job4531953598647135356/upload/AndroidManifest.xml:32:13-58
Error: Attribute property#android.adservices.AD_SERVICES_CONFIG@resource
value=(@xml/ga_ad_services_config) from AndroidManifest.xml:32:13-58 is also
present at AndroidManifest.xml:92:13-59 value=(@xml/gma_ad_services_config).
Suggestion: add 'tools:replace="android:resource"' to <property> element at
AndroidManifest.xml to override. 
```

この問題と回避策の詳細は、Defold に報告された問題 [#9453](https://github.com/defold/defold/issues/9453#issuecomment-2367367269) と Google に報告された問題 [#327696048](https://issuetracker.google.com/issues/327696048?pli=1) を参照してください。