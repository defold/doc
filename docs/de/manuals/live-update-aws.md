---
title: Inhalte für Live Update auf AWS hochladen
brief: Dieser Abschnitt erklärt, wie du bei Amazon Web Services einen neuen Benutzer mit eingeschränktem Zugriff erstellst, mit dem der Defold-Editor beim Erstellen eines Bundles für dein Spiel automatisch Ressourcen für Live Update hochladen kann.
---

# Amazon Web Services einrichten {#setting-up-amazon-web-service}

Um die Funktion Live Update von Defold zusammen mit den Diensten von Amazon zu verwenden, benötigst du ein Konto bei Amazon Web Services. Falls du noch kein Konto hast, kannst du hier eines erstellen: https://aws.amazon.com/.

Dieser Abschnitt erklärt, wie du bei Amazon Web Services einen neuen Benutzer mit eingeschränktem Zugriff erstellst, mit dem der Defold-Editor beim Erstellen eines Bundles für dein Spiel automatisch Ressourcen für Live Update hochladen kann. Außerdem erfährst du, wie du Amazon S3 so konfigurierst, dass Spielclients Ressourcen abrufen können. Weitere Informationen zur Konfiguration von Amazon S3 findest du in der [Dokumentation zu Amazon S3](http://docs.aws.amazon.com/AmazonS3/latest/dev/Welcome.html).

1. Einen Bucket für Ressourcen für Live Update erstellen

    Öffne das Menü `Services` und wähle `S3` in der Kategorie _Storage_ ([Amazon S3-Konsole](https://console.aws.amazon.com/s3)). Du siehst alle vorhandenen Buckets sowie die Möglichkeit, einen neuen Bucket zu erstellen. Du kannst zwar einen vorhandenen Bucket verwenden, wir empfehlen jedoch, einen neuen Bucket für Ressourcen für Live Update zu erstellen, damit du den Zugriff leicht einschränken kannst.

    ![Einen Bucket erstellen](images/live-update/01-create-bucket.png)

2. Deinem Bucket eine Bucket-Richtlinie hinzufügen

    Wähle den Bucket aus, den du verwenden möchtest, öffne den Bereich *Properties* und klappe darin die Option *Permissions* auf. Öffne die Bucket-Richtlinie, indem du auf die Schaltfläche *Add bucket policy* klickst. Die Bucket-Richtlinie in diesem Beispiel erlaubt einem anonymen Benutzer, Dateien aus dem Bucket abzurufen. Dadurch kann ein Spielclient die Ressourcen für Live Update herunterladen, die das Spiel benötigt. Weitere Informationen zu Bucket-Richtlinien findest du in der [Dokumentation von Amazon](https://docs.aws.amazon.com/AmazonS3/latest/dev/using-iam-policies.html).

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

    ![Bucket-Richtlinie](images/live-update/02-bucket-policy.png)

3. Deinem Bucket eine CORS-Konfiguration hinzufügen (optional)

    [Ursprungsübergreifende Ressourcenfreigabe (Cross-Origin Resource Sharing, CORS)](https://en.wikipedia.org/wiki/Cross-origin_resource_sharing) ist ein Mechanismus, mit dem eine Website mithilfe von JavaScript eine Ressource von einer anderen Domain abrufen kann. Wenn du dein Spiel als HTML5-Client veröffentlichen möchtest, musst du deinem Bucket eine CORS-Konfiguration hinzufügen.

    Wähle den Bucket aus, den du verwenden möchtest, öffne den Bereich *Properties* und klappe darin die Option *Permissions* auf. Öffne die Bucket-Richtlinie, indem du auf die Schaltfläche *Add CORS Configuration* klickst. Die Konfiguration in diesem Beispiel erlaubt durch die Angabe eines Platzhalters für die Domain den Zugriff von jeder Website. Du kannst diesen Zugriff jedoch weiter einschränken, wenn du weißt, auf welchen Domains du dein Spiel bereitstellen wirst. Weitere Informationen zur CORS-Konfiguration bei Amazon findest du in der [Dokumentation von Amazon](https://docs.aws.amazon.com/AmazonS3/latest/dev/cors.html).

    ```xml
    <?xml version="1.0" encoding="UTF-8"?>
    <CORSConfiguration xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
        <CORSRule>
            <AllowedOrigin>*</AllowedOrigin>
            <AllowedMethod>GET</AllowedMethod>
        </CORSRule>
    </CORSConfiguration>
    ```

    ![CORS-Konfiguration](images/live-update/03-cors-configuration.png)

4. Eine IAM-Richtlinie erstellen

    Öffne das Menü *Services* und wähle *IAM* in der Kategorie _Security, Identity & Compliance_ ([Amazon IAM-Konsole](https://console.aws.amazon.com/iam)). Wähle im Menü links *Policies* aus. Du siehst alle vorhandenen Richtlinien sowie die Möglichkeit, eine neue Richtlinie zu erstellen.

    Klicke auf die Schaltfläche *Create Policy* und wähle anschließend _Create Your Own Policy_. Die Richtlinie in diesem Beispiel erlaubt einem Benutzer, alle Buckets aufzulisten. Das ist nur erforderlich, wenn du ein Defold-Projekt für Live Update konfigurierst. Außerdem erlaubt sie dem Benutzer, die Zugriffssteuerungsliste (Access Control List, ACL) des für Ressourcen für Live Update verwendeten Buckets abzurufen und Ressourcen in diesen Bucket hochzuladen. Weitere Informationen zu Amazon Identity and Access Management (IAM) findest du in der [Dokumentation von Amazon](http://docs.aws.amazon.com/IAM/latest/UserGuide/access.html).

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

    ![IAM-Richtlinie](images/live-update/04-create-policy.png)

5. Einen Benutzer für den programmgesteuerten Zugriff erstellen

    Öffne das Menü *Services* und wähle *IAM* in der Kategorie _Security, Identity & Compliance_ ([Amazon IAM-Konsole](https://console.aws.amazon.com/iam)). Wähle im Menü links *Users* aus. Du siehst alle vorhandenen Benutzer sowie die Möglichkeit, einen neuen Benutzer hinzuzufügen. Du kannst zwar einen vorhandenen Benutzer verwenden, wir empfehlen jedoch, einen neuen Benutzer für Ressourcen für Live Update hinzuzufügen, damit du den Zugriff leicht einschränken kannst.

    Klicke auf die Schaltfläche *Add User*, gib einen Benutzernamen ein und wähle *Programmatic access* als *Access type*. Klicke dann auf *Next: Permissions*. Wähle *Attach existing policies directly* und anschließend die Richtlinie aus, die du in Schritt 4 erstellt hast.

    Wenn du den Vorgang abgeschlossen hast, erhältst du eine *Access key ID* und einen *Secret access key*.

    ::: important
    Es ist *sehr wichtig*, dass du diese Schlüssel speicherst, da du sie nicht mehr bei Amazon abrufen kannst, nachdem du die Seite verlassen hast.
    :::

6. Eine Profildatei mit Zugangsdaten erstellen

    Zu diesem Zeitpunkt solltest du einen Bucket erstellt, eine Bucket-Richtlinie konfiguriert, eine CORS-Konfiguration hinzugefügt, eine Benutzerrichtlinie erstellt und einen neuen Benutzer angelegt haben. Jetzt musst du nur noch eine [Profildatei mit Zugangsdaten](https://aws.amazon.com/blogs/security/a-new-and-standardized-way-to-manage-credentials-in-the-aws-sdks) erstellen, damit der Defold-Editor in deinem Namen auf den Bucket zugreifen kann.

    Erstelle in deinem persönlichen Ordner ein neues Verzeichnis namens *.aws* und darin eine Datei namens *credentials*.

    ```bash
    $ mkdir ~/.aws
    $ touch ~/.aws/credentials
    ```

    Die Datei *~/.aws/credentials* enthält deine Zugangsdaten für den programmgesteuerten Zugriff auf Amazon Web Services und ist eine standardisierte Möglichkeit, AWS-Zugangsdaten zu verwalten. Öffne die Datei in einem Texteditor und trage deine *Access key ID* und deinen *Secret access key* im unten gezeigten Format ein.

    ```ini
    [defold-liveupdate-example]
    aws_access_key_id = <Access key ID>
    aws_secret_access_key = <Secret access key>
    ```

    Die Kennung in den eckigen Klammern, in diesem Beispiel _defold-liveupdate-example_, ist dieselbe Kennung, die du beim Konfigurieren der Einstellungen für Live Update deines Projekts im Defold-Editor angeben solltest.

    ![Einstellungen für Live Update](images/live-update/05-liveupdate-settings.png)
