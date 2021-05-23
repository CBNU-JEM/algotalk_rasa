import pymysql
from func import UserLevel
debug = True

db = pymysql.connect(host='localhost', user='algotalk', password='algojem', db='algotalk_db', autocommit=True,
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


class AlgorithmClassification:
    def __init__(self, problem_id=None, algorithm_id=None):
        self.problem_id = problem_id
        self.algorithm_id = algorithm_id


class Problem:
    def __init__(self, name=None, level=None, content=None, input=None, output=None,
                 source=None, uri=None):
        self.name = name
        self.level = level
        self.content = content
        self.input = input
        self.output = output
        self.source = source
        self.uri = uri


class ContestProblem:
    def __init__(self, problem_id=None, contest_id=None):
        self.problem_id = problem_id
        self.contest_id = contest_id


class Contest:
    def __init__(self, name=None, date=None, reception_period=None, content=None, source=None, uri=None):
        self.name = name
        self.date = date
        self.reception_period = reception_period
        self.content = content
        self.source = source
        self.uri = uri


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
    q = 'INSERT INTO  ALGORITHM (NAME, BRIEF_EXPLAIN, DETAIL_EXPLAIN, LEVEL, EXAMPLE_CODE, PARENT) VALUES '
    tmp_query = ""
    for algorithm in algorithm_list:
        tmp_query += f', (\'{algorithm.name}\', \'{algorithm.brief_explain}\', \'{algorithm.detail_explain}\', \'{algorithm.level}\', \'{algorithm.example_code}\', {algorithm.parent})'
    q += tmp_query.replace(', ', '', 1).replace('None', 'NULL').replace('\'None\'', 'NULL')
    execute_query(q)


def delete_algorithm(part):
    q = f'DELETE FROM ALGORITHM WHERE part=\'{part}\''
    execute_query(q)


def get_algorithm_by_name(name):
    q = f'SELECT * FROM ALGORITHM WHERE NAME LIKE \'%{name}%\''
    rows = execute_query(q)
    algorithms = []
    for row in rows:
        algorithms.append(Algorithm(row[1], row[2], row[3], row[4], row[5]))
    return algorithms


def create_problem(problem_list):
    q = 'INSERT INTO PROBLEM (NAME, LEVEL, CONTENT, INPUT, OUTPUT, SOURCE, URI) VALUES '
    tmp_query = ""
    for problem in problem_list:
        tmp_query += f', (\'{problem.name}\', \'{problem.level}\', \'{problem.content}\', \'{problem.input}\', \'{problem.output}\', \'{problem.source}\', \'{problem.uri}\')'
    q += tmp_query.replace(', ', '', 1).replace('None', 'NULL').replace('\'None\'', 'NULL')
    execute_query(q)


def delete_problem(part):
    q = f'DELETE FROM PROBLEM WHERE part=\'{part}\''
    execute_query(q)


def get_problem(problem_name, algorithm_name, level, contest_name, number):
    q = f'SELECT P.NAME, P.LEVEL, P.CONTENT, P.INPUT, P.OUTPUT, P.SOURCE, P.URI, C.NAME, A.NAME FROM PROBLEM AS P '\
        'LEFT JOIN CONTEST_PROBLEM AS CP ON P.NAME =CP.NAME LEFT JOIN CONTEST AS C ON CP.NAME = C.NAME '\
        'LEFT JOIN ALGORITHM_CLASSIFICATION AS AP ON P.NAME=AP.NAME LEFT JOIN ALGORITHM AS A ON AP.NAME=A.NAME '

    if problem_name:
        q += "WHERE " + f"P.NAME LIKE \'%{problem_name}%\'"
    if algorithm_name:
        q += "AND " if q.contains("WHERE") else "WHERE " + f"A.NAME LIKE%\'{algorithm_name}\'%"
    if contest_name:
        q += "AND " if q.contains("WHERE") else "WHERE " + f"C.NAME LIKE%\'{contest_name}\'%"
    if level:
        q += "AND " if q.contains("WHERE") else "WHERE " + f"LEVEL LIKE%\'{level}\'%"
    q += f"ORDER BY RAND() LIMIT {number}"
    rows = execute_query(q)
    problems = []
    for row in rows:
        problems.append(Problem(row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
    return problems


def create_contest(contest_list):
    q = 'INSERT INTO CONTEST (NAME, DATE, RECEPTION_PERIOD, CONTENT, SOURCE, URI) VALUES '
    tmp_query = ""
    for contest in contest_list:
        tmp_query += f', (\'{contest.name}\', \'{contest.date}\', \'{contest.reception_period}\', \'{contest.content}\', \'{contest.source}\', \'{contest.uri}\')'
    q += tmp_query.replace(', ', '', 1).replace('None', 'NULL').replace('\'None\'', 'NULL')
    execute_query(q)


def delete_contest(part):
    q = f'DELETE FROM CONTEST WHERE part=\'{part}\''
    execute_query(q)


def create_algorithm_classification(problem_id, algorithm_id):
    q = f'INSERT INTO ALGORITHM_CLASSIFICATION VALUES problem_id={problem_id},algorithm_id{algorithm_id}'
    execute_query(q)


def delete_algorithm_classification(problem_id, algorithm_id):
    q = f'DELETE FROM ALGORITHM_CLASSIFICATION WHERE problem_id=\'{problem_id}\' AND algorithm_id=\'{algorithm_id}\''
    execute_query(q)


def create_contest_problem(problem_id, contest_id):
    q = f'INSERT INTO CONTEST_PROBLEM VALUES problem_id={problem_id},contest_id{contest_id}'
    execute_query(q)


def delete_contest_problem(problem_id, contest_id):
    q = f'DELETE FROM CONTEST_PROBLEM WHERE problem_id=\'{problem_id}\' AND contest_id=\'{contest_id}\''
    execute_query(q)


def update_algorithm(name, brief_explain, detail_explain, level, example_code, uri):
    q = f'UPDATE ALGORITHM SET name={name}, brief_explain={brief_explain},detail_explain={detail_explain},' \
        f'level={level},example_code={example_code},uri={uri}'
    q = q.replace('None', 'NULL').replace('\'None\'', 'NULL')
    execute_query(q)


def update_problem(name, level, content, input, output, source, algorithm_classification, uri):
    q = f'UPDATE PROBLEM SET name={name}, level={level},content={content},input={input}' \
        f',output={output},source={source},algorithm_classification={algorithm_classification}.uri={uri}'
    q = q.replace('None', 'NULL').replace('\'None\'', 'NULL')
    execute_query(q)


def update_contest(name, date, reception_period, content, source, uri):
    q = f'UPDATE CONTEST SET name={name}, date={date},reception_period={reception_period},content={content}' \
        f',source={source},uri={uri}'
    q = q.replace('None', 'NULL').replace('\'None\'', 'NULL')
    execute_query(q)


if __name__ == "__main__":
    while True:
        q = get_query()
        if q == '':
            break
        execute_query(q)
