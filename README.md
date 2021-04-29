# algotalk_rasa
korean_tokenizer.py
rasa/nlu/tokenizers
- 로컬사용시 81번째 줄 주석 바꾸기
- #mecab_tagger = MeCab.Tagger(mecab_ko_dic.MECAB_ARGS)

crf_entity_extractor_korean.py
rasa/nlu/extractors

bilou_utils_Kr.py
rasa/nlu/utils

registry.py
rasa/nlu

# 로컬 db 설정
## mac
- brew install mysql
- mysql.server start
- mysql
- create user algotalk@localhost identified by 'algojem';
- create database algotalk_db default character set utf8;
- grant all privileges on algotalk_db.* to algotalk@localhost;


# action 서버 실행
rasa run actions --actions actions.actions

# form
- action에서 get_slot을 쓰기위해 사용
- 여러 의도에 퍼져있는 엔티티를 하나의 엔티티 슬롯으로 지정해주는 역할 (from_entity)
- 필요한 슬롯이 있는지 확인해주는 역할 (required_slots)
- 슬롯 데이터가 정확한지 판단해주는 역할 (def validate_이름)
