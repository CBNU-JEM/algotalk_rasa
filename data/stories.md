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

## algorithm explain 1
* algorithm_type{"algorithm_type": "정렬"}
   - utter_sort_algorithm
   

## algorithm explain 2
* algorithm_type{"algorithm_type": "최단거리"}
   - utter_SD_algorithm


## algorithm explain 3
* algorithm_type{"algorithm_type": "스택"}
   - utter_stack_algorithm
   
## contest

## recommendation

## tutorial