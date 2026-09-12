## Bileşen sayısı üst sınırı optimizasyonları {#component-max-count-optimizations}
*game.project* ayar dosyası, belirli bir kaynak (resource) türünden aynı anda en fazla kaç tane bulunabileceğini belirten birçok değer içerir. Bu sayılar genellikle yüklenen her koleksiyon (collection; dünya olarak da adlandırılır) için ayrı hesaplanır. Defold motoru, oyun çalışırken dinamik bellek ayırmayı ve bellek parçalanmasını önlemek için bu üst sınır değerlerini kullanarak gereken belleği önceden ayırır.

Defold'da bileşenleri (component) ve diğer kaynakları temsil etmek için kullanılan veri yapıları, mümkün olduğunca az bellek kullanacak şekilde optimize edilmiştir. Yine de gerçekten gerekenden fazla bellek ayırmamak için bu değerleri belirlerken dikkatli olunmalıdır.

Bellek kullanımını daha da optimize etmek için Defold'un proje derleme süreci oyunun içeriğini analiz eder ve tam sayının kesin olarak bilinebildiği durumlarda sayı üst sınırlarını geçersiz kılarak bu sayıyı kullanır:

* Bir koleksiyon hiçbir fabrika (factory) bileşeni içermiyorsa her bileşen ve oyun nesnesi (game object) için tam olarak gereken miktarda bellek ayrılır ve sayı üst sınırı değerleri yok sayılır.
* Bir koleksiyon fabrika bileşeni içeriyorsa çalışma sırasında oluşturulan nesneler analiz edilir ve fabrikalardan oluşturulabilecek bileşenler ile oyun nesneleri için sayı üst sınırı kullanılır.
* Bir koleksiyon, "Dynamic Prototype" seçeneği etkinleştirilmiş bir fabrika veya koleksiyon fabrikası (collection factory) içeriyorsa bu koleksiyon sayı üst sınırı değerlerini kullanır.
