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

The *Editor* pane

: The center view shows the currently open file in an editor for that file type. All visual editors allows you to change the camera view:

- Pan: <kbd>Alt + left mouse button</kbd>.
- Zoom: <kbd>Alt + Right button</kbd> (three button mouse) or <kbd>Ctrl + Mouse button</kbd> (one button). If your mouse has a scroll wheel, it can be used to zoom.
- Rotate in 3D: <kbd>Ctrl + left mouse button</kbd>.

There is a toolbar in the top right corner of the scene view where you find object manipulation tools: *Move*, *Rotate* and *Scale*.

![toolbar](images/editor/toolbar.png){srcset="images/editor/toolbar@2x.png 2x"}

The *Outline* pane
: This view shows the content of the file currently being edited, but in a hierarchial tree structure. The outline reflects the editor view and allows you to perform operations on your items:
   - <kbd>Click</kbd> to select an item. Hold <kbd>Shift</kbd> or <kbd>Option</kbd> to expand the selection.
   - <kbd>Drag and drop</kbd> to move items. Drop a game object on another game object in a collection to child it.
   - <kbd>Right click</kbd> to open a _context menu_ from where you can add items, delete selected items etc.

The *Properties* pane
: This view shows properties associated with the currently selected item, like Position, Rotation, Animation etc, etc.

The *Tools* pane
: This view has several tabs. The *Console* tab shows any error output or purposeful printing that you do while your game is running. Alongside the console are tabs containing *Build Errors*, *Search Results* and the *Curve Editor* which is used when editing curves in the particle editor. The Tools pane is also used for interacting with the integrated debugger.

The *Changed Files* pane
: If you project uses the distributed version-control system Git this view lists any files that has been changed, added or deleted in your project. By synchronizing the project regularly you can bring your local copy in sync with what is stored in the project Git repository, that way you can collaborate within a team, and you won’t lose your work if disaster strikes. Some file oriented operations can be performed in this view:

   - <kbd>Double click</kbd> a file to open a diff view of the file. The editor opens the file in a suitable editor, just like in the assets view.
   - <kbd>Right click</kbd> a file to open a pop up menu from where you can open a diff view, revert all changes done to the file, find the file on the filesystem and more.

## Side-by-side editing

If you have multiple files open, a separate tab for each file is shown at the top of the editor view. It is possible to open 2 editor views side by side. <kbd>Right click</kbd> the tab for the editor you want to move and select <kbd>Move to Other Tab Pane</kbd>.

![2 panes](images/editor/2-panes.png){srcset="images/editor/2-panes@2x.png 2x"}

You can also use the tab menu to swap the position of the two panes and join them to a single pane.

## The scene editor

Double clicking a collection or game object file brings up the *Scene Editor*:

![Select object](images/editor/select.jpg)

Selecting objects
: Click on objects in the main window to select them. The rectangle surrounding the object in the editor view will highlight green to indicate what item is selected. The selected object is also highlighted in the *Outline* view.

  You can also select objects by:

  - <kbd>Click and drag</kbd> to select all objects inside the selection region.
  - <kbd>Click</kbd> objects in the Outline view.

  Hold <kbd>Shift</kbd> or <kbd>⌘</kbd> (Mac) / <kbd>Ctrl</kbd> (Win/Linux) while clicking to expand the selection.

The move tool
: ![Move tool](images/editor/icon_move.png){.left}
  To move objects, use the *Move Tool*. You find it in the toolbar in the top right corner of the scene editor, or by pressing the <kbd>W</kbd> key.

  ![Move object](images/editor/move.jpg)

  The selected object shows a set of manipulators (squares and arrows). Click and drag the green center square handle to move the object freely in screen space, click and drag the arrows to move the object along the X, Y or Z-axis. There arn also square handles for moving the object in the X-Y plane and (visible if rotating the camera in 3D) for moving the object in the X-Z and Y-Z planes.

The rotate tool
: ![Rotate tool](images/editor/icon_rotate.png){.left}
  To rotate objects, use the *Rotate Tool* by selecting it in the toolbar, or by pressing the <kbd>E</kbd> key.

  ![Move object](images/editor/rotate.jpg)

  This tool consists of four circular manipulators. An orange manipulator that rotates the object in screen space and one for rotation around each of the X, Y and Z axes. Since the view is peripendicular to the X- and Y-axis, the circles only appear as two lines crossing the object.

