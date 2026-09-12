---
title: Defold'da GUI kutu düğümleri
brief: Bu kılavuz, GUI kutu düğümlerinin nasıl kullanılacağını açıklar.
---

# GUI kutu düğümleri

Kutu düğümü (box node), bir renk, doku (texture) veya animasyonla doldurulmuş bir dikdörtgendir.

## Kutu düğümleri ekleme

Yeni kutu düğümleri eklemek için *Outline* görünümünde <kbd>sağ tıklayın</kbd> ve <kbd>Add ▸ Box</kbd> seçeneğini seçin ya da <kbd>A</kbd> tuşuna basıp <kbd>Box</kbd> seçeneğini seçin.

GUI'ye eklenmiş atlaslardan veya karo kaynaklarından (tile source) görüntü ve animasyon kullanabilirsiniz. Doku eklemek için *Outline* görünümündeki *Textures* klasör simgesine <kbd>sağ tıklayın</kbd> ve <kbd>Add ▸ Textures...</kbd> seçeneğini seçin. Ardından kutu düğümündeki *Texture* özelliğini ayarlayın:

![Dokular](images/gui-box/create.png)

Kutu düğümünün renginin, grafiklere renk çarpanı (tint) olarak uygulandığını unutmayın. Bu renk, görüntü verileriyle çarpılır; dolayısıyla rengi beyaz (varsayılan) olarak ayarlarsanız görüntünün rengi değişmez.

![Renk çarpanı uygulanmış doku](images/gui-box/tinted.png)

Kutu düğümleri, kendilerine bir doku atanmamış olsa, alfa değerleri `0` olarak ayarlanmış olsa veya boyutları `0, 0, 0` olsa bile her zaman işleme (rendering) sürecine dahil edilir. İşleyicinin bunları düzgün biçimde toplu olarak çizebilmesi ve çizim çağrısı sayısını azaltabilmesi için kutu düğümlerine her zaman bir doku atanması önerilir.

## Animasyonları oynatma

Kutu düğümleri, atlaslardaki veya karo kaynaklarındaki animasyonları oynatabilir. Daha fazla bilgi için [kare dizisi animasyonu kılavuzuna](/manuals/flipbook-animation) bakın.

:[Slice-9](../shared/slice-9-texturing.md)
