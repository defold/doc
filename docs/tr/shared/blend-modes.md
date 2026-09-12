*Blend Mode* özelliği, bileşenin (component) grafiklerinin arkasındaki grafiklerle nasıl harmanlanacağını belirler. Kullanılabilir harmanlama modları (blend modes) ve hesaplanma biçimleri şunlardır:

Alpha
: Normal harmanlama: `src.a * src.rgb + (1 - src.a) * dst.rgb`

Add
: Bileşenin karşılık gelen piksellerinin renk değerleriyle arka planı aydınlatır: `src.rgb + dst.rgb`

Multiply
: Bileşenin karşılık gelen piksellerinin değerleriyle arka planı koyulaştırır: `src.rgb * dst.rgb`

Screen
: Multiply modunun tersidir. Arka planın ve bileşenin karşılık gelen piksellerinin parlaklığını artırır: `src.rgb - dst.rgb * dst.rgb`
