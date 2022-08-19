#
# this file is default setting
# C:/Users/yue/Desktop/MultiChoice/
# ==== please don't change this settings =====

output_dir = "doc/.output/"
parsing_path = "doc/.output/file.txt"
# hanlp_api_auth
api_auth = "MTIyMEBiYnMuaGFubHAuY29tOnpJOU9JcTczWjAyUUZhOGw="
# key extract server name
service_name = "https://www.hanlp.com/api"
# config for word embedding
chinese_word_vector = ".model/sgns.renmin.bigram.bz2"
stop_file_path = ".config/stopwords.txt"
user_dict_path = ".config/userdict.txt"
restrict_vocab_size = 10000  # the total number is 25K
key_phrase_num = 100
default_style = {
    'name': 'combine',
    'columns': ["问题题干", "选项", "答案"]
}

detail_style = {
    'name': 'detail',
    'columns': ["题干", "选项A", "选项B", "选项C", "选项D", "正确选项1", "正确选项2", "正确选项3", "正确选项4"],
    'sheets': ['4选1', '4选2', '4选3', '4选4']
}
combine_style = {
    'name':'combine',
    'columns': ["题干", "正确选项"]
}