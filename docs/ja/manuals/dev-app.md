---
title: デバイスで開発用アプリを実行する
brief: このマニュアルでは、デバイス上で開発とテストを繰り返すために、開発用アプリをデバイスにインストールする方法を説明します。
---

# モバイル開発用アプリ {#the-mobile-development-app}

開発用アプリ（development app）には、Wi-Fi 経由でコンテンツを送信できます。変更をテストするたびにバンドル（bundle）を作成してインストールする必要がなくなるため、開発とテストを繰り返す時間を大幅に短縮できます。1台以上のデバイスに開発用アプリをインストールして起動し、エディターでそのデバイスをビルドターゲット（build target）として選択します。

## 開発用アプリのインストール {#installing-a-development-app}

Debug モードでバンドルを作成した iOS または Android アプリケーションは、どれでも開発用アプリとして使用できます。実際、この方法を推奨します。開発用アプリに適切なプロジェクト設定が反映され、作業中のプロジェクトと同じ[ネイティブ拡張（native extension）](/manuals/extensions/)が使われるためです。 

コンテンツを一切含めずに、プロジェクトの Debug バリアントのバンドルを作成することもできます。このオプションを使うと、ネイティブ拡張を含み、このマニュアルで説明する開発とテストの繰り返しに適したバージョンのアプリケーションを作成できます。

![コンテンツを含まないバンドル](images/dev-app/contentless-bundle.png)

### iOS へのインストール {#installing-on-ios}

[iOS マニュアルの手順](/manuals/ios/#creating-an-ios-application-bundle)に従って、iOS 向けのバンドルを作成します。バリアントには必ず Debug を選択してください！

### Android へのインストール {#installing-on-android}

[Android マニュアルの手順](https://defold.com/manuals/android/#creating-an-android-application-bundle)に従って、Android 向けのバンドルを作成します。

## ゲームの起動 {#launching-your-game}

デバイスでゲームを起動するには、開発用アプリとエディターが、同じ Wi-Fi ネットワーク経由または USB 経由（後述）で接続できる必要があります。

1. エディターが起動して動作していることを確認します。
2. デバイスで開発用アプリを起動します。
3. エディターの <kbd>Project ▸ Targets</kbd> でデバイスを選択します。
4. <kbd>Project ▸ Build</kbd> を選択してゲームを実行します。ゲームのコンテンツはネットワーク経由でデバイスへストリーミングされるため、ゲームの起動までに時間がかかることがあります。
5. ゲームの実行中は、通常どおり[ホットリロード（hot reload）](/manuals/hot-reload/)を使用できます。

### Windows で USB を使って iOS デバイスに接続する {#connecting-to-an-ios-device-using-usb-on-windows}

Windows で USB 経由で iOS デバイス上の開発用アプリに接続するには、まず [iTunes をインストールする](https://www.apple.com/lae/itunes/download/)必要があります。iTunes をインストールしたら、iOS デバイスの Settings メニューで [Personal Hotspot を有効にする](https://support.apple.com/en-us/HT204023)必要もあります。「Trust This Computer?」という警告が表示された場合は、Trust をタップします。これで、開発用アプリの実行中は <kbd>Project ▸ Targets</kbd> にデバイスが表示されるはずです。

### Linux で USB を使って iOS デバイスに接続する {#connecting-to-an-ios-device-using-usb-on-linux}

Linux で USB を使って接続する場合は、デバイスの Settings メニューで Personal Hotspot を有効にする必要があります。「Trust This Computer?」という警告が表示された場合は、Trust をタップします。これで、開発用アプリの実行中は <kbd>Project ▸ Targets</kbd> にデバイスが表示されるはずです。

### macOS で USB を使って iOS デバイスに接続する {#connecting-to-an-ios-device-using-usb-on-macos}

新しいバージョンの iOS では、macOS で USB を使って接続すると、デバイスとコンピューターの間に新しい Ethernet インターフェースが自動的に開かれます。開発用アプリの実行中は <kbd>Project ▸ Targets</kbd> にデバイスが表示されるはずです。

古いバージョンの iOS では、macOS で USB を使って接続する場合、デバイスの Settings メニューで Personal Hotspot を有効にする必要があります。「Trust This Computer?」という警告が表示された場合は、Trust をタップします。これで、開発用アプリの実行中は <kbd>Project ▸ Targets</kbd> にデバイスが表示されるはずです。

### macOS で USB を使って Android デバイスに接続する {#connecting-to-an-android-device-using-usb-on-macos}

macOS では、Android デバイスが USB Tethering Mode になっていると、そのデバイスで実行中の開発用アプリに USB 経由で接続できます。macOS では、[HoRNDIS](https://joshuawise.com/horndis#available_versions) などのサードパーティー製ドライバーをインストールする必要があります。HoRNDIS をインストールしたら、Security & Privacy 設定で実行を許可する必要もあります。USB Tethering を有効にすると、開発用アプリの実行中は <kbd>Project ▸ Targets</kbd> にデバイスが表示されます。

### Windows または Linux で USB を使って Android デバイスに接続する {#connecting-to-an-android-device-using-usb-on-windows-or-linux}

Windows と Linux では、Android デバイスが USB Tethering Mode になっていると、そのデバイスで実行中の開発用アプリに USB 経由で接続できます。USB Tethering を有効にすると、開発用アプリの実行中は <kbd>Project ▸ Targets</kbd> にデバイスが表示されます。

## トラブルシューティング {#troubleshooting}

アプリケーションをダウンロードできない
: アプリの署名に使用したモバイルプロビジョニングに、デバイスの UDID が含まれていることを確認します。

Targets メニューにデバイスが表示されない
: デバイスがコンピューターと同じ Wi-Fi ネットワークに接続されていることを確認します。開発用アプリが Debug モードでビルドされていることを確認します。

バージョンが一致しないというメッセージが表示され、ゲームが起動しない
: これは、エディターを最新バージョンにアップグレードした場合に発生します。新しいバージョンをビルドしてインストールする必要があります。
