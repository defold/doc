---
title: Σήμανση εμπλουτισμένου κειμένου στο Defold
brief: Αυτό το εγχειρίδιο εξηγεί πώς να μορφοποιείτε στοιχεία Label και κόμβους κειμένου GUI με σήμανση εμπλουτισμένου κειμένου και πώς να εξετάζετε συνδέσμους και sprite από τη Lua.
---

# Σήμανση εμπλουτισμένου κειμένου {#rich-text-markup}

Χρησιμοποιήστε σήμανση σε στοιχεία Label και κόμβους κειμένου GUI για να εφαρμόσετε ένθετα οπτικά στυλ και εφέ και να εξετάσετε συνδέσμους και sprite από τη Lua.

```lua
go.set("#label", "text", "Score: <color=#69D2E7>1200</color>")
```

Εναλλακτικά, ορίστε στη γραμματοσειρά ένα επαναχρησιμοποιήσιμο στυλ αντικειμένου με όνομα και επιλέξτε το από έναν σύνδεσμο:

```lua
local fontpath = "/fonts/ui.fontc"
font.set_style(fontpath, "menu_link", "<color=#69D2E7>")
go.set("#label", "text", "Open <link style=menu_link src=inventory>inventory</link>")
```

## Αναφορά ετικετών {#tag-reference}

