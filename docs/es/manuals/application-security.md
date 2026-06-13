---
title: Manual de seguridad de aplicaciones
brief: Este manual cubre varias áreas relacionadas con prácticas de desarrollo seguro.
---

# Seguridad de aplicaciones

La seguridad de aplicaciones es un tema amplio que abarca desde prácticas de desarrollo seguro hasta la protección del contenido de tu juego después de su lanzamiento. Este manual cubre varias áreas y las pone en el contexto de la seguridad de aplicaciones al usar el motor, las herramientas y los servicios de Defold:

* Protección de propiedad intelectual
* Soluciones anti-cheat
* Comunicación de red segura
* Uso de software de terceros
* Uso de servidores de build en la nube
* Contenido descargable


## Proteger tu propiedad intelectual contra el robo
Una preocupación común para la mayoría de los desarrolladores es cómo proteger sus creaciones contra el robo. Desde un punto de vista legal, los derechos de autor, las patentes y las marcas comerciales pueden usarse para proteger los distintos aspectos de la propiedad intelectual de los videojuegos. Los derechos de autor dan a su titular el derecho exclusivo a distribuir la obra creativa, las patentes protegen las invenciones y las marcas comerciales protegen nombres, símbolos y logos.

También puede ser deseable tomar precauciones técnicas para proteger la obra creativa de un juego. Sin embargo, es importante tener en cuenta que, una vez que el juego está en manos del jugador, es posible encontrar formas de extraer los assets. Esto se puede lograr mediante ingeniería inversa de la aplicación y los archivos del juego, pero también usando herramientas para extraer texturas y modelos cuando se envían a la GPU o cuando otros assets se cargan en memoria.

Por esta razón, nuestra postura general es que si los usuarios están decididos a extraer los assets de un juego, podrán hacerlo.

Los desarrolladores pueden agregar su propia protección para hacer más difícil, __pero no imposible__, extraer los assets. Esto normalmente incluye varios métodos de cifrado y ofuscación para proteger y ocultar assets del juego.

### Ofuscación del código fuente
Aplicar ofuscación del código fuente es un proceso automatizado en el que el código fuente se vuelve deliberadamente difícil de entender para las personas, sin afectar la salida del programa. El propósito suele ser proteger contra el robo, pero también dificultar las trampas.

Es posible aplicar ofuscación del código fuente en Defold como un paso de prebuild o como parte integrada del proceso de build de Defold. Con la ofuscación prebuild, el código fuente se ofusca mediante una herramienta de ofuscación antes de iniciar el proceso de build de Defold.

