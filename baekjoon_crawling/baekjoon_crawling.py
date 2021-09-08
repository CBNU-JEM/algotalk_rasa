# -*- coding: utf-8 -*-
import os

from bs4 import BeautifulSoup
from pprint import pprint
import requests
import json
import time
import solvedacAPI


def get_url_of_algorithm():
    file_path = "./json/url_of_algorithm.json"
    html = requests.get('https://www.acmicpc.net/problem/tags')
    soup = BeautifulSoup(html.text, 'html.parser')

    trs = soup.select('body > div.wrapper > div.container.content > div:nth-child(5) > div > div > table > tbody > tr')
    a_list = list()
    link_list = {}
    link_list['algorithm'] = []

    for tr in trs:
        a_list.append(tr.select_one('td:nth-child(1)').find('a'))

    for a in a_list:
        href = "https://www.acmicpc.net" + a.attrs['href']
        text = a.string
        link_list['algorithm'].append({"classification": text, "url": href})

    print(link_list)

    with open(file_path, 'w', encoding='UTF-8') as outfile:
        json.dump(link_list, outfile, indent=4, ensure_ascii=False)


def get_problem_url_per_algorithm_step_1():
    file_path = "./json/url_of_algorithm.json"
    with open(file_path, 'r', encoding='UTF-8') as readfile:
        algorithm_data = json.load(readfile)
        # print(algorithm_data)

    for a in algorithm_data['algorithm']:
        get_problem_url_per_algorithm_step_2(a['classification'], a['url'])
        time.sleep(3)


def get_problem_url_per_algorithm_step_2(classification, url_per_algorithm):
    file_path = "./json/url_of_problem_per_algorithm.json"
    html = requests.get(url_per_algorithm)
    soup = BeautifulSoup(html.text, 'html.parser')

    trs = soup.select('#problemset > tbody > tr')
    pid_list = list()
    a_list = list()
    link_list = {}

    if os.path.isfile(file_path):
        with open(file_path, 'r', encoding='UTF-8') as readfile:
            link_list = json.load(readfile)
    else:
        link_list['problem'] = []

    for tr in trs:
        pid_list.append(tr.select_one('td:nth-child(1)'))
        a_list.append(tr.select_one('td:nth-child(2)').find('a'))

    for pi, a in zip(pid_list, a_list):
        problem_id = pi.text
        href = "https://www.acmicpc.net" + a.attrs['href']
        text = a.string
        link_list['problem'].append({"classification": classification, "problem_id": problem_id, "problem_title": text, "url": href})

    print(link_list)

    with open(file_path, 'w', encoding='UTF-8') as outfile:
        json.dump(link_list, outfile, indent=4, ensure_ascii=False)


def get_problem_information_step_1():
    file_path = "./json/url_of_problem_per_algorithm.json"

    with open(file_path, 'r', encoding='UTF-8') as readfile:
        problem_list_data = json.load(readfile)
        # print(problem_list_data)

    for a in problem_list_data['problem']:
        get_problem_information_step_2(a['classification'], a['problem_id'], a['url'])
        time.sleep(1)


def get_problem_information_step_2(classification, problem_id, url_of_problem):
    file_path = "./json/problem_information.json"
    html = requests.get(url_of_problem)
    soup = BeautifulSoup(html.text, 'html.parser')
    # soup = BeautifulSoup(html, 'html.parser')

    problem_information = {}

    if os.path.isfile(file_path):
        with open(file_path, 'r', encoding='UTF-8') as readfile:
            problem_information = json.load(readfile)
    else:
        problem_information['problem_information'] = []

    title = soup.select_one('#problem_title')
    if title is not None:
        title = title.text
    content = soup.select_one('#problem_description > p')
    if content is not None:
        content = content.text
    input_value = soup.select_one('#problem_input > p')
    if input_value is not None:
        input_value = input_value.text
    output_value = soup.select_one('#problem_output > p')
    if output_value is not None:
        output_value = output_value.text
    level = solvedacAPI.get_problem_level_from_solvedac(problem_id)

    problem_information['problem_information'].append({
        "classification": classification,
        "problem_id": problem_id,
        "title": title,
        "content": content,
        "input": input_value,
        "output": output_value,
        "uri": url_of_problem,
        "level": level
    })

    print(classification)
    print(title)
    # print(problem_information)

    with open(file_path, 'w', encoding='UTF-8') as outfile:
        json.dump(problem_information, outfile, indent=4, ensure_ascii=False)


# 알고리즘 별 문제 모아놓은 페이지 url 크롤링
# get_url_of_algorithm()

# 알고리즘 별 문제 모아놓은 페이지에서 문제 url 크롤링
get_problem_url_per_algorithm_step_1()

# 각 문제 페이지에서 문제 정보 크롤링
get_problem_information_step_1()
