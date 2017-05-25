Feature: Eliminar un personatge
  Amb l'objectiu d'eliminar un personatge
  Jo com a usuari
  Vull eliminar un personatge que he creat

  Background: Hi ha un usuari registrat
    Given Existeix un usuari "username" amb contrasenya "password"

Scenario: Eliminar un personatge
    Given Faig login com a usuari "username" amb contrasenya "password"
    And Hi ha un personatge creat pel usuari "username" amb nom "pozo"
    | name            |
    | pozo            |
    | race            |
    | human           |
    | gender          |
    | male            |
    | level           |
    | 80              |
    | guild           |
    | The Guild       |
    | profession_type |
    | Guardian        |
    When Eliminar el personatge "pozo"
    Then Comprovo que s'ha borrat el personatge