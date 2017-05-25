Feature: Crear Personatge
  Amb l'objectiu de crear una instància d'un personatge
  Jo com a usuari
  Vull crear un personatge personalitzat

  Background: Hi ha un usuari registrat
    Given Existeix un usuari "user" amb contrasenya "password"

  Scenario: Crear un personatge
    Given Faig login com a usuari "user" amb contrasenya "password"
    When Crea un personatge
    | name            |
    | character       |
    | player          |
    | user            |
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
    Then Si miro el detalls del personatge pel usuari "user"
    | name            |
    | character       |
    | player          |
    | user            |
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
    And Hi ha 1 personatge creat