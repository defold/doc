# Defold manuals

This repo holds the markdown source files and assets for Defold documentation. Each language has its own subfolder in "docs".

## Dependencies

Node.js and Gulp:

```sh
$ brew install node
$ npm install gulp-cli -g
$ npm install
```

(Don't bother about "npm WARN deprecated" things during npm install.)

## Edit and preview

```sh
$ gulp watch
```

Builds all documentation for preview and opens a browser pointing to the build root. Edits to any .md manual or image is detected, rebuilt and reloaded in browser.

## Build and publish

```sh
$ gulp build
$ ./publish_sh
```

Publishing documentation to GCS is done with the `gsutil` which is part of the Google Cloud SDK. It's automatically installed if needed.

## Installing Google Cloud SDK & Getting access

1. Go to https://cloud.google.com/sdk/docs/quickstart-macos and download the correct package.
2. Run the `install.sh` script.
3. Run `gcloud init` logging into your King account (`...@king.com`).
4. Select the `defold-web` project when asked which should be the active project. If you don't see it in the list ask Samuel or Jonas about access.
5. Everything should be OK now and you should have permission to run the `./publish_sh` script.
