from bs4 import BeautifulSoup


class GraspingEnglishText:
    #  表示单个贴吧爬虫的类
    def __init__(self):
        self.html = ''
        self.text_str = ''

    # 重置参数
    def reset_var(self):
        self.html = ''
        self.text_str = ''

    # 写原文文件
    def write_txt(self, ori_file_path):
        # 写原始文件TXT
        if self.text_str:
            with open(ori_file_path, 'w', encoding='utf-8') as f:
                f.write(self.text_str)

    # 获取HTML文件
    def get_html(self, ori_file_path):
        with open(ori_file_path, 'rb') as f:
            #   写文件用bytes而不是str，所以要转码
            self.html = f.read()

    # 解析HTML文件
    def parse_html(self):
        soup = BeautifulSoup(self.html, features="html.parser")
        #  查找页面中所有news的文本内容
        #  查找标题
        title_soup = soup.find('h3')
        title_text = title_soup.get_text()
        if title_text == '':
            print('title is None! ... ', end='')
        #  查找内容
        artical_body_soup = soup.find('div', attrs={'class': 'span12 row-content'})
        if artical_body_soup:
            content_body_text = artical_body_soup.get_text()
        else:
            print('artical is None! ... ', end='')
            content_body_text = ''
        # 汇总标题和内容
        text = title_text.strip() + '. ' + content_body_text.strip()
        # 去除回车等其他不兼容字符
        text = text.replace('\n', '').replace('\r', '').replace('\\n', '')
        self.text_str = text
        # print('获取的新闻内容：', self.news_text)

    # 获取新闻文本信息
    def get_news_text_info(self, html_file_path, ori_file_path):
        self.reset_var()
        if html_file_path:
            self.get_html(html_file_path)
            self.parse_html()
            self.write_txt(ori_file_path)

