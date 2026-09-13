---
title: Die Entwicklungs-App auf einem Gerät ausführen
brief: Dieses Handbuch erklärt, wie du die Entwicklungs-App auf deinem Gerät installierst, um iterativ auf dem Gerät zu entwickeln.
---

# Die mobile Entwicklungs-App {#the-mobile-development-app}

Mit der Entwicklungs-App (development app) kannst du Inhalte über WLAN auf dein Gerät übertragen. Das verkürzt die Zeit zwischen Entwicklungsdurchläufen erheblich, da du nicht jedes Mal ein Bundle erstellen und installieren musst, wenn du deine Änderungen testen möchtest. Installiere die Entwicklungs-App auf deinen Geräten, starte die App und wähle dann im Editor das Gerät als Build-Ziel aus.

## Eine Entwicklungs-App installieren {#installing-a-development-app}

Jede iOS- oder Android-Anwendung, deren Bundle im Modus Debug erstellt wurde, kann als Entwicklungs-App dienen. Dies ist auch die empfohlene Lösung, da die Entwicklungs-App dann die richtigen Projekteinstellungen hat und dieselben [nativen Erweiterungen (native extensions)](/manuals/extensions/) wie das Projekt verwendet, an dem du arbeitest. 

Du kannst aus deinem Projekt ein Bundle der Variante Debug ohne Inhalte erstellen. Verwende diese Option, um eine Version deiner Anwendung mit nativen Erweiterungen zu erstellen, die für die in diesem Handbuch beschriebene iterative Entwicklung geeignet ist.

![Bundle ohne Inhalte](images/dev-app/contentless-bundle.png)

### Unter iOS installieren {#installing-on-ios}

Folge den [Anweisungen im iOS-Handbuch](/manuals/ios/#creating-an-ios-application-bundle), um ein Bundle für iOS zu erstellen. Achte darauf, Debug als Variante auszuwählen!

### Unter Android installieren {#installing-on-android}

Folge den [Anweisungen im Android-Handbuch](https://defold.com/manuals/android/#creating-an-android-application-bundle), um ein Bundle für Android zu erstellen.

## Dein Spiel starten {#launching-your-game}

Um dein Spiel auf deinem Gerät zu starten, müssen sich die Entwicklungs-App und der Editor über dasselbe WLAN-Netzwerk oder über USB verbinden können (siehe unten).

1. Stelle sicher, dass der Editor gestartet ist und läuft.
2. Starte die Entwicklungs-App auf dem Gerät.
3. Wähle dein Gerät im Editor unter <kbd>Project ▸ Targets</kbd> aus.
4. Wähle <kbd>Project ▸ Build</kbd>, um das Spiel auszuführen. Es kann eine Weile dauern, bis das Spiel startet, da die Spielinhalte über das Netzwerk auf das Gerät übertragen werden.
5. Während das Spiel läuft, kannst du wie gewohnt [Hot Reload](/manuals/hot-reload/) verwenden.

### Unter Windows über USB mit einem iOS-Gerät verbinden {#connecting-to-an-ios-device-using-usb-on-windows}

Wenn du unter Windows über USB eine Verbindung zu einer Entwicklungs-App auf einem iOS-Gerät herstellen möchtest, musst du zunächst [iTunes installieren](https://www.apple.com/lae/itunes/download/). Nach der Installation von iTunes musst du außerdem auf deinem iOS-Gerät im Menü Settings [Personal Hotspot aktivieren](https://support.apple.com/en-us/HT204023). Wenn die Meldung "Trust This Computer?" erscheint, tippe auf Trust. Das Gerät sollte nun unter <kbd>Project ▸ Targets</kbd> erscheinen, wenn die Entwicklungs-App läuft.

### Unter Linux über USB mit einem iOS-Gerät verbinden {#connecting-to-an-ios-device-using-usb-on-linux}

Unter Linux musst du auf deinem Gerät im Menü Settings die Option Personal Hotspot aktivieren, wenn du es über USB verbindest. Wenn die Meldung "Trust This Computer?" erscheint, tippe auf Trust. Das Gerät sollte nun unter <kbd>Project ▸ Targets</kbd> erscheinen, wenn die Entwicklungs-App läuft.

### Unter macOS über USB mit einem iOS-Gerät verbinden {#connecting-to-an-ios-device-using-usb-on-macos}

Bei neueren iOS-Versionen öffnet das Gerät automatisch eine neue Ethernet-Schnittstelle zwischen dem Gerät und dem Computer, wenn du es unter macOS über USB verbindest. Das Gerät sollte unter <kbd>Project ▸ Targets</kbd> erscheinen, wenn die Entwicklungs-App läuft.

Bei älteren iOS-Versionen musst du auf deinem Gerät im Menü Settings die Option Personal Hotspot aktivieren, wenn du es unter macOS über USB verbindest. Wenn die Meldung "Trust This Computer?" erscheint, tippe auf Trust. Das Gerät sollte nun unter <kbd>Project ▸ Targets</kbd> erscheinen, wenn die Entwicklungs-App läuft.

### Unter macOS über USB mit einem Android-Gerät verbinden {#connecting-to-an-android-device-using-usb-on-macos}

Unter macOS kannst du über USB eine Verbindung zu einer laufenden Entwicklungs-App auf einem Android-Gerät herstellen, wenn auf dem Gerät USB Tethering Mode aktiviert ist. Unter macOS musst du einen Treiber eines Drittanbieters wie [HoRNDIS](https://joshuawise.com/horndis#available_versions) installieren. Nach der Installation von HoRNDIS musst du dessen Ausführung außerdem in den Einstellungen unter Security & Privacy erlauben. Sobald USB Tethering aktiviert ist, erscheint das Gerät unter <kbd>Project ▸ Targets</kbd>, wenn die Entwicklungs-App läuft.

### Unter Windows oder Linux über USB mit einem Android-Gerät verbinden {#connecting-to-an-android-device-using-usb-on-windows-or-linux}

Unter Windows und Linux kannst du über USB eine Verbindung zu einer laufenden Entwicklungs-App auf einem Android-Gerät herstellen, wenn auf dem Gerät USB Tethering Mode aktiviert ist. Sobald USB Tethering aktiviert ist, erscheint das Gerät unter <kbd>Project ▸ Targets</kbd>, wenn die Entwicklungs-App läuft.

## Fehlerbehebung {#troubleshooting}

Unable to download application
: Stelle sicher, dass die UDID deines Geräts im Bereitstellungsprofil enthalten ist, das zum Signieren der App verwendet wurde.

Dein Gerät erscheint nicht im Menü Targets
: Stelle sicher, dass dein Gerät mit demselben WLAN-Netzwerk wie dein Computer verbunden ist. Stelle sicher, dass der Build der Entwicklungs-App im Modus Debug erstellt wurde.

Das Spiel startet nicht und meldet, dass die Versionen nicht übereinstimmen
: Dies passiert, wenn du den Editor auf die neueste Version aktualisiert hast. Du musst einen Build einer neuen Version erstellen und diese installieren.
