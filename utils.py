# author: yue
# datetime: 2022/6/28 18:41
# file: utils.py
from settings import customer_setting as cs

import os
from docx import Document
import pandas as pd


class WordUtils(object):
    def __init__(self):
        self.source_path = cs.word_file_path
        self.output_path = "doc/.output/file.txt"
        if not os.path.exists(self.source_path):
            raise ValueError("Could not find the input file :", self.source_path)

    def parsing(self):
        document = Document(self.source_path)
        output_file = open(self.output_path, 'w', encoding='utf-8')

        for para in document.paragraphs:
            output_file.write(para.text)
            output_file.write("\n")


class ExcelUtils(object):
    def __init__(self):
        self.output_file = cs.excel_file_path

    def writer(self, data: dict, columns: list):
        df = pd.DataFrame(data=data, columns=columns)
        with pd.ExcelWriter(self.output_file) as writer:
            df.to_excel(writer)


# unit test
# if __name__ == '__main__':
#     utils = ExcelUtils()
    # print("Done!")
