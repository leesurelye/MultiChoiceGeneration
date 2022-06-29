# author: yue
# datetime: 2022/6/28 19:19
# file: main.py

# the main function for this project
from settings import system_setting
from settings import customer_setting
import os
from utils import WordUtils, ExcelUtils

#  注意： 该项目不要安装在以中文命名的目录下
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))


class MultiChoiceGenerator(object):
    def __init__(self):
        self.min_len = customer_setting.min_question_length
        self.processed_file = system_setting.parsing_path
        self.word_utils = WordUtils(ROOT_PATH + customer_setting.word_file_path,
                                    ROOT_PATH + system_setting.parsing_path)
        if not os.path.exists(self.processed_file):
            self._processed_word_file()
        self.excel_utils = ExcelUtils(ROOT_PATH + customer_setting.excel_file_path)

    def _processed_word_file(self):
        self.word_utils.parsing()

    def read_sentence(self) -> list:
        source_txt = open(self.processed_file, 'r', encoding='utf-8').read()
        sentences = list()
        for para in source_txt.split('\n'):
            if len(para) < customer_setting.min_question_length:
                continue
            if len(para) > customer_setting.max_question_length:
                sentences.extend(para.split('。'))
            else:
                sentences.append(para)
        return sentences

    def key_extract_by_public_api(self, sentence: str) -> list:

    def key_extract_by_text_rank(self, sentence: str) -> list:

    def writer_question(self, data: dict):
        self.excel_utils.writer(data)

    def run(self):
        pass


if __name__ == '__main__':
    generator = MultiChoiceGenerator()
    generator.run()
