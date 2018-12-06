import math


class InvertedList:
    #  表示单个倒排表的类
    def __init__(self):
        self.lines = []
        self.word_list = []
        self.file_seq_list = []
        self.idf_list = []
        self.inverted_list = []

    # 重置变量
    def reset_var(self):
        self.lines = []

    # 写倒排表文件
    def write_txt(self, tra_file_path):
        if self.word_list:
            # 组合倒排表
            index = 0
            for word in self.word_list:
                self.inverted_list.append((word, self.idf_list[index], self.file_seq_list[index]))
                index += 1
            # 写文件
            with open(tra_file_path, 'w', encoding='utf-8') as f:
                #   写文件用str
                for content in self.inverted_list:
                    word = content[0]
                    idf = ' ' + str(content[1])
                    file_seq = content[2]
                    str_file_seq = ''
                    for file in file_seq:
                        str_file_seq += ' '
                        str_file_seq += file
                    f.write(word + idf + str_file_seq + '\n')

    # 获取词袋文件
    def get_bow(self, ori_file_path):
        with open(ori_file_path, 'rb') as f:
            #   写文件用bytes而不是str，所以要转码
            text = f.read().decode('utf-8', 'ignore')
            lines = text.splitlines()  # 读取全部内容 ，并以列表方式返回
        self.lines = lines

    # 更新倒排表
    def update_inverted_list(self, file_name):
        for line in self.lines:
            word = line.split()[0]
            if word in self.word_list:
                index = self.word_list.index(word)
                file_seq = self.file_seq_list[index]
                file_seq.append(file_name)
                self.file_seq_list[index] = file_seq
            else:
                self.word_list.append(word)
                self.file_seq_list.append([file_name])

    # 添加信息到倒排表
    def add_info(self, ori_file_path, file_name):
        self.reset_var()
        if ori_file_path:
            self.get_bow(ori_file_path)
            self.update_inverted_list(file_name)

    # 计算idf值
    def cal_idf(self, num_file):
        if self.file_seq_list:
            for file_seq in self.file_seq_list:
                idf = round(math.log10(num_file / len(file_seq)), 4)
                self.idf_list.append(idf)

