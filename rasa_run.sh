#!/bin/bash

printf "rasa run actions\n"
nohup rasa run actions --actions actions.actions &

printf "rasa run endpoints\n"
nohup rasa run --endpoints endpoints.yml &