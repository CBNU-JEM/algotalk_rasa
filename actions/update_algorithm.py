import json

import db

with open('algorithm_name.json', encoding='UTF8') as json_file:
    json_data = json.load(json_file)
    algorithm_list = []
    for algorithm in json_data['algorithm']:
        db.update_algorithm(db.Algorithm(None, algorithm['name'], algorithm['brief_explain'], algorithm['detail_explain'],
                            algorithm['level'], algorithm['parent']))
