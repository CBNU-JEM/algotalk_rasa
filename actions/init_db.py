import db

print("algodb drop")

db.execute_query('drop table ALGORITHM_PROBLEM_CLASSIFICATION')
db.execute_query('drop table CONTEST_PROBLEM')
db.execute_query('drop table PROBLEM')
db.execute_query('drop table ALGORITHM')
db.execute_query('drop table CONTEST')

print("algodb create")

db.execute_query('''CREATE TABLE ALGORITHM (
                    ID INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
                    NAME VARCHAR(100) NOT NULL,
                    BRIEF_EXPLAIN VARCHAR(255),
                    DETAIL_EXPLAIN VARCHAR(1000),
                    LEVEL VARCHAR(20),
                    PARENT VARCHAR(100),
                    NORMALIZED_NAME VARCHAR(100),
                    CONSTRAINT PARENT_ALGORITHM FOREIGN KEY (PARENT) REFERENCES ALGORITHM (NAME)
                    )ENGINE=InnoDB DEFAULT CHARSET=utf8
                    ''')
db.execute_query('''CREATE TABLE PROBLEM (
                    ID INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
                    PROBLEM_ID INT (11) ,
                    TYPE TINYINT(1) default 0,
                    NAME VARCHAR(100) NOT NULL,
                    LEVEL VARCHAR(20),
                    URI VARCHAR(256),
                    NORMALIZED_NAME VARCHAR(100)
                    )ENGINE=InnoDB DEFAULT CHARSET=utf8
                    ''')
db.execute_query('''CREATE TABLE CONTEST (
                    ID INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
                    NAME VARCHAR(100) NOT NULL,
                    CONTEST_START DATETIME,
                    CONTEST_END DATETIME,
                    RECEPTION_START DATETIME,
                    RECEPTION_END DATETIME,
                    URI VARCHAR(256),
                    NORMALIZED_NAME VARCHAR(100)
                    )ENGINE=InnoDB DEFAULT CHARSET=utf8
                    ''')
db.execute_query('''CREATE TABLE ALGORITHM_PROBLEM_CLASSIFICATION (
                    ID INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
                    ALGORITHM_ID VARCHAR(100) not null,
                    PROBLEM_ID VARCHAR(100) not null,
                    FOREIGN KEY (ALGORITHM_ID) 
                    REFERENCES ALGORITHM (ID)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE,
                    FOREIGN KEY (PROBLEM_ID) 
                    REFERENCES PROBLEM (ID)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE
                    )ENGINE=InnoDB DEFAULT CHARSET=utf8
                    ''')
db.execute_query('''CREATE TABLE CONTEST_PROBLEM (
                    ID INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
                    CONTEST_ID VARCHAR(100) not null,
                    PROBLEM_ID VARCHAR(100) not null,
                    CONSTRAINT CP_CONTEST_FOREIGN FOREIGN KEY (CONTEST_ID) 
                    REFERENCES CONTEST (ID)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE,
                    CONSTRAINT CP_PROBLEM_FOREIGN FOREIGN KEY (PROBLEM_ID) 
                    REFERENCES PROBLEM (ID)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE
                    )ENGINE=InnoDB DEFAULT CHARSET=utf8
                    ''')
