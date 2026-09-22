---
title: AWS への Live Update コンテンツのアップロード
brief: このセクションでは、Amazon Web Services でアクセスを制限した新しいユーザーを作成し、Defold エディターと組み合わせてゲームのバンドル作成時に Live Update リソースを自動的にアップロードする方法を説明します。
---

# Amazon Web Service の設定 {#setting-up-amazon-web-service}

Defold の Live Update 機能を Amazon のサービスと組み合わせて使用するには、Amazon Web Services のアカウントが必要です。アカウントをまだ持っていない場合は、https://aws.amazon.com/ で作成できます。

このセクションでは、Amazon Web Services でアクセスを制限した新しいユーザーを作成し、Defold エディターと組み合わせてゲームのバンドル（bundle）作成時に Live Update リソース（resource）を自動的にアップロードする方法と、ゲームクライアントがリソースを取得できるように Amazon S3 を設定する方法を説明します。Amazon S3 の設定方法の詳細は、[Amazon S3 のドキュメント](http://docs.aws.amazon.com/AmazonS3/latest/dev/Welcome.html)を参照してください。

1. Live Update リソース用のバケットを作成する

    `Services` メニューを開き、_Storage_ カテゴリーにある `S3` を選択します（[Amazon S3 コンソール](https://console.aws.amazon.com/s3)）。既存のすべてのバケットと、新しいバケットを作成するオプションが表示されます。既存のバケットを使用することもできますが、アクセスを簡単に制限できるように、Live Update リソース用に新しいバケットを作成することをお勧めします。

    ![バケットの作成](images/live-update/01-create-bucket.png)

2. バケットにバケットポリシーを追加する

    使用するバケットを選択し、*Properties* パネルを開いて、パネル内の *Permissions* オプションを展開します。*Add bucket policy* ボタンをクリックしてバケットポリシーを開きます。この例のバケットポリシーは、匿名ユーザーがバケットからファイルを取得することを許可します。これにより、ゲームクライアントはゲームに必要な Live Update リソースをダウンロードできます。バケットポリシーの詳細は、[Amazon のドキュメント](https://docs.aws.amazon.com/AmazonS3/latest/dev/using-iam-policies.html)を参照してください。

    ```json
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "AddPerm",
                "Effect": "Allow",
                "Principal": "*",
                "Action": "s3:GetObject",
                "Resource": "arn:aws:s3:::defold-liveupdate-example/*"
            }
        ]
    }
    ```

    ![バケットポリシー](images/live-update/02-bucket-policy.png)

3. バケットに CORS 設定を追加する（任意）

    [クロスオリジンリソース共有（Cross-Origin Resource Sharing、CORS）](https://en.wikipedia.org/wiki/Cross-origin_resource_sharing)は、Web サイトが JavaScript を使って異なるドメインからリソースを取得できるようにする仕組みです。ゲームを HTML5 クライアントとして公開する場合は、バケットに CORS 設定を追加する必要があります。

    使用するバケットを選択し、*Properties* パネルを開いて、パネル内の *Permissions* オプションを展開します。*Add CORS Configuration* ボタンをクリックしてバケットポリシーを開きます。この例の設定は、ドメインにワイルドカードを指定することで、あらゆる Web サイトからのアクセスを許可します。ただし、ゲームを公開するドメインが分かっている場合は、アクセスをさらに制限できます。Amazon の CORS 設定の詳細は、[Amazon のドキュメント](https://docs.aws.amazon.com/AmazonS3/latest/dev/cors.html)を参照してください。

    ```xml
    <?xml version="1.0" encoding="UTF-8"?>
    <CORSConfiguration xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
        <CORSRule>
            <AllowedOrigin>*</AllowedOrigin>
            <AllowedMethod>GET</AllowedMethod>
        </CORSRule>
    </CORSConfiguration>
    ```

    ![CORS 設定](images/live-update/03-cors-configuration.png)

4. IAM ポリシーを作成する

    *Services* メニューを開き、_Security, Identity & Compliance_ カテゴリーにある *IAM* を選択します（[Amazon IAM コンソール](https://console.aws.amazon.com/iam)）。左側のメニューで *Policies* を選択すると、既存のすべてのポリシーと、新しいポリシーを作成するオプションが表示されます。

    *Create Policy* ボタンをクリックし、_Create Your Own Policy_ を選択します。この例のポリシーは、ユーザーがすべてのバケットを一覧表示することを許可します。この権限は、Defold プロジェクトで Live Update を設定するときにのみ必要です。また、アクセスコントロールリスト（Access Control List、ACL）の取得と、Live Update リソースに使用する特定のバケットへのリソースのアップロードも許可します。Amazon Identity and Access Management（IAM）の詳細は、[Amazon のドキュメント](http://docs.aws.amazon.com/IAM/latest/UserGuide/access.html)を参照してください。

    ```json
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "s3:ListAllMyBuckets"
                ],
                "Resource": "arn:aws:s3:::*"
            },
            {
                "Effect": "Allow",
                "Action": [
                    "s3:GetBucketAcl"
                ],
                "Resource": "arn:aws:s3:::defold-liveupdate-example"
            },
            {
                "Effect": "Allow",
                "Action": [
                    "s3:PutObject"
                ],
                "Resource": "arn:aws:s3:::defold-liveupdate-example/*"
            }
        ]
    }
    ```

    ![IAM ポリシー](images/live-update/04-create-policy.png)

5. プログラムによるアクセス用のユーザーを作成する

    *Services* メニューを開き、_Security, Identity & Compliance_ カテゴリーにある *IAM* を選択します（[Amazon IAM コンソール](https://console.aws.amazon.com/iam)）。左側のメニューで *Users* を選択すると、既存のすべてのユーザーと、新しいユーザーを追加するオプションが表示されます。既存のユーザーを使用することもできますが、アクセスを簡単に制限できるように、Live Update リソース用に新しいユーザーを追加することをお勧めします。

    *Add User* ボタンをクリックしてユーザー名を入力し、*Access type* として *Programmatic access* を選択して、*Next: Permissions* を押します。*Attach existing policies directly* を選択し、手順4で作成したポリシーを選びます。

    手続きが完了すると、*Access key ID* と *Secret access key* が発行されます。

    ::: important
    ページを離れると、これらのキーを Amazon から再取得できなくなるため、保存しておくことが *非常に重要* です。
    :::

6. 認証情報のプロファイルファイルを作成する

    ここまでで、バケットの作成、バケットポリシーの設定、CORS 設定の追加、ユーザーポリシーの作成、新しいユーザーの作成が完了しているはずです。あとは、Defold エディターがユーザーに代わってバケットにアクセスできるように、[認証情報のプロファイルファイル](https://aws.amazon.com/blogs/security/a-new-and-standardized-way-to-manage-credentials-in-the-aws-sdks)を作成するだけです。

    ホームフォルダーに *.aws* という新しいディレクトリを作成し、その中に *credentials* という名前のファイルを作成します。

    ```bash
    $ mkdir ~/.aws
    $ touch ~/.aws/credentials
    ```

    *~/.aws/credentials* ファイルには、プログラムによるアクセスを通じて Amazon Web Services にアクセスするための認証情報を記述します。このファイルを使用する方法は、AWS 認証情報を管理する標準化された方法です。テキストエディターでファイルを開き、以下の形式で *Access key ID* と *Secret access key* を入力します。

    ```ini
    [defold-liveupdate-example]
    aws_access_key_id = <Access key ID>
    aws_secret_access_key = <Secret access key>
    ```

    角括弧内に指定した識別子（この例では _defold-liveupdate-example_ ）は、Defold エディターでプロジェクトの Live Update 設定を行う際に指定する識別子と同じです。

    ![Live Update 設定](images/live-update/05-liveupdate-settings.png)