La ofuscación durante la build, por otro lado, se integra en el proceso de build usando un plugin builder de Lua. Un plugin builder de Lua toma el código fuente sin procesar como entrada y devuelve una versión ofuscada del código fuente como salida. Un ejemplo de ofuscación durante la build se muestra en la [extensión Prometheus](https://github.com/defold/extension-prometheus), basada en el ofuscador de Lua Prometheus disponible en GitHub. Abajo encontrarás un ejemplo de uso de Prometheus para ofuscar agresivamente un fragmento de código (ten en cuenta que este tipo de ofuscación pesada tendrá un impacto en el rendimiento en runtime del código Lua):

Ejemplo:

```
function init(self)
 print("hello")
 test.greet("Bob")
end
```

Salida ofuscada:

```
local v={"+qdW","ZK0tEKf=";"XP/IX3+="}for o,J in ipairs({{1;3};{1,1},{2,3}})do while J[1]<J[2]do v[J[1]],v[J[2]],J[1],J[2]=v[J[2]],v[J[1]],J[1]+1,J[2]-1 end end local function J(o)return v[o+45816]end do local o={["/"]=9;["8"]=48;["9"]=1;q=38,o=62;V=33;y=43,d=61,B=50,L=54;v=2;["0"]=21,n=31;p=63;R=5;N=3;i=10;e=35;C=7;l=56;a=47,J=58;m=59;["2"]=36;z=11;M=12;Z=26;O=18;["5"]=20;s=8,["4"]=30,P=55;w=4;U=29;Q=28;r=24,h=41;G=45;c=19;W=34,k=57;T=14,t=44,S=0;f=60;F=42,E=27;u=40;X=25,j=17;["3"]=23,b=13;["1"]=53;Y=32,A=22,K=6,["+"]=16,["6"]=46;["7"]=51;I=37;D=52;H=15,x=49,g=39}local J=type local x=string.sub local d=v local l=string.len local W=string.char local L=table.insert local w=table.concat local h=math.floor for v=1,#d,1 do local X=d[v]if J(X)=="string"then local J=l(X)local H={}local S=1 local k=0 local K=0 while S<=J do local v=x(X,S,S)local d=o[v]if d then k=k+d*64^(3-K)K=K+1 if K==4 then K=0 local o=h(k/65536)local v=h((k%65536)/256)local J=k%256 L(H,W(o,v,J))k=0 end elseif v=="="then L(H,W(h(k/65536)))if S>=J or x(X,S+1,S+1)~="="then L(H,W(h((k%65536)/256)))end break end S=S+1 end d[v]=w(H)end end end local function o(o)test[J(-45815)](o)end function init(v)print(J(-45813))o(J(-45814))end
```

### Cifrado de recursos
Durante el proceso de build de Defold, los recursos del juego se procesan y se transforman en formatos adecuados para su consumo en runtime por parte del motor Defold. Las texturas se compilan al formato Basis Universal, las colecciones, los objetos de juego y los componentes se convierten de una representación de texto legible por humanos a sus equivalentes binarios, y el código fuente Lua se procesa y se compila a bytecode. Otros assets, como los archivos de sonido, se usan tal cual.

Cuando este proceso se completa, los assets se agregan al archivo del juego, uno por uno. El archivo del juego es un archivo binario grande, y la ubicación de cada recurso dentro de él se almacena en un archivo de índice asociado. El formato está documentado [aquí](https://github.com/defold/defold/blob/dev/engine/docs/ARCHIVE_FORMAT.md).

Antes de que los archivos fuente Lua se agreguen al archivo, también se cifran de forma opcional. El cifrado predeterminado proporcionado en Defold es un cifrado de bloque simple que se usa para evitar que los strings del código sean visibles de inmediato si el archivo del juego se inspecciona con una herramienta de visualización de archivos binarios. No debe considerarse criptográficamente seguro, ya que el código fuente de Defold está disponible en GitHub con la clave de cifrado visible en el código fuente.

Es posible agregar cifrado personalizado a los archivos fuente Lua implementando un plugin de cifrado de recursos (Resource encryption plugin). Un plugin de cifrado de recursos consta de una parte de tiempo de build para cifrar recursos como parte del proceso de build y una parte de runtime para descifrar recursos cuando se leen desde el archivo del juego. Un plugin básico de cifrado de recursos (Resource Encryption plugin) que puedes usar como punto de partida para tu propio cifrado está [disponible en GitHub](https://github.com/defold/extension-resource-encryption).


### Codificación de valores de configuración del proyecto
El archivo *game.project* se incluirá tal cual en el bundle de tu aplicación. A veces puedes querer almacenar claves de acceso a API públicas o valores similares, que son de naturaleza sensible, aunque quizá no privada. Para reforzar la seguridad de esos valores, pueden incluirse en el binario de la aplicación, en lugar de almacenarse en *game.project*, y seguir siendo accesibles para funciones de la API de Defold como `sys.get_config_string()` y funciones similares. Puedes hacerlo agregando una extensión nativa en tu *game.project* y usando la macro `DM_DECLARE_CONFIGFILE_EXTENSION` para proporcionar tus propios reemplazos al obtener valores de configuración mediante las funciones de la API de Defold. Un proyecto de ejemplo que puedes usar como punto de partida está [disponible en GitHub](https://github.com/defold/example-configfile-extension/tree/master).


## Proteger tu juego contra tramposos
Las trampas en los videojuegos han existido desde la propia industria de los videojuegos. Antes, los cheat codes se compartían en revistas populares de videojuegos y se vendían cartuchos especiales de trucos para las primeras computadoras domésticas. A medida que la industria y los juegos evolucionaron, también lo hicieron los tramposos y sus métodos. Algunos de los mecanismos de trampas más populares para juegos son:

* Reempaquetado de contenido del juego para inyectar lógica personalizada
* Speed hacks para hacer que un juego se ejecute más rápido o más lento de lo normal
* Automatización y análisis visual para apuntado automático y bots
* Inyección de código y memoria para modificar puntajes, vidas, munición, etc.

Protegerse contra tramposos es difícil, casi imposible. Incluso el juego en la nube (cloud gaming), donde los juegos se ejecutan en servidores remotos y se transmiten directamente al dispositivo de un usuario, no está completamente exento de tramposos.

Defold no proporciona ninguna solución anti-cheat en el motor ni en las herramientas y, en su lugar, delega ese trabajo a una de las muchas empresas especializadas en proporcionar soluciones anti-cheat para juegos.


## Proteger tu comunicación de red
La comunicación por socket y HTTP de Defold admite conexiones de socket seguras. Se recomienda usar conexiones seguras para cualquier comunicación con servidores, con el fin de autenticar el servidor y proteger la privacidad y la integridad de los datos intercambiados mientras están en tránsito desde el cliente al servidor y viceversa. Defold usa la popular y ampliamente adoptada implementación de código abierto [Mbed TLS](https://github.com/Mbed-TLS/mbedtls) de los protocolos TLS y SSL. Mbed TLS es desarrollado por ARM y sus socios tecnológicos.

### Validación de certificados SSL
Para prevenir ataques man-in-the-middle en tu comunicación de red, es posible validar la cadena de certificados durante el handshake SSL al negociar una conexión con un servidor. Esto se puede hacer proporcionando una lista de claves públicas al cliente de red en Defold. Para obtener más información sobre cómo proteger tu comunicación de red, lee la sección sobre verificación SSL en el [manual de red](https://defold.com/manuals/networking/#secure-connections).


## Proteger tu uso de software de terceros
Aunque no es necesario usar librerías de terceros ni extensiones nativas para crear un juego, entre desarrolladores se ha vuelto una práctica muy común usar assets del [Asset Portal](https://defold.com/assets/) oficial para acelerar el desarrollo. El Asset Portal contiene una gran selección de assets, desde integraciones con SDKs de terceros hasta gestores de pantalla, librerías de interfaz, cámaras y mucho más.

Ninguno de los assets del Asset Portal ha sido revisado por la Defold Foundation, y no asumimos responsabilidad por daños al sistema de tu computadora u otro dispositivo, ni por pérdida de datos que resulte del uso de cualquier asset obtenido mediante el Asset Portal. Puedes leer la letra pequeña en nuestros [Terms and Conditions](https://defold.com/terms-and-conditions/#3-no-warranties).

Recomendamos que revises cualquier asset antes de usarlo y que, una vez que consideres que es adecuado para tu proyecto, crees un fork o una copia del asset para asegurarte de que no cambie sin que lo notes.


## Proteger tu uso de servidores de build en la nube
Los servidores de build en la nube de Defold (también llamados extender servers) se crearon para ayudar a los desarrolladores a agregar nueva funcionalidad al motor Defold sin requerir un rebuild del propio motor. Cuando un proyecto Defold que contiene código nativo se crea por primera vez, el código nativo y cualquier recurso asociado se envían a los servidores de build en la nube, donde se crea una versión personalizada del motor Defold y se envía de vuelta al desarrollador. El mismo proceso se aplica cuando un proyecto se crea usando un application manifest personalizado para eliminar componentes no usados del motor.

Los servidores de build en la nube están alojados en AWS y se crean de acuerdo con prácticas recomendadas de seguridad. Sin embargo, la Defold Foundation no garantiza que los servidores de build en la nube cumplan tus requisitos, estén libres de defectos, libres de virus, sean seguros o estén libres de errores, ni que tu uso de los servidores sea ininterrumpido o seguro. Puedes leer la letra pequeña en nuestros [Terms and Conditions](https://defold.com/terms-and-conditions/#3-no-warranties).

Si la seguridad y disponibilidad de los servidores de build te preocupan, recomendamos que configures tus propios servidores de build privados. Las instrucciones sobre cómo configurar tu propio servidor se pueden encontrar en el [archivo README principal](https://github.com/defold/extender) del repositorio extender en GitHub.


## Proteger tu contenido descargable
El sistema Live Update de Defold permite a los desarrolladores excluir contenido del bundle principal del juego para descargarlo y usarlo en un momento posterior. Un caso de uso típico es descargar niveles, mapas o mundos adicionales a medida que el jugador avanza en el juego.

Cuando el contenido excluido se descarga y se prepara para usarlo en un juego, el motor lo verificará antes de usarlo. La verificación consta de varias comprobaciones:

* ¿El formato binario es correcto?
* ¿El contenido descargado es compatible con la versión del motor que está en ejecución actualmente?
* ¿El contenido descargado está completo y no le falta ningún archivo?

Puedes leer más sobre este proceso en el [manual de Live Update](https://defold.com/manuals/live-update/#content-verification).
