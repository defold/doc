---
title: Handbuch zur Anwendungssicherheit
brief: Dieses Handbuch behandelt verschiedene Bereiche im Zusammenhang mit sicheren Entwicklungspraktiken.
---

# Anwendungssicherheit {#application-security}

Anwendungssicherheit ist ein breites Thema, das von sicheren Entwicklungspraktiken bis zum Schutz deiner Spielinhalte nach der Veröffentlichung reicht. Dieses Handbuch behandelt verschiedene Bereiche und ordnet sie im Zusammenhang mit der Nutzung der Defold-Engine, ihrer Werkzeuge und Dienste in die Anwendungssicherheit ein:

* Schutz des geistigen Eigentums
* Anti-Cheat-Lösungen
* Sichere Netzwerkkommunikation
* Verwendung von Drittanbietersoftware
* Nutzung von Cloud-Build-Servern
* Herunterladbare Inhalte


## Dein geistiges Eigentum vor Diebstahl schützen {#securing-your-intellectual-property-from-theft}
Die meisten Entwickler beschäftigt die Frage, wie sie ihre Werke vor Diebstahl schützen können. Urheberrecht, Patente und Marken können aus rechtlicher Sicht dazu dienen, die verschiedenen Aspekte des geistigen Eigentums an Videospielen zu schützen. Das Urheberrecht gibt seinem Inhaber das ausschließliche Recht, das kreative Werk zu verbreiten. Patente schützen Erfindungen, und Marken schützen Namen, Symbole und Logos.

Es kann auch wünschenswert sein, technische Vorkehrungen zum Schutz der kreativen Arbeit an einem Spiel zu treffen. Dabei solltest du jedoch bedenken, dass sich Wege finden lassen, die Assets zu extrahieren, sobald das Spiel in den Händen der Spieler ist. Dies ist durch Reverse Engineering der Spielanwendung und ihrer Dateien möglich, aber auch mithilfe von Werkzeugen, die Texturen und Modelle extrahieren, wenn diese an die GPU gesendet werden oder andere Assets in den Arbeitsspeicher geladen werden.

Aus diesem Grund vertreten wir grundsätzlich die Auffassung, dass Nutzer die Assets eines Spiels extrahieren können, wenn sie entschlossen genug dazu sind.

Entwickler können eigene Schutzmaßnahmen hinzufügen, um das Extrahieren der Assets zu erschweren, __aber nicht unmöglich zu machen__. Dazu gehören in der Regel verschiedene Verfahren zur Verschlüsselung und Verschleierung, um Spiel-Assets zu schützen und zu verbergen.

### Quellcode-Verschleierung {#source-code-obfuscation}
Die Quellcode-Verschleierung ist ein automatisierter Vorgang, bei dem der Quellcode für Menschen absichtlich schwer verständlich gemacht wird, ohne die Ausgabe des Programms zu beeinflussen. Der Zweck besteht in der Regel darin, vor Diebstahl zu schützen, aber auch das Cheaten zu erschweren.

In Defold lässt sich die Quellcode-Verschleierung entweder als vorbereitender Schritt vor dem Build oder als integrierter Bestandteil des Defold-Build-Vorgangs anwenden. Bei einer Verschleierung vor dem Build wird der Quellcode mit einem Werkzeug zur Verschleierung bearbeitet, bevor der Defold-Build-Vorgang startet.