| Ετικέτα | Σκοπός | Παράδειγμα |
| --- | --- | --- |
| [`color`](#color) | Ορισμός του χρώματος γεμίσματος των γλύφων. | <img src="/manuals/images/richtext/color_green.webp" alt="Πράσινο κείμενο" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`size`](#size) | Αλλαγή της διαμόρφωσης των γλύφων και του μεγέθους της διάταξης. | <img src="/manuals/images/richtext/size_24.webp" alt="Κείμενο σε μέγεθος 24 pixel" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`gradient`](#gradient) | Εφαρμογή στατικής ή κινούμενης χρωματικής διαβάθμισης. | <img src="/manuals/images/richtext/gradient_horizontal.webp" alt="Κείμενο με οριζόντια διαβάθμιση" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`ul`](#ul) | Υπογράμμιση κειμένου. | <img src="/manuals/images/richtext/underline_solid.webp" alt="Υπογραμμισμένο κείμενο" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`strike`](#strike) | Προσθήκη γραμμής διαγραφής στο κείμενο. | <img src="/manuals/images/richtext/strike_solid.webp" alt="Κείμενο με γραμμή διαγραφής" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`outline`](#outline) | Ορισμός του πλάτους και του χρώματος περιγράμματος των γλύφων. | <img src="/manuals/images/richtext/outline.webp" alt="Κείμενο με περίγραμμα" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`shadow`](#shadow) | Προσθήκη σκιάς στο κείμενο. | <img src="/manuals/images/richtext/shadow.webp" alt="Κείμενο με σκιά" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`shake`](#shake) | Εφαρμογή κινούμενης τυχαίας μετατόπισης. | <img src="/manuals/images/richtext/shake_glyph.webp" alt="Κείμενο που τρέμει" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`wave`](#wave) | Μετακίνηση κειμένου σε κινούμενο ημιτονοειδές κύμα. | <img src="/manuals/images/richtext/wave_glyph.webp" alt="Κείμενο με κυματισμό" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`sprite`](#sprite) | Προσθήκη αντικειμένου sprite μέσα στο κείμενο. | <img src="/manuals/images/richtext/sprite.webp" alt="Sprite μέσα στο κείμενο" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`link`](#link) | Προσθήκη διαδραστικού αντικειμένου συνδέσμου. | <img src="/manuals/images/richtext/link.webp" alt="Κείμενο συνδέσμου" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |

## Σύνταξη {#syntax}

Στις ετικέτες και στα ονόματα γνωρισμάτων γίνεται διάκριση πεζών και κεφαλαίων. Μια ετικέτα με αντίστοιχη ετικέτα κλεισίματος εφαρμόζεται στο ορατό κείμενο UTF-32 που περικλείει. Τα αντικείμενα sprite χρησιμοποιούν αυτοκλειόμενες ετικέτες.

```text
<color=#69D2E7>colored text</color>
<ul pattern=dashed>underlined text</ul>
<outline size=2 color=#000000>outlined text</outline>
<shadow x=2 y=-2 color=#00000080>shadowed text</shadow>
<sprite src=images/icon.png width=2em/>
```

### Γνωρίσματα {#attributes}

Τα γνωρίσματα μπορούν να γράφονται χωρίς εισαγωγικά όταν δεν περιέχουν κενά διαστήματα ή να περικλείονται σε μονά ή διπλά εισαγωγικά. Τα `color` και `size` υποστηρίζουν μια σύντομη πρώτη τιμή, καθώς και τη μορφή με το όνομα `value`.

```text
<color=#FF8800>Orange</color>
<color value="#FF8800">Orange</color>
<size='120%'>Larger</size>
```

### Ένθεση {#nesting}

Οι ετικέτες πρέπει να κλείνουν με αντίστροφη σειρά από εκείνη με την οποία ανοίγουν. Οι τιμές ενός εσωτερικού στυλ αντικαθιστούν την ίδια ιδιότητα ενός εξωτερικού στυλ. Διαφορετικές ιδιότητες συνδυάζονται. Τα εφέ των τμημάτων κειμένου παραμένουν ενεργά ανεξάρτητα, οπότε οι ένθετες χρωματικές διαβαθμίσεις πολλαπλασιάζουν τα χρώματα και τα ένθετα εφέ θέσης προσθέτουν τις μετατοπίσεις τους.

```text
<color=#FFCC00>
    Gold <outline size=2 color=#000000>with a black outline</outline>
</color>
```

### Οντότητες χαρακτήρων {#entities}

Χρησιμοποιήστε τα `&amp;`, `&apos;`, `&gt;`, `&lt;` και `&quot;` για δεσμευμένους χαρακτήρες στο ορατό κείμενο. Προς το παρόν δεν υποστηρίζονται αριθμητικές οντότητες.

## Ετικέτες {#tags}

Οι ετικέτες εμπλουτισμένου κειμένου είτε μορφοποιούν ένα τμήμα κειμένου που περικλείουν είτε περιγράφουν ένα αντικείμενο που μπορεί να εξεταστεί από τη Lua. Οι ετικέτες στυλ χρησιμοποιούν μια αντίστοιχη ετικέτα κλεισίματος. Το αντικείμενο `sprite` είναι αυτοκλειόμενο, ενώ το `link` περικλείει το κείμενο του συνδέσμου.

### `color` {#color}

Ορίζει το χρώμα γεμίσματος των γλύφων. Τα χρώματα χρησιμοποιούν τη μορφή `#RRGGBB` ή `#RRGGBBAA`. Το πρόθεμα της δίεσης είναι υποχρεωτικό· τα `0xFF0000` και `FF0000` δεν είναι έγκυρα. Το αποτέλεσμα πολλαπλασιάζει το βασικό χρώμα του label ή του μηχανισμού απόδοσης.

| Γνώρισμα | Υποχρεωτικό | Προεπιλογή | Σημασία |
| --- | --- | --- | --- |
| `=color` ή `value=color` | Ναι | Χωρίς προεπιλογή | Χρώμα γεμίσματος σε δεκαεξαδική μορφή RGB ή RGBA. |

```text
<color=#00FF00>Opaque green</color>
<color=#00FF0080>Half-alpha green</color>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*#00FF00*

![Δείγμα κειμένου αποδίδεται με αδιαφανές πράσινο χρώμα](images/richtext/color_green.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*#00FF0080*

![Δείγμα κειμένου αποδίδεται με πράσινο χρώμα και διαφάνεια άλφα στο μισό](images/richtext/color_green_alpha.webp)

</div>
</div>

### `size` {#size}

Αλλάζει τη διαμόρφωση των γλύφων και το μέγεθος της διάταξης, όχι μόνο την κλίμακα των κορυφών. Οι σχετικές τιμές χρησιμοποιούν πάντα το βασικό μέγεθος γραμματοσειράς της διάταξης. Δεν συσσωρεύονται με τις τιμές μιας εξωτερικής ετικέτας `size`.

| Γνώρισμα | Υποχρεωτικό | Προεπιλογή | Σημασία |
| --- | --- | --- | --- |
| `=size` ή `value=size` | Ναι | Χωρίς προεπιλογή | Απόλυτο μέγεθος, ποσοστό, πολλαπλάσιο του βασικού μεγέθους ή μετατόπιση από το βασικό μέγεθος με πρόσημο, χρησιμοποιώντας μία από τις παρακάτω μορφές. |

| Μορφή | Παράδειγμα με βάση τα 32 px | Τελικό μέγεθος |
| --- | --- | --- |
| Αριθμός χωρίς μονάδα ή με `px` | `24`, `24px` | 24 px |
| Ποσοστό του βασικού μεγέθους | `120%` | 38.4 px |
| Πολλαπλάσιο του βασικού μεγέθους | `2em` | 64 px |
| Μετατόπιση από το βασικό μέγεθος με πρόσημο | `+4`, `-4` | 36 px, 28 px |

```text
<size=24px>Exactly 24 pixels</size>
<size=120%>120% of the layout base size</size>
<size=2em>Twice the layout base size</size>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*24px*

![Δείγμα κειμένου αποδίδεται σε μέγεθος 24 pixel](images/richtext/size_24.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*120% των 32px*

![Δείγμα κειμένου αποδίδεται στο 120 τοις εκατό των 32 pixel](images/richtext/size_120.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*2em με βάση τα 32px*

![Δείγμα κειμένου αποδίδεται στο διπλάσιο του βασικού μεγέθους των 32 pixel](images/richtext/size_2em.webp)

</div>
</div>

### `gradient` {#gradient}

Μια χρωματική διαβάθμιση δέχεται ακριβώς ένα πλήρες σύνολο γνωρισμάτων. Ο συνδυασμός διαφορετικών συνόλων ή η παράλειψη ενός γνωρίσματος δεν είναι έγκυρα.

| Λειτουργία | Υποχρεωτικά γνωρίσματα | Παρεμβολή |
| --- | --- | --- |
| Οριζόντια | `left`, `right` | Παρεμβολή μεταξύ των δύο οριζόντιων χρωμάτων. |
| Κατακόρυφη | `bottom`, `top` | Παρεμβολή μεταξύ του κάτω και του επάνω χρώματος. |
| Τεσσάρων γωνιών | `tl`, `tr`, `bl`, `br` | Παρεμβολή μεταξύ των χρωμάτων τεσσάρων κορυφών. |

| Γνώρισμα | Υποχρεωτικό | Προεπιλογή | Σημασία |
| --- | --- | --- | --- |
| `left`, `right` | Για την οριζόντια λειτουργία | Καμία | Χρώματα των οριζόντιων άκρων σε μορφή `#RRGGBB` ή `#RRGGBBAA`. Πρέπει να υπάρχουν και τα δύο. |
| `bottom`, `top` | Για την κατακόρυφη λειτουργία | Καμία | Χρώματα των κατακόρυφων άκρων. Πρέπει να υπάρχουν και τα δύο. |
| `tl`, `tr`, `bl`, `br` | Για τη λειτουργία τεσσάρων γωνιών | Καμία | Χρώματα επάνω αριστερά, επάνω δεξιά, κάτω αριστερά και κάτω δεξιά. Πρέπει να υπάρχουν και τα τέσσερα. |
| `fit` | Όχι | `span` | Το `glyph` δειγματοληπτεί κάθε θέση του διαμορφωμένου κειμένου· το `span` κατανέμει τη διαβάθμιση σε ολόκληρο το κείμενο που περικλείεται στην ετικέτα. |
| `hz` | Όχι | `0` | Πλήρεις κύκλοι ροής ανά δευτερόλεπτο στο εύρος `[0,)`· το μηδέν διατηρεί τη διαβάθμιση στατική. |
| `direction` | Όχι | `forward` | `forward` ή `reverse`. Ελέγχει την κατεύθυνση της ροής όταν το `hz` δεν είναι μηδέν. |

Όταν παραλείπεται το `fit`, το `fit=span` κατανέμει τη διαβάθμιση σε ολόκληρο το κείμενο που περικλείεται στην ετικέτα. Το `fit=glyph` δειγματοληπτεί κάθε θέση του διαμορφωμένου κειμένου ανεξάρτητα. Το προαιρετικό `hz` καθορίζει τους πλήρεις κύκλους της κινούμενης ροής ανά δευτερόλεπτο· η προεπιλεγμένη τιμή μηδέν διατηρεί τη διαβάθμιση στατική. Η επαναλαμβανόμενη χρωματική κλίμακα με κατοπτρική συμμετρία ρέει συνεχώς και επανέρχεται στην αρχή χωρίς απότομη αλλαγή χρώματος. Η προεπιλογή είναι `direction=forward`· χρησιμοποιήστε `direction=reverse` για να αντιστρέψετε τη ροή.

```text
<gradient left=#FF00FF right=#FFFFFF>Horizontal Gradient</gradient>

<gradient hz=0.25 fit=glyph bottom=#182848 top=#4B6CB7>Animated vertical glyphs</gradient>

<gradient hz=0.25 direction=reverse left=#FF0000 right=#0000FF>Reverse flow</gradient>

<gradient hz=0.25 direction=reverse fit=span left=#FF0000 right=#0000FF>One animated span color</gradient>

<gradient fit=glyph tl=#FF0000 tr=#00FF00 bl=#0000FF br=#FFFFFF>
    Four corners
</gradient>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*Οριζόντια*

![Δείγμα κειμένου με οριζόντια διαβάθμιση από ματζέντα σε λευκό](images/richtext/gradient_horizontal.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*Κατακόρυφη*

![Δείγμα κειμένου με κατακόρυφη μπλε διαβάθμιση](images/richtext/gradient_vertical.webp)

</div>
</div>

**Τεσσάρων γωνιών**

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=glyph`*

![Δείγμα κειμένου με διαβάθμιση τεσσάρων γωνιών προσαρμοσμένη σε κάθε γλύφο](images/richtext/gradient_four_glyph.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=span`*

![Δείγμα κειμένου με διαβάθμιση τεσσάρων γωνιών προσαρμοσμένη στο τμήμα κειμένου](images/richtext/gradient_four_text.webp)

</div>
</div>

**Με κίνηση**

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=glyph`*

![Κινούμενη ρέουσα διαβάθμιση προσαρμοσμένη σε κάθε γλύφο](images/richtext/gradient_flow_glyph.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=span`*

![Κινούμενη ρέουσα διαβάθμιση προσαρμοσμένη στο τμήμα κειμένου](images/richtext/gradient_flow_span.webp)

</div>
</div>

Τα χρώματα της διαβάθμισης πολλαπλασιάζουν το τρέχον χρώμα γεμίσματος. Συνεπώς, μια διαβάθμιση μέσα σε `color=#808080` δεν μπορεί να παράγει κανάλι φωτεινότερο από αυτόν τον βασικό πολλαπλασιαστή.

### `ul` {#ul}

Σχεδιάζει υπογράμμιση χρησιμοποιώντας τις μετρικές υπογράμμισης της γραμματοσειράς, όταν είναι διαθέσιμες. Η ετικέτα δεν έχει ανεξάρτητο χρώμα: η γραμμή κληρονομεί το τελικό χρώμα γεμίσματος, συμπεριλαμβανομένων των οριζόντιων, κατακόρυφων και τεσσάρων γωνιών διαβαθμίσεων.

| Γνώρισμα | Υποχρεωτικό | Προεπιλογή | Σημασία |
| --- | --- | --- | --- |
| `pattern` | Όχι | `solid` | `solid` ή `dashed`. |

```text
<ul>Solid underline</ul>
<ul pattern=dashed>Dashed underline</ul>
<ul><gradient left=#FF00FF right=#FFFFFF>Gradient line</gradient></ul>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*Συνεχής*

![Δείγμα κειμένου με συνεχή υπογράμμιση](images/richtext/underline_solid.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*Διακεκομμένη*

![Δείγμα κειμένου με διακεκομμένη υπογράμμιση](images/richtext/underline_dashed.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*Με διαβάθμιση*

![Δείγμα κειμένου με υπογράμμιση χρωματικής διαβάθμισης](images/richtext/underline_gradient.webp)

</div>
</div>

### `strike` {#strike}

Σχεδιάζει μια γραμμή διαγραφής μέσα στο κείμενο που περικλείει. Δέχεται τις ίδιες τιμές `pattern` με το `ul` και επίσης κληρονομεί το τελικό χρώμα γεμίσματος.

| Γνώρισμα | Υποχρεωτικό | Προεπιλογή | Σημασία |
| --- | --- | --- | --- |
| `pattern` | Όχι | `solid` | `solid` ή `dashed`. |

```text
<strike>No longer available</strike>
<strike pattern=dashed>Dashed strikethrough</strike>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*Συνεχής*

![Δείγμα κειμένου με συνεχή γραμμή διαγραφής](images/richtext/strike_solid.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*Διακεκομμένη*

![Δείγμα κειμένου με διακεκομμένη γραμμή διαγραφής](images/richtext/strike_dashed.webp)

</div>
</div>

### `outline` {#outline}

Ορίζει το πλάτος του περιγράμματος, το χρώμα του ή και τα δύο. Απαιτείται τουλάχιστον ένα γνώρισμα. Το μηδενικό πλάτος απενεργοποιεί ρητά το περίγραμμα για το τμήμα κειμένου.

| Γνώρισμα | Υποχρεωτικό | Προεπιλογή | Σημασία |
| --- | --- | --- | --- |
| `size` | Ένα από τα size/color | Κληρονομείται· `0` σε προεπιλεγμένη γραμματοσειρά | Πλάτος σε μονάδες διάταξης, στο εύρος `[0,)`. Δεν γίνονται δεκτά επιθήματα μονάδων. |
| `color` | Ένα από τα size/color | Κληρονομείται· `#000000` σε προεπιλεγμένο label | Ένα χρώμα περιγράμματος σε δεκαεξαδική μορφή RGB (`#RRGGBB`) ή RGBA (`#RRGGBBAA`)· η συνιστώσα άλφα ελέγχει την αδιαφάνεια. |

```text
<outline size=3 color=#000000>Black outline</outline>
<outline color=#FF0000>Keep inherited width, change color</outline>
<outline size=0>Disable inherited outline</outline>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*Εξωτερικό μαύρο περίγραμμα*

![Δείγμα κειμένου με εξωτερικό μαύρο περίγραμμα](images/richtext/outline.webp)

</div>
</div>

### `shadow` {#shadow}

Προσθέτει σκιά με σκληρά άκρα στο κείμενο που περικλείει. Απαιτείται τουλάχιστον ένα γνώρισμα. Τα γνωρίσματα που παραλείπονται από μια ένθετη ετικέτα διατηρούν την τιμή της εξωτερικής σκιάς· όσα παραλείπονται από την πιο εξωτερική ετικέτα διατηρούν τη βασική τιμή σκιάς της γραμματοσειράς.

| Γνώρισμα | Υποχρεωτικό | Προεπιλογή | Σημασία |
| --- | --- | --- | --- |
| `color` | Όχι | Κληρονομείται· `#000000` σε προεπιλεγμένο label | Χρώμα σκιάς σε μορφή `#RRGGBB` ή `#RRGGBBAA`. |
| `x` | Όχι | Κληρονομείται· `0` σε προεπιλεγμένη γραμματοσειρά | Οριζόντια μετατόπιση σκιάς σε μονάδες διάταξης. Οι θετικές τιμές τη μετακινούν δεξιά. |
| `y` | Όχι | Κληρονομείται· `0` σε προεπιλεγμένη γραμματοσειρά | Κατακόρυφη μετατόπιση σκιάς σε μονάδες διάταξης. Οι θετικές τιμές τη μετακινούν προς τα επάνω. |
| `blur` | Όχι | Κληρονομείται· `0` σε προεπιλεγμένη γραμματοσειρά | Ακτίνα θόλωσης σε μονάδες διάταξης, στο εύρος `[0,)`. |

```text
<shadow x=6 y=-6 blur=4 color=#000000A0>Shadow</shadow>
<shadow x=-2>Override only the horizontal offset</shadow>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*x=6, y=-6, blur=4*

![Δείγμα κειμένου με μετατοπισμένη σκιά](images/richtext/shadow.webp)

</div>
</div>

::: sidenote
Η θόλωση της σκιάς δημιουργείται και αποθηκεύεται στο atlas των γλύφων. Ένα τμήμα κειμένου μπορεί να ζητήσει μικρότερη θόλωση από την προϋπολογισμένη θόλωση της γραμματοσειράς· μεγαλύτερες τιμές διατηρούνται στη διάταξη, αλλά προς το παρόν αποδίδονται χρησιμοποιώντας τη μεγαλύτερη διαθέσιμη θόλωση στο atlas.
:::

### `shake` {#shake}

Εφαρμόζει μια ντετερμινιστική κινούμενη τυχαία μετατόπιση χωρίς να αλλάζει την αναδίπλωση γραμμών ή τα όρια της διάταξης. Το εφέ παρακολουθεί τον χρόνο εσωτερικά· τα script δεν χρειάζεται να τροποποιούν το κείμενο του label σε κάθε καρέ της κίνησης.

| Γνώρισμα | Υποχρεωτικό | Προεπιλογή | Έγκυρες τιμές | Σημασία |
| --- | --- | --- | --- | --- |
| `hz` | Όχι | 20 | `[0,)` | Μεταβάσεις προς τυχαίους στόχους ανά δευτερόλεπτο. Το μηδέν θέτει το εφέ σε παύση. |
| `amplitude` | Όχι | 0.5 | `[0,)` | Μέγιστη μετατόπιση σε μονάδες διάταξης. |
| `fit` | Όχι | `glyph` | `glyph` ή `span` | Το `glyph` δειγματοληπτεί μια μετατόπιση για κάθε μονάδα διαμορφωμένων γλύφων, διατηρώντας ενιαίες τις ομάδες χαρακτήρων. Το `span` μετακινεί ολόκληρο το τμήμα κειμένου που περικλείεται στην ετικέτα ως μία άκαμπτη μονάδα. |

```text
<shake>Default shake</shake>
<shake hz=12 amplitude=0.8 fit=glyph>Glyph shake</shake>
<shake hz=12 amplitude=0.8 fit=span>Rigid span shake</shake>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=glyph`*

![Δείγμα κειμένου με κινούμενο τρέμουλο ανά γλύφο](images/richtext/shake_glyph.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=span`*

![Δείγμα κειμένου με κινούμενο τρέμουλο σε ολόκληρο το τμήμα κειμένου](images/richtext/shake_span.webp)

</div>
</div>

### `wave` {#wave}

Μετακινεί τους χαρακτήρες πάνω και κάτω με κινούμενο ημιτονοειδές κύμα, χωρίς να αλλάζει την αναδίπλωση γραμμών ή τα όρια της διάταξης. Η διάταξη συσσωρεύει τον χρόνο κίνησης όταν ενημερώνεται.

| Γνώρισμα | Υποχρεωτικό | Προεπιλογή | Σημασία |
| --- | --- | --- | --- |
| `amplitude` | Όχι | 1 | Μέγιστη κατακόρυφη μετατόπιση σε μονάδες διάταξης, στο εύρος `[0,)`. |
| `hz` | Όχι | 1 | Πλήρεις χρονικοί κύκλοι ανά δευτερόλεπτο, στο εύρος `[0,)`. Το μηδέν θέτει το κύμα σε παύση. |
| `wavelength` | Όχι | 6 | Θέσεις ορατού κειμένου UTF-32 ανά πλήρη χωρικό κύκλο, στο εύρος `[1,)`. Οι χαρακτήρες που η γραμματοσειρά διαμορφώνει μαζί, όπως ένας βασικός χαρακτήρας και ο συνδυαζόμενος τόνος του, μετακινούνται ως μία μονάδα. |
| `fit` | Όχι | `glyph` | Το `glyph` εφαρμόζει το χωρικό κύμα κατά μήκος του κειμένου. Το `span` δίνει σε ολόκληρο το τμήμα κειμένου που περικλείεται στην ετικέτα μία κοινή κατακόρυφη ημιτονοειδή μετατόπιση. |
| `direction` | Όχι | `forward` | Το `forward` προχωρά κανονικά. Το `reverse` αντιστρέφει την κατεύθυνση διάδοσης του κύματος. |

```text
<wave>Animated character wave</wave>
<wave amplitude=4 hz=3 wavelength=8 fit=glyph>Travelling wave</wave>
<wave amplitude=4 hz=3 wavelength=8 fit=glyph direction=reverse>Reverse travelling wave</wave>
<wave amplitude=4 hz=1 fit=span>Whole span moves together</wave>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=glyph`*

![Δείγμα κειμένου με κινούμενο κύμα ανά γλύφο](images/richtext/wave_glyph.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=span`*

![Δείγμα κειμένου κινείται ως ένα ενιαίο τμήμα κειμένου](images/richtext/wave_span.webp)

</div>
</div>

### `sprite` {#sprite}

Προσθέτει ένα αυτοκλειόμενο αντικείμενο sprite στην τρέχουσα θέση του ορατού κειμένου. Τα γνωρίσματά του διατηρούνται ως μεταδεδομένα για τις `label.get_layout_objects()` και `gui.get_layout_objects()`.

| Γνώρισμα | Υποχρεωτικό | Προεπιλογή | Σημασία |
| --- | --- | --- | --- |
| `id` | Όχι | Παράγεται αυτόματα | Σταθερό αναγνωριστικό που κατακερματίζεται στο `id` του επιστρεφόμενου αντικειμένου διάταξης. |
| `src` | Όχι | Καμία | Αναγνωριστικό πόρου sprite που ορίζει η εφαρμογή, όπως η διαδρομή μιας εικόνας ή ενός atlas στο έργο. |
| `animation` | Όχι | Καμία | Αναγνωριστικό κίνησης μέσα στον πόρο, που ορίζει η εφαρμογή. |
| `width` | Όχι | `1em` | Υπολογισμένο πλάτος του sprite. |
| `height` | Όχι | `1em` | Υπολογισμένο ύψος του sprite. |
| Οποιοδήποτε άλλο γνώρισμα | Όχι | Απουσιάζει | Μεταδεδομένα που ορίζει η εφαρμογή και διατηρούνται για τον μηχανισμό επίλυσης αντικειμένων και τα API αντικειμένων διάταξης. |

```text
A <sprite src=engine/engine/content/builtins/assets/images/logo/logo_256.png/> logo
<sprite src=images/banner.png width=4em height=2em/>
<sprite src=images/icons.atlas animation=coin width=2em/>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*Αποδομένο sprite μέσα στο κείμενο*

![Λογότυπο του Defold που αποδίδεται μέσα στο κείμενο](images/richtext/sprite.webp)

</div>
</div>

Οι διαστάσεις δέχονται θετικές τιμές σε μονάδες διάταξης χωρίς επίθημα ή με `px`, `em` ή `%`. Τόσο το `em` όσο και το `%` χρησιμοποιούν το βασικό μέγεθος γραμματοσειράς της διάταξης κειμένου.

Κάθε διάσταση που παραλείπεται παίρνει ανεξάρτητα την προεπιλεγμένη τιμή `1em`. Η παράλειψη και των δύο παράγει ένα αντικείμενο `1em × 1em`· αν ορίσετε μόνο το πλάτος, το ύψος δεν προκύπτει αυτόματα από την αναλογία διαστάσεων ενός πόρου.

::: important
Η ετικέτα sprite είναι απλώς μια δεσμευμένη θέση όπου ο προγραμματιστής μπορεί να τοποθετήσει οποιοδήποτε αντικείμενο!
:::

### `link` {#link}

Περιγράφει ένα εύρος ορατού κειμένου ως αντικείμενο συνδέσμου. Το κείμενο που περικλείει διατάσσεται κανονικά και λαμβάνει από προεπιλογή το στυλ με όνομα `link`. Τα στοιχεία Label και GUI επιλέγουν τα `link:hover` και `link:active` ως απόκριση στην είσοδο, χωρίς να διαμορφώνουν ξανά το κείμενο. Δείτε τα [Μηνύματα αλληλεπίδρασης](#interaction-messages) για τα μηνύματα που παράγονται από την είσοδο σε συνδέσμους.

| Γνώρισμα | Υποχρεωτικό | Προεπιλογή | Σημασία |
| --- | --- | --- | --- |
| `src` | Όχι | Καμία | Προορισμός συνδέσμου που ορίζει η εφαρμογή. Η τιμή επιστρέφεται ως συμβολοσειρά χωρίς αυτόματη επικύρωση ή πλοήγηση. |
| `id` | Όχι | Παράγεται αυτόματα | Σταθερό αναγνωριστικό που κατακερματίζεται στο `id` του επιστρεφόμενου αντικειμένου διάταξης. |
| `style` | Όχι | `link` | Προεπιλεγμένο στυλ με όνομα για το κείμενο του συνδέσμου. |
| Οποιοδήποτε άλλο γνώρισμα | Όχι | Απουσιάζει | Μεταδεδομένα που ορίζει η εφαρμογή, όπως αναγνωριστικό, ενέργεια, επεξήγηση εργαλείου ή τιμή για ανάλυση χρήσης. |

```text
<ul><link id=website src=https://www.defold.com>www.defold.com</link></ul>
<link id=inventory style=menu_link action=open_inventory item=sword>Iron sword</link>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`style=link`*

![Το www.defold.com αποδίδεται με το προεπιλεγμένο στυλ συνδέσμου και υπογράμμιση](images/richtext/link.webp)

</div>
</div>

Το στοιχείο παρακολουθεί την κατάσταση του δείκτη για κάθε σύνδεσμο. Εφαρμόζει το `link:hover` όσο ο δείκτης βρίσκεται πάνω στον σύνδεσμο και το `link:active` όσο το κουμπί του δείκτη παραμένει πατημένο. Όταν δεν ισχύει καμία από τις δύο καταστάσεις, το στοιχείο επαναφέρει το στυλ που ονομάζεται στο γνώρισμα `style` του συνδέσμου ή το `link` όταν το γνώρισμα απουσιάζει.

### Μηνύματα αλληλεπίδρασης {#interaction-messages}

Η αλληλεπίδραση με συνδέσμους χρησιμοποιεί το κανονικό σύστημα εισόδου του Defold. Προσθέστε μια σύνδεση <kbd>Mouse Trigger</kbd> για το `MOUSE_BUTTON_LEFT`, η οποία ενεργοποιεί και την είσοδο με μία αφή, και αποκτήστε εστίαση εισόδου στο script του αντικειμένου παιχνιδιού ή στο script GUI:

```lua
function init(self)
    msg.post(".", "acquire_input_focus")
end
```

Δείτε την [Εστίαση εισόδου](/manuals/input/#input-focus) και την [Είσοδο ποντικιού και αφής](/manuals/input-mouse-and-touch) για λεπτομέρειες ρύθμισης.

Όταν ένα στοιχείο label ή GUI λαμβάνει είσοδο δείκτη, οι σύνδεσμοι παράγουν τα ακόλουθα μηνύματα. Τα μηνύματα label αποστέλλονται στο αντικείμενο παιχνιδιού στο οποίο ανήκει το στοιχείο· τα μηνύματα GUI αποστέλλονται στο script GUI.

| Μήνυμα | Πότε αποστέλλεται |
| --- | --- |
| `text_object_hovered` | Ο δείκτης εισέρχεται σε έναν σύνδεσμο. |
| `text_object_unhovered` | Ο δείκτης εξέρχεται από έναν σύνδεσμο. |
| `text_object_clicked` | Το πάτημα απελευθερώνεται πάνω στον ίδιο σύνδεσμο. |

Κάθε μήνυμα περιέχει τα εξής πεδία:

| Πεδίο | Τύπος | Περιγραφή |
| --- | --- | --- |
| `id` | `hash` | Το γνώρισμα `id` του αντικειμένου ή το αναγνωριστικό αντικειμένου διάταξης που παράγεται αυτόματα. |
| `type` | `hash` | Ο τύπος του αντικειμένου διάταξης, προς το παρόν `hash("link")`. |
| `src` | `string` | Η τιμή του γνωρίσματος `src` του αντικειμένου που ορίζει η εφαρμογή ή μια κενή συμβολοσειρά όταν απουσιάζει. |

```lua
function on_message(self, message_id, message)
    if message_id == hash("text_object_clicked") then
        assert(message.type == hash("link"))
        print(message.id, message.src)
    end
end
```

## Στυλ με όνομα {#named-styles}

Κάθε συλλογή γραμματοσειρών περιέχει στυλ αντικειμένων με όνομα που επηρεάζουν μόνο την απόδοση. Ένας σύνδεσμος χρησιμοποιεί το στυλ που ονομάζεται στο γνώρισμα `style` του ή το `link` όταν το γνώρισμα απουσιάζει. Δεν υπάρχει γενική ετικέτα `<style>` για τμήματα κειμένου.

Το Defold παρέχει τις ακόλουθες προεπιλογές:

| Στυλ | Πολλαπλασιαστής χρώματος γεμίσματος | Διακόσμηση |
| --- | --- | --- |
| `link` | `(0.10, 0.45, 0.90, 1.0)` | Συνεχής υπογράμμιση |
| `link:hover` | `(0.30, 0.65, 1.00, 1.0)` | Καμία |
| `link:active` | `(0.05, 0.30, 0.70, 1.0)` | Καμία |

Ορίστε ένα στυλ με μια συμβολοσειρά κειμένου που περιέχει ετικέτες ανοίγματος. Οι ετικέτες κλείνουν έμμεσα με αντίστροφη σειρά, επομένως δεν επιτρέπονται ετικέτες κλεισίματος ούτε ορατό κείμενο.

```lua
font.set_style("/fonts/ui.fontc", "link",
    "<color=#2673ff><outline color=#000000 size=1>")

font.set_style("/fonts/ui.fontc", "link:hover",
    "<color=#66b3ff><shake amplitude=0.2 hz=20>")
```

Οι ετικέτες εφαρμόζονται από αριστερά προς τα δεξιά, σαν να ήταν ένθετες γύρω από το κείμενο του αντικειμένου. Ένα στυλ αντικειμένου που επιλέγει ο καλών εφαρμόζεται μετά το προεπιλεγμένο στυλ. Όταν πολλές ετικέτες ορίζουν την ίδια ιδιότητα απόδοσης, η τιμή που εφαρμόζεται αργότερα αντικαθιστά τις προηγούμενες. Τα εφέ προστίθενται με σειρά από αριστερά προς τα δεξιά.

::: sidenote
Η κλήση της `font.set_style()` αντικαθιστά τις ιδιότητες απόδοσης και τα εφέ του συγκεκριμένου στυλ με όνομα. Οι διακοσμήσεις που ορίζονται στον πόρο παραμένουν αμετάβλητες, οπότε ο επανακαθορισμός του `link` δεν αφαιρεί την προεπιλεγμένη υπογράμμισή του. Τα στυλ με όνομα δέχονται ετικέτες που επηρεάζουν μόνο την απόδοση, όπως `color`, `outline`, `shadow`, `gradient`, `wave` και `shake`. Οι ετικέτες που αλλάζουν τη διάταξη, προσθέτουν διακοσμήσεις ή περιγράφουν αντικείμενα απορρίπτονται.
:::

## API αντικειμένων διάταξης {#layout-object-api}

Χρησιμοποιήστε τη `label.get_layout_objects()` ή τη `gui.get_layout_objects()` για να ανακτήσετε τα αντικείμενα `sprite` και `link` από κείμενο του οποίου η διάταξη έχει υπολογιστεί.

### `label.get_layout_objects()` {#labelget_layout_objects}

```lua
objects = label.get_layout_objects(url)
```

| Όρισμα | Τύπος | Περιγραφή |
| --- | --- | --- |
| `url` | `string`, `hash` ή `url` | Το στοιχείο label που θέλετε να εξετάσετε, για παράδειγμα `"#label"`. |

### `gui.get_layout_objects()` {#guiget_layout_objects}

```lua
objects = gui.get_layout_objects(node)
```

| Όρισμα | Τύπος | Περιγραφή |
| --- | --- | --- |
| `node` | `node` | Ο κόμβος κειμένου GUI που θέλετε να εξετάσετε, για παράδειγμα `gui.get_node("rich_text")`. |

Και οι δύο συναρτήσεις επιστρέφουν έναν νέο πίνακα που περιέχει τα τρέχοντα αντικείμενα διάταξης με τη σειρά εμφάνισής τους στο αρχικό κείμενο. Επιστρέφουν κενό πίνακα όταν το κείμενο δεν περιέχει ετικέτες αντικειμένων. Επειδή τα αντικείμενα και τα γνωρίσματά τους αντιγράφονται στη Lua σε κάθε κλήση, αποθηκεύστε προσωρινά το αποτέλεσμα και επαναλάβετε το ερώτημα αφού αλλάξετε το κείμενο ή κάποια άλλη ιδιότητα που αλλάζει τη διάταξή του.

### Πεδία επιστρεφόμενων αντικειμένων {#returned-object-fields}

| Πεδίο | Τύπος | Περιγραφή |
| --- | --- | --- |
| `type` | `string` | `"sprite"` ή `"link"`. |
| `id` | `hash` | Αναγνωριστικό αντικειμένου που χρησιμοποιείται στα μηνύματα αλληλεπίδρασης. |
| `text_offset` | `number` | Θέση στο ορατό κείμενο με αρίθμηση από το μηδέν, μετρημένη σε κωδικά σημεία Unicode. Η σήμανση εξαιρείται και οι οντότητες μετρώνται ως οι αποκωδικοποιημένοι χαρακτήρες τους. Για ένα sprite, αυτή είναι η θέση εισαγωγής του. |
| `text_length` | `number` | Μήκος του ορατού κειμένου που περικλείεται, σε κωδικά σημεία Unicode. Ένα sprite έχει μήκος ένα λόγω του κωδικού σημείου αντικατάστασης αντικειμένου U+FFFC που εισάγεται για αυτό. |
| `width` | `number` | Υπολογισμένο πλάτος σε μονάδες διάταξης κειμένου. Οι σύνδεσμοι έχουν προς το παρόν μηδενικό πλάτος. |
| `height` | `number` | Υπολογισμένο ύψος σε μονάδες διάταξης κειμένου. Οι σύνδεσμοι έχουν προς το παρόν μηδενικό ύψος. |
| `x` | `number` | Οριζόντια θέση της κάτω αριστερής γωνίας του αντικειμένου ως προς την επάνω αριστερή αρχή συντεταγμένων της διάταξης κειμένου. |
| `y` | `number` | Κατακόρυφη θέση της κάτω αριστερής γωνίας του αντικειμένου ως προς την επάνω αριστερή αρχή συντεταγμένων της διάταξης κειμένου. |
| `attributes` | `table` | Όλα τα γνωρίσματα ετικετών ως ζεύγη κλειδιού/τιμής συμβολοσειρών. Οι τιμές των γνωρισμάτων διατηρούν την αρχική τους αναπαράσταση, όπως `"2em"`. Μια σύντομη τιμή χωρίς όνομα αποθηκεύεται στο κλειδί `value`. |

::: sidenote
Τα `text_offset` και `text_length` δεν είναι μετατοπίσεις σε byte UTF-8. Ένας χαρακτήρας εκτός ASCII, όπως το `å` ή το `猫`, μετρά ως μία θέση.
:::

### Παράδειγμα Lua {#lua-example}

```lua
local text = [[
Read the <link src=https://defold.com/manuals/ id=manual>manual</link>
or inspect <sprite src=images/info.png width=2em/> for more information.
]]

go.set("#label", "text", text)

local objects = label.get_layout_objects("#label")
for _, object in ipairs(objects) do
    if object.type == "link" then
        print("link", object.attributes.src)
        print("visible range", object.text_offset, object.text_length)
        print("position", object.x, object.y)
    elseif object.type == "sprite" then
        print("sprite", object.x, object.y, object.width, object.height)
        pprint(object.attributes)
    end
end

local gui_objects = gui.get_layout_objects(gui.get_node("rich_text"))
```

## Χρήσιμοι συνδυασμοί {#useful-combinations}

### Έγχρωμο περίγραμμα με οριζόντια διαβάθμιση {#colored-outline-with-a-horizontal-gradient}

```text
<outline size=2 color=#101820>
    <gradient left=#FEE715 right=#FF6F61>Gradient title</gradient>
</outline>
```

Η διαβάθμιση πολλαπλασιάζει μόνο το χρώμα γεμίσματος· το περίγραμμα διατηρεί το δικό του χρώμα.

### Τρέμουλο σε μια πρόταση, διαβάθμιση σε μία λέξη {#shake-a-sentence-gradient-one-word}

```text
<shake hz=20 amplitude=0.5>
    This <gradient left=#FF00FF right=#FFFFFF>whole</gradient> text shakes!
</shake>
```

Το εξωτερικό εφέ θέσης εφαρμόζεται σε κάθε γλύφο. Το ένθετο εφέ χρώματος εφαρμόζεται μόνο στη λέξη «whole».

### Αντικατάσταση μίας ιδιότητας με διατήρηση των υπόλοιπων {#override-one-property-without-losing-the-others}

```text
<color=#FFFFFF><outline size=2 color=#000000>
    Normal <color=#FF4040>warning</color> normal
</outline></color>
```

Το εσωτερικό χρώμα αλλάζει το γέμισμα διατηρώντας το κληρονομημένο πλάτος και χρώμα περιγράμματος.
