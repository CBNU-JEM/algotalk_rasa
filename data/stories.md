## happy path
* greet
  - utter_greet
* mood_great
  - utter_happy

## sad path 1
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* affirm
  - utter_happy

## sad path 2
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* deny
  - utter_goodbye

## say goodbye
* goodbye
  - utter_goodbye

## bot challenge
* bot_challenge
  - utter_iamabot
  
## user asks whats possible
* ask_whatspossible
  - utter_explain_whatspossible
  
## say thanks
* thanks
  - utter_thank

## algorithm explain 
* algorithm_explain
  - algorithm_form
  - form{"name": "algorithm_form"}
  - slot{"requested_slot": "algorithm_name"}
  - form{"name": null}
  - action_algorithm_explain

## contest explain
* contest_explain
  - contest_form
  - form{"name": "contest_form"}
  - slot{"requested_slot": "contest_name"}
  - form{"name": null}
  - action_contest_explain

## recommendation
* problem_type
  - problem_form
  - form{"name": "problem_form"}
  - slot{"requested_slot":"level"}
  - form{"name": null}
  - action_problem_recommended
  
## change_problem
* change
  - action_problem_recommended


## change_problem_easy
* change_easy
  - action_level_change_easy
  - action_problem_recommended


## change_problem_hard
* change_hard
  - action_level_change_hard
  - action_problem_recommended
  
## tutorial
