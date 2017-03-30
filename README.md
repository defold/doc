# Defold manuals

This repo holds the markdown source files and assets for Defold documentation. Each language has its own subfolder in "docs".

## Dependencies

Node.js:

```sh
$ npm install
```

Publishing documentation is done with the `gsutil` which is part of the Google Cloud SDK:

```sh
$ ./install_deps
```

## Edit and preview

```sh
$ gulp watch
```

Builds all documentation for preview and opens a browser pointing to the build root. Edits to any .md manual or image is detected, rebuilt and reloaded in browser.

## Publish

Builds all docs and publishes them onto GCS.

```sh
$ gulp publish
```
