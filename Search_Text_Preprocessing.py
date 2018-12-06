from settings import Settings
from preprocessing_chinese_text import PreprocessingChineseText
from preprocessing_english_text import PreprocessingEnglishText
from bag_of_word import BagOfWord
import os


def main(global_set, search_str):
    #  设置参数 ========================================================================================================
    print('Search Text Preprocessing Function Start.')

    # 检测中文还是英文
    chinese_or_english = 'E'
    for ch in search_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            chinese_or_english = 'C'
    # print(chinese_or_english)

    if chinese_or_english == 'C':
        #  中文文本预处理
        # step1
        print('Chinese Search Text Preprocessing')
        string = '搜索原文生成简单文本'
        global_set.print_gui(string)
        # 生成预处理类
        preprocessing_c = PreprocessingChineseText(global_set.punctuation, global_set.stopwords_c)
        search_word_path = os.path.join(global_set.sys_log_dir_name, 'search_word.txt')
        # 处理信息
        preprocessing_c.get_search_text_info(search_str, search_word_path)

        # step2
        print('Chinese Search BOW generation')
        string = '搜索简单文本生成词袋'
        global_set.print_gui(string)
        # 生成预处理类
        bow = BagOfWord()
        search_bow_path = os.path.join(global_set.sys_log_dir_name, 'search_bow.txt')
        # 处理信息
        bow.convert_info(search_word_path, search_bow_path)
        bow_word_list = bow.bow_word_list
        bow_tf_list = bow.bow_tf_list

    else:
        #  英文文本预处理
        # step1
        print('English News Text Preprocessing')
        string = '搜索原文生成简单文本'
        global_set.print_gui(string)
        # 生成预处理类
        preprocessing_e = PreprocessingEnglishText(global_set.punctuation, global_set.stopwords_e)
        search_word_path = os.path.join(global_set.sys_log_dir_name, 'search_word.txt')
        # 处理信息
        preprocessing_e.get_search_text_info(search_str, search_word_path)

        # step2
        print('English Search BOW generation')
        string = '搜索简单文本生成词袋'
        global_set.print_gui(string)
        # 生成预处理类
        bow = BagOfWord()
        search_bow_path = os.path.join(global_set.sys_log_dir_name, 'search_bow.txt')
        # 处理信息
        bow.convert_info(search_word_path, search_bow_path)
        bow_word_list = bow.bow_word_list
        bow_tf_list = bow.bow_tf_list
    # 结束信息
    print('Search Text Preprocessing Function Finish!')

    return bow_word_list, bow_tf_list


if __name__ == '__main__':
    global_set = Settings()
    search_str = '我爱中国！ i love China!'
    print(str(main(global_set, search_str)))
