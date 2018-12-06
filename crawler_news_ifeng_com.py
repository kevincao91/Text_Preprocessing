import requests
from bs4 import BeautifulSoup
import time


class CrawlerForNewsIfengCom:
    #  表示单个贴吧爬虫的类
    def __init__(self, target_url):
        self.target_url = target_url
        self.news_url_list = []
        self.next_pag = target_url
        self.start_time = time.time()
        self.finish_time = time.time()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/47.0.2526.80 Safari/537.36 '}

    # 获取网页HTML页面
    def get_html(self):
        #  html = requests.get(self.target_url, headers=self.headers).content
        html = requests.get(self.next_pag).content
        return html

    # 解析HTML页面
    def parse_html(self, html):
        soup = BeautifulSoup(html, features="html.parser")
        #  查找页面中所有news的URL
        news_body_soup = soup.find('div', attrs={'class': 'newsList'})
        li_list_soup = news_body_soup.find_all('li')
        for li_soup in li_list_soup:
            if li_soup:
                a_soup = li_soup.find('a')
                news_url = a_soup.get('href')
                if len(news_url) == 49:
                    self.news_url_list.append(news_url)

        #  查找下一页URL
        next_pag_div_soup = news_body_soup.find('div', attrs={'class': 'nextPage'})
        m_pag_div_soup = next_pag_div_soup.find('div', attrs={'class': 'm_page'})
        m_pag_a_soup = m_pag_div_soup.find_all('a')
        m_pag_soup = m_pag_a_soup[-1]
        if m_pag_soup:
            if m_pag_soup.text == '下一页 ':
                self.next_pag = m_pag_soup.get('href')
            else:
                # 这一天新闻已完结，选择前一天新闻继续
                r_end_div_soup = next_pag_div_soup.find('div', attrs={'class': 'r_end'})
                r_end_a_soup = r_end_div_soup.find('a')
                if r_end_a_soup.text == '前一天':
                    self.next_pag = r_end_a_soup.get('href')
                else:
                    self.next_pag = ""
        else:
            self.next_pag = ""

    # 获取网页信息
    def get_info(self):
        if self.next_pag:
            html = self.get_html()
            self.parse_html(html)
            self.finish_time = time.time()
