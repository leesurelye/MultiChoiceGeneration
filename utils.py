# author: yue
# datetime: 2022/6/28 18:41
# file: utils.py

import os
from docx import Document
import pandas as pd
from settings import system_setting


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
        output_file.close()


class ExcelStyle(object):
    def __init__(self, name='default'):
        self.name = name
        if name == 'default':
            self.columns = system_setting.default_style['columns']
            # TODO　
            self.sheets = None
        elif name == 'detail':
            self.columns = system_setting.default_style['detail']
            self.sheets = system_setting.default_style['sheets']
        elif name == 'combine':
            self.columns = system_setting.default_style['detail']
            self.sheets = None
        else:
            raise KeyError("ExcelStyle.name")


class ExcelUtils(object):
    def __init__(self, question_file_path):
        self.output_file = question_file_path

    def writer(self, data: list, style: ExcelStyle):
        columns = style.columns
        df = pd.DataFrame(data=data, columns=columns)
        with pd.ExcelWriter(self.output_file) as writer:
            df.to_excel(writer, index_label='序号')
        writer.close()

    # def composite_mode(self, data: list, scales, style: ExcelStyle):
    #     """ 综合模式 """
    #     n = len(data)
    #     offset = 0
    #     writer = pd.ExcelWriter(self.output_file)
    #     for i in range(len(scales)):
    #         start, end = offset, offset + int(n * scales[i])
    #         tmp = data[start:end]
    #         data = self.__generate_questions(sentences=tmp, limit_blank=i + 1)
    #         new_data = self.__trans_data(data, columns=user_setting.combine_columns)
    #         df = pd.DataFrame(data=new_data, columns=user_setting.combine_columns)
    #         df.to_excel(writer, index_label='序号', sheet_name=user_setting.sheets[i])
    #         offset = end
    #     writer.close()

# # unit test
# if __name__ == '__main__':
#     test_data = {"a": "b", "b": "c"}
#     utils = ExcelUtils(test_data)
#     heapq.nlargest()
#     print("Done!")
