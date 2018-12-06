import math
import os


class CosineDistance:
    #  表示余弦距离计算的类
    def __init__(self, global_set, word_list, idf_list, file_seq_list):
        self.global_set = global_set
        self.word_list = word_list
        self.idf_list = idf_list
        self.file_seq_list = file_seq_list
        self.doc_word_list_1 = []
        self.doc_word_list_2 = []
        self.doc_vector_1 = []
        self.doc_vector_2 = []
        self.cos_dis = 0

    # 重置变量
    def reset_var(self):
        self.doc_word_list_1 = []
        self.doc_word_list_2 = []
        self.doc_vector_1 = []
        self.doc_vector_2 = []
        self.cos_dis = 0

    # 获取文档词袋
    def get_doc_bow(self, file_name):
        word_list = []
        tf_list = []
        file_path = os.path.join(self.global_set.bow_all_dir_name, file_name)
        with open(file_path, 'rb') as f:
            #   写文件用bytes而不是str，所以要转码
            text = f.read().decode('utf-8', 'ignore')
            lines = text.splitlines()  # 读取全部内容 ，并以列表方式返回
        for line in lines:
            word, num_word, tf = line.split(' ', 2)
            word_list.append(word)
            tf_list.append(float(tf))
        return word_list, tf_list

    # 余弦距离计算
    def cos_dis_cal(self):
        self.cos_dis = 0
        # 查找相同Word
        same_word_list = list(set(self.doc_word_list_1).intersection(set(self.doc_word_list_2)))
        # 判断是否有相同词
        if same_word_list:
            print('has same word!')
            print(same_word_list)
            for same_word in same_word_list:
                list_index_1 = self.doc_word_list_1.index(same_word)
                tf_idf_1 = self.doc_vector_1[list_index_1]
                list_index_2 = self.doc_word_list_2.index(same_word)
                tf_idf_2 = self.doc_vector_2[list_index_2]
                self.cos_dis += (tf_idf_1 * tf_idf_2)
        # 没有相同词
        else:
            print('has not same word!')
            self.cos_dis = 0

    # 多维向量归一化
    def length_normalized(self, doc_vector):
        sum_2 = 0
        for item in doc_vector:
            sum_2 += math.pow(item, 2)
        vector_length = math.sqrt(sum_2)
        # length_normalized
        normalized_doc_vector = []
        for item in doc_vector:
            normalized_doc_vector.append(item / vector_length)
        #  show
        # print('before length_normalized: ', doc_vector)
        # print('after length_normalized: ', normalized_doc_vector)
        return normalized_doc_vector

    # 得到 tf-idf 向量
    def get_tf_idf_vector(self, word_list, tf_list):
        tf_idf_vector = []
        for word in word_list:
            if word in self.word_list:
                inverted_list_index = self.word_list.index(word)
                idf = self.idf_list[inverted_list_index]
                list_index = word_list.index(word)
                tf = tf_list[list_index]
                tf_idf = tf * idf
                tf_idf_vector.append(tf_idf)
            else:
                tf_idf_vector.append(0)
        return tf_idf_vector

    # 文档 与 文档 余弦距离计算
    def doc_doc_cos_dis_cal(self, file_name_1, file_name_2):
        self.reset_var()
        # 获取文件词袋
        word_list_1, tf_list_1 = self.get_doc_bow(file_name_1)
        word_list_2, tf_list_2 = self.get_doc_bow(file_name_2)
        self.doc_word_list_1 = word_list_1
        self.doc_word_list_2 = word_list_2
        # 获取 tf-idf
        self.doc_vector_1 = self.get_tf_idf_vector(word_list_1, tf_list_1)
        print('doc_vector_1: ', end='')
        for word in word_list_1:
            print(' ' + word + '-' + str(self.doc_vector_1[word_list_1.index(word)]), end='')
        print('\n')
        self.doc_vector_2 = self.get_tf_idf_vector(word_list_2, tf_list_2)
        print('doc_vector_2: ', end='')
        for word in word_list_2:
            print(' ' + word + '-' + str(self.doc_vector_2[word_list_2.index(word)]), end='')
        print('\n')
        # length_normalized
        self.doc_vector_1 = self.length_normalized(self.doc_vector_1)
        self.doc_vector_2 = self.length_normalized(self.doc_vector_2)
        # 计算余弦距离
        self.cos_dis_cal()
        return self.cos_dis

    # 搜索 与 文档 余弦距离计算
    def search_doc_cos_dis_cal(self, search_word_list, search_tf_list, file_name_2):
        self.reset_var()
        # 获取搜索和文件的词袋
        word_list_2, tf_list_2 = self.get_doc_bow(file_name_2)
        self.doc_word_list_1 = search_word_list
        self.doc_word_list_2 = word_list_2
        # 获取 搜索的 tf-idf
        self.doc_vector_1 = self.get_tf_idf_vector(search_word_list, search_tf_list)
        print('search_vector: ', end='')
        for word in search_word_list:
            print(' ' + word + '-' + str(self.doc_vector_1[search_word_list.index(word)]), end='')
        print('\n')
        # 搜索时文档不用tf-idf，直接用tf
        self.doc_vector_2 = tf_list_2
        print('doc_vector_2: ', end='')
        for word in word_list_2:
            print(' ' + word + '-' + str(self.doc_vector_2[word_list_2.index(word)]), end='')
        print('\n')
        # length_normalized
        self.doc_vector_1 = self.length_normalized(self.doc_vector_1)
        self.doc_vector_2 = self.length_normalized(self.doc_vector_2)
        # 计算余弦距离
        self.cos_dis_cal()
        return self.cos_dis
