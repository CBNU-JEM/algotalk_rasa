import db

algorithm_list = [db.Algorithm('정렬 알고리즘', '자료를 특정 목적에 맞는 순서로 재배열 하는 것',
                               '정렬 알고리즘은 수많은 자료를 특정 목적에 맞게 순서있게 재배치하는 것으로 삽입/선택/버블/병합/큇/버블/힙 정렬 등이 있습니다.',
                               '하', '_'),
                  db.Algorithm('최단거리 알고리즘', '네트워크에서 최단 경로를 찾는 알고리즘',
                               '최단거리 알고리즘은 네트워크에서 하나의 시작 정점으로부터 모든 다른 정점까지의 최단 경로를 찾는 알고리즘이야.',
                               '중', '_')]

problem_list = [db.Problem('수 정렬하기', '브론즈 1', 'N개의 수가 주어졌을 때, 이를 오름차순으로 정렬하는 프로그램을 작성하시오.',
                           '첫째 줄에 수의 개수 N(1 ≤ N ≤ 1,000)이 주어진다. 둘째 줄부터 N개의 줄에는 숫자가 주어진다. ' +
                           '이 수는 절댓값이 1,000보다 작거나 같은 정수이다. 수는 중복되지 않는다.',
                           '첫째 줄부터 N개의 줄에 오름차순으로 정렬한 결과를 한 줄에 하나씩 출력한다.',
                           '_',
                           'https://www.acmicpc.net/problem/2750'),
                db.Problem('쉬운 최단거리', '골드 5', '''지도가 주어지면 모든 지점에 대해서 목표지점까지의 거리를 구하여라. 
                문제를 쉽게 만들기 위해 오직 가로와 세로로만 움직일 수 있다고 하자.''',
                           '지도의 크기 n과 m이 주어진다. n은 세로의 크기, m은 가로의 크기다.(2 ≤ n ≤ 1000, 2 ≤ m ≤ 1000) ' +
                           '다음 n개의 줄에 m개의 숫자가 주어진다. 0은 갈 수 없는 땅이고 1은 갈 수 있는 땅, 2는 목표지점이다. 입력에서 2는 단 한개이다.',
                           '각 지점에서 목표지점까지의 거리를 출력한다. 원래 벽인 위치는 0을 출력하고, 원래 땅인 부분 중에서 도달할 수 없는 위치는 -1을 출력한다.',
                           '_',
                           'https://www.acmicpc.net/problem/14940')]

contest_list = [db.Contest('준파고를 잡아라', '2021.06.07', '2021.05.10 ~ 21',
                           '준파고보다 빨리 코팅해라! 준파고의 코딩을 따라잡는 스피드 코딩 대회!',
                           '프로그래머스', 'https://programmers.co.kr/competitions')]

# INSERT INTO Films (Title) VALUES ('Title2');
# SET @film_id = LAST_INSERT_ID();
# -- if you get ids of genre from your UI just use them
# INSERT INTO Films_Genres (film_id, genre_id)
# SELECT @film_id, id
# FROM Genres
# WHERE id IN (2, 3, 4);
#
# INSERT INTO Films (Title) VALUES ('Title3');
# SET @film_id = LAST_INSERT_ID();
# -- if you names of genres you can use them too
# INSERT INTO Films_Genres (film_id, genre_id)
# SELECT @film_id, id
# FROM Genres
# WHERE Name IN ('Genre2', 'Genre4');
#
# public JsonResult FoodMenu(FoodMenuViewModel vm)
# {
# if (ModelState.IsValid)
# {
#     ManyDbContext ctx = new ManyDbContext();
# foreach (var item in vm.MenuIds)
# {
#     ctx.FoodMenu.Add(new FoodMenu{
#     FoodID = vm.fooId, //this is the food ID from your foodMenuViewModel
# MenuID = item
# });
# ctx.SaveChanges();
# }
# return Json(new { Result = true, Mesaj = "" });
# }
# else
# {
# return Json(new { Result = false, Mesaj = "" });
# }
# }

db.execute_query('drop table ALGORITHMCLASSIFICATION')
db.execute_query('drop table CONTESTPROBLEM')
db.execute_query('drop table PROBLEM')
db.execute_query('drop table ALGORITHM')
db.execute_query('drop table CONTEST')
print("algodb create")
db.execute_query('''CREATE TABLE ALGORITHM (
                    ALGORITHM_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                    NAME VARCHAR(20) NOT NULL,
                    BRIEF_EXPLAIN VARCHAR(50),
                    DETAIL_EXPLAIN VARCHAR(100),
                    EXAMPLE_CODE VARCHAR(200),
                    LEVEL VARCHAR(20),
                    PARENT INT,
                    CONSTRAINT PARENT_ALGORITHM FOREIGN KEY (PARENT) REFERENCES ALGORITHM (ALGORITHM_ID)
                    )ENGINE=InnoDB DEFAULT CHARSET=utf8
                    ''')
db.execute_query('''CREATE TABLE PROBLEM (
                    PROBLEM_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                    NAME VARCHAR(20),
                    LEVEL VARCHAR(20),
                    CONTENT VARCHAR(50),
                    INPUT VARCHAR(100),
                    OUTPUT VARCHAR(100),
                    SOURCE VARCHAR(200),
                    URI VARCHAR(200)
                    )ENGINE=InnoDB DEFAULT CHARSET=utf8
                    ''')
db.execute_query('''CREATE TABLE CONTEST (
                    CONTEST_ID int not null primary key,
                    NAME VARCHAR(20),
                    DATE varchar(20),
                    RECEPTION_PERIOD varchar(30),
                    CONTENT varchar(500),
                    SOURCE varchar(200),
                    URI varchar(200)
                    )''')
db.execute_query('''CREATE TABLE ALGORITHM_CLASSIFICATION (
                    ALGORITHM_ID int not null,
                    PROBLEM_ID int not null,
                    PRIMARY KEY (ALGORITHM_ID, PROBLEM_ID),
                    CONSTRAINT AC_ALGORITHM_FOREIGN FOREIGN KEY (ALGORITHM_ID) 
                    REFERENCES ALGORITHM (ALGORITHM_ID)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE,
                    CONSTRAINT AC_PROBLEM_FOREIGN FOREIGN KEY (PROBLEM_ID) 
                    REFERENCES PROBLEM (PROBLEM_ID)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE
                    )''')
db.execute_query('''CREATE TABLE CONTEST_PROBLEM (
                    CONTEST_ID int not null,
                    PROBLEM_ID int not null,
                    PRIMARY KEY (CONTEST_ID, PROBLEM_ID),
                    CONSTRAINT CP_CONTEST_FOREIGN FOREIGN KEY (CONTEST_ID) 
                    REFERENCES CONTEST (CONTEST_ID)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE,
                    CONSTRAINT CP_PROBLEM_FOREIGN FOREIGN KEY (PROBLEM_ID) 
                    REFERENCES PROBLEM (PROBLEM_ID)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE
                    )''')

db.create_algorithm(algorithm_list)
db.create_problem(problem_list)
db.create_contest(contest_list)

# CONSTRAINT `B_M_ID`
# FOREIGN KEY (`M_ID`)
# REFERENCES `my_movie`.`MOVIE` (`M_ID`)
# ON DELETE CASCADE
# ON UPDATE CASCADE,
# CONSTRAINT `B_G_ID`
# FOREIGN KEY (`G_ID`)
# REFERENCES `my_movie`.`GENRE` (`G_ID`)
# ON DELETE CASCADE
# ON UPDATE CASCADE
