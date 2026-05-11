---
title: Uploads de conteúdo Live Update para AWS
brief: Esta seção explicará como criar um novo usuário com acesso limitado no Amazon Web Services, que pode ser usado junto com o editor Defold para fazer upload automático de recursos Live Update ao empacotar seu jogo.
---

# Configurando Amazon Web Service

Para usar o recurso Live Update do Defold junto com serviços Amazon, você precisa de uma conta Amazon Web Services. Se ainda não tiver uma conta, você pode criar uma aqui: https://aws.amazon.com/.

Esta seção explicará como criar um novo usuário com acesso limitado no Amazon Web Services, que pode ser usado junto com o editor Defold para fazer upload automático de recursos Live Update ao empacotar seu jogo, bem como como configurar o Amazon S3 para permitir que clientes do jogo recuperem recursos. Para informações adicionais sobre como configurar o Amazon S3, consulte a [documentação do Amazon S3](http://docs.aws.amazon.com/AmazonS3/latest/dev/Welcome.html).

1. Crie um bucket para recursos Live Update

    Abra o menu `Services` e selecione `S3`, localizado na categoria _Storage_ ([Console Amazon S3](https://console.aws.amazon.com/s3)). Você verá todos os seus buckets existentes junto com a opção de criar um novo bucket. Embora seja possível usar um bucket existente, recomendamos criar um novo bucket para recursos Live Update, para que você possa restringir o acesso facilmente.

    ![Create a bucket](images/live-update/01-create-bucket.png)

2. Adicione uma política de bucket ao seu bucket

    Selecione o bucket que deseja usar, abra o painel *Properties* e expanda a opção *Permissions* dentro do painel. Abra a política de bucket clicando no botão *Add bucket policy*. A política de bucket neste exemplo permitirá que um usuário anônimo recupere arquivos do bucket, o que permitirá que um cliente do jogo baixe os recursos Live Update exigidos pelo jogo. Para informações adicionais sobre políticas de bucket, consulte [a documentação da Amazon](https://docs.aws.amazon.com/AmazonS3/latest/dev/using-iam-policies.html).

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

3. Adicione uma configuração CORS ao seu bucket (opcional)

    [Cross-Origin Resource Sharing (CORS)](https://en.wikipedia.org/wiki/Cross-origin_resource_sharing) é um mecanismo que permite que um site recupere um recurso de um domínio diferente usando JavaScript. Se você pretende publicar seu jogo como um cliente HTML5, precisará adicionar uma configuração CORS ao seu bucket.

    Selecione o bucket que deseja usar, abra o painel *Properties* e expanda a opção *Permissions* dentro do painel. Abra a política de bucket clicando no botão *Add CORS Configuration*. A configuração neste exemplo permitirá acesso de qualquer site especificando um domínio curinga, embora seja possível restringir esse acesso ainda mais se você souber em quais domínios disponibilizará seu jogo. Para informações adicionais sobre a configuração CORS da Amazon, consulte [a documentação da Amazon](https://docs.aws.amazon.com/AmazonS3/latest/dev/cors.html).

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

4. Crie uma política IAM

    Abra o menu *Services* e selecione *IAM*, localizado na categoria _Security, Identity & Compliance_ ([Console Amazon IAM](https://console.aws.amazon.com/iam)). Selecione *Policies* no menu à esquerda e você verá todas as suas políticas existentes junto com a opção de criar uma nova política.

    Clique no botão *Create Policy* e então escolha _Create Your Own Policy_. A política neste exemplo permitirá que um usuário liste todos os buckets, o que é necessário apenas ao configurar um projeto Defold para Live Update. Ela também permitirá que o usuário obtenha a Access Control List (ACL) e faça upload de recursos para o bucket específico usado para recursos Live Update. Para informações adicionais sobre Amazon Identity and Access Management (IAM), consulte [a documentação da Amazon](http://docs.aws.amazon.com/IAM/latest/UserGuide/access.html).

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

5. Crie um usuário para acesso programático

    Abra o menu *Services* e selecione *IAM*, localizado na categoria _Security, Identity & Compliance_ ([Console Amazon IAM](https://console.aws.amazon.com/iam)). Selecione *Users* no menu à esquerda e você verá todos os seus usuários existentes junto com a opção de adicionar um novo usuário. Embora seja possível usar um usuário existente, recomendamos adicionar um novo usuário para recursos Live Update, para que você possa restringir o acesso facilmente.

    Clique no botão *Add User*, forneça um nome de usuário e escolha *Programmatic access* como *Access type*, então pressione *Next: Permissions*. Selecione *Attach existing policies directly* e escolha a política que você criou na etapa 4.

    Quando você concluir o processo, receberá um *Access key ID* e uma *Secret access key*.

    ::: important
    É *muito importante* que você armazene essas chaves, pois não será possível recuperá-las da Amazon depois de sair da página.
    :::

6. Crie um arquivo de perfil de credenciais

    Neste ponto, você deve ter criado um bucket, configurado uma política de bucket, adicionado uma configuração CORS, criado uma política de usuário e criado um novo usuário. A única coisa que resta é criar um [arquivo de perfil de credenciais](https://aws.amazon.com/blogs/security/a-new-and-standardized-way-to-manage-credentials-in-the-aws-sdks) para que o editor Defold possa acessar o bucket em seu nome.

    Crie um novo diretório *.aws* na sua pasta home e crie um arquivo chamado *credentials* dentro do novo diretório.

    ```bash
    $ mkdir ~/.aws
    $ touch ~/.aws/credentials
    ```

    O arquivo *~/.aws/credentials* conterá suas credenciais para acessar Amazon Web Services por meio de acesso programático e é uma forma padronizada de gerenciar credenciais AWS. Abra o arquivo em um editor de texto e insira seu *Access key ID* e sua *Secret access key* no formato mostrado abaixo.

    ```ini
    [defold-liveupdate-example]
    aws_access_key_id = <Access key ID>
    aws_secret_access_key = <Secret access key>
    ```

    O identificador especificado entre colchetes, neste exemplo _defold-liveupdate-example_, é o mesmo identificador que você deve fornecer ao configurar as definições de Live Update do seu projeto no editor Defold.

    ![Live update settings](images/live-update/05-liveupdate-settings.png)
