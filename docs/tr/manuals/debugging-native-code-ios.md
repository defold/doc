---
title: iOS/macOS üzerinde hata ayıklama
brief: Bu kılavuz, Xcode kullanarak bir derleme çıktısında nasıl hata ayıklanacağını açıklar.
---

# iOS/macOS üzerinde hata ayıklama

Burada, Apple'ın macOS ve iOS için geliştirmede tercih ettiği bütünleşik geliştirme ortamı (IDE) olan [Xcode](https://developer.apple.com/xcode/) kullanılarak bir derleme çıktısında hata ayıklamanın (debugging) nasıl yapıldığını açıklıyoruz.

## Xcode

* bob kullanarak, `--with-symbols` seçeneğiyle uygulamanın dağıtım paketini oluşturun ([daha fazla bilgi](/manuals/debugging-native-code/#symbolicate-a-callstack)):

```sh
$ cd myproject
$ wget http://d.defold.com/archive/<sha1>/bob/bob.jar
$ java -jar bob.jar --platform armv7-darwin build --with-symbols --variant debug --archive bundle -bo build/ios -mp <app>.mobileprovision --identity "iPhone Developer: Your Name (ID)"
```

* Uygulamayı `Xcode`, `iTunes` veya [ios-deploy](https://github.com/ios-control/ios-deploy) ile kurun

```sh
$ ios-deploy -b <AppName>.ipa
```

* `.dSYM` klasörünü, yani hata ayıklama sembollerini (debug symbols) edinin

	* Uygulama yerel kod eklentileri (Native Extensions) kullanmıyorsa `.dSYM` dosyasını [d.defold.com](http://d.defold.com) adresinden indirebilirsiniz

	* Yerel kod eklentisi kullanıyorsanız `.dSYM` klasörü, [bob.jar](https://www.defold.com/manuals/bob/) ile projeyi derlediğinizde oluşturulur. Yalnızca projeyi derlemek gerekir (arşivleme veya paketleme gerekmez):

```sh
$ cd myproject
$ unzip .internal/cache/arm64-ios/build.zip
$ mv dmengine.dSYM <AppName>.dSYM
$ mv <AppName>.dSYM/Contents/Resources/DWARF/dmengine <AppName>.dSYM/Contents/Resources/DWARF/<AppName>
```

### Proje oluşturma

Düzgün hata ayıklayabilmek için bir projemiz olması ve kaynak kodun eşlenmesi gerekir.
Bu projeyi yalnızca hata ayıklamak için kullanıyoruz; derleme yapmak için kullanmıyoruz.

* Yeni bir Xcode projesi oluşturun, `Game` şablonunu seçin

	![Proje şablonu](images/extensions/debugging/ios/project_template.png)

* Bir ad (örneğin `debug`) ve varsayılan ayarları seçin

* Projenin kaydedileceği klasörü seçin

* Kodunuzu uygulamaya ekleyin

	![Dosya ekleme](images/extensions/debugging/ios/add_files.png)

* "Copy items if needed" seçeneğinin işaretli olmadığından emin olun.

	![Kaynak kod ekleme](images/extensions/debugging/ios/add_source.png)

* Sonuç şöyle görünür

	![Eklenen kaynak kod](images/extensions/debugging/ios/added_source.png)


* `Build` adımını devre dışı bırakın

	![Şema düzenleme](images/extensions/debugging/ios/edit_scheme.png)

	![Derleme adımını devre dışı bırakma](images/extensions/debugging/ios/disable_build.png)

* `Deployment target` sürümünü, artık cihazınızın iOS sürümünden daha yüksek olacak şekilde ayarlayın

	![Dağıtıma alma sürümü](images/extensions/debugging/ios/deployment_version.png)

* Hedef cihazı seçin

	![Cihaz seçme](images/extensions/debugging/ios/select_device.png)


### Hata ayıklayıcıyı başlatma

Bir uygulamada hata ayıklamak için birkaç seçeneğiniz vardır

1. `Debug` -> `Attach to process...` yolunu seçip uygulamayı buradan seçebilirsiniz

2. Ya da `Attach to process by PID or Process name` seçeneğini seçebilirsiniz

	![Cihaz seçme](images/extensions/debugging/ios/attach_to_process_name.png)

3. Uygulamayı cihazda başlatın

4. `Edit Scheme` içinde <AppName>.app klasörünü yürütülebilir dosya olarak ekleyin

### Hata ayıklama sembolleri

**lldb kullanabilmek için yürütme duraklatılmış olmalıdır**

* `.dSYM` yolunu lldb'ye ekleyin

```
(lldb) add-dsym <PathTo.dSYM>
```

	![dSYM ekleme](images/extensions/debugging/ios/add_dsym.png)

* `lldb` tarafından sembollerin başarıyla okunduğunu doğrulayın

```
(lldb) image list <AppName>
```

### Yol eşlemeleri

* Motorun kaynak kodunu ekleyin (gereksinimlerinize göre değiştirin)

```
(lldb) settings set target.source-map /Users/builder/ci/builds/engine-ios-64-master/build /Users/mathiaswesterdahl/work/defold
(lldb) settings append target.source-map /private/var/folders/m5/bcw7ykhd6vq9lwjzq1mkp8j00000gn/T/job4836347589046353012/upload/videoplayer/src /Users/mathiaswesterdahl/work/projects/extension-videoplayer-native/videoplayer/src
```

* İş klasörünü yürütülebilir dosyadan öğrenebilirsiniz. İş klasörü `job1298751322870374150` biçiminde adlandırılır ve her seferinde rastgele bir sayı kullanılır.

```sh
$ dsymutil -dump-debug-map <executable> 2>&1 >/dev/null | grep /job

```

* Kaynak eşlemelerini doğrulayın

```
(lldb) settings show target.source-map
```

Bir sembolün hangi kaynak dosyadan geldiğini şu komutla kontrol edebilirsiniz

```
(lldb) image lookup -va <SymbolName>
```

### Kesme noktaları

* Proje görünümünde bir dosya açın ve bir kesme noktası (breakpoint) belirleyin

	![Kesme noktası](images/extensions/debugging/ios/breakpoint.png)

## Notlar

### İkili dosyanın UUID değerini kontrol etme

Hata ayıklayıcının `.dSYM` klasörünü kabul etmesi için UUID değerinin, hata ayıklanan yürütülebilir dosyanın UUID değeriyle eşleşmesi gerekir. UUID değerini şu şekilde kontrol edebilirsiniz:

```sh
$ dwarfdump -u <PathToBinary>
```