import requests
from bs4 import BeautifulSoup
import time


class CrawlerForGlobalTimesCn:
    #  表示单个贴吧爬虫的类
    def __init__(self, target_url_list):
        self.target_url_list = target_url_list
        self.column_url_index = 0
        self.target_url = self.target_url_list[self.column_url_index]
        self.news_url_list = []
        self.next_pag = self.target_url
        self.start_time = time.time()
        self.finish_time = time.time()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/47.0.2526.80 Safari/537.36 '}

    def get_html(self):
        #  html = requests.get(self.target_url, headers=self.headers).content
        html = requests.get(self.next_pag).content
        return html

    def parse_html(self, html):
        soup = BeautifulSoup(html, features="html.parser")
        #  查找页面中所有news的URL
        news_body_soup = soup.find('div', attrs={'id': 'channel-list'})
        a_list_soup = news_body_soup.find_all('a', attrs={'target': '_blank'})
        for a_soup in a_list_soup:
            if a_soup:
                if a_soup.text != '':
                    news_url = a_soup.get('href')
                    self.news_url_list.append(news_url)

        #  查找下一页URL
        next_pag_div_soup = news_body_soup.find('div', attrs={'class': 'row-fluid text-center pages'})
        next_a_soup = next_pag_div_soup.find('a', text='Next >>')
        if next_a_soup:
            self.next_pag = self.target_url + next_a_soup.get('href')
        else:
            # 切换其他栏目新闻
            self.column_url_index += 1
            self.target_url = self.target_url_list[self.column_url_index]
            self.next_pag = self.target_url

    def get_info(self):
        if self.next_pag:
            html = self.get_html()
            self.parse_html(html)
            self.finish_time = time.time()
