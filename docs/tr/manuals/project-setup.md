---
title: Proje kurulumu
brief: Bu kılavuz, Defold'da proje oluşturmayı veya açmayı açıklar.
---

# Proje kurulumu

Defold düzenleyicisinden kolayca yeni bir proje oluşturabilirsiniz. Ayrıca bilgisayarınızda bulunan mevcut bir projeyi de açabilirsiniz.

## Yeni bir yerel proje oluşturma {#creating-a-new-project}

<kbd>New Project</kbd> seçeneğine tıklayın ve oluşturmak istediğiniz proje türünü seçin. Proje dosyalarının saklanacağı konumu sabit diskinizde belirtin. Projeyi seçtiğiniz konumda oluşturmak için <kbd>Create New Project</kbd> seçeneğine tıklayın. Bir şablondan (Template) yeni proje oluşturabilirsiniz:

![proje açma](images/workflow/open_project.png)

Veya adım adım yönergeler içeren bir öğreticiden (Tutorial):

![öğreticiden proje oluşturma](images/workflow/create_from_tutorial.png)

Veya tamamlanmış bir örnek oyundan (Sample):

![örnekten proje oluşturma](images/workflow/create_from_sample.png)

### Projeyi GitHub'a ekleme

Yerel bir proje herhangi bir sürüm kontrol sistemiyle (version control system) bütünleşik değildir; yani dosyalar yalnızca sabit diskinizde bulunur ve değişiklikleri geri alabileceğiniz bir geçmiş yoktur. Düzenleyicinin *Assets* bölmesinden silinen dosyalar, desteklendiğinde sistemin Trash veya Recycle Bin klasörüne taşınır; ancak bu işlem kullanılamıyorsa veya başarısız olursa dosyalar kalıcı olarak silinebilir. Çöp kutusu, dosyalarda yapılan düzenlemelere karşı koruma sağlamaz ve sürüm geçmişi tutmaz; bu nedenle dosyalarınızdaki değişiklikleri izlemek için Git gibi bir sürüm kontrol sistemi kullanmanız önerilir. Bu, bir projede başkalarıyla birlikte çalışmayı da çok kolaylaştırır. Yerel bir projeyi GitHub'a yüklemek yalnızca birkaç adımda yapılabilir:

1. [GitHub](https://github.com/) üzerinde bir hesap oluşturun veya hesabınıza giriş yapın
2. [New Repository](https://help.github.com/en/articles/creating-a-new-repository) seçeneğini kullanarak bir depo oluşturun
3. [Upload Files](https://help.github.com/en/articles/adding-a-file-to-a-repository) seçeneğiyle tüm proje dosyalarını yükleyin

Proje artık sürüm kontrolü altındadır; [projeyi klonlayarak](https://help.github.com/en/articles/cloning-a-repository) yerel sabit diskinize kopyalamanız ve artık bu yeni konumda çalışmanız önerilir.

## Mevcut bir projeyi açma

Bilgisayarınızda bulunan bir projeyi açmak için <kbd>Open From Disk</kbd> seçeneğine tıklayın.

![projeyi içe aktarma](images/workflow/open_from_disk.png)

## Son kullanılan bir projeyi açma

Bir proje bir kez açıldıktan sonra son kullanılan projeler listesinde görünür. Bu liste, en son üzerinde çalıştığınız projeleri gösterir ve listedeki bir projeye çift tıklayarak onu hızla açmanızı sağlar.
