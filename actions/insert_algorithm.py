import db

f = open("algorithm_name.txt", 'r')
algorithm_list = []
lines = f.readlines()
for algorithm in lines:
    algorithm = algorithm.replace('\n', '')
    algorithm_list.append(db.Algorithm(algorithm))
db.create_algorithm(list(set(algorithm_list)))
f.close()
