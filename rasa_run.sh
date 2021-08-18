#!/bin/bash

printf "rasa run actions\n"
nohup rasa run actions --actions actions.actions > rasa_actions.log 2>&1 &

printf "rasa run endpoints\n"
nohup run --endpoints endpoints.yml > rasa.log 2>&1 &