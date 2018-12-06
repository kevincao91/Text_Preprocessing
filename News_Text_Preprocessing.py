import time
import os
from settings import Settings
from preprocessing_chinese_text import PreprocessingChineseText
from preprocessing_english_text import PreprocessingEnglishText


def main(global_set):
    #  设置参数 ========================================================================================================
    print('Text Preprocessing Function Start.')
    string = '步骤 3:-> 原文生成简单文本'
    global_set.print_gui(string)
    # 计时
    fun_start_time = time.time()

    if not os.path.exists(global_set.text_c_dir_name):
        os.mkdir(global_set.text_c_dir_name)
    if not os.path.exists(global_set.text_e_dir_name):
        os.mkdir(global_set.text_e_dir_name)

    #  中文新闻网页文本预处理 ==========================================================================================
    print('Chinese News Text Preprocessing')
    string = '步骤 3-1:-> 中文新闻网页文本预处理'
    global_set.print_gui(string)
    preprocessing_c = PreprocessingChineseText(global_set.punctuation, global_set.stopwords_c)
    start_time = time.time()
    #  遍历中文文件夹下所有HTML文件 ===================================
    ori_dir_path = global_set.ori_text_c_dir_name
    tra_dir_path = global_set.text_c_dir_name
    for file in os.listdir(ori_dir_path):
        ori_file_path = os.path.join(ori_dir_path, file)
        tra_file_path = os.path.join(tra_dir_path, file)
        #  显示开始抓取信息
        print('get file: ' + ori_file_path + ' ============> saving simple text to: ' + tra_file_path)
        string = '=====:-> 解析新闻原文： ' + ori_file_path + ' 提取新闻词条到： ' + tra_file_path
        global_set.print_gui(string)
        #  抓取信息 & 处理信息
        preprocessing_c.get_news_text_info(ori_file_path, tra_file_path)
    #  显示结束信息  ======================================
    end_time = time.time()
    print('Function Finished! in ' + str(end_time - start_time) + 's')
    string = '=====:-> 处理完毕！ 用时： ' + str(round(end_time - start_time, 2)) + '秒'
    global_set.print_gui(string)
    print(str(global_set.news_max_num) + ' news has been decode to simple txt files.')
    string = '=====:-> ' + str(global_set.news_max_num) + ' 个新闻文本已解析。'
    global_set.print_gui(string)

    #  英文新闻网页文本预处理 ==========================================================================================
    print('English News Text Preprocessing')
    string = '步骤 3-2:-> 英文新闻网页文本预处理'
    global_set.print_gui(string)
    preprocessing_e = PreprocessingEnglishText(global_set.punctuation, global_set.stopwords_e)
    start_time = time.time()
    #  遍历英文文件夹下所有HTML文件 ===================================
    ori_dir_path = global_set.ori_text_e_dir_name
    tra_dir_path = global_set.text_e_dir_name
    for file in os.listdir(ori_dir_path):
        ori_file_path = os.path.join(ori_dir_path, file)
        tra_file_path = os.path.join(tra_dir_path, file)
        #  显示开始抓取信息
        print('get file: ' + ori_file_path + ' ============> saving simple text to: ' + tra_file_path)
        string = '=====:-> 解析新闻原文： ' + ori_file_path + ' 提取新闻词条到： ' + tra_file_path
        global_set.print_gui(string)
        #  抓取信息 & 处理信息
        preprocessing_e.get_news_text_info(ori_file_path, tra_file_path)
    #  显示结束信息  ======================================
    end_time = time.time()
    print('Function Finished! in ' + str(end_time - start_time) + 's')
    string = '=====:-> 处理完毕！ 用时： ' + str(round(end_time - start_time, 2)) + '秒'
    global_set.print_gui(string)
    print(str(global_set.news_max_num) + ' news has been decode to txt files.')
    string = '=====:-> ' + str(global_set.news_max_num) + ' 个新闻文本已解析。'
    global_set.print_gui(string)

    # 模块结束信息
    fun_end_time = time.time()
    string = '步骤 3:-> 原文生成简单文本  成功完成！ 用时： ' + str(round(fun_end_time - fun_start_time, 2)) + '秒'
    global_set.print_gui(string)


if __name__ == '__main__':
    global_set = Settings()
    main(global_set)
