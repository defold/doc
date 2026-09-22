---
title: Defold のライブラリプロジェクトを使用する
brief: ライブラリ機能では、プロジェクト間でアセットを共有できます。このマニュアルでは、その仕組みを説明します。
---

# ライブラリ {#libraries}

ライブラリ（library）機能では、プロジェクト間でアセット（asset）を共有できます。シンプルでありながら非常に強力な仕組みで、作業の流れにさまざまな形で取り入れられます。

ライブラリは、次の用途に役立ちます:

* 完成したプロジェクトから新しいプロジェクトにアセットをコピーします。以前のゲームの続編を制作する場合、簡単に作業を始められます。
* テンプレートのライブラリを作成し、プロジェクトにコピーしてからカスタマイズしたり、特定の用途に合わせて変更したりします。
* 直接参照できる、作成済みのオブジェクトやスクリプトのライブラリを1つ以上作成します。共通のスクリプトモジュールを保存したり、グラフィックス、音声、アニメーションのアセットを共有するライブラリを作成したりする際に、とても便利です。

## ライブラリ共有の設定 {#setting-up-library-sharing}

共有するスプライト（sprite）とタイルソース（tile source）を含むライブラリを作成するとします。まず、[新しいプロジェクトを設定します](/manuals/project-setup/)。プロジェクト内で共有するフォルダーを決め、そのフォルダー名をプロジェクト設定の *`include_dirs`* プロパティに追加します。複数のフォルダーを指定する場合は、名前をスペースで区切ります:

![共有するディレクトリ](images/libraries/libraries_include_dirs.png)

このライブラリを別のプロジェクトに追加する前に、ライブラリの場所を指定する方法が必要です。

## ライブラリの URL {#library-url}

ライブラリは標準的な URL で参照します。GitHub でホストされているプロジェクトの場合は、プロジェクトのリリースの URL を使用します:

![GitHub のライブラリ URL](images/libraries/libraries_library_url_github.png)

::: important
ライブラリプロジェクトの `master` ブランチではなく、常に特定のリリースに依存することを推奨します。これにより、ライブラリプロジェクトの `master` ブランチから最新の変更（互換性を損なう可能性のある変更を含みます）を常に取得するのではなく、ライブラリプロジェクトの変更をいつ取り込むかを開発者自身で決められます。
:::

