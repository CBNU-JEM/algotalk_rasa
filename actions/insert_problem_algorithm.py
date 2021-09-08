import json
import db

with open('../baekjoon_crawling/json/url_of_problem_per_algorithm.json') as json_file:
    json_data = json.load(json_file)
    algorithm_problem_list = set()

    for problem in json_data['problem']:
        algorithm_name = problem['classification']
        rows = db.execute_query(f'SELECT ID FROM ALGORITHM WHERE NAME = "{algorithm_name}"')

        problem_id = problem['problem_id']
        rows2 = db.execute_query(f'SELECT ID FROM ALGORITHM WHERE NAME = "{problem_id}"')

        if rows and rows2:
            db.create_algorithm_problem_classification([db.AlgorithmProblemClassification(None, rows[0][0], rows2[0][0])])