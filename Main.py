import Web_News_Download
import News_Text_Grasping
import News_Text_Preprocessing
import BOW_Generation
import Inverted_List_Generation
import Search_Text_Preprocessing
from k_means_chinese_news import KMeansChineseNews
from k_means_english_news import KMeansEnglishNews
from cosine_distance import CosineDistance
from settings import Settings
import os
import tkinter
import tkinter.messagebox
import time


class AppGUI(object):
    def __init__(self):
        # 初始化参数
        self.global_set = Settings()
        # 创建主窗口,用于容纳其它组件
        self.root_window = tkinter.Tk()
        self.root_window.geometry("800x500")
        # 预定义显示对象
        self.display_info = None
        self.file_label_1 = None
        self.file_label_2 = None
        self.cos_dis_listbox_1 = None
        self.cos_dis_listbox_2 = None
        self.text_1 = None
        self.text_2 = None
        self.cos_dis_label = None
        self.search_text_entry = None
        self.search_listbox = None
        self.search_text_show = None
        self.k_means_c_class_listbox = None
        self.k_means_c_file_listbox = None
        self.k_means_c_text_show = None
        self.k_means_e_class_listbox = None
        self.k_means_e_file_listbox = None
        self.k_means_e_text_show = None
        # 预定义显示子窗口
        self.search_window = None
        self.cos_dis_window = None
        self.k_means_c_window = None
        self.k_means_e_window = None
        # 预定义类
        self.CDC = None
        self.k_means_c = None
        self.k_means_e = None
        # 运算变量
        self.word_list = []
        self.file_seq_list = []
        self.idf_list = []

    # root窗口布局
    def root_gui_arrange(self):
        # 给主窗口设置标题内容
        self.root_window.title("文本预处理-演示系统")
        # 创建一个回显列表
        self.display_info = tkinter.Listbox(self.root_window, width=50)
        self.global_set.display_info = self.display_info
        # 创建Scrollbar
        y_scrollbar = tkinter.Scrollbar(self.root_window)
        y_scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.display_info.config(yscrollcommand=y_scrollbar.set)
        y_scrollbar.config(command=self.display_info.yview)

        # 创建菜单项
        menu_bar = tkinter.Menu(self.root_window)
        # 下拉菜单1
        menu_c1 = tkinter.Menu(self.root_window, tearoff=0)
        # 添加的是下拉菜单的菜单项
        menu_c1.add_command(label='步骤 1:-> 下载最新新闻网页', command=self.file_step_1)
        menu_c1.add_command(label='步骤 2:-> 抓取网页新闻原文', command=self.file_step_2)
        menu_c1.add_command(label='步骤 3:-> 原文生成简单文本', command=self.file_step_3)
        menu_c1.add_command(label='步骤 4:-> 简单文本生成词袋', command=self.file_step_4)
        menu_c1.add_command(label='步骤 5:-> 由词袋变成倒排表', command=self.file_step_5)
        menu_c1.add_command(label='完整  :-> 一次性完成以上预处理', command=self.file_step_6)
        # 下拉菜单2
        menu_c2 = tkinter.Menu(self.root_window, tearoff=0)
        # 添加的是下拉菜单的菜单项
        menu_c2.add_command(label='功能 1:-> 搜索文档（对所有文档）', command=self.search_check)
        menu_c2.add_command(label='功能 2:-> 比较两文档之间的余弦距离（对所有文档）', command=self.cos_dis_check)
        menu_c2.add_command(label='功能 3:-> K-Means聚类（中文）', command=self.k_means_c_gui_arrange)
        menu_c2.add_command(label='功能 4:-> K-Means聚类（英文）', command=self.k_means_e_gui_arrange)
        # 下拉菜单3
        menu_c3 = tkinter.Menu(self.root_window, tearoff=0)
        for item in ['版权信息', '其他说明']:
            menu_c3.add_command(label=item)
        # 指明父菜单
        menu_bar.add_cascade(label="文件处理", menu=menu_c1)
        menu_bar.add_cascade(label="主要功能", menu=menu_c2)
        menu_bar.add_cascade(label="关于", menu=menu_c3)
        # 菜单实例应用到大窗口中
        self.root_window['menu'] = menu_bar
        # 信息显示框布局
        self.display_info.pack(expand='yes', fill='both')

    # 搜索窗口布局
    def search_gui_arrange(self):
        # 定义长在窗口上的搜索窗口
        self.search_window = tkinter.Toplevel(self.root_window)
        self.search_window.geometry('800x450')
        self.search_window.title('搜索文档')

        # 设定标签
        show_label_1 = tkinter.Label(self.search_window, text='搜索文档（对所有文档）')
        show_label_2 = tkinter.Label(self.search_window, text='请输入关键词：')
        show_label_3 = tkinter.Label(self.search_window, text='搜索结果：')
        show_label_4 = tkinter.Label(self.search_window, text='文档原文（双击列表框内文件名显示原文）：')
        # 设定输入框
        self.search_text_entry = tkinter.Entry(self.search_window)
        # 设定按钮
        button = tkinter.Button(self.search_window, text='搜索！', command=self.search_btn_fun)
        # 创建第一个Listbox
        self.search_listbox = tkinter.Listbox(self.search_window, height=20, width=25)
        # 创建匹配的Scrollbar
        y_scrollbar_1 = tkinter.Scrollbar(self.search_window)
        self.search_listbox.config(yscrollcommand=y_scrollbar_1.set)
        y_scrollbar_1.config(command=self.search_listbox.yview)
        # 绑定事件
        self.search_listbox.bind('<Double-Button-1>', self.search_listbox_click_fun)
        # 设定文本框
        self.search_text_show = tkinter.Text(self.search_window, height=20, width=80)
        # 创建匹配的Scrollbar
        y_scrollbar_2 = tkinter.Scrollbar(self.search_window)
        self.search_text_show.config(yscrollcommand=y_scrollbar_2.set)
        y_scrollbar_2.config(command=self.search_text_show.yview)

        # 布局
        # 第一行
        show_label_1.grid(row=0, column=3)
        # 第二行
        show_label_2.grid(row=1, column=0)
        self.search_text_entry.grid(row=1, column=1, columnspan=8, sticky=tkinter.E + tkinter.W)
        button.grid(row=1, column=9)
        # 第三行
        show_label_3.grid(row=2, column=0, sticky=tkinter.W)
        show_label_4.grid(row=2, column=3, sticky=tkinter.W)
        # 第四行
        self.search_listbox.grid(row=3, column=0, columnspan=2, sticky=tkinter.E + tkinter.W)
        y_scrollbar_1.grid(row=3, column=2, sticky=tkinter.N + tkinter.S + tkinter.W)
        self.search_text_show.grid(row=3, column=3, columnspan=7, sticky=tkinter.N + tkinter.S)
        y_scrollbar_2.grid(row=3, column=10, sticky=tkinter.N + tkinter.S + tkinter.W)

    # 余弦距离窗口布局
    def cos_dis_gui_arrange(self):
        # 定义长在窗口上的搜索窗口
        self.cos_dis_window = tkinter.Toplevel(self.root_window)
        self.cos_dis_window.geometry('800x500')
        self.cos_dis_window.title('余弦距离')
        #  获取Listbox内容，既新闻原文本列表，遍历新闻原文文件夹下所有TXT文件
        ori_dir_path = self.global_set.ori_text_all_dir_name
        file_list = os.listdir(ori_dir_path)

        # 设定标签
        show_label_1 = tkinter.Label(self.cos_dis_window, text='选择第一个文档：')
        self.file_label_1 = tkinter.Label(self.cos_dis_window, text='_____None_____')
        show_label_2 = tkinter.Label(self.cos_dis_window, text='选择第二个文档：')
        self.file_label_2 = tkinter.Label(self.cos_dis_window, text='_____None_____')
        show_label_3 = tkinter.Label(self.cos_dis_window, text='文档一原文（双击列表框内文件名显示原文）：')
        show_label_4 = tkinter.Label(self.cos_dis_window, text='文档二原文（双击列表框内文件名显示原文）：')
        self.cos_dis_label = tkinter.Label(self.cos_dis_window, text='NaN', bg='red', fg='blue')
        # 设定按钮
        button_1 = tkinter.Button(self.cos_dis_window, text='计算余弦距离', command=self.cos_dis_cal_fun)
        # 创建第一个Listbox
        self.cos_dis_listbox_1 = tkinter.Listbox(self.cos_dis_window)  # 将file_list的值赋给Listbox
        for item in file_list:
            self.cos_dis_listbox_1.insert('end', item)  # 从最后一个位置开始加入值
        # 创建匹配的Scrollbar
        y_scrollbar_1 = tkinter.Scrollbar(self.cos_dis_window)
        self.cos_dis_listbox_1.config(yscrollcommand=y_scrollbar_1.set)
        y_scrollbar_1.config(command=self.cos_dis_listbox_1.yview)
        # 绑定事件
        self.cos_dis_listbox_1.bind('<Double-Button-1>', self.cos_dis_listbox_btn_fun_1)
        # 创建第二个Listbox
        self.cos_dis_listbox_2 = tkinter.Listbox(self.cos_dis_window)  # 将file_list的值赋给Listbox
        for item in file_list:
            self.cos_dis_listbox_2.insert('end', item)  # 从最后一个位置开始加入值
        # 创建匹配的Scrollbar
        y_scrollbar_2 = tkinter.Scrollbar(self.cos_dis_window)
        self.cos_dis_listbox_2.config(yscrollcommand=y_scrollbar_2.set)
        y_scrollbar_2.config(command=self.cos_dis_listbox_2.yview)
        # 绑定事件
        self.cos_dis_listbox_2.bind('<Double-Button-1>', self.cos_dis_listbox_btn_fun_2)
        # 设定文本框1
        self.text_1 = tkinter.Text(self.cos_dis_window, height=15, width=80)
        # 创建匹配的Scrollbar
        y_scrollbar_3 = tkinter.Scrollbar(self.cos_dis_window)
        self.text_1.config(yscrollcommand=y_scrollbar_3.set)
        y_scrollbar_3.config(command=self.text_1.yview)
        # 设定文本框2
        self.text_2 = tkinter.Text(self.cos_dis_window, height=15, width=80)
        # 创建匹配的Scrollbar
        y_scrollbar_4 = tkinter.Scrollbar(self.cos_dis_window)
        self.text_2.config(yscrollcommand=y_scrollbar_4.set)
        y_scrollbar_4.config(command=self.text_2.yview)

        # 布局
        # 第一行
        show_label_1.grid(row=0, column=0, sticky=tkinter.W)
        self.file_label_1.grid(row=0, column=1, sticky=tkinter.W)
        show_label_3.grid(row=0, column=3, sticky=tkinter.W)
        # 第二行
        self.cos_dis_listbox_1.grid(row=1, column=0, columnspan=2, sticky=tkinter.E + tkinter.W)
        y_scrollbar_1.grid(row=1, column=2, sticky=tkinter.N + tkinter.S + tkinter.W)
        self.text_1.grid(row=1, column=3, columnspan=7, sticky=tkinter.NW)
        y_scrollbar_3.grid(row=1, column=10, sticky=tkinter.N + tkinter.S + tkinter.W)
        # 第三行
        show_label_2.grid(row=2, column=0, sticky=tkinter.W)
        self.file_label_2.grid(row=2, column=1, sticky=tkinter.W)
        show_label_4.grid(row=2, column=3, sticky=tkinter.W)
        # 第四行
        self.cos_dis_listbox_2.grid(row=3, column=0, columnspan=2, sticky=tkinter.E + tkinter.W)
        y_scrollbar_2.grid(row=3, column=2, sticky=tkinter.N + tkinter.S + tkinter.W)
        self.text_2.grid(row=3, column=3, columnspan=7, sticky=tkinter.NW)
        y_scrollbar_4.grid(row=3, column=10, sticky=tkinter.N + tkinter.S + tkinter.W)
        # 第五行
        button_1.grid(row=4, column=3, sticky=tkinter.W)
        self.cos_dis_label.grid(row=4, column=3)

    # K-Means 中文文档 窗口布局
    def k_means_c_gui_arrange(self):
        # 定义长在窗口上的搜索窗口
        self.k_means_c_window = tkinter.Toplevel(self.root_window)
        self.k_means_c_window.geometry('850x500')
        self.k_means_c_window.title('K-Means聚类（中文）')

        # 设定标签
        show_label_1 = tkinter.Label(self.k_means_c_window, text='聚类文档（中文文档）')
        show_label_2 = tkinter.Label(self.k_means_c_window, text='聚类结果（前三类）：')
        show_label_3 = tkinter.Label(self.k_means_c_window, text='类中的文件列表（按离质心距离排序）：')
        show_label_4 = tkinter.Label(self.k_means_c_window, text='文档原文（双击列表框内文件名显示原文）：')
        # 创建列表
        self.k_means_c_class_listbox = tkinter.Listbox(self.k_means_c_window, height=3, width=60)
        self.k_means_c_class_listbox.bind('<Double-Button-1>', self.k_means_c_class_listbox_click_fun)  # 绑定事件
        # 设定按钮
        button = tkinter.Button(self.k_means_c_window, text='点击开始聚类！', command=self.k_means_c_btn_fun)
        # 创建第一个Listbox
        self.k_means_c_file_listbox = tkinter.Listbox(self.k_means_c_window, height=20, width=25)
        # 创建匹配的Scrollbar
        y_scrollbar_1 = tkinter.Scrollbar(self.k_means_c_window)
        self.k_means_c_file_listbox.config(yscrollcommand=y_scrollbar_1.set)
        y_scrollbar_1.config(command=self.k_means_c_file_listbox.yview)
        # 绑定事件
        self.k_means_c_file_listbox.bind('<Double-Button-1>', self.k_means_c_file_listbox_click_fun)
        # 设定文本框
        self.k_means_c_text_show = tkinter.Text(self.k_means_c_window, height=20, width=80)
        # 创建匹配的Scrollbar
        y_scrollbar_2 = tkinter.Scrollbar(self.k_means_c_window)
        self.k_means_c_text_show.config(yscrollcommand=y_scrollbar_2.set)
        y_scrollbar_2.config(command=self.k_means_c_text_show.yview)

        # 布局
        # 第一行
        show_label_1.grid(row=0, column=3)
        # 第二行
        show_label_2.grid(row=1, column=0, sticky=tkinter.W)
        self.k_means_c_class_listbox.grid(row=1, column=1, columnspan=8, sticky=tkinter.W + tkinter.E)
        button.grid(row=1, column=9)
        # 第三行
        show_label_3.grid(row=2, column=0, sticky=tkinter.W)
        show_label_4.grid(row=2, column=3, sticky=tkinter.W)
        # 第四行
        self.k_means_c_file_listbox.grid(row=3, column=0, columnspan=2, sticky=tkinter.E + tkinter.W)
        y_scrollbar_1.grid(row=3, column=2, sticky=tkinter.N + tkinter.S + tkinter.W)
        self.k_means_c_text_show.grid(row=3, column=3, columnspan=7, sticky=tkinter.N + tkinter.S)
        y_scrollbar_2.grid(row=3, column=10, sticky=tkinter.N + tkinter.S + tkinter.W)

    # K-Means 英文文档 窗口布局
    def k_means_e_gui_arrange(self):
        # 定义长在窗口上的搜索窗口
        self.k_means_e_window = tkinter.Toplevel(self.root_window)
        self.k_means_e_window.geometry('850x500')
        self.k_means_e_window.title('K-Means聚类（英文）')

        # 设定标签
        show_label_1 = tkinter.Label(self.k_means_e_window, text='聚类文档（英文文档）')
        show_label_2 = tkinter.Label(self.k_means_e_window, text='聚类结果（前三类）：')
        show_label_3 = tkinter.Label(self.k_means_e_window, text='类中的文件列表（按离质心距离排序）：')
        show_label_4 = tkinter.Label(self.k_means_e_window, text='文档原文（双击列表框内文件名显示原文）：')
        # 创建列表
        self.k_means_e_class_listbox = tkinter.Listbox(self.k_means_e_window, height=3, width=60)
        self.k_means_e_class_listbox.bind('<Double-Button-1>', self.k_means_e_class_listbox_click_fun)  # 绑定事件
        # 设定按钮
        button = tkinter.Button(self.k_means_e_window, text='点击开始聚类！', command=self.k_means_e_btn_fun)
        # 创建第一个Listbox
        self.k_means_e_file_listbox = tkinter.Listbox(self.k_means_e_window, height=20, width=25)
        # 创建匹配的Scrollbar
        y_scrollbar_1 = tkinter.Scrollbar(self.k_means_e_window)
        self.k_means_e_file_listbox.config(yscrollcommand=y_scrollbar_1.set)
        y_scrollbar_1.config(command=self.k_means_e_file_listbox.yview)
        # 绑定事件
        self.k_means_e_file_listbox.bind('<Double-Button-1>', self.k_means_e_file_listbox_click_fun)
        # 设定文本框
        self.k_means_e_text_show = tkinter.Text(self.k_means_e_window, height=20, width=80)
        # 创建匹配的Scrollbar
        y_scrollbar_2 = tkinter.Scrollbar(self.k_means_e_window)
        self.k_means_e_text_show.config(yscrollcommand=y_scrollbar_2.set)
        y_scrollbar_2.config(command=self.k_means_e_text_show.yview)

        # 布局
        # 第一行
        show_label_1.grid(row=0, column=3)
        # 第二行
        show_label_2.grid(row=1, column=0)
        self.k_means_e_class_listbox.grid(row=1, column=1, columnspan=8, sticky=tkinter.E + tkinter.W)
        button.grid(row=1, column=9)
        # 第三行
        show_label_3.grid(row=2, column=0, sticky=tkinter.W)
        show_label_4.grid(row=2, column=3, sticky=tkinter.W)
        # 第四行
        self.k_means_e_file_listbox.grid(row=3, column=0, columnspan=2, sticky=tkinter.E + tkinter.W)
        y_scrollbar_1.grid(row=3, column=2, sticky=tkinter.N + tkinter.S + tkinter.W)
        self.k_means_e_text_show.grid(row=3, column=3, columnspan=7, sticky=tkinter.N + tkinter.S)
        y_scrollbar_2.grid(row=3, column=10, sticky=tkinter.N + tkinter.S + tkinter.W)

    # 搜索前提条件检查
    def search_check(self):
        # 检查新闻原文文件是否存在
        file_list = []
        file_path = os.path.join(self.global_set.sys_log_dir_name, 'inverted_list_data.txt')
        #  遍历新闻原文文件夹下所有TXT文件
        ori_dir_path = self.global_set.ori_text_all_dir_name
        try:
            file_list = os.listdir(ori_dir_path)
        except FileNotFoundError:
            print('has no ori_dir!')
            string = '请先完成文本处理！'
            self.global_set.print_gui(string)
            tkinter.messagebox.showwarning(title='注意', message=string, parent=self.root_window)  # 提出警告对话窗
        if file_list is None:
            print('has no ori_file!')
            string = '请先完成文本处理！'
            self.global_set.print_gui(string)
            tkinter.messagebox.showwarning(title='注意', message=string, parent=self.root_window)  # 提出警告对话窗
        # 判断倒排表是否存在
        elif os.path.exists(file_path):
            self.search_data_initial_fun(file_path)
            print('entry search function!')
            string = '进入全文搜索功能！'
            self.global_set.print_gui(string)
            # 布置余弦距离界面
            self.search_gui_arrange()
        else:
            print('has no inverted_list_data.txt!')
            string = '缺少倒排表，请先完成文本处理！'
            self.global_set.print_gui(string)
            tkinter.messagebox.showwarning(title='注意', message=string, parent=self.root_window)  # 提出警告对话窗

    # 余弦距离前提条件检查
    def cos_dis_check(self):
        # 检查新闻原文文件是否存在
        file_list = []
        file_path = os.path.join(self.global_set.sys_log_dir_name, 'inverted_list_data.txt')
        #  遍历新闻原文文件夹下所有TXT文件
        ori_dir_path = self.global_set.ori_text_all_dir_name
        try:
            file_list = os.listdir(ori_dir_path)
        except FileNotFoundError:
            print('has no ori_dir!')
            string = '请先完成文本处理！'
            self.global_set.print_gui(string)
            tkinter.messagebox.showwarning(title='注意', message=string, parent=self.root_window)  # 提出警告对话窗
        if file_list is None:
            print('has no ori_file!')
            string = '请先完成文本处理！'
            self.global_set.print_gui(string)
            tkinter.messagebox.showwarning(title='注意', message=string, parent=self.root_window)  # 提出警告对话窗
        # 判断倒排表是否存在
        elif os.path.exists(file_path):
            self.search_data_initial_fun(file_path)
            print('entry cos_dis function!')
            string = '进入余弦距离计算功能！'
            self.global_set.print_gui(string)
            # 布置余弦距离界面
            self.cos_dis_gui_arrange()
        else:
            print('has no inverted_list_data.txt!')
            string = '缺少倒排表，请先完成文本处理！'
            self.global_set.print_gui(string)
            tkinter.messagebox.showwarning(title='注意', message=string, parent=self.root_window)  # 提出警告对话窗

    # 搜索界面/余弦距离 - 搜索功能数据初始化功能
    def search_data_initial_fun(self, file_path):
        # 初始化数据
        self.word_list = []
        self.idf_list = []
        self.file_seq_list = []
        # 获取倒排表
        with open(file_path, 'rb') as f:
            #   写文件用bytes而不是str，所以要转码
            text = f.read().decode('utf-8', 'ignore')
            lines = text.splitlines()  # 读取全部内容 ，并以列表方式返回
        for line in lines:
            word, idf, str_file_seq = line.split(' ', 2)
            self.word_list.append(word)
            self.idf_list.append(float(idf))
            file_seq = str_file_seq.split()
            self.file_seq_list.append(file_seq)
        # 定义余弦距离计算类
        self.CDC = CosineDistance(self.global_set, self.word_list, self.idf_list, self.file_seq_list)
        # 显示
        print('inverted_list_data get!')
        string = '搜索功能数据初始化成功！'
        self.global_set.print_gui(string)

    # 搜索界面 - 搜索功能
    def search_btn_fun(self):
        # 清空显示
        self.search_text_show.delete('1.0', 'end')
        self.search_listbox.delete(0, 'end')
        # 计时
        start_time = time.time()
        # 获取用户输入
        search_str = self.search_text_entry.get()
        # 是否有值
        if search_str:
            print('get user input string --> ' + search_str)
            string = '搜索文本：' + search_str
            self.global_set.print_gui(string)
            # 搜索文本预处理
            key_word_list, key_tf_list = Search_Text_Preprocessing.main(self.global_set, search_str)
            string = '分解成关键字：' + str(key_word_list)
            self.global_set.print_gui(string)
            # 倒排表多个关键词查询得到对应多个文件序列
            file_seq_list = []
            for key_word in key_word_list:
                if key_word in self.word_list:
                    index = self.word_list.index(key_word)
                    file_seq = self.file_seq_list[index]
                else:
                    # 对于没有查到的文件序列取空
                    file_seq = []
                file_seq_list.append(file_seq)
            # 对文件序列取交集,得到最终包含搜索词的所有文件列表
            if len(file_seq_list) == 0:
                search_find_file_list = []
            elif len(file_seq_list) == 1:
                search_find_file_list = file_seq_list[0]
            else:
                for index in range(len(file_seq_list) - 1):
                    file_seq_list[index + 1] = list(
                        set(file_seq_list[index + 1]).intersection(set(file_seq_list[index])))
                search_find_file_list = file_seq_list[-1]
            print('未排序文件列表：' + str(search_find_file_list))
            # 计算余弦距离，通过结果排序搜索结果
            sort_search_find_file_list = []
            for find_file in search_find_file_list:
                cos_dis = self.CDC.search_doc_cos_dis_cal(key_word_list, key_tf_list, find_file)
                sort_search_find_file_list.append((cos_dis, find_file))
            # 按 cos_dis 倒排
            sort_search_find_file_list.sort(reverse=True)
            # 取最后结果
            search_find_final_file_list = []
            for item in sort_search_find_file_list:
                cos_dis = round(item[0], 2)
                find_file = item[1]
                search_find_final_file_list.append('相似度:' + str(cos_dis) + '->' + find_file)
            print('已排序文件列表：' + str(search_find_final_file_list))
            # 显示结果
            self.search_listbox.delete(0, 'end')
            if search_find_final_file_list:
                # 添加到listbox
                for find_file in search_find_final_file_list:
                    self.search_listbox.insert('end', find_file)
                    # 选中第一项
                self.search_listbox.select_set(0)
                # 添加到text
                listbox_str = self.search_listbox.get(self.search_listbox.curselection())
                file_name = listbox_str.split('>')[1]
                self.search_text_show.delete('1.0', 'end')
                self.search_text_show.insert('insert', self.get_txt(file_name))
                # 结束计时
                end_time = time.time()
                # 显示到控制台
                print('file find! in ' + str(round(end_time - start_time, 2)) + 's')
                string = '共找到' + str(len(search_find_final_file_list)) + '篇相关文档！用时： ' \
                         + str(round(end_time - start_time, 2)) + '秒'
                self.global_set.print_gui(string)
                tkinter.messagebox.showwarning(title='注意', message=string, parent=self.search_window)  # 提出警告对话窗
            else:
                print('no file find!')
                string = '未找到相关文档！'
                self.global_set.print_gui(string)
                tkinter.messagebox.showwarning(title='注意', message='未找到相关文档！', parent=self.search_window)  # 提出警告对话窗
        else:
            print('no input!')
            string = '未输入查询内容！'
            self.global_set.print_gui(string)
            tkinter.messagebox.showwarning(title='注意', message='请输入查询内容！', parent=self.search_window)  # 提出警告对话窗
        pass

    # 搜索界面 - 列表框双击功能
    def search_listbox_click_fun(self, event):
        listbox_str = self.search_listbox.get(self.search_listbox.curselection())
        file_name = listbox_str.split('>')[1]
        self.search_text_show.delete('1.0', 'end')
        self.search_text_show.insert('insert', self.get_txt(file_name))
        pass

    # 计算余弦距离界面 - 计算余弦距离
    def cos_dis_cal_fun(self):
        if self.file_label_1.cget("text") == '_____None_____' or self.file_label_2.cget("text") == '_____None_____':
            print('no file has been selected!')
            string = '请先选择文件！'
            self.global_set.print_gui(string)
            tkinter.messagebox.showwarning(title='注意', message='请先选择文件！', parent=self.cos_dis_window)  # 提出警告对话窗
        else:
            file_name_1 = self.file_label_1.cget("text")
            file_name_2 = self.file_label_2.cget("text")
            cos_dis = self.CDC.doc_doc_cos_dis_cal(file_name_1, file_name_2)
            self.cos_dis_label.config(text=str(cos_dis))
            self.cos_dis_label.update()
        pass

    # K_Means 中文文档 界面 - 聚类功能
    def k_means_c_btn_fun(self):
        self.k_means_c = KMeansChineseNews(self.global_set)
        self.k_means_c.k_means_cal()
        # 取前三个大类 加入类列表
        self.k_means_c_class_listbox.delete(0, 'end')
        for index in range(3):
            class_label = self.k_means_c.class_file_seq_list[index][0]
            # 取类对应特征词前8个
            class_feature_word = self.k_means_c.class_word_seq_list[class_label][1][0:8]
            class_listbox_str = '类序号:' + str(class_label) + ' > 类特征词:' + str(class_feature_word)
            self.k_means_c_class_listbox.insert('end', class_listbox_str)
        # 类列表 默认选第一类
        class_label = 0
        self.k_means_c_class_listbox.select_set(class_label)
        self.k_means_c_file_listbox.delete(0, 'end')
        # 取类中所有文件 加入文件列表
        for file_index in self.k_means_c.class_file_seq_list[class_label][1]:
            file_name = 'News_' + str(file_index + 1) + '_C.txt'
            self.k_means_c_file_listbox.insert('end', file_name)
        # 文件列表 默认选第一个
        file_index = 0
        self.k_means_c_file_listbox.select_set(file_index)
        # 取文件内容
        file_name = self.k_means_c_file_listbox.get(0)
        print('default file selected: ' + file_name)
        self.k_means_c_text_show.delete('1.0', 'end')
        self.k_means_c_text_show.insert('insert', self.get_txt(file_name))

    # K_Means 中文文档 界面 - 类点击功能
    def k_means_c_class_listbox_click_fun(self, event):
        # 添加到k_means_c_file_listbox
        class_label = self.k_means_c_class_listbox.curselection()[0]
        self.k_means_c_file_listbox.delete(0, 'end')
        # 取类中所有文件 加入列表
        for file_index in self.k_means_c.class_file_seq_list[class_label][1]:
            file_name = 'News_' + str(file_index + 1) + '_C.txt'
            self.k_means_c_file_listbox.insert('end', file_name)
        # 文件列表 默认选第一个
        file_index = 0
        self.k_means_c_file_listbox.select_set(file_index)
        # 取文件内容
        file_name = self.k_means_c_file_listbox.get(0)
        print('default file selected: ' + file_name)
        self.k_means_c_text_show.delete('1.0', 'end')
        self.k_means_c_text_show.insert('insert', self.get_txt(file_name))

    # K_Means 中文文档 界面 - 文件点击功能
    def k_means_c_file_listbox_click_fun(self, event):
        file_name = self.k_means_c_file_listbox.get(self.k_means_c_file_listbox.curselection())
        print('user file selected: ' + file_name)
        self.k_means_c_text_show.delete('1.0', 'end')
        self.k_means_c_text_show.insert('insert', self.get_txt(file_name))
        pass

    # K_Means 英文文档 界面 - 聚类功能
    def k_means_e_btn_fun(self):
        self.k_means_e = KMeansEnglishNews(self.global_set)
        self.k_means_e.k_means_cal()
        # 取前三个大类 加入类列表
        self.k_means_e_class_listbox.delete(0, 'end')
        for index in range(3):
            class_label = self.k_means_e.class_file_seq_list[index][0]
            # 取类对应特征词前8个
            class_feature_word = self.k_means_e.class_word_seq_list[class_label][1][0:8]
            class_listbox_str = str(class_label) + ' > ' + str(class_feature_word)
            self.k_means_e_class_listbox.insert('end', class_listbox_str)
        # 类列表 默认选第一类
        class_label = 0
        self.k_means_e_class_listbox.select_set(class_label)
        self.k_means_e_file_listbox.delete(0, 'end')
        # 取类中所有文件 加入文件列表
        for file_index in self.k_means_e.class_file_seq_list[class_label][1]:
            file_name = 'News_' + str(file_index + 1) + '_E.txt'
            self.k_means_e_file_listbox.insert('end', file_name)
        # 文件列表 默认选第一个
        file_index = 0
        self.k_means_e_file_listbox.select_set(file_index)
        # 取文件内容
        file_name = self.k_means_e_file_listbox.get(0)
        print('default file selected: ' + file_name)
        self.k_means_e_text_show.delete('1.0', 'end')
        self.k_means_e_text_show.insert('insert', self.get_txt(file_name))

    # K_Means 英文文档 界面 - 类点击功能
    def k_means_e_class_listbox_click_fun(self, event):
        # 添加到k_means_e_file_listbox
        class_label = self.k_means_e_class_listbox.curselection()[0]
        self.k_means_e_file_listbox.delete(0, 'end')
        # 取类中所有文件 加入列表
        for file_index in self.k_means_e.class_file_seq_list[class_label][1]:
            file_name = 'News_' + str(file_index + 1) + '_E.txt'
            self.k_means_e_file_listbox.insert('end', file_name)
        # 文件列表 默认选第一个
        file_index = 0
        self.k_means_e_file_listbox.select_set(file_index)
        # 取文件内容
        file_name = self.k_means_e_file_listbox.get(0)
        print('default file selected: ' + file_name)
        self.k_means_e_text_show.delete('1.0', 'end')
        self.k_means_e_text_show.insert('insert', self.get_txt(file_name))

    # K_Means 英文文档 界面 - 文件点击功能
    def k_means_e_file_listbox_click_fun(self, event):
        file_name = self.k_means_e_file_listbox.get(self.k_means_e_file_listbox.curselection())
        print('user file selected: ' + file_name)
        self.k_means_e_text_show.delete('1.0', 'end')
        self.k_means_e_text_show.insert('insert', self.get_txt(file_name))
        pass

    # 通用功能 - 提取原文文本
    def get_txt(self, file_name):
        ori_txt = '_____None_____'
        if file_name:
            ori_file_path = os.path.join(self.global_set.ori_text_all_dir_name, file_name)
            with open(ori_file_path, 'rb') as f:
                #   写文件用bytes而不是str，所以要转码
                ori_txt = f.read().decode('utf-8', 'ignore')
        return ori_txt

    # 计算余弦距离界面 - 列表框双击功能1
    def cos_dis_listbox_btn_fun_1(self, event):
        file_name = self.cos_dis_listbox_1.get(self.cos_dis_listbox_1.curselection())
        print('file 1 selected: ' + file_name)
        self.file_label_1.config(text=file_name)
        self.file_label_1.update()
        self.text_1.delete('1.0', 'end')
        self.text_1.insert('insert', self.get_txt(file_name))
        pass

    # 计算余弦距离界面 - 列表框双击功能2
    def cos_dis_listbox_btn_fun_2(self, event):
        file_name = self.cos_dis_listbox_2.get(self.cos_dis_listbox_2.curselection())
        print('file 2 selected: ' + file_name)
        self.file_label_2.config(text=file_name)
        self.file_label_2.update()
        self.text_2.delete('1.0', 'end')
        self.text_2.insert('insert', self.get_txt(file_name))
        pass

    # Step 1:-> 下载最新新闻网页
    def file_step_1(self):
        Web_News_Download.main(self.global_set)

    # Step 2:-> 网页生成简单文本
    def file_step_2(self):
        News_Text_Grasping.main(self.global_set)

    # Step 2:-> 网页生成简单文本
    def file_step_3(self):
        News_Text_Preprocessing.main(self.global_set)

    # Step 3:-> 简单文本生成词袋
    def file_step_4(self):
        BOW_Generation.main(self.global_set)

    # Step 4:-> 由词袋变成倒排表
    def file_step_5(self):
        Inverted_List_Generation.main(self.global_set)

    # All in one:-> 一次性完成以上预处理
    def file_step_6(self):
        Web_News_Download.main(self.global_set)
        News_Text_Grasping.main(self.global_set)
        News_Text_Preprocessing.main(self.global_set)
        BOW_Generation.main(self.global_set)
        Inverted_List_Generation.main(self.global_set)


def main():
    # 初始化对象
    app = AppGUI()
    # 进行布局
    app.root_gui_arrange()
    # 程序自检
    app.global_set.sys_log_check()
    # 主程序执行
    tkinter.mainloop()


if __name__ == "__main__":
    main()
