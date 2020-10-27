Właściwość *Blend Mode* określa w jaki sposób graficzne komponenty mają być ze sobą mieszane, czyli wyświetlane w momencie nakładania się dwóch obrazów na siebie. Oto dostępne tryby blendowania i wyjaśnienie w jaki sposób są obliczane kolory:

Alpha
: Normalne blendowanie: `src.a * src.rgb + (1 - src.a) * dst.rgb`

Add
: Rozświetl grafikę w tle wartościami kolorów z grafiki na przednim planie: `src.rgb + dst.rgb`

Multiply
: Zaciemnij grafikę w tle wartościami kolorów z grafiki na przednim planie: `src.rgb * dst.rgb`
