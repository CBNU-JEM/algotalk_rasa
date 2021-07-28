import random
import re

import pymysql

debug = True

db = pymysql.connect(host='mysql_service', user='algotalk', password='algojem', db='algotalk_db', autocommit=True,
                     sql_mode='STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION', charset='utf8')
cur = db.cursor()
cur.execute('set @@auto_increment_increment=1')


class Algorithm:
    def __init__(self, name=None, brief_explain=None, detail_explain=None, level=None, example_code=None, parent=None):
        self.name = name
        self.brief_explain = brief_explain
        self.detail_explain = detail_explain
        self.level = level
        self.example_code = example_code
        self.parent = parent
        self.normalized_name = normalize(name)


class AlgorithmProblemClassification:
    def __init__(self, algorithm_name=None, problem_name=None):
        self.algorithm_name = algorithm_name
        self.problem_name = problem_name


class Problem:
    def __init__(self, name=None, level=None, content=None, input=None, output=None, uri=None):
        self.name = name
        self.level = level
        self.content = content
        self.input = input
        self.output = output
        self.uri = uri
        self.normalized_name = normalize(name)


class ContestProblem:
    def __init__(self, problem_name=None, contest_name=None):
        self.problem_name = problem_name
        self.contest_name = contest_name


class Contest:
    def __init__(self, name=None, contest_start=None, contest_end=None, reception_start=None, reception_end=None,
                 content=None, source=None, uri=None):
        self.name = name
        self.contest_start = contest_start
        self.contest_end = contest_end
        self.reception_start = reception_start
        self.reception_end = reception_end
        self.content = content
        self.source = source
        self.uri = uri
        self.normalized_name = normalize(name)


def get_query():
    q = ''
    while True:
        print('> ', end='')
        p = input()
        if p == '':
            break
        q += p + '\n'
    return q


def execute_query(q):
    if debug:
        print(f'executing query..\n{q}')
    rows = None
    try:
        db.ping(reconnect=True)
        cur.execute(q)
        rows = cur.fetchall()
        if debug:
            for row in rows:
                print(row)
            print()
    except Exception as e:
        print(f'ERROR({e.args[0]}): {e.args[1]}')
        print()
    return rows


def create_algorithm(algorithm_list):
    q = "INSERT IGNORE INTO  ALGORITHM (NAME, BRIEF_EXPLAIN, DETAIL_EXPLAIN, LEVEL, EXAMPLE_CODE, PARENT, NORMALIZED_NAME) VALUES "
    tmp_query = ""
    for algorithm in algorithm_list:
        tmp_query += f', ("{algorithm.name}", "{algorithm.brief_explain}", "{algorithm.detail_explain}", ' \
                     f'"{algorithm.level}", "{algorithm.example_code}", "{algorithm.parent}", "{normalize(algorithm.name)}")'
    q += tmp_query.replace(', ', '', 1)
    execute_query(none_to_null(q))


def delete_algorithm(name):
    q = f'DELETE FROM ALGORITHM WHERE part="{name}"'
    execute_query(q)


def get_algorithm_by_normalized_name(name):
    normalized_name = normalize(name)
    q = f'SELECT * FROM ALGORITHM WHERE NORMALIZED_NAME LIKE "{normalized_name}"'
    rows = execute_query(q)
    algorithms = []
    for row in rows:
        algorithms.append(Algorithm(row[0], row[1], row[2], row[3], row[4], row[5]))

    if algorithms:
        return algorithms

    q = f'SELECT * FROM ALGORITHM WHERE NORMALIZED_NAME LIKE "%{normalized_name}%"'
    rows = execute_query(q)
    algorithms = []
    for row in rows:
        algorithms.append(Algorithm(row[0], row[1], row[2], row[3], row[4], row[5]))
    return algorithms


def create_problem(problem_list):
    q = 'INSERT IGNORE INTO PROBLEM (NAME, LEVEL, CONTENT, INPUT, OUTPUT, URI, NORMALIZED_NAME) VALUES '
    tmp_query = ""
    for problem in problem_list:
        tmp_query += f', ("{problem.name}", "{problem.level}", "{problem.content}", ' \
                     f'"{problem.input}", "{problem.output}", "{problem.uri}", "{normalize(problem.name)}")'
    q += tmp_query.replace(', ', '', 1)
    execute_query(none_to_null(q))


def delete_problem(name):
    q = f'DELETE FROM PROBLEM WHERE NAME="{name}"'
    execute_query(q)


