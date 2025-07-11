---
title: Кэширование ассетов
brief: В этом руководстве объясняется, как использовать кэш ассетов для ускорения сборки.
---

# Кэширование ассетов

Игры, созданные с помощью Defold, обычно собираются за несколько секунд, но по мере роста проекта увеличивается и количество ассетов. Компиляция шрифтов и сжатие текстур могут занимать значительное время в большом проекте, поэтому кэш ассетов существует для ускорения сборки, перестраивая только те ассеты, которые изменились, и используя уже скомпилированные ассеты из кэша для неизмененных активов.

Defold использует трехуровневый кэш:

1. Проектный кэш
2. Локальный кэш
3. Удаленный кэш


## Проектный кэш

По умолчанию Defold будет кэшировать скомпилированные ассеты в папке `build/default` проекта Defold. Кэш проекта ускоряет последующие сборки, так как перекомпилировать нужно только измененные ассеты, а ассеты без изменений будут использоваться из кэша проекта. Этот кэш всегда включен и используется как редактором, так и инструментами командной строки.

Кэш проекта можно удалить вручную, удалив файлы в `build/default` или выполнив команду `clean` из [командной строки сборщика Bob](/manuals/bob).


## Локальный кэш

Добавлен в Defold 1.2.187

Локальный кэш - это дополнительный второй кэш, в котором скомпилированные ассеты хранятся во внешнем файловом месте на той же машине или на сетевом диске. Благодаря внешнему расположению, содержимое кэша сохраняется при очистке кэша проекта. Он также может быть общим для нескольких разработчиков, работающих над одним проектом. В настоящее время кэш доступен только при сборке с помощью инструментов командной строки. Он включается с помощью опции `resource-cache-local`:

```sh
java -jar bob.jar --resource-cache-local /Users/john.doe/defold_local_cache
```

Доступ к скомпилированным ассетам из локального кэша осуществляется на основе вычисленной контрольной суммы, которая учитывает версию движка Defold, имена и содержимое исходных ассетов, а также параметры сборки проекта. Это гарантирует уникальность кэшированных активов и возможность совместного использования кэша несколькими версиями Defold.

::: sidenote
Файлы, хранящиеся в локальном кэше, хранятся неограниченное время. Разработчик должен вручную удалять старые/неиспользуемые файлы.
:::


## Удаленный кэш

Добавлен в Defold 1.2.187

Удаленный кэш - это дополнительный третий кэш, в котором скомпилированные ассеты хранятся на сервере, а доступ к ним осуществляется через HTTP-запрос. В настоящее время кэш доступен только при сборке с помощью инструментов командной строки. Он включается с помощью опции `resource-cache-remote`:

```sh
java -jar bob.jar --resource-cache-remote http://192.168.0.100/
```

Как и в случае с локальным кэшем, доступ ко всем активам из удаленного кэша осуществляется на основе вычисленной контрольной суммы. Доступ к кэшированным активам осуществляется с помощью методов HTTP-запросов GET, PUT и HEAD. Defold не предоставляет сервер удаленного кэша. Разработчик должен настроить его самостоятельно. Пример [базового Python-сервера можно посмотреть здесь](https://github.com/britzl/httpserver-python).
