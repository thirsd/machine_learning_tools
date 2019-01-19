#coding:utf-8

import os
import sys
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

class DetectApp(object):
    ''' detect which host in the app is deployed

    '''

    def __init__(self, app_file_dir, host_file_dir):
        self.app_file_dir = app_file_dir
        self.host_file_dir = host_file_dir

        # init the sklearn's class to cut list to words
        self.vectorizer = CountVectorizer(token_pattern=r"(?u)\b[^/\n]+\b")
        # init the sklearn's class to compute the tf-idf weight about words
        self.transformer = TfidfTransformer()
        self.tfidf = None

    def _read_files_(self, file_dir):
        file_content = {}
        files_list = os.listdir(file_dir)
        for file in files_list:
            file_path = os.path.join(file_dir, file)
            with open(file_path) as fd:
                file_content[file] = '/'.join(fd.readlines())
        return file_content

    def _build_tfidf_(self):
        apps_cotent = self._read_files_(self.app_file_dir)
        print(apps_cotent.values())
        tfidf = self.transformer.fit_transform(
            self.vectorizer.fit_transform(apps_cotent.values()))
        return tfidf

    def show_tfidf(self):
        word = self.vectorizer.get_feature_names()
        weight = self.tfidf.toarray()
        for i in range(len(weight)):
            print(u"-------这里输出第", i, u"类文本的词语tf-idf权重------")
            for j in range(len(word)):
                print("%s:%s" % (word[j], weight[i][j]))

    def _cosine_distance_(v1, v2):
        dot_product = 0.0
        sqr_v1 = 0.0
        sqr_v2 = 0.0
        for a, b in zip(v1, v2):
            dot_product += a * b
            sqr_v1 += a ** 2
            sqr_v2 += b ** 2
        if sqr_v1 == 0.0 or sqr_v2 == 0.0:
            return None
        else:
            return dot_product / ((sqr_v1 * sqr_v2) ** 0.5)

    def detect_app(self):
        self.tfidf = self._build_tfidf_()



if __name__ == "__main__":
    detector = DetectApp("./data/apps/", "./data/hosts/")
    detector.detect_app()
    detector.show_tfidf()

