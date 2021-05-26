import json
import db

def fix_json(string_):
    if string_[0] == string_[-1] == "'":
        return '"' + string_[1:-1] +'"'
    return string_

with open('problem.json') as json_file:
    json_data = json.load(json_file)
    problem_list = []


    for problem in json_data['problem']:
        problem_list.append(db.Problem(problem['title'], None, problem['content'], problem['input'], problem['output'], problem['uri']))

    db.create_problem(list(set(problem_list)))
