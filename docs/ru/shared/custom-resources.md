Custom resources упаковываются в основной архив игры с помощью поля [*Custom Resources*](https://defold.com/manuals/project-settings/#custom-resources) в *game.project*.

Поле *Custom Resources* должно содержать список ресурсов, разделённых запятыми, которые будут включены в основной архив игры. Если указаны каталоги, все файлы и папки в этих каталогах будут включены рекурсивно. Читать эти файлы можно с помощью [`sys.load_resource()`](/ref/sys/#sys.load_resource).
