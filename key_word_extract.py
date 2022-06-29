# author: yue
# datetime: 2022/6/28 18:14
# file: key_word_extract.py
import os
from settings import system_setting
from hanlp_restful import HanLPClient
from textrank4zh import util
from textrank4zh.Segmentation import Segmentation

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

sentence_delimiters = ['?', '!', ';', '？', '！', '。', '；', '……', '…', '\n']
allow_POS_tags = ['an', 'i', 'j', 'l', 'n', 'nr', 'nrfg', 'ns', 'nt', 'nz', 't', 'v', 'vd', 'vn', 'eng']


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

        self.seg = Segmentation(stop_words_file=ROOT_PATH + system_setting.stop_file_path,
                                allow_speech_tags=allow_POS_tags,
                                delimiters=sentence_delimiters)

    def using_hanlp_api(self, sent: str, top_k=6):
        """

        :param sent:str
        :param top_k:int,
        :return: question: [str] the sentence that black out by the key phrase
                 answer: [list],
        """
        key_phrases = self.hanlpClient.keyphrase_extraction(sent, topk=top_k)
        question, answer = self._write_question(sent, key_phrases)
        return question, answer

    def using_text_rank(self,
                     sent: str,
                     top_k=6,
                     word_min_len=2):
        keywords = self._analyze(sent)
        # get phrase
        key_phrases = dict()
        count = 0
        for item in keywords:
            if count >= top_k:
                break
            if len(item.word) >= word_min_len:
                key_phrases[item.word] = item.weight
                count += 1
        question, answer = self._write_question(sent, key_phrases)
        return question, answer

    @staticmethod
    def _write_question(text: str, scores: dict, limit_blank=4):
        _index = 1
        answer = list()
        _text = text
        for k, v in scores.items():
            _text = _text.replace(k, '__[{index}]__'.format(index=_index))
            answer.append({_index: k})
            if _index > limit_blank - 1:
                break
            _index += 1
        return _text, answer

    def _analyze(self, text,
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


# unite test
if __name__ == '__main__':
    key_extractor = KeyExtract()
    T = "省第十四次党代会以来的五年极不平凡，是感恩奋进、实干争先的五年，是开启系统性变革、实现历史性跨越的五年。面对百年变局和世纪疫情相互叠加的复杂局面，我们在以习近平同志为核心的党中央坚强领导下，全面落实党的十九大和十九届历次全会精神，增强“四个意识”、坚定“四个自信”、做到“两个维护”，以最真挚的感情感悟总书记殷殷嘱托，以最坚决的行动落实总书记重要指示，团结带领全省人民忠实践行“八八战略”、奋力打造“重要窗口”，坚决扛起高质量发展建设共同富裕示范区政治责任，深入实施富民强省十大行动计划，全面建设“六个浙江”，高水平全面建成小康社会，浙江发展取得了历史性成就、站上了新的更高起点。"
    Q, A = key_extractor.using_hanlp_api(T)
    print(Q)
    print(A)
