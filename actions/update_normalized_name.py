import db

q = f'SELECT * FROM ALGORITHM'
rows = db.execute_query(q)
for row in rows:
    db.update_algorithm(db.Algorithm(row[0], row[1], row[2], row[3], row[4], row[5]))

q = f'SELECT * FROM PROBLEM'
rows = db.execute_query(q)
for row in rows:
    db.update_problem(db.Problem(row[0], row[1], row[2], row[3], row[4]))


q = f'SELECT * FROM CONTEST'
rows = db.execute_query(q)
for row in rows:
    db.update_contest(db.Contest(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
