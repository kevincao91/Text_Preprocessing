import time
import os
from settings import Settings
from bag_of_word import BagOfWord
import shutil


def main(global_set):
    #  设置参数 ========================================================================================================
    print('BOW Generation Function Start.')
    string = '步骤 4:-> 简单文本生成词袋'
    global_set.print_gui(string)
    # 计时
    fun_start_time = time.time()

    if not os.path.exists(global_set.bow_c_dir_name):
        os.mkdir(global_set.bow_c_dir_name)
    if not os.path.exists(global_set.bow_e_dir_name):
        os.mkdir(global_set.bow_e_dir_name)
    if not os.path.exists(global_set.bow_all_dir_name):
        os.mkdir(global_set.bow_all_dir_name)

    #  中文新闻文本词袋生成 ============================================================================================
    print('Chinese News Text BOW Generating')
    string = '步骤 4-1:-> 中文新闻简单文本生成词袋'
    global_set.print_gui(string)
    bow = BagOfWord()
    start_time = time.time()
    #  遍历中文文件夹下所有HTML文件 ===================================
    ori_dir_path = global_set.text_c_dir_name
    tra_dir_path = global_set.bow_c_dir_name
    for file in os.listdir(ori_dir_path):
        ori_file_path = os.path.join(ori_dir_path, file)
        tra_file_path = os.path.join(tra_dir_path, file)
        #  显示开始抓取信息
        print('get file: ' + ori_file_path + ' ============>  decode to: ' + tra_file_path + '... ', end='')
        # print('\n')
        string = '=====:-> 获取简单文本： ' + ori_file_path + ' 提取词袋到： ' + tra_file_path
        global_set.print_gui(string)
        #  抓取信息 & 处理信息
        bow.convert_info(ori_file_path, tra_file_path)
        #  提示ok
        print(' Done!!!')
    #  显示结束信息  ======================================
    end_time = time.time()
    print('Function Finished! in ' + str(end_time - start_time) + 's')
    string = '=====:-> 处理完毕！ 用时： ' + str(round(end_time - start_time, 2)) + '秒'
    global_set.print_gui(string)
    print(str(global_set.news_max_num) + ' news files has been decode to bow files.')
    string = '=====:-> ' + str(global_set.news_max_num) + ' 个新闻文本词袋已生产。'
    global_set.print_gui(string)

    #  英文新闻网页文本预处理 ==========================================================================================
    print('English News Text BOW Generating')
    string = '步骤 4-2:-> 英文新闻简单文本生成词袋'
    global_set.print_gui(string)
    start_time = time.time()
    #  遍历中文文件夹下所有HTML文件 ===================================
    ori_dir_path = global_set.text_e_dir_name
    tra_dir_path = global_set.bow_e_dir_name
    for file in os.listdir(ori_dir_path):
        ori_file_path = os.path.join(ori_dir_path, file)
        tra_file_path = os.path.join(tra_dir_path, file)
        #  显示开始抓取信息
        print('get file: ' + ori_file_path + ' ============>  decode to: ' + tra_file_path + '... ', end='')
        # print('\n')
        string = '=====:-> 获取简单文本： ' + ori_file_path + ' 提取词袋到： ' + tra_file_path
        global_set.print_gui(string)
        #  抓取信息 & 处理信息
        bow.convert_info(ori_file_path, tra_file_path)
        #  提示ok
        print(' Done!!!')
    #  显示结束信息  ======================================
    end_time = time.time()
    print('Function Finished! in ' + str(end_time - start_time) + 's')
    string = '=====:-> 处理完毕！ 用时： ' + str(round(end_time - start_time, 2)) + '秒'
    global_set.print_gui(string)
    print(str(global_set.news_max_num) + ' news files has been decode to bow files.')
    string = '=====:-> ' + str(global_set.news_max_num) + ' 个新闻文本词袋已生产。'
    global_set.print_gui(string)

    # 为余弦距离功能拷贝所有词袋文档
    print('copy bow_file ...', end='')
    string = '=====:-> 复制所有词袋文件 ... ...'
    global_set.print_gui(string)
    start_time = time.time()
    #  遍历中文文件夹下所有词袋文本文件
    ori_dir_path = global_set.bow_c_dir_name
    tra_dir_path = global_set.bow_all_dir_name
    for file_name in os.listdir(ori_dir_path):
        ori_file_path = os.path.join(ori_dir_path, file_name)
        tra_file_path = os.path.join(tra_dir_path, file_name)
        shutil.copy(ori_file_path, tra_file_path)
    #  遍历英文文件夹下所有词袋文本文件
    ori_dir_path = global_set.bow_e_dir_name
    tra_dir_path = global_set.bow_all_dir_name
    for file_name in os.listdir(ori_dir_path):
        ori_file_path = os.path.join(ori_dir_path, file_name)
        tra_file_path = os.path.join(tra_dir_path, file_name)
        shutil.copy(ori_file_path, tra_file_path)
    print('finish!')
    end_time = time.time()
    string = '=====:-> 复制所有词袋文件  完成！ 用时： ' + str(round(end_time - start_time, 2)) + '秒'
    global_set.print_gui(string)

    # 模块结束信息
    fun_end_time = time.time()
    string = '步骤 4:-> 简单文本生成词袋  成功完成！ 用时： ' + str(round(fun_end_time - fun_start_time, 2)) + '秒'
    global_set.print_gui(string)


if __name__ == '__main__':
    global_set = Settings()
    main(global_set)
