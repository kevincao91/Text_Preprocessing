import tkinter
import tkinter.messagebox
import os
import sys


class Settings:
    # 配置程序所有的设置数据
    def __init__(self):
        #  初始化程序的设置
        self.display_info = None
        self.display_index = 0
        # 目标网址设置
        self.news_c_start_url = 'http://news.ifeng.com/listpage/11502/20181205/1/rtlist.shtml'  # 凤凰网资讯 > 即时新闻
        self.news_e_start_url_list = ['http://www.globaltimes.cn/china/',
                                      'http://www.globaltimes.cn/business/',
                                      'http://www.globaltimes.cn/world/',
                                      'http://www.globaltimes.cn/opinion/']  # GlobalTimes
        # 系统文件夹设置
        self.sys_log_dir_name = 'Log/'
        self.html_c_dir_name = 'News_Chinese_HTML/'
        self.html_e_dir_name = 'News_English_HTML/'
        self.ori_text_c_dir_name = 'News_Chinese_Original_Text/'
        self.ori_text_e_dir_name = 'News_English_Original_Text/'
        self.ori_text_all_dir_name = 'News_All_Original_Text/'
        self.text_c_dir_name = 'News_Chinese_Processed_Text/'
        self.text_e_dir_name = 'News_English_Processed_Text/'
        self.bow_c_dir_name = 'News_Chinese_BOW_Text/'
        self.bow_e_dir_name = 'News_English_BOW_Text/'
        self.bow_all_dir_name = 'News_All_BOW_Text/'
        # 目标文章数目
        self.news_max_num = 500
        self.news_c_now_num = 0
        self.news_e_now_num = 0
        self.class_num = 20
        # 运行变量
        self.download_c_news_url_list = []
        self.download_e_news_url_list = []
        # 标点、停用词变量
        self.punctuation = []
        self.stopwords_c = []
        self.stopwords_e = []

    # 获取标点符号
    def get_punctuation(self):
        with open('Log/punctuation.txt', encoding='utf-8') as file:  # 这是标点符号集
            punctuation = []
            for line in file:
                word = line.strip('\r\n')  # 除去换行符，注意是\r\n
                punctuation.append(word)
            self.punctuation = punctuation

    # 获取停用词
    def get_stopwords(self):
        with open('Log/stopwords_c.txt', "r") as file:  # 这是中文stopwords集
            stopwords_c = []
            for line in file:
                word = line.strip('\r\n')  # 除去换行符，注意是\r\n
                stopwords_c.append(word)
            self.stopwords_c = stopwords_c
        with open('Log/stopwords_e.txt', "r") as file:  # 这是英文stopwords集
            stopwords_e = []
            for line in file:
                word = line.strip('\r\n')  # 除去换行符，注意是\r\n
                stopwords_e.append(word)
            self.stopwords_e = stopwords_e

    # GUI上显示的滚动行
    def print_gui(self, string):
        self.display_info.insert(self.display_index, string)
        self.display_info.see(self.display_index)
        self.display_info.select_clear(0, 'end')
        self.display_info.select_set(self.display_index)
        self.display_info.update()
        self.display_index += 1

    # 前提条件检查
    def sys_log_check(self):
        # 显示信息
        string = '系统自检中 ... ...'
        self.print_gui(string)
        # 判断各类表是否存在
        file_path_1 = 'Log/stopwords_c.txt'
        file_path_2 = 'Log/stopwords_e.txt'
        file_path_3 = 'Log/punctuation.txt'
        if os.path.exists(file_path_1):
            pass
        else:
            print('have no ' + file_path_1 + '!')
            string = '缺失文件：' + file_path_1
            self.print_gui(string)
            tkinter.messagebox.showerror(title='错误', message=string)  # 提出错误对话窗
            sys.exit()

        if os.path.exists(file_path_2):
            pass
        else:
            print('have no ' + file_path_1 + '!')
            string = '缺失文件：' + file_path_2
            self.print_gui(string)
            tkinter.messagebox.showerror(title='错误', message=string)  # 提出错误对话窗
            sys.exit()

        if os.path.exists(file_path_3):
            pass
        else:
            print('have no ' + file_path_1 + '!')
            string = '缺失文件：' + file_path_3
            self.print_gui(string)
            tkinter.messagebox.showerror(title='错误', message=string)  # 提出错误对话窗
            sys.exit()
        # 自检完成，读取各类表
        self.get_punctuation()
        self.get_stopwords()
        # 显示信息
        string = '系统自检成功，载入数据完成！'
        self.print_gui(string)
