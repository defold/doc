---
title: Düzenleyici stilini değiştirme
brief: Özel bir stil sayfası kullanarak düzenleyicinin renklerini, tipografisini ve diğer görsel özelliklerini değiştirebilirsiniz.
---

# Düzenleyici stilini değiştirme

Özel bir stil sayfası (stylesheet) kullanarak düzenleyicinin renklerini, tipografisini ve diğer görsel özelliklerini değiştirebilirsiniz:

* Kullanıcı ana dizininizde `.defold` adlı bir klasör oluşturun.
  * Windows'ta `C:\Users\**Your Username**\.defold`
  * macOS'te `/Users/**Your Username**/.defold`
  * Linux'ta `~/.defold`
* `.defold` klasöründe bir `editor.css` dosyası oluşturun

Düzenleyici, başlatıldığında özel stil sayfanızı yükler ve varsayılan stilin üzerine uygular. Düzenleyici, kullanıcı arayüzü için JavaFX kullanır. Stil sayfaları, tarayıcıda bir web sayfasının öğelerine stil öznitelikleri uygulamak için kullanılan CSS dosyalarıyla neredeyse aynıdır. Düzenleyicinin varsayılan stil sayfalarını [GitHub üzerinde inceleyebilirsiniz](https://github.com/defold/defold/tree/editor-dev/editor/styling/stylesheets/base).

## Renkleri değiştirme

Varsayılan renkler [`_palette.scss`](https://github.com/defold/defold/blob/editor-dev/editor/styling/stylesheets/base/_palette.scss) dosyasında tanımlanır ve şöyledir:

```
* {
	// Background
	-df-background-darker:    derive(#212428, -10%);
	-df-background-dark:      derive(#212428, -5%);
	-df-background:           #212428;
	-df-background-light:     derive(#212428, 10%);
	-df-background-lighter:   derive(#212428, 20%);

	// Component
	-df-component-darker:     derive(#464c55, -20%);
	-df-component-dark:       derive(#464c55, -10%);
	-df-component:            #464c55;
	-df-component-light:      derive(#464c55, 10%);
	-df-component-lighter:    derive(#464c55, 20%);

	// Text & icons
	-df-text-dark:            derive(#b4bac1, -10%);
	-df-text:                 #b4bac1;
	-df-text-selected:        derive(#b4bac1, 20%);

  and so on...
```

Temel tema, daha koyu ve daha açık çeşitleriyle birlikte üç renk grubuna ayrılır:

* Arka plan rengi - panellerin, pencerelerin ve iletişim kutularının arka plan rengi
* Bileşen rengi - düğmeler, kaydırma çubuğu tutamaçları, metin alanlarının kenarlıkları
* Metin rengi - metin ve simgeler

Örneğin, kullanıcı ana dizininizdeki `.defold` klasöründe bulunan özel `editor.css` stil sayfanıza şunları eklerseniz:

```
* {
	-df-background-darker:    derive(#0a0a42, -10%);
	-df-background-dark:      derive(#0a0a42, -5%);
	-df-background:           #0a0a42;
	-df-background-light:     derive(#0a0a42, 10%);
	-df-background-lighter:   derive(#0a0a42, 20%);
}
```

Düzenleyicinizde aşağıdaki görünümü elde edersiniz:

![](images/editor/editor-styling-color.png)


## Yazı tiplerini değiştirme

Düzenleyici iki yazı tipi kullanır: kod ve sabit genişlikli metin (hatalar) için `Dejavu Sans Mono`, arayüzün geri kalanı için `Source Sans Pro`. Yazı tipi tanımları ağırlıklı olarak [`_typography.scss`](https://github.com/defold/defold/blob/editor-dev/editor/styling/stylesheets/base/_typography.scss) dosyasında bulunur ve şöyledir:

```
@font-face {
  src: url("SourceSansPro-Light.ttf");
}

@font-face {
  src: url("DejaVuSansMono.ttf");
}

$default-font-mono: 'Dejavu Sans Mono';
$default-font: 'Source Sans Pro';
$default-font-bold: 'Source Sans Pro Semibold';
$default-font-italic: 'Source Sans Pro Italic';
$default-font-light: 'Source Sans Pro Light';

.root {
    -fx-font-size: 13px;
    -fx-font-family: $default-font;
}

Text.strong {
  -fx-font-family: $default-font-bold;
}

and so on...
```

Ana yazı tipi bir kök öğede tanımlanır; bu da çoğu yerde yazı tipini değiştirmeyi oldukça kolaylaştırır. `editor.css` dosyanıza şunları ekleyin:

```
@import url('https://fonts.googleapis.com/css2?family=Architects+Daughter&display=swap');

.root {
    -fx-font-family: "Architects Daughter";
}
```

Düzenleyicinizde aşağıdaki görünümü elde edersiniz:

![](images/editor/editor-styling-fonts.png)

Web yazı tipi yerine yerel bir yazı tipi kullanmak da mümkündür:

```
@font-face {
  font-family: 'Comic Sans MS';
  src: local("cs.ttf");
}

.root {
  -fx-font-family: 'Comic Sans MS';
}
```

::: sidenote
Kod düzenleyicisinin yazı tipi, düzenleyicinin Preferences ayarlarında ayrıca tanımlanır!
:::
