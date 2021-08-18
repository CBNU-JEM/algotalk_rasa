#!/bin/bash

printf "rasa run endpoints\n"
rasa run --endpoints endpoints.yml > rasa.log 2>&1 &

printf "rasa run actions\n"
rasa run actions --actions actions.actions > rasa_actions.log 2>&1
