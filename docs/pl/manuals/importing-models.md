---
title: Importowanie modeli 3D
brief: Ta instrukcja opisuje ze szczegółami jak importować i edytować modele 3D.
---

# Importowanie modeli 3D
Defold obecnie wspiera modele, szkielety i animacje w formacie GL Transmission Format *.glTF* oraz *Collada *.dae*. Możesz używać narzędzi takich jak Maya, 3D Max, Sketchup czy Blender do tworzenia i/lub konwertowania modeli trójwymiarowych do formatu glTF i Collada. Blender jest jednym z popularniejszych i potężnych narzędzi do modelowania 3D, animacji, a nawet renderowania. Działa na systemach operacyjnych Windows, macOS i Linux i jest dostępny za darmo do pobrania ze strony http://www.blender.org

![Model w Blenderze](images/model/blender.png)

## Importowanie do Defolda
Aby zaimportować model 3D do Defold, przeciągnij i upuść plik *.gltf* lub *.dae* oraz odpowiednie obrazy tekstur w dowolnej lokalizacji w panelu *Assets*.

![Importowanie](images/model/assets.png)

## Używanie Modeli
Kiedy model został zaimportowany do Defolda możesz go użyć jako [komponent typu Model](/manuals/model).

## Exportowanie do formatu glTF i Collada
Kiedy eksportujesz model 3D do formatu glTF lub Collada, otrzymujesz plik z rozszerzeniem *.gltf* lub *.dae*. Plik ten zawiera wszystkie informacje o wierzchołkach (ang. vertices), krawędziach i teksturach (ang. faces), które składają się na model trójwymiarowy, a także współrzędne UV (ang. _UV coordinates_) (które, w skrócie, przypisują daną część tekstury do siatki modelu) jeśli zostały zdefiniowane, kości szkieletu i dane o animacji.

* Szczegółowy opisy wielokątów (ang. polygons) siatki możesz znaleźć na stronie (https://pl.wikipedia.org/wiki/Siatka_(grafika_3D))[https://pl.wikipedia.org/wiki/Siatka_(grafika_3D)].

* Współrzędne UV i mapowanie UV opisane jest na stronie (http://en.wikipedia.org/wiki/UV_mapping)[http://en.wikipedia.org/wiki/UV_mapping].

Defold nakłada pewne ograniczenia na eksportowane dane o animacji:

* Defold obecnie wspiera tylko wypiekane animacje (ang. baked animations). Animacje muszą posiadać macierze dla każdej ramki animacji szkieletowej, a nie pozycję, rotację i skalę w osobnych kluczach.

* Animacje są interpolowane liniowo. Jeśli tworzysz bardziej zaawansowaną krzywą interpolacji animacje muszę być wypiekane przed eksportowaniem (prebaked).

* Klipy animacji (ang. animation clips) w formacie Collada nie są wspierane. W celu używania wielu animacji dla modelu wyeksportuj je do osobnych plików *.dae* i zbierz je w zasób *.animationset* w edytorze Defold.

### Wymagania
Kiedy eksportujesz model do formatu Collada musisz zapewnić spełnienie poniższych wymagań:

* Model musi zawierać pojedynczą siatkę (ang. mesh)
* Model musi używać jednego materiału
* Wyeksportowany plik *.gltf* musi używać wbudowanych danych o siatce trójwymiarowej (embedded mesh data). Dane w osobnych plikach binarnych nie są wspierane.

#### Łączenie wielu siatek
Możesz użyć np. Blendera do połączenia wielu siatek. Wybierz wszystkie siatki i naciśnij `CTRL`/`CMD` + `J`.

![Łączenie siatek](images/model/blender_join_meshes.png)

#### Usuwanie materiałów
Możesz użyć np. Blendera do usunięcia dodatkowych materiałó z modeli. Wybierz dany materiał i naciśnij `-`.

![Usuwanie materiałów](images/model/blender_remove_materials.png)


#### Exportowanie tekstur
Jeśli nie masz jeszcze gotowej tekstury dla modelu, możesz użyć np. Blendera do wygenerowania tekstury. Powinno się to uczynić przed usunięciem materiałów z modelu. Najpierw wybierz siatkę i wszystkie jej wierzchołki:

![Wybierz wszystkie](images/model/blender_select_all_vertices.png)

Kiedy wszystkie wierzchołki są wybrane, rozwiń (ang. unwrap) siatkę, żeby otrzymać rozkład (ang. layout) UV:

![Rozwiń siatkę](images/model/blender_unwrap_mesh.png)

Następnie możesz wyeksportować rozkład UV do pliku graficznego, który później można używać jako teksturę:

![Eksportuj rozkład UV](images/model/blender_export_uv_layout.png)

![Eksportuj ustawienia rozkładu - UV layout settings](images/model/blender_export_uv_layout_settings.png)

![Eksportuj rozkład - UV layout result](images/model/blender_export_uv_layout_result.png)


## Exportowanie używając Blendera
Możesz eksportować modele do formatu Collada używając opcji Export z menu w Blenderze. Wybierz dany model, wybierz opcję Export i zaznacz opcję "Selection Only".

![Exportowanie używając Blendera](images/model/blender_export.png)
