## The editor views

The Defold editor is separated into a set of panes, or views, that display specific information.

![Editor 2](../shared/images/editor2_overview.png)

The *Assets* view (*Project Explorer* in editor 1)
: Lists all the files that are part of your project. Click and scroll to navigate the list. All file oriented operations can be made in this view:

::: sidenote
Editor 1 looks different but works very much the same, only with less functionality.)
:::

   - <kbd>Double click</kbd> a file to open it in an editor for that file type.
   - <kbd>Drag and drop</kbd> to add files from elsewhere on your disk to the project or move files and folders to new locations in the project.
   - <kbd>Right click</kbd> to open a pop up menu from where you can create new files or folders, rename, delete, track file dependencies and more.

The *Editor* view

: The center view shows the currently open file in an editor for that file type. All visual editors allows you to change the camera view:

- Pan: <kbd>Alt + left mouse button</kbd>.
- Zoom: <kbd>Alt + Right button</kbd> (three button mouse) or <kbd>Ctrl + Mouse button</kbd> (one button). If your mouse has a scroll wheel, it can be used to zoom.
- Rotate in 3D: <kbd>Ctrl + left mouse button</kbd>.

::: sidenote
Panning in editor 1: <kbd>Alt + Middle button</kbd> (three button mouse) or <kbd>Ctrl + ⌘ + Mouse button</kbd> (one button mouse, Mac) or <kbd>Ctrl + Alt + Mouse button</kbd> (one button mouse, Windows/Linux). You can change the mouse type in the application preferences, under *Defold / Scene Editor* and *Mouse Type*.

Rotating in 3D is not possible in editor 1.

The menu <kbd>Scene</kbd> contains the tools to move, rotate and scale the currently selected object, options to frame the view to the current selection and to realign the camera.
:::

There is a toolbar in the top right corner of the scene view where you find object manipulation tools: *Move*, *Rotate* and *Scale*.

The *Outline*
: This view shows the content of the file currently being edited, but in a hierarchial tree structure. The outline reflects the editor view and allows you to perform operations on your items:
   - <kbd>Click</kbd> to select an item. Hold <kbd>Shift</kbd> or <kbd>Option</kbd> to expand the selection.
   - <kbd>Drag and drop</kbd> to move items. Drop a game object on another game object in a collection to child it.
   - <kbd>Right click</kbd> to open a pop up menu from where you can add items, delete selected items etc.

The *Properties* view
: This view shows properties associated with the currently selected item, like Position, Rotation, Animation etc, etc.

The *Console*
: This view shows any error output or purposeful printing that you do while your game is running. Alongside the console are tabs containing the *Curve Editor* which is used when editing curves in the particle editor, the *Build Errors* view that shows build errors, and the *Search Results* view that displays search results.

The *Changed Files* view:
: This view lists any files that has been changed, added or deleted in your project. By synchronizing the project regularly you can bring your local copy in sync with what is stored in the project Git repository, that way you can collaborate within a team, and you won’t lose your work if unfortune strikes. Some file oriented operations can be performed in this view:

   - <kbd>Double click</kbd> a file to open a diff view of the file. Editor 2 opens the file in a suitable editor, just like in the assets view.
   - <kbd>Right click</kbd> a file to open a pop up menu from where you can open a diff view, revert all changes done to the file, find the file on the filesystem and more (editor 2).
