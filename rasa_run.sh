#!/bin/bash

printf "rasa run endpoints\n"
run --endpoints endpoints.yml > rasa.log 2>&1 &

printf "rasa run actions\n"
rasa run actions --actions actions.actions > rasa_actions.log 2>&1
