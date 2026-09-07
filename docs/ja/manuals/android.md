---
title: Android プラットフォーム向けの Defold 開発
brief: このマニュアルでは、Android デバイスで Defold アプリケーションをビルドして実行する方法を説明します
---

# Android 向け開発 {#android-development}

Android デバイスでは、自作のアプリを自由に実行できます。ゲームをビルドして Android デバイスにコピーするのは非常に簡単です。このマニュアルでは、Android 向けにゲームのバンドル（bundle）を作成する手順を説明します。開発中は、コンテンツとコードをデバイスに直接ホットリロード（hot reload）できるため、[開発用アプリ（development app）](/manuals/dev-app) でゲームを実行する方法がよく選ばれます。

## Android と Google Play の署名プロセス {#android-and-google-play-signing-process}

Android では、すべての APK に、デバイスへのインストールまたは更新の前に証明書でデジタル署名を行う必要があります。Android App Bundle を使用する場合は、Play Console にアップロードする前にアプリバンドルに署名するだけで、残りは [Play App Signing](https://developer.android.com/studio/publish/app-signing#app-signing-google-play) が処理します。ただし、Google Play やほかのアプリストアへのアップロード、またはストアを介さない配布のために、アプリに手動で署名することもできます。

Defold エディターまたは[コマンドラインツール](/manuals/bob) で Android アプリケーションのバンドルを作成するときに、アプリケーションの署名に使うキーストア（証明書とキーを含みます）とキーストアのパスワードを指定できます。指定しない場合、Defold はデバッグ用キーストアを生成し、アプリケーションバンドルの署名に使用します。

::: important
デバッグ用キーストアで署名したアプリケーションは、Google Play に **絶対に** アップロードしないでください。必ず自分で作成した専用のキーストアを使用してください。
:::

## キーストアの作成 {#creating-a-keystore}

::: sidenote
Defold は Android の署名プロセスにキーストアを使用します。[詳細はこのフォーラムの投稿を参照してください](https://forum.defold.com/t/upcoming-change-to-the-android-build-pipeline/66084)。
:::

キーストアは [Android Studio を使用して](https://developer.android.com/studio/publish/app-signing#generate-key)、またはターミナル/コマンドプロンプトから作成できます。

```bash
keytool -genkey -v -noprompt -dname "CN=John Smith, OU=Area 51, O=US Air Force, L=Unknown, ST=Nevada, C=US" -keystore mykeystore.keystore -storepass 5Up3r_53cR3t -alias myAlias -keyalg RSA -validity 9125
```

これにより、キーと証明書を含む `mykeystore.keystore` という名前のキーストアファイルが作成されます。キーと証明書へのアクセスは、パスワード `5Up3r_53cR3t` で保護されます。キーと証明書の有効期間は25年（9125日）です。生成されたキーと証明書は、エイリアス `myAlias` で識別されます。

::: important
キーストアとそのパスワードは、安全な場所に保管してください。自分でアプリケーションに署名して Google Play にアップロードしている場合、キーストアまたはキーストアのパスワードを紛失すると、Google Play 上のアプリケーションを更新する方法がなくなります。Google Play App Signing を使用して Google にアプリケーションの署名を任せると、この問題を回避できます。
:::


## Android アプリケーションバンドルの作成 {#creating-an-android-application-bundle}

エディターを使うと、ゲームのスタンドアロンアプリケーションバンドルを簡単に作成できます。バンドルの作成前に、*game.project* [プロジェクト設定ファイル](/manuals/project-settings/#android) で、アプリに使用するアイコンやバージョンコードなどを指定できます。

バンドルを作成するには、メニューから <kbd>Project ▸ Bundle... ▸ Android Application...</kbd> を選択します。

ランダムなデバッグ用証明書をエディターで自動生成する場合は、*Keystore* と *Keystore password* のフィールドを空のままにします。

![Android バンドルの署名](images/android/sign_bundle.png)

特定のキーストアでバンドルに署名する場合は、*Keystore* と *Keystore password* を指定します。*Keystore* のファイルの拡張子は `.keystore` とし、パスワードは拡張子 `.txt` のテキストファイルに保存する必要があります。キーストア内のキーがキーストア自体とは異なるパスワードを使う場合は、*Key password* も指定できます。

![Android バンドルの署名](images/android/sign_bundle2.png)

Defold は APK ファイルと AAB ファイルの両方の作成に対応しています。*Bundle Format* ドロップダウンから APK または AAB を選択します。

アプリケーションバンドルの設定が完了したら、<kbd>Create Bundle</kbd> を押します。続いて、コンピューター上でバンドルを作成する場所を指定するよう求められます。

![Android アプリケーションパッケージファイル](images/android/apk_file.png)

:[Build Variants](../shared/build-variants.md)

### Android アプリケーションバンドルのインストール {#installing-an-android-application-bundle}

#### APK のインストール {#installing-an-apk}

*`.apk`* ファイルは、`adb` ツールでデバイスにコピーするか、[Google Play デベロッパーコンソール](https://play.google.com/apps/publish/) 経由で Google Play にコピーできます。

:[Android ADB](../shared/android-adb.md)

```
$ adb install Defold\ examples.apk
4826 KB/s (18774344 bytes in 3.798s)
  pkg: /data/local/tmp/my_app.apk
Success
```

#### エディターを使った APK のインストール {#installing-an-apk-using-editor}

エディターの Bundle ダイアログにある「Install on connected device」と「Launch installed app」のチェックボックスを使うと、*`.apk`* ファイルをインストールして起動できます。

![APK のインストールと起動](images/android/install_and_launch.png)

この機能を使うには、*ADB* をインストールし、接続したデバイスで *USB debugging* を有効にする必要があります。エディターが ADB コマンドラインツールのインストール場所を検出できない場合は、[Preferences](/manuals/editor-preferences/#tools) で指定する必要があります。

#### AAB のインストール {#installing-an-aab}

*.aab* ファイルは、[Google Play デベロッパーコンソール](https://play.google.com/apps/publish/) 経由で Google Play にアップロードできます。[Android bundletool](https://developer.android.com/studio/command-line/bundletool) を使い、*.aab* ファイルから *`.apk`* ファイルを生成してローカルにインストールすることもできます。

## 権限 {#permissions}

Defold エンジンのすべての機能を動作させるには、いくつかの異なる権限が必要です。権限は、*game.project* [プロジェクト設定ファイル](/manuals/project-settings/#android) で指定した `AndroidManifest.xml` に定義されています。Android の権限について詳しくは、[公式ドキュメント](https://developer.android.com/guide/topics/permissions/overview) を参照してください。デフォルトのマニフェストでは、次の権限を要求します。

### android.permission.INTERNET と android.permission.ACCESS_NETWORK_STATE（保護レベル: normal） {#androidpermissioninternet-and-androidpermissionaccess_network_state-protection-level-normal}
アプリケーションが *ネットワークソケット* を開き、ネットワークに関する情報にアクセスできるようにします。これらの権限は、インターネットアクセスに必要です。（[Android 公式ドキュメント](https://developer.android.com/reference/android/Manifest.permission#INTERNET)）および（[Android 公式ドキュメント](https://developer.android.com/reference/android/Manifest.permission#ACCESS_NETWORK_STATE)）。

### android.permission.WAKE_LOCK（保護レベル: normal） {#androidpermissionwake_lock-protection-level-normal}
PowerManager WakeLocks を使い、プロセッサーがスリープ状態になったり、画面が暗くなったりするのを防げるようにします。この権限は、プッシュ通知の受信中にデバイスがスリープ状態になるのを一時的に防ぐために必要です。（[Android 公式ドキュメント](https://developer.android.com/reference/android/Manifest.permission#WAKE_LOCK)）


## AndroidX の使用 {#using-androidx}
AndroidX は、メンテナンスが終了した従来の Android Support Library を大幅に改善したものです。AndroidX パッケージは、同等の機能と新しいライブラリを提供することで、Support Library を完全に置き換えます。[Asset Portal](/assets) にある Android 拡張のほとんどは AndroidX に対応しています。AndroidX を使用せず、従来の Android Support Library を使用する場合は、[アプリケーションマニフェスト](https://defold.com/manuals/app-manifest/) で `Use Android Support Lib` にチェックを入れると、AndroidX を明示的に無効にできます。

![](images/android/enable_supportlibrary.png)

## よくある質問 {#faq}
:[Android FAQ](../shared/android-faq.md)
