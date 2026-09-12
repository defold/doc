  `.`
  : Kurzform, die auf das aktuelle Spielobjekt (game object) verweist.

  `#`
  : Kurzform, die auf die aktuelle Komponente (component) verweist.

  Zum Beispiel:

  ```lua
   -- Let this game object acquire input focus
   msg.post(".", "acquire_input_focus")
  ```

  ```lua
   -- Post "reset" to the current script
   msg.post("#", "reset")
  ```
