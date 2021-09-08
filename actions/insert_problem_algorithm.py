import json
import db

with open('problem_algorithm.json') as json_file:
    json_data = json.load(json_file)
    algorithm_problem_list = set()

    for problem in json_data['problem']:
        db.create_algorithm_problem_classification([db.AlgorithmProblemClassification(None, problem['classification'], problem['problem_title'])])