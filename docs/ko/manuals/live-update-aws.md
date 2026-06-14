---
title: AWS로 Live update 컨텐츠 업로드하기
brief: 이 섹션에서는 게임을 번들링할 때 Defold 에디터와 함께 사용해 Live update 리소스를 자동으로 업로드할 수 있도록 Amazon Web Services에서 제한된 액세스 권한을 가진 새 사용자를 만드는 방법을 설명합니다.
---

# Amazon Web Services 설정

Defold Live update 기능을 Amazon 서비스와 함께 사용하려면 Amazon Web Services 계정이 필요합니다. 아직 계정이 없다면 여기에서 만들 수 있습니다 https://aws.amazon.com/.

이 섹션에서는 게임을 번들링할 때 Defold 에디터와 함께 사용해 Live update 리소스를 자동으로 업로드할 수 있도록 Amazon Web Services에서 제한된 액세스 권한을 가진 새 사용자를 만드는 방법과, 게임 클라이언트가 리소스를 가져올 수 있도록 Amazon S3를 구성하는 방법을 설명합니다. Amazon S3 구성 방법에 대한 추가 정보는 [Amazon S3 문서](http://docs.aws.amazon.com/AmazonS3/latest/dev/Welcome.html)를 참고하세요.

1. Live update 리소스용 버켓 생성

    `Services` 메뉴를 열고 _Storage_ 카테고리 아래에 있는 `S3`를 선택합니다([Amazon S3 Console](https://console.aws.amazon.com/s3)). 기존 버켓이 모두 표시되며 새 버켓을 만들 수 있는 옵션도 보입니다. 기존 버켓을 사용할 수도 있지만, 액세스를 쉽게 제한할 수 있도록 Live update 리소스용 새 버켓을 만드는 것을 권장합니다.

    ![버켓 생성](images/live-update/01-create-bucket.png)

2. 버켓에 버켓 정책 추가

    사용하려는 버켓을 선택하고 *Properties* 패널을 연 다음 패널 안의 *Permissions* 옵션을 펼칩니다. *Add bucket policy* 버튼을 클릭해 버켓 정책을 엽니다. 이 예제의 버켓 정책은 익명 사용자가 버켓에서 파일을 가져올 수 있게 허용하며, 이를 통해 게임 클라이언트가 게임에 필요한 Live update 리소스를 다운로드할 수 있습니다. 버켓 정책에 대한 추가 정보는 [Amazon 문서](https://docs.aws.amazon.com/AmazonS3/latest/dev/using-iam-policies.html)를 참고하세요.

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

    ![버켓 정책](images/live-update/02-bucket-policy.png)

3. 버켓에 CORS 설정 추가(선택 사항)

    [Cross-Origin Resource Sharing (CORS)](https://en.wikipedia.org/wiki/Cross-origin_resource_sharing)는 웹사이트가 JavaScript를 사용해 다른 도메인에서 리소스를 가져올 수 있게 하는 메커니즘입니다. 게임을 HTML5 클라이언트로 게시하려면 버켓에 CORS 설정을 추가해야 합니다.

    사용하려는 버켓을 선택하고 *Properties* 패널을 연 다음 패널 안의 *Permissions* 옵션을 펼칩니다. *Add CORS Configuration* 버튼을 클릭해 CORS 설정을 엽니다. 이 예제의 설정은 와일드카드 도메인을 지정하여 모든 웹사이트의 액세스를 허용하지만, 게임을 제공할 도메인을 알고 있다면 이 액세스를 더 제한할 수도 있습니다. Amazon CORS 설정에 대한 추가 정보는 [Amazon 문서](https://docs.aws.amazon.com/AmazonS3/latest/dev/cors.html)를 참고하세요.

    ```xml
    <?xml version="1.0" encoding="UTF-8"?>
    <CORSConfiguration xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
        <CORSRule>
            <AllowedOrigin>*</AllowedOrigin>
            <AllowedMethod>GET</AllowedMethod>
        </CORSRule>
    </CORSConfiguration>
    ```

    ![CORS 설정](images/live-update/03-cors-configuration.png)

4. IAM 정책 생성

    *Services* 메뉴를 열고 _Security, Identity & Compliance_ 카테고리 아래에 있는 *IAM*을 선택합니다([Amazon IAM Console](https://console.aws.amazon.com/iam)). 왼쪽 메뉴에서 *Policies*를 선택하면 기존 정책이 모두 표시되며 새 정책을 만들 수 있는 옵션도 보입니다.

    *Create Policy* 버튼을 클릭한 다음 _Create Your Own Policy_를 선택합니다. 이 예제의 정책은 사용자가 모든 버켓을 나열할 수 있게 허용하며, 이는 Live update용 Defold 프로젝트를 구성할 때만 필요합니다. 또한 사용자가 Access Control List (ACL)를 가져오고 Live update 리소스에 사용하는 특정 버켓에 리소스를 업로드할 수 있게 허용합니다. Amazon Identity and Access Management (IAM)에 대한 추가 정보는 [Amazon 문서](http://docs.aws.amazon.com/IAM/latest/UserGuide/access.html)를 참고하세요.

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

    ![IAM 정책](images/live-update/04-create-policy.png)

5. 프로그램 방식 액세스용 사용자 생성

    *Services* 메뉴를 열고 _Security, Identity & Compliance_ 카테고리 아래에 있는 *IAM*을 선택합니다([Amazon IAM Console](https://console.aws.amazon.com/iam)). 왼쪽 메뉴에서 *Users*를 선택하면 기존 사용자가 모두 표시되며 새 사용자를 추가할 수 있는 옵션도 보입니다. 기존 사용자를 사용할 수도 있지만, 액세스를 쉽게 제한할 수 있도록 Live update 리소스용 새 사용자를 추가하는 것을 권장합니다.

    *Add User* 버튼을 클릭하고 사용자 이름을 입력한 다음 *Access type*으로 *Programmatic access*를 선택하고 *Next: Permissions*를 누릅니다. *Attach existing policies directly*를 선택하고 4단계에서 만든 정책을 선택합니다.

    이 과정을 완료하면 *Access key ID*와 *Secret access key*가 제공됩니다.

    ::: important
    페이지를 떠난 뒤에는 Amazon에서 이 키들을 다시 가져올 수 없으므로 키를 저장해 두는 것이 *매우 중요*합니다.
    :::

6. 자격 증명 프로파일 파일 생성

    이 시점에서는 버켓 생성, 버켓 정책 구성, CORS 설정 추가, 사용자 정책 생성, 새 사용자 생성이 모두 완료되어 있어야 합니다. 남은 일은 Defold 에디터가 사용자를 대신해 버켓에 액세스할 수 있도록 [자격 증명 프로파일 파일](https://aws.amazon.com/blogs/security/a-new-and-standardized-way-to-manage-credentials-in-the-aws-sdks)을 만드는 것뿐입니다.

    홈 폴더에 새 디렉토리 *.aws*를 만들고, 새 디렉토리 안에 *credentials*라는 파일을 만듭니다.

    ```bash
    $ mkdir ~/.aws
    $ touch ~/.aws/credentials
    ```

    *~/.aws/credentials* 파일에는 프로그램 방식 액세스로 Amazon Web Services에 액세스하기 위한 자격 증명이 들어가며, 이는 AWS 자격 증명을 관리하는 표준화된 방식입니다. 텍스트 에디터에서 파일을 열고 아래 형식으로 *Access key ID*와 *Secret access key*를 입력합니다.

    ```ini
    [defold-liveupdate-example]
    aws_access_key_id = <Access key ID>
    aws_secret_access_key = <Secret access key>
    ```

    대괄호 안에 지정한 식별자, 이 예제에서는 _defold-liveupdate-example_이 Defold 에디터에서 프로젝트의 Live update 설정을 구성할 때 제공해야 하는 동일한 식별자입니다.

    ![Live update 설정](images/live-update/05-liveupdate-settings.png)
