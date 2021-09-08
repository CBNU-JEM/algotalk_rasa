import json
import db

f = open("algorithm_name.txt", 'r')
algorithm_list = []
lines = f.readlines()
for algorithm in lines:
    algorithm = algorithm.replace('\n', '')
    algorithm_list.append(db.Algorithm(None, algorithm))
db.create_algorithm(list(set(algorithm_list)))
f.close()

with open('algorithm_name.json', encoding='UTF8') as json_file:
    json_data = json.load(json_file)
    algorithm_list = []
    for algorithm in json_data['algorithm']:
        algorithm_name = algorithm['name']
        q = f'SELECT ID FROM ALGORITHM WHERE NAME = "{algorithm_name}"'
        rows = db.execute_query(q)

        algorithm_id = None
        if rows:
            algorithm_id = rows[0][0]

        parent_name = algorithm['parent']
        q = f'SELECT ID FROM ALGORITHM WHERE NAME = "{parent_name}"'
        rows = db.execute_query(q)
        algorithm_parent = None
        if rows:
            algorithm_parent = rows[0][0]

        db.update_algorithm(db.Algorithm(algorithm_id, algorithm['name'], algorithm['brief_explain'], algorithm['detail_explain'],
                                         algorithm['level'], algorithm_parent))