Die Verschleierung während des Builds wird hingegen mithilfe eines Lua-Builder-Plugins in den Build-Vorgang integriert. Ein Lua-Builder-Plugin nimmt den unverarbeiteten Quellcode als Eingabe entgegen und gibt eine verschleierte Version des Quellcodes aus. Ein Beispiel für die Verschleierung während des Builds zeigt die [Prometheus-Erweiterung](https://github.com/defold/extension-prometheus), die auf Prometheus basiert, einem auf GitHub verfügbaren Lua-Obfuskator. Unten findest du ein Beispiel dafür, wie Prometheus einen Codeausschnitt stark verschleiert (beachte, dass sich eine derart starke Verschleierung auf die Leistung des Lua-Codes zur Laufzeit auswirkt):

Beispiel:

```
function init(self)
 print("hello")
 test.greet("Bob")
end
```

Verschleierte Ausgabe:

```
local v={"+qdW","ZK0tEKf=";"XP/IX3+="}for o,J in ipairs({{1;3};{1,1},{2,3}})do while J[1]<J[2]do v[J[1]],v[J[2]],J[1],J[2]=v[J[2]],v[J[1]],J[1]+1,J[2]-1 end end local function J(o)return v[o+45816]end do local o={["/"]=9;["8"]=48;["9"]=1;q=38,o=62;V=33;y=43,d=61,B=50,L=54;v=2;["0"]=21,n=31;p=63;R=5;N=3;i=10;e=35;C=7;l=56;a=47,J=58;m=59;["2"]=36;z=11;M=12;Z=26;O=18;["5"]=20;s=8,["4"]=30,P=55;w=4;U=29;Q=28;r=24,h=41;G=45;c=19;W=34,k=57;T=14,t=44,S=0;f=60;F=42,E=27;u=40;X=25,j=17;["3"]=23,b=13;["1"]=53;Y=32,A=22,K=6,["+"]=16,["6"]=46;["7"]=51;I=37;D=52;H=15,x=49,g=39}local J=type local x=string.sub local d=v local l=string.len local W=string.char local L=table.insert local w=table.concat local h=math.floor for v=1,#d,1 do local X=d[v]if J(X)=="string"then local J=l(X)local H={}local S=1 local k=0 local K=0 while S<=J do local v=x(X,S,S)local d=o[v]if d then k=k+d*64^(3-K)K=K+1 if K==4 then K=0 local o=h(k/65536)local v=h((k%65536)/256)local J=k%256 L(H,W(o,v,J))k=0 end elseif v=="="then L(H,W(h(k/65536)))if S>=J or x(X,S+1,S+1)~="="then L(H,W(h((k%65536)/256)))end break end S=S+1 end d[v]=w(H)end end end local function o(o)test[J(-45815)](o)end function init(v)print(J(-45813))o(J(-45814))end
```

### Ressourcenverschlüsselung {#resource-encryption}
Während des Defold-Build-Vorgangs werden die Spielressourcen verarbeitet und in Formate umgewandelt, die sich für die Verwendung durch die Defold-Engine zur Laufzeit eignen. Texturen werden in das Format Basis Universal kompiliert, Sammlungen (collections), Spielobjekte (game objects) und Komponenten (components) werden von einer menschenlesbaren Textdarstellung in ihre binären Entsprechungen umgewandelt, und der Lua-Quellcode wird verarbeitet und in Bytecode kompiliert. Andere Assets wie Audiodateien werden unverändert verwendet.

Nach Abschluss dieses Vorgangs werden die Assets einzeln zum Spielarchiv hinzugefügt. Das Spielarchiv ist eine große Binärdatei, und die Position jeder Ressource innerhalb des Archivs wird in einer Archivindexdatei gespeichert. Das Format ist [hier](https://github.com/defold/defold/blob/dev/engine/docs/ARCHIVE_FORMAT.md) dokumentiert.

Bevor Lua-Quelldateien zum Archiv hinzugefügt werden, werden sie optional auch verschlüsselt. Die in Defold standardmäßig bereitgestellte Verschlüsselung ist eine einfache Blockchiffre. Sie verhindert, dass Zeichenfolgen im Code sofort sichtbar sind, wenn das Spielarchiv mit einem Anzeigeprogramm für Binärdateien untersucht wird. Sie sollte nicht als kryptografisch sicher angesehen werden, da der Defold-Quellcode auf GitHub verfügbar ist und der Chiffrierschlüssel darin sichtbar ist.

Du kannst eine eigene Verschlüsselung für Lua-Quelldateien hinzufügen, indem du ein Plugin zur Ressourcenverschlüsselung implementierst. Ein solches Plugin besteht aus einem Teil, der Ressourcen während des Build-Vorgangs verschlüsselt, und einem Teil, der Ressourcen zur Laufzeit entschlüsselt, wenn sie aus dem Spielarchiv gelesen werden. Ein grundlegendes Plugin zur Ressourcenverschlüsselung, das du als Ausgangspunkt für deine eigene Verschlüsselung verwenden kannst, ist [auf GitHub verfügbar](https://github.com/defold/extension-resource-encryption).


### Projektkonfigurationswerte kodieren {#encoding-project-configuration-values}
Die Datei *game.project* wird unverändert in dein Anwendungs-Bundle aufgenommen. Manchmal möchtest du öffentliche API-Zugriffsschlüssel oder ähnliche Werte speichern, die sensibel, aber möglicherweise nicht vertraulich sind. Um die Sicherheit solcher Werte zu erhöhen, kannst du sie in die Binärdatei der Anwendung aufnehmen, statt sie in *game.project* zu speichern. Sie bleiben dabei für Defold-API-Funktionen wie `sys.get_config_string()` und ähnliche Funktionen zugänglich. Dazu kannst du eine native Erweiterung (native extension) in deiner Datei *game.project* hinzufügen und das Makro `DM_DECLARE_CONFIGFILE_EXTENSION` verwenden, um eigene Überschreibungen für das Abrufen von Konfigurationswerten über die Defold-API-Funktionen bereitzustellen. Ein Beispielprojekt, das du als Ausgangspunkt verwenden kannst, ist [auf GitHub verfügbar](https://github.com/defold/example-configfile-extension/tree/master).


## Dein Spiel vor Cheatern schützen {#securing-your-game-against-cheaters}
Cheaten in Videospielen gibt es schon so lange wie die Spielebranche selbst. Früher wurden Cheat-Codes in beliebten Videospielzeitschriften veröffentlicht, und für die frühen Heimcomputer wurden spezielle Cheat-Module verkauft. Mit der Weiterentwicklung der Branche und der Spiele haben sich auch die Cheater und ihre Methoden weiterentwickelt. Zu den beliebtesten Cheat-Methoden für Spiele gehören:

* Erneutes Verpacken von Spielinhalten, um eigene Logik einzuschleusen
* Speed-Hacks, um ein Spiel schneller oder langsamer als normal laufen zu lassen
* Automatisierung und visuelle Analyse für automatisches Zielen und Bots
* Code- und Speicherinjektion, um Punktzahlen, Leben, Munition usw. zu verändern

Der Schutz vor Cheatern ist schwierig und grenzt an das Unmögliche. Selbst Cloud-Gaming, bei dem Spiele auf entfernten Servern ausgeführt und direkt auf das Gerät eines Nutzers gestreamt werden, ist nicht vollständig vor Cheatern gefeit.

Defold bietet in der Engine oder den Werkzeugen keine Anti-Cheat-Lösungen an und überlässt diese Arbeit einem der vielen Unternehmen, die auf Anti-Cheat-Lösungen für Spiele spezialisiert sind.


## Deine Netzwerkkommunikation absichern {#securing-your-network-communication}
Die Socket- und HTTP-Kommunikation in Defold unterstützt sichere Socket-Verbindungen. Es wird empfohlen, für jede Serverkommunikation sichere Verbindungen zu verwenden, um den Server zu authentifizieren und die Vertraulichkeit und Integrität aller ausgetauschten Daten während der Übertragung vom Client zum Server und umgekehrt zu schützen. Defold verwendet die beliebte und weitverbreitete Open-Source-Implementierung [Mbed TLS](https://github.com/Mbed-TLS/mbedtls) der Protokolle TLS und SSL. Mbed TLS wird von ARM und seinen Technologiepartnern entwickelt.

### Validierung von SSL-Zertifikaten {#ssl-certificate-validation}
Um Man-in-the-Middle-Angriffe auf deine Netzwerkkommunikation zu verhindern, kannst du die Zertifikatskette während des SSL-Handshakes beim Aushandeln einer Verbindung mit einem Server validieren. Dazu stellst du dem Netzwerk-Client in Defold eine Liste öffentlicher Schlüssel bereit. Weitere Informationen zum Absichern deiner Netzwerkkommunikation findest du im Abschnitt zur SSL-Überprüfung im [Netzwerkhandbuch](https://defold.com/manuals/networking/#secure-connections).


## Drittanbietersoftware sicher verwenden {#securing-your-use-of-third-party-software}
Obwohl du keine Bibliotheken oder nativen Erweiterungen von Drittanbietern benötigst, um ein Spiel zu erstellen, ist es unter Entwicklern sehr üblich geworden, Assets aus dem offiziellen [Asset Portal](https://defold.com/assets/) zu verwenden, um die Entwicklung zu beschleunigen. Das Asset Portal enthält eine große Auswahl an Assets, von Integrationen mit SDKs von Drittanbietern über Bildschirmmanager, UI-Bibliotheken und Kameras bis hin zu vielem mehr.

Keines der Assets im Asset Portal wurde von der Defold Foundation überprüft. Wir übernehmen keine Verantwortung für Schäden an deinem Computersystem oder einem anderen Gerät oder für Datenverluste, die durch die Verwendung eines über das Asset Portal bezogenen Assets entstehen. Das Kleingedruckte findest du in unseren [Allgemeinen Geschäftsbedingungen](https://defold.com/terms-and-conditions/#3-no-warranties).

Wir empfehlen dir, jedes Asset vor der Verwendung zu prüfen. Sobald du es als für dein Projekt geeignet beurteilt hast, solltest du einen Fork oder eine Kopie des Assets erstellen, damit es sich nicht unbemerkt ändert.


## Cloud-Build-Server sicher nutzen {#securing-your-use-of-cloud-build-servers}
Die Defold-Cloud-Build-Server (auch als Extender-Server bekannt) wurden entwickelt, um Entwicklern das Hinzufügen neuer Funktionen zur Defold-Engine zu ermöglichen, ohne die Engine selbst neu erstellen zu müssen. Wenn ein Defold-Projekt mit nativem Code zum ersten Mal erstellt wird, werden der native Code und alle zugehörigen Ressourcen an die Cloud-Build-Server gesendet. Dort wird eine angepasste Version der Defold-Engine erstellt und an den Entwickler zurückgesendet. Derselbe Vorgang kommt zum Einsatz, wenn ein Projekt mit einem benutzerdefinierten Anwendungsmanifest erstellt wird, um nicht verwendete Komponenten aus der Engine zu entfernen.

Die Cloud-Build-Server werden bei AWS gehostet und nach bewährten Sicherheitspraktiken eingerichtet. Die Defold Foundation garantiert jedoch nicht, dass die Cloud-Build-Server deine Anforderungen erfüllen, frei von Mängeln, virenfrei, sicher oder fehlerfrei sind oder dass deine Nutzung der Server unterbrechungsfrei oder sicher ist. Das Kleingedruckte findest du in unseren [Allgemeinen Geschäftsbedingungen](https://defold.com/terms-and-conditions/#3-no-warranties).

Wenn dir die Sicherheit und Verfügbarkeit der Build-Server Sorgen bereiten, empfehlen wir dir, eigene private Build-Server einzurichten. Eine Anleitung zum Einrichten deines eigenen Servers findest du in der [zentralen Readme-Datei](https://github.com/defold/extender) des Extender-Repositorys auf GitHub.


## Deine herunterladbaren Inhalte absichern {#securing-your-downloadable-content}
Mit dem Live-Update-System von Defold können Entwickler Inhalte aus dem Haupt-Bundle des Spiels ausschließen, um sie später herunterzuladen und zu verwenden. Ein typischer Anwendungsfall ist das Herunterladen zusätzlicher Level, Karten oder Welten, während der Spieler im Spiel voranschreitet.

Wenn ausgeschlossene Inhalte heruntergeladen und für die Verwendung in einem Spiel vorbereitet werden, überprüft die Engine sie vor der Verwendung. Diese Überprüfung besteht aus mehreren Prüfungen:

* Ist das Binärformat korrekt?
* Werden die heruntergeladenen Inhalte von der aktuell laufenden Engine-Version unterstützt?
* Sind die heruntergeladenen Inhalte vollständig, ohne dass Dateien fehlen?

Weitere Informationen zu diesem Vorgang findest du im [Handbuch zu Live Update](https://defold.com/manuals/live-update/#content-verification).
