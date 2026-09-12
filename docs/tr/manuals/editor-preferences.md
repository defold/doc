---
title: Düzenleyici tercihleri
brief: Düzenleyicinin ayarlarını Preferences penceresinden değiştirebilirsiniz.
---

# Düzenleyici tercihleri

Düzenleyicinin ayarlarını Preferences penceresinden değiştirebilirsiniz. Tercihler penceresi <kbd>File -> Preferences</kbd> menüsünden açılır.

## General

![](images/editor/preferences_general.png)

Load External Changes on App Focus
: Düzenleyici odaklandığında dışarıda yapılan değişikliklerin taranmasını etkinleştirir.

Open Bundle Target Folder
: Paketleme işlemi tamamlandıktan sonra dağıtım paketinin hedef klasörünün açılmasını etkinleştirir.

Enable Texture Compression
: Düzenleyicide yapılan tüm derlemeler için [doku sıkıştırmayı](/manuals/texture-profiles) etkinleştirir.

Escape Quits Game
: Oyununuzun çalışan bir derlemesini <kbd>Esc</kbd> tuşuyla kapatın.

Track Active Tab in Asset Browser
: *Editor* bölmesinde seçili sekmede düzenlenen dosya, Asset Browser görünümünde (*Asset* bölmesi olarak da bilinir) seçilir.

