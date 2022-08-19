# author: yue
# datetime: 2022/6/30 17:58
# file: question_generator.py
import time
import random
from settings import system_setting
from settings import user_setting
from utils import WordUtils, ExcelUtils, ExcelStyle
from choices_generator import SimilarCalculate
from key_word_extract import KeyExtract
import os
from typing import List
from tqdm import tqdm


class MultiChoiceGenerator(object):
    __mapping__ = {1: 'A', 2: 'B', 3: 'C', 4: 'D'}

    # 当前默认的算法为text-rank, excel 表格的风格为 default_style
    def __init__(self, algorithm='text-rank', excel_style=user_setting.excel_style):
        # 存储当前设置的算法
        self.algorithm = algorithm
        self.excel_style = ExcelStyle(excel_style)
        # 判断算法是否为 api, tf-idf,  text-rank 算法之一
        if self.algorithm not in ['api', 'tf-idf', 'text-rank']:
            raise KeyError("algorithm key error {error}".format(error=algorithm))
        self.min_len = user_setting.min_question_length
        self.sentences = None
        self.word_utils = WordUtils(user_setting.word_file_path,
                                    system_setting.parsing_path)
        self.processed_file = system_setting.parsing_path

        self.excel_utils = ExcelUtils(user_setting.excel_file_path)
        if not os.path.exists(system_setting.output_dir):
            os.mkdir(system_setting.output_dir)
        if not os.path.exists(system_setting.parsing_path):
            self._processed_word_file()
        self.__load_sentence()
        self.question_writer = KeyExtract()
        self.choice_writer = SimilarCalculate()

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
        self.__generate_questions()

    def single_mode(self):
        """
        单项选择: 4选1
        :return:
        """
        data = self.__generate_questions(limit_blank=1)
        self.__dump_question(data)

    def lack_mode(self):
        """
        多选：缺省模式： 4选3
        系统随机生成4选2的多选，或者4选3的多选
        :return:
        """
        data = self.__generate_questions(3)
        self.__dump_question(data)

    def __generate_questions(self, sentences=None, limit_blank=4):
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
            index = len(answers) + 1
            if len(interference) == 0:
                interference = candidates
            for error in interference:
                choice[index] = error
                index += 1
                if index >= 5:
                    break
            data.append([questions, choice, answers])
            if self.algorithm == 'hanlp':
                time.sleep(2)
        return data

    @staticmethod
    def __mess_up_choices():
        cur = [1, 2, 3, 4]
        random.shuffle(cur)
        return cur

    def __trans_data(self, data: list):
        new_data = list()
        columns = self.excel_style.columns
        N = len(columns)
        if self.excel_style.name == 'combine':
            for question, choice, answer in data:
                # 打乱选项
                messed_up = MultiChoiceGenerator.__mess_up_choices()
                new_row = [''] * N
                tmp_q = question+"。"

                for i in range(1, 5):
                    tmp_q += '\n' + MultiChoiceGenerator.__mapping__[i] + '.' + choice.get(messed_up[i-1], '')
                new_row[0] = tmp_q
                ans = ''
                for i in range(1, 1 + len(answer)):
                    answer_index = messed_up.index(i) + 1
                    ans += MultiChoiceGenerator.__mapping__[answer_index]
                new_row[1] = ans
                new_data.append(new_row)
        elif self.excel_style.name == 'detail':
            for question, choice, answer in data:
                # 打乱选项
                messed_up = MultiChoiceGenerator.__mess_up_choices()
                new_row = [''] * N
                tmp_q = question + "。"
                new_row[0] = tmp_q
                for i in range(1, 5):
                    new_row[i] = MultiChoiceGenerator.__mapping__[i] + '.' + choice.get(messed_up[i - 1], '')
                for i in range(5, 9):
                    if i - 4 in answer:
                        new_row[i] = MultiChoiceGenerator.__mapping__[i - 4]
                new_data.append(new_row)
        elif self.excel_style.name == 'default':
            for question, choice, answer in data:
                # 打乱选项
                messed_up = MultiChoiceGenerator.__mess_up_choices()
                new_row = [''] * N
                tmp_q = question + "。"
                new_row[0] = tmp_q
                choices = ''
                for i in range(1, 5):
                    choices += '\n' + MultiChoiceGenerator.__mapping__[i] + '.' + choice.get(messed_up[i - 1], '')
                new_row[1] = choice
                answers = ''
                for i in range(1, 5):
                    if i in answer:
                        answers += MultiChoiceGenerator.__mapping__[i] + '\n'
                new_row[2] = answers
                new_data.append(new_row)
        return new_data

    def __dump_question(self, data: list):
        if os.path.exists(user_setting.excel_file_path):
            os.remove(user_setting.excel_file_path)
        # 写入excel表格的代码，在修改excel表格风格
        self.excel_utils.writer(data, self.excel_style)

    def composite_mode(self, scales=user_setting.type_scale):
        """ 综合模式 """
        n = len(self.sentences)
        offset = 0
        data = list()
        for i in range(len(scales)):
            start, end = offset, offset + int(n * scales[i])
            tmp = self.sentences[start:end]
            data = self.__generate_questions(sentences=tmp, limit_blank=i + 1)
            new_data = self.__trans_data(data)
            data.extend(new_data)
            # df = pd.DataFrame(data=new_data, columns=user_setting.combine_columns)
            # df.to_excel(writer, index_label='序号', sheet_name=user_setting.sheets[i])
            offset = end
        self.excel_utils.writer(data, self.excel_style)
