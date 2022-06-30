# author: yue
# datetime: 2022/6/30 17:58
# file: question_generator.py
import time
import random
from settings import system_setting
from settings import user_setting
from utils import WordUtils, ExcelUtils
from choices_generator import SimilarCalculate
from key_word_extract import KeyExtract
import os
from tqdm import tqdm


class MultiChoiceGenerator(object):
    def __init__(self, algorithm='text-rank'):
        self.__mapping__ = {1: 'A', 2: 'B', 3: 'C', 4: 'D'}
        self.algorithm = algorithm
        if self.algorithm not in ['api', 'tf-idf', 'text-rank']:
            raise KeyError("algorithm key error {error}".format(error=algorithm))
        self.min_len = user_setting.min_question_length
        self.sentences = None
        self.word_utils = WordUtils(user_setting.word_file_path,
                                    system_setting.parsing_path)
        self.processed_file = system_setting.parsing_path

        self.excel_utils = ExcelUtils(user_setting.excel_file_path)
        if not os.path.exists(system_setting.parsing_path):
            self._processed_word_file()
        self.__load_sentence()
        self.question_writer = KeyExtract()
        self.choice_writer = SimilarCalculate()

    def _config_parsing(self, config_path: str):
        pass

    def _processed_word_file(self):
        self.word_utils.parsing()

    @staticmethod
    def __check_sentence(sent: str):
        if user_setting.min_question_length < len(sent):
            return True
        else:
            return False

    def __load_sentence(self):
        source_txt = open(self.processed_file, 'r', encoding='utf-8').read()
        self.sentences = list()
        for para in source_txt.split('\n'):
            if len(para) <= user_setting.filter_question_length:
                continue
            for sentence in para.split("。"):
                if self.__check_sentence(sentence):
                    self.sentences.append(sentence)
        print("[*] Total question length: {length}".format(length=len(self.sentences)))

    def full_mode(self):
        """
        全量模式：多选 4选4
        :return:
        """
        if self.sentences is None:
            self.__load_sentence()
        self.__write()

    def single_mode(self):
        """
        单项选择: 4选1
        :return:
        """
        data = self.__write(limit_blank=1)
        self.__dump_question(data)

    def lack_mode(self):
        """
        多选：缺省模式： 4选3
        系统随机生成4选2的多选，或者4选3的多选
        :return:
        """
        data = self.__write(3)
        self.__dump_question(data)

    def __write(self, sentences=None, limit_blank=4):
        data = list()
        if sentences is None:
            sentences = self.sentences
        for sent in tqdm(sentences,
                         desc="[Writer Questions] type={type}".format(type=limit_blank)):
            if self.algorithm == 'text-rank':
                questions, answers, candidates = self.question_writer.using_text_rank(sent, limit_blank=limit_blank)
            elif self.algorithm == 'tf-idf':
                questions, answers, candidates = self.question_writer.using_tf_idf(sent, limit_blank=limit_blank)
            elif self.algorithm == 'api':
                questions, answers, candidates = self.question_writer.using_hanlp_api(sent, limit_blank=limit_blank)
            else:
                raise KeyError("algorithm key error! {error}".format(error=self.algorithm))
            _index = random.randint(1, len(answers))
            choice = answers.copy()
            interference = self.choice_writer.most_similar(answers[_index], limit=4 - limit_blank)
            # if there is no similar word, chose one from key phrase
            index = len(answers)
            if len(interference) == 0:
                interference = candidates
            for error in interference:
                choice[index] = error
                index += 1
                if index == 4:
                    break
            data.append([questions, str(choice), str(answers)])
            if self.algorithm == 'hanlp':
                time.sleep(2)
        return data

    def __dump_question(self, data: list, style='default'):
        if os.path.exists(user_setting.excel_file_path):
            os.remove(user_setting.excel_file_path)
        if style == 'default':
            self.excel_utils.writer(data, columns=user_setting.default_columns)
        else:
            new_data = list()
            for question, choice, answer in data:
                new_row = [''] * 9
                new_row[0] = question
                for i in range(1, 5):
                    new_row[i] = choice.get(i, '')
                for i in range(5, 9):
                    if i - 4 in answer:
                        new_row[i] = self.__mapping__[i - 4]
                new_data.append(new_row)
            self.excel_utils.writer(new_data, columns=user_setting.columns)

    def composite_mode(self, scales=user_setting.type_scale):
        """ 综合模式 """
        n = len(self.sentences)
        offset = 0
        total = list()
        for i in range(len(scales)):
            start, end = offset, offset + int(n * scales[i])
            data = self.sentences[start:end]
            tmp = self.__write(sentences=data, limit_blank=i + 1)
            total.extend(tmp)
            offset = end
        self.__dump_question(total)
