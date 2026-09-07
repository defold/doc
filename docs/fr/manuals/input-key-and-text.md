---
title: Entrées clavier et saisie de texte dans Defold
brief: Ce manuel explique le fonctionnement des entrées clavier et de la saisie de texte.
---

::: sidenote
Il est recommandé de vous familiariser avec le fonctionnement général des entrées dans Defold, la manière de les recevoir et l'ordre dans lequel vos fichiers script les reçoivent. Pour en savoir plus sur le système d'entrée, consultez le [manuel de présentation des entrées](/manuals/input).
:::

# Déclencheurs de touches {#key-triggers}
Les déclencheurs de touches vous permettent d'associer la saisie d'une touche du clavier à une action du jeu. Chaque touche est associée séparément à une action correspondante. Les déclencheurs de touches servent à relier des touches précises à des fonctions précises, comme le déplacement d'un personnage avec les touches fléchées ou WASD. Si vous devez lire une saisie quelconque au clavier, utilisez les déclencheurs de texte (voir ci-dessous).

![](images/input/key_bindings.png)

```lua
function on_input(self, action_id, action)
    if action_id == hash("left") then
        if action.pressed then
            -- start moving left
        elseif action.released then
            -- stop moving left
        end
    end
end
```

# Déclencheurs de texte {#text-triggers}
Les déclencheurs de texte servent à lire une saisie de texte libre. Il existe deux types de déclencheurs de texte : `text` et `marked-text`.

![](images/input/text_bindings.png)

## Texte {#text}
Le déclencheur `text` capture la saisie de texte normale. Il définit le champ `text` de la table d'action sur une chaîne contenant le caractère saisi. L'action n'est déclenchée qu'à l'appui sur la touche ; aucune action `release` ou `repeated` n'est envoyée.

```lua
function on_input(self, action_id, action)
    if action_id == hash("text") then
        -- Concatenate the typed character to the "user" node...
        local node = gui.get_node("user")
        local name = gui.get_text(node)
        name = name .. action.text
        gui.set_text(node, name)
    end
end
```

## Texte marqué {#marked-text}
Le déclencheur `marked-text` est principalement utilisé pour les claviers asiatiques, où plusieurs frappes peuvent correspondre à une seule entrée. Par exemple, avec le clavier iOS "Japanese-Kana", l'utilisateur peut saisir des combinaisons et la partie supérieure du clavier affiche les symboles ou séquences de symboles disponibles pour la saisie.

![Saisie de texte marqué](images/input/marked_text.png)

- Chaque frappe génère une action distincte et définit le champ d'action `text` sur la séquence de symboles en cours de saisie (le « texte marqué »).
- Lorsque l'utilisateur sélectionne un symbole ou une combinaison de symboles, une action distincte de déclencheur de type `text` est envoyée (à condition qu'un tel déclencheur soit configuré dans la liste des liaisons d'entrée). Cette action distincte définit le champ d'action `text` sur la séquence finale de symboles.
