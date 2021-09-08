import json
import db

with open('../baekjoon_crawling/json/problem_information.json') as json_file:
    json_data = json.load(json_file)
    problem_list = []


    for problem in json_data['problem']:
        problem_list.append(db.Problem(None, problem['problem_id'],problem['title'], problem['level'], problem['uri']))

    db.create_problem(list(set(problem_list)))
    #db.update_problem_list((list(set(problem_list))))
