#!/bin/bash

printf "rasa run actions\n"
rasa run actions --actions actions.actions &

printf "rasa run endpoints\n"
rasa run --endpoints endpoints.yml &