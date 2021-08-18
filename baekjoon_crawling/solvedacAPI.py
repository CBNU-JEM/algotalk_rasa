# -*- coding: utf-8 -*-
import os

from bs4 import BeautifulSoup
from pprint import pprint
import requests
import json
import time


def get_problem_level_from_solvedac(problem_id):
    url = "https://solved.ac/api/v3/problem/show?problemId="
    url += str(problem_id)
    response = requests.get(url)
    # print(response.status_code)
    # print(response.text)
    response_json = response.json()
    # print(response_json["level"])
    return response_json["level"]