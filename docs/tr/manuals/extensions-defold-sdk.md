---
title: Yerel kod eklentileri - Defold SDK
brief: Bu kılavuz, yerel kod eklentileri oluştururken Defold SDK ile nasıl çalışılacağını açıklar.
---

# Defold SDK

Defold yazılım geliştirme kiti (SDK), bir yerel kod eklentisini (native extension) bildirmek için gereken işlevlerin yanı sıra uygulamanın çalıştığı düşük düzeyli yerel platform katmanıyla ve oyun mantığının oluşturulduğu yüksek düzeyli Lua katmanıyla etkileşim kurmak için gereken işlevleri içerir.

## Kullanım

C++ eklentileri, diğer başlıkları bir araya getiren `dmsdk/sdk.h` başlık dosyasını (header file) dahil edebilir:

```cpp
#include <dmsdk/sdk.h>
```

Birleştirilmiş başlık dosyası, C++ bildirimleri içerir ve bir C kaynak dosyasından dahil edilemez. C kaynak dosyalarına, gereken C uyumlu `.h` başlık dosyalarını ayrı ayrı dahil etmeniz önerilir; örneğin:

```c
#include <dmsdk/extension/extension.h>
#include <dmsdk/dlib/configfile.h>
#include <dmsdk/resource/resource.h>
```

Şu anda dmSDK'nin yalnızca bir bölümünde saf C arayüzü bulunur; her C++ alt sisteminin C karşılığı yoktur. Kullanılabilir işlevler ve türler, [C API'sine genel bakış](/ref/overview_defoldc/) ve [C++ API'sine genel bakış](/ref/overview_defoldcpp/) sayfalarında belgelenmiştir. Defold SDK başlık dosyaları, ayrı bir `defoldsdk_headers.zip` arşivi olarak Defold'un [GitHub'da yayımlanan her sürümüne](https://github.com/defold/defold/releases) dahil edilir. Bu başlık dosyalarını, tercih ettiğiniz düzenleyicide kod tamamlama için kullanabilirsiniz.