def get_problem(problem_name, algorithm_name, level, contest_name, number):
    q = f'SELECT P.NAME, P.LEVEL, P.CONTENT, P.INPUT, P.OUTPUT, P.URI, C.NAME, A.NAME FROM PROBLEM AS P ' \
        'LEFT JOIN CONTEST_PROBLEM AS CP ON P.NAME =CP.PROBLEM_NAME LEFT JOIN CONTEST AS C ON CP.CONTEST_NAME = C.NAME ' \
        'LEFT JOIN ALGORITHM_PROBLEM_CLASSIFICATION AS AP ON P.NAME=AP.PROBLEM_NAME ' \
        'LEFT JOIN ALGORITHM AS A ON AP.ALGORITHM_NAME=A.NAME '

    normalized_problem_name = normalize(problem_name)

    if problem_name:
        q += "WHERE " + f'P.NORMALIZED_NAME LIKE "{normalized_problem_name}" '
    if get_algorithm_by_normalized_name(algorithm_name):
        db_algorithm_name = get_algorithm_by_normalized_name(algorithm_name)[0].normalized_name
        q += ("OR " if q.find("WHERE") != -1 else "WHERE ") + f'A.NORMALIZED_NAME LIKE "{db_algorithm_name}" '
    if get_contest_by_normalized_name(contest_name):
        db_contest_name = get_contest_by_normalized_name(contest_name)[0].normalized_name
        q += ("AND " if q.find("WHERE") != -1 else "WHERE ") + f'C.NORMALIZED_NAME LIKE "{db_contest_name}" '
    if level:
        q += ("AND " if q.find("WHERE") != -1 else "WHERE ") + f'P.LEVEL LIKE "%{level}%" '
    q += f"ORDER BY RAND() LIMIT {number}"
    rows = execute_query(q)
    problems = []
    for row in rows:
        problems.append(Problem(row[0], row[1], row[2], row[3], row[4], row[5]))
    if problems:
        return problems

    q = f'SELECT P.NAME, P.LEVEL, P.CONTENT, P.INPUT, P.OUTPUT, P.URI, C.NAME, A.NAME FROM PROBLEM AS P ' \
        'LEFT JOIN CONTEST_PROBLEM AS CP ON P.NAME =CP.PROBLEM_NAME LEFT JOIN CONTEST AS C ON CP.CONTEST_NAME = C.NAME ' \
        'LEFT JOIN ALGORITHM_PROBLEM_CLASSIFICATION AS AP ON P.NAME=AP.PROBLEM_NAME ' \
        'LEFT JOIN ALGORITHM AS A ON AP.ALGORITHM_NAME=A.NAME '

    if problem_name:
        q += "WHERE " + f'P.NAME LIKE "%{normalized_problem_name}%" '
    if get_algorithm_by_normalized_name(algorithm_name):
        db_algorithm_name = get_algorithm_by_normalized_name(algorithm_name)[0].normalized_name
        q += ("OR " if q.find("WHERE") != -1 else "WHERE ") + f'A.NORMALIZED_NAME LIKE "{db_algorithm_name}" '
    if get_contest_by_normalized_name(contest_name):
        db_contest_name = get_contest_by_normalized_name(contest_name)[0].normalized_name
        q += ("AND " if q.find("WHERE") != -1 else "WHERE ") + f'C.NORMALIZED_NAME LIKE "{db_contest_name}" '
    if level:
        q += ("AND " if q.find("WHERE") != -1 else "WHERE ") + f'P.LEVEL LIKE "%{level}%" '
    q += f"ORDER BY RAND() LIMIT {number}"
    rows = execute_query(q)
    problems = []
    for row in rows:
        problems.append(Problem(row[0], row[1], row[2], row[3], row[4], row[5]))
    return problems


def create_contest(contest_list):
    q = 'INSERT INTO CONTEST (NAME, CONTEST_START, CONTEST_END, RECEPTION_START, RECEPTION_END, ' \
        'CONTENT, SOURCE, URI, NORMALIZED_NAME) VALUES '
    tmp_query = ""
    for contest in contest_list:
        tmp_query += f', ("{contest.name}", "{contest.contest_start}", "{contest.contest_end}", ' \
                     f'"{contest.reception_start}", "{contest.reception_end}", "{contest.content}", ' \
                     f'"{contest.source}", "{contest.uri}", "{normalize(contest.name)}")'
    q += tmp_query.replace(', ', '', 1)
    execute_query(none_to_null(q))


