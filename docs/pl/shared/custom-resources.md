Zasoby niestandardowe są dołączane do głównego archiwum gry za pomocą pola [*Custom Resources*](https://defold.com/manuals/project-settings/#custom-resources) w pliku *game.project*.

Pole *Custom Resources* powinno zawierać listę zasobów rozdzielonych przecinkami, które zostaną uwzględnione w głównym archiwum gry. Jeśli podasz katalogi, wszystkie pliki i katalogi w danym katalogu zostaną dołączone rekurencyjnie. Pliki możesz odczytywać za pomocą [`sys.load_resource()`](/ref/sys/#sys.load_resource).
