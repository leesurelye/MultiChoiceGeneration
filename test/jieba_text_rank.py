# author: yue
# datetime: 2022/6/30 16:21
# file: jieba_text_rank.py‘
import jieba
import jieba.analyse
from settings import system_setting
if __name__ == '__main__':
    jieba.analyse.set_stop_words(system_setting.stop_file_path)
    content = "这次大会是我省迈入高水平全面建设社会主义现代化、高质量发展建设共同富裕示范区新征程，召开的第一次党代会。大会主题是：高举习近平新时代中国特色社会主义思想伟大旗帜，忠实践行“八八战略”，坚决做到“两个维护”，在高质量发展中奋力推进中国特色社会主义共同富裕先行和省域现代化先行！"
    #  TF-IDF 共同富裕,社会主义,高质量,先行,现代化,特色,大会,党代会
    tags = jieba.analyse.extract_tags(content, withWeight=True, topK=8)

    # Text Rank
    # tags = jieba.analyse.textrank(content, topK=8, allowPOS=('ns', 'n'))
    print(tags)
