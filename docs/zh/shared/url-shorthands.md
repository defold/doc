  `.`
  : Shorthand resolving to the current game object.

  `#`
  : Shorthand resolving to the current component.

  For example:

  ```lua
   -- Let this game object acquire input focus
   msg.post(".", "acquire_input_focus")
  ```

  ```lua
   -- Post "reset" to the current script
   msg.post("#", "reset")
  ```
