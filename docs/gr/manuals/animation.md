---
title: Εγχειρίδιο Animation στη Defold
brief: Αυτό το εγχειρίδιο περιγράφει την υποστήριξη animation του Defold.
---

# Κινούμενων γραφικών

Το Defold διαθέτει ενσωματωμένη υποστήριξη για πολλούς τύπους κινούμενων γραφικών που μπορείτε να χρησιμοποιήσετε ως πηγή γραφικών για στοιχεία:

* Flip-book animation
* Κινούμενη εικόνα της σπονδυλικής στήλης
* 3D κινούμενα σχέδια
* Κινούμενα σχέδια ιδιοκτησίας

## Κινούμενη εικόνα flip-book

Ένα animation flipbook αποτελείται από μια σειρά ακίνητων εικόνων που εμφανίζονται διαδοχικά. Η τεχνική είναι πολύ παρόμοια με την παραδοσιακή κινούμενη εικόνα των κυττάρων (βλ. Http://en.wikipedia.org/wiki/Traditional_animation). Η τεχνική προσφέρει απεριόριστες ευκαιρίες δεδομένου ότι κάθε πλαίσιο μπορεί να χειριστεί μεμονωμένα. Ωστόσο, δεδομένου ότι κάθε πλαίσιο αποθηκεύεται σε μια μοναδική εικόνα, το αποτύπωμα μνήμης μπορεί να είναι υψηλό. Η ομαλότητα της κινούμενης εικόνας εξαρτάται επίσης από τον αριθμό των εικόνων που εμφανίζονται κάθε δευτερόλεπτο, αλλά η αύξηση του αριθμού των εικόνων συνήθως αυξάνει επίσης την ποσότητα εργασίας. Τα κινούμενα σχέδια του Defold flipbook αποθηκεύονται είτε ως μεμονωμένες εικόνες που προστίθενται σε [Atlas](/manuals/atlas), είτε ως [Tile Source](/manuals/tilesource) με όλα τα καρέ να είναι οριζόντια.

  ![Animation sheet](images/animation/animsheet.png){.inline}
  ![Run loop](images/animation/runloop.gif){.inline}

## 3D κινούμενα γραφικά

Το σκελετικό animation των τρισδιάστατων μοντέλων είναι παρόμοιο με το Spine animation, αλλά λειτουργεί σε 3D σε αντίθεση με το 2D. Το τρισδιάστατο μοντέλο δεν είναι κομμένο σε ξεχωριστά μέρη και δεμένο σε κόκαλο, όπως σε κινούμενα σχέδια. Αντ 'αυτού, τα οστά εφαρμόζουν παραμόρφωση στις κορυφές του μοντέλου και έχετε μεγάλο έλεγχο του πόσο ένα οστό πρέπει να επηρεάζει τις κορυφές.

  Για λεπτομέρειες σχετικά με τον τρόπο εισαγωγής δεδομένων 3D σε ένα μοντέλο για κινούμενα σχέδια, ανατρέξτε στο [Model documentation](/manuals/model).

  ![Blender animation](images/animation/blender_animation.png){.inline srcset="images/animation/blender_animation@2x.png 2x"}
  ![Wiggle loop](images/animation/suzanne.gif){.inline}


## Ιδιότητα Κινούμενων γραφικών 

Όλες οι αριθμητικές ιδιότητες (numbers, vector3, vector4 and quaterions) και οι σταθερές shader μπορούν να κινούνται με το ενσωματωμένο σύστημα κινούμενης εικόνας, χρησιμοποιώντας τη συνάρτηση  `go.animate()`. η μηχανή θα "tween" ιδιότητες αυτόματα για εσάς σύμφωνα με δεδομένες λειτουργίες αναπαραγωγής και λειτουργίες χαλάρωσης. Μπορείτε επίσης να καθορίσετε προσαρμοσμένες λειτουργίες χαλάρωσης.

  ![Property animation](images/animation/property_animation.png){.inline srcset="images/animation/property_animation@2x.png 2x"}
  ![Bounce loop](images/animation/bounce.gif){.inline}

## Αναπαραγωγή κινούμενων εικόνων

Οι κόμβοι Sprites και GUI μπορούν να αναπαράγουν κινούμενες εικόνες με flip-book και έχετε μεγάλο έλεγχο σε αυτά κατά την εκτέλεση.

Σπρέι
: Για να εκτελέσετε μια κινούμενη εικόνα κατά τη διάρκεια του χρόνου εκτέλεσης, χρησιμοποιείτε τη λειτουργία [`sprite.play_flipbook()`](/ref/sprite/?q=play_flipbook#sprite.play_flipbook:url-id-[complete_function]-[play_properties]) function. Δείτε παρακάτω για ένα παράδειγμα.

Κόμβοι πλαισίου GUI
: Για να εκτελέσετε μια κινούμενη εικόνα κατά τη διάρκεια του χρόνου εκτέλεσης, χρησιμοποιείτε τη λειτουργία [`gui.play_flipbook()`](/ref/gui/?q=play_flipbook#gui.play_flipbook:node-animation-[complete_function]-[play_properties]) function. Δείτε παρακάτω για ένα παράδειγμα.

::: υποσημείωση
Η λειτουργία αναπαραγωγής μόλις το πινγκ πονγκ θα αναπαράγει το κινούμενο σχέδιο μέχρι το τελευταίο καρέ και στη συνέχεια θα αντιστρέψει τη σειρά και θα αναπαράγει μέχρι το ** δεύτερο ** καρέ της κινούμενης εικόνας, όχι πίσω στο πρώτο καρέ. Αυτό γίνεται έτσι ώστε η αλυσίδα των κινούμενων σχεδίων να γίνεται ευκολότερη.
:::

### Παράδειγμα Sprite

Ας υποθέσουμε ότι το παιχνίδι σας διαθέτει δυνατότητα "αποφυγής" που επιτρέπει στον παίκτη να πατήσει ένα συγκεκριμένο κουμπί για να αποφύγει. Έχετε δημιουργήσει τέσσερα κινούμενα σχέδια για να υποστηρίξετε τη λειτουργία με οπτικά σχόλια:

"idle"(αδρανής)
: Ένα κινούμενο σχέδιο βρόχου του ρελαντί χαρακτήρα του παίκτη.

"dodge_idle"
: Ένα κινούμενο σχέδιο βρόχου του χαρακτήρα του παίκτη στο ρελαντί ενώ βρίσκεται στη στάση αποφυγής.

"start_dodge"
: Ένα κινούμενο σχέδιο μετάβασης μιας φοράς που παίρνει τον χαρακτήρα του παίκτη από τη στάση έως την αποφυγή.

"stop_dodge"
: Ένα κινούμενο σχέδιο μετάβασης με μία φορά που μεταφέρει τον χαρακτήρα του παίκτη από την αποφυγή της στάσης.

Το ακόλουθο script παρέχει τη λογική:

```lua

local function play_idle_animation(self)
    if self.dodge then
        sprite.play_flipbook("#sprite", hash("dodge_idle"))
    else
        sprite.play_flipbook("#sprite", hash("idle"))
    end
end

function on_input(self, action_id, action)
    -- "dodge" is our input action
    if action_id == hash("dodge") then
        if action.pressed then
            sprite.play_flipbook("#sprite", hash("start_dodge"), play_idle_animation)
            -- remember that we are dodging
            self.dodge = true
        elseif action.released then
            sprite.play_flipbook("#sprite", hash("stop_dodge"), play_idle_animation)
            -- we are not dodging anymore
            self.dodge = false
        end
    end
end
```

### Παράδειγμα κόμβου GUI

Όταν επιλέγετε μια κινούμενη εικόνα ή μια εικόνα για έναν κόμβο, στην πραγματικότητα εκχωρείτε την πηγή εικόνας (πηγή άτλαντα ή πλακίδια) και την προεπιλεγμένη κινούμενη εικόνα με μία κίνηση. Η πηγή εικόνας ορίζεται στατικά στον κόμβο, αλλά η τρέχουσα κινούμενη εικόνα για αναπαραγωγή μπορεί να αλλάξει κατά το χρόνο εκτέλεσης. Οι ακίνητες εικόνες αντιμετωπίζονται ως κινούμενες εικόνες ενός καρέ, οπότε η αλλαγή μιας εικόνας σημαίνει ότι ο χρόνος εκτέλεσης ισοδυναμεί με την αναπαραγωγή ενός διαφορετικού κινούμενου βιβλίου flipbook για τον κόμβο:

```lua
local function flipbook_done(self)
    msg.post("#", "jump_completed")
end

function init(self)
    local character_node = gui.get_node("character")
    -- This requires that the node has a default animation in the same atlas or tile source as
    -- the new animation/image we're playing.
    gui.play_flipbook(character_node, "jump_left", flipbook_done)
end
```

Μπορεί να παρέχεται μια προαιρετική συνάρτηση που καλείται μετά την ολοκλήρωση. Θα κληθεί σε κινούμενα σχέδια που αναπαράγονται σε οποιαδήποτε από τις λειτουργίες `ONCE_*`.

## 3D μοντέλο κινουμένων σχεδίων

Τα μοντέλα είναι κινούμενα με το [`model.play_anim()`](/ref/model#model.play_anim) function:

```lua
function init(self)
    -- Start the "wiggle" animation back and forth on #model
    model.play_anim("#model", "wiggle", go.PLAYBACK_LOOP_PINGPONG)
end
```

::: σημαντικό
Το Defold υποστηρίζει προς το παρόν μόνο κινούμενες εικόνες. Τα κινούμενα σχέδια πρέπει να έχουν πίνακες για κάθε κινούμενο οστό κάθε βασικό καρέ και όχι θέση, περιστροφή και κλίμακα ως ξεχωριστά πλήκτρα.

Τα κινούμενα σχέδια παρεμβάλλονται επίσης γραμμικά. Εάν κάνετε πιο προηγμένη παρεμβολή καμπύλης, τα κινούμενα σχέδια πρέπει να προκαταβληθούν από τον εξαγωγέα.

Δεν υποστηρίζονται κλιπ κινουμένων σχεδίων στο Collada. Για να χρησιμοποιήσετε πολλά κινούμενα σχέδια ανά μοντέλο, εξαγάγετε τα σε ξεχωριστά αρχεία *.dae* και συγκεντρώστε τα αρχεία σε ένα αρχείο *.animationset* στο Defold.
:::

### 3D Μοντέλο - Η ιεραρχία των οστών

Τα οστά στο σκελετό του Μοντέλου παρουσιάζονται εσωτερικά ως αντικείμενα παιχνιδιού.

Μπορείτε να ανακτήσετε το αναγνωριστικό παρουσίας του αντικειμένου παιχνιδιού οστών στο χρόνο εκτέλεσης. Η λειτουργία [`model.get_go()`](/ref/model#model.get_go) επιστρέφει το αναγνωριστικό του αντικειμένου παιχνιδιού για το καθορισμένο κόκκαλο.

```lua
-- Get the middle bone go of our wiggler model
local bone_go = model.get_go("#wiggler", "Bone_002")

-- Now do something useful with the game object...
```

### 3D Μοντέλο - Κινούμενα σχέδια δρομέα

Ακριβώς όπως τα μοντέλα Spine, τα 3D μοντέλα μπορούν να κινούνται με χειρισμό της ιδιότητας `cursor`:

```lua
-- Set the animation on #model but don't start it
model.play_anim("#model", "wiggle", go.PLAYBACK_NONE)
-- Set the cursor to the beginning of the animation
go.set("#model", "cursor", 0)
-- Tween the cursor between 0 and 1 pingpong with in-out quad easing.
go.animate("#model", "cursor", go.PLAYBACK_LOOP_PINGPONG, 1, go.EASING_INOUTQUAD, 3)
```

## Property animation

## Κίνηση ιδιοκτησίας

Για να κινήσετε ένα αντικείμενο παιχνιδιού ή μια ιδιότητα στοιχείου, χρησιμοποιήστε τη συνάρτηση `go.animate()`. Για ιδιότητες κόμβου GUI, η αντίστοιχη συνάρτηση είναι `gui.animate()`.

```lua
-- Set the position property y component to 200
go.set(".", "position.y", 200)
-- Then animate it
go.animate(".", "position.y", go.PLAYBACK_LOOP_PINGPONG, 100, go.EASING_OUTBOUNCE, 2)
```

Για να σταματήσετε όλες τις κινούμενες εικόνες μιας συγκεκριμένης ιδιότητας, καλέστε `go.cancel_animations()`, ή για κόμβους GUI, `gui.cancel_animation()`:

```lua
-- Stop euler z rotation animation on the current game object
go.cancel_animation(".", "euler.z")
```

Εάν ακυρώσετε την κινούμενη εικόνα μιας σύνθετης ιδιότητας, όπως `position`, θα ακυρωθούν επίσης κινούμενες εικόνες των υπο-στοιχείων (`position.x`, `position.y` και `position.z`).

Το [Properties Manual](/manuals/properties) περιέχει όλες τις διαθέσιμες ιδιότητες σε αντικείμενα παιχνιδιών, στοιχεία και κόμβους GUI.

## Κίνηση ιδιοτήτων κόμβου GUI

Σχεδόν όλες οι ιδιότητες κόμβου GUI είναι δυνατές για κινούμενη εικόνα. Μπορείτε, για παράδειγμα, να κάνετε έναν κόμβο αόρατο ορίζοντας την ιδιότητα `color` σε πλήρη διαφάνεια και, στη συνέχεια, να τον εξασθενίσετε, κινούμενος το χρώμα σε λευκό (δηλ. Χωρίς χρώμα απόχρωσης).

```lua
local node = gui.get_node("button")
local color = gui.get_color(node)
-- Animate the color to white
gui.animate(node, gui.PROP_COLOR, vmath.vector4(1, 1, 1, 1), gui.EASING_INOUTQUAD, 0.5)
-- Animate the outline red color component
gui.animate(node, "outline.x", 1, gui.EASING_INOUTQUAD, 0.5)
-- And move to x position 100
gui.animate(node, hash("position.x"), 100, gui.EASING_INOUTQUAD, 0.5)
```

## Λειτουργίες αναπαραγωγής

Τα κινούμενα σχέδια μπορούν να παιχτούν είτε μία φορά είτε σε ένα βρόχο. Πώς καθορίζεται η αναπαραγωγή της κινούμενης εικόνας από τη λειτουργία αναπαραγωγής:

* go.PLAYBACK_NONE
* go.PLAYBACK_ONCE_FORWARD
* go.PLAYBACK_ONCE_BACKWARD
* go.PLAYBACK_ONCE_PINGPONG
* go.PLAYBACK_LOOP_FORWARD
* go.PLAYBACK_LOOP_BACKWARD
* go.PLAYBACK_LOOP_PINGPONG

Οι λειτουργίες pingpong εκτελούν το animation πρώτα προς τα εμπρός και μετά προς τα πίσω. Υπάρχει ένα σύνολο αντίστοιχων λειτουργιών για κινούμενα σχέδια ιδιοτήτων GUI:

* gui.PLAYBACK_NONE
* gui.PLAYBACK_ONCE_FORWARD
* gui.PLAYBACK_ONCE_BACKWARD
* gui.PLAYBACK_ONCE_PINGPONG
* gui.PLAYBACK_LOOP_FORWARD
* gui.PLAYBACK_LOOP_BACKWARD
* gui.PLAYBACK_LOOP_PINGPONG

## Easing

Το Easing καθορίζει πώς αλλάζει η κινούμενη τιμή με την πάροδο του χρόνου. Οι παρακάτω εικόνες περιγράφουν τις λειτουργίες που εφαρμόζονται με την πάροδο του χρόνου για τη δημιουργία της easing.

Τα παρακάτω είναι έγκυρες τιμές easing για `go.animate()`:

|---|---|
| go.EASING_LINEAR | |
| go.EASING_INBACK | go.EASING_OUTBACK |
| go.EASING_INOUTBACK | go.EASING_OUTINBACK |
| go.EASING_INBOUNCE | go.EASING_OUTBOUNCE |
| go.EASING_INOUTBOUNCE | go.EASING_OUTINBOUNCE |
| go.EASING_INELASTIC | go.EASING_OUTELASTIC |
| go.EASING_INOUTELASTIC | go.EASING_OUTINELASTIC |
| go.EASING_INSINE | go.EASING_OUTSINE |
| go.EASING_INOUTSINE | go.EASING_OUTINSINE |
| go.EASING_INEXPO | go.EASING_OUTEXPO |
| go.EASING_INOUTEXPO | go.EASING_OUTINEXPO |
| go.EASING_INCIRC | go.EASING_OUTCIRC |
| go.EASING_INOUTCIRC | go.EASING_OUTINCIRC |
| go.EASING_INQUAD | go.EASING_OUTQUAD |
| go.EASING_INOUTQUAD | go.EASING_OUTINQUAD |
| go.EASING_INCUBIC | go.EASING_OUTCUBIC |
| go.EASING_INOUTCUBIC | go.EASING_OUTINCUBIC |
| go.EASING_INQUART | go.EASING_OUTQUART |
| go.EASING_INOUTQUART | go.EASING_OUTINQUART |
| go.EASING_INQUINT | go.EASING_OUTQUINT |
| go.EASING_INOUTQUINT | go.EASING_OUTINQUINT |

Τα παρακάτω είναι έγκυρες τιμές χαλάρωσης για `gui.animate()`:

|---|---|
| gui.EASING_LINEAR | |
| gui.EASING_INBACK | gui.EASING_OUTBACK |
| gui.EASING_INOUTBACK | gui.EASING_OUTINBACK |
| gui.EASING_INBOUNCE | gui.EASING_OUTBOUNCE |
| gui.EASING_INOUTBOUNCE | gui.EASING_OUTINBOUNCE |
| gui.EASING_INELASTIC | gui.EASING_OUTELASTIC |
| gui.EASING_INOUTELASTIC | gui.EASING_OUTINELASTIC |
| gui.EASING_INSINE | gui.EASING_OUTSINE |
| gui.EASING_INOUTSINE | gui.EASING_OUTINSINE |
| gui.EASING_INEXPO | gui.EASING_OUTEXPO |
| gui.EASING_INOUTEXPO | gui.EASING_OUTINEXPO |
| gui.EASING_INCIRC | gui.EASING_OUTCIRC |
| gui.EASING_INOUTCIRC | gui.EASING_OUTINCIRC |
| gui.EASING_INQUAD | gui.EASING_OUTQUAD |
| gui.EASING_INOUTQUAD | gui.EASING_OUTINQUAD |
| gui.EASING_INCUBIC | gui.EASING_OUTCUBIC |
| gui.EASING_INOUTCUBIC | gui.EASING_OUTINCUBIC |
| gui.EASING_INQUART | gui.EASING_OUTQUART |
| gui.EASING_INOUTQUART | gui.EASING_OUTINQUART |
| gui.EASING_INQUINT | gui.EASING_OUTQUINT |
| gui.EASING_INOUTQUINT | gui.EASING_OUTINQUINT |

![Linear interpolation](images/properties/easing_linear.png){.inline}
![In back](images/properties/easing_inback.png){.inline}
![Out back](images/properties/easing_outback.png){.inline}
![In-out back](images/properties/easing_inoutback.png){.inline}
![Out-in back](images/properties/easing_outinback.png){.inline}
![In bounce](images/properties/easing_inbounce.png){.inline}
![Out bounce](images/properties/easing_outbounce.png){.inline}
![In-out bounce](images/properties/easing_inoutbounce.png){.inline}
![Out-in bounce](images/properties/easing_outinbounce.png){.inline}
![In elastic](images/properties/easing_inelastic.png){.inline}
![Out elastic](images/properties/easing_outelastic.png){.inline}
![In-out elastic](images/properties/easing_inoutelastic.png){.inline}
![Out-in elastic](images/properties/easing_outinelastic.png){.inline}
![In sine](images/properties/easing_insine.png){.inline}
![Out sine](images/properties/easing_outsine.png){.inline}
![In-out sine](images/properties/easing_inoutsine.png){.inline}
![Out-in sine](images/properties/easing_outinsine.png){.inline}
![In exponential](images/properties/easing_inexpo.png){.inline}
![Out exponential](images/properties/easing_outexpo.png){.inline}
![In-out exponential](images/properties/easing_inoutexpo.png){.inline}
![Out-in exponential](images/properties/easing_outinexpo.png){.inline}
![In circlic](images/properties/easing_incirc.png){.inline}
![Out circlic](images/properties/easing_outcirc.png){.inline}
![In-out circlic](images/properties/easing_inoutcirc.png){.inline}
![Out-in circlic](images/properties/easing_outincirc.png){.inline}
![In quadratic](images/properties/easing_inquad.png){.inline}
![Out quadratic](images/properties/easing_outquad.png){.inline}
![In-out quadratic](images/properties/easing_inoutquad.png){.inline}
![Out-in quadratic](images/properties/easing_outinquad.png){.inline}
![In cubic](images/properties/easing_incubic.png){.inline}
![Out cubic](images/properties/easing_outcubic.png){.inline}
![In-out cubic](images/properties/easing_inoutcubic.png){.inline}
![Out-in cubic](images/properties/easing_outincubic.png){.inline}
![In quartic](images/properties/easing_inquart.png){.inline}
![Out quartic](images/properties/easing_outquart.png){.inline}
![In-out quartic](images/properties/easing_inoutquart.png){.inline}
![Out-in quartic](images/properties/easing_outinquart.png){.inline}
![In quintic](images/properties/easing_inquint.png){.inline}
![Out quintic](images/properties/easing_outquint.png){.inline}
![In-out quintic](images/properties/easing_inoutquint.png){.inline}
![Out-in quintic](images/properties/easing_outinquint.png){.inline}

## Custom easing

Μπορείτε να δημιουργήσετε προσαρμοσμένες καμπύλες χαλάρωσης καθορίζοντας ένα `vector` με ένα σύνολο τιμών και, στη συνέχεια, παρέχετε το διάνυσμα αντί για μία από τις προκαθορισμένες σταθερές χαλάρωσης παραπάνω. Οι διανυσματικές τιμές εκφράζουν μια καμπύλη από την τιμή έναρξης (`0`) έως την τιμή-στόχο (`1`). Ο χρόνος εκτέλεσης δειγμάτων από το διάνυσμα και παρεμβάλλεται γραμμικά κατά τον υπολογισμό τιμών μεταξύ των σημείων που εκφράζονται στο διάνυσμα.

Για παράδειγμα, το διάνυσμα:

```lua
local values = { 0, 0.4, 0.2, 0.2, 0.5. 1 }
local my_easing = vmath.vector(values)
```

αποδίδει την ακόλουθη καμπύλη:

![Custom curve](images/animation/custom_curve.png)

Το ακόλουθο παράδειγμα αναγκάζει τη θέση y ενός αντικειμένου παιχνιδιού να μεταπηδήσει μεταξύ της τρέχουσας θέσης και 200 ​​σύμφωνα με μια τετραγωνική καμπύλη:

```lua
local values = { 0, 0, 0, 0, 0, 0, 0, 0,
                 1, 1, 1, 1, 1, 1, 1, 1,
                 0, 0, 0, 0, 0, 0, 0, 0,
                 1, 1, 1, 1, 1, 1, 1, 1,
                 0, 0, 0, 0, 0, 0, 0, 0,
                 1, 1, 1, 1, 1, 1, 1, 1,
                 0, 0, 0, 0, 0, 0, 0, 0,
                 1, 1, 1, 1, 1, 1, 1, 1 }
local square_easing = vmath.vector(values)
go.animate("go", "position.y", go.PLAYBACK_LOOP_PINGPONG, 200, square_easing, 2.0)
```

![Square curve](images/animation/square_curve.png)

## Επιστροφές κλήσεων ολοκλήρωσης - Completion callbacks

Όλες οι συναρτήσεις κινούμενης εικόνας (`go.animate()`, `gui.animate()`, `gui.play_flipbook()`, `sprite.play_flipbook()` και `model.play_anim()`)  υποστηρίζουν μια προαιρετική λειτουργία επανάκλησης Lua ως το τελευταίο όρισμα. Αυτή η λειτουργία θα κληθεί όταν το κινούμενο σχέδιο έχει παιχτεί μέχρι το τέλος. Η λειτουργία δεν απαιτείται ποτέ για βρόχους κινούμενων εικόνων, ούτε όταν μια κινούμενη εικόνα ακυρώνεται χειροκίνητα μέσω του `go.cancel_animations()`. Η επιστροφή κλήσης μπορεί να χρησιμοποιηθεί για την ενεργοποίηση συμβάντων κατά την ολοκλήρωση των κινούμενων σχεδίων ή για την αλυσίδα πολλαπλών κινούμενων σχεδίων μαζί.


Η ακριβής υπογραφή λειτουργίας της επιστροφής κλήσης διαφέρει ελαφρώς μεταξύ των λειτουργιών κινούμενης εικόνας. Δείτε την τεκμηρίωση API για τη λειτουργία που χρησιμοποιείτε.

```lua
local function done_bouncing(self, url, property)
    -- We're done animating. Do something...
end

function init(self)
    go.animate(".", "position.y", go.PLAYBACK_ONCE_FORWARD, 100, go.EASING_OUTBOUNCE, 2, 0, done_bouncing)
end
```
