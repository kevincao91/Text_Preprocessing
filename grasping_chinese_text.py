from bs4 import BeautifulSoup


class GraspingChineseText:
    #  表示单个贴吧爬虫的类
    def __init__(self):
        self.html = ''
        self.text_str = ''

    def reset_var(self):
        self.html = ''
        self.text_str = ''

    def write_txt(self, ori_file_path):
        # 写原始文件TXT
        if self.text_str:
            with open(ori_file_path, 'w', encoding='utf-8') as f:
                f.write(self.text_str)

    def get_html(self, ori_file_path):
        with open(ori_file_path, "rb") as f:
            #   写文件用bytes而不是str，所以要转码
            self.html = f.read()

    def parse_html(self):
        soup = BeautifulSoup(self.html, features="html.parser")
        #  查找页面中所有news的文本内容
        #  查找标题
        title_soup = soup.find('h1')
        if title_soup:
            title_text = title_soup.get_text()
        else:
            title_soup = soup.find('div', attrs={'class': 'title'})
            if title_soup:
                title_text = title_soup.get_text()
            else:
                title_text = ''
                print('title is None! ... ', end='')
        #  查找内容
        artical_body_soup = soup.find('div', attrs={'id': 'artical'})
        if artical_body_soup:
            content_body_soup = artical_body_soup.find('div', attrs={'id': 'main_content'})
            content_body_text = content_body_soup.get_text()
        else:
            print('artical is None! ... ', end='')
            content_body_text = ''
        # 汇总标题和内容
        text = title_text.strip() + '。' + content_body_text.strip()
        # 去除回车等其他不兼容字符
        text = text.replace('\n', '').replace('\r', '').replace('\\n', '')
        self.text_str = text
        # print('获取的新闻内容：', self.news_text)

    def get_news_text_info(self, html_file_path, ori_file_path):
        self.reset_var()
        if html_file_path:
            self.get_html(html_file_path)
            self.parse_html()
            self.write_txt(ori_file_path)


