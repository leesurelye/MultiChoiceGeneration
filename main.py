# author: yue
# datetime: 2022/6/28 19:19
# file: main.py

# the main function for this project

import jieba.analyse
from settings import system_setting
from settings import user_setting
import os
import sys
from question_generator import MultiChoiceGenerator
# jieba 配置
jieba.analyse.set_stop_words(system_setting.stop_file_path)
jieba.load_userdict(system_setting.user_dict_path)
#  注意： 该项目不要安装在以中文命名的目录下
sys.path.append(os.getcwd())


if __name__ == '__main__':
    generator = MultiChoiceGenerator(algorithm='tf-idf')
    generator.composite_mode()
    print("Done! The output file at:", user_setting.excel_file_path)
