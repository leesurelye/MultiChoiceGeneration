# author: yue
# datetime: 2022/6/28 19:19
# file: main.py

# the main function for this project
from settings import default_setting as ds
from settings import customer_setting as cs
import os
from utils import WordUtils, ExcelUtils

#  注意： 该项目不要安装在以中文命名的目录下
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

class MultiChoiceGenerator(object):
    def __init__(self):
        self.min_len = cs.min_sentence_length
        self.processed_file = ds.parsing_path
        self.word_utils = WordUtils(ROOT_PATH + cs.word_file_path, ROOT_PATH + ds.parsing_path)
        if not os.path.exists(self.processed_file):
            self._processed_word_file()
        self.excel_utils = ExcelUtils(ROOT_PATH + cs.excel_file_path)

    def _processed_word_file(self):
        self.word_utils.parsing()

    def writer_question(self, data: dict):
        self.excel_utils.writer(data)

    def run(self):


if __name__ == '__main__':
    generator = MultiChoiceGenerator()
    generator.run()
