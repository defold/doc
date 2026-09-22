#### Q: 無料の Apple Developer アカウントを使って Defold のゲームをインストールできません。 {#q-i-am-unable-to-install-my-defold-game-using-a-free-apple-developer-account}
A: Defold プロジェクトで使用しているバンドル識別子（bundle identifier）が、モバイルプロビジョニングプロファイルを生成したときに Xcode プロジェクトで使用したものと同じであることを確認してください。

#### Q: バンドルを作成したアプリケーションのエンタイトルメントを確認するにはどうすればよいですか？ {#q-how-can-i-check-the-entitlements-of-a-bundled-application}
A: [ビルドしたアプリのエンタイトルメントの確認](https://developer.apple.com/library/archive/technotes/tn2415/_index.html#//apple_ref/doc/uid/DTS40016427-CH1-APPENTITLEMENTS)より:

```sh
codesign -d --ent :- /path/to/the.app
```

#### Q: プロビジョニングプロファイルのエンタイトルメントを確認するにはどうすればよいですか？ {#q-how-can-i-check-the-entitlements-of-a-provisioning-profile}
A: [プロファイルのエンタイトルメントの確認](https://developer.apple.com/library/archive/technotes/tn2415/_index.html#//apple_ref/doc/uid/DTS40016427-CH1-PROFILESENTITLEMENTS)より:

```sh
security cms -D -i /path/to/iOSTeamProfile.mobileprovision
```