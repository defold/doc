---
title: AWS Live Update内容上传
brief: 本节将解释如何在 Amazon Web Services 上创建一个具有有限访问权限的新用户，该用户可以与 Defold 编辑器一起使用，在您打包游戏时自动上传 Live update 资源。
---

# 设置 Amazon Web Service

要将 Defold Live update 功能与 Amazon 服务一起使用，您需要一个 Amazon Web Services 账户。如果您还没有账户，可以在这里创建：https://aws.amazon.com/。

本节将解释如何在 Amazon Web Services 上创建一个具有有限访问权限的新用户，该用户可以与 Defold 编辑器一起使用，在您打包游戏时自动上传 Live update 资源，以及如何配置 Amazon S3 以允许游戏客户端检索资源。有关如何配置 Amazon S3 的更多信息，请参阅 [Amazon S3 文档](http://docs.aws.amazon.com/AmazonS3/latest/dev/Welcome.html)。

1. 为 Live update 资源创建存储桶

    打开 `Services` 菜单并选择位于 _Storage_ 类别下的 `S3`（[Amazon S3 Console](https://console.aws.amazon.com/s3)）。您将看到所有现有的存储桶以及创建新存储桶的选项。虽然可以使用现有的存储桶，但我们建议您为 Live update 资源创建一个新的存储桶，以便您可以轻松限制访问。
    
    ![Create a bucket](images/live-update/01-create-bucket.png)

2. 为您的存储桶添加存储桶策略

    选择您希望使用的存储桶，打开 *Properties* 面板并展开面板内的 *Permissions* 选项。通过点击 *Add bucket policy* 按钮打开存储桶策略。本示例中的存储桶策略将允许匿名用户从存储桶中检索文件，这将允许游戏客户端下载游戏所需的 Live update 资源。有关存储桶策略的更多信息，请参阅 [Amazon 文档](https://docs.aws.amazon.com/AmazonS3/latest/dev/using-iam-policies.html)。

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

    ![Bucket policy](images/live-update/02-bucket-policy.png)

3. 为您的存储桶添加 CORS 配置（可选）

    [Cross-Origin Resource Sharing (CORS)](https://en.wikipedia.org/wiki/Cross-origin_resource_sharing) 是一种允许网站使用 JavaScript 从不同域检索资源的机制。如果您打算将游戏发布为 HTML5 客户端，则需要为存储桶添加 CORS 配置。

    选择您希望使用的存储桶，打开 *Properties* 面板并展开面板内的 *Permissions* 选项。通过点击 *Add CORS Configuration* 按钮打开存储桶策略。本示例中的配置将通过指定通配符域允许来自任何网站的访问，尽管如果您知道将在哪些域上提供游戏，可以进一步限制此访问。有关 Amazon CORS 配置的更多信息，请参阅 [Amazon 文档](https://docs.aws.amazon.com/AmazonS3/latest/dev/cors.html)。

    ```xml
    <?xml version="1.0" encoding="UTF-8"?>
    <CORSConfiguration xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
        <CORSRule>
            <AllowedOrigin>*</AllowedOrigin>
            <AllowedMethod>GET</AllowedMethod>
        </CORSRule>
    </CORSConfiguration>
    ```

    ![CORS configuration](images/live-update/03-cors-configuration.png)

4. 创建 IAM 策略

    打开 *Services* 菜单并选择位于 _Security, Identity & Compliance_ 类别下的 *IAM*（[Amazon IAM Console](https://console.aws.amazon.com/iam)）。选择左侧菜单中的 *Policies*，您将看到所有现有的策略以及创建新策略的选项。

    点击 *Create Policy* 按钮，然后选择 _Create Your Own Policy_。本示例中的策略将允许用户列出所有存储桶，这仅在为 Live update 配置 Defold 项目时才需要。它还将允许用户获取访问控制列表（ACL）并将资源上传到用于 Live update 资源的特定存储桶。有关 Amazon Identity and Access Management (IAM) 的更多信息，请参阅 [Amazon 文档](http://docs.aws.amazon.com/IAM/latest/UserGuide/access.html)。

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

    ![IAM policy](images/live-update/04-create-policy.png)

5. 创建用于编程访问的用户

    打开 *Services* 菜单并选择位于 _Security, Identity & Compliance_ 类别下的 *IAM*（[Amazon IAM Console](https://console.aws.amazon.com/iam)）。选择左侧菜单中的 *Users*，您将看到所有现有的用户以及添加新用户的选项。虽然可以使用现有用户，但我们建议您为 Live update 资源添加一个新用户，以便您可以轻松限制访问。

    点击 *Add User* 按钮，提供用户名并选择 *Programmatic access* 作为 *Access type*，然后按 *Next: Permissions*。选择 *Attach existing policies directly* 并选择您在第 4 步中创建的策略。

    完成该过程后，您将获得一个 *Access key ID* 和一个 *Secret access key*。

    ::: important
    存储这些密钥 *非常重要*，因为离开页面后您将无法从 Amazon 检索它们。
    :::

6. 创建凭证配置文件

    此时，您应该已经创建了一个存储桶，配置了存储桶策略，添加了 CORS 配置，创建了用户策略并创建了一个新用户。剩下的唯一事情是创建一个[凭证配置文件](https://aws.amazon.com/blogs/security/a-new-and-standardized-way-to-manage-credentials-in-the-aws-sdks)，以便 Defold 编辑器可以代表您访问存储桶。

    在您的主文件夹中创建一个新目录 *.aws*，并在新目录中创建一个名为 *credentials* 的文件。

    ```bash
    $ mkdir ~/.aws
    $ touch ~/.aws/credentials
    ```

    文件 *~/.aws/credentials* 将包含您通过编程访问访问 Amazon Web Services 的凭证，是管理 AWS 凭证的标准方式。在文本编辑器中打开文件，并按照下面显示的格式输入您的 *Access key ID* 和 *Secret access key*。

    ```ini
    [defold-liveupdate-example]
    aws_access_key_id = <Access key ID>
    aws_secret_access_key = <Secret access key>
    ```

    在括号内指定的标识符，在本例中为 _defold-liveupdate-example_，是您在 Defold 编辑器中配置项目的 Live update 设置时应提供的相同标识符。

    ![Live update settings](images/live-update/05-liveupdate-settings.png)
