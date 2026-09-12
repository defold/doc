---
title: Live Update içeriğini AWS'ye yükleme
brief: Bu bölümde, oyununuzu paketlerken Live Update kaynaklarını otomatik olarak yüklemek için Defold düzenleyicisiyle birlikte kullanabileceğiniz, Amazon Web Services üzerinde sınırlı erişime sahip yeni bir kullanıcının nasıl oluşturulacağı açıklanır.
---

# Amazon Web Service kurulumu

Defold'un Live Update özelliğini Amazon hizmetleriyle birlikte kullanmak için bir Amazon Web Services hesabınızın olması gerekir. Henüz bir hesabınız yoksa buradan oluşturabilirsiniz: https://aws.amazon.com/.

Bu bölümde, oyununuzu paketlerken Live Update kaynaklarını (resources) otomatik olarak yüklemek için Defold düzenleyicisiyle birlikte kullanabileceğiniz, Amazon Web Services üzerinde sınırlı erişime sahip yeni bir kullanıcının nasıl oluşturulacağı ve oyun istemcilerinin kaynakları alabilmesi için Amazon S3'ün nasıl yapılandırılacağı açıklanır. Amazon S3'ü nasıl yapılandırabileceğiniz hakkında daha fazla bilgi için [Amazon S3 belgelerine](http://docs.aws.amazon.com/AmazonS3/latest/dev/Welcome.html) bakın.

1. Live Update kaynakları için bir kova oluşturun

    `Services` menüsünü açın ve `S3` seçeneğini seçin; bu seçenek _Storage_ kategorisinde bulunur ([Amazon S3 Konsolu](https://console.aws.amazon.com/s3)). Mevcut tüm kovalarınızı (bucket) ve yeni bir kova oluşturma seçeneğini göreceksiniz. Mevcut bir kovayı kullanmak mümkün olsa da erişimi kolayca kısıtlayabilmeniz için Live Update kaynaklarına yönelik yeni bir kova oluşturmanızı öneririz.

    ![Kova oluşturma](images/live-update/01-create-bucket.png)

2. Kovanıza bir kova politikası ekleyin

    Kullanmak istediğiniz kovayı seçin, *Properties* panelini açın ve paneldeki *Permissions* seçeneğini genişletin. *Add bucket policy* düğmesine tıklayarak kova politikasını (bucket policy) açın. Bu örnekteki kova politikası, anonim bir kullanıcının kovadan dosya almasına izin verir; böylece oyun istemcisi, oyunun gerektirdiği Live Update kaynaklarını indirebilir. Kova politikaları hakkında daha fazla bilgi için [Amazon belgelerine](https://docs.aws.amazon.com/AmazonS3/latest/dev/using-iam-policies.html) bakın.

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

    ![Kova politikası](images/live-update/02-bucket-policy.png)

3. Kovanıza bir CORS yapılandırması ekleyin (İsteğe bağlı)

    [Kökenler arası kaynak paylaşımı (Cross-Origin Resource Sharing, CORS)](https://en.wikipedia.org/wiki/Cross-origin_resource_sharing), bir web sitesinin JavaScript kullanarak farklı bir etki alanından kaynak almasını sağlayan bir mekanizmadır. Oyununuzu bir HTML5 istemcisi olarak yayımlamayı planlıyorsanız kovanıza bir CORS yapılandırması eklemeniz gerekir.

    Kullanmak istediğiniz kovayı seçin, *Properties* panelini açın ve paneldeki *Permissions* seçeneğini genişletin. *Add CORS Configuration* düğmesine tıklayarak kova politikasını açın. Bu örnekteki yapılandırma, etki alanı için joker karakter belirterek herhangi bir web sitesinden erişime izin verir; ancak oyununuzu hangi etki alanlarında sunacağınızı biliyorsanız bu erişimi daha fazla kısıtlayabilirsiniz. Amazon CORS yapılandırması hakkında daha fazla bilgi için [Amazon belgelerine](https://docs.aws.amazon.com/AmazonS3/latest/dev/cors.html) bakın.

    ```xml
    <?xml version="1.0" encoding="UTF-8"?>
    <CORSConfiguration xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
        <CORSRule>
            <AllowedOrigin>*</AllowedOrigin>
            <AllowedMethod>GET</AllowedMethod>
        </CORSRule>
    </CORSConfiguration>
    ```

    ![CORS yapılandırması](images/live-update/03-cors-configuration.png)

4. IAM politikası oluşturun

    *Services* menüsünü açın ve *IAM* seçeneğini seçin; bu seçenek _Security, Identity & Compliance_ kategorisinde bulunur ([Amazon IAM Konsolu](https://console.aws.amazon.com/iam)). Soldaki menüden *Policies* seçeneğini seçtiğinizde mevcut tüm politikalarınızı ve yeni bir politika oluşturma seçeneğini göreceksiniz.

    *Create Policy* düğmesine tıklayın ve ardından _Create Your Own Policy_ seçeneğini seçin. Bu örnekteki politika, kullanıcının tüm kovaları listelemesine izin verir; bu yalnızca bir Defold projesini Live Update için yapılandırırken gereklidir. Ayrıca kullanıcının erişim denetim listesini (Access Control List, ACL) almasına ve Live Update kaynakları için kullanılan belirli kovaya kaynak yüklemesine izin verir. Amazon Identity and Access Management (IAM) hakkında daha fazla bilgi için [Amazon belgelerine](http://docs.aws.amazon.com/IAM/latest/UserGuide/access.html) bakın.

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

    ![IAM politikası](images/live-update/04-create-policy.png)

5. Program aracılığıyla erişim için bir kullanıcı oluşturun

    *Services* menüsünü açın ve *IAM* seçeneğini seçin; bu seçenek _Security, Identity & Compliance_ kategorisinde bulunur ([Amazon IAM Konsolu](https://console.aws.amazon.com/iam)). Soldaki menüden *Users* seçeneğini seçtiğinizde mevcut tüm kullanıcılarınızı ve yeni bir kullanıcı ekleme seçeneğini göreceksiniz. Mevcut bir kullanıcıyı kullanmak mümkün olsa da erişimi kolayca kısıtlayabilmeniz için Live Update kaynaklarına yönelik yeni bir kullanıcı eklemenizi öneririz.

    *Add User* düğmesine tıklayın, bir kullanıcı adı girin ve *Programmatic access* seçeneğini *Access type* olarak seçin, ardından *Next: Permissions* düğmesine basın. *Attach existing policies directly* seçeneğini seçin ve 4. adımda oluşturduğunuz politikayı seçin.

    İşlemi tamamladığınızda size bir *Access key ID* ve bir *Secret access key* verilecektir.

    ::: important
    Bu anahtarları saklamanız *çok önemlidir*, çünkü sayfadan ayrıldıktan sonra bunları Amazon'dan tekrar alamazsınız.
    :::

6. Kimlik bilgileri profil dosyası oluşturun

    Bu aşamada bir kova oluşturmuş, bir kova politikası yapılandırmış, bir CORS yapılandırması eklemiş, bir kullanıcı politikası oluşturmuş ve yeni bir kullanıcı oluşturmuş olmalısınız. Geriye yalnızca, Defold düzenleyicisinin sizin adınıza kovaya erişebilmesi için bir [kimlik bilgileri profil dosyası](https://aws.amazon.com/blogs/security/a-new-and-standardized-way-to-manage-credentials-in-the-aws-sdks) oluşturmak kalır.

    Ana klasörünüzde *.aws* adlı yeni bir dizin oluşturun ve bu yeni dizinde *credentials* adlı bir dosya oluşturun.

    ```bash
    $ mkdir ~/.aws
    $ touch ~/.aws/credentials
    ```

    *~/.aws/credentials* dosyası, Amazon Web Services hizmetlerine program aracılığıyla erişmek için kullanacağınız kimlik bilgilerinizi içerir ve AWS kimlik bilgilerini yönetmenin standartlaştırılmış bir yoludur. Dosyayı bir metin düzenleyicisinde açın ve *Access key ID* ile *Secret access key* değerlerinizi aşağıda gösterilen biçimde girin.

    ```ini
    [defold-liveupdate-example]
    aws_access_key_id = <Access key ID>
    aws_secret_access_key = <Secret access key>
    ```

    Köşeli parantezler içinde belirtilen tanımlayıcı, bu örnekte _defold-liveupdate-example_, Defold düzenleyicisinde projenizin Live Update ayarlarını yapılandırırken girmeniz gereken tanımlayıcının aynısıdır.

    ![Live Update ayarları](images/live-update/05-liveupdate-settings.png)
