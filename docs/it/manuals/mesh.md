---
title: Mesh 3D in Defold
brief: Questo manuale descrive come creare mesh 3D durante l'esecuzione del gioco.
---

# Componente Mesh {#mesh-component}

Defold è, alla base, un motore 3D. Anche quando lavori soltanto con contenuti 2D, tutto il rendering avviene in 3D, ma viene proiettato sullo schermo con una proiezione ortografica. Defold ti permette di sfruttare contenuti interamente 3D aggiungendo e creando mesh 3D durante l'esecuzione nelle tue collezioni (collection). Puoi creare giochi completamente in 3D con soli asset 3D oppure combinare contenuti 3D e 2D come preferisci.

## Creazione di un componente Mesh {#creating-a-mesh-component}

I componenti Mesh si creano come qualsiasi altro componente di un oggetto di gioco (game object). Puoi farlo in due modi:

- Crea un *file Mesh* facendo <kbd>clic con il pulsante destro</kbd> su una posizione nel browser *Assets* e selezionando <kbd>New... ▸ Mesh</kbd>.
- Crea il componente incorporato direttamente in un oggetto di gioco facendo <kbd>clic con il pulsante destro</kbd> su un oggetto di gioco nella vista *Outline* e selezionando <kbd>Add Component ▸ Mesh</kbd>.

![Mesh in un oggetto di gioco](images/mesh/mesh.png)

Dopo aver creato la mesh, devi specificare alcune proprietà:

### Proprietà della mesh {#mesh-properties}

Oltre alle proprietà *Id*, *Position* e *Rotation*, sono disponibili le seguenti proprietà specifiche del componente:

*Material*
: Il materiale da usare per il rendering della mesh.

*Vertices*
: Un file buffer che descrive i dati della mesh per ciascun flusso.

*Primitive Type*
: Lines, Triangles o Triangle Strip.

*Position Stream*
: Questa proprietà deve contenere il nome del flusso *position*. Il flusso viene fornito automaticamente come input al vertex shader.

*Normal Stream*
: Questa proprietà deve contenere il nome del flusso *normal*. Il flusso viene fornito automaticamente come input al vertex shader.

*tex0*
: Imposta questa proprietà sulla texture da usare per la mesh.

## Manipolazione nell'editor {#editor-manipulation}

Dopo aver aggiunto il componente Mesh, puoi modificare e manipolare il componente e/o l'oggetto di gioco che lo contiene con i consueti strumenti di *Scene Editor*, per spostare, ruotare e ridimensionare la mesh come preferisci.

## Manipolazione a runtime {#runtime-manipulation}

Puoi manipolare le mesh durante l'esecuzione usando i buffer di Defold. Ecco un esempio di creazione di un cubo a partire da strisce di triangoli:

```Lua

-- cube
local vertices = {
	0, 0, 0,
	0, 1, 0,
	1, 0, 0,
	1, 1, 0,
	1, 1, 1,
	0, 1, 0,
	0, 1, 1,
	0, 0, 1,
	1, 1, 1,
	1, 0, 1,
	1, 0, 0,
	0, 0, 1,
	0, 0, 0,
	0, 1, 0
}

-- create a buffer with a position stream
local buf = buffer.create(#vertices / 3, {
	{ name = hash("position"), type=buffer.VALUE_TYPE_FLOAT32, count = 3 }
})

-- get the position stream and write the vertices
local positions = buffer.get_stream(buf, "position")
for i, value in ipairs(vertices) do
	positions[i] = vertices[i]
end

-- set the buffer with the vertices on the mesh
local res = go.get("#mesh", "vertices")
resource.set_buffer(res, buf)
```

Consulta il [post di annuncio sul forum per ulteriori informazioni](https://forum.defold.com/t/mesh-component-in-defold-1-2-169-beta/65137) sull'uso del componente Mesh, inclusi progetti di esempio e frammenti di codice.

## Culling del frustum {#frustum-culling}

I componenti Mesh non vengono esclusi automaticamente dal rendering fuori dal frustum, a causa della loro natura dinamica e dell'impossibilità di sapere con certezza come sono codificati i dati di posizione. Per poter escludere una mesh, occorre impostare il suo volume delimitatore allineato agli assi come metadati del buffer, usando 6 valori in virgola mobile (minimo/massimo dell'AABB):

```lua
buffer.set_metadata(buf, hash("AABB"), { 0, 0, 0, 1, 1, 1 }, buffer.VALUE_TYPE_FLOAT32)
```

## Costanti del materiale {#material-constants}

{% include shared/material-constants.md component='mesh' variable='tint' %}

`tint`
: La tinta della mesh (`vector4`). Il `vector4` rappresenta la tinta con x, y, z e w corrispondenti alle componenti rossa, verde, blu e alfa.

## Vertici nello spazio locale e nello spazio globale {#vertex-local-vs-world-space}
Se l'impostazione Vertex Space del materiale della mesh è impostata su Local Space, i dati vengono forniti allo shader così come sono e dovrai trasformare vertici e normali sulla GPU come di consueto.

Se l'impostazione Vertex Space del materiale della mesh è impostata su World Space, devi fornire i flussi predefiniti `position` e `normal` oppure selezionarli dal menu a discesa durante la modifica della mesh. In questo modo il motore può trasformare i dati nello spazio globale per raggruppare la mesh con altri oggetti in un'unica operazione di rendering.
