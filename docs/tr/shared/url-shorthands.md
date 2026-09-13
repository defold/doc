  `.`
  : Geçerli oyun nesnesine (game object) karşılık gelen kısa gösterim.

  `#`
  : Geçerli bileşene (component) karşılık gelen kısa gösterim.

  Örneğin:

  ```lua
   -- Let this game object acquire input focus
   msg.post(".", "acquire_input_focus")
  ```

  ```lua
   -- Post "reset" to the current script
   msg.post("#", "reset")
  ```
