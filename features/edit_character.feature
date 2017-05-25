Feature: Editar un personatge
  Amb l'objectiu d'editar un personatge
  Jo com a usuari
  Vull editar un personatge que he creat

  Background: Hi ha un usuari registrat
    Given Existeix un usuari "username" amb contrasenya "password"

Scenario: Editar un personatge
    Given Faig login com a usuari "username" amb contrasenya "password"
    And Existeix un personatge creat pel usuari "username" amb nom "pozo"
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
    When Editar un personatge "pozo" canviant el nom a "manolito" i guild a "No Guild"
    | name            |
    | manolito        |
    | guild           |
    | No Guild        |
    Then Comprovo que s'ha modificat el personatge amb el camp nom "manolito" i camp guild "No Guild"
    | name            |
    | manolito        |
    | guild           |
    | No Guild        |
    And Segueix existint el mateix nombre de personatge