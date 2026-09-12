---
title: Bir Defold oyununun bellek kullanımını optimize etme
brief: Bu kılavuz, bir Defold oyununun bellek kullanımının nasıl optimize edileceğini açıklar.
---

# Bellek kullanımını optimize etme

## Doku sıkıştırma
Doku sıkıştırma (texture compression) kullanmak, oyun arşivinizdeki kaynakların (resource) boyutunu azaltır; sıkıştırılmış dokular gereken GPU belleği miktarını da azaltabilir.

## Dinamik yükleme
Çoğu oyunda en azından seyrek kullanılan bir miktar içerik bulunur. Bellek kullanımı açısından bu tür içeriği her zaman bellekte yüklü tutmak anlamlı değildir; bunun yerine gerektiğinde yüklemek ve bellekten kaldırmak daha uygundur. Bu, doğal olarak, çalışma sırasında bellek kullanımı pahasına bir içeriği hemen erişilebilir tutmak ile yükleme süresi pahasına onu yüklemek arasında bir ödünleşimdir.

Defold, içeriği dinamik olarak yüklemek için birkaç farklı yol sunar:

* [Koleksiyon vekilleri (collection proxy)](/manuals/collection-proxy/)
* [Dinamik koleksiyon fabrikaları (collection factory)](/manuals/collection-factory/#dynamic-loading-of-factory-resources)
* [Dinamik fabrikalar (factory)](/manuals/factory/#dynamic-loading-of-factory-resources)
* [Live Update](/manuals/live-update/)

## Bileşen sayaçlarını optimize etme
Defold, bellek parçalanmasını azaltmak için bir koleksiyon (collection) oluşturulduğunda bileşenler (component) ve kaynaklar için belleği tek seferde ayırır. Ayrılan bellek miktarı, *game.project* dosyasındaki çeşitli bileşen sayaçlarının yapılandırmasına bağlıdır. Bileşen ve kaynak kullanımını doğru ölçmek için [profil çıkarıcıyı (profiler)](/manuals/profiling/) kullanın ve oyununuzu, gerçek bileşen ve kaynak sayılarına daha yakın en yüksek değerleri kullanacak şekilde yapılandırın. Bu, oyununuzun kullandığı bellek miktarını azaltır (bileşenlerin [en yüksek sayılarını optimize etme](/manuals/project-settings/#component-max-count-optimizations) hakkındaki bilgilere bakın).

## GUI düğümü sayısını optimize etme
GUI dosyasındaki en fazla düğüm sayısını yalnızca gereken miktara ayarlayarak GUI düğümlerinin (node) sayısını optimize edin. [GUI bileşeni özelliklerindeki](https://defold.com/manuals/gui/#gui-properties) `Current Nodes` alanı, GUI bileşeninin kullandığı düğüm sayısını gösterir.

:[HTML5 Optimizations](../shared/optimization-memory-html5.md)

