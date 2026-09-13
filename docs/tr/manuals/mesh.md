---
title: Defold'da 3B örgüler
brief: Bu kılavuz, oyununuzda çalışma sırasında 3B örgülerin nasıl oluşturulacağını açıklar.
---

# Örgü bileşeni

Defold özünde bir 3B motordur. Yalnızca 2B içerikle çalışsanız bile görüntü oluşturmak için yapılan tüm işleme (rendering) 3B olarak gerçekleştirilir ve ekrana ortografik izdüşümle yansıtılır. Defold, koleksiyonlarınıza (collection) çalışma sırasında 3B örgüler (mesh) ekleyip oluşturarak 3B içerikten tam olarak yararlanmanıza olanak tanır. Yalnızca 3B varlıklarla tamamen 3B oyunlar oluşturabilir veya 3B ve 2B içeriği dilediğiniz gibi bir arada kullanabilirsiniz.

## Örgü bileşeni oluşturma

Örgü bileşenleri, diğer oyun nesnesi (game object) bileşenleri (component) gibi oluşturulur. Bunu iki şekilde yapabilirsiniz:

- *Assets* tarayıcısında bir konuma <kbd>sağ tıklayıp</kbd> <kbd>New... ▸ Mesh</kbd> seçeneğini seçerek bir *örgü dosyası* oluşturun.
- *Outline* görünümünde bir oyun nesnesine <kbd>sağ tıklayıp</kbd> <kbd>Add Component ▸ Mesh</kbd> seçeneğini seçerek bileşeni doğrudan oyun nesnesine gömülü olarak oluşturun.

![Oyun nesnesindeki örgü](images/mesh/mesh.png)

Örgüyü oluşturduktan sonra bazı özellikleri belirtmeniz gerekir:

### Örgü özellikleri

*Id*, *Position* ve *Rotation* özelliklerine ek olarak bileşene özgü şu özellikler bulunur:

*Material*
: Örgüyü işlemek için kullanılacak materyal (material).

*Vertices*
: Örgü verilerini akış (stream) başına tanımlayan bir arabellek (buffer) dosyası.

*Primitive Type*
: Lines, Triangles veya Triangle Strip.

*Position Stream*
: Bu özelliğin değeri, *position* akışının adı olmalıdır. Akış, köşe gölgelendiricisine (vertex shader) otomatik biçimde girdi olarak sağlanır.

*Normal Stream*
: Bu özelliğin değeri, *normal* akışının adı olmalıdır. Akış, köşe gölgelendiricisine otomatik biçimde girdi olarak sağlanır.

*tex0*
: Bunu örgü için kullanılacak dokuya (texture) ayarlayın.

## Düzenleyicide değiştirme

Örgü bileşenini ekledikten sonra, standart *Scene Editor* araçlarıyla bileşeni ve/veya onu içeren oyun nesnesini düzenleyip değiştirerek örgüyü istediğiniz gibi taşıyabilir, döndürebilir ve ölçekleyebilirsiniz.

## Çalışma sırasında değiştirme

Defold arabelleklerini kullanarak çalışma sırasında örgüleri değiştirebilirsiniz. Üçgen şeritlerinden (triangle strips) bir küp oluşturma örneği:

```Lua

-- cube
local vertices = {
	0, 0, 0,
	0, 1, 0,
	1, 0, 0,
	1, 1, 0,
	1, 1, 1,
	0, 1, 0,
	0, 1, 1,
	0, 0, 1,
	1, 1, 1,
	1, 0, 1,
	1, 0, 0,
	0, 0, 1,
	0, 0, 0,
	0, 1, 0
}

-- create a buffer with a position stream
local buf = buffer.create(#vertices / 3, {
	{ name = hash("position"), type=buffer.VALUE_TYPE_FLOAT32, count = 3 }
})

-- get the position stream and write the vertices
local positions = buffer.get_stream(buf, "position")
for i, value in ipairs(vertices) do
	positions[i] = vertices[i]
end

-- set the buffer with the vertices on the mesh
local res = go.get("#mesh", "vertices")
resource.set_buffer(res, buf)
```

Örgü bileşeninin nasıl kullanılacağı hakkında örnek projeler ve kod parçaları içeren [daha fazla bilgi için forumdaki duyuru yazısına bakın](https://forum.defold.com/t/mesh-component-in-defold-1-2-169-beta/65137).

## Görüş hacmi dışında kalanları eleme {#frustum-culling}

Örgü bileşenlerine, dinamik yapıları ve konum verilerinin nasıl kodlandığının kesin olarak bilinememesi nedeniyle görünmeyenleri eleme (culling) işlemi otomatik uygulanmaz. Bir örgünün elenebilmesi için eksenlere hizalı sınırlayıcı kutusunun (axis-aligned bounding box) 6 kayan noktalı sayı kullanılarak arabelleğe üst veri olarak ayarlanması gerekir (AABB min/max):

```lua
buffer.set_metadata(buf, hash("AABB"), { 0, 0, 0, 1, 1, 1 }, buffer.VALUE_TYPE_FLOAT32)
```

## Materyal sabitleri

{% include shared/material-constants.md component='mesh' variable='tint' %}

`tint`
: Örgünün renk çarpanı (`vector4`). Renk çarpanını temsil etmek için `vector4` kullanılır; x, y, z ve w sırasıyla kırmızı, yeşil, mavi ve alfa renk çarpanlarına karşılık gelir.

## Köşelerin yerel uzayı ve dünya uzayı
Örgü materyalinin Vertex Space ayarı Local Space olarak ayarlanmışsa veriler gölgelendiricinize olduğu gibi sağlanır ve köşeleri/normalleri her zamanki gibi GPU üzerinde dönüştürmeniz gerekir.

Örgü materyalinin Vertex Space ayarı World Space olarak ayarlanmışsa varsayılan bir `position` ve `normal` akışı sağlamanız gerekir veya örgüyü düzenlerken akışı açılır listeden seçebilirsiniz. Böylece motor, diğer nesnelerle toplu çizim (batching) yapmak için verileri dünya uzayına (world space) dönüştürebilir.
