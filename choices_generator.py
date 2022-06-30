# author: yue
# datetime: 2022/6/28 21:16
# file: choices_generator.py

from settings import system_setting
from gensim.models.keyedvectors import KeyedVectors


class SimilarCalculate(object):
    def __init__(self):
        # TODO loading this model may take a lot of time
        print("[*] Loading word to vector model... [it may take a while, about 3 minutes]")
        self.w2v_model = KeyedVectors.load_word2vec_format(system_setting.chinese_word_vector,
                                                           binary=False,
                                                           unicode_errors='ignore')
        print("[*] Load finished!")

    def most_similar(self, word: str, limit=3, top_k=10, threshold=0.5) -> list:
        """
        given a word and calculate the most similar word in this directory
        :param word:
        :param limit:
        :param top_k:
        :param threshold:
        :return: list
        """
        if limit == 0:
            return list()
        try:
            similarity = self.w2v_model.most_similar(negative=[word], topn=top_k)
        except KeyError:
            return list()
        res = list()
        for s_word, weight in similarity:
            if len(word) == len(s_word):
                res.append(s_word)
            if len(res) == limit:
                return res
        if len(res) == 0:
            return [x for x, w in similarity if w >= threshold]
        return res


# if __name__ == "__main__":
#     calculator = SimilarCalculate()
#     while True:
#         print("input:")
#         text = input()
#         calculator.most_similar(text)
