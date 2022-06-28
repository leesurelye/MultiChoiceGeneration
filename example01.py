# -*- encoding:utf-8 -*-
import codecs
from textrank4zh import TextRank4Keyword, TextRank4Sentence
from settings import default_setting as ds

# just for test
if __name__ == '__main__':

    # text = codecs.open(ds.parsing_path, 'r', 'utf-8').read().split('\n')
    tr4w = TextRank4Keyword()
    text = "这次大会是我省迈入高水平全面建设社会主义现代化、高质量发展建设共同富裕示范区新征程，召开的第一次党代会。大会主题是：高举习近平新时代中国特色社会主义思想伟大旗帜，忠实践行“八八战略”，坚决做到“两个维护”，在高质量发展中奋力推进中国特色社会主义共同富裕先行和省域现代化先行！"
    tr4w.analyze(text=text, lower=True, window=3)  # py2中text必须是utf8编码的str或者unicode对象，py3中必须是utf8编码的bytes或者str对象

    print('关键词：')
    for item in tr4w.get_keywords(10, word_min_len=3):
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