Lint Code on Build
: Proje derlenirken [statik kod denetimini](/manuals/writing-code/#linting-configuration) etkinleştirir. Bu seçenek varsayılan olarak etkindir, ancak büyük bir projede statik kod denetimi çok uzun sürüyorsa devre dışı bırakılabilir.

Engine Arguments
: Düzenleyici derleyip çalıştırdığında dmengine yürütülebilir dosyasına iletilecek bağımsız değişkenler.
 Her satırda bir bağımsız değişken kullanın. Örneğin:
 ```
--config=bootstrap.main_collection=/my dir/1.collectionc
--verbose
--graphics-adapter=vulkan
```


## Code

![](images/editor/preferences_code.png)

Custom Editor
: Harici bir düzenleyicinin mutlak yolu. macOS'ta .app içindeki yürütülebilir dosyanın yolu olmalıdır (ör. `/Applications/Atom.app/Contents/MacOS/Atom`).

Open File
: Özel düzenleyicinin hangi dosyanın açılacağını belirtmek için kullandığı kalıp. `{file}` kalıbı, açılacak dosyanın adıyla değiştirilir.

Open File at Line
: Özel düzenleyicinin hangi dosyanın ve hangi satır numarasında açılacağını belirtmek için kullandığı kalıp. `{file}` kalıbı, açılacak dosyanın adıyla; `{line}` ise satır numarasıyla değiştirilir.

Code editor font
: Kod düzenleyicisinde kullanılacak, sistemde yüklü bir yazı tipinin adı.

Zoom on Scroll
: Cmd/Ctrl tuşu basılı tutulurken kod düzenleyicisinde kaydırma yapıldığında yazı tipi boyutunun değiştirilip değiştirilmeyeceğini belirler.

Auto-insert closing parens
: Kod düzenlenirken eşleşen kapanış karakterlerini otomatik olarak ekler. Bu seçenek varsayılan olarak etkindir.

Format on save
: Kaydederken dil sunucusunun biçimlendiricisini değiştirilmiş açık kod dosyalarında çalıştırır. Varsayılan olarak devre dışıdır. Dil sunucusu biçimlendirmeyi desteklemelidir; bir belgeyi veya seçimi elle biçimlendirmek için [kod biçimlendirme](/manuals/writing-code/#formatting-code) bölümüne bakın.


### Betik dosyalarını Visual Studio Code'da açma

![](images/editor/preferences_vscode.png)

Betik dosyalarını Defold düzenleyicisinden doğrudan Visual Studio Code'da açmak için yürütülebilir dosyanın yolunu belirterek aşağıdaki ayarları yapmanız gerekir:

- macOS: `/Applications/Visual Studio Code.app/Contents/MacOS/Electron`
- Linux: `/usr/bin/code`
- Windows: `C:\Program Files\Microsoft VS Code\Code.exe`

 Belirli dosyaları ve satırları açmak için şu parametreleri ayarlayın:

- Open File: `. {file}`
- Open File at Line: `. -g {file}:{line}`

Buradaki `.` karakteri, tek bir dosya yerine çalışma alanının tamamını açmak için gereklidir.


## Extensions

![](images/editor/preferences_extensions.png)

Build Server
: [Yerel kod eklentileri (native extensions)](/manuals/extensions) içeren bir proje derlenirken kullanılan derleme sunucusunun URL adresi. Derleme sunucusuna kimliği doğrulanmış erişim için URL adresine bir kullanıcı adı ve erişim belirteci eklenebilir. Kullanıcı adını ve erişim belirtecini belirtmek için şu gösterimi kullanın: `username:token@build.defold.com`. Nintendo Switch derlemelerinde ve kimlik doğrulamanın etkinleştirildiği kendi derleme sunucusu örneğinizi çalıştırırken kimliği doğrulanmış erişim gerekir (daha fazla bilgi için [derleme sunucusu belgelerine bakın](https://github.com/defold/extender/blob/dev/README_SECURITY.md)). Kullanıcı adı ve parola, `DM_EXTENDER_USERNAME` ve `DM_EXTENDER_PASSWORD` sistem ortam değişkenleri olarak da ayarlanabilir.

Build Server Username
: Kimlik doğrulama için kullanıcı adı.

Build Server Password
: Kimlik doğrulama için parola; tercihler dosyasında şifrelenmiş olarak saklanır.

Build Server Headers
: Yerel kod eklentileri derlenirken derleme sunucusuna gönderilen ek üstbilgiler. CloudFlare hizmetini veya benzer hizmetleri extender ile kullanmak için önemlidir.

## Tools

![](images/editor/preferences_tools.png)

ADB path
: Bu sistemde kurulu [ADB](https://developer.android.com/tools/adb) komut satırı aracının yolu. Sisteminizde ADB kuruluysa Defold düzenleyicisi, paketlenmiş Android APK dosyalarını bağlı bir Android cihazına kurmak ve çalıştırmak için bu aracı kullanır. Düzenleyici varsayılan olarak ADB'nin yaygın konumlarda kurulu olup olmadığını denetler; bu nedenle yolu yalnızca ADB'yi özel bir konuma kurduysanız belirtmeniz gerekir.

ios-deploy path
: Bu sistemde kurulu [ios-deploy](https://github.com/ios-control/ios-deploy) komut satırı araçlarının yolu (yalnızca macOS için geçerlidir). ADB yolunda olduğu gibi Defold düzenleyicisi, paketlenmiş iOS uygulamalarını bağlı bir iPhone'a kurmak ve çalıştırmak için bu aracı kullanır. Düzenleyici varsayılan olarak ios-deploy aracının yaygın konumlarda kurulu olup olmadığını denetler; bu nedenle yolu yalnızca ios-deploy için özel bir kurulum kullanıyorsanız belirtmeniz gerekir.

## Keymap

![](images/editor/preferences_keymap.png)

Düzenleyicinin klavye kısayollarını ve fare kontrollerini Keymap sekmesinde yapılandırabilirsiniz. Bir komutu değiştirmek için komuta çift tıklayın, <kbd>Enter</kbd> veya <kbd>Space</kbd> tuşuna basın ya da satırın bağlam menüsünü kullanın.

Klavye kısayolları *Shortcuts* sütununda tuş birleşimleri olarak görünür. Fare kontrolleri aynı listede bir rozetle görünür:

- <kbd>MB</kbd>, isteğe bağlı olarak <kbd>Shift</kbd>, <kbd>Ctrl</kbd>/<kbd>Control</kbd> veya <kbd>Alt</kbd> ile birleştirilen bir fare düğmesi eşlemesini belirtir.
- <kbd>MM</kbd>, bir fare eyleminin kullandığı değiştirici tuşu belirtir.

Bazı fare kontrolleri, varsayılan Scene 2D Camera eşlemelerini yeniden kullanır; bu nedenle bir satır, siz özelleştirmeden önce de bir eşleme gösterebilir. Bunlar genellikle daha koyu bir renkle gösterilir. Bu satır için özel bir eşleme ayarlarsanız Defold sizin eşlemenizi kullanır. Değişikliğinizi kaldırıp yerleşik veya devralınan davranışa dönmek için *Reset to Defaults* seçeneğini kullanın.

Uyarılar turuncu renkte gösterilir. Ayrıntıları görmek için işaretçiyi uyarının üzerine getirin. Uyarılar genellikle şunları belirtir:
- Kısayol metin girebilir ve metin alanlarını etkileyebilir.
- Aynı kısayol veya fare eşlemesi başka bir komut tarafından zaten kullanılıyordur.