::: important
サードパーティー製のライブラリは、使用前に必ず確認することを推奨します。詳しくは、[サードパーティー製ソフトウェアの利用を安全にする方法](https://defold.com/manuals/application-security/#securing-your-use-of-third-party-software)を参照してください。
:::

### 基本アクセス認証 {#basic-access-authentication}

一般公開されていないライブラリを使用する場合は、ライブラリの URL にユーザー名とパスワードまたはトークンを追加して、基本アクセス認証を行えます:

```
https://username:password@github.com/defold/private/archive/main.zip
```

`username` フィールドと `password` フィールドが抽出され、`Authorization` リクエストヘッダーとして追加されます。これは、基本アクセス認可をサポートする任意のサーバーで機能します。

::: important
生成した個人用アクセストークンやパスワードを共有したり、誤って漏えいさせたりしないようにしてください。悪意のある人物の手に渡ると、深刻な結果を招くおそれがあります。
:::

ライブラリの URL に認証情報を平文で含めることで誤って漏えいさせないように、文字列の置換パターンを使用し、認証情報を環境変数に保存することもできます:

```
https://__PRIVATE_USERNAME__:__PRIVATE_TOKEN__@github.com/defold/private/archive/main.zip
```

上の例では、ユーザー名とトークンがシステムの環境変数 `PRIVATE_USERNAME` と `PRIVATE_TOKEN` から読み取られます。

#### GitHub の認証 {#github-authentication}

GitHub のプライベートリポジトリから取得するには、[個人用アクセストークンを生成](https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/creating-a-personal-access-token)し、それをパスワードとして使用する必要があります。

```
https://github-username:personal-access-token@github.com/defold/private/archive/main.zip
```

#### GitLab の認証 {#gitlab-authentication}

GitLab のプライベートリポジトリから取得するには、[個人用アクセストークンを生成](https://docs.gitlab.com/ee/security/token_overview.html)し、URL パラメーターとして送信する必要があります。

```
https://gitlab.com/defold/private/-/archive/main/test-main.zip?private_token=personal-access-token
```

### 高度なアクセス認証 {#advanced-access-authentication}

基本アクセス認証を使用すると、ユーザーのアクセストークンとユーザー名が、プロジェクトで使用するどのリポジトリでも共有されます。チームが1人より多い場合、これが問題になることがあります。この問題を解決するには、リポジトリのライブラリへのアクセスに「読み取り専用」のユーザーを使用する必要があります。GitHub では、組織、チーム、リポジトリを編集する必要のない（つまり読み取り専用の）ユーザーが必要です。

GitHub での手順:
* [組織を作成します](https://docs.github.com/en/github/setting-up-and-managing-organizations-and-teams/creating-a-new-organization-from-scratch)
* [組織内にチームを作成します](https://docs.github.com/en/github/setting-up-and-managing-organizations-and-teams/creating-a-team)
* [対象のプライベートリポジトリを組織に移譲します](https://docs.github.com/en/github/administering-a-repository/transferring-a-repository)
* [チームにリポジトリへの「読み取り専用」アクセス権を付与します](https://docs.github.com/en/github/setting-up-and-managing-organizations-and-teams/managing-team-access-to-an-organization-repository)
* [このチームに所属するユーザーを作成または選択します](https://docs.github.com/en/github/setting-up-and-managing-organizations-and-teams/organizing-members-into-teams)
* 上記の「基本アクセス認証」を使用して、このユーザーの個人用アクセストークンを作成します

この時点で、新しいユーザーの認証情報をリポジトリにコミットしてプッシュできます。これにより、プライベートリポジトリで作業する人は誰でも、ライブラリ自体の編集権限を持たずに、ライブラリとして取得できるようになります。

::: important
読み取り専用ユーザーのトークンには、そのライブラリを使用しているゲームのリポジトリにアクセスできる人なら誰でも完全にアクセスできます。
:::

この解決策は Defold フォーラムで提案され、[このスレッドで議論されました](https://forum.defold.com/t/private-github-for-library-solved/67240)。

## ライブラリへの依存関係の設定 {#setting-up-library-dependencies}

ライブラリにアクセスするプロジェクトを開きます。プロジェクト設定の *dependencies* プロパティにライブラリの URL を追加します。必要に応じて、依存するプロジェクトを複数指定できます。`+` ボタンで1つずつ追加し、`-` ボタンで削除します:

![依存関係](images/libraries/libraries_dependencies.png)

次に、<kbd>Project ▸ Fetch Libraries</kbd> を選択して、ライブラリへの依存関係を更新します。これはプロジェクトを開くたびに自動的に行われるため、プロジェクトを開き直さずに依存関係が変わった場合にだけ、この操作が必要です。依存先のライブラリを追加または削除した場合や、依存先のライブラリプロジェクトのいずれかを誰かが変更して同期した場合が該当します。

![ライブラリの取得](images/libraries/libraries_fetch_libraries.png)

これで、共有したフォルダーが *Assets ペイン* に表示され、共有したすべてのものを使用できます。ライブラリプロジェクトに加えられて同期された変更は、使用するプロジェクトで利用できます。

![ライブラリの設定完了](images/libraries/libraries_done.png)

## 依存先ライブラリ内のファイルの編集 {#editing-files-in-library-dependencies}

ライブラリ内のファイルは保存できません。変更を加えることはでき、エディターはその変更を反映してビルドできるため、テストに便利です。ただし、ファイル自体は変更されず、ファイルを閉じるとすべての変更が破棄されます。

ライブラリのファイルを変更したい場合は、必ずライブラリを自分用にフォークし、そのフォークで変更してください。別の方法として、ライブラリのフォルダー全体をプロジェクトのディレクトリにコピーして貼り付け、ローカルのコピーを使用することもできます。この場合、ローカルのフォルダーが元の依存先より優先されるため、`game.project` から依存関係のリンクを削除することを推奨します（その後、<kbd>Project ▸ Fetch Libraries</kbd> を選択するのを忘れないでください）。

`builtins` も、エンジンが提供するライブラリです。その中のファイルを編集したい場合は、必ずプロジェクトにコピーし、元の `builtins` ファイルの代わりにコピーを使用してください。たとえば、`default.render_script` を変更するには、`/builtins/render/default.render` と `/builtins/render/default.render_script` の両方を、それぞれ `my_custom.render` と `my_custom.render_script` としてプロジェクトのフォルダーにコピーします。次に、ローカルの `my_custom.render` を更新して、組み込みのものではなく `my_custom.render_script` を参照するようにし、`game.project` の Render 設定に独自の `my_custom.render` を設定します。

マテリアル（material）をコピーして貼り付け、特定の種類のすべてのコンポーネント（component）で使用したい場合は、[プロジェクトごとのテンプレート](/manuals/editor/#creating-new-project-files)を使用すると便利な場合があります。

## 無効な参照 {#broken-references}

ライブラリ共有に含まれるのは、共有フォルダーの下にあるファイルだけです。共有する階層の外にあるアセットを参照するものを作成すると、参照パスの参照先が見つからなくなります。

## 名前の衝突 {#name-collisions}

プロジェクト設定の *dependencies* には複数のプロジェクトの URL を指定できるため、名前の衝突が発生する場合があります。これは、依存先のプロジェクトのうち2つ以上が、プロジェクト設定の *`include_dirs`* で同じ名前のフォルダーを共有している場合に発生します。

Defold は、*dependencies* リストに指定されたプロジェクトの URL の順序に従い、同じ名前のフォルダーへの最後の参照だけを残して、それ以外をすべて無視することで名前の衝突を解決します。たとえば、依存関係に3つのライブラリプロジェクトの URL を指定し、すべてが *items* という名前のフォルダーを共有しているとします。この場合、表示される *items* フォルダーは1つだけで、URL リストの最後のプロジェクトに属するフォルダーになります。
