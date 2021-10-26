# -*- coding: utf-8 -*-
import re

import requests
from bs4 import BeautifulSoup

import json


def get_information_of_contest():
    file_path = "programmers_crawling/json/url_of_contest.json"

    html = requests.get('https://programmers.co.kr/competitions')
    soup = BeautifulSoup(html.text, 'html.parser')

    links = get_url_of_contest()
    contest = {'contest': []}
    idx = 0
    for name, link in links.items():
        current_url = link
        response = requests.get(current_url)
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            a_list = list()
            contest_information = soup.select_one('body > div.main > div.container-competition')
            # print(contest_information)
            # date_information = contest_information.select(
            #     'div:nth-child(2) > div > div:nth-child(2) > div')
            year_match = re.findall(r'\d{2}[년]\s', str(contest_information))
            date_match = re.findall(r'\d{2}[월]\s\d{2}[일]\s\d{2}:\d{2}', str(contest_information))
            date_match_second = re.findall(r'\d{2}', str(date_match))
            date_iter = iter(date_match_second)
            print("idx: " + str(idx))
            idx += 1
            print(name)
            if len(date_match) != 4:
                continue
            print(date_match)
            contest_date = []
            for i in range(2):
                for j in range(2):
                    datetime = '20' + year_match[i][0:2] + '-' + next(date_iter) + '-' + next(date_iter) + ' ' + next(
                        date_iter) + ':' + next(date_iter) + ':00'

                    contest_date.append(datetime)
            # content_information = contest_information.select(
            #     'div:nth-last-child(1) > div.competition-body > div:nth-last-child(1) > div > div > div')
            # content = content_information
            contest['contest'].append(
                {"name": name, "contest_start": contest_date[2], "contest_end": contest_date[3],
                 "reception_start": contest_date[0],
                 "reception_end": contest_date[1], "source": link, "uri": link})
        # time.sleep(1)
    else:
        print("step2")
        print(response.status_code)
    print(contest)
    with open(file_path, 'w', encoding='UTF-8') as outfile:
        json.dump(contest, outfile, indent=4, ensure_ascii=False)


# self.name = name o
# self.contest_start = contest_start
# self.contest_end = contest_end
# self.reception_start = reception_start
# self.reception_end = reception_end
# self.source = source 접수
# self.uri = uri 홈페이지 주소 o


def get_url_of_contest():
    file_path = "programmers_crawling/json/url_of_contest.json"
    # html = requests.get('https://programmers.co.kr/competitions')
    # soup = BeautifulSoup(html.text, 'html.parser')
    url = 'https://programmers.co.kr/competitions'
    current_url = url
    flag = True
    link_list = {}
    while flag:
        response = requests.get(current_url)
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            a_list = list()
            contests_proceed = soup.select('body > div.main > div.container > div.tab-content > div > div')
            for contests in contests_proceed:
                contest = contests.select('ul.list-competitions > li > div > div:nth-child(2) > h4')
                for contest_information in contest:
                    a_list.append(contest_information.find('a'))

            for a in a_list:
                href = "https://programmers.co.kr" + a.attrs['href']
                text = a.string
                text=text.strip()
                link_list[text] = href

            ##페이지 별로
            pages = soup.select(
                'body > div.main > div.container > div.tab-content > div > div.ended-competition > ul > div > nav > '
                'ul > li:nth-last-child(1)')
            page_list = list()
            for page in pages:
                href = page.find('a')['href']
                if href != "#":
                    current_url = "https://programmers.co.kr" + href
                else:
                    flag = False


        else:
            print(response.status_code)

    return link_list

import db

# 크롤링한 대회 데이터 디비에 삽입
def insert_contest_data():
    with open('programmers_crawling/json/url_of_contest.json') as json_file:
        json_data = json.load(json_file)
    contest_list = []

    for contest in json_data['contest']:
        if db.find_contest_by_name(contest['name']):
            continue
        contest_list.append(db.Contest(None, contest['name'], contest['contest_start'], contest['contest_end'],
                                       contest['reception_start'], contest['reception_end'], contest['uri']))

    if contest_list:
        db.create_contest(list(set(contest_list)))

get_information_of_contest()
insert_contest_data()