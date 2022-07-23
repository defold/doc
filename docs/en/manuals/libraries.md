---
title: Working with library projects in Defold
brief: The Libraries feature allows you to share assets between projects. This manual explains how it works.
---

# Libraries

The Libraries feature allows you to share assets between projects. It is a simple but very powerful mechanism that you can use in your workflow in a number of ways.

Libraries are useful for the following purposes:

* To copy assets from a finished project to a new one. If you are making a sequel to an earlier game, this is an easy way to get going.
* To build a library of templates that you can copy into you projects and then customize or specialize.
* To build one or more libraries of ready-made objects or scripts that you can reference directly. This is very handy for storing common script modules or to build a shared library of graphics, sound and animation assets.

## Setting up library sharing

Suppose you want to build a library containing shared sprites and tile sources. You start by [setting up a new project](/manuals/project-setup/). Decide what folders you want to share from the project and add the names of those folders to the *include_dirs* property in the Project settings. If you want to list more than one folder, separate the names with spaces:

![Include dirs](images/libraries/libraries_include_dirs.png)

Before we can add this library to another project we need to a way to locate the library.

## Library URL

Libraries are referred to via a standard URL. For a project hosted on GitHub it would be the URL to a project release:

![GitHub Library URL](images/libraries/libraries_library_url_github.png)

::: important
It is recommend to always depend on a specific release of a library project instead of on the master branch. This way it is up to you as a developer to decide when to incorporate changes from a library project as opposed to always getting the latest (and potentially breaking) changes from the master branch of a library project.
:::


### Basic access authentication

It is possible to add a username and password/token to the library URL to perform basic access authentication when using libraries that are not publicly available:

```
https://username:password@github.com/defold/private/archive/main.zip
```

The `username` and `password` fields will be extracted and added as an `Authorization` request header. This works for any server which supports basic access authorization. It can also be used to fetch libraries from private repositories hosted on GitHub. In the case of GitHub you need to [generate a personal access token](https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/creating-a-personal-access-token) and use that as your password.

```
https://github-username:personal-access-token@github.com/defold/private/archive/main.zip
```

::: important
Make sure to not share or accidentally leak your generated personal access token or password as it can have dire consequences if they fall into the wrong hands!
:::

To avoid accidentally leaking any credentials by having them in clear text in the library URL it is also possible to use a string replacement pattern and store the credentials as environment variables:

```
https://__PRIVATE_USERNAME__:__PRIVATE_TOKEN__@github.com/defold/private/archive/main.zip
```

In the above example the username and token will be read from the system environment variables `PRIVATE_USERNAME` and `PRIVATE_TOKEN`.


### Advanced access authentication

When using the basic access authentication a user's access token and username will be shared on any repository used for the project.  With a greater than 1 man team this can be an issue. To solve this issue a "read only" user needs to be used for library access to the repository, on GitHub this requires an organisation, a team and a user who doesn't need to edit the repo (hence read only).

GitHub Steps:
* [Create an organisation](https://docs.github.com/en/github/setting-up-and-managing-organizations-and-teams/creating-a-new-organization-from-scratch)
* [Create a team within the organisation](https://docs.github.com/en/github/setting-up-and-managing-organizations-and-teams/creating-a-team)
* [Transfer the desired private repository to your organisation](https://docs.github.com/en/github/administering-a-repository/transferring-a-repository)
* [Give the team "read only" access to the repository](https://docs.github.com/en/github/setting-up-and-managing-organizations-and-teams/managing-team-access-to-an-organization-repository)
* [Create or select a user to be part of this team](https://docs.github.com/en/github/setting-up-and-managing-organizations-and-teams/organizing-members-into-teams)
* Use the "basic access authentication" above to create a personal access token for this user

At this point the new user's authentication details can be committed and pushed to the repository.  This will allow anyone working with your private repository to fetch it as a library without having edit permissions to the library itself.

::: important
The read only user's token is fully accessible to anyone who can access the game repositories that are using the library.
:::

This solution was proposed on the Defold forum and [discussed in this thread](https://forum.defold.com/t/private-github-for-library-solved/67240).

## Setting up library dependencies

Open the project that you would like to access the library from. In the project settings, add the Library URL to the *dependencies* property. You can specify multiple dependent projects if you want. Just add them one by one using the `+` button and remove using the `-` button:

![Dependencies](images/libraries/libraries_dependencies.png)

Now, select <kbd>Project ▸ Fetch Libraries</kbd> to update library dependencies. This happens automatically whenever you open a project so you will only need to do this if the dependencies change without re-opening the project. This happens if you add or remove dependency libraries or if one of the dependency library projects is changed and synchronized by someone.

![Fetch Libraries](images/libraries/libraries_fetch_libraries.png)

Now the folders that you shared appear in the *Assets pane* and you can use everything you shared. Any synchronized changes done to the library project will be available in your project.

![Library setup done](images/libraries/libraries_done.png)

## Broken references

Library sharing only includes files that are located under the shared folder(s). If you create something that references assets that are located outside of the shared hierarchy, the reference paths will be broken.

## Name collisions

Since you can list several project URLs in the *dependencies* project setting you might encounter a name collision. This happens if two or more of the dependent projects share a folder with the same name in the *include_dirs* project setting.

Defold resolves name collisions by simply ignoring all but the last reference to folders of the same name in the order the project URLs are specified in the *dependencies* list. For instance. If you list 3 library project URLs in the dependencies and all of them share a folder named *items*, only one *items* folder will show up---the one belonging to the project that is last in the URL list.
