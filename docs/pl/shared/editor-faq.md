#### P: Jakie są wymagania systemowe edytora?
O: Edytor będzie używał do 75% dostępnej pamięci systemu. Na komputerze z 4 GB RAM powinno to wystarczyć dla mniejszych projektów Defold. W przypadku projektów średniej wielkości lub dużych zaleca się 6 GB RAM lub więcej.


#### P: Czy wersje beta Defold aktualizują się automatycznie?
O: Tak. Wersja beta edytora Defold sprawdza dostępność aktualizacji przy uruchomieniu, tak samo jak wersja stabilna.


#### P: Dlaczego podczas uruchamiania edytora pojawia się błąd `java.awt.AWTError: Assistive Technology not found`?
O: Ten błąd jest związany z problemami z technologią wspomagającą Java, taką jak [czytnik ekranu NVDA](https://www.nvaccess.org/download/). Prawdopodobnie masz plik `.accessibility.properties` w katalogu domowym. Usuń ten plik i spróbuj uruchomić edytor ponownie. (Uwaga: jeśli korzystasz z technologii wspomagającej i potrzebujesz, aby ten plik był obecny, skontaktuj się z nami pod adresem info@defold.se, aby omówić alternatywne rozwiązania).

Omówiono to [tutaj na forum Defold](https://forum.defold.com/t/editor-endless-loading-windows-10-1-2-169-solved/65481/3).


#### P: Dlaczego podczas uruchamiania edytora pojawia się błąd `sun.security.validator.ValidatorException: PKIX path building failed`?
O: Ten wyjątek występuje, gdy edytor próbuje nawiązać połączenie https, ale łańcuch certyfikatów dostarczony przez serwer nie może zostać zweryfikowany.

Szczegóły tego błędu znajdziesz [pod tym linkiem](https://github.com/defold/defold/blob/master/editor/README_TROUBLESHOOTING_PKIX.md).


#### P: Dlaczego podczas wykonywania niektórych operacji pojawia się `java.lang.OutOfMemoryError: Java heap space`?
O: Edytor Defold jest zbudowany w Javie i w niektórych przypadkach domyślna konfiguracja pamięci Javy może nie wystarczyć. Jeśli tak się stanie, możesz ręcznie skonfigurować edytor tak, aby przydzielał więcej pamięci, edytując plik konfiguracyjny edytora. Plik konfiguracyjny o nazwie `config` znajduje się w folderze `Defold.app/Contents/Resources/` na macOS. Na Windows znajduje się obok pliku wykonywalnego `Defold.exe`, a na Linux obok pliku wykonywalnego `Defold`. Otwórz plik `config` i dodaj `-Xmx6gb` do linii zaczynającej się od `vmargs`. Dodanie `-Xmx6gb` ustawi maksymalny rozmiar sterty na 6 gigabajtów (domyślnie zwykle jest to 4Gb). Powinno to wyglądać mniej więcej tak:

```
vmargs = -Xmx6gb,-Dfile.encoding=UTF-8,-Djna.nosys=true,-Ddefold.launcherpath=${bootstrap.launcherpath},-Ddefold.resourcespath=${bootstrap.resourcespath},-Ddefold.version=${build.version},-Ddefold.editor.sha1=${build.editor_sha1},-Ddefold.engine.sha1=${build.engine_sha1},-Ddefold.buildtime=${build.time},-Ddefold.channel=${build.channel},-Ddefold.archive.domain=${build.archive_domain},-Djava.net.preferIPv4Stack=true,-Dsun.net.client.defaultConnectTimeout=30000,-Dsun.net.client.defaultReadTimeout=30000,-Djogl.texture.notexrect=true,-Dglass.accessible.force=false,--illegal-access=warn,--add-opens=java.base/java.lang=ALL-UNNAMED,--add-opens=java.desktop/sun.awt=ALL-UNNAMED,--add-opens=java.desktop/sun.java2d.opengl=ALL-UNNAMED,--add-opens=java.xml/com.sun.org.apache.xerces.internal.jaxp=ALL-UNNAMED
```
