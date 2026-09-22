  `.`
  : Raccourci désignant l'objet de jeu (game object) actuel.

  `#`
  : Raccourci désignant le composant (component) actuel.

  Par exemple :

  ```lua
   -- Let this game object acquire input focus
   msg.post(".", "acquire_input_focus")
  ```

  ```lua
   -- Post "reset" to the current script
   msg.post("#", "reset")
  ```
