import time
import os

from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt


class KMeansChineseNews:
    # 配置程序所有的设置数据
    def __init__(self, global_set):
        #  初始化程序的设置
        self.global_set = global_set
        self.news_str_list = []
        self.feature_word_list = []
        self.class_file_seq_list = []
        self.class_word_seq_list = []
        self.tf_idf_weight_mat = []

    def load_data(self):
        #  遍历简单文本所有文件
        ori_dir_path = self.global_set.text_c_dir_name
        for file_index in range(self.global_set.news_max_num):
            file_name = 'News_' + str(file_index + 1) + '_C.txt'
            file_path = os.path.join(ori_dir_path, file_name)
            print('get simple text file: ' + file_path)
            # string = '获取简单文本： ' + file_path
            # self.global_set.print_gui(string)
            with open(file_path, 'r', encoding='utf-8') as f:
                text_str = f.read()
            self.news_str_list.append(text_str)

    def get_class_file_seq_list(self, label_list):
        class_label_list = []
        file_seq_list = []
        file_index = 0
        #  遍历所有文件
        for class_label in label_list:
            if class_label in class_label_list:
                index = class_label_list.index(class_label)
                file_seq = file_seq_list[index]
                file_seq.append(file_index)
                file_seq_list[index] = file_seq
            else:
                class_label_list.append(class_label)
                file_seq_list.append([file_index])
            file_index += 1
        # 组合
        for index in range(len(class_label_list)):
            self.class_file_seq_list.append((class_label_list[index], file_seq_list[index]))
        # 排序
        self.class_file_seq_list.sort(reverse=True, key=lambda x: len(x[1]))

    def sort_class_file_seq_list(self, cluster_centers_list):
        index = 0
        #  遍历self.class_file_seq_list 所有类别
        for item in self.class_file_seq_list:
            class_label_index, file_seq = item
            cluster_centers = cluster_centers_list[class_label_index]
            # 遍历所有文件
            temp_file_file_center_score_list = []
            for file_index in file_seq:
                file_vector = self.tf_idf_weight_mat[file_index]
                # 两个向量点乘
                file_center_score = 0
                for ii in range(len(cluster_centers)):
                    file_center_score += file_vector[ii] * cluster_centers[ii]
                temp_file_file_center_score_list.append((file_index, file_center_score))
            # 排序结果
            temp_file_file_center_score_list.sort(reverse=True, key=lambda x: x[1])
            # 获取排序完成的文件序列
            sorted_file_seq = []
            for content in temp_file_file_center_score_list:
                sorted_file_seq.append(content[0])
            # 更新原文件列表
            self.class_file_seq_list[index] = (class_label_index, sorted_file_seq)
            # 循环
            index += 1

    def get_class_word_seq_list(self, cluster_centers_list):
        class_label_index = 0
        #  遍历所有类别
        for cluster_centers in cluster_centers_list:
            temp_center_word_list = []
            index = 0
            for center in cluster_centers:
                temp_center_word_list.append((center, self.feature_word_list[index]))
                index += 1
            temp_center_word_list.sort(reverse=True)
            word_seq_list = []
            for item in temp_center_word_list:
                word_seq_list.append(item[1])
            # 组合
            self.class_word_seq_list.append((class_label_index, word_seq_list))
            # 循环
            class_label_index += 1

    def k_means_cal(self):
        #  开始功能
        print('K_Means Chinese News Function Start.')
        string = '对中文文档进行 K-Means 聚类'
        self.global_set.print_gui(string)
        # 计时
        fun_start_time = time.time()

        # 1 加载语料
        # 显示开始信息
        print('1-> 加载语料')
        string = '1-> 加载语料'
        self.global_set.print_gui(string)
        self.load_data()

        # 2 计算 tf-idf 设为权重
        # 显示开始信息
        print('2-> 计算 tf-idf 设为权重')
        string = '2-> 计算 tf-idf 设为权重'
        self.global_set.print_gui(string)

        vectorizer = CountVectorizer()
        transformer = TfidfTransformer()
        tf_idf = transformer.fit_transform(vectorizer.fit_transform(self.news_str_list))

        # 3 获取词袋模型中的所有词语特征
        #   如果特征数量非常多的情况下可以按照权重降维
        # 显示开始信息
        print('3-> 获取词袋模型中的所有词语特征')
        string = '3-> 获取词袋模型中的所有词语特征'
        self.global_set.print_gui(string)

        self.feature_word_list = vectorizer.get_feature_names()
        print("word feature length: {}".format(len(self.feature_word_list)))

        # 4 导出权重，到这边就实现了将文字向量化的过程，矩阵中的每一行就是一个文档的向量表示
        # 显示开始信息
        print('4-> 导出权重')
        string = '4-> 导出权重'
        self.global_set.print_gui(string)

        tf_idf_weight = tf_idf.toarray()
        self.tf_idf_weight_mat = tf_idf_weight

        # 5 对向量进行聚类
        # 显示开始信息
        print('5-> 对向量进行聚类')
        string = '5-> 对向量进行聚类'
        self.global_set.print_gui(string)

        # 指定分成 class_num 个类
        k_means = KMeans(n_clusters=self.global_set.class_num)
        k_means.fit(tf_idf_weight)

        # 打印出各个族的中心点
        print(k_means.cluster_centers_)
        # 打印分组结果
        for file_index, class_label in enumerate(k_means.labels_, 1):
            print("index: {}, label: {}".format(file_index, class_label))
        # 求类对应文件序列表
        self.get_class_file_seq_list(k_means.labels_)
        # 文件序列排序
        self.sort_class_file_seq_list(k_means.cluster_centers_)
        # 求类对应词序列表
        self.get_class_word_seq_list(k_means.cluster_centers_)

        # 样本距其最近的聚类中心的平方距离之和，用来评判分类的准确度，值越小越好
        # k-means的超参数n_clusters可以通过该值来评估
        print("inertia: {}".format(k_means.inertia_))

        # 6 可视化
        # 使用T-SNE算法，对权重进行降维，准确度比PCA算法高，但是耗时长
        # 显示开始信息
        print('6-> 可视化')
        string = '6-> 可视化'
        self.global_set.print_gui(string)

        t_sne = TSNE(n_components=2)
        decomposition_data = t_sne.fit_transform(tf_idf_weight)

        # 显示设置
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False

        x = []
        y = []

        for i in decomposition_data:
            x.append(i[0])
            y.append(i[1])

        fig = plt.figure(figsize=(5, 5))
        ax = plt.axes()
        plt.title('聚类结果降维显示')
        plt.scatter(x, y, c=k_means.labels_, marker="x")
        plt.xticks(())
        plt.yticks(())
        plt.ion()
        plt.show()
        plt.savefig(os.path.join(self.global_set.sys_log_dir_name, 'sample.png'), aspect=1)

        #  显示结束信息
        fun_end_time = time.time()
        print('Function Finished! in ' + str(fun_end_time - fun_start_time) + 's')
        string = '处理完毕！ 用时： ' + str(round(fun_end_time - fun_start_time, 2)) + '秒'
        self.global_set.print_gui(string)
