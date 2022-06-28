#-*- encoding:utf-8 -*-

# import sys
import codecs
from textrank4zh import TextRank4Sentence

# text = codecs.open('../../doc/03.txt', 'r', 'utf-8').read()
if __name__ == '__main__':
    text = "这间酒店位于北京东三环，里面摆放很多雕塑，文艺气息十足。答谢宴于晚上8点开始。"
    tr4s = TextRank4Sentence()
    tr4s.analyze(text=text, lower=True, source = 'all_filters')

    for st in tr4s.sentences:
        print(type(st), st)

    print(20*'*')
    for item in tr4s.get_key_sentences(num=4):
        print(item.weight, item.sentence, type(item.sentence))