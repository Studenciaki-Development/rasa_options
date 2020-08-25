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
* general_questions{"category":"costs"}
  - action_general_options

## bot single 2
* greet
  - utter_greet
  - action_general_options
* general_questions{"category":"deadlines"}
  - action_general_options

## bot single 2
* greet
  - utter_greet
  - action_general_options
* general_questions{"category":"recruitment"}
  - action_general_options

## bot challenge + question
* bot_challenge
  - utter_iamabot
* general_questions{"category":"deadlines"}
  - action_general_options
* general_questions{"category":"recruitment"}
  - action_general_options
* general_questions{"category":"costs"}
  - action_general_options
* goodbye
  - utter_goodbye