def create_algorithm_problem_classification(algorithm_problem_list):
    q = 'INSERT INTO ALGORITHM_PROBLEM_CLASSIFICATION (ALGORITHM_NAME, PROBLEM_NAME) VALUES '

    tmp_query = ""
    for algorithm_problem in algorithm_problem_list:
        tmp_query += f', ("{algorithm_problem.algorithm_name}", "{algorithm_problem.problem_name}")'
    q += tmp_query.replace(', ', '', 1)
    execute_query(none_to_null(q))


def delete_contest(name):
    q = f'DELETE FROM CONTEST WHERE NAME="{name}"'
    execute_query(q)


def get_contest_by_normalized_name(name):
    normalized_name = normalize(name)
    q = f'SELECT * FROM CONTEST WHERE NORMALIZED_NAME LIKE "{normalized_name}"'
    rows = execute_query(q)
    contests = []
    for row in rows:
        contests.append(Contest(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
    if contests:
        return contests

    q = f'SELECT * FROM CONTEST WHERE NORMALIZED_NAME LIKE "%{normalized_name}%"'
    rows = execute_query(q)
    contests = []
    for row in rows:
        contests.append(Contest(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
    return contests


def get_contest_by_sql(sql):
    rows = execute_query(sql)
    contests = []
    for row in rows:
        contests.append(Contest(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
    return contests


def create_algorithm_problem_classification_one(algorithm_name, problem_name):
    q = f'INSERT INTO ALGORITHM_PROBLEM_CLASSIFICATION (algorithm_name, problem_name) VALUES ("{algorithm_name}", "{problem_name}")'
    execute_query(q)


def delete_algorithm_problem_classification(algorithm_name, problem_name):
    q = f'DELETE FROM ALGORITHM_PROBLEM_CLASSIFICATION WHERE problem_name="{problem_name}" AND algorithm_name="{algorithm_name}"'
    execute_query(q)


def create_contest_problem(contest_name, problem_name):
    q = f'INSERT INTO CONTEST_PROBLEM (contest_name, problem_name)VALUES ("{contest_name}", "{problem_name}")'
    execute_query(q)


def delete_contest_problem(contest_name, problem_name):
    q = f'DELETE FROM CONTEST_PROBLEM WHERE problem_name="{problem_name}" AND contest_name="{contest_name}"'
    execute_query(q)


def update_algorithm(algorithm):
    normalized_name = normalize(algorithm.name)
    q = f'UPDATE ALGORITHM SET brief_explain="{algorithm.brief_explain}",detail_explain="{algorithm.detail_explain}", ' \
        f'level="{algorithm.level}", example_code="{algorithm.example_code}", parent="{algorithm.parent}", ' \
        f'normalized_name="{normalized_name}" WHERE NAME ="{algorithm.name}"'
    execute_query(none_to_null(q))


def update_problem_list(problem_list):
    for problem in problem_list:
        update_problem(problem)


def update_problem(problem):
    normalized_name = normalize(problem.name)
    q = f'UPDATE PROBLEM SET level="{problem.level}", content="{problem.content}", ' \
        f'input="{problem.input}", output="{problem.output}", uri="{problem.uri}", normalized_name="{normalized_name}" ' \
        f'WHERE NAME="{problem.name}"'
    execute_query(none_to_null(q))


def update_contest(contest):
    normalized_name = normalize(contest.name)
    q = f'UPDATE CONTEST SET name="{contest.name}", CONTEST_START="{contest.contest_start}", CONTEST_END="{contest.contest_end}", ' \
        f'RECEPTION_START="{contest.reception_start}", RECEPTION_END="{contest.reception_end}", CONTENT="{contest.content}", ' \
        f'SOURCE="{contest.source}", URI="{contest.uri}", NORMALIZED_NAME="{normalized_name}" WHERE NAME ="{contest.name}"'
    execute_query(none_to_null(q))


def normalize(name):
    if not name:
        return None
    return re.sub("[-/: –\\s]", "", name)


def none_to_null(q):
    return q.replace('None', 'NULL').replace('\'None\'', 'NULL').replace('\"None\"', 'NULL').replace('\"NULL\"', 'NULL')


if __name__ == "__main__":
    while True:
        q = get_query()
        if q == '':
            break
        execute_query(q)


def get_algorithm_name_by_problem(problem):
    q = f'SELECT * FROM ALGORITHM_PROBLEM_CLASSIFICATION WHERE PROBLEM_NAME LIKE "{problem.name}" LIMIT 1'
    rows = execute_query(q)

    algorithm_problem_classification = AlgorithmProblemClassification(rows[0][0], rows[0][1])
    if algorithm_problem_classification.algorithm_name:
        return algorithm_problem_classification.algorithm_name
    return None
