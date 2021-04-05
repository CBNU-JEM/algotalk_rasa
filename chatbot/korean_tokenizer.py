from typing import Any, List, Text,Optional,Dict

from rasa.nlu.components import Component
from rasa.nlu.config import RasaNLUModelConfig
from rasa.nlu.tokenizers.tokenizer import Token, Tokenizer
from rasa.nlu.training_data import Message, TrainingData

from rasa.nlu.constants import (
    RESPONSE,
    TEXT,
    CLS_TOKEN,
    TOKENS_NAMES,
    MESSAGE_ATTRIBUTES,
    INTENT,
)

import MeCab
import mecab_ko_dic


class KoreanTokenizer(Tokenizer, Component):
    # name = "tokenizer_korean"
    #provides = ["tokens"]
    # defaults =  {}
    # language_list = ["kr"]

    # def train(
    #         self, training_data: TrainingData, config: RasaNLUModelConfig, **kwargs: Any
    # ) -> None:
    #
    #     for example in training_data.training_examples:
    #         example.set("tokens", self.tokenize(example.text))
    #
    # def process(self, message: Message, **kwargs: Any) -> None:
    #
    #     message.set("tokens", self.tokenize(message.text))
    def train(
            self,
            training_data: TrainingData,
            config: Optional[RasaNLUModelConfig] = None,
            **kwargs: Any,
    ) -> None:
        """Tokenize all training data."""


        for example in training_data.training_examples:
            for attribute in MESSAGE_ATTRIBUTES:
                if example.get(attribute) is not None:

                    if attribute == INTENT:
                        tokens = self._split_intent(example)
                    else:
                        tokens = self.tokenize(example, attribute)
                        tokens = self.add_cls_token(tokens, attribute)
                    example.set(TOKENS_NAMES[attribute], tokens)

    def process(self, message: Message, **kwargs: Any) -> None:
        """Tokenize the incoming message."""
        tokens = self.tokenize(message, TEXT)
        tokens = self.add_cls_token(tokens, TEXT)
        message.set(TOKENS_NAMES[TEXT], tokens)

    @staticmethod
    def tokenize(message: Message, attribute: Text) -> List[Token]:
        def mecabsplit(mecab_tagger, inputs, pos):
            r = []
            inputs = mecab_tagger.parse(inputs)
            t = inputs.split('\n')[:-2]
            for i in t:
                field = i.split('\t')
                if field[1].split(',')[-1] is not '*':
                    r.extend([(x.split('/')[0], x.split('/')[1]) for x in field[1].split(',')[-1].split('+')])
                else:
                    r.append((field[0], field[1].split(',')[0]))
            if pos:
                return r
            else:
                return [x[0] for x in r]
            return r

        mecab_tagger = MeCab.Tagger(mecab_ko_dic.MECAB_ARGS)
        a = mecab_tagger.parse(message.get(attribute))
        t = a.split('\n')[:-2]

        tokenpointer = []
        pointeroffset = 0
        for i in t:
            field = i.split('\t')
            if field[1].split(',')[-1] is not '*':
                currentptr = message.get(attribute).index(field[0], pointeroffset)
                for x in field[1].split(',')[-1].split('+'):
                    try:
                        w = x.split('/')[0]
                        temp = field[0].index(w)
                        tokenpointer.append((currentptr + temp, currentptr + temp + len(w)))
                    except:
                        tokenpointer.append((currentptr, currentptr + len(field[0])))
                pointeroffset = currentptr + len(field[0])
            else:
                currentptr = message.get(attribute).index(field[0], pointeroffset)
                tokenpointer.append((currentptr, currentptr + len(field[0])))
                pointeroffset = currentptr + len(field[0])
        words = mecabsplit(mecab_tagger, message.get(attribute), False)
        tokens = []
        offset = 0
        for word in words:
            word_offset = tokenpointer[words.index(word, offset)][0]
            tokens.append(Token(word, word_offset))
            offset += 1
        return tokens