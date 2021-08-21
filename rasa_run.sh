#!/bin/bash
cp korean_tokenizer.py $RASA_DIR/nlu/tokenizers
cp crf_entity_extractor_korean.py $RASA_DIR/nlu/extractors
cp bilou_utils_Kr.py $RASA_DIR/nlu/utils
cp registry.py $RASA_DIR/nlu
printf "copy rasa_config\n"

rasa run --endpoints endpoints.yml > rasa.log 2>rasa_error.log &
printf "rasa run endpoints\n"

rasa run actions --actions actions.actions > rasa_actions.log 2>rasa_actions_error.log
printf "rasa run actions\n"