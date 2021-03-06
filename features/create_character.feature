Feature: Crear Personatge
  Amb l'objectiu de crear una instància d'un personatge
  Jo com a usuari
  Vull crear un personatge personalitzat

  Background: Hi ha un usuari registrat
    Given Existeix un usuari "username" amb contrasenya "password"

  Scenario: Crear un personatge
    Given Faig login com a usuari "username" amb contrasenya "password"
    When Crea un personatge "pozo"
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
    Then Hi ha un personatge mes creat