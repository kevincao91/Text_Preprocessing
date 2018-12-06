from nltk.stem.porter import PorterStemmer


class PreprocessingEnglishText:
    #  表示单个贴吧爬虫的类
    def __init__(self, punctuation, stopwords):
        self.text_str = ''
        self.seg_list = []
        self.word_list = []
        self.word_stem_list = []
        self.punctuation = punctuation
        self.stopwords = stopwords

    def reset_var(self):
        self.text_str = ''
        self.seg_list = []
        self.word_list = []
        self.word_stem_list = []

    def write_txt(self, tra_file_path):
        if self.word_list:
            with open(tra_file_path, 'w', encoding='utf-8') as f:
                #   写文件用str
                f.write(' '.join(self.word_list))

    def get_ori_text(self, ori_file_path):
        with open(ori_file_path, "rb") as f:
            #   写文件用bytes而不是str，所以要转码
            self.text_str = f.read().decode('utf-8', 'ignore')

    def delete_punctuations(self):
        temp_text = ''
        # 去除标点
        for item in self.text_str:
            if item in self.punctuation:  # 如果是标点符号，即跳过
                continue
            else:
                temp_text += item
        self.text_str = temp_text
        # print("去 标 点 结 果: ", self.news_text)

    def fen_ci(self):
        # 英文文章按照空格“分词”
        self.seg_list = self.text_str.split()
        # print("分  词  结  果: ", ' '.join(self.seg_list))

    def word_stemming(self):
        # 取词干
        for word in self.seg_list:
            word = PorterStemmer().stem(word)
            self.word_stem_list.append(word)
        # print("取 词 干 结 果: ", ' '.join(self.word_stem_list))

    def delete_stopwords(self):
        # 去除标点
        for word in self.word_stem_list:
            if word in self.stopwords:  # 如果是stopwords，即跳过
                continue
            else:
                self.word_list.append(word)
        # print("去除停用词结果: ", ' '.join(self.word_list))

    def parse_txt(self):
        # 去除标点
        self.delete_punctuations()
        # 按照空格分词
        self.fen_ci()
        # 取词干
        self.word_stemming()
        # 去除停用词
        self.delete_stopwords()

    def get_news_text_info(self, ori_file_path, tra_file_path):
        self.reset_var()
        if ori_file_path:
            self.get_ori_text(ori_file_path)
            self.parse_txt()
            self.write_txt(tra_file_path)

    # 获取搜索文本信息
    def get_search_text_info(self, search_str, tra_file_path):
        self.reset_var()
        if search_str:
            self.text_str = search_str
            self.parse_txt()
            self.write_txt(tra_file_path)
