---
title: Optymalizacja zużycia pamięci gry w silniku Defold
brief: Ta instrukcja opisuje, jak optymalizować zużycie pamięci gry w silniku Defold.
---

# Optymalizacja zużycia pamięci

## Kompresja tekstur
Korzystanie z kompresji tekstur nie tylko zmniejszy rozmiar zasobów w archiwum gry, ale skompresowane tekstury mogą też ograniczyć ilość pamięci GPU potrzebnej do ich przechowywania.

## Dynamiczne wczytywanie
Większość gier ma przynajmniej część zawartości, z której korzysta się rzadko. Z punktu widzenia zużycia pamięci nie ma sensu, aby taka zawartość była wczytana przez cały czas. Lepiej wczytywać ją i zwalniać wtedy, gdy jest potrzebna. To oczywiście oznacza kompromis między natychmiastową dostępnością a kosztem pamięci w czasie działania oraz kosztem czasu wczytywania.

Defold oferuje kilka sposobów dynamicznego wczytywania zawartości:

* [Pełnomocniki kolekcji](/manuals/collection-proxy/)
* [Dynamiczne fabryki kolekcji](/manuals/collection-factory/#dynamic-loading-of-factory-resources)
* [Dynamiczne fabryki](/manuals/factory/#dynamic-loading-of-factory-resources)
* [Live Update](/manuals/live-update/)

## Optymalizacja liczników komponentów
Defold przydziela pamięć dla komponentów i zasobów jednorazowo podczas tworzenia kolekcji, aby ograniczyć fragmentację pamięci. Ilość przydzielanej pamięci zależy od konfiguracji różnych liczników komponentów w pliku *game.project*. Użyj [profilera](/manuals/profiling/), aby uzyskać dokładne dane o użyciu komponentów i zasobów, a następnie skonfiguruj grę tak, by korzystała z wartości maksymalnych bliższych rzeczywistej liczbie komponentów i zasobów. Zmniejszy to ilość pamięci używanej przez grę (zobacz informacje o [optymalizacji liczników maksymalnych komponentów](/manuals/project-settings/#component-max-count-optimizations)).

## Optymalizacja liczby węzłów GUI
Optymalizuj liczbę węzłów GUI, ustawiając maksymalną liczbę węzłów w pliku GUI tylko na tyle, ile jest potrzebne. Pole `Current Nodes` w [właściwościach komponentu GUI](https://defold.com/manuals/gui/#gui-properties) pokazuje liczbę węzłów używanych przez komponent GUI.

:[Optymalizacje HTML5](../shared/optimization-memory-html5.md)
