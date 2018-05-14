# Defold manuals

This repo holds the markdown source files and assets for Defold documentation. Each language has its own subfolder in "docs".

## Dependencies

Node.js and Gulp:

```sh
$ brew install node
$ npm install gulp-cli -g
$ npm install gulp -g
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
