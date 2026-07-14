---
title: Importowanie modeli
brief: Ta instrukcja opisuje, jak importować modele 3D używane przez komponent Model.
---

# Importowanie modeli 3D
Defold obsługuje modele, szkielety i animacje w formacie glTF 2.0 (GL Transmission Format). Do modeli 3D używaj plików *.gltf* lub *.glb*. glTF to nowoczesny format przeznaczony do przenoszenia i ładowania danych 3D w silnikach gier i aplikacjach czasu rzeczywistego.

Możesz użyć narzędzi takich jak Maya, 3ds Max, SketchUp i Blender do tworzenia modeli 3D albo konwertowania ich do formatu glTF.

Blender to potężny i popularny program do modelowania 3D, animacji i renderowania. Działa w systemach Windows, macOS i Linux i jest dostępny za darmo na stronie [https://www.blender.org](https://www.blender.org).

![Model w Blenderze](images/model/blender_gltf.png)

## Importowanie do Defold
Aby zaimportować model, przeciągnij i upuść plik *.gltf* lub *.glb* do panelu *Assets* edytora Defold.

glTF może być przechowywany na dwa popularne sposoby:

* *.glb* to pojedynczy plik binarny. Zawiera dane modelu i może też zawierać spakowane obrazy tekstur. Jest wygodny, gdy chcesz przenosić lub przechowywać model jako jeden plik.
* *.gltf* to tekstowy plik JSON. Zwykle odwołuje się do osobnego pliku *.bin* z danymi siatki oraz osobnych obrazów tekstur, takich jak *.png* lub *.jpg*. Przy tym wariancie dodaj wszystkie powiązane pliki do projektu i zachowaj ich względne ścieżki.

Jeśli model ma używać tekstury w Defold, zaimportuj obraz tekstury jako osobny zasób. Nawet gdy źródłowy plik glTF/GLB zawiera osadzone obrazy, tekstury trzeba przypisać do komponentu Model przez właściwości tekstur materiału komponentu.

![Zaimportowane zasoby modelu](images/model/assets_gltf.png)

::: sidenote
Począwszy od Defold 1.13.0, Defold zachowuje pozycje i transformacje z importowanego pliku glTF i nie wyśrodkowuje automatycznie modelu podczas importu. Podgląd w edytorze i środowisko uruchomieniowe używają importowanych transformacji w spójny sposób: siatki ze skinningiem lub powiązane z kośćmi zachowują transformacje lokalne względem szkieletu, a siatki sztywne zachowują spłaszczone położenie w przestrzeni świata.

Jeśli model utworzony w starszej wersji Defold zmieni pozycję lub orientację po ponownym zaimportowaniu, popraw transformację w Blenderze lub innym narzędziu autorskim, a następnie ponownie wyeksportuj plik *.gltf* lub *.glb*.
:::

## Używanie modelu
Po zaimportowaniu modelu użyj go w [komponencie Model](/manuals/model):

1. Utwórz plik Model z panelu *Assets* za pomocą <kbd>New... ▸ Model</kbd>, albo dodaj komponent Model bezpośrednio do obiektu gry za pomocą <kbd>Add Component ▸ Model</kbd>.
2. Ustaw właściwość *Mesh* na zaimportowany plik *.gltf* lub *.glb* zawierający siatkę.
3. W przypadku modelu animowanego ustaw właściwość *Skeleton* na plik *.gltf* lub *.glb* zawierający szkielet. Często jest to ten sam plik, którego używasz dla *Mesh*, gdy siatka, szkielet i animacje są eksportowane razem.
4. Utwórz plik *Animation Set* dla animacji i przypisz go do właściwości *Animations*. Ustaw *Default Animation*, jeśli animacja ma rozpocząć się automatycznie.
5. Ustaw właściwość *Material* na materiał odpowiedni dla modelu. Wbudowane pliki *model.material*, *model_instanced.material*, *model_skinned.material* i *model_skinned_instanced.material* są przydatnymi punktami wyjścia. Materiały dla modeli ze skinningiem używają lokalnej przestrzeni wierzchołków, aby skinning mógł być wykonywany na GPU; niestandardowe materiały dla modeli ze skinningiem GPU lub instancjonowanych również powinny używać lokalnej przestrzeni wierzchołków. Wymagania dotyczące adaptera graficznego opisano w [instrukcji Model](/manuals/model/#material).
6. Ustaw właściwości tekstur materiału, takie jak *Texture*, na zaimportowane pliki obrazów tekstur. Jeśli materiał używa wielu tekstur, przypisz każdą teksturę w odpowiednim polu tekstury materiału.


## Eksport do glTF
Wyeksportowany plik *.gltf* lub *.glb* zawiera wszystkie wierzchołki, krawędzie i ściany tworzące model, a także _współrzędne UV_ (czyli informację o tym, która część obrazu tekstury odpowiada konkretnej części siatki), jeśli zostały zdefiniowane, kości w szkielecie oraz dane animacji.

* Szczegółowy opis siatek wielokątnych można znaleźć na stronie http://en.wikipedia.org/wiki/Polygon_mesh.

* Współrzędne UV i mapowanie UV opisano na stronie http://en.wikipedia.org/wiki/UV_mapping.

Defold nakłada pewne ograniczenia na eksportowane dane animacji:

* Defold obecnie obsługuje tylko animacje wypieczone. Animacje muszą mieć macierze dla każdej animowanej kości w każdej klatce kluczowej, a nie osobne klucze pozycji, rotacji i skali.

* Animacje są również interpolowane liniowo. Jeśli używasz bardziej zaawansowanej interpolacji krzywych, animacje muszą zostać wstępnie wypieczone przez eksporter.

### Wymagania
Podczas eksportu modelu pamiętaj, że obsługa glTF może różnić się między narzędziami i silnikami. Używaj glTF 2.0, upewnij się, że model ma poprawne współrzędne UV, jeśli używa tekstur, i importuj obrazy tekstur osobno, gdy mają być przypisane do komponentu Model.

Naszym celem jest pełna obsługa formatu glTF, ale nie jesteśmy jeszcze w tym miejscu.
Jeśli brakuje jakiejś funkcji, zgłoś prośbę o jej dodanie w [naszym repozytorium](https://github.com/defold/defold/issues)

### Eksport tekstury
Jeśli nie masz jeszcze tekstury dla swojego modelu, możesz użyć Blendera do wygenerowania tekstury. Zrób to, zanim usuniesz dodatkowe materiały z modelu. Zacznij od zaznaczenia siatki i wszystkich jej wierzchołków:

![Zaznacz wszystkie](images/model/blender_select_all_vertices.png)

Gdy wszystkie wierzchołki są zaznaczone, rozwiń siatkę, aby uzyskać układ UV:

![Rozwiń siatkę](images/model/blender_unwrap_mesh.png)

Następnie możesz wyeksportować układ UV do obrazu, którego można użyć jako tekstury:

![Eksport układu UV](images/model/blender_export_uv_layout.png)

![Wynik eksportu układu UV](images/model/blender_export_uv_layout_result.png)

### Eksportowanie w Blenderze
Eksportuj model z Blendera za pomocą <kbd>File ▸ Export ▸ glTF 2.0 (.glb/.gltf)</kbd>.

![Eksportowanie w Blenderze](images/model/export_gltf.png)

Zaznacz obiekt lub obiekty przed eksportem i włącz *Selected Objects*, jeśli chcesz wyeksportować tylko zaznaczenie.

Wybierz jedną z opcji *Format*:

* *glTF Binary (.glb)* tworzy jeden plik. Użyj tej opcji, gdy model ma być łatwy do przenoszenia lub przechowywania jako pojedynczy zasób.
* *glTF Separate (.gltf + .bin + textures)* tworzy osobne pliki dla opisu modelu, danych binarnych i tekstur. Użyj tej opcji, gdy chcesz edytować obrazy tekstur albo przypisywać je osobno w Defold.

Jeśli model zawiera animacje, włącz eksport animacji i upewnij się, że animacje są wypieczone. Jeśli model używa tekstur, upewnij się, że siatka ma rozwinięcie UV i że obrazy tekstur są eksportowane w formacie, który Defold może importować, takim jak PNG lub JPEG.

![Eksportowanie w Blenderze](images/model/export_settings.png)
