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

# 함수 설명
## form
- slot 
  - 실제 선언된 entity이어야만 함
  - tracker.get_slot(key) 로 받아올 수 있는 변수
  - slot_mappings을 통해 다른 엔티티를 매핑하여 대입이 가능
- slot_mappings
  - 여러 문장이나 엔티티를 slot변수로 매핑해주는 역할
- validate_'slot 이름'
  - required_slots 슬롯은 자동으로 호출하여 매핑된 value를 통해 리턴값을 넘겨줌
- submit
  - 값 리턴
  
## tracker
- tracker.get_latest_entity_values(entity)
  - entity는 실제 받아온 entity