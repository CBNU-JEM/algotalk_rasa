import json
import db

with open('../baekjoon_crawling/json/url_of_problem_per_algorithm.json') as json_file:
    json_data = json.load(json_file)
    algorithm_problem_list = set()

    for problem in json_data['problem']:
        algorithm_name = problem['classification']
        algorithm_id = db.execute_query(f'SELECT ID FROM ALGORITHM WHERE NAME = "{algorithm_name}"')
        db.create_algorithm_problem_classification([db.AlgorithmProblemClassification(None, algorithm_id[0][0], problem['problem_id'])])