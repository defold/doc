  `.`
  : Skrót oznaczający obecny obiekt gry.

  `#`
  : Skrót oznaczający obecny komponent.

  Na przykład:

  ```lua
   -- Let this game object acquire input focus
   msg.post(".", "acquire_input_focus")
  ```

  ```lua
   -- Post "reset" to the current script
   msg.post("#", "reset")
  ```
