---
title: Defold'da kinematik çarpışmaları çözme
brief: Bu kılavuz, kinematik fizik çarpışmalarının nasıl çözüleceğini açıklar.
---

# Kinematik çarpışmaları çözme

Kinematik çarpışma nesnelerini (kinematic collision objects) kullanırken çarpışmaları kendiniz çözmeniz ve tepki olarak nesneleri hareket ettirmeniz gerekir. Çarpışan iki nesneyi ayırmak için basit bir uygulama şöyle görünür:

```lua
function on_message(self, message_id, message, sender)
  -- Handle collision
  if message_id == hash("contact_point_response") then
    local newpos = go.get_position() + message.normal * message.distance
    go.set_position(newpos)
  end
end
```

Bu kod, kinematik nesnenizi iç içe geçtiği diğer fizik nesnelerinden ayırır; ancak ayırma işlemi çoğu zaman gerekenin ötesine geçer ve birçok durumda titreme görürsünüz. Sorunu daha iyi anlamak için oyuncu karakterinin *A* ve *B* adlı iki nesneyle çarpıştığı aşağıdaki durumu ele alın:

![Fizik çarpışması](images/physics/collision_multi.png)

Fizik motoru, çarpışmanın gerçekleştiği karede biri *A* nesnesi, diğeri *B* nesnesi için olmak üzere birden fazla `"contact_point_response"` iletisi gönderir. Karakteri yukarıdaki basit kodda olduğu gibi her iç içe geçmeye tepki olarak hareket ettirirseniz ayırma işlemi şöyle gerçekleşir:

- Karakteri, iç içe geçme mesafesine (penetration distance) göre *A* nesnesinin dışına çıkarın (siyah ok)
- Karakteri, iç içe geçme mesafesine göre *B* nesnesinin dışına çıkarın (siyah ok)

Bunların sırası değişebilir, ancak her iki durumda da sonuç aynıdır: toplam ayırma, *tek tek iç içe geçme vektörlerinin toplamına* eşittir:

![Basit fizik ayırma işlemi](images/physics/separation_naive.png)

Karakteri *A* ve *B* nesnelerinden doğru şekilde ayırmak için her temas noktasının (contact point) iç içe geçme mesafesini ele almanız ve önceki ayırma işlemlerinin gerekli ayrılmayı zaten tamamen veya kısmen sağlayıp sağlamadığını kontrol etmeniz gerekir.

İlk temas noktası iletisinin *A* nesnesinden geldiğini ve karakteri *A* nesnesinin iç içe geçme vektörü kadar hareket ettirerek dışarı çıkardığınızı varsayın:

![Fizik ayırma işleminin 1. adımı](images/physics/separation_step1.png)

Bu durumda karakter, *B* nesnesinden de kısmen ayrılmış olur. *B* nesnesinden tamamen ayrılmak için gereken son telafi, yukarıdaki siyah okla gösterilmiştir. Telafi vektörünün uzunluğu, *A* nesnesinin iç içe geçme vektörünün *B* nesnesinin iç içe geçme vektörü üzerine izdüşümü (projection) alınarak hesaplanabilir:

![İzdüşüm](images/physics/projection.png)

```
l = vmath.project(A, B) * vmath.length(B)
```

Telafi vektörü, *B* vektörünün uzunluğu *l* kadar azaltılarak bulunabilir. Bunu herhangi bir sayıda iç içe geçme için hesaplamak üzere, uzunluğu sıfır olan bir düzeltme vektörüyle başlayıp her temas noktası için şu adımları uygulayarak gerekli düzeltmeyi bir vektörde biriktirebilirsiniz:

1. Geçerli düzeltmenin, temasın iç içe geçme vektörü üzerine izdüşümünü alın.
2. İç içe geçme vektöründen geriye ne kadar telafi kaldığını hesaplayın (yukarıdaki formüle göre).
3. Nesneyi telafi vektörü kadar hareket ettirin.
4. Telafiyi biriktirilen düzeltmeye ekleyin.

Tam bir uygulama şöyle görünür:

```lua
function init(self)
  -- correction vector
  self.correction = vmath.vector3()
end

function update(self, dt)
  -- reset correction
  self.correction = vmath.vector3()
end

function on_message(self, message_id, message, sender)
  -- Handle collision
  if message_id == hash("contact_point_response") then
    -- Get the info needed to move out of collision. We might
    -- get several contact points back and have to calculate
    -- how to move out of all of them by accumulating a
    -- correction vector for this frame:
    if message.distance > 0 then
      -- First, project the accumulated correction onto
      -- the penetration vector
      local proj = vmath.project(self.correction, message.normal * message.distance)
      if proj < 1 then
        -- Only care for projections that does not overshoot.
        local comp = (message.distance - message.distance * proj) * message.normal
        -- Apply compensation
        go.set_position(go.get_position() + comp)
        -- Accumulate correction done
        self.correction = self.correction + comp
      end
    end
  end
end
```
