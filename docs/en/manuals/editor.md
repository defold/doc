---
title: Editor overview
brief: This manual gives an overview on how the Defold editor look and works, and how to navigate in it.
---

# Editor overview

The editor allows you to browse and manipulate all files in your game project in an efficient manner. Editing files brings up a suitable editor and shows all relevant information about the file in separate views.

## Starting the editor

When you run the Defold editor, you are presented with a project selection and creation screen. Click to select what you want to do:

Home
: Click to show your recently opened projects so you can quickly access them. This is the default view.

New Project
: Click if you want to create a new Defold project, then select if you want to base your project on a basic template (from the *From Template* tab), if you would like to follow a tutorial (the *From Tutorial* tab), or try one of the sample projects (the *From Sample* tab).

  ![new project](images/editor/new_project.png){srcset="images/editor/new_project@2x.png 2x"}

  When you create a new project it is stored on your local drive and any edits you do are saved locally.

You can learn more about the different options in the [Project Setup manual](https://www.defold.com/manuals/project-setup/).

## The editor panes

The Defold editor is separated into a set of panes, or views, that display specific information.

![Editor 2](images/editor/editor2_overview.png)

The *Assets* pane
: Lists all the files that are part of your project. Click and scroll to navigate the list. All file oriented operations can be made in this view:

   - <kbd>Double click</kbd> a file to open it in an editor for that file type.
   - <kbd>Drag and drop</kbd> to add files from elsewhere on your disk to the project or move files and folders to new locations in the project.
   - <kbd>Right click</kbd> to open a _context menu_ from where you can create new files or folders, rename, delete, track file dependencies and more.

### Editor pane
The center view shows the currently open file in an editor for that file type. All visual editors allows you to change the camera view:

- Pan: <kbd>Alt + left mouse button</kbd>.
- Zoom: <kbd>Alt + Right button</kbd> (three button mouse) or <kbd>Ctrl + Mouse button</kbd> (one button). If your mouse has a scroll wheel, it can be used to zoom.
- Rotate in 3D: <kbd>Ctrl + left mouse button</kbd>.

There is a toolbar in the top right corner of the scene view where you find object manipulation tools: *Move*, *Rotate* and *Scale* as well as *Camera Perspective* and *Visibility Filters*.

![toolbar](images/editor/toolbar.png)

### Outline pane

This view shows the content of the file currently being edited, but in a hierarchical tree structure. The outline reflects the editor view and allows you to perform operations on your items:
   - <kbd>Click</kbd> to select an item. Hold <kbd>Shift</kbd> or <kbd>Option</kbd> to expand the selection.
   - <kbd>Drag and drop</kbd> to move items. Drop a game object on another game object in a collection to child it.
   - <kbd>Right click</kbd> to open a _context menu_ from where you can add items, delete selected items etc.

It is possible to toggle the visibility of game objects and visual components by clicking on the little eye icon to the right of an element in the list (Defold 1.9.8 and newer).

![toolbar](images/editor/outline.png)

### Properties pane

This view shows properties associated with the currently selected item, like Position, Rotation, Animation etc, etc.

### Tools pane

This view has several tabs. The *Console* tab shows any error output or purposeful printing that you do while your game is running. Alongside the console are tabs containing *Build Errors*, *Search Results* and the *Curve Editor* which is used when editing curves in the particle editor. The Tools pane is also used for interacting with the integrated debugger.

### Changed Files pane

If your project uses the distributed version-control system Git this view lists any files that has been changed, added or deleted in your project. By synchronizing the project regularly you can bring your local copy in sync with what is stored in the project Git repository, that way you can collaborate within a team, and you won’t lose your work if disaster strikes. You can learn more about Git in our [Version Control manual](/manuals/version-control/). Some file oriented operations can be performed in this view:

   - <kbd>Double click</kbd> a file to open a diff view of the file. The editor opens the file in a suitable editor, just like in the assets view.
   - <kbd>Right click</kbd> a file to open a pop up menu from where you can open a diff view, revert all changes done to the file, find the file on the filesystem and more.


## Side-by-side editing

If you have multiple files open, a separate tab for each file is shown at the top of the editor view. It is possible to open 2 editor views side by side. <kbd>Right click</kbd> the tab for the editor you want to move and select <kbd>Move to Other Tab Pane</kbd>.

![2 panes](images/editor/2-panes.png){srcset="images/editor/2-panes@2x.png 2x"}

You can also use the tab menu to swap the position of the two panes and join them to a single pane.

## The scene editor

Double clicking a collection or game object file brings up the *Scene Editor*:

![Select object](images/editor/select.png)

### Selecting objects
Click on objects in the main window to select them. The rectangle surrounding the object in the editor view will highlight green to indicate what item is selected. The selected object is also highlighted in the *Outline* view.

  You can also select objects by:

  - <kbd>Click and drag</kbd> to select all objects inside the selection region.
  - <kbd>Click</kbd> objects in the Outline view.

  Hold <kbd>Shift</kbd> or <kbd>⌘</kbd> (Mac) / <kbd>Ctrl</kbd> (Win/Linux) while clicking to expand the selection.

### Move tool
![Move tool](images/editor/icon_move.png){.left}
To move objects, use the *Move Tool*. You find it in the toolbar in the top right corner of the scene editor, or by pressing the <kbd>W</kbd> key.

![Move object](images/editor/move.png)

The selected object shows a set of manipulators (squares and arrows). Click and drag the green center square handle to move the object freely in screen space, click and drag the arrows to move the object along the X, Y or Z-axis. There are also square handles for moving the object in the X-Y plane and (visible if rotating the camera in 3D) for moving the object in the X-Z and Y-Z planes.

### Rotate tool
![Rotate tool](images/editor/icon_rotate.png){.left}
To rotate objects, use the *Rotate Tool* by selecting it in the toolbar, or by pressing the <kbd>E</kbd> key.

![Move object](images/editor/rotate.png)

This tool consists of four circular manipulators. An orange manipulator that rotates the object in screen space and one for rotation around each of the X, Y and Z axes. Since the view is perpendicular to the X- and Y-axis, the circles only appear as two lines crossing the object.


### Scale tool
![Scale tool](images/editor/icon_scale.png){.left}
To scale objects, use the *Scale Tool* by selecting it in the toolbar, or by pressing the <kbd>R</kbd> key.

![Scale object](images/editor/scale.png)

This tool consists of a set of square handles. The center one scales the object uniformly in all axes (including Z). There also one handle for scaling along each of the X, Y and Z axes and one handle for scaling in the X-Y plane, the X-Z plane and the Y-Z plane.


### Visibility filters
Toggle visibility of various component types as well as bounding boxes and guide lines.

![Visibility filters](images/editor/visibilityfilters.png)


## Creating new project files

To create new resource files, either select <kbd>File ▸ New...</kbd> and then choose the file type from the menu, or use the context menu:

<kbd>Right click</kbd> the target location in the *Assets* browser, then select <kbd>New... ▸ [file type]</kbd>:

![create file](images/editor/create_file.png){srcset="images/editor/create_file@2x.png 2x"}

Type a suitable name for the new file. The full file name including the file type suffix is shown under *Path* in the dialog:

![create file name](images/editor/create_file_name.png){srcset="images/editor/create_file_name@2x.png 2x"}

It is possible to specify custom templates for each project. To do so, create a new folder named `templates` in the project’s root directory, and add new files named `default.*` with the desired extensions, such as `/templates/default.gui` or `/templates/default.script`. Additionally, if the `{{NAME}}` token is used in these files, it will be replaced with the filename specified in the file creation window.

## Importing files to your project

To add asset files (images, sounds, models etc) to your project, simply drag and drop them to the correct position in the *Assets* browser. This will make _copies_ of the files at the selected location in the project file structure. Read more about [how to import assets in our manual](/manuals/importing-assets/).

![Import files](images/editor/import.png){srcset="images/editor/import@2x.png 2x"}

## Updating the editor

The editor will automatically check for updates. When an update is detected it will be shown in the lower right corner of the editor window and on the project selection screen. Pressing the Update Available link will download and update the editor.

![Update from project selection](images/editor/update-project-selection.png){srcset="images/editor/update-project-selection@2x.png 2x"}

![Update from editor](images/editor/update-main.png){srcset="images/editor/update-main@2x.png 2x"}

## Preferences

You can modify the settings of the editor [from the Preferences window](/manuals/editor-preferences).

## Keyboard shortcuts

Keyboard shortcuts and how to customize them can be seen in the [keyboard shortcut manual](/manuals/editor-keyboard-shortcuts).

## Editor logs
If you run into a problem with the editor and need to [report an issue](/manuals/getting-help/#getting-help) it is a good idea to provide log files from the editor itself. The editor logs files can be found here:

  * Windows: `C:\Users\ **Your Username** \AppData\Local\Defold`
  * macOS: `/Users/ **Your Username** /Library/Application Support/` or `~/Library/Application Support/Defold`
  * Linux: `$XDG_STATE_HOME/Defold` or `~/.local/state/Defold`

You can also get access to editor logs while the editor is running if it is started from a terminal/command prompt. To launch the editor from the terminal on macOS:

```
$ > ./path/to/Defold.app/Contents/MacOS/Defold
```


## FAQ
:[Editor FAQ](../shared/editor-faq.md)
