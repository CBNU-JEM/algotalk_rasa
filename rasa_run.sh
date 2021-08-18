#!/bin/bash

printf "rasa run actions"
rasa run actions --actions actions.actions

printf "rasa run endpoints"
rasa run --endpoints endpoints.yml