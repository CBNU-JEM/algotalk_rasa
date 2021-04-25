import pymysql

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


def create_algorithm(part_list):
    q = 'insert into algorithm values '
    for part in part_list:
        q += f', (\'{part}\')'
    q = q.replace(', ', '', 1)
    execute_query(q)


def delete_algorithm(part):
    q = f'delete from algorithm where part=\'{part}\''
    execute_query(q)

def get_algorithm_by_name(name):
    q = f'select * from algorithm where name like \'%{name}%\''
    rows = execute_query(q)
    algorithms = []
    for row in rows:
        algorithms.append(Algorithm(row[1], row[2], row[3], row[4], row[5]))
    return algorithms

def create_problem(part_list):
    q = 'insert into problem values '
    for part in part_list:
        q += f', (\'{part}\')'
    q = q.replace(', ', '', 1)
    execute_query(q)


def delete_problem(part):
    q = f'delete from problem where part=\'{part}\''
    execute_query(q)


def create_contest(part_list):
    q = 'insert into contest values '
    for part in part_list:
        q += f', (\'{part}\')'
    q = q.replace(', ', '', 1)
    execute_query(q)


def delete_contest(part):
    q = f'delete from contest where part=\'{part}\''
    execute_query(q)


def create_algorithm_classification(problem_id, algorithm_id):
    q = f'insert into algorithm_classification values problem_id={problem_id},algorithm_id{algorithm_id}'
    execute_query(q)


def delete_algorithm_classification(problem_id, algorithm_id):
    q = f'delete from algorithm_classification where problem_id=\'{problem_id}\' and algorithm_id=\'{algorithm_id}\''
    execute_query(q)


def create_contest_problem(problem_id, contest_id):
    q = f'insert into contest_problem values problem_id={problem_id},contest_id{contest_id}'
    execute_query(q)


def delete_contest_problem(problem_id, contest_id):
    q = f'delete from contest_problem where problem_id=\'{problem_id}\' and contest_id=\'{contest_id}\''
    execute_query(q)


def update_algorithm(name, brief_explain, detail_explain, level, example_code, uri):
    q = f'update algorithm set name={name}, brief_explain={brief_explain},detail_explain={detail_explain},' \
        f'level={level},example_code={example_code},uri={uri}'
    q = q.replace('None', 'NULL').replace('\'None\'', 'NULL')
    execute_query(q)


def update_problem(name, level, content, input, output, source, algorithm_classification, uri):
    q = f'update problem set name={name}, level={level},content={content},input={input}' \
        f',output={output},source={source},algorithm_classification={algorithm_classification}.uri={uri}'
    q = q.replace('None', 'NULL').replace('\'None\'', 'NULL')
    execute_query(q)


def update_contest(name, date, reception_period, content, source, uri):
    q = f'update contest set name={name}, date={date},reception_period={reception_period},content={content}' \
        f',source={source},uri={uri}'
    q = q.replace('None', 'NULL').replace('\'None\'', 'NULL')
    execute_query(q)


if __name__ == "__main__":
    while True:
        q = get_query()
        if q == '':
            break
        execute_query(q)
