## Dokuz parçalı ölçekleme ile doku kaplama

GUI kutu düğümleri (box nodes) ve sprite bileşenleri (sprite components) bazen boyutları bağlama göre değişen öğeler içerir: içeriklerine uyacak şekilde yeniden boyutlandırılması gereken paneller ve iletişim kutuları ya da bir düşmanın kalan sağlığını gösterecek şekilde yeniden boyutlandırılması gereken bir sağlık çubuğu. Yeniden boyutlandırılan düğüme veya sprite bileşenine doku (texture) uyguladığınızda bu durum görsel sorunlara yol açabilir.

Motor normalde dokuyu dikdörtgen sınırlarına sığacak şekilde ölçekler, ancak dokuz parçalı ölçekleme (slice-9) için kenar alanları tanımlayarak dokunun hangi bölümlerinin ölçekleneceğini sınırlayabilirsiniz:

![GUI ölçekleme](../shared/images/gui_slice9_scaling.png)

*Slice9* kutu düğümü, normal biçimde ölçeklenmemesi gereken sol, üst, sağ ve alt kenar boşluklarının piksel sayısını belirten 4 sayıdan oluşur:

![Dokuz parçalı ölçekleme özellikleri](../shared/images/gui_slice9_properties.png)

Kenar boşlukları, sol kenardan başlayarak saat yönünde ayarlanır:

![Dokuz parçalı ölçekleme bölümleri](../shared/images/gui_slice9.png)

- Köşe parçaları hiçbir zaman ölçeklenmez.
- Kenar parçaları tek bir eksen boyunca ölçeklenir. Sol ve sağ kenar parçaları dikey olarak ölçeklenir. Üst ve alt kenar parçaları yatay olarak ölçeklenir.
- Merkezdeki doku alanı gerektiği gibi yatay ve dikey olarak ölçeklenir.

Yukarıda açıklanan *Slice9* doku ölçeklemesi yalnızca kutu düğümünün veya sprite bileşeninin boyutunu değiştirdiğinizde uygulanır:

![GUI kutu düğümü boyutu](../shared/images/gui_slice9_size.png)

![Sprite bileşeni boyutu](../shared/images/sprite_slice9_size.png)

::: important
Kutu düğümünün, sprite bileşeninin veya oyun nesnesinin (game object) ölçek parametresini değiştirirseniz düğüm veya sprite bileşeni ile doku, *Slice9* parametreleri uygulanmadan ölçeklenir.
:::

::: important
Sprite bileşenlerinde dokuz parçalı ölçekleme ile doku kaplama kullanırken [görüntünün Sprite Trim Mode ayarı](https://defold.com/manuals/atlas/#image-properties) Off olarak ayarlanmalıdır.
:::


### Mipmapler ve dokuz parçalı ölçekleme
Grafik işleyicisinde (renderer) mipmap kullanımının çalışma biçimi nedeniyle, doku parçaları ölçeklenirken bazen görüntü kusurları oluşabilir. Bu durum, parçaları özgün doku boyutunun altına _küçülttüğünüzde_ ortaya çıkar. İşleyici bu durumda parça için daha düşük çözünürlüklü bir mipmap seçer ve bu da görüntü kusurlarına neden olur.

![Dokuz parçalı ölçeklemede mipmap kullanımı](../shared/images/gui_slice9_mipmap.png)

Bu sorunu önlemek için dokunun ölçeklenecek parçalarının, hiçbir zaman küçültülmeyip yalnızca büyütülecek kadar küçük olduğundan emin olun.
