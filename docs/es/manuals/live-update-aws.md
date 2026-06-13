---
title: Cargas de contenido de Live update a AWS
brief: Esta sección explicará cómo crear un usuario nuevo con acceso limitado en Amazon Web Services que se puede usar junto con el editor Defold para cargar automáticamente recursos de Live update cuando creas el bundle de tu juego.
---

# Configuración de Amazon Web Services

Para usar la funcionalidad Live update de Defold junto con los servicios de Amazon necesitas una cuenta de Amazon Web Services. Si todavía no tienes una cuenta, puedes crear una aquí https://aws.amazon.com/.

Esta sección explicará cómo crear un usuario nuevo con acceso limitado en Amazon Web Services que se puede usar junto con el editor Defold para cargar automáticamente recursos de Live update cuando creas el bundle de tu juego, así como cómo configurar Amazon S3 para permitir que los clientes del juego recuperen recursos. Para más información sobre cómo puedes configurar Amazon S3, consulta la [documentación de Amazon S3](http://docs.aws.amazon.com/AmazonS3/latest/dev/Welcome.html).

1. Crea un bucket para los recursos de Live update

    Abre el menú `Services` y selecciona `S3`, que se encuentra bajo la categoría _Storage_ ([Amazon S3 Console](https://console.aws.amazon.com/s3)). Verás todos tus buckets existentes junto con la opción para crear un bucket nuevo. Aunque es posible usar un bucket existente, recomendamos que crees un bucket nuevo para los recursos de Live update para que puedas restringir el acceso fácilmente.

    ![Crear un bucket](images/live-update/01-create-bucket.png)

2. Agrega una política del bucket a tu bucket

    Selecciona el bucket que quieres usar, abre el panel *Properties* y expande la opción *Permissions* dentro del panel. Abre la política del bucket haciendo click en el botón *Add bucket policy*. La política del bucket de este ejemplo permitirá que un usuario anónimo recupere archivos del bucket, lo que permitirá que un cliente del juego descargue los recursos de Live update que requiere el juego. Para más información sobre las políticas de buckets, consulta [la documentación de Amazon](https://docs.aws.amazon.com/AmazonS3/latest/dev/using-iam-policies.html).

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

    ![Política del bucket](images/live-update/02-bucket-policy.png)

3. Agrega una configuración CORS a tu bucket (opcional)

    [Cross-Origin Resource Sharing (CORS)](https://en.wikipedia.org/wiki/Cross-origin_resource_sharing) es un mecanismo que permite que un sitio web recupere un recurso de un dominio diferente usando JavaScript. Si tienes pensado publicar tu juego como cliente HTML5, necesitarás agregar una configuración CORS a tu bucket.

    Selecciona el bucket que quieres usar, abre el panel *Properties* y expande la opción *Permissions* dentro del panel. Abre la política del bucket haciendo click en el botón *Add CORS Configuration*. La configuración de este ejemplo permitirá el acceso desde cualquier sitio web mediante la especificación de un dominio comodín, aunque es posible restringir más este acceso si sabes en qué dominios harás disponible tu juego. Para más información sobre la configuración CORS de Amazon, consulta [la documentación de Amazon](https://docs.aws.amazon.com/AmazonS3/latest/dev/cors.html).

    ```xml
    <?xml version="1.0" encoding="UTF-8"?>
    <CORSConfiguration xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
        <CORSRule>
            <AllowedOrigin>*</AllowedOrigin>
            <AllowedMethod>GET</AllowedMethod>
        </CORSRule>
    </CORSConfiguration>
    ```

    ![Configuración CORS](images/live-update/03-cors-configuration.png)

4. Crea una política IAM

    Abre el menú *Services* y selecciona *IAM*, que se encuentra bajo la categoría _Security, Identity & Compliance_ ([Amazon IAM Console](https://console.aws.amazon.com/iam)). Selecciona *Policies* en el menú de la izquierda y verás todas tus políticas existentes junto con la opción para crear una política nueva.

    Haz click en el botón *Create Policy* y luego elige _Create Your Own Policy_. La política de este ejemplo permitirá que un usuario liste todos los buckets, lo que solo se requiere al configurar un proyecto Defold para Live update. También permitirá que el usuario obtenga la Access Control List (ACL) y cargue recursos al bucket específico usado para los recursos de Live update. Para más información sobre Amazon Identity and Access Management (IAM), consulta [la documentación de Amazon](http://docs.aws.amazon.com/IAM/latest/UserGuide/access.html).

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

    ![Política IAM](images/live-update/04-create-policy.png)

5. Crea un usuario para acceso programático

    Abre el menú *Services* y selecciona *IAM*, que se encuentra bajo la categoría _Security, Identity & Compliance_ ([Amazon IAM Console](https://console.aws.amazon.com/iam)). Selecciona *Users* en el menú de la izquierda y verás todos tus usuarios existentes junto con la opción para agregar un usuario nuevo. Aunque es posible usar un usuario existente, recomendamos que agregues un usuario nuevo para los recursos de Live update para que puedas restringir el acceso fácilmente.

    Haz click en el botón *Add User*, proporciona un nombre de usuario y elige *Programmatic access* como *Access type*, luego presiona *Next: Permissions*. Selecciona *Attach existing policies directly* y elige la política que creaste en el paso 4.

    Cuando hayas completado el proceso, recibirás un *Access key ID* y una *Secret access key*.

    ::: important
    Es *muy importante* que almacenes esas claves, ya que no podrás recuperarlas de Amazon después de salir de la página.
    :::

6. Crea un archivo de perfil de credenciales

    En este punto deberías haber creado un bucket, configurado una política del bucket, agregado una configuración CORS, creado una política de usuario y creado un usuario nuevo. Lo único que queda es crear un [archivo de perfil de credenciales](https://aws.amazon.com/blogs/security/a-new-and-standardized-way-to-manage-credentials-in-the-aws-sdks) para que el editor Defold pueda acceder al bucket en tu nombre.

    Crea un directorio nuevo llamado *.aws* en tu carpeta de inicio y crea un archivo llamado *credentials* dentro del directorio nuevo.

    ```bash
    $ mkdir ~/.aws
    $ touch ~/.aws/credentials
    ```

    El archivo *~/.aws/credentials* contendrá tus credenciales para acceder a Amazon Web Services mediante acceso programático y es una forma estandarizada de administrar credenciales de AWS. Abre el archivo en un editor de texto e ingresa tu *Access key ID* y tu *Secret access key* en el formato que se muestra a continuación.

    ```ini
    [defold-liveupdate-example]
    aws_access_key_id = <Access key ID>
    aws_secret_access_key = <Secret access key>
    ```

    El identificador especificado entre corchetes, en este ejemplo _defold-liveupdate-example_, es el mismo identificador que deberías proporcionar al configurar los ajustes de Live update de tu proyecto en el editor Defold.

    ![Configuración de Live update](images/live-update/05-liveupdate-settings.png)
