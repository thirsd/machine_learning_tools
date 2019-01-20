#coding:utf-8

import os
import copy
import sys
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
class DetectApp(object):
    ''' detect which host in the app is deployed

    '''

    def __init__(self, app_file_dir, host_file_dir):
        self.app_file_dir = app_file_dir
        self.host_file_dir = host_file_dir

        self.app_ids, self.app_vectorizer, self.app_tfidf  \
            = self._build_tfidf_(self.app_file_dir)

        self.host_ids, self.host_vectorizer, self.host_tfidf \
            = self._build_tfidf_(self.host_file_dir)

    def _read_files_(self, file_dir):
        file_content = {}
        files_list = os.listdir(file_dir)
        for file in files_list:
            file_path = os.path.join(file_dir, file)
            with open(file_path) as fd:
                file_content[file] = '/'.join(fd.readlines())
        return file_content

    def _build_tfidf_(self, file_dir):
        content = self._read_files_(file_dir)
        ids = content.keys()
        # init the sklearn's class to cut list to words
        vectorizer = CountVectorizer(token_pattern=r"(?u)\b[^/\n]+\b")
        # init the sklearn's class to compute the tf-idf weight about words
        transformer = TfidfTransformer()
        #print(cotent.values())
        tfidf = transformer.fit_transform(
            vectorizer.fit_transform(content.values()))
        return ids, vectorizer, tfidf

    def _show_tfidf_(self, vectorizer, tfidf):
        words = vectorizer.get_feature_names()
        #print(words)

        #weight = tfidf.toarray()
        #for i in range(len(weight)):
        #    print(weight[i])
            #print(u"-------这里输出第", i, u"类文本的词语tf-idf权重------")
            #for j in range(len(word)):
            #    print("%s:%s" % (word[j], weight[i][j]))
        #print(type(tfidf))
        df_tfidf = pd.DataFrame(tfidf.todense(), columns=words)
        print(df_tfidf.T)

    def show_tfidf(self, type="app"):
        if type=="host":
            self._show_tfidf_(self.host_vectorizer, self.host_tfidf)
        else:
            self._show_tfidf_(self.app_vectorizer, self.app_tfidf)

    def cosine_distance(self, v1, v2):
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
        df_app_tfidf = pd.DataFrame(self.app_tfidf.todense(),
                                    columns=self.app_vectorizer.get_feature_names()).T
        set_app_words_org = self.app_vectorizer.get_feature_names()
        ser_app_tfidf_median = df_app_tfidf.median()

        for index, val in ser_app_tfidf_median.items():
            set_app_words

        pass


if __name__ == "__main__":
    detector = DetectApp("./data/apps/", "./data/hosts/")
    detector.detect_app()
    detector.show_tfidf(type="app")
    detector.show_tfidf(type="host")

