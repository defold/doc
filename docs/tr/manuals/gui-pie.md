---
title: Defold GUI daire dilimi düğümleri
brief: Bu kılavuz, Defold GUI sahnelerinde daire dilimi düğümlerinin nasıl kullanılacağını açıklar.
---

# GUI daire dilimi düğümleri

Daire dilimi düğümleri (pie nodes), basit dairelerden daire dilimlerine ve kare halka şekillerine kadar uzanan dairesel veya elipsoit biçimli nesneler oluşturmak için kullanılır.

## Daire dilimi düğümü oluşturma

*Outline* görünümündeki *Nodes* bölümüne <kbd>sağ tıklayın</kbd> ve <kbd>Add ▸ Pie</kbd> seçeneğini seçin. Yeni daire dilimi düğümü seçilir ve özelliklerini değiştirebilirsiniz.

![Daire dilimi düğümü oluşturma](images/gui-pie/create.png)

Aşağıdaki özellikler daire dilimi düğümlerine özgüdür:

Inner Radius
: Düğümün X ekseni boyunca belirtilen iç yarıçapı.

Outer Bounds
: Düğümün dış sınırlarının şekli.

  - `Ellipse`, düğümü dış yarıçapa kadar uzatır.
  - `Rectangle`, düğümü sınırlayıcı kutusuna (bounding box) kadar uzatır.

Perimeter Vertices
: Şekli oluşturmak için kullanılacak bölüm sayısı; düğümün 360 derecelik çevresini tamamen çevrelemek için gereken köşe (vertex) sayısı olarak belirtilir.

Pie Fill Angle
: Daire diliminin ne kadarının doldurulacağı. Sağdan başlayıp saat yönünün tersine ilerleyen bir açı olarak belirtilir.

![Özellikler](images/gui-pie/properties.png)

Düğüme bir doku (texture) atarsanız doku görüntüsü, dokunun köşeleri düğümün sınırlayıcı kutusunun köşelerine karşılık gelecek şekilde düz olarak uygulanır.

## Çalışma sırasında daire dilimi düğümlerini değiştirme

Daire dilimi düğümleri, boyut, dayanak noktası (pivot), renk ve benzeri ayarları değiştiren tüm genel düğüm işlevlerini destekler. Yalnızca daire dilimi düğümlerine özgü birkaç işlev ve özellik de bulunur:

```lua
local pienode = gui.get_node("my_pie_node")

-- get the outer bounds
local fill_angle = gui.get_fill_angle(pienode)

-- increase perimeter vertices
local vertices = gui.get_perimeter_vertices(pienode)
gui.set_perimeter_vertices(pienode, vertices + 1)

-- change outer bounds
gui.set_outer_bounds(pienode, gui.PIEBOUNDS_RECTANGLE)

-- animate the inner radius
gui.animate(pienode, "inner_radius", 100, gui.EASING_INOUTSINE, 2, 0, nil, gui.PLAYBACK_LOOP_PINGPONG)
```
