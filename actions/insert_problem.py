import json
import db

with open('problem.json') as json_file:
    json_data = json.load(json_file)
    problem_list = []


    for problem in json_data['problem']:
        problem_list.append(db.Problem(problem['title'], None, problem['content'], problem['input'], problem['output'], problem['uri']))

    db.create_problem(list(set(problem_list)))
