# author: yue
# datetime: 2022/6/28 21:16
# file: similarity_calculate.py

from settings import default_setting as ds
from gensim.models.keyedvectors import KeyedVectors


class SimilarCalculate(object):
    def __init__(self):
        self.w2v_model = KeyedVectors.load_word2vec_format(ds.chinese_word_vector,
                                                           binary=False,
                                                           unicode_errors='ignore')

    def most_similar(self, word: str):
        results = self.w2v_model.similar_by_word(word)
        for word in results:
            print(word)


if __name__ == "__main__":
    calculator = SimilarCalculate()
    calculator.most_similar("八八战略")