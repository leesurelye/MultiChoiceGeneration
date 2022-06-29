# author: yue
# datetime: 2022/6/28 18:14
# file: key_word_extract.py
import os
from settings import system_setting
from hanlp_restful import HanLPClient
from textrank4zh import TextRank4Keyword
from textrank4zh import util
from textrank4zh.Segmentation import Segmentation

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

sentence_delimiters = ['?', '!', ';', '？', '！', '。', '；', '……', '…', '\n']
allow_POS_tags = ['an', 'i', 'j', 'l', 'n', 'nr', 'nrfg', 'ns', 'nt', 'nz', 't', 'v', 'vd', 'vn', 'eng']


class KeyExtract(object):
    def __init__(self, method="api"):
        self.method = method
        self.hanlpClient = HanLPClient(system_setting.service_name, auth=system_setting.api_auth,
                                       language='zh') if self.method == 'api' else None
        self.extract_model = TextRank4Keyword(stop_words_file=ROOT_PATH + system_setting.stop_file_path)
        self.seg = Segmentation(stop_words_file=ROOT_PATH + system_setting.stop_file_path,
                                allow_speech_tags=allow_POS_tags,
                                delimiters=sentence_delimiters)

    def by_hanlp_api(self, sent: str, top_k=6):
        """

        :param sent:
        :param top_k:
        :return: question: [str] the sentence that black out by the key phrase
                 answer: [list],
        """
        key_phrases = self.hanlpClient.keyphrase_extraction(sent, topk=top_k)
        question, answer = self._write_question(sent, key_phrases)
        return question, answer

    def by_text_rank(self,
                     sent: str,
                     top_k=6,
                     word_min_len=2):
        keywords = self.analyze(sent)
        # get phrase
        result = []
        count = 0
        for item in keywords:
            if count >= top_k:
                break
            if len(item.word) >= word_min_len:
                result.append(item)
                count += 1
        return result

    @staticmethod
    def _write_question(text: str, scores: dict, limit_blank=4):
        index = 1
        answer = list()
        for k, v in scores.items():
            text = text.replace(k, '__[{index}]__'.format(index=index))
            index += 1
            answer.append({index: k})
            if index == limit_blank:
                break
        return text, answer

    def analyze(self, text,
                window=2,
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
