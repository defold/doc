---
title: Kommunikation zwischen Anwendungen in Defold
brief: Mit der Kommunikation zwischen Anwendungen kannst du die Argumente auslesen, die beim Start deiner Anwendung übergeben wurden. Dieses Handbuch erklärt die dafür verfügbare API von Defold.
---

# Kommunikation zwischen Anwendungen {#inter-app-communication}

Auf den meisten Betriebssystemen lassen sich Anwendungen auf verschiedene Arten starten:

* Aus der Liste der installierten Anwendungen
* Über einen anwendungsspezifischen Link
* Über eine Push-Benachrichtigung
* Als letzter Schritt eines Installationsvorgangs.

Wenn die Anwendung über einen Link, eine Benachrichtigung oder bei der Installation gestartet wird, können zusätzliche Argumente übergeben werden. Dazu gehören beispielsweise ein Installationsverweis (install referrer) bei der Installation oder ein Deep Link beim Start über einen anwendungsspezifischen Link oder eine Benachrichtigung. Defold bietet über eine native Erweiterung (native extension) eine einheitliche Möglichkeit, Informationen darüber abzurufen, wie die Anwendung aufgerufen wurde.

## Die Erweiterung installieren {#installing-the-extension}

Um die Erweiterung für die Kommunikation zwischen Anwendungen (Inter-app communication) zu verwenden, musst du sie deiner Datei *game.project* als Abhängigkeit hinzufügen. Die neueste stabile Version ist unter dieser Abhängigkeits-URL verfügbar:
```
https://github.com/defold/extension-iac/archive/master.zip
```

Wir empfehlen einen Link zu einer ZIP-Datei einer [bestimmten Version](https://github.com/defold/extension-iac/releases).

## Die Erweiterung verwenden {#using-the-extension}

Die API ist sehr einfach zu verwenden. Du übergibst der Erweiterung eine Listener-Funktion und reagierst auf die Callbacks des Listeners.

```
local function iac_listener(self, payload, type)
     if type == iac.TYPE_INVOCATION then
         -- This was an invocation
         print(payload.origin) -- origin may be empty string if it could not be resolved
         print(payload.url)
     end
end

function init(self)
     iac.set_listener(iac_listener)
end
```

Die vollständige API-Dokumentation findest du auf der [GitHub-Seite der Erweiterung](https://defold.github.io/extension-iac/).