The scale tool
: ![Scale tool](images/editor/icon_scale.png){.left}
  To scale objects, use the *Scale Tool* by selecting it in the toolbar, or by pressing the <kbd>R</kbd> key.

  ![Scale object](images/editor/scale.jpg)

  This tool consists of a set of square handles. The center one scales the object uniformly in all axes (including Z). There also one handle for scaling along each of the X, Y and Z axes and one handle for scaling in the X-Y plane, the X-Z plane and the Y-Z plane.

## Creating new project files

To create new resource files, either select <kbd>File ▸ New...</kbd> and then choose the file type from the menu, or use the context menu:

<kbd>Right click</kbd> the target location in the *Assets* browser, then select <kbd>New... ▸ [file type]</kbd>:

![create file](images/editor/create_file.png){srcset="images/editor/create_file@2x.png 2x"}

Type a suitable name for the new file. The full file name including the file type suffix is shown under *Path* in the dialog:

![create file name](images/editor/create_file_name.png){srcset="images/editor/create_file_name@2x.png 2x"}

## Importing files to your project

To add asset files (images, sounds, models etc) to your project, simply drag and drop them to the correct position in the *Assets* browser. This will make _copies_ of the files at the selected location in the project file structure. Read more about [how to import assets in our manual](/manuals/importing-assets/).

![Import files](images/editor/import.png){srcset="images/editor/import@2x.png 2x"}

## Keyboard shortcuts

### Default shortcuts

