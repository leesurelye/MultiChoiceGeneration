# author: yue
# datetime: 2022/6/28 19:19
# file: main.py

# the main function for this project
import time
import random

import jieba.analyse

from settings import system_setting
from settings import customer_setting
from utils import WordUtils, ExcelUtils
from interference_generator import SimilarCalculate
from key_word_extract import KeyExtract
import os
import sys
from tqdm import tqdm

#  注意： 该项目不要安装在以中文命名的目录下
sys.path.append(os.getcwd())


class MultiChoiceGenerator(object):
    def __init__(self, algorithm='text-rank'):
        self.algorithm = algorithm
        if self.algorithm not in ['api', 'tf-idf', 'text-rank']:
            raise KeyError("algorithm key error {error}".format(error=algorithm))
        self.min_len = customer_setting.min_question_length
        self.sentences = None
        self.word_utils = WordUtils(customer_setting.word_file_path,
                                    system_setting.parsing_path)
        self.processed_file = system_setting.parsing_path

        self.excel_utils = ExcelUtils(customer_setting.excel_file_path)
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
        if customer_setting.min_question_length < len(sent):
            return True
        else:
            return False

    def __load_sentence(self):
        source_txt = open(self.processed_file, 'r', encoding='utf-8').read()
        self.sentences = list()
        for para in source_txt.split('\n'):
            if len(para) <= customer_setting.filter_question_length:
                continue
            for sentence in para.split("。"):
                if self.__check_sentence(sentence):
                    self.sentences.append(sentence)

    def full_mode(self):
        """
        全量模式：多选 4选4
        :return:
        """
        if self.sentences is None:
            self.__load_sentence()
        self.write()

    def lack_mode(self):
        """
        多选：缺省模式： 4选3或2
        系统随机生成4选2的多选，或者4选3的多选
        :return:
        """
        self.write(3)

    def write(self, limit_blank=4):
        data = list()
        for sent in tqdm(self.sentences, desc="[Writer Questions]:"):
            if self.algorithm == 'text-rank':
                questions, answers, candidates = self.question_writer.using_text_rank(sent, limit_blank=limit_blank)
            elif self.algorithm == 'tf-idf':
                questions, answers, candidates = self.question_writer.using_tf_idf(sent, limit_blank=limit_blank)
            elif self.algorithm == 'api':
                questions, answers, candidates = self.question_writer.using_hanlp_api(sent, limit_blank=limit_blank)
            else:
                raise KeyError("algorithm key error! {error}".format(error=self.algorithm))
            _index = random.randint(0, len(answers) - 1)
            choice = answers.copy()
            interference = self.choice_writer.most_similar(answers[_index], limit=4 - limit_blank)
            # if there is no similar word, chose one from key phrase
            index = len(answers)
            if len(interference) == 0:
                interference = candidates
            for error in interference:
                choice[index] = error
                index += 1
            data.append([questions, str(choice), str(answers)])
            if self.algorithm == 'hanlp':
                time.sleep(2)
        self.__dump_question(data)

    def single_mode(self):
        """
        单项选择: 4选1
        :return:
        """
        self.write(limit_blank=1)

    def __dump_question(self, data: list):
        if os.path.exists(customer_setting.excel_file_path):
            os.remove(customer_setting.excel_file_path)
        self.excel_utils.writer(data)


if __name__ == '__main__':
    # system initial code
    jieba.analyse.set_stop_words(system_setting.stop_file_path)
    generator = MultiChoiceGenerator(algorithm='tf-idf')
    generator.single_mode()
    print("Done!")
    # print(generator.sentences)
