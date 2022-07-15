# author: yue
# datetime: 2022/6/28 18:14
# file: key_word_extract.py
import os
from settings import system_setting
from hanlp_restful import HanLPClient
from textrank4zh import util
import jieba
import jieba.analyse
from textrank4zh.Segmentation import Segmentation

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

sentence_delimiters = ['?', '!', ';', '？', '！', '。', '；', '……', '…', '\n']
allow_POS_tags = ['an', 'i', 'j', 'l', 'n', 'nr', 'nrfg', 'ns', 'nt', 'nz', 't']


class KeyExtract(object):
    """
        关键词抽取类：一共有两个实现方法
            方法一：使用Hanlp API工具
            方法二：使用TextRank算法

    """
    def __init__(self):
        self.hanlpClient = HanLPClient(system_setting.service_name,
                                       auth=system_setting.api_auth,
                                       language='zh')

        self.seg = Segmentation(stop_words_file=system_setting.stop_file_path,
                                allow_speech_tags=allow_POS_tags,
                                delimiters=sentence_delimiters)

    def using_hanlp_api(self, sent: str, top_k=8, limit_blank=4):
        """

        :param sent:str
        :param top_k:int,
        :param limit_blank: 控制产生空格的个数
        :return: question: [str] the sentence that black out by the key phrase
                 answer: [list],
        """
        key_phrases = self.hanlpClient.keyphrase_extraction(sent, topk=top_k)
        question, answer, remain = self._write_question(sent, key_phrases, limit_blank=limit_blank)
        return question, answer, remain

    def using_tf_idf(self, sen: str, top_k=8, limit_blank=4, word_min_len=2):
        words = jieba.analyse.extract_tags(sen, topK=top_k, withWeight=True)
        key_phrase = dict()
        for k, v in words:
            key_phrase[k] = v
        question, answer, remain = self._write_question(sen, key_phrase, limit_blank=limit_blank)
        return question, answer, remain

    def using_text_rank(self, sent: str, top_k=8, limit_blank=4, word_min_len=2):
        keywords = self._analyze(sent)
        # get phrase
        key_phrases = dict()
        count = 0
        for item in keywords:
            if count >= limit_blank:
                break
            # if len(item.word) >= word_min_len:
            key_phrases[item.word] = item.weight
            count += 1
        question, answer, remain = self._write_question(sent, key_phrases)
        return question, answer, remain

    @staticmethod
    def _write_question(text: str, scores: dict, limit_blank=4):
        _index = 0
        answer = dict()
        remain = list()
        _text = text
        for k, v in scores.items():
            if _index < limit_blank:
                _text = _text.replace(k, '#{index}'.format(index=_index), 1)
                answer[_index] = k
            else:
                remain.append(k)
            _index += 1
        _text, answer = KeyExtract._beautify(_text, answer)
        return _text, answer, remain

    @staticmethod
    def _beautify(text: str, answer: dict):
        mapping = {}
        index = 1
        while True:
            blank_index = text.find('#')
            if blank_index == -1:
                break
            slot = text[blank_index: blank_index + 2]
            mapping[int(text[blank_index + 1])] = index
            text = text.replace(slot, '__[{i}]__'.format(i=index))
            index += 1
        _corrected_ = dict()
        for k, v in answer.items():
            _corrected_[mapping[k]] = v

        return text, _corrected_

    def _analyze(self, text,
                 window=4,
                 lower=False,
                 vertex_source='all_filters',
                 edge_source='no_stop_words'):
        """分析文本

        Keyword arguments:
        text       --  文本内容，字符串。
        window     --  窗口大小，int，用来构造单词之间的边。默认值为2。
        lower      --  是否将文本转换为小写。默认为False。
        vertex_source   --  选择使用words_no_filter, words_no_stop_words, words_all_filters中的哪一个来构造pagerank对应的图中的节点。
                            默认值为`'all_filters'`，可选值为`'no_filter', 'no_stop_words', 'all_filters'`。关键词也来自`vertex_source`。
        edge_source     --  选择使用words_no_filter, words_no_stop_words, words_all_filters中的哪一个来构造pagerank对应的图中的节点之间的边。
                            默认值为`'no_stop_words'`，可选值为`'no_filter', 'no_stop_words', 'all_filters'`。边的构造要结合`window`参数。
        """

        # self.text = util.as_text(text)
        result = self.seg.segment(text=text, lower=lower)
        options = ['no_filter', 'no_stop_words', 'all_filters']
        if vertex_source in options:
            _vertex_source = result['words_' + vertex_source]
        else:
            _vertex_source = result['words_all_filters']

        if edge_source in options:
            _edge_source = result['words_' + edge_source]
        else:
            _edge_source = result['words_no_stop_words']

        return util.sort_words(_vertex_source, _edge_source, window=window)


# unite test
# if __name__ == '__main__':
#     key_extractor = KeyExtract()
#     text = "#2大抓#0鲜明导向，全面加强基层党组织和书记队伍建设，深化“导师#1制”，更好发挥党员先锋模范作用，推动基层党建全省域建强、全领域过硬、全面走在前列"
#     Q, A = KeyExtract._beautify(text, {0: '基层', 1: '帮带', 2: '树牢'})
#     print(Q)
#     print(A)