| Command | Windows | macOS | Linux |
|---------|---------|-------|-------|
| Add | <kbd>A</kbd> | <kbd>A</kbd> | <kbd>A</kbd> |
| Add secondary | <kbd>Shift</kbd>+<kbd>A</kbd> | <kbd>Shift</kbd>+<kbd>A</kbd> | <kbd>Shift</kbd>+<kbd>A</kbd> |
| Backwards tab trigger | <kbd>Shift</kbd>+<kbd>Tab</kbd> | <kbd>Shift</kbd>+<kbd>Tab</kbd> | <kbd>Shift</kbd>+<kbd>Tab</kbd> |
| Beginning of file | <kbd>Ctrl</kbd>+<kbd>Home</kbd> | <kbd>Cmd</kbd>+<kbd>Up</kbd> | <kbd>Ctrl</kbd>+<kbd>Home</kbd> |
| Beginning of line |  | <kbd>Ctrl</kbd>+<kbd>A</kbd> |  |
| Beginning of line text | <kbd>Home</kbd> | <kbd>Home</kbd> | <kbd>Home</kbd> |
| Build | <kbd>Ctrl</kbd>+<kbd>B</kbd> | <kbd>Cmd</kbd>+<kbd>B</kbd> | <kbd>Ctrl</kbd>+<kbd>B</kbd> |
| Close | <kbd>Ctrl</kbd>+<kbd>W</kbd> | <kbd>Cmd</kbd>+<kbd>W</kbd> | <kbd>Ctrl</kbd>+<kbd>W</kbd> |
| Close all | <kbd>Shift</kbd>+<kbd>Ctrl</kbd>+<kbd>W</kbd> | <kbd>Shift</kbd>+<kbd>Cmd</kbd>+<kbd>W</kbd> | <kbd>Shift</kbd>+<kbd>Ctrl</kbd>+<kbd>W</kbd> |
| Continue | <kbd>F5</kbd> | <kbd>F5</kbd> | <kbd>F5</kbd> |
| Copy | <kbd>Ctrl</kbd>+<kbd>C</kbd> | <kbd>Cmd</kbd>+<kbd>C</kbd> | <kbd>Ctrl</kbd>+<kbd>C</kbd> |
| Cut | <kbd>Ctrl</kbd>+<kbd>X</kbd> | <kbd>Cmd</kbd>+<kbd>X</kbd> | <kbd>Ctrl</kbd>+<kbd>X</kbd> |
| Delete | <kbd>Delete</kbd> | <kbd>Delete</kbd> | <kbd>Delete</kbd> |
| Delete backward | <kbd>Backspace</kbd> | <kbd>Backspace</kbd> | <kbd>Backspace</kbd> |
| Delete line |  | <kbd>Ctrl</kbd>+<kbd>D</kbd> |  |
| Delete next word | <kbd>Ctrl</kbd>+<kbd>Delete</kbd> | <kbd>Alt</kbd>+<kbd>Delete</kbd> | <kbd>Ctrl</kbd>+<kbd>Delete</kbd> |
| Delete prev word | <kbd>Ctrl</kbd>+<kbd>Backspace</kbd> | <kbd>Alt</kbd>+<kbd>Backspace</kbd> | <kbd>Ctrl</kbd>+<kbd>Backspace</kbd> |
| Delete to end of line | <kbd>Shift</kbd>+<kbd>Ctrl</kbd>+<kbd>Delete</kbd> | <kbd>Cmd</kbd>+<kbd>Delete</kbd> | <kbd>Shift</kbd>+<kbd>Ctrl</kbd>+<kbd>Delete</kbd> |
| Documentation | <kbd>F1</kbd> | <kbd>F1</kbd> | <kbd>F1</kbd> |
| Down | <kbd>Down</kbd> | <kbd>Down</kbd> | <kbd>Down</kbd> |
| End of file | <kbd>Ctrl</kbd>+<kbd>End</kbd> | <kbd>Cmd</kbd>+<kbd>Down</kbd> | <kbd>Ctrl</kbd>+<kbd>End</kbd> |
| End of line | <kbd>End</kbd> | <kbd>Ctrl</kbd>+<kbd>E</kbd> | <kbd>End</kbd> |
| Enter | <kbd>Enter</kbd> | <kbd>Enter</kbd> | <kbd>Enter</kbd> |
| Erase tool | <kbd>Shift</kbd>+<kbd>E</kbd> | <kbd>Shift</kbd>+<kbd>E</kbd> | <kbd>Shift</kbd>+<kbd>E</kbd> |
| Escape | <kbd>Esc</kbd> | <kbd>Esc</kbd> | <kbd>Esc</kbd> |
| Find next | <kbd>Ctrl</kbd>+<kbd>G</kbd> | <kbd>Cmd</kbd>+<kbd>G</kbd> | <kbd>Ctrl</kbd>+<kbd>G</kbd> |
| Find prev | <kbd>Shift</kbd>+<kbd>Ctrl</kbd>+<kbd>G</kbd> | <kbd>Shift</kbd>+<kbd>Cmd</kbd>+<kbd>G</kbd> | <kbd>Shift</kbd>+<kbd>Ctrl</kbd>+<kbd>G</kbd> |
| Find text | <kbd>Ctrl</kbd>+<kbd>F</kbd> | <kbd>Cmd</kbd>+<kbd>F</kbd> | <kbd>Ctrl</kbd>+<kbd>F</kbd> |
| Frame selection | <kbd>F</kbd> | <kbd>F</kbd> | <kbd>F</kbd> |
| Goto line | <kbd>Ctrl</kbd>+<kbd>L</kbd> | <kbd>Cmd</kbd>+<kbd>L</kbd> | <kbd>Ctrl</kbd>+<kbd>L</kbd> |
| Hide selected | <kbd>Ctrl</kbd>+<kbd>E</kbd> | <kbd>Cmd</kbd>+<kbd>E</kbd> | <kbd>Ctrl</kbd>+<kbd>E</kbd> |
| Hot reload | <kbd>Ctrl</kbd>+<kbd>R</kbd> | <kbd>Cmd</kbd>+<kbd>R</kbd> | <kbd>Ctrl</kbd>+<kbd>R</kbd> |
| Left | <kbd>Left</kbd> | <kbd>Left</kbd> | <kbd>Left</kbd> |
| Move down | <kbd>Alt</kbd>+<kbd>Down</kbd> | <kbd>Alt</kbd>+<kbd>Down</kbd> | <kbd>Alt</kbd>+<kbd>Down</kbd> |
| Move tool | <kbd>W</kbd> | <kbd>W</kbd> | <kbd>W</kbd> |
| Move up | <kbd>Alt</kbd>+<kbd>Up</kbd> | <kbd>Alt</kbd>+<kbd>Up</kbd> | <kbd>Alt</kbd>+<kbd>Up</kbd> |
| New file | <kbd>Ctrl</kbd>+<kbd>N</kbd> | <kbd>Cmd</kbd>+<kbd>N</kbd> | <kbd>Ctrl</kbd>+<kbd>N</kbd> |
| Next word | <kbd>Ctrl</kbd>+<kbd>Right</kbd> | <kbd>Alt</kbd>+<kbd>Right</kbd> | <kbd>Ctrl</kbd>+<kbd>Right</kbd> |
| Open | <kbd>Ctrl</kbd>+<kbd>O</kbd> | <kbd>Cmd</kbd>+<kbd>O</kbd> | <kbd>Ctrl</kbd>+<kbd>O</kbd> |
| Open asset | <kbd>Shift</kbd>+<kbd>Ctrl</kbd>+<kbd>R</kbd> | <kbd>Cmd</kbd>+<kbd>P</kbd> | <kbd>Shift</kbd>+<kbd>Ctrl</kbd>+<kbd>R</kbd> |
| Page down | <kbd>Page Down</kbd> | <kbd>Page Down</kbd> | <kbd>Page Down</kbd> |
| Page up | <kbd>Page Up</kbd> | <kbd>Page Up</kbd> | <kbd>Page Up</kbd> |
| Paste | <kbd>Ctrl</kbd>+<kbd>V</kbd> | <kbd>Cmd</kbd>+<kbd>V</kbd> | <kbd>Ctrl</kbd>+<kbd>V</kbd> |
| Preferences | <kbd>Ctrl</kbd>+<kbd>Comma</kbd> | <kbd>Cmd</kbd>+<kbd>Comma</kbd> | <kbd>Ctrl</kbd>+<kbd>Comma</kbd> |
| Prev word | <kbd>Ctrl</kbd>+<kbd>Left</kbd> | <kbd>Alt</kbd>+<kbd>Left</kbd> | <kbd>Ctrl</kbd>+<kbd>Left</kbd> |
| Proposals | <kbd>Ctrl</kbd>+<kbd>Space</kbd> | <kbd>Ctrl</kbd>+<kbd>Space</kbd> | <kbd>Ctrl</kbd>+<kbd>Space</kbd> |
| Quit | <kbd>Ctrl</kbd>+<kbd>Q</kbd> | <kbd>Cmd</kbd>+<kbd>Q</kbd> | <kbd>Ctrl</kbd>+<kbd>Q</kbd> |
| Realign camera | <kbd>Period</kbd> | <kbd>Period</kbd> | <kbd>Period</kbd> |
| Rebuild | <kbd>Shift</kbd>+<kbd>Ctrl</kbd>+<kbd>B</kbd> | <kbd>Shift</kbd>+<kbd>Cmd</kbd>+<kbd>B</kbd> | <kbd>Shift</kbd>+<kbd>Ctrl</kbd>+<kbd>B</kbd> |
| Rebundle | <kbd>Ctrl</kbd>+<kbd>U</kbd> | <kbd>Cmd</kbd>+<kbd>U</kbd> | <kbd>Ctrl</kbd>+<kbd>U</kbd> |
| Redo | <kbd>Shift</kbd>+<kbd>Ctrl</kbd>+<kbd>Z</kbd> | <kbd>Shift</kbd>+<kbd>Cmd</kbd>+<kbd>Z</kbd> | <kbd>Shift</kbd>+<kbd>Ctrl</kbd>+<kbd>Z</kbd> |
| Reindent | <kbd>Ctrl</kbd>+<kbd>I</kbd> | <kbd>Ctrl</kbd>+<kbd>I</kbd> | <kbd>Ctrl</kbd>+<kbd>I</kbd> |
| Reload stylesheet |  | <kbd>Ctrl</kbd>+<kbd>R</kbd> |  |
| Rename | <kbd>F2</kbd> | <kbd>F2</kbd> | <kbd>F2</kbd> |
| Replace next | <kbd>Shift</kbd>+<kbd>Ctrl</kbd>+<kbd>H</kbd> | <kbd>Alt</kbd>+<kbd>Cmd</kbd>+<kbd>G</kbd> | <kbd>Shift</kbd>+<kbd>Ctrl</kbd>+<kbd>H</kbd> |
| Replace text |  | <kbd>Alt</kbd>+<kbd>Cmd</kbd>+<kbd>F</kbd> |  |
| Right | <kbd>Right</kbd> | <kbd>Right</kbd> | <kbd>Right</kbd> |
| Rotate tool | <kbd>E</kbd> | <kbd>E</kbd> | <kbd>E</kbd> |
| Save all | <kbd>Ctrl</kbd>+<kbd>S</kbd> | <kbd>Cmd</kbd>+<kbd>S</kbd> | <kbd>Ctrl</kbd>+<kbd>S</kbd> |
| Scale tool | <kbd>R</kbd> | <kbd>R</kbd> | <kbd>R</kbd> |
| Scene stop | <kbd>Ctrl</kbd>+<kbd>T</kbd> | <kbd>Cmd</kbd>+<kbd>T</kbd> | <kbd>Ctrl</kbd>+<kbd>T</kbd> |
| Search in files | <kbd>Shift</kbd>+<kbd>Ctrl</kbd>+<kbd>F</kbd> | <kbd>Shift</kbd>+<kbd>Cmd</kbd>+<kbd>F</kbd> | <kbd>Shift</kbd>+<kbd>Ctrl</kbd>+<kbd>F</kbd> |
| Select all | <kbd>Ctrl</kbd>+<kbd>A</kbd> | <kbd>Cmd</kbd>+<kbd>A</kbd> | <kbd>Ctrl</kbd>+<kbd>A</kbd> |
| Select beginning of file | <kbd>Shift</kbd>+<kbd>Ctrl</kbd>+<kbd>Home</kbd> | <kbd>Shift</kbd>+<kbd>Cmd</kbd>+<kbd>Up</kbd> | <kbd>Shift</kbd>+<kbd>Ctrl</kbd>+<kbd>Home</kbd> |
| Select beginning of line |  | <kbd>Shift</kbd>+<kbd>Ctrl</kbd>+<kbd>A</kbd> |  |
| Select beginning of line text | <kbd>Shift</kbd>+<kbd>Home</kbd> | <kbd>Shift</kbd>+<kbd>Home</kbd> | <kbd>Shift</kbd>+<kbd>Home</kbd> |
| Select down | <kbd>Shift</kbd>+<kbd>Down</kbd> | <kbd>Shift</kbd>+<kbd>Down</kbd> | <kbd>Shift</kbd>+<kbd>Down</kbd> |
| Select end of file | <kbd>Shift</kbd>+<kbd>Ctrl</kbd>+<kbd>End</kbd> | <kbd>Shift</kbd>+<kbd>Cmd</kbd>+<kbd>Down</kbd> | <kbd>Shift</kbd>+<kbd>Ctrl</kbd>+<kbd>End</kbd> |
| Select end of line | <kbd>Shift</kbd>+<kbd>End</kbd> | <kbd>Shift</kbd>+<kbd>Alt</kbd>+<kbd>Down</kbd> | <kbd>Shift</kbd>+<kbd>End</kbd> |
| Select left | <kbd>Shift</kbd>+<kbd>Left</kbd> | <kbd>Shift</kbd>+<kbd>Left</kbd> | <kbd>Shift</kbd>+<kbd>Left</kbd> |
| Select next occurrence | <kbd>Ctrl</kbd>+<kbd>D</kbd> | <kbd>Cmd</kbd>+<kbd>D</kbd> | <kbd>Ctrl</kbd>+<kbd>D</kbd> |
| Select next word | <kbd>Shift</kbd>+<kbd>Ctrl</kbd>+<kbd>Right</kbd> | <kbd>Shift</kbd>+<kbd>Alt</kbd>+<kbd>Right</kbd> | <kbd>Shift</kbd>+<kbd>Ctrl</kbd>+<kbd>Right</kbd> |
| Select page down | <kbd>Shift</kbd>+<kbd>Page Down</kbd> | <kbd>Shift</kbd>+<kbd>Page Down</kbd> | <kbd>Shift</kbd>+<kbd>Page Down</kbd> |
| Select page up | <kbd>Shift</kbd>+<kbd>Page Up</kbd> | <kbd>Shift</kbd>+<kbd>Page Up</kbd> | <kbd>Shift</kbd>+<kbd>Page Up</kbd> |
| Select prev word | <kbd>Shift</kbd>+<kbd>Ctrl</kbd>+<kbd>Left</kbd> | <kbd>Shift</kbd>+<kbd>Ctrl</kbd>+<kbd>Left</kbd> | <kbd>Shift</kbd>+<kbd>Ctrl</kbd>+<kbd>Left</kbd> |
| Select right | <kbd>Shift</kbd>+<kbd>Right</kbd> | <kbd>Shift</kbd>+<kbd>Right</kbd> | <kbd>Shift</kbd>+<kbd>Right</kbd> |
| Show last hidden | <kbd>Shift</kbd>+<kbd>Ctrl</kbd>+<kbd>E</kbd> | <kbd>Shift</kbd>+<kbd>Cmd</kbd>+<kbd>E</kbd> | <kbd>Shift</kbd>+<kbd>Ctrl</kbd>+<kbd>E</kbd> |
| Show palette | <kbd>Space</kbd> | <kbd>Space</kbd> | <kbd>Space</kbd> |
| Split selection into lines | <kbd>Shift</kbd>+<kbd>Ctrl</kbd>+<kbd>L</kbd> | <kbd>Shift</kbd>+<kbd>Cmd</kbd>+<kbd>L</kbd> | <kbd>Shift</kbd>+<kbd>Ctrl</kbd>+<kbd>L</kbd> |
| Step into | <kbd>F11</kbd> | <kbd>F11</kbd> | <kbd>F11</kbd> |
| Step out | <kbd>Shift</kbd>+<kbd>F11</kbd> | <kbd>Shift</kbd>+<kbd>F11</kbd> | <kbd>Shift</kbd>+<kbd>F11</kbd> |
| Step over | <kbd>F10</kbd> | <kbd>F10</kbd> | <kbd>F10</kbd> |
| Stop debugger | <kbd>Shift</kbd>+<kbd>F5</kbd> |  | <kbd>Shift</kbd>+<kbd>F5</kbd> |
| Tab | <kbd>Tab</kbd> | <kbd>Tab</kbd> | <kbd>Tab</kbd> |
| Toggle breakpoint | <kbd>F9</kbd> | <kbd>F9</kbd> | <kbd>F9</kbd> |
| Toggle comment | <kbd>Ctrl</kbd>+<kbd>Slash</kbd> | <kbd>Cmd</kbd>+<kbd>Slash</kbd> | <kbd>Ctrl</kbd>+<kbd>Slash</kbd> |
| Toggle component guides | <kbd>Ctrl</kbd>+<kbd>H</kbd> | <kbd>Ctrl</kbd>+<kbd>Cmd</kbd>+<kbd>H</kbd> | <kbd>Ctrl</kbd>+<kbd>H</kbd> |
| Toggle pane bottom | <kbd>F7</kbd> | <kbd>F7</kbd> | <kbd>F7</kbd> |
| Toggle pane left | <kbd>F6</kbd> | <kbd>F6</kbd> | <kbd>F6</kbd> |
| Toggle pane right | <kbd>F8</kbd> | <kbd>F8</kbd> | <kbd>F8</kbd> |
| Toggle visibility filters | <kbd>Shift</kbd>+<kbd>Ctrl</kbd>+<kbd>I</kbd> | <kbd>Shift</kbd>+<kbd>Cmd</kbd>+<kbd>I</kbd> | <kbd>Shift</kbd>+<kbd>Ctrl</kbd>+<kbd>I</kbd> |
| Undo | <kbd>Ctrl</kbd>+<kbd>Z</kbd> | <kbd>Cmd</kbd>+<kbd>Z</kbd> | <kbd>Ctrl</kbd>+<kbd>Z</kbd> |
| Up | <kbd>Up</kbd> | <kbd>Up</kbd> | <kbd>Up</kbd> |
| Up major | <kbd>Shift</kbd>+<kbd>Up</kbd> | <kbd>Shift</kbd>+<kbd>Up</kbd> | <kbd>Shift</kbd>+<kbd>Up</kbd> |
| Zoom in | <kbd>Ctrl</kbd>+<kbd>'</kbd>+<kbd>'</kbd> | <kbd>Cmd</kbd>+<kbd>'</kbd>+<kbd>'</kbd> | <kbd>Ctrl</kbd>+<kbd>'</kbd>+<kbd>'</kbd> |
| Zoom out | <kbd>Ctrl</kbd>+<kbd>'-'</kbd> | <kbd>Cmd</kbd>+<kbd>'-'</kbd> | <kbd>Ctrl</kbd>+<kbd>'-'</kbd> |


### Customizing shortcuts

You can customize keyboard shortcuts by creating a configuration file (e.g. `keymap.edn` in your home directory). Then go into <kbd>File ▸ Preferences</kbd>, and set <kbd>Path to custom keymap</kbd> to the created file. You need to restart Defold after setting this setting, and every time you edit the keymap file.

You can see and download keymaps for: [Windows](examples/keymap_win.edn), [MacOS](examples/keymap_macos.edn) and [Linux](examples/keymap_linux.edn)

## Editor logs
If you run into a problem with the editor and need to [report an issue](/manuals/getting-help/#getting-help) it is a good idea to provide log files from the editor itself. The editor logs files can be found here:

  * Windows: `C:\Users\ **Your Username** \AppData\Local\Defold`
  * macOS: `/Users/ **Your Username** /Library/Application Support/` or `~/Library/Application Support/Defold`
  * Linux: `~/.Defold`

You can also get access to editor logs while the editor is running if it is started from a terminal/command prompt. To launch the editor from the terminal on macOS:

```
$ > ./path/to/Defold.app/Contents/MacOS/Defold
```


## FAQ
:[Editor FAQ](../shared/editor-faq.md)
