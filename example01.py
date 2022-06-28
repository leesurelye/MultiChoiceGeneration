# -*- encoding:utf-8 -*-
import codecs
from textrank4zh import TextRank4Keyword, TextRank4Sentence
from settings import default_setting as ds
import sys

# just for test
if __name__ == '__main__':

    text = codecs.open(ds.parsing_path, 'r', 'utf-8').read()
    tr4w = TextRank4Keyword()

    tr4w.analyze(text=text, lower=True, window=2)  # py2中text必须是utf8编码的str或者unicode对象，py3中必须是utf8编码的bytes或者str对象

    print('关键词：')
    for item in tr4w.get_keywords(10, word_min_len=4):
        print(item.word, item.weight)
    #
    print()
    print('关键短语：')
    for phrase in tr4w.get_keyphrases(keywords_num=20, min_occur_num=2):
        print(phrase)

    tr4s = TextRank4Sentence()
    tr4s.analyze(text=text, lower=True, source='all_filters')

    print()
    print('摘要：')
    for item in tr4s.get_key_sentences(num=3):
        print(item.index, item.weight, item.sentence)
