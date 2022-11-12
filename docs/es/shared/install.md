## Descarga

Ve a la [página de descarga de Defold](https://defold.com/download/) donde encontrarás botones de descarga para macOS, Windows y Linux (Ubuntu):

![download editor](../shared/images/editor_download.png)

## Instalación

Instalación en macOS
: El archivo descargado es una imagen DMG que contiene el programa.

  1. Localiza el archivo "Defold-x86_64-darwin.dmg" y haz doble click para abrir la imagen.
  2. Arrastra la aplicación "Defold" a la carpeta "Applications".

  Para iniciar el editor, abre tu carpeta de "Applications" y haz <kbd>doble click</kbd> al archivo "Defold".

  ![Defold macOS](../shared/images/macos_content.png)

Instalación en Windows
: El archivo descargado es un archivo ZIP que necesita ser extraído:

  1. Localiza el archivo "Defold-x86_64-win32.zip", <kbd>mantén presionado</kbd> (o <kbd>click derecho</kbd>) a la carpeta, selecciona *Extraer todo*(/*Extract All*), y después sigue las instrucciones para extraer el archivo en una carpeta denominada "Defold".
  2. Mueve la carpeta "Defold" a "C:\Program Files (x86)\"

  Para iniciar el editor, abre la carpeta "Defold" y <kbd>doble click</kbd> al ejecutable "Defold.exe".

  ![Defold windows](../shared/images/windows_content.png)

Instalción en Linux
: El archivo descargado es un archivo ZIP que necesita ser extraído:

  1. Desde una terminal, localiza el archivo "Defold-x86_64-linux.zip" y extráelo a un directorio llamado "Defold".

     ```bash
     $ unzip Defold-x86_64-linux.zip -d Defold
     ```

  Para iniciar el editor, cambia el directorio a donde quieras extraer la aplicación, entonces arranca el ejecutable `Defold`, o hazle <kbd>doble click</kbd> en tu escritorio.

  ```bash
  $ cd Defold
  $ ./Defold
  ```

  Si presentas problemas iniciando el editor, abriendo un proyecto o corriendo un juego de Defold por favor refiere a la [sección del FAQ de Linux](/faq/faq#linux-issues).

## Instalar una versión anterior

### Desde la página de lanzamientos de Defold en GitHub

Toda versión estable de Defold también están [lanzadas en GitHub](https://github.com/defold/defold/releases).

### Desde la página de descargas de Defold

Puedes descargar e instalar una versión antigua del editor utilizando el siguiente patrón de ligas:

* Windows: https://d.defold.com/archive/%sha1%/stable/editor2/Defold-x86_64-win32.zip
* macOS: https://d.defold.com/archive/%sha1%/stable/editor2/Defold-x86_64-darwin.dmg
* Linux: https://d.defold.com/archive/%sha1%/stable/editor2/Defold-x86_64-linux.zip

Reemplaza `%sha1%` por el hash de lanzamiento representando la versión en cuestión. El hash de cada versión de Defold puede verse en los vínculos de la versión lanzada en la página de descarga en https://d.defold.com/stable/ (asegúrate de remover el caracter # inicial y solo copia la parte alfanumérica):

![Descargar editor](../shared/images/old_version_sha1.png)
