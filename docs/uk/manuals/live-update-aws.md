---
title: Вивантаження вмісту Live update в AWS
brief: У цьому розділі пояснено, як створити нового користувача з обмеженим доступом в Amazon Web Services, якого редактор Defold зможе використовувати для автоматичного вивантаження ресурсів Live update під час пакування гри.
---

# Налаштування Amazon Web Service {#setting-up-amazon-web-service}

Щоб використовувати функцію Live update у Defold разом із сервісами Amazon, вам потрібен обліковий запис Amazon Web Services. Якщо у вас ще немає облікового запису, ви можете створити його тут: https://aws.amazon.com/.

У цьому розділі пояснено, як створити нового користувача з обмеженим доступом в Amazon Web Services, якого редактор Defold зможе використовувати для автоматичного вивантаження ресурсів Live update під час пакування гри, а також як налаштувати Amazon S3, щоб клієнти гри могли отримувати ресурси. Докладніше про налаштування Amazon S3 див. у [документації Amazon S3](http://docs.aws.amazon.com/AmazonS3/latest/dev/Welcome.html).

1. Створіть бакет (bucket) для ресурсів Live update

    Відкрийте меню `Services` і виберіть `S3` у категорії _Storage_ ([консоль Amazon S3](https://console.aws.amazon.com/s3)). Ви побачите всі наявні бакети та можливість створити новий. Хоча можна використовувати наявний бакет, радимо створити новий для ресурсів Live update, щоб було легко обмежити доступ.

    ![Створення бакета](images/live-update/01-create-bucket.png)

2. Додайте політику бакета

    Виберіть бакет, який хочете використовувати, відкрийте панель *Properties* і розгорніть у ній пункт *Permissions*. Відкрийте політику бакета, натиснувши кнопку *Add bucket policy*. Політика бакета в цьому прикладі дозволить анонімному користувачеві отримувати файли з бакета, завдяки чому клієнт гри зможе завантажувати потрібні грі ресурси Live update. Докладніше про політики бакетів див. у [документації Amazon](https://docs.aws.amazon.com/AmazonS3/latest/dev/using-iam-policies.html).

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

    ![Політика бакета](images/live-update/02-bucket-policy.png)

3. Додайте конфігурацію CORS до бакета (необов’язково)

    [Спільне використання ресурсів між джерелами (Cross-Origin Resource Sharing, CORS)](https://en.wikipedia.org/wiki/Cross-origin_resource_sharing) — це механізм, який дає вебсайту змогу отримувати ресурс з іншого домену за допомогою JavaScript. Якщо ви плануєте опублікувати гру як клієнт HTML5, потрібно додати конфігурацію CORS до бакета.

    Виберіть бакет, який хочете використовувати, відкрийте панель *Properties* і розгорніть у ній пункт *Permissions*. Відкрийте політику бакета, натиснувши кнопку *Add CORS Configuration*. Конфігурація в цьому прикладі дозволить доступ із будь-якого вебсайту завдяки символу підстановки в домені, хоча ви можете додатково обмежити доступ, якщо знаєте, на яких доменах буде доступна ваша гра. Докладніше про конфігурацію CORS в Amazon див. у [документації Amazon](https://docs.aws.amazon.com/AmazonS3/latest/dev/cors.html).

    ```xml
    <?xml version="1.0" encoding="UTF-8"?>
    <CORSConfiguration xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
        <CORSRule>
            <AllowedOrigin>*</AllowedOrigin>
            <AllowedMethod>GET</AllowedMethod>
        </CORSRule>
    </CORSConfiguration>
    ```

    ![Конфігурація CORS](images/live-update/03-cors-configuration.png)

4. Створіть політику IAM

    Відкрийте меню *Services* і виберіть *IAM* у категорії _Security, Identity & Compliance_ ([консоль Amazon IAM](https://console.aws.amazon.com/iam)). Виберіть *Policies* у меню ліворуч, і ви побачите всі наявні політики та можливість створити нову.

    Натисніть кнопку *Create Policy*, а потім виберіть _Create Your Own Policy_. Політика в цьому прикладі дозволить користувачеві переглядати список усіх бакетів, що потрібно лише під час налаштування Live update у проєкті Defold. Вона також дозволить користувачеві отримувати список контролю доступу (ACL) і вивантажувати ресурси до конкретного бакета, призначеного для ресурсів Live update. Докладніше про Amazon Identity and Access Management (IAM) див. у [документації Amazon](http://docs.aws.amazon.com/IAM/latest/UserGuide/access.html).

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

    ![Політика IAM](images/live-update/04-create-policy.png)

5. Створіть користувача для програмного доступу

    Відкрийте меню *Services* і виберіть *IAM* у категорії _Security, Identity & Compliance_ ([консоль Amazon IAM](https://console.aws.amazon.com/iam)). Виберіть *Users* у меню ліворуч, і ви побачите всіх наявних користувачів та можливість додати нового. Хоча можна використовувати наявного користувача, радимо додати нового для ресурсів Live update, щоб було легко обмежити доступ.

    Натисніть кнопку *Add User*, вкажіть ім’я користувача й виберіть *Programmatic access* як *Access type*, а потім натисніть *Next: Permissions*. Виберіть *Attach existing policies directly* і політику, створену на кроці 4.

    Після завершення процесу ви отримаєте *Access key ID* і *Secret access key*.

    ::: important
    *Дуже важливо* зберегти ці ключі, оскільки ви не зможете отримати їх від Amazon після того, як залишите сторінку.
    :::

6. Створіть файл профілю облікових даних

    На цьому етапі ви вже мали створити бакет, налаштувати його політику, додати конфігурацію CORS, створити політику користувача й нового користувача. Залишилося лише створити [файл профілю облікових даних](https://aws.amazon.com/blogs/security/a-new-and-standardized-way-to-manage-credentials-in-the-aws-sdks), щоб редактор Defold міг отримувати доступ до бакета від вашого імені.

    Створіть новий каталог *.aws* у домашній теці, а в ньому — файл із назвою *credentials*.

    ```bash
    $ mkdir ~/.aws
    $ touch ~/.aws/credentials
    ```

    Файл *~/.aws/credentials* міститиме ваші облікові дані для програмного доступу до Amazon Web Services; це стандартний спосіб керування обліковими даними AWS. Відкрийте файл у текстовому редакторі й введіть свої *Access key ID* та *Secret access key* у наведеному нижче форматі.

    ```ini
    [defold-liveupdate-example]
    aws_access_key_id = <Access key ID>
    aws_secret_access_key = <Secret access key>
    ```

    Ідентифікатор у квадратних дужках, у цьому прикладі _defold-liveupdate-example_, — це той самий ідентифікатор, який потрібно вказати в налаштуваннях Live update вашого проєкту в редакторі Defold.

    ![Налаштування Live update](images/live-update/05-liveupdate-settings.png)
