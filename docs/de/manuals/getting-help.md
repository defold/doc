---
title: So bekommst du Hilfe
brief: Dieses Handbuch beschreibt, wie du Hilfe bekommst, wenn bei der Verwendung von Defold ein Problem auftritt.
---

# Hilfe bekommen {#getting-help}

Wenn bei der Verwendung von Defold ein Problem auftritt, möchten wir davon erfahren, damit wir den Fehler beheben und/oder dir helfen können, das Problem zu umgehen! Es gibt mehrere Möglichkeiten, Probleme zu besprechen und zu melden. Wähle die für dich passende Möglichkeit:

## Ein Problem im Forum melden {#report-a-problem-on-the-forum}

Eine gute Möglichkeit, ein Problem zu besprechen und Hilfe zu erhalten, ist eine Frage in unserem [Forum](https://forum.defold.com). Veröffentliche deinen Beitrag je nach Art des Problems in der Kategorie [Questions](https://forum.defold.com/c/questions) oder [Bugs](https://forum.defold.com/c/bugs). Denke daran, vor dem Fragen nach deiner Frage oder deinem Problem zu [suchen](https://forum.defold.com/search), da es möglicherweise bereits eine Lösung gibt.

Wenn du mehrere Fragen hast, erstelle mehrere Beiträge. Stelle keine Fragen zu unterschiedlichen Themen im selben Beitrag.

### Erforderliche Informationen {#required-information}
Wir können dir nur helfen, wenn du die benötigten Informationen angibst:

**Titel**
Verwende einen kurzen und aussagekräftigen Titel. Ein guter Titel wäre „Wie bewege ich ein Spielobjekt (game object) in die Richtung, in die es gedreht ist?“ oder „Wie blende ich ein Sprite aus?“. Ein schlechter Titel wäre „Ich brauche Hilfe mit Defold!“ oder „Mein Spiel funktioniert nicht!“.

**Beschreibung des Fehlers (ERFORDERLICH)**
Eine klare und knappe Beschreibung des Fehlers.

**Schritte zum Nachstellen (ERFORDERLICH)**
Schritte zum Nachstellen des Verhaltens:
1. Gehe zu '...'
2. Klicke auf '....'
3. Scrolle nach unten zu '....'
4. Beobachte den Fehler

**Erwartetes Verhalten (ERFORDERLICH)**
Eine klare und knappe Beschreibung dessen, was du erwartet hast.

**Defold-Version (ERFORDERLICH):**
  - Version [z. B. 1.2.155]

**Plattformen (ERFORDERLICH):**
 - Plattformen: [z. B. iOS, Android, Windows, macOS, Linux, HTML5]
 - Betriebssystem: [z. B. iOS8.1, Windows 10, High Sierra]
 - Gerät: [z. B. iPhone6]

**Minimales Beispielprojekt zum Nachstellen des Fehlers (OPTIONAL):**
Bitte füge ein minimales Projekt bei, in dem sich der Fehler nachstellen lässt. Das hilft der Person, die den Fehler untersucht und behebt, erheblich.

**Protokolle (OPTIONAL):**
Bitte stelle relevante Protokolle der Engine, des Editors oder des Build-Servers bereit. Wo die Protokolle gespeichert werden, erfährst du [hier](#log-files).

**Behelfslösung (OPTIONAL):**
Falls es eine Behelfslösung gibt, beschreibe sie bitte hier.

**Bildschirmaufnahmen (OPTIONAL):**
Füge gegebenenfalls Bildschirmaufnahmen hinzu, um dein Problem zu veranschaulichen.

**Zusätzlicher Kontext (OPTIONAL):**
Ergänze hier weitere Hintergrundinformationen zum Problem.


### Code teilen {#sharing-code}
Wenn du Code teilst, empfehlen wir, ihn als Text und nicht als Bildschirmaufnahme zu teilen. Text lässt sich leichter durchsuchen und ermöglicht es, Fehler hervorzuheben sowie Änderungen vorzuschlagen und vorzunehmen. Um Code zu teilen, umschließe ihn mit drei \`\`\` oder rücke ihn mit 4 Leerzeichen ein.

Beispiel:

\`\`\`
print("Hello code!")
\`\`\`

Ergebnis:

```
print("Hello code!")
```


## Ein Problem aus dem Editor melden {#report-a-problem-from-the-editor}

Der Editor bietet eine bequeme Möglichkeit, Probleme zu melden. Wähle im Editor den Menüpunkt <kbd>Help->Report Issue</kbd>, um ein Problem zu melden.

![](images/getting_help/report_issue.png)

Dieser Menüpunkt führt dich zu einem Issue-Tracker auf GitHub. Stelle [Protokolldateien](#log-files), Informationen zu deinem Betriebssystem, Schritte zum Nachstellen des Problems, mögliche Behelfslösungen usw. bereit.

::: sidenote
Du benötigst ein GitHub-Konto, um auf diese Weise einen Fehlerbericht einzureichen.
:::


## Ein Problem auf Discord besprechen {#discuss-a-problem-on-discord}

Wenn bei der Verwendung von Defold ein Problem auftritt, kannst du versuchen, deine Frage auf [Discord](https://www.defold.com/discord/) zu stellen. Wir empfehlen jedoch, komplexe Fragen und ausführliche Diskussionen im Forum zu veröffentlichen. Beachte außerdem, dass wir keine Fehlerberichte über Discord annehmen.


# Protokolldateien {#log-files}

Die Engine, der Editor und der Build-Server erzeugen Protokollinformationen, die bei der Bitte um Hilfe und bei der Fehlersuche sehr wertvoll sein können. Stelle beim Melden eines Problems immer Protokolldateien bereit:

* [Engine-Protokolle](/manuals/debugging-game-and-system-logs)
* [Editor-Protokolle](/manuals/editor#editor-logs)
* [Build-Server-Protokolle](/manuals/extensions#build-server-logs)
