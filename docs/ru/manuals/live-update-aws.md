---
title: Загрузка контента Live update в AWS
brief: В этом разделе объясняется, как создать нового пользователя с ограниченным доступом в Amazon Web Services, которого можно использовать вместе с редактором Defold для автоматической загрузки ресурсов Live update при бандлинге игры.
---

# Настройка Amazon Web Services

Чтобы использовать функцию Defold Live update вместе с сервисами Amazon, вам потребуется учетная запись Amazon Web Services. Если у вас еще нет учетной записи, ее можно создать здесь: https://aws.amazon.com/.

В этом разделе объясняется, как создать нового пользователя с ограниченным доступом в Amazon Web Services, которого можно использовать вместе с редактором Defold для автоматической загрузки ресурсов Live update при бандлинге игры, а также как настроить Amazon S3 так, чтобы игровые клиенты могли получать ресурсы. Дополнительную информацию о настройке Amazon S3 см. в [документации Amazon S3](http://docs.aws.amazon.com/AmazonS3/latest/dev/Welcome.html).

1. Создайте bucket для ресурсов Live update

    Откройте меню `Services` и выберите `S3`, который находится в категории _Storage_ ([Amazon S3 Console](https://console.aws.amazon.com/s3)). Вы увидите все существующие bucket'ы и возможность создать новый. Хотя можно использовать уже существующий bucket, мы рекомендуем создать новый bucket для ресурсов Live update, чтобы было проще ограничить доступ.

    ![Создание bucket](images/live-update/01-create-bucket.png)

2. Добавьте политику bucket'а

    Выберите bucket, который хотите использовать, откройте панель *Properties* и разверните параметр *Permissions*. Откройте политику bucket'а, нажав кнопку *Add bucket policy*. Политика bucket'а в этом примере позволит анонимному пользователю получать файлы из bucket'а, что позволит игровому клиенту загружать ресурсы Live update, необходимые игре. Дополнительную информацию о политиках bucket'ов см. в [документации Amazon](https://docs.aws.amazon.com/AmazonS3/latest/dev/using-iam-policies.html).

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

    ![Политика bucket'а](images/live-update/02-bucket-policy.png)

3. Добавьте CORS-конфигурацию в bucket (необязательно)

    [Cross-Origin Resource Sharing (CORS)](https://en.wikipedia.org/wiki/Cross-origin_resource_sharing) — это механизм, позволяющий веб-сайту получать ресурс с другого домена с помощью JavaScript. Если вы планируете публиковать игру как HTML5-клиент, вам потребуется добавить CORS-конфигурацию в ваш bucket.

    Выберите bucket, который хотите использовать, откройте панель *Properties* и разверните параметр *Permissions*. Откройте настройки CORS, нажав кнопку *Add CORS Configuration*. Конфигурация в этом примере разрешит доступ с любого сайта, поскольку используется домен с подстановочным символом, хотя доступ можно дополнительно ограничить, если вы знаете, на каких доменах будет доступна ваша игра. Дополнительную информацию о конфигурации Amazon CORS см. в [документации Amazon](https://docs.aws.amazon.com/AmazonS3/latest/dev/cors.html).

    ```xml
    <?xml version="1.0" encoding="UTF-8"?>
    <CORSConfiguration xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
        <CORSRule>
            <AllowedOrigin>*</AllowedOrigin>
            <AllowedMethod>GET</AllowedMethod>
        </CORSRule>
    </CORSConfiguration>
    ```

    ![CORS-конфигурация](images/live-update/03-cors-configuration.png)

4. Создайте IAM-политику

    Откройте меню *Services* и выберите *IAM*, который находится в категории _Security, Identity & Compliance_ ([Amazon IAM Console](https://console.aws.amazon.com/iam)). Выберите *Policies* в меню слева, и вы увидите все существующие политики и возможность создать новую.

    Нажмите кнопку *Create Policy*, затем выберите _Create Your Own Policy_. Политика в этом примере позволит пользователю просматривать список всех bucket'ов, что требуется только при настройке проекта Defold для Live update. Она также позволит пользователю получать Access Control List (ACL) и загружать ресурсы в конкретный bucket, используемый для ресурсов Live update. Дополнительную информацию об Amazon Identity and Access Management (IAM) см. в [документации Amazon](http://docs.aws.amazon.com/IAM/latest/UserGuide/access.html).

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

    ![IAM-политика](images/live-update/04-create-policy.png)

5. Создайте пользователя для программного доступа

    Откройте меню *Services* и выберите *IAM*, который находится в категории _Security, Identity & Compliance_ ([Amazon IAM Console](https://console.aws.amazon.com/iam)). Выберите *Users* в меню слева, и вы увидите всех существующих пользователей и возможность добавить нового. Хотя можно использовать существующего пользователя, мы рекомендуем добавить отдельного пользователя для ресурсов Live update, чтобы было проще ограничить доступ.

    Нажмите кнопку *Add User*, укажите имя пользователя и выберите *Programmatic access* как *Access type*, затем нажмите *Next: Permissions*. Выберите *Attach existing policies directly* и укажите политику, созданную на шаге 4.

    После завершения процесса вы получите *Access key ID* и *Secret access key*.

    ::: important
    *Очень важно* сохранить эти ключи, поскольку после ухода со страницы вы не сможете получить их в Amazon повторно.
    :::

6. Создайте файл профиля учетных данных

    На этом этапе вы должны были создать bucket, настроить политику bucket'а, добавить CORS-конфигурацию, создать пользовательскую политику и нового пользователя. Осталось только создать [credentials profile file](https://aws.amazon.com/blogs/security/a-new-and-standardized-way-to-manage-credentials-in-the-aws-sdks), чтобы редактор Defold мог обращаться к bucket'у от вашего имени.

    Создайте новый каталог *.aws* в домашней папке и создайте в нем файл *credentials*.

    ```bash
    $ mkdir ~/.aws
    $ touch ~/.aws/credentials
    ```

    Файл *~/.aws/credentials* будет содержать ваши учетные данные для доступа к Amazon Web Services через программный доступ и является стандартизированным способом управления AWS credentials. Откройте файл в текстовом редакторе и укажите *Access key ID* и *Secret access key* в формате, показанном ниже.

    ```ini
    [defold-liveupdate-example]
    aws_access_key_id = <Access key ID>
    aws_secret_access_key = <Secret access key>
    ```

    Идентификатор, указанный в квадратных скобках, в данном примере _defold-liveupdate-example_, — это тот же идентификатор, который нужно указать при настройке параметров Live update вашего проекта в редакторе Defold.

    ![Настройки Live update](images/live-update/05-liveupdate-settings.png)
