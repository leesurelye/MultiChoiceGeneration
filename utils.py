# author: yue
# datetime: 2022/6/28 18:41
# file: utils.py

import os
from docx import Document
import pandas as pd


class WordUtils(object):
    def __init__(self, word_file_path: str, output_file_path: str):
        self.source_path = word_file_path
        self.output_path = output_file_path
        if not os.path.exists(self.source_path):
            raise ValueError("No such file :", self.source_path)

    def parsing(self):
        document = Document(self.source_path)
        output_file = open(self.output_path, 'w', encoding='utf-8')
        for para in document.paragraphs:
            output_file.write(para.text)
            output_file.write("\n")


class ExcelUtils(object):
    def __init__(self, question_file_path):
        self.output_file = question_file_path

    def writer(self, data: list, columns: list):
        df = pd.DataFrame(data=data, columns=columns)
        with pd.ExcelWriter(self.output_file) as writer:
            df.to_excel(writer)


# unit test
if __name__ == '__main__':
    test_data = {"a": "b", "b": "c"}
    utils = ExcelUtils(test_data)
    print("Done!")
