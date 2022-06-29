# author: yue
# datetime: 2022/6/28 19:19
# file: main.py

# the main function for this project
import time

from settings import system_setting
from settings import customer_setting
from utils import WordUtils, ExcelUtils
from interference_generator import SimilarCalculate
from key_word_extract import KeyExtract
import os
import sys

#  注意： 该项目不要安装在以中文命名的目录下
sys.path.append(os.getcwd())


class MultiChoiceGenerator(object):
    def __init__(self, generated_mode=None):
        self.config = generated_mode
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
        if customer_setting.min_question_length < len(sent) < customer_setting.max_question_length:
            return True
        else:
            return False

    def __load_sentence(self):
        source_txt = open(self.processed_file, 'r', encoding='utf-8').read()
        self.sentences = list()
        for para in source_txt.split('\n'):
            if self.__check_sentence(para):
                self.sentences.append(para)
            elif len(para) > customer_setting.max_question_length:
                self.sentences.extend([s for s in para.split('。') if self.__check_sentence(s)])

    def full_mode_using_hanlp(self):
        """
        全量模式：多选 4选4
        :return:
        """
        if self.sentences is None:
            self.__load_sentence()
        data = list()
        for sent in self.sentences:
            question, answer = self.question_writer.using_hanlp_api(sent)
            data.append([question, str(answer)])
            print(question)
            print(answer)
            time.sleep(2)  # since the api can only called 50 times every minute.
        self.dump_question(data)

    def lack_mode_using_hanlp(self):
        """
        多选：缺省模式： 4选3或2
        系统随机生成4选2的多选，或者4选3的多选
        :return:
        """
        pass

    def single_mode_using_hanlp(self):
        """
        单项选择
        :return:
        """
        pass

    def dump_question(self, data: list):
        self.excel_utils.writer(data)


if __name__ == '__main__':
    generator = MultiChoiceGenerator()
    generator.full_mode_using_hanlp()
