## base
* greet
  - utter_greet
  - action_general_options
* goodbye
  - utter_goodbye

## bot challenge
* bot_challenge
  - utter_iamabot

## base + challenge
* greet
  - utter_greet
  - action_general_options
* bot_challenge
  - utter_iamabot
* goodbye
  - utter_goodbye

## bot single 1
* greet
  - utter_greet
  - action_general_options
* general_questions{"category":"Opłaty"}
  - action_general_options

## bot single 2
* greet
  - utter_greet
  - action_general_options
* general_questions{"category":"Terminy"}
  - action_general_options
* specific_dedlines_turns{"subcategory_Terminy":"2turn","category":"Terminy"}
  - action_general_options

## bot single 2
* greet
  - utter_greet
  - action_general_options
* general_questions{"category":"Rekrutacja"}
  - action_general_options

## bot challenge + question
* bot_challenge
  - utter_iamabot
* general_questions{"category":"Terminy"}
  - action_general_options
* specific_dedlines_turns{"subcategory_Terminy":"1turn"}
  - action_general_options
* general_questions{"category":"Rekrutacja"}
  - action_general_options
* general_questions{"category":"Opłaty"}
  - action_general_options
* goodbye
  - utter_goodbye

## bot subcategory
* greet
  - utter_greet
  - action_general_options
* general_questions{"subcategory_Terminy":"1turn"}
  - action_general_options