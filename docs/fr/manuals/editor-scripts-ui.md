---
title: "Scripts de l'éditeur : interface utilisateur"
brief: Ce manuel explique comment créer des éléments d'interface utilisateur dans l'éditeur à l'aide de Lua
---

# Scripts de l'éditeur et interface utilisateur {#editor-scripts-and-ui}

Ce manuel explique comment créer des boîtes de dialogue interactives et ouvrir des ressources dans l'éditeur à l'aide de scripts d'éditeur écrits en Lua. Pour commencer avec les scripts d'éditeur, consultez le [manuel des scripts d'éditeur](/manuals/editor-scripts). La référence complète de l'API de l'éditeur se trouve [ici](/ref/stable/editor-lua/).

## Bonjour tout le monde {#hello-world}

Toutes les fonctionnalités liées à l'interface se trouvent dans le module `editor.ui`. Voici un exemple minimal de script de l'éditeur avec une interface personnalisée pour commencer :
```lua
local M = {}

function M.get_commands()
    return {
        {
            label = "Do with confirmation",
            locations = {"View"},
            run = function()
                local result = editor.ui.show_dialog(editor.ui.dialog({
                    title = "Perform action?",
                    buttons = {
                        editor.ui.dialog_button({
                            text = "Cancel",
                            cancel = true,
                            result = false
                        }),
                        editor.ui.dialog_button({
                            text = "Perform",
                            default = true,
                            result = true
                        })
                    }
                }))
                print('Perform action:', result)
            end
        }
    }
end

return M

```

Cet extrait de code définit une commande **View → Do with confirmation**. Lorsque vous l'exécutez, la boîte de dialogue suivante s'affiche :

![Boîte de dialogue du premier exemple](images/editor_scripts/perform_action_dialog.png)

Enfin, après avoir appuyé sur <kbd>Enter</kbd> (ou cliqué sur le bouton `Perform`), vous verrez la ligne suivante dans la console de l'éditeur :
```
Perform action:	true
```

## Ouverture de ressources {#opening-resources}

Appelez `editor.ui.open_resource()` depuis la fonction `run` d'une commande pour ouvrir une ressource du projet. Le chemin commence par `/`. Si vous omettez la vue, la vue principale de la ressource est sélectionnée :

```lua
editor.ui.open_resource("/main/main.script")
```

Les vues `code` et `text` acceptent une position de curseur ou une sélection en troisième argument. Les numéros de ligne et de colonne commencent à `1` ; une colonne omise vaut `1` par défaut. Précisez la vue lorsque vous passez ces arguments :

```lua
editor.ui.open_resource("/main/main.script", "code", { line = 10 })
editor.ui.open_resource("/main/main.script", "code", { line = 10, column = 5 })
```

Pour sélectionner une plage, fournissez plutôt les positions de curseur `from` et `to` :

```lua
editor.ui.open_resource("/main/main.script", "code", {
    from = { line = 10, column = 1 },
    to = { line = 12, column = 1 }
})
```

La vue configurée pour la ressource peut s'ouvrir dans l'éditeur ou dans une application externe. Les vues intégrées Code et Text prennent en charge les arguments de curseur et de sélection. Consultez [`editor.ui.open_resource()`](/ref/beta/editor/#editor.ui.open_resource:resource_path-view-args) pour connaître les noms de vues pris en charge.

## Concepts de base {#basic-concepts}

### Composants {#components}

L'éditeur propose différents **composants** (components) d'interface que vous pouvez combiner pour créer l'interface souhaitée. Par convention, tous les composants sont configurés à l'aide d'une seule table appelée **props**. Les composants eux-mêmes ne sont pas des tables, mais des **userdata immuables** que l'éditeur utilise pour créer l'interface.

### Propriétés (props) {#props}

Les **props** sont des tables qui définissent les données d'entrée des composants. Les props doivent être traitées comme immuables : modifier la table de props sur place ne provoque pas un nouveau rendu du composant, contrairement à l'utilisation d'une autre table. L'interface est mise à jour lorsque l'instance du composant reçoit une table de props dont la comparaison superficielle avec la précédente indique une différence.

### Alignement {#alignment}

Lorsqu'une zone est attribuée au composant dans l'interface, il en occupe tout l'espace, sans que sa partie visible s'étire nécessairement. La partie visible occupe uniquement l'espace dont elle a besoin, puis s'aligne dans la zone attribuée. C'est pourquoi la plupart des composants intégrés définissent une prop `alignment`.

Considérons par exemple ce composant de libellé :
```lua
editor.ui.label({
    text = "Hello",
    alignment = editor.ui.ALIGNMENT.RIGHT
})
```
La partie visible est le texte `Hello`, qui s'aligne dans la zone attribuée au composant :

![Alignement](images/editor_scripts/alignment.png)

## Composants intégrés {#built-in-components}

L'éditeur définit différents composants intégrés que vous pouvez utiliser ensemble pour construire l'interface. On peut globalement les répartir en trois catégories : mise en page, présentation des données et saisie.

### Composants de mise en page {#layout-components}

Les composants de mise en page servent à placer d'autres composants les uns à côté des autres. Les principaux sont **`horizontal`**, **`vertical`** et **`grid`**. Ces composants définissent aussi des props telles que **padding** et **spacing** : padding correspond à la marge intérieure, c'est-à-dire l'espace vide entre le bord de la zone attribuée et le contenu, tandis que spacing correspond à l'espacement entre les enfants :

![Marge intérieure et espacement](images/editor_scripts/padding_and_spacing.png)

L'éditeur définit les constantes `small`, `medium` et `large` pour les marges intérieures et les espacements. Pour l'espacement, `small` est destiné à séparer les différentes parties d'un même élément d'interface, `medium` sépare les éléments d'interface individuels et `large` sépare les groupes d'éléments. L'espacement par défaut est `medium`. Une marge intérieure de `large` correspond à l'espace entre les bords de la fenêtre et le contenu, `medium` à la marge depuis les bords d'un élément d'interface important, et `small` à la marge depuis les bords de petits éléments d'interface comme les menus contextuels et les infobulles (pas encore implémentés).

Un conteneur **`horizontal`** place ses enfants les uns après les autres horizontalement, en faisant toujours occuper à chaque enfant toute la hauteur disponible. Par défaut, la largeur de chaque enfant est maintenue au minimum, mais vous pouvez lui faire occuper autant d'espace que possible en définissant sa prop `grow` sur `true`.

Un conteneur **`vertical`** est similaire au conteneur horizontal, mais avec les axes inversés.

Enfin, **`grid`** est un composant conteneur qui dispose ses enfants dans une grille en deux dimensions, comme un tableau. Le paramètre `grow` d'une grille s'applique aux lignes ou aux colonnes ; il est donc défini dans la table de configuration des colonnes, et non sur un enfant. Les enfants d'une grille peuvent également être configurés pour s'étendre sur plusieurs lignes ou colonnes grâce aux props `row_span` et `column_span`. Les grilles sont utiles pour créer des formulaires à plusieurs champs de saisie :
```lua
editor.ui.grid({
    padding = editor.ui.PADDING.LARGE, -- add padding around dialog edges
    columns = {{}, {grow = true}}, -- make 2nd column grow
    children = {
        {
            editor.ui.label({ 
                text = "Level Name",
                alignment = editor.ui.ALIGNMENT.RIGHT
            }),
            editor.ui.string_field({})
        },
        {
            editor.ui.label({ 
                text = "Author",
                alignment = editor.ui.ALIGNMENT.RIGHT
            }),
            editor.ui.string_field({})
        }
    }
})
```
Le code ci-dessus produit le formulaire de boîte de dialogue suivant :

![Boîte de dialogue de création d'un niveau](images/editor_scripts/new_level_dialog.png)

### Composants de présentation des données {#data-presentation-components}

L'éditeur définit les composants de présentation des données suivants :

- **`label`** — un libellé textuel destiné à accompagner les champs de saisie d'un formulaire.
- **`icon`** — une icône ; actuellement, ce composant ne peut afficher qu'un petit ensemble d'icônes prédéfinies, mais nous prévoyons d'en proposer davantage à l'avenir.
- **`image`** — une image chargée depuis un chemin de ressource du projet commençant par `/`, ou depuis une URL externe. Les props facultatives `width` et `height` ajustent l'image aux dimensions spécifiées tout en préservant ses proportions.
- **`heading`** — un élément textuel destiné à afficher une ligne de titre, par exemple dans un formulaire ou une boîte de dialogue. L'énumération `editor.ui.HEADING_STYLE` définit différents styles de titres, dont les titres HTML `H1`-`H6`, ainsi que les styles `DIALOG` et `FORM` propres à l'éditeur.
- **`paragraph`** — un élément textuel destiné à afficher un paragraphe. La principale différence avec `label` est la prise en charge du retour à la ligne automatique : si la zone attribuée est trop étroite, le texte passe à la ligne et peut être raccourci avec `"..."` s'il ne tient pas dans la vue.

Par exemple, une interface peut afficher à la fois une image du projet et une image provenant du Web :

```lua
editor.ui.vertical({
    children = {
        editor.ui.image({
            image = "/builtins/assets/images/logo/logo_256.png",
            width = 64,
            height = 64
        }),
        editor.ui.image({
            image = "https://defold.com/images/assets/monarch-hero.jpg"
        })
    }
})
```

### Composants de saisie {#input-components}

Les composants de saisie permettent à l'utilisateur d'interagir avec l'interface. Tous prennent en charge la prop `enabled`, qui détermine si l'interaction est activée, et définissent différentes props de callback qui informent le script de l'éditeur lors d'une interaction.

Si vous créez une interface statique, il suffit de définir des callbacks qui modifient simplement des variables locales. Pour les interfaces dynamiques et les interactions plus avancées, consultez la section sur la [réactivité](#reactivity).

Par exemple, vous pouvez créer une simple boîte de dialogue statique New File comme suit :
```lua
-- initial file name, will be replaced by the dialog
local file_name = ""
local create_file = editor.ui.show_dialog(editor.ui.dialog({
    title = "Create New File",
    content = editor.ui.horizontal({
        padding = editor.ui.PADDING.LARGE,
        spacing = editor.ui.SPACING.MEDIUM,
        children = {
            editor.ui.label({
                text = "New File Name",
                alignment = editor.ui.ALIGNMENT.CENTER
            }),
            editor.ui.string_field({
                grow = true,
                text = file_name,
                -- Typing callback:
                on_value_changed = function(new_text)
                    file_name = new_text
                end
            })
        }
    }),
    buttons = {
        editor.ui.dialog_button({ text = "Cancel", cancel = true, result = false }),
        editor.ui.dialog_button({ text = "Create File", default = true, result = true })
    }
}))
if create_file then
    print("create", file_name)
end
```
Voici la liste des composants de saisie intégrés :
- **`string_field`**, **`integer_field`** et **`number_field`** sont des variantes d'un champ de texte sur une seule ligne qui permettent de modifier respectivement des chaînes de caractères, des entiers et des nombres.
- **`select_box`** permet de choisir une option dans un tableau prédéfini d'options à l'aide d'une liste déroulante.
- **`check_box`** est un champ de saisie booléen avec un callback `on_value_changed`
- **`button`** possède un callback `on_press` appelé lorsque l'utilisateur appuie sur le bouton.
- **`external_file_field`** est un composant destiné à sélectionner un chemin de fichier sur l'ordinateur. Il se compose d'un champ de texte et d'un bouton qui ouvre une boîte de dialogue de sélection de fichier.
- **`resource_field`** est un composant destiné à sélectionner une ressource du projet.

Tous les composants, sauf les boutons, permettent de définir une prop `issue` qui affiche le problème lié au composant (de niveau `editor.ui.ISSUE_SEVERITY.ERROR` ou `editor.ui.ISSUE_SEVERITY.WARNING`), par exemple :
```lua
issue = {severity = editor.ui.ISSUE_SEVERITY.WARNING, message = "This value is deprecated"}
```
Lorsqu'un problème est spécifié, il modifie l'apparence du composant de saisie et ajoute une infobulle contenant le message du problème.

Voici une démonstration de tous les champs de saisie et de leurs variantes signalant un problème :

![Champs de saisie](images/editor_scripts/inputs_demo.png)

### Composants de boîte de dialogue {#dialog-related-components}

Pour afficher une boîte de dialogue, vous devez utiliser la fonction `editor.ui.show_dialog`. Elle attend un composant **`dialog`** qui définit la structure principale des boîtes de dialogue Defold : `title`, `header`, `content` et `buttons`. Le composant de boîte de dialogue est un peu particulier : vous ne pouvez pas l'utiliser comme enfant d'un autre composant, car il représente une fenêtre et non un élément d'interface. En revanche, `header` et `content` sont des composants ordinaires.

Les boutons de boîte de dialogue sont eux aussi particuliers : ils sont créés à l'aide du composant **`dialog_button`**. Contrairement aux boutons ordinaires, ils n'ont pas de callback `on_pressed`. Ils définissent à la place une prop `result` dont la valeur sera renvoyée par la fonction `editor.ui.show_dialog` à la fermeture de la boîte de dialogue. Les boutons de boîte de dialogue définissent aussi les props booléennes `cancel` et `default` : un bouton avec la prop `cancel` est déclenché lorsque l'utilisateur appuie sur <kbd>Escape</kbd> ou ferme la boîte de dialogue avec le bouton de fermeture du système d'exploitation, et le bouton `default` est déclenché lorsque l'utilisateur appuie sur <kbd>Enter</kbd>. Les props `cancel` et `default` d'un même bouton peuvent toutes deux être définies sur `true`.

### Composants utilitaires {#utility-components}

L'éditeur définit également quelques composants utilitaires :
- **`separator`** est une ligne fine qui sert à délimiter des blocs de contenu
- **`scroll`** est un composant d'encapsulation qui affiche des barres de défilement lorsque le composant encapsulé ne tient pas dans l'espace attribué

## Réactivité {#reactivity}

Comme les composants sont des **userdata immuables**, il est impossible de les modifier après leur création. Comment faire évoluer l'interface dans le temps ? La réponse : les **composants réactifs**.

::: sidenote
L'API d'interface des scripts de l'éditeur s'inspire de la bibliothèque [React](https://react.dev/) ; connaître les interfaces réactives et les hooks de React vous sera donc utile.
:::

Pour faire simple, un composant réactif est un composant associé à une fonction Lua qui reçoit des données (props) et renvoie une vue (un autre composant). La fonction d'un composant réactif peut utiliser des **hooks** : des fonctions spéciales du module `editor.ui` qui ajoutent des fonctionnalités réactives à vos composants. Par convention, le nom de tous les hooks commence par `use_`.

Pour créer un composant réactif, utilisez la fonction `editor.ui.component()`.

Examinons cet exemple : une boîte de dialogue New File qui n'autorise la création d'un fichier que si le nom saisi n'est pas vide :

```lua
-- 1. dialog is a reactive component
local dialog = editor.ui.component(function(props)
    -- 2. the component defines a local state (file name) that defaults to empty string
    local name, set_name = editor.ui.use_state("")

    return editor.ui.dialog({ 
        title = props.title,
        content = editor.ui.vertical({
            padding = editor.ui.PADDING.LARGE,
            children = { 
                editor.ui.string_field({ 
                    value = name,
                    -- 3. typing + Enter updates the local state
                    on_value_changed = set_name 
                }) 
            }
        }),
        buttons = {
            editor.ui.dialog_button({ 
                text = "Cancel", 
                cancel = true 
            }),
            editor.ui.dialog_button({ 
                text = "Create File",
                -- 4. creation is enabled when the name exists
                enabled = name ~= "",
                default = true,
                -- 5. result is the name
                result = name
            })
        }
    })
end)

-- 6. show_dialog will either return non-empty file name or nil on cancel
local file_name = editor.ui.show_dialog(dialog({ title = "New File Name" }))
if file_name then 
    print("create " .. file_name)
else
    print("cancelled")
end
```

Lorsque vous exécutez une commande de menu qui lance ce code, l'éditeur affiche une boîte de dialogue dont le bouton `"Create File"` est initialement désactivé. Il s'active lorsque vous saisissez un nom et appuyez sur <kbd>Enter</kbd> :

![Boîte de dialogue de création d'un fichier](images/editor_scripts/reactive_new_file_dialog.png)

Comment cela fonctionne-t-il ? Au tout premier rendu, le hook `use_state` crée un état local associé au composant et le renvoie avec une fonction permettant de le modifier. Lorsque cette fonction est appelée, elle planifie un nouveau rendu du composant. Lors des rendus suivants, la fonction du composant est appelée à nouveau et `use_state` renvoie l'état mis à jour. Le nouveau composant de vue renvoyé par la fonction est alors comparé à l'ancien, et l'interface est mise à jour là où des changements ont été détectés.

Cette approche réactive simplifie considérablement la création d'interfaces interactives et le maintien de leur synchronisation : au lieu de mettre à jour explicitement tous les composants concernés lors d'une saisie de l'utilisateur, la vue est définie comme une fonction pure des données d'entrée (props et état local), et l'éditeur gère lui-même toutes les mises à jour.

### Règles de réactivité {#rules-of-reactivity}

Pour que les composants fonctionnels réactifs fonctionnent correctement, l'éditeur exige qu'ils respectent les règles suivantes :

1. Les fonctions des composants doivent être pures. Il n'y a aucune garantie sur le moment ou la fréquence de leur appel. Tous les effets de bord devraient se produire en dehors du rendu, par exemple dans les callbacks
2. Les props et l'état local doivent être immuables. Ne modifiez pas les props. Si votre état local est une table, ne la modifiez pas sur place : créez-en une nouvelle et transmettez-la à la fonction de modification de l'état lorsque celui-ci doit changer.
3. Les fonctions des composants doivent appeler les mêmes hooks dans le même ordre à chaque invocation. N'appelez pas de hooks dans des boucles, dans des blocs conditionnels, après des retours anticipés, etc. Il est recommandé d'appeler les hooks au début de la fonction du composant, avant tout autre code.
4. Appelez les hooks uniquement depuis les fonctions des composants. Les hooks fonctionnent dans le contexte d'un composant réactif ; il est donc uniquement permis de les appeler dans la fonction du composant (ou dans une autre fonction appelée directement par celle-ci).

### Hooks {#hooks}

::: sidenote
Si vous connaissez [React](https://react.dev/), vous remarquerez que la sémantique des hooks de l'éditeur diffère légèrement en ce qui concerne leurs dépendances.
:::

L'éditeur définit deux hooks : **`use_memo`** et **`use_state`**.

### **`use_state`** {#use_state}

L'état local peut être créé de deux manières : avec une valeur par défaut ou avec une fonction d'initialisation :
```lua
-- default value
local enabled, set_enabled = editor.ui.use_state(true)
-- initializer function + args
local id, set_id = editor.ui.use_state(string.lower, props.name)
```
De même, la fonction de modification de l'état peut être appelée avec une nouvelle valeur ou avec une fonction de mise à jour :
```lua
-- updater function
local function increment_by(n, by)
    return n + by
end

local counter = editor.ui.component(function(props)
    local count, set_count = editor.ui.use_state(0)
    
    return editor.ui.horizontal({
        spacing = editor.ui.SPACING.SMALL,
        children = {
            editor.ui.label({
                text = tostring(count),
                alignment = editor.ui.ALIGNMENT.LEFT,
                grow = true
            }),
            editor.ui.text_button({
                text = "+1",
                on_pressed = function() set_count(increment_by, 1) end
            }),
            editor.ui.text_button({
                text = "+5",
                on_pressed = function() set_count(increment_by, 5) end
            })
        }
    })
end)
```

Enfin, l'état peut être **réinitialisé**. Il est réinitialisé lorsqu'un des arguments de `editor.ui.use_state()` change, selon une comparaison avec `==`. C'est pourquoi vous ne devez pas utiliser de tables littérales ni de fonctions d'initialisation littérales comme arguments du hook `use_state` : cela réinitialiserait l'état à chaque nouveau rendu. Par exemple :
```lua
-- ❌ BAD: literal table initializer causes state reset on every re-render
local user, set_user = editor.ui.use_state({ first_name = props.first_name, last_name = props.last_name})

-- ✅ GOOD: use initializer function outside of component function to create table state
local function create_user(first_name, last_name) 
    return { first_name = first_name, last_name = last_name}
end
-- ...later, in component function:
local user, set_user = editor.ui.use_state(create_user, props.first_name, props.last_name)


-- ❌ BAD: literal initializer function causes state reset on every re-render
local id, set_id = editor.ui.use_state(function() return string.lower(props.name) end)

-- ✅ GOOD: use referenced initializer function to create the state
local id, set_id = editor.ui.use_state(string.lower, props.name)
```

### **`use_memo`** {#use_memo}

Vous pouvez utiliser le hook `use_memo` pour améliorer les performances. Il est courant d'effectuer certains calculs dans les fonctions de rendu, par exemple pour vérifier la validité de la saisie de l'utilisateur. Le hook `use_memo` peut être utilisé lorsqu'il est moins coûteux de vérifier si les arguments de la fonction de calcul ont changé que d'appeler cette fonction. Le hook appelle la fonction de calcul au premier rendu, puis réutilise la valeur calculée lors des rendus suivants si tous les arguments de `use_memo` sont inchangés :
```lua
-- validation function outside of component function
local function validate_password(password)
    if #password < 8 then
        return false, "Password must be at least 8 characters long."
    elseif not password:match("%l") then
        return false, "Password must include at least one lowercase letter."
    elseif not password:match("%u") then
        return false, "Password must include at least one uppercase letter."
    elseif not password:match("%d") then
        return false, "Password must include at least one number."
    else
        return true, "Password is valid."
    end
end

-- ...later, in component function
local username, set_username = editor.ui.use_state('')
local password, set_password = editor.ui.use_state('')
local valid, message = editor.ui.use_memo(validate_password, password)
```
Dans cet exemple, la validation du mot de passe s'exécute à chaque modification du mot de passe (par exemple lors de la saisie dans un champ de mot de passe), mais pas lorsque le nom d'utilisateur change.

Un autre cas d'utilisation de `use_memo` consiste à créer des callbacks ensuite utilisés dans les composants de saisie, ou à utiliser une fonction créée localement comme valeur de prop d'un autre composant : cela évite des rendus inutiles.
