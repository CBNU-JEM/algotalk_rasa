import re

import pymysql

import logging

# 로그 생성
logger = logging.getLogger()

# 로그의 출력 기준 설정
logger.setLevel(logging.INFO)

# log 출력 형식
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# log 출력
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

debug = True

db = pymysql.connect(host='mysql_service', user='algotalk', password='algojem', db='algotalk_db', autocommit=True,
                     sql_mode='STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION', charset='utf8')
cur = db.cursor()
cur.execute('set @@auto_increment_increment=1')


class Algorithm:
    def __init__(self, id, name=None, brief_explain=None, detail_explain=None, level=None, parent=None):
        self.id = id
        self.name = name
        self.brief_explain = brief_explain
        self.detail_explain = detail_explain
        self.level = level
        self.parent = parent
        self.normalized_name = normalize(name)


class AlgorithmProblemClassification:
    def __init__(self, id, algorithm_id=None, problem_id=None):
        self.id = id
        self.algorithm_id = algorithm_id
        self.problem_id = problem_id


class Problem:
    def __init__(self, id, problem_id=None, name=None, level=None, uri=None, type=0):
        self.id = id
        self.problem_id = problem_id
        self.type = type
        self.name = name
        self.level = level
        self.uri = uri
        self.normalized_name = normalize(name)


class ContestProblem:
    def __init__(self, id, problem_id=None, contest_id=None):
        self.id = id
        self.problem_id = problem_id
        self.contest_id = contest_id


class Contest:
    def __init__(self, id, name=None, contest_start=None, contest_end=None, reception_start=None, reception_end=None,
                 uri=None):
        self.id = id
        self.name = name
        self.contest_start = contest_start
        self.contest_end = contest_end
        self.reception_start = reception_start
        self.reception_end = reception_end
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
    q = "INSERT IGNORE INTO  ALGORITHM (NAME, BRIEF_EXPLAIN, DETAIL_EXPLAIN, LEVEL, PARENT, NORMALIZED_NAME) VALUES "
    tmp_query = ""
    for algorithm in algorithm_list:
        tmp_query += f', ("{algorithm.name}", "{algorithm.brief_explain}", "{algorithm.detail_explain}", ' \
                     f'"{algorithm.level}", "{algorithm.parent}", "{normalize(algorithm.name)}")'
    q += tmp_query.replace(', ', '', 1)
    execute_query(none_to_null(q))


def delete_algorithm(id):
    q = f'DELETE FROM ALGORITHM WHERE id="{id}"'
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
    q = 'INSERT IGNORE INTO PROBLEM (PROBLEM_ID, NAME, LEVEL, URI, NORMALIZED_NAME) VALUES '
    tmp_query = ""
    for problem in problem_list:
        tmp_query += f", ('{problem.problem_id}', '{problem.name}', '{problem.level}', '{problem.uri}', '{normalize(problem.name)}')"
    q += tmp_query.replace(', ', '', 1)
    execute_query(none_to_null(q))


def delete_problem(id):
    q = f'DELETE FROM PROBLEM WHERE ID="{id}"'
    execute_query(q)


def get_problem(problem_name, algorithm_name, level, number):
    q = f'SELECT P.ID, P.PROBLEM_ID, P.NAME, P.LEVEL, P.URI, A.ID FROM PROBLEM AS P ' \
        'LEFT JOIN ALGORITHM_PROBLEM_CLASSIFICATION AS AP ON P.ID=AP.PROBLEM_ID ' \
        'LEFT JOIN ALGORITHM AS A ON AP.ALGORITHM_ID=A.ID '

    normalized_problem_name = normalize(problem_name)

    if problem_name:
        q += "WHERE " + f'P.NORMALIZED_NAME LIKE "{normalized_problem_name}" '

    if get_algorithm_by_normalized_name(algorithm_name):
        db_algorithm_name = get_algorithm_by_normalized_name(algorithm_name)[0].normalized_name
        q += ("OR " if q.find("WHERE") != -1 else "WHERE ") + f'A.NORMALIZED_NAME LIKE "{db_algorithm_name}" '

    if level:
        if level != 0:
            level_end = level + 4
        else:  # 랜덤으로 전체검색
            level_end = 25
        q += ("AND " if q.find("WHERE") != -1 else "WHERE ") + f'P.LEVEL BETWEEN {level} AND {level_end} '

    q += f"ORDER BY RAND() LIMIT {number}"
    rows = execute_query(q)
    problems = []

    logger.info(f"problem_recommand sql : {q}")
    logger.info(f"sql result: {rows}")

    if rows is None:
        return None

    for row in rows:
        problems.append(Problem(row[0], row[1], row[2], row[3], row[4]))
    if problems:
        return problems

    q = f'SELECT P.ID, P.PROBLEM_ID, P.NAME, P.LEVEL, P.URI, A.ID FROM PROBLEM AS P ' \
        'LEFT JOIN ALGORITHM_PROBLEM_CLASSIFICATION AS AP ON P.ID=AP.PROBLEM_ID ' \
        'LEFT JOIN ALGORITHM AS A ON AP.ALGORITHM_ID=A.ID '

    if problem_name:
        q += "WHERE " + f'P.NAME LIKE "%{normalized_problem_name}%" '

    if get_algorithm_by_normalized_name(algorithm_name):
        db_algorithm_name = get_algorithm_by_normalized_name(algorithm_name)[0].normalized_name
        q += ("OR " if q.find("WHERE") != -1 else "WHERE ") + f'A.NORMALIZED_NAME LIKE "{db_algorithm_name}" '

    if level:
        if level != 0:
            level_end = level + 4
        else:  # 랜덤으로 전체검색
            level_end = 25
        q += ("AND " if q.find("WHERE") != -1 else "WHERE ") + f'P.LEVEL BETWEEN {level} AND {level_end} '

    q += f"ORDER BY RAND() LIMIT {number}"
    rows = execute_query(q)
    problems = []
    for row in rows:
        problems.append(Problem(row[0], row[1], row[2], row[3], row[4]))
    return problems


