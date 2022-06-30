# author: yue
# datetime: 2022/6/28 18:14
# file: user_setting.py
# encoding utf-8
# 该文件为用户配置文件，可以按照说明修改相关配置

# 需要生成问题的原始文本，需要的文件格式为docx
word_file_path = "C:/Users/yue/Desktop/MultiChoice/doc/浙江省第十五次党代会报告（全文）.docx"
# excel文档输出位置
excel_file_path = "C:/Users/yue/Desktop/MultiChoice/result/questions.xlsx"
# 最短的题干长度
min_question_length = 40
# 最长的体感长度
max_question_length = 200
# 过滤标题长度
filter_question_length = 30
# 生成表格的标题
columns = ["题干", "选项A", "选项B", "选项C", "选项D", "正确选项1", "正确选项2", "正确选项3", "正确选项4"]
sheets = ['4选1', '4选2', '4选3', '4选4']
default_columns = ["问题题干", "选项", "答案"]
# 生成问题的比列, 从左到右依次是，4选1, 4选2, 4选3, 4选4占比
type_scale = [0.4, 0.2, 0.2, 0.2]
