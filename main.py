# author: yue
# datetime: 2022/6/28 19:19
# file: main.py

# the main function for this project
import time

from settings import system_setting
from settings import customer_setting
import os
from utils import WordUtils, ExcelUtils
from interference_generator import SimilarCalculate
from key_word_extract import KeyExtract

#  注意： 该项目不要安装在以中文命名的目录下
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))


class MultiChoiceGenerator(object):
    def __init__(self, generated_mode=None):
        self.config = generated_mode
        self.min_len = customer_setting.min_question_length
        self.sentences = None
        self.word_utils = WordUtils(ROOT_PATH + customer_setting.word_file_path,
                                    ROOT_PATH + system_setting.parsing_path)
        if not os.path.exists(system_setting.parsing_path):
            self._processed_word_file()
        self.__load_sentence()
        self.processed_file = system_setting.parsing_path


        self.excel_utils = ExcelUtils(ROOT_PATH + customer_setting.excel_file_path)
        self.question_writer = KeyExtract()
        self.choice_writer = SimilarCalculate()

    def _config_parsing(self, config_path: str):
        pass

    def _processed_word_file(self):
        self.word_utils.parsing()

    def __load_sentence(self) -> list:
        source_txt = open(self.processed_file, 'r', encoding='utf-8').read()
        self.sentences = list()
        for para in source_txt.split('\n'):
            if len(para) < customer_setting.min_question_length:
                continue
            if len(para) > customer_setting.max_question_length:
                self.sentences.extend(para.split('。'))
            else:
                self.sentences.append(para)
        return self.sentences

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
            data.append([question, ' '.join(answer)])
            print(question)
            print(answer)
            time.sleep(2)  # since the api can only called 50 times every minute.
        self.dump_question(data)

    def dump_question(self, data: list):
        self.excel_utils.writer(data)


if __name__ == '__main__':
    generator = MultiChoiceGenerator()
    generator.full_mode_using_hanlp()
