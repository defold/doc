## Optimizaciones de max count de componentes {#component-max-count-optimizations}
El archivo de configuración *game.project* contiene muchos valores que especifican la cantidad máxima de un recurso determinado que puede existir al mismo tiempo, a menudo contada por colección cargada (también llamada mundo). El motor Defold usará estos valores máximos para preasignar la memoria necesaria para esa cantidad, y así evitar asignaciones dinámicas y fragmentación de memoria mientras el juego se ejecuta.

Las estructuras de datos de Defold usadas para representar componentes y otros recursos están optimizadas para usar la menor cantidad de memoria posible, pero aun así se debe tener cuidado al definir los valores para evitar asignar más memoria de la realmente necesaria.

Para optimizar aún más el uso de memoria, el proceso de build de Defold analizará el contenido del juego y sobrescribirá los max counts si es posible conocer con certeza la cantidad exacta:

* Si una colección no contiene componentes factory, se asignará la cantidad exacta de cada componente y Game Object, y se ignorarán los valores de max count.
* Si una colección contiene un componente factory, se analizarán los objetos generados y se usará el max count para los componentes que puedan generarse desde las factories y para los Game Objects.
* Si una colección contiene una factory o una factory de colección con la opción "Dynamic Prototype" activada, esta colección usará los contadores máximos.
