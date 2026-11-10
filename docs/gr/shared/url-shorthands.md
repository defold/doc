  `.`
  : Συντόμευση που αναφέρεται στο τρέχον αντικείμενο παιχνιδιού.

  `#`
  : Συντόμευση που αναφέρεται στο τρέχον στοιχείο.

  Για παράδειγμα:

  ```lua
   -- Let this game object acquire input focus
   msg.post(".", "acquire_input_focus")
  ```

  ```lua
   -- Post "reset" to the current script
   msg.post("#", "reset")
  ```
