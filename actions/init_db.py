import db

algorithm_list = [db.Algorithm('정렬 알고리즘', '자료를 특정 목적에 맞는 순서로 재배열 하는 것',
                               '정렬 알고리즘은 수많은 자료를 특정 목적에 맞게 순서있게 재배치하는 것으로 삽입/선택/버블/병합/큇/버블/힙 정렬 등이 있습니다.',
                               '하',
                               '''
# include <stdio.h>
# define MAX_SIZE 9
# define SWAP(x, y, temp) ( (temp)=(x), (x)=(y), (y)=(temp) )

// 1. 피벗을 기준으로 2개의 부분 리스트로 나눈다.
// 2. 피벗보다 작은 값은 모두 왼쪽 부분 리스트로, 큰 값은 오른쪽 부분 리스트로 옮긴다.
/* 2개의 비균등 배열 list[left...pivot-1]와 list[pivot+1...right]의 합병 과정 */
/* (실제로 숫자들이 정렬되는 과정) */
int partition(int list[], int left, int right){
  int pivot, temp;
  int low, high;

  low = left;
  high = right + 1;
  pivot = list[left]; // 정렬할 리스트의 가장 왼쪽 데이터를 피벗으로 선택(임의의 값을 피벗으로 선택)

  /* low와 high가 교차할 때까지 반복(low<high) */
  do{
    /* list[low]가 피벗보다 작으면 계속 low를 증가 */
    do {
      low++; // low는 left+1 에서 시작
    } while (low<=right && list[low]<pivot);

    /* list[high]가 피벗보다 크면 계속 high를 감소 */
    do {
      high--; //high는 right 에서 시작
    } while (high>=left && list[high]>pivot);

    // 만약 low와 high가 교차하지 않았으면 list[low]를 list[high] 교환
    if(low<high){
      SWAP(list[low], list[high], temp);
    }
  } while (low<high);

  // low와 high가 교차했으면 반복문을 빠져나와 list[left]와 list[high]를 교환
  SWAP(list[left], list[high], temp);

  // 피벗의 위치인 high를 반환
  return high;
}

// 퀵 정렬
void quick_sort(int list[], int left, int right){

  /* 정렬할 범위가 2개 이상의 데이터이면(리스트의 크기가 0이나 1이 아니면) */
  if(left<right){
    // partition 함수를 호출하여 피벗을 기준으로 리스트를 비균등 분할 -분할(Divide)
    int q = partition(list, left, right); // q: 피벗의 위치

    // 피벗은 제외한 2개의 부분 리스트를 대상으로 순환 호출
    quick_sort(list, left, q-1); // (left ~ 피벗 바로 앞) 앞쪽 부분 리스트 정렬 -정복(Conquer)
    quick_sort(list, q+1, right); // (피벗 바로 뒤 ~ right) 뒤쪽 부분 리스트 정렬 -정복(Conquer)
  }

}
https://gmlwjd9405.github.io/2018/05/10/algorithm-quick-sort.html
                               '''
                               ),
                  db.Algorithm('최단거리 알고리즘', '네트워크에서 최단 경로를 찾는 알고리즘',
                               '최단거리 알고리즘은 네트워크에서 하나의 시작 정점으로부터 모든 다른 정점까지의 최단 경로를 찾는 알고리즘이야.',
                               '중', '_'),
                  db.Algorithm('트리 알고리즘', '트리 알고리즘',
                               '트리 알고리즘은 트리 알고리즘이야.',
                               '중', '_')
                  ]

problem_list = [db.Problem('수 정렬하기', '브론즈 1', 'N개의 수가 주어졌을 때, 이를 오름차순으로 정렬하는 프로그램을 작성하시오.',
                           '첫째 줄에 수의 개수 N(1 ≤ N ≤ 1,000)이 주어진다. 둘째 줄부터 N개의 줄에는 숫자가 주어진다. ' +
                           '이 수는 절댓값이 1,000보다 작거나 같은 정수이다. 수는 중복되지 않는다.',
                           '첫째 줄부터 N개의 줄에 오름차순으로 정렬한 결과를 한 줄에 하나씩 출력한다.',
                           'https://www.acmicpc.net/problem/2750'),
                db.Problem('쉬운 최단거리', '골드 5', '''지도가 주어지면 모든 지점에 대해서 목표지점까지의 거리를 구하여라. 
                문제를 쉽게 만들기 위해 오직 가로와 세로로만 움직일 수 있다고 하자.''',
                           '지도의 크기 n과 m이 주어진다. n은 세로의 크기, m은 가로의 크기다.(2 ≤ n ≤ 1000, 2 ≤ m ≤ 1000) ' +
                           '다음 n개의 줄에 m개의 숫자가 주어진다. 0은 갈 수 없는 땅이고 1은 갈 수 있는 땅, 2는 목표지점이다. 입력에서 2는 단 한개이다.',
                           '각 지점에서 목표지점까지의 거리를 출력한다. 원래 벽인 위치는 0을 출력하고, 원래 땅인 부분 중에서 도달할 수 없는 위치는 -1을 출력한다.',
                           'https://www.acmicpc.net/problem/14940')]

