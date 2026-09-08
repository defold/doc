---
title: Téléversement du contenu Live Update vers AWS
brief: Cette section explique comment créer sur Amazon Web Services un nouvel utilisateur disposant d'un accès limité, que l'éditeur Defold pourra utiliser pour téléverser automatiquement les ressources Live Update lorsque vous créez un bundle de votre jeu.
---

# Configurer Amazon Web Service {#setting-up-amazon-web-service}

Pour utiliser la fonctionnalité Live Update de Defold avec les services Amazon, vous avez besoin d'un compte Amazon Web Services. Si vous n'avez pas encore de compte, vous pouvez en créer un ici https://aws.amazon.com/.

Cette section explique comment créer sur Amazon Web Services un nouvel utilisateur disposant d'un accès limité, que l'éditeur Defold pourra utiliser pour téléverser automatiquement les ressources Live Update lorsque vous créez un bundle de votre jeu, ainsi que comment configurer Amazon S3 pour permettre aux clients du jeu de récupérer les ressources. Pour plus d'informations sur la configuration d'Amazon S3, consultez la [documentation d'Amazon S3](http://docs.aws.amazon.com/AmazonS3/latest/dev/Welcome.html).

1. Créer un compartiment pour les ressources Live Update

    Ouvrez le menu `Services` et sélectionnez `S3`, qui se trouve dans la catégorie _Storage_ ([console Amazon S3](https://console.aws.amazon.com/s3)). Vous verrez tous vos compartiments existants ainsi qu'une option pour créer un nouveau compartiment. Bien qu'il soit possible d'utiliser un compartiment existant, nous vous recommandons d'en créer un nouveau pour les ressources Live Update afin de pouvoir facilement en restreindre l'accès.

    ![Créer un compartiment](images/live-update/01-create-bucket.png)

2. Ajouter une stratégie de compartiment à votre compartiment

    Sélectionnez le compartiment que vous souhaitez utiliser, ouvrez le panneau *Properties* et développez l'option *Permissions* dans ce panneau. Ouvrez la stratégie de compartiment en cliquant sur le bouton *Add bucket policy*. La stratégie de compartiment de cet exemple permettra à un utilisateur anonyme de récupérer des fichiers du compartiment, ce qui permettra à un client du jeu de télécharger les ressources Live Update nécessaires au jeu. Pour plus d'informations sur les stratégies de compartiment, consultez [la documentation d'Amazon](https://docs.aws.amazon.com/AmazonS3/latest/dev/using-iam-policies.html).

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

    ![Stratégie de compartiment](images/live-update/02-bucket-policy.png)

3. Ajouter une configuration CORS à votre compartiment (facultatif)

    Le [partage de ressources entre origines (CORS)](https://en.wikipedia.org/wiki/Cross-origin_resource_sharing) est un mécanisme qui permet à un site web de récupérer une ressource depuis un autre domaine à l'aide de JavaScript. Si vous comptez publier votre jeu sous forme de client HTML5, vous devrez ajouter une configuration CORS à votre compartiment.

    Sélectionnez le compartiment que vous souhaitez utiliser, ouvrez le panneau *Properties* et développez l'option *Permissions* dans ce panneau. Ouvrez la stratégie de compartiment en cliquant sur le bouton *Add CORS Configuration*. La configuration de cet exemple permettra l'accès depuis n'importe quel site web en spécifiant un domaine générique, mais il est possible de restreindre davantage cet accès si vous savez sur quels domaines vous mettrez votre jeu à disposition. Pour plus d'informations sur la configuration CORS d'Amazon, consultez [la documentation d'Amazon](https://docs.aws.amazon.com/AmazonS3/latest/dev/cors.html).

    ```xml
    <?xml version="1.0" encoding="UTF-8"?>
    <CORSConfiguration xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
        <CORSRule>
            <AllowedOrigin>*</AllowedOrigin>
            <AllowedMethod>GET</AllowedMethod>
        </CORSRule>
    </CORSConfiguration>
    ```

    ![Configuration CORS](images/live-update/03-cors-configuration.png)

4. Créer une stratégie IAM

    Ouvrez le menu *Services* et sélectionnez *IAM*, qui se trouve dans la catégorie _Security, Identity & Compliance_ ([console Amazon IAM](https://console.aws.amazon.com/iam)). Sélectionnez *Policies* dans le menu de gauche : vous verrez toutes vos stratégies existantes ainsi qu'une option pour créer une nouvelle stratégie.

    Cliquez sur le bouton *Create Policy*, puis choisissez _Create Your Own Policy_. La stratégie de cet exemple permettra à un utilisateur de lister tous les compartiments, ce qui n'est nécessaire que lors de la configuration d'un projet Defold pour Live Update. Elle permettra également à l'utilisateur de récupérer la liste de contrôle d'accès (ACL) et de téléverser des ressources dans le compartiment spécifique utilisé pour les ressources Live Update. Pour plus d'informations sur Amazon Identity and Access Management (IAM), consultez [la documentation d'Amazon](http://docs.aws.amazon.com/IAM/latest/UserGuide/access.html).

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

    ![Stratégie IAM](images/live-update/04-create-policy.png)

5. Créer un utilisateur pour l'accès programmatique

    Ouvrez le menu *Services* et sélectionnez *IAM*, qui se trouve dans la catégorie _Security, Identity & Compliance_ ([console Amazon IAM](https://console.aws.amazon.com/iam)). Sélectionnez *Users* dans le menu de gauche : vous verrez tous vos utilisateurs existants ainsi qu'une option pour ajouter un nouvel utilisateur. Bien qu'il soit possible d'utiliser un utilisateur existant, nous vous recommandons d'en ajouter un nouveau pour les ressources Live Update afin de pouvoir facilement en restreindre l'accès.

    Cliquez sur le bouton *Add User*, indiquez un nom d'utilisateur et choisissez *Programmatic access* comme *Access type*, puis appuyez sur *Next: Permissions*. Sélectionnez *Attach existing policies directly* et choisissez la stratégie que vous avez créée à l'étape quatre.

    Une fois la procédure terminée, vous recevrez une valeur *Access key ID* et une valeur *Secret access key*.

    ::: important
    Il est *très important* que vous conserviez ces clés, car vous ne pourrez plus les récupérer auprès d'Amazon après avoir quitté la page.
    :::

6. Créer un fichier de profils d'identifiants

    À ce stade, vous devriez avoir créé un compartiment, configuré une stratégie de compartiment, ajouté une configuration CORS, créé une stratégie utilisateur et créé un nouvel utilisateur. Il ne vous reste plus qu'à créer un [fichier de profils d'identifiants](https://aws.amazon.com/blogs/security/a-new-and-standardized-way-to-manage-credentials-in-the-aws-sdks) pour que l'éditeur Defold puisse accéder au compartiment en votre nom.

    Créez un nouveau répertoire *.aws* dans votre dossier personnel, puis créez un fichier nommé *credentials* dans ce nouveau répertoire.

    ```bash
    $ mkdir ~/.aws
    $ touch ~/.aws/credentials
    ```

    Le fichier *~/.aws/credentials* contiendra vos identifiants pour accéder à Amazon Web Services par accès programmatique et constitue un moyen standardisé de gérer les identifiants AWS. Ouvrez ce fichier dans un éditeur de texte et saisissez vos valeurs *Access key ID* et *Secret access key* au format indiqué ci-dessous.

    ```ini
    [defold-liveupdate-example]
    aws_access_key_id = <Access key ID>
    aws_secret_access_key = <Secret access key>
    ```

    L'identifiant indiqué entre crochets, dans cet exemple _defold-liveupdate-example_, est celui que vous devez fournir lorsque vous configurez les paramètres Live Update de votre projet dans l'éditeur Defold.

    ![Paramètres de Live Update](images/live-update/05-liveupdate-settings.png)
