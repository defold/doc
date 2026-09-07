---
title: ネイティブ拡張 - ベストプラクティス
brief: このマニュアルでは、ネイティブ拡張（native extension）を開発する際のベストプラクティスについて説明します。
---

# ベストプラクティス {#best-practices}

複数のプラットフォームに対応するコードを書くのは難しいことがありますが、その開発と保守をしやすくする方法がいくつかあります。


## プロジェクト構成 {#project-structure}

拡張を作成する際には、開発と保守の両方に役立つ点がいくつかあります。

### Lua API

Lua API とその実装は、それぞれ1つだけにすることをお勧めします。これにより、すべてのプラットフォームで同じ動作を実現しやすくなります。

対象のプラットフォームで拡張をサポートしない場合は、Lua モジュールをまったく登録しないことをお勧めします。そうすれば、`nil` かどうかを調べてサポートの有無を検出できます。

```lua
    if myextension ~= nil then
        myextension.do_something()
    end
```

### フォルダー構成 {#folder-structure}

拡張では、次のフォルダー構成がよく使われます。

```
    /root
        /input
        /main                            -- All the files for the actual example project
            /...
        /myextension                     -- The actual root folder of the extension
            ext.manifest
            /include                     -- External includes, used by other extensions
            /libs
                /<platform>              -- External libraries for all supported platforms
            /src
                myextension.cpp          -- The extension Lua api and the extension life cycle functions
                                            Also contains generic implementations of your Lua api functions.
                myextension_private.h    -- Your internal api that each platform will implement (I.e. `myextension_Init` etc)
                myextension.mm           -- If native calls are needed for iOS/macOS. Implements `myextension_Init` etc for iOS/macOS
                myextension_android.cpp  -- If JNI calls are needed for Android. Implements `myextension_Init` etc for Android
                /java
                    /<platform>          -- Any java files needed for Android
            /res                         -- Any resources needed for a platform
            /external
                README.md                -- Notes/scripts on how to build or package any external libraries
        /bundleres                       -- Resources that should be bundles for (see game.project and the [bundle_resources setting]([physics scale setting](/manuals/project-settings/#project))
            /<platform>
        game.project
        game.appmanifest                 -- Any extra app configuration info
```

`myextension.mm` と `myextension_android.cpp` が必要になるのは、そのプラットフォームに固有のネイティブ呼び出しを行う場合だけです。

#### プラットフォーム別のフォルダー {#platform-folders}

特定の場所では、アプリケーションのコンパイルやバンドル作成で使うファイルを識別するために、プラットフォームのアーキテクチャをフォルダー名として使います。形式は次のとおりです。

    <architecture>-<platform>

現在の一覧は次のとおりです。

    arm64-ios, arm64_sim-ios, arm64-android, armv7-android, x86_64-android, x86_64-linux, x86_64-osx, x86_64-win32, x86-win32

たとえば、プラットフォーム固有のライブラリは次の場所に配置します。

    /libs
        /arm64-ios
                            /libFoo.a
        /arm64-android
                            /libFoo.a


## ネイティブコードの作成 {#writing-native-code}

Defold のソースでは C++ の機能を控えめに使っており、ほとんどのコードは C に近いものです。テンプレートはコンパイル時間と実行ファイルのサイズにコストがかかるため、少数のコンテナークラスを除いてほとんど使われていません。

### C++ のバージョン {#c-version}

コアエンジンのビルドには C++11 を使っていますが、Windows では C++14 を使っています。ゲーム機向けのビルドでは、現在は一般的に C++14 以降が必要です。

ネイティブ拡張では C++ のバージョンを固定せず、プラットフォームのツールチェーンの既定のバージョンを使います。

Defold のソースでは、C++ の最新の機能やバージョンの使用を避けています。主な理由は、ゲームエンジンを構築する際に新しい機能を必要としないことですが、C++ の最新機能を把握し続ける作業には時間がかかり、それらの機能を十分に使いこなすには貴重な時間を多く費やす必要があることも理由です。

これには、Defold が安定した ABI を維持できるという、拡張開発者にとっての利点もあります。また、最新の C++ 機能を使うと、プラットフォームごとのサポート状況の違いにより、ほかのプラットフォームでコードをコンパイルできなくなる可能性がある点にも注意してください。

### C++ の例外を使わない {#no-c-exceptions}

Defold は、エンジン内で例外をまったく使っていません。ゲームエンジンでは、データのほとんどが開発中にあらかじめ分かっているため、一般的に例外の使用を避けます。C++ の例外サポートを取り除くと、実行ファイルのサイズが小さくなり、実行時のパフォーマンスが向上します。

### 標準テンプレートライブラリ - STL {#standard-template-libraries-stl}

Defold エンジンは、一部のアルゴリズムや数学処理（`std::sort`、`std::upper_bound` など）を除いて STL のコードを使っていないため、拡張内で STL を使っても動作する場合があります。

ただし、拡張をほかの拡張やサードパーティー製のライブラリと組み合わせて使う際には、ABI の非互換性が障害となる可能性があることに、あらためて注意してください。

テンプレートを多用する STL ライブラリを避けると、ビルド時間も短くなり、さらに重要なことに、実行ファイルのサイズも小さくなります。

#### 文字列 {#strings}

Defold エンジンでは、`std::string` の代わりに `const char*` を使います。C++ やコンパイラーのバージョンが異なるものを混在させる場合、`std::string` の使用はよくある落とし穴です。ABI の不一致が起こる可能性があるためです。`const char*` といくつかの補助関数を使うことで、この問題を回避できます。

### 関数を非公開にする {#make-functions-hidden}

可能であれば、コンパイル単位内だけで使う関数には `static` キーワードを付けてください。これにより、コンパイラーがいくつかの最適化を行えるようになり、パフォーマンスの向上と実行ファイルのサイズ削減の両方につながる可能性があります。

## サードパーティー製のライブラリ {#3rd-party-libraries}

使用するサードパーティー製のライブラリを選ぶ際には、言語に関係なく、次の点を検討してください。

* 機能 - 解決したい具体的な問題を解決できますか？
* パフォーマンス - 実行時のパフォーマンスに負担がかかりますか？
* ライブラリのサイズ - 最終的な実行ファイルのサイズはどれだけ大きくなりますか？許容できる範囲ですか？
* 依存関係 - 追加のライブラリが必要ですか？
* サポート - ライブラリはどのような状態ですか？未解決の問題が多くありますか？現在も保守されていますか？
* ライセンス - このプロジェクトで使用しても問題ありませんか？


## オープンソースの依存先 {#open-source-dependencies}

依存先にアクセスできることを常に確認してください。たとえば GitHub 上の何かに依存している場合、そのリポジトリが削除されたり、突然方針や所有者が変わったりする可能性があります。リポジトリをフォークし、上流のプロジェクトの代わりに自分のフォークを使うことで、このリスクを軽減できます。

ライブラリ内のコードはゲームに組み込まれることを忘れないでください。ライブラリが本来行うべき処理だけを行い、それ以外の処理を行わないことを確認してください！
