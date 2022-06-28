# author: yue
# datetime: 2022/6/28 21:00
# file: test.py
from hanlp_restful import HanLPClient

if __name__ == '__main__':
    HanLP = HanLPClient('https://www.hanlp.com/api', auth=None, language='zh')  # auth不填则匿名，zh中文，mul多语种
    text = "这次大会是我省迈入高水平全面建设社会主义现代化、高质量发展建设共同富裕示范区新征程，召开的第一次党代会。大会主题是：高举习近平新时代中国特色社会主义思想伟大旗帜，忠实践行“八八战略”，坚决做到“两个维护”，在高质量发展中奋力推进中国特色社会主义共同富裕先行和省域现代化先行！"
    res = HanLP.keyphrase_extraction(text, topk=10)
    print(res)
