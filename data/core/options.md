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
* specific_deadlines{"subcategory":"2turn","category":"Terminy"}
  - action_general_options

## bot single 3
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
* specific_deadlines{"subcategory":"1turn"}
  - action_general_options
* general_questions{"category":"Rekrutacja"}
  - action_general_options
* general_questions{"category":"Opłaty"}
  - action_general_options
* specific_costs{"subcategory":"students_costs"}
  - action_general_options
* goodbye
  - utter_goodbye

## bot subcategory
* greet
  - utter_greet
  - action_general_options
* general_questions{"subcategory":"1turn"}
  - action_general_options

## bot subcategory 2
* greet
  - utter_greet
  - action_general_options
* general_questions{"subcategory":"1turn"}
  - action_general_options
* specific_recruitment{"subcategory":"limits"}
  - action_general_options

## bot subcategory 3
* greet
  - utter_greet
  - action_general_options
* specific_recruitment{"subcategory":"courses"}
  - action_general_options

## bot subcategory 4
* greet
  - utter_greet
  - action_general_options
* specific_costs{"subcategory":"returns"}
  - action_general_options