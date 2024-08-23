Custom resources are bundled in the main game archive using the [*Custom Resources* field](https://defold.com/manuals/project-settings/#custom-resources) in *game.project*.

The *Custom Resources* field should contain a comma separated list of resources that will be included in the main game archive. If directories are specified, all files and directories in that directory are recursively included. You can read the files using [`sys.load_resource()`](/ref/sys/#sys.load_resource).
