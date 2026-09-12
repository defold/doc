---
title: Projekteinrichtung
brief: Dieses Handbuch beschreibt, wie du in Defold ein Projekt erstellst oder öffnest.
---

# Projekteinrichtung {#project-setup}

Du kannst direkt im Defold-Editor ganz einfach ein neues Projekt erstellen. Du kannst auch ein vorhandenes Projekt öffnen, das sich bereits auf deinem Computer befindet.

## Ein neues lokales Projekt erstellen {#creating-a-new-project}

Klicke auf die Option <kbd>New Project</kbd> und wähle aus, welche Art von Projekt du erstellen möchtest. Gib einen Speicherort auf deiner Festplatte an, an dem die Projektdateien gespeichert werden sollen. Klicke auf <kbd>Create New Project</kbd>, um das Projekt am ausgewählten Speicherort zu erstellen. Du kannst ein neues Projekt aus einer Vorlage erstellen:

![Projekt öffnen](images/workflow/open_project.png)

Oder aus einem Tutorial mit einer Schritt-für-Schritt-Anleitung:

![Projekt aus einem Tutorial erstellen](images/workflow/create_from_tutorial.png)

Oder aus einem fertigen Beispielspiel:

![Projekt aus einem Beispiel erstellen](images/workflow/create_from_sample.png)

### Das Projekt zu GitHub hinzufügen {#adding-the-project-to-github}

Ein lokales Projekt ist in kein Versionsverwaltungssystem eingebunden. Das bedeutet, dass die Dateien nur auf deiner Festplatte liegen und es keinen Verlauf gibt, mit dem du Änderungen rückgängig machen kannst. Dateien, die du über den Bereich *Assets* des Editors löschst, werden in den Papierkorb des Systems verschoben, sofern dies unterstützt wird. Sie können jedoch endgültig gelöscht werden, wenn dieser Vorgang nicht verfügbar ist oder fehlschlägt. Der Papierkorb schützt nicht vor beliebigen Bearbeitungen und bietet keinen Versionsverlauf. Daher wird empfohlen, ein Versionsverwaltungssystem wie Git zu verwenden, um Änderungen an deinen Dateien nachzuverfolgen. Das macht es auch sehr einfach, mit anderen Personen an einem Projekt zusammenzuarbeiten. Du kannst ein lokales Projekt in wenigen Schritten auf GitHub hochladen:

1. Erstelle ein Konto auf [GitHub](https://github.com/) oder melde dich bei einem bestehenden Konto an
2. Erstelle mit der Option [New Repository](https://help.github.com/en/articles/creating-a-new-repository) ein Repository
3. Lade alle Projektdateien über die Option [Upload Files](https://help.github.com/en/articles/adding-a-file-to-a-repository) hoch

Das Projekt steht nun unter Versionsverwaltung. Du solltest [das Projekt klonen](https://help.github.com/en/articles/cloning-a-repository), um es auf deiner lokalen Festplatte zu speichern, und anschließend von diesem neuen Speicherort aus arbeiten.

## Ein vorhandenes Projekt öffnen {#open-an-existing-project}

Klicke auf die Option <kbd>Open From Disk</kbd>, um ein Projekt zu öffnen, das sich bereits auf deinem Computer befindet.

![Projekt importieren](images/workflow/open_from_disk.png)

## Ein zuletzt verwendetes Projekt öffnen {#open-a-recent-project}

Sobald du ein Projekt einmal geöffnet hast, erscheint es in der Liste der zuletzt verwendeten Projekte. Die Liste zeigt die Projekte an, an denen du zuletzt gearbeitet hast. Du kannst jedes dieser Projekte schnell öffnen, indem du es in der Liste doppelt anklickst.
