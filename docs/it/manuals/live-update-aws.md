---
title: Caricamento di contenuti Live update su AWS
brief: Questa sezione spiega come creare su Amazon Web Services un nuovo utente con accesso limitato da usare con l'editor Defold per caricare automaticamente le risorse Live update quando crei il bundle del gioco.
---

# Configurazione di Amazon Web Service {#setting-up-amazon-web-service}

Per usare la funzionalità Live update di Defold con i servizi Amazon, ti serve un account Amazon Web Services. Se non hai già un account, puoi crearne uno qui https://aws.amazon.com/.

Questa sezione spiega come creare su Amazon Web Services un nuovo utente con accesso limitato da usare con l'editor Defold per caricare automaticamente le risorse Live update quando crei il bundle del gioco, e come configurare Amazon S3 per consentire ai client del gioco di recuperare le risorse. Per ulteriori informazioni sulla configurazione di Amazon S3, consulta la [documentazione di Amazon S3](http://docs.aws.amazon.com/AmazonS3/latest/dev/Welcome.html).

1. Crea un bucket per le risorse Live update

    Apri il menu `Services` e seleziona `S3`, nella categoria _Storage_ ([console Amazon S3](https://console.aws.amazon.com/s3)). Vedrai tutti i bucket esistenti e l'opzione per crearne uno nuovo. Anche se puoi usare un bucket esistente, consigliamo di crearne uno nuovo per le risorse Live update, così da poterne limitare facilmente l'accesso.

    ![Creazione di un bucket](images/live-update/01-create-bucket.png)

2. Aggiungi una policy al bucket

    Seleziona il bucket che vuoi usare, apri il pannello *Properties* ed espandi l'opzione *Permissions* al suo interno. Apri la policy del bucket facendo clic sul pulsante *Add bucket policy*. La policy del bucket in questo esempio consente a un utente anonimo di recuperare file dal bucket, permettendo così a un client del gioco di scaricare le risorse Live update necessarie al gioco. Per ulteriori informazioni sulle policy dei bucket, consulta [la documentazione di Amazon](https://docs.aws.amazon.com/AmazonS3/latest/dev/using-iam-policies.html).

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

    ![Policy del bucket](images/live-update/02-bucket-policy.png)

3. Aggiungi una configurazione CORS al bucket (facoltativo)

    La [condivisione delle risorse tra origini diverse (Cross-Origin Resource Sharing, CORS)](https://en.wikipedia.org/wiki/Cross-origin_resource_sharing) è un meccanismo che consente a un sito web di recuperare una risorsa da un dominio diverso tramite JavaScript. Se intendi pubblicare il gioco come client HTML5, devi aggiungere una configurazione CORS al bucket.

    Seleziona il bucket che vuoi usare, apri il pannello *Properties* ed espandi l'opzione *Permissions* al suo interno. Apri la policy del bucket facendo clic sul pulsante *Add CORS Configuration*. La configurazione di questo esempio consente l'accesso da qualsiasi sito web specificando un dominio con carattere jolly, ma puoi limitare ulteriormente l'accesso se sai su quali domini renderai disponibile il gioco. Per ulteriori informazioni sulla configurazione CORS di Amazon, consulta [la documentazione di Amazon](https://docs.aws.amazon.com/AmazonS3/latest/dev/cors.html).

    ```xml
    <?xml version="1.0" encoding="UTF-8"?>
    <CORSConfiguration xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
        <CORSRule>
            <AllowedOrigin>*</AllowedOrigin>
            <AllowedMethod>GET</AllowedMethod>
        </CORSRule>
    </CORSConfiguration>
    ```

    ![Configurazione CORS](images/live-update/03-cors-configuration.png)

4. Crea una policy IAM

    Apri il menu *Services* e seleziona *IAM*, nella categoria _Security, Identity & Compliance_ ([console Amazon IAM](https://console.aws.amazon.com/iam)). Seleziona *Policies* nel menu a sinistra: vedrai tutte le policy esistenti e l'opzione per crearne una nuova.

    Fai clic sul pulsante *Create Policy*, quindi scegli _Create Your Own Policy_. La policy di questo esempio consente a un utente di elencare tutti i bucket, un'autorizzazione necessaria solo quando si configura un progetto Defold per Live update. Consente inoltre all'utente di ottenere la lista di controllo degli accessi (Access Control List, ACL) e caricare risorse nel bucket specifico usato per le risorse Live update. Per ulteriori informazioni su Amazon Identity and Access Management (IAM), consulta [la documentazione di Amazon](http://docs.aws.amazon.com/IAM/latest/UserGuide/access.html).

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

    ![Policy IAM](images/live-update/04-create-policy.png)

5. Crea un utente per l'accesso programmatico

    Apri il menu *Services* e seleziona *IAM*, nella categoria _Security, Identity & Compliance_ ([console Amazon IAM](https://console.aws.amazon.com/iam)). Seleziona *Users* nel menu a sinistra: vedrai tutti gli utenti esistenti e l'opzione per aggiungerne uno nuovo. Anche se puoi usare un utente esistente, consigliamo di aggiungerne uno nuovo per le risorse Live update, così da poterne limitare facilmente l'accesso.

    Fai clic sul pulsante *Add User*, inserisci un nome utente e scegli *Programmatic access* come *Access type*, quindi premi *Next: Permissions*. Seleziona *Attach existing policies directly* e scegli la policy creata al punto 4.

    Una volta completata la procedura, riceverai un *Access key ID* e una *Secret access key*.

    ::: important
    È *molto importante* conservare queste chiavi, perché non potrai recuperarle da Amazon dopo aver lasciato la pagina.
    :::

6. Crea un file di profilo delle credenziali

    A questo punto dovresti aver creato un bucket, configurato una policy del bucket, aggiunto una configurazione CORS, creato una policy utente e creato un nuovo utente. Non resta che creare un [file di profilo delle credenziali](https://aws.amazon.com/blogs/security/a-new-and-standardized-way-to-manage-credentials-in-the-aws-sdks) per consentire all'editor Defold di accedere al bucket per tuo conto.

    Crea una nuova directory *.aws* nella tua cartella home e, al suo interno, crea un file chiamato *credentials*.

    ```bash
    $ mkdir ~/.aws
    $ touch ~/.aws/credentials
    ```

    Il file *~/.aws/credentials* conterrà le credenziali per l'accesso programmatico ad Amazon Web Services e rappresenta un modo standardizzato di gestire le credenziali AWS. Apri il file in un editor di testo e inserisci il tuo *Access key ID* e la tua *Secret access key* nel formato mostrato di seguito.

    ```ini
    [defold-liveupdate-example]
    aws_access_key_id = <Access key ID>
    aws_secret_access_key = <Secret access key>
    ```

    L'identificatore specificato tra parentesi quadre, in questo esempio _defold-liveupdate-example_, è lo stesso che devi fornire quando configuri le impostazioni Live update del progetto nell'editor Defold.

    ![Impostazioni Live update](images/live-update/05-liveupdate-settings.png)