contest_list = [db.Contest('준파고를 잡아라', '2021-06-07 00:00:00','2021-06-07 00:00:00', '2021-05-10 00:00:00','2021:05:10 00:00:00',
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

print("algodb drop")

db.execute_query('drop table ALGORITHM_PROBLEM_CLASSIFICATION')
db.execute_query('drop table CONTEST_PROBLEM')
db.execute_query('drop table PROBLEM')
db.execute_query('drop table ALGORITHM')
db.execute_query('drop table CONTEST')

print("algodb create")

db.execute_query('''CREATE TABLE ALGORITHM (
                    NAME VARCHAR(100) NOT NULL PRIMARY KEY,
                    BRIEF_EXPLAIN VARCHAR(50),
                    DETAIL_EXPLAIN VARCHAR(250),
                    LEVEL VARCHAR(20),
                    EXAMPLE_CODE VARCHAR(5000),
                    PARENT VARCHAR(100),
                    CONSTRAINT PARENT_ALGORITHM FOREIGN KEY (PARENT) REFERENCES ALGORITHM (NAME)
                    )ENGINE=InnoDB DEFAULT CHARSET=utf8
                    ''')
db.execute_query('''CREATE TABLE PROBLEM (
                    NAME VARCHAR(100) NOT NULL PRIMARY KEY,
                    LEVEL VARCHAR(20),
                    CONTENT VARCHAR(5000),
                    INPUT VARCHAR(1000),
                    OUTPUT VARCHAR(1000),
                    URI VARCHAR(200)
                    )ENGINE=InnoDB DEFAULT CHARSET=utf8
                    ''')
db.execute_query('''CREATE TABLE CONTEST (
                    NAME VARCHAR(100) NOT NULL PRIMARY KEY,
                    CONTEST_START DATETIME,
                    CONTEST_END DATETIME,
                    RECEPTION_START DATETIME,
                    RECEPTION_END DATETIME,
                    CONTENT VARCHAR(5000),
                    SOURCE VARCHAR(5000),
                    URI VARCHAR(200)
                    )''')
db.execute_query('''CREATE TABLE ALGORITHM_PROBLEM_CLASSIFICATION (
                    ALGORITHM_NAME VARCHAR(100) not null,
                    PROBLEM_NAME VARCHAR(100) not null,
                    PRIMARY KEY (ALGORITHM_NAME, PROBLEM_NAME),
                    FOREIGN KEY (ALGORITHM_NAME) 
                    REFERENCES ALGORITHM (NAME)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE,
                    FOREIGN KEY (PROBLEM_NAME) 
                    REFERENCES PROBLEM (NAME)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE
                    )''')
db.execute_query('''CREATE TABLE CONTEST_PROBLEM (
                    CONTEST_NAME VARCHAR(100) not null,
                    PROBLEM_NAME VARCHAR(100) not null,
                    PRIMARY KEY (CONTEST_NAME, PROBLEM_NAME),
                    CONSTRAINT CP_CONTEST_FOREIGN FOREIGN KEY (CONTEST_NAME) 
                    REFERENCES CONTEST (NAME)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE,
                    CONSTRAINT CP_PROBLEM_FOREIGN FOREIGN KEY (PROBLEM_NAME) 
                    REFERENCES PROBLEM (NAME)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE
                    )''')

db.create_algorithm(algorithm_list)
db.create_problem(problem_list)
db.create_contest(contest_list)

db.create_algorithm_problem_classification([db.AlgorithmProblemClassification("정렬 알고리즘", "수 정렬하기")])
db.create_contest_problem("준파고를 잡아라","쉬운 최단거리")
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
