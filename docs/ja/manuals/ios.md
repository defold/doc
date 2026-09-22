---
title: Defold での iOS プラットフォーム向け開発
brief: このマニュアルでは、Defold で iOS デバイス向けのゲームやアプリをビルドして実行する方法を説明します。
---

# iOS 向け開発 {#ios-development}

::: sidenote
iOS 向けゲームのバンドル（bundle）を作成できるのは、Mac 版の Defold エディターのみです。
:::

iOS では、ビルドしてスマートフォンやタブレットで実行する _すべての_ アプリに、Apple が発行した証明書とプロビジョニングプロファイルを使って署名する _必要があります_ 。このマニュアルでは、iOS 向けにゲームのバンドルを作成する手順を説明します。開発中は、コンテンツやコードをデバイスへ直接ホットリロード（hot reload）できるため、[開発用アプリ（development app）](/manuals/dev-app) を通じてゲームを実行する方法がよく使われます。

## Apple のコード署名の仕組み {#apples-code-signing-process}

iOS アプリのセキュリティは、いくつかの要素で構成されています。[Apple の iOS Developer Program](https://developer.apple.com/programs/) に登録すると、必要なツールを利用できます。登録後、[Apple の Developer Member Center](https://developer.apple.com/membercenter/index.action) にアクセスします。

![Apple の Member Center](images/ios/apple_member_center.png)

*Certificates, Identifiers & Profiles* セクションには、必要なツールがすべて揃っています。ここでは、次の項目を作成、削除、編集できます。

Certificates
: 開発者としての身元を証明する、Apple が発行した暗号証明書です。開発用または本番用の証明書を作成できます。開発用証明書を使うと、サンドボックスのテスト環境でアプリ内購入の仕組みなど、特定の機能をテストできます。本番用証明書は、App Store にアップロードする最終版のアプリへの署名に使います。テストのためにアプリをデバイスへインストールするには、その前に証明書でアプリへ署名する必要があります。

Identifiers
: さまざまな用途に使う識別子です。複数のアプリで使用できるワイルドカード識別子（たとえば `some.prefix.*`）を登録できます。App ID には、アプリが Passbook 連携や Game Center などを有効にするかどうかといった Application Service 情報を含めることができます。そのような App ID にワイルドカード識別子は使えません。Application Services を機能させるには、アプリケーションの *バンドル識別子（bundle identifier）* が App ID の識別子と一致する必要があります。

Devices
: 開発用の各デバイスを、その UDID（Unique Device IDentifier、後述）で登録する必要があります。

Provisioning Profiles
: プロビジョニングプロファイルは、証明書を App ID およびデバイスのリストに関連付けます。どの開発者のどのアプリを、どのデバイスにインストールできるかを定めます。

Defold でゲームやアプリに署名するには、有効な証明書と有効なプロビジョニングプロファイルが必要です。

::: sidenote
Member Center のホームページでできる操作の一部は、Xcode 開発環境がインストールされていれば、そこからも実行できます。
:::

デバイス識別子（UDID）
: iOS デバイスの UDID は、Wi-Fi またはケーブルでデバイスをコンピューターに接続して確認できます。Xcode を開き、<kbd>Window ▸ Devices and Simulators</kbd> を選択します。デバイスを選択すると、シリアル番号と識別子が表示されます。

  ![Xcode のデバイス一覧](images/ios/xcode_devices.png)

  Xcode がインストールされていない場合は、iTunes で識別子を確認できます。デバイスのアイコンをクリックして、使用するデバイスを選択します。

  ![iTunes のデバイス一覧](images/ios/itunes_devices.png)

  1. *Summary* ページで *Serial Number* を探します。
  2. *Serial Number* を1回クリックすると、フィールドが *UDID* に変わります。繰り返しクリックすると、デバイスに関するいくつかの情報が順に表示されます。*UDID* が表示されるまでクリックします。
  3. 長い UDID 文字列を右クリックし、<kbd>Copy</kbd> を選択して識別子をクリップボードにコピーします。これで、Apple の Developer Member Center でデバイスを登録するときに、UDID フィールドへ簡単に貼り付けられます。

## 無料の Apple 開発者アカウントを使った開発 {#developing-using-a-free-apple-developer-account}

Xcode 7 以降では、誰でも Xcode をインストールして、無料で実機を使った開発ができます。iOS Developer Program に登録する必要はありません。代わりに、Xcode が開発者用の証明書（有効期間は1年）と、特定のデバイス上のアプリ用のプロビジョニングプロファイル（有効期間は1週間）を自動的に発行します。

1. デバイスを接続します。
2. Xcode をインストールします。
3. Xcode に新しいアカウントを追加し、Apple ID でサインインします。
4. 新しいプロジェクトを作成します。最もシンプルな `Single View App` で十分です。
5. 自動的に作成された `Team` を選択し、アプリにバンドル識別子を設定します。

::: important
Defold プロジェクトで同じバンドル識別子を使用する必要があるため、バンドル識別子を控えておいてください。
:::

6. Xcode がアプリの *Provisioning Profile* と *Signing Certificate* を作成したことを確認します。

   ![](images/ios/xcode_certificates.png)

7. デバイス上でアプリをビルドします。初回は Xcode から Developer mode を有効にするよう求められ、デバイスがデバッガーをサポートするための準備が行われます。これには時間がかかることがあります。
8. アプリが動作することを確認したら、ディスク上でアプリを探します。ビルド先は、`Report Navigator` のビルドレポートで確認できます。

   ![](images/ios/app_location.png)

9. アプリを見つけて右クリックし、<kbd>Show Package Contents</kbd> を選択します。

   ![](images/ios/app_contents.png)

10. `embedded.mobileprovision` ファイルを、ドライブ上の見つけやすい場所にコピーします。

   ![](images/ios/free_provisioning.png)

このプロビジョニングファイルをコード署名 ID とともに使うと、Defold で1週間アプリに署名できます。

プロビジョニングの有効期限が切れたら、Xcode でアプリを再度ビルドし、上記の手順で新しい一時的なプロビジョニングファイルを取得する必要があります。

## iOS アプリケーションバンドルの作成 {#creating-an-ios-application-bundle}

コード署名 ID とプロビジョニングプロファイルが揃ったら、エディターからゲームのスタンドアロンのアプリケーションバンドルを作成できます。メニューから <kbd>Project ▸ Bundle... ▸ iOS Application...</kbd> を選択します。

![iOS バンドルへの署名](images/ios/sign_bundle.png)

コード署名 ID を選択し、モバイルプロビジョニングファイルの場所を指定して、ビルドバリアント（build variant、Debug または Release）を選択します。必要に応じて `Sign application` チェックボックスをオフにすると、署名処理をスキップし、後で手動で署名できます。`Simulator` をオンにすると、デバイス用バンドルの代わりに iOS シミュレーター用の `arm64_sim-ios` バンドルを作成します。

::: important
シミュレーター用バンドルは、Apple Silicon Mac 上の iOS シミュレーターでのみ実行できます。署名 ID やプロビジョニングプロファイルを使わないため、`Simulator` がオンの場合は署名、インストール、起動のオプションが無効になります。以下で説明するように、`xcrun simctl` でバンドルをインストールしてください。
:::

*Create Bundle* を押すと、コンピューター上のバンドルの作成先を指定するよう求められます。

![ipa 形式の iOS アプリケーションバンドル](images/ios/ipa_file.png){.left}

アプリに使用するアイコンや起動画面のストーリーボードなどは、プロジェクト設定ファイル *game.project* の [iOS セクション](/manuals/project-settings/#ios) で指定します。

### カスタム Info.plist とローカルターゲットの検出 {#custom-infoplist-and-local-target-discovery}

組み込みの iOS `Info.plist` には、リリース以外のビルドでエディターがターゲットを自動検出するために必要な Bonjour サービスとローカルネットワークの使用目的の説明が含まれています。カスタム `Info.plist` は、この組み込みのベースマニフェストを置き換えます。デバッグビルドでカスタムマニフェストを使い、ローカルネットワーク経由のターゲット検出、プロファイリング、ホットリロード、ログのストリーミングが必要な場合は、次のエントリーを含めてください。

```xml
{{^variant_release}}
<key>NSBonjourServices</key>
<array>
    <string>_defold._tcp</string>
</array>
<key>NSLocalNetworkUsageDescription</key>
<string>Discover Defold targets on the local network.</string>
{{/variant_release}}
```

Mustache の条件により、リリースバンドルには検出用のエントリーが含まれなくなります。使用目的を説明する文字列は iOS がユーザーに表示するもので、変更やローカライズが可能です。リリース版アプリケーション自体が同じ Bonjour サービスとローカルネットワーク機能を使う場合にのみ、この条件を削除してください。

:[Build Variants](../shared/build-variants.md)

## 接続した iPhone へのバンドルのインストールと起動 {#installing-and-launching-bundle-on-a-connected-iphone}

エディターの Bundle ダイアログにある `Install on connected device` と `Launch installed app` のチェックボックスを使うと、ビルドしたバンドルをインストールして起動できます。

![iOS バンドルのインストールと起動](images/ios/install_and_launch.png)

この機能を使うには、[ios-deploy](https://github.com/ios-control/ios-deploy) コマンドラインツールをインストールする必要があります。最も簡単なインストール方法は Homebrew を使うことです。
```
$ brew install ios-deploy
```

エディターが ios-deploy ツールのインストール先を検出できない場合は、[環境設定](/manuals/editor-preferences/#tools) で指定する必要があります。

### ストーリーボードの作成 {#creating-a-storyboard}

ストーリーボードファイルは Xcode で作成します。Xcode を起動して新しいプロジェクトを作成します。iOS と Single View App を選択します。

![プロジェクトの作成](images/ios/xcode_create_project.png)

Next をクリックし、プロジェクトの設定に進みます。Product Name を入力します。

![プロジェクト設定](images/ios/xcode_storyboard_create_project_settings.png)

Create をクリックして手順を完了します。これでプロジェクトが作成されたので、ストーリーボードの作成に進みます。

![プロジェクトのビュー](images/ios/xcode_storyboard_project_view.png)

画像をドラッグ＆ドロップしてプロジェクトにインポートします。次に `Assets.xcassets` を選択し、画像を `Assets.xcassets` にドロップします。

![画像の追加](images/ios/xcode_storyboard_add_image.png)

`LaunchScreen.storyboard` を開き、プラスボタン（<kbd>+</kbd>）をクリックします。ダイアログに `imageview` と入力して、ImageView コンポーネントを探します。

![Image View の追加](images/ios/xcode_storyboard_add_imageview.png)

Image View コンポーネントをストーリーボードにドラッグします。

![ストーリーボードへの追加](images/ios/xcode_storyboard_add_imageview_to_storyboard.png)

Image ドロップダウンから、先ほど `Assets.xcassets` に追加した画像を選択します。

![](images/ios/xcode_storyboard_select_image.png)

画像の位置を調整し、必要に応じて Label やその他の UI 要素を追加するなどの調整を行います。完了したら、アクティブなスキームを **Any iOS Device (arm64)**（または **Generic iOS Device**）に設定し、**Product ▸ Build** を選択します。Defold は64ビットデバイス上の iOS 15.0 以降をサポートしているため、デプロイメントターゲットは15.0以降にしてください。ビルド処理が完了するまで待ちます。

ストーリーボードで画像を使っても、それらは `LaunchScreen.storyboardc` に自動では含まれません。*game.project* の `Bundle Resources` フィールドを使ってリソースを同梱してください。
たとえば、Defold プロジェクト内に `LaunchScreen` フォルダーを作成し、その中に `ios` フォルダーを作成します（これらのファイルを iOS バンドルにのみ含めるために `ios` フォルダーが必要です）。次に、ファイルを `LaunchScreen/ios/` に配置します。このパスを `Bundle Resources` に追加します。

![](images/ios/bundle_res.png)

最後に、コンパイルされた `LaunchScreen.storyboardc` ファイルを Defold プロジェクトにコピーします。Finder で次の場所を開き、`LaunchScreen.storyboardc` ファイルを Defold プロジェクトにコピーします。

    /Library/Developer/Xcode/DerivedData/YOUR-PRODUCT-NAME-cbqnwzfisotwygbybxohrhambkjy/Build/Intermediates.noindex/YOUR-PRODUCT-NAME.build/Debug-iphonesimulator/YOUR-PRODUCT-NAME.build/Base.lproj/LaunchScreen.storyboardc

::: sidenote
フォーラムユーザーの Sergey Lerg が、[この手順を紹介する動画チュートリアル](https://www.youtube.com/watch?v=6jU8wGp3OwA&feature=emb_logo) を作成しています。
:::

ストーリーボードファイルが用意できたら、*game.project* から参照できます。


### アイコンのアセットカタログの作成 {#creating-an-icon-asset-catalog}

アセットカタログを使うことは、アプリケーションのアイコンを管理する方法として Apple が推奨しています。実際、App Store の掲載情報で使われるアイコンを指定する唯一の方法です。アセットカタログはストーリーボードと同じように、Xcode で作成します。Xcode を起動して新しいプロジェクトを作成します。iOS と Single View App を選択します。

![プロジェクトの作成](images/ios/xcode_create_project.png)

Next をクリックし、プロジェクトの設定に進みます。Product Name を入力します。

![プロジェクト設定](images/ios/xcode_icons_create_project_settings.png)

Create をクリックして手順を完了します。これでプロジェクトが作成されたので、アセットカタログの作成に進みます。

![プロジェクトのビュー](images/ios/xcode_icons_project_view.png)

サポートされている各アイコンサイズを表す空の枠に、画像をドラッグ＆ドロップします。

![アイコンの追加](images/ios/xcode_icons_add_icons.png)

::: sidenote
Notifications、Settings、Spotlight 用のアイコンは追加しないでください。
:::

完了したら、アクティブなスキームを `Build -> Any iOS Device (arm64)`（または `Generic iOS Device`）に設定し、<kbd>Product</kbd> -> <kbd>Build</kbd> を選択します。ビルド処理が完了するまで待ちます。

::: sidenote
必ず `Any iOS Device (arm64)` または `Generic iOS Device` 向けにビルドしてください。そうしないと、ビルドをアップロードするときに `ERROR ITMS-90704` エラーが発生します。
:::

![プロジェクトのビルド](images/ios/xcode_icons_build.png)

最後に、コンパイルされた `Assets.car` ファイルを Defold プロジェクトにコピーします。Finder で次の場所を開き、`Assets.car` ファイルを Defold プロジェクトにコピーします。

    /Library/Developer/Xcode/DerivedData/YOUR-PRODUCT-NAME-cbqnwzfisotwygbybxohrhambkjy/Build/Products/Debug-iphoneos/Icons.app/Assets.car

アセットカタログファイルが用意できたら、そのファイルとアイコンを *game.project* から参照できます。

![game.project へのアイコンとアセットカタログの追加](images/ios/defold_icons_game_project.png)

::: sidenote
App Store のアイコンを *game.project* から参照する必要はありません。iTunes Connect へのアップロード時に、`Assets.car` ファイルから自動的に抽出されます。
:::


## iOS アプリケーションバンドルのインストール {#installing-an-ios-application-bundle}

エディターは、iOS アプリケーションバンドルである *.ipa* ファイルを書き出します。このファイルをデバイスにインストールするには、次のいずれかのツールを使えます。

* Xcode の `Devices and Simulators` ウィンドウ
* [`ios-deploy`](https://github.com/ios-control/ios-deploy) コマンドラインツール
* macOS App Store の [`Apple Configurator 2`](https://apps.apple.com/us/app/apple-configurator-2/)
* iTunes

`xcrun simctl` コマンドラインツールを使って、Xcode から利用できる iOS シミュレーターを操作することもできます。

```
# show a list of available devices
xcrun simctl list

# boot an iPhone X simulator
xcrun simctl boot "iPhone X"

# install your.app to a booted simulator
xcrun simctl install booted your.app

# launch the simulator
open /Applications/Xcode.app/Contents/Developer/Applications/Simulator.app
```

:[Apple Privacy Manifest](../shared/apple-privacy-manifest.md)


## 輸出コンプライアンス情報 {#export-compliance-information}

App Store にゲームを提出すると、ゲームでの暗号化の使用に関する輸出コンプライアンス情報の提供を求められます。[Apple はこれが必要な理由を次のように説明しています](https://developer.apple.com/documentation/security/complying_with_encryption_export_regulations)。

「TestFlight または App Store にアプリを提出すると、アプリは米国内のサーバーにアップロードされます。米国またはカナダ以外でアプリを配布する場合、法人の所在地にかかわらず、アプリには米国の輸出法が適用されます。アプリで暗号化を使用したり、暗号化にアクセスしたり、暗号化を含めたり、実装したり、組み込んだりしている場合、これは暗号化ソフトウェアの輸出とみなされます。そのため、アプリには米国の輸出コンプライアンス要件に加え、アプリを配布する国の輸入コンプライアンス要件が適用されます。」

Defold ゲームエンジンは、次の目的で暗号化を使います。

* 安全な通信経路（HTTPS や SSL）を使った呼び出し
* Lua コードの著作権保護（複製を防ぐため）

Defold エンジンにおけるこれらの暗号化の用途は、米国および欧州連合の法律で、輸出コンプライアンス書類の要件から免除されています。ほとんどの Defold プロジェクトは引き続き免除対象となりますが、ほかの暗号方式を追加すると、この扱いが変わる場合があります。プロジェクトがこれらの法律の要件と App Store の規則を満たしていることを確認する責任は、開発者にあります。詳しくは、Apple の[輸出コンプライアンスの概要](https://help.apple.com/app-store-connect/#/dev88f5c7bf9)を参照してください。

プロジェクトが免除対象だと判断した場合は、[`ITSAppUsesNonExemptEncryption`](https://developer.apple.com/documentation/bundleresources/information-property-list/itsappusesnonexemptencryption) キーの値が `False` になるように、プロジェクトの `Info.plist` を設定します。詳しくは、[アプリケーションマニフェスト](/manuals/extensions-manifest-merge-tool)を参照してください。

## よくある質問 {#faq}
:[iOS FAQ](../shared/ios-faq.md)