def create_contest(contest_list):
    q = 'INSERT IGNORE INTO CONTEST (NAME, CONTEST_START, CONTEST_END, RECEPTION_START, RECEPTION_END, URI, NORMALIZED_NAME) VALUES '
    tmp_query = ""
    for contest in contest_list:
        tmp_query += f', ("{contest.name}", "{contest.contest_start}", "{contest.contest_end}", "{contest.reception_start}", ' \
                     f'"{contest.reception_end}", "{contest.uri}", "{normalize(contest.name)}")'

    q += tmp_query.replace(', ', '', 1)
    execute_query(none_to_null(q))


def create_algorithm_problem_classification(algorithm_problem_list):
    q = 'INSERT INTO ALGORITHM_PROBLEM_CLASSIFICATION (ALGORITHM_ID, PROBLEM_ID) VALUES '

    tmp_query = ""
    for algorithm_problem in algorithm_problem_list:
        tmp_query += f', ("{algorithm_problem.algorithm_id}", "{algorithm_problem.problem_id}")'

    q += tmp_query.replace(', ', '', 1)
    execute_query(none_to_null(q))


def delete_contest(id):
    q = f'DELETE FROM CONTEST WHERE ID="{id}"'
    execute_query(q)

def get_contests():
    q = f'SELECT * FROM CONTEST'
    rows = execute_query(q)
    contests = []
    for row in rows:
        contests.append(Contest(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))

    if contests:
        return contests

def get_contest_by_normalized_name(name):
    normalized_name = normalize(name)
    q = f'SELECT * FROM CONTEST WHERE NORMALIZED_NAME LIKE "{normalized_name}"'
    rows = execute_query(q)
    contests = []
    for row in rows:
        contests.append(Contest(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))

    if contests:
        return contests

    q = f'SELECT * FROM CONTEST WHERE NORMALIZED_NAME LIKE "%{normalized_name}%"'
    rows = execute_query(q)
    contests = []
    for row in rows:
        contests.append(Contest(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
    return contests


def get_contest_by_sql(sql):
    rows = execute_query(sql)
    contests = []
    for row in rows:
        contests.append(Contest(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
    return contests


def create_algorithm_problem_classification_one(algorithm_id, problem_id):
    q = f'INSERT INTO ALGORITHM_PROBLEM_CLASSIFICATION (algorithm_id, problem_id) VALUES ("{algorithm_id}", "{problem_id}")'
    execute_query(q)


def delete_algorithm_problem_classification(algorithm_id, problem_id):
    q = f'DELETE FROM ALGORITHM_PROBLEM_CLASSIFICATION WHERE problem_id="{problem_id}" AND algorithm_id="{algorithm_id}"'
    execute_query(q)


def create_contest_problem(contest_id, problem_id):
    q = f'INSERT INTO CONTEST_PROBLEM (contest_id, problem_id)VALUES ("{contest_id}", "{problem_id}")'
    execute_query(q)


def delete_contest_problem(contest_id, problem_id):
    q = f'DELETE FROM CONTEST_PROBLEM WHERE problem_id="{problem_id}" AND contest_id="{contest_id}"'
    execute_query(q)


def update_algorithm(algorithm):
    normalized_name = normalize(algorithm.name)
    q = f'UPDATE ALGORITHM SET NAME ="{algorithm.name}", brief_explain="{algorithm.brief_explain}",detail_explain="{algorithm.detail_explain}", ' \
        f'level="{algorithm.level}", parent="{algorithm.parent}", normalized_name="{normalized_name}" WHERE ID ="{algorithm.id}"'
    execute_query(none_to_null(q))


def update_problem_list(problem_list):
    for problem in problem_list:
        update_problem(problem)


def update_problem(problem):
    normalized_name = normalize(problem.name)
    q = f'UPDATE PROBLEM SET NAME="{problem.name}", PROBLEM_ID="{problem.problem_id}", level="{problem.level}", uri="{problem.uri}", ' \
        f'normalized_name="{normalized_name}" WHERE ID="{problem.id}"'
    execute_query(none_to_null(q))


def update_contest(contest):
    normalized_name = normalize(contest.name)
    q = f'UPDATE CONTEST SET NAME ="{contest.name}", CONTEST_START="{contest.contest_start}", CONTEST_END="{contest.contest_end}", ' \
        f'RECEPTION_START="{contest.reception_start}", RECEPTION_END="{contest.reception_end}",' \
        f'URI="{contest.uri}", NORMALIZED_NAME="{normalized_name}" WHERE ID ="{contest.id}"'
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
    q = f'SELECT * FROM ALGORITHM_PROBLEM_CLASSIFICATION WHERE PROBLEM_ID = "{problem.id}"'
    rows = execute_query(q)
    logger.info(f"algorithm_problem_classification : {rows}")
    if not rows:
        return None
    else:
        algorithm_problem_classification = AlgorithmProblemClassification(rows[0][0], rows[0][1], rows[0][2])

    logger.info(f"algorithm_problem_classification is exist")

    if algorithm_problem_classification.algorithm_id:
        q = f'SELECT name FROM ALGORITHM WHERE ID = "{algorithm_problem_classification.algorithm_id}"'
        rows = execute_query(q)
        logger.info(f"problem {algorithm_problem_classification.problem_id} 관련 algorithm {rows}")
        return rows[0][0]
    return None
