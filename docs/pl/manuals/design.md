---
title: Założenia projektowe Defold
brief: Filozofia stojąca za założeniami projektowymi Defold.
---

# Założenia projektowe Defold

Defold powstał z myślą o następujących celach:

- Ma być kompletną, profesjonalną platformą produkcyjną, czyli gotowym rozwiązaniem dla zespołów tworzących gry.
- Ma być prosty i przejrzysty oraz dostarczać jednoznacznych rozwiązań typowych problemów architektonicznych i organizacyjnych występujących podczas tworzenia gier.
- Ma być bardzo szybką platformą deweloperską, idealną do iteracyjnego tworzenia gier.
- Ma zapewniać wysoką wydajność w czasie działania.
- Ma być naprawdę wieloplatformowy.

Projekt edytora i silnika został starannie dopracowany tak, aby osiągnąć te cele. Niektóre z naszych decyzji projektowych różnią się od tego, do czego możesz być przyzwyczajony, jeśli masz doświadczenie z innymi platformami. Na przykład:

- Wymagamy statycznego deklarowania drzewa zasobów oraz całego nazewnictwa. Wymaga to od Ciebie pewnego początkowego wysiłku, ale w dłuższej perspektywie bardzo usprawnia proces tworzenia.
- Zachęcamy do przekazywania wiadomości między prostymi, zamkniętymi w sobie jednostkami.
- Nie ma dziedziczenia zorientowanego obiektowo.
- Nasze API są asynchroniczne.
- Potok renderowania (ang. rendering pipeline) jest sterowany kodem i w pełni konfigurowalny.
- Wszystkie pliki zasobów mają proste, tekstowe formaty, optymalnie przygotowane zarówno do scalania w Git, jak i do importu oraz przetwarzania za pomocą zewnętrznych narzędzi.
- Zasoby można zmieniać i szybko przeładowywać (ang. hot reload) w działającej grze, co pozwala na niezwykle szybkie iterowanie i eksperymentowanie.
