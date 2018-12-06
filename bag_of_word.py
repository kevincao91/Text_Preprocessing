import math


class BagOfWord:
    #  表示单个贴吧爬虫的类
    def __init__(self):
        self.text = ''
        self.text_word_list = []
        self.bow_word_list = []
        self.bow_tf_list = []
        self.bow_list = []

    def reset_var(self):
        self.text = ''
        self.text_word_list = []
        self.bow_word_list = []
        self.bow_tf_list = []
        self.bow_list = []

    def write_txt(self, tra_file_path):
        if self.bow_list:
            with open(tra_file_path, 'w', encoding='utf-8') as f:
                #   写文件用str
                for bow in self.bow_list:
                    f.write(bow[0]+' '+str(bow[1])+' '+str(bow[2])+'\n')

    def get_words(self, ori_file_path):
        with open(ori_file_path, 'rb') as f:
            #   写文件用bytes而不是str，所以要转码
            self.text = f.read().decode('utf-8', 'ignore')
        self.text_word_list = self.text.split()

    def parse_word(self):
        word_set = set(self.text_word_list)
        for word in word_set:
            num_word = self.text_word_list.count(word)
            tf = round(1 + math.log10(num_word), 4)
            self.bow_list.append((word, num_word, tf))
        # 按词频排序 倒序
        self.bow_list.sort(reverse=True, key=lambda x: x[1])
        # 取元素
        for bow in self.bow_list:
            word, num_word, tf = bow
            self.bow_word_list.append(word)
            self.bow_tf_list.append(tf)

    # 转换信息 由词条到词袋
    def convert_info(self, ori_file_path, tra_file_path):
        self.reset_var()
        if ori_file_path:
            self.get_words(ori_file_path)
            self.parse_word()
            self.write_txt(tra_file_path)


