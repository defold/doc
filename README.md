# Defold manuals

This repo holds the markdown source files and assets for Defold documentation. The files are processed by the Defold site project at https://www.github.com/defold/defold.github.io.

The www.defold.com site is automatically rebuilt via a `repository_dispatch` event generated from [this workflow](https://github.com/defold/doc/blob/master/.github/workflows/trigger-site-rebuild.yml) when changes are pushed to the this repository.

## Information for translators

If you wish to contribute translations in your language we happily accept pull requests. Start by [forking the repository](https://docs.github.com/en/github/getting-started-with-github/fork-a-repo). The English master documentation and the translations can be found in the [docs folder](https://github.com/defold/doc/tree/master/docs). If your language doesn't already exist then create a new folder with the [two-letter language code](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) for your language (zh for Chinese, pt for Portuguese etc) and a sub-folder named "manuals". You are now ready to start translating the manuals!

Translate the manuals found in the English master documentation (i.e. in "docs/en/manuals") one-by-one. Start by translating the [introduction.md](https://github.com/defold/doc/blob/master/docs/en/manuals/introduction.md) and then proceed with the pages such as [addressing.md](https://github.com/defold/doc/blob/master/docs/en/manuals/addressing.md), [building-blocks.md](https://github.com/defold/doc/blob/master/docs/en/manuals/building-blocks.md) and any of the other pages describing the basics of the engine.

NOTE: Please do not contribute machine translated manuals!
