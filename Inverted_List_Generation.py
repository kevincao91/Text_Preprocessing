import time
import os
from settings import Settings
from inverted_list import InvertedList


def main(global_set):
    #  设置参数 ========================================================================================================
    print('Inverted List Generation Function Start.')
    string = '步骤 5:-> 由词袋变成倒排表'
    global_set.print_gui(string)
    # 计时
    fun_start_time = time.time()

    if not os.path.exists(global_set.sys_log_dir_name):
        os.mkdir(global_set.sys_log_dir_name)
    tra_dir_path = global_set.sys_log_dir_name
    tra_file_path = tra_dir_path + 'inverted_list_data.txt'

    #  中文新闻倒排表生成 ============================================================================================
    print('Chinese News Inverted List Generating')
    string = '步骤 5-1:-> 中文新闻倒排表生成'
    global_set.print_gui(string)
    inv_list = InvertedList()
    start_time = time.time()
    #  遍历中文文件夹下所有bow文件 ===================================
    ori_dir_path = global_set.bow_c_dir_name
    for file_name in os.listdir(ori_dir_path):
        ori_file_path = os.path.join(ori_dir_path, file_name)
        #  显示开始抓取信息
        print('get file: ' + ori_file_path + ' ============>  add to inverted list. ', end='')
        # print('\n')
        string = '=====:-> 获取新闻词袋： ' + ori_file_path + ' 加入到倒排表。 '
        global_set.print_gui(string)
        #  抓取信息 & 处理信息
        inv_list.add_info(ori_file_path, file_name)
        #  提示ok
        print(' Done!!!')
    # 显示中文倒排表
    for content in inv_list.inverted_list:
        print(content[0] + '->' + str(content[1]))
    #  显示结束信息  ======================================
    end_time = time.time()
    print('Function Finished! in ' + str(end_time - start_time) + 's')
    string = '=====:-> 处理完毕！ 用时： ' + str(round(end_time - start_time, 2)) + '秒'
    global_set.print_gui(string)
    print('Chinese news inverted list has been generate.')
    string = '=====:-> 中文新闻倒排表已生成。'
    global_set.print_gui(string)

    #  英文新闻网页文本预处理 ==========================================================================================
    print('English News Inverted List Generating')
    string = '步骤 5-2:-> 英文新闻倒排表生成'
    global_set.print_gui(string)
    start_time = time.time()
    #  遍历英文文件夹下所有bow文件 ===================================
    ori_dir_path = global_set.bow_e_dir_name
    for file_name in os.listdir(ori_dir_path):
        ori_file_path = os.path.join(ori_dir_path, file_name)
        #  显示开始抓取信息
        print('get file: ' + ori_file_path + ' ============>  add to inverted list. ', end='')
        # print('\n')
        string = '=====:-> 获取新闻词袋： ' + ori_file_path + ' 加入到倒排表。 '
        global_set.print_gui(string)
        #  抓取信息 & 处理信息
        inv_list.add_info(ori_file_path, file_name)
        #  提示ok
        print(' Done!!!')
    #  显示结束信息  ======================================
    end_time = time.time()
    print('Function Finished! in ' + str(end_time - start_time) + 's')
    string = '=====:-> 处理完毕！ 用时： ' + str(round(end_time - start_time, 2)) + '秒'
    global_set.print_gui(string)
    print('English news inverted list has been generate.')
    string = '=====:-> 英文新闻倒排表已生成。'
    global_set.print_gui(string)

    # 计算倒排表中所有词的idf ==========================================================================================
    string = '=====:-> 计算所有词的 idf ... ...'
    global_set.print_gui(string)
    start_time = time.time()
    # 计算 idf
    inv_list.cal_idf(global_set.news_max_num * 2)
    # 模块结束信息
    end_time = time.time()
    string = '=====:-> 计算所有词的 idf -> 完成！ 用时： ' + str(round(end_time - start_time, 2)) + '秒'
    global_set.print_gui(string)
    # 写最终倒排表 =====================================================================================================
    inv_list.write_txt(tra_file_path)
    string = '=====:-> 写最终倒排表。'
    global_set.print_gui(string)
    # 模块结束信息
    fun_end_time = time.time()
    string = '步骤 5:-> 由词袋变成倒排表 -> 完成！ 用时： ' + str(round(fun_end_time - fun_start_time, 2)) + '秒'
    global_set.print_gui(string)


if __name__ == '__main__':
    global_set = Settings()
    main(global_set)
