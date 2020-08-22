# Defold manuals

This repo holds the markdown source files and assets for Defold documentation. The files are processed by the Defold site project at https://www.github.com/defold/defold.github.io.

The www.defold.com site is automatically rebuilt via a `repository_dispatch` event generated from [this workflow](https://github.com/defold/doc/blob/master/.github/workflows/trigger-site-rebuild.yml) when changes are pushed to the this repository.

## Information for translators

If you wish to contribute translations in your language we happily accept pull requests! Please read the following sections to learn how to get started, what to translate and so on.

### Getting started as a translator
Start by [forking the repository](https://docs.github.com/en/github/getting-started-with-github/fork-a-repo). The English master documentation and the translations can be found in the [docs folder](https://github.com/defold/doc/tree/master/docs). If your language doesn't already exist then create a new folder with the [two-letter language code](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) for your language (zh for Chinese, pt for Portuguese etc) and a sub-folder named "manuals". You are now ready to start translating the manuals!


### What to translate
Translate the manuals found in the English master documentation (i.e. in "docs/en/manuals") one-by-one. Start by translating the [introduction.md](https://github.com/defold/doc/blob/master/docs/en/manuals/introduction.md) and then proceed with the pages such as [addressing.md](https://github.com/defold/doc/blob/master/docs/en/manuals/addressing.md), [building-blocks.md](https://github.com/defold/doc/blob/master/docs/en/manuals/building-blocks.md) and any of the other pages describing the basics of the engine.

NOTE: Please do not contribute machine translated manuals!

#### Translate important concepts
It is recommended to translate but also show the English words for key concept of the Defold engine such as "game object", "collection", "factory" and "component":

Examples for Polish:

* obiekty gry (ang. game object)
* pełnomocnik kolekcji (ang. collection proxy)
* fabryka (ang. factory)

#### Do NOT translate keyboard shortcuts
Do not translate things such as keyboard shortcuts as those are still in English in the editor:

```
<kbd>Edit ▸ World Space</kbd>;
```

#### Translate user actions
You should however translate actions the user should perform:

```
<kbd>drag</kbd> and <kbd>drop</kbd>
    
-- Polish
<kbd>przeciągnij</kbd> i <kbd>upuść</kbd>
```

#### Translate links
Markdown links should be translated:

```
[addressing manual](/manuals/addressing)

-- Polish
[Instrukcji adresowania](/manuals/addressing)
```

#### Do NOT translate API functions
References to Defold API functions, messages or ids should not be translated:

```
`init()`, `update()`, `on_message()`, `go.animate()` etc
`set_parent`, `enable`, `disable` etc
`bean`, `buddy`, `controller`, `team_1` etc
```


#### Do NOT translate code snippets
Comments in code snippets should not be translated
