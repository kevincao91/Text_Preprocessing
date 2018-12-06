import time
import os
import shutil
from settings import Settings
from grasping_chinese_text import GraspingChineseText
from grasping_english_text import GraspingEnglishText


def main(global_set):
    #  设置参数 ========================================================================================================
    print('Text Grasping Function Start.')
    string = '步骤 2:-> 抓取网页新闻原文'
    global_set.print_gui(string)
    # 计时
    fun_start_time = time.time()

    if not os.path.exists(global_set.ori_text_c_dir_name):
        os.mkdir(global_set.ori_text_c_dir_name)
    if not os.path.exists(global_set.ori_text_e_dir_name):
        os.mkdir(global_set.ori_text_e_dir_name)
    if not os.path.exists(global_set.ori_text_all_dir_name):
        os.mkdir(global_set.ori_text_all_dir_name)

    #  中文新闻网页文本抓取 ============================================================================================
    print('Chinese News Text Grasping')
    string = '步骤 2-1:-> 中文新闻网页原文抓取'
    global_set.print_gui(string)
    grasping_c = GraspingChineseText()
    start_time = time.time()
    #  遍历中文文件夹下所有HTML文件 ===================================
    html_dir_path = global_set.html_c_dir_name
    ori_dir_path = global_set.ori_text_c_dir_name
    for file in os.listdir(html_dir_path):
        html_file_path = os.path.join(html_dir_path, file)
        ori_file_path = os.path.join(ori_dir_path, file[:-4] + 'txt')
        #  显示开始抓取信息
        print('get file: ' + html_file_path + ' ============> saving news text to: ' + ori_file_path + ' ... ', end='')
        # print('\n')
        string = '=====:-> 解析新闻网页： ' + html_file_path + ' 提取新闻文本到： ' + ori_file_path
        global_set.print_gui(string)
        #  抓取信息 & 处理信息
        grasping_c.get_news_text_info(html_file_path, ori_file_path)
        # 提示OK
        print('Done!')
    #  显示结束信息  ======================================
    end_time = time.time()
    print('Function Finished! in ' + str(end_time - start_time) + 's')
    string = '=====:-> 处理完毕！ 用时： ' + str(round(end_time - start_time, 2)) + '秒'
    global_set.print_gui(string)
    print(str(global_set.news_max_num) + ' html files has been decode to txt files.')
    string = '=====:-> ' + str(global_set.news_max_num) + ' 个新闻文本原文已抓取。'
    global_set.print_gui(string)

    #  英文新闻网页文本预处理 ==========================================================================================
    print('English News Text Grasping')
    string = '步骤 2-2:-> 英文新闻网页原文抓取'
    global_set.print_gui(string)
    grasping_e = GraspingEnglishText()
    start_time = time.time()
    #  遍历中文文件夹下所有HTML文件 ===================================
    html_dir_path = global_set.html_e_dir_name
    ori_dir_path = global_set.ori_text_e_dir_name
    for file in os.listdir(html_dir_path):
        html_file_path = os.path.join(html_dir_path, file)
        ori_file_path = os.path.join(ori_dir_path, file[:-4] + 'txt')
        #  显示开始抓取信息
        print('get file: ' + html_file_path + ' ============> saving news text to: ' + ori_file_path + ' ... ', end='')
        # print('\n')
        string = '=====:-> 解析新闻网页： ' + html_file_path + ' 提取新闻文本到： ' + ori_file_path
        global_set.print_gui(string)
        #  抓取信息 & 处理信息
        grasping_e.get_news_text_info(html_file_path, ori_file_path)
        # 提示OK
        print('Done!')
    #  显示结束信息  ======================================
    end_time = time.time()
    print('Function Finished! in ' + str(end_time - start_time) + 's')
    string = '=====:-> 处理完毕！ 用时： ' + str(round(end_time - start_time, 2)) + '秒'
    global_set.print_gui(string)
    print(str(global_set.news_max_num) + ' html files has been decode to txt files.')
    string = '=====:-> ' + str(global_set.news_max_num) + ' 个新闻文本原文已抓取。'
    global_set.print_gui(string)

    # 为搜索、余弦距离、聚类功能拷贝所有原始文档
    print('copy ori_file ...', end='')
    string = '=====:-> 复制所有原文文件 ... ...'
    global_set.print_gui(string)
    start_time = time.time()
    #  遍历中文文件夹下所有原文文本文件
    ori_dir_path = global_set.ori_text_c_dir_name
    tra_dir_path = global_set.ori_text_all_dir_name
    for file_name in os.listdir(ori_dir_path):
        ori_file_path = os.path.join(ori_dir_path, file_name)
        tra_file_path = os.path.join(tra_dir_path, file_name)
        shutil.copy(ori_file_path, tra_file_path)
    #  遍历英文文件夹下所有原文文本文件
    ori_dir_path = global_set.ori_text_e_dir_name
    tra_dir_path = global_set.ori_text_all_dir_name
    for file_name in os.listdir(ori_dir_path):
        ori_file_path = os.path.join(ori_dir_path, file_name)
        tra_file_path = os.path.join(tra_dir_path, file_name)
        shutil.copy(ori_file_path, tra_file_path)
    print('finish!')
    end_time = time.time()
    string = '=====:-> 复制所有原文文件  完成！ 用时： ' + str(round(end_time - start_time, 2)) + '秒'
    global_set.print_gui(string)

    # 模块结束信息
    fun_end_time = time.time()
    string = '步骤 2:-> 抓取网页新闻原文  成功完成！ 用时： ' + str(round(fun_end_time - fun_start_time, 2)) + '秒'
    global_set.print_gui(string)


if __name__ == '__main__':
    global_set = Settings()
    main(global_set)
