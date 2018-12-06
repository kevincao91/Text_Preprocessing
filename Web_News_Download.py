import time
import os
import requests
from settings import Settings
from crawler_news_ifeng_com import CrawlerForNewsIfengCom
from crawler_global_times_cn import CrawlerForGlobalTimesCn


def main(global_set):
    #  设置参数 ========================================================================================================
    print('Web News Download Function Start.')
    string = '步骤 1:-> 下载最新新闻网页'
    global_set.print_gui(string)
    # 计时
    fun_start_time = time.time()

    if not os.path.exists(global_set.html_c_dir_name):
        os.mkdir(global_set.html_c_dir_name)
    if not os.path.exists(global_set.html_e_dir_name):
        os.mkdir(global_set.html_e_dir_name)
    if not os.path.exists(global_set.sys_log_dir_name):
        os.mkdir(global_set.sys_log_dir_name)

    #  创建中文新闻网页爬虫 ============================================================================================
    print('Scan News in http://news.ifeng.com')
    string = '步骤 1-1:-> 获取最新中文新闻网页网址( 从 http://news.ifeng.com 获取 )'
    global_set.print_gui(string)
    crawler_c = CrawlerForNewsIfengCom(global_set.news_c_start_url)
    start_time = time.time()
    #  抓取页面News链接 ===================================
    now_pag_number = 0
    while (crawler_c.next_pag != "") & (global_set.news_c_now_num < global_set.news_max_num):
        #  显示开始抓取信息
        now_pag_number += 1
        print('news list page ' + str(now_pag_number))
        print(crawler_c.next_pag)
        string = '=====:-> 获取新闻网页 ' + str(now_pag_number) + ' 从: ' + crawler_c.next_pag
        global_set.print_gui(string)
        #  抓取信息
        crawler_c.get_info()
        #  显示抓取结果
        global_set.news_c_now_num = len(crawler_c.news_url_list)
        print(str(global_set.news_c_now_num) + ' news has been find.')
        string = '=====:-> 现已获取到 ' + str(global_set.news_c_now_num) + ' 个新闻网址。'
        global_set.print_gui(string)
    #  显示结束信息  ======================================
    end_time = time.time()
    print('Function Finished! in ' + str(end_time - start_time) + 's')
    string = '=====:-> 获取完毕！ 用时： ' + str(round(end_time - start_time, 2)) + '秒'
    global_set.print_gui(string)
    print(str(now_pag_number) + ' page has been scan, and ', end="")
    print(str(global_set.news_c_now_num) + ' news has been find.')
    string = '=====:-> ' + str(now_pag_number) + ' 个新闻网址已扫描，并且 ' + str(global_set.news_c_now_num) +\
             ' 个新闻网址已获取。'
    global_set.print_gui(string)

    #  下载中文网页 =======================================
    print('\nWriting Files')
    string = '步骤 1-2:-> 下载最新中文新闻网页( 从上一步获取的新闻网址下载 )'
    global_set.print_gui(string)
    start_time = time.time()
    global_set.download_c_news_url_list = crawler_c.news_url_list[:global_set.news_max_num]
    #  记录下载的URL
    file_name = global_set.sys_log_dir_name + 'Download_C_News_URL.txt'
    print('writing ' + file_name)
    string = '=====:-> 记录获取的新闻网址到系统记录'
    global_set.print_gui(string)
    with open(file_name, "w") as f:
        #   写文件用str
        for url in global_set.download_c_news_url_list:
            f.write(url+'\n')
    #  根据URL下载HTML文件
    file_index = 0
    for url in global_set.download_c_news_url_list:
        html = requests.get(url).content.decode('utf-8', 'ignore')
        file_index += 1
        #    注意windows文件命名的禁用符，比如 /
        file_name = global_set.html_c_dir_name + 'News_' + str(file_index) + '_C.html'
        print('download file to ' + file_name)
        string = '=====:-> 下载网页到： ' + file_name
        global_set.print_gui(string)
        with open(file_name, 'w', encoding='utf-8') as f:
            #   写文件用bytes而不是str，所以要转码
            f.write(html)
    #  显示结束信息  ======================================
    end_time = time.time()
    print('Writing Files is Finished! in ' + str(end_time - start_time) + 's')
    print(str(global_set.news_max_num) + ' html files has been download')
    string = '=====:-> 下载完毕！ 用时： ' + str(round(end_time - start_time, 2)) + '秒'
    global_set.print_gui(string)
    string = '=====:-> ' + str(global_set.news_max_num) + ' 个网页已下载。'
    global_set.print_gui(string)

    #  创建英文新闻网页爬虫 ============================================================================================
    print('Scan News in http://www.globaltimes.cn')
    string = '步骤 1-3:-> 获取最新英文新闻网页网址( 从 http://www.globaltimes.cn 获取 )'
    global_set.print_gui(string)
    crawler_e = CrawlerForGlobalTimesCn(global_set.news_e_start_url_list)
    start_time = time.time()
    #  抓取页面News链接 ===================================
    now_pag_number = 0
    while (crawler_e.next_pag != "") & (global_set.news_e_now_num < global_set.news_max_num):
        #  显示开始抓取信息
        now_pag_number += 1
        print('news list page ' + str(now_pag_number))
        print(crawler_e.next_pag)
        string = '=====:-> 获取新闻网页 ' + str(now_pag_number) + ' 从: ' + crawler_e.next_pag
        global_set.print_gui(string)
        #  抓取信息
        crawler_e.get_info()
        #  显示抓取结果
        global_set.news_e_now_num = len(crawler_e.news_url_list)
        print(str(global_set.news_e_now_num) + ' news has been find.')
        string = '=====:-> 现已获取到 ' + str(global_set.news_e_now_num) + ' 个新闻网址。'
        global_set.print_gui(string)
    #  显示结束信息  ======================================
    end_time = time.time()
    print('Function Finished! in ' + str(end_time - start_time) + 's')
    string = '=====:-> 获取完毕！ 用时： ' + str(round(end_time - start_time, 2)) + '秒'
    global_set.print_gui(string)
    print(str(now_pag_number) + ' page has been scan, and ', end="")
    print(str(global_set.news_e_now_num) + ' news has been find.')
    string = '=====:-> ' + str(now_pag_number) + ' 个新闻网址已扫描，并且 ' + str(global_set.news_e_now_num) + \
             ' 个新闻网址已获取。'
    global_set.print_gui(string)

    #  下载英文网页 =======================================
    print('\nWriting Files')
    string = '步骤 1-4:-> 下载最新英文新闻网页( 从上一步获取的新闻网址下载 )'
    global_set.print_gui(string)
    start_time = time.time()
    global_set.download_e_news_url_list = crawler_e.news_url_list[:global_set.news_max_num]
    #  记录下载的URL
    file_name = global_set.sys_log_dir_name + 'Download_E_News_URL.txt'
    print('writing ' + file_name)
    string = '=====:-> 记录获取的新闻网址到系统记录'
    global_set.print_gui(string)
    with open(file_name, "w") as f:
        #   写文件用str
        for url in global_set.download_e_news_url_list:
            f.write(url+'\n')
    #  根据URL下载HTML文件
    file_index = 0
    for url in global_set.download_e_news_url_list:
        html = requests.get(url).content.decode('utf-8', 'ignore')
        file_index += 1
        #    注意windows文件命名的禁用符，比如 /
        file_name = global_set.html_e_dir_name + 'News_' + str(file_index) + '_E.html'
        print('download file to ' + file_name)
        string = '=====:-> 下载网页到： ' + file_name
        global_set.print_gui(string)
        with open(file_name, 'w', encoding='utf-8') as f:
            #   写文件用bytes而不是str，所以要转码
            f.write(html)
    #  显示结束信息  ======================================
    end_time = time.time()
    print('Writing Files is Finished! in ' + str(end_time - start_time) + 's')
    print(str(global_set.news_max_num) + ' html files has been download')
    string = '=====:-> 下载完毕！ 用时： ' + str(round(end_time - start_time, 2)) + '秒'
    global_set.print_gui(string)
    string = '=====:-> ' + str(global_set.news_max_num) + ' 个网页已下载。'
    global_set.print_gui(string)

    # 模块结束信息
    fun_end_time = time.time()
    string = '步骤 1:-> 下载最新新闻网页  成功完成！ 用时： ' + str(round(fun_end_time - fun_start_time, 2)) + '秒'
    global_set.print_gui(string)


if __name__ == '__main__':
    global_set = Settings()
    main(global_set)
