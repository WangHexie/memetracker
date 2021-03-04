from typing import List
from tqdm import tqdm

import pysparnn.cluster_index as ci

from sklearn.feature_extraction.text import TfidfVectorizer

from dataset import Dataset
from sentence_similarity import compare_sentence
from config import mode
import pandas as pd


class SentenceSearch:
    def __init__(self, data: List[str], index=None):
        """

        :param data: [(str, index)]
        """
        self.data = data
        self.index = index

    def _build_index(self):
        pass

    def search_data(self, queries, k=50):
        """

        :param queries:
        :param k:
        :return: index of document
        """
        return []


class TfidfAnnSearch(SentenceSearch):
    def __init__(self, data: List[str]):
        super().__init__(data)
        self._build_index()

    def _build_index(self):
        print("building search engine index")

        print("start train tfidf")
        self.tv = TfidfVectorizer(max_df=0.7, min_df=10)
        self.tv.fit(self.data)

        print("start transform tfidf")
        features_vec = self.tv.transform(self.data)

        # build the search index!
        print("start build index")
        self.cp = ci.MultiClusterIndex(features_vec, list(range(len(self.data))))
        print("build finished")

    def search_data(self, queries: List[str], k=50):
        search_features_vec = self.tv.transform(queries)

        return self.cp.search(search_features_vec, k=k, k_clusters=2, return_distance=False)


class SentenceGraph:
    def __init__(self, data: List[str], k=50):
        """

        :param data: List[str]
        """

        self.k = k

        self.quoted_sentences: List[str] = data

        self.edges: List[(int, int)] = []  # the index is the index of Q

        self.search_engine: SentenceSearch = TfidfAnnSearch(self.quoted_sentences)

    def create_graph(self):
        """
        this can be parallelized
        :return:
        """
        # TODO: enable batch or ... handle
        for q in tqdm(range(len(self.quoted_sentences))):
            recalled_q_indexes = self.search_engine.search_data([self.quoted_sentences[q]], k=self.k)
            for index in recalled_q_indexes[0]:
                if q == index:
                    continue
                index = int(index)
                have_a_link, direction = compare_sentence(self.quoted_sentences[q], self.quoted_sentences[index])
                if have_a_link:
                    if direction == 0:
                        self.edges.append([q, index])
                    else:
                        self.edges.append([index, q])

        return self

# class SentenceGraph:
#     def __init__(self, data: List[dict], k=50, mode="test"):
#         """
#
#         :param data: List[dict("P", "T", "Q", "L")]
#         """
#         self.data = data
#
#         if mode=="test":
#             self.data = self.data[:10000]
#
#         self.k = k
#
#         self.quoted_sentences: List[str] = []
#         self.quoted_sentences_index: List[int] = []  # the index is the index of news(P)
#         self._create_index_for_data()
#
#         self.edges: List[(int, int)] = []  # the index is the index of Q
#
#         self.search_engine: SentenceSearch = TfidfAnnSearch(self.quoted_sentences)
#
#     def _create_index_for_data(self):
#         for i in tqdm(range(len(self.data))):
#             self.quoted_sentences += self.data[i]["Q"]
#             self.quoted_sentences_index += [i] * len(self.data[i]["Q"])
#         return self
#
#     def create_graph(self):
#         """
#         this can be parallelized
#         :return:
#         """
#         # TODO: enable batch or ... handle
#         for q in tqdm(range(len(self.quoted_sentences))):
#             recalled_q_indexes = self.search_engine.search_data([self.quoted_sentences[q]], k=self.k)
#             for index in recalled_q_indexes[0]:
#                 if q == index:
#                     continue
#                 index = int(index)
#                 have_a_link, direction = compare_sentence(self.quoted_sentences[q], self.quoted_sentences[index])
#                 if have_a_link:
#                     if direction == 0:
#                         self.edges.append([q, index])
#                     else:
#                         self.edges.append([index, q])
#
#         return self


if __name__ == '__main__':
    data_t = Dataset(None, None).build_from_one_file("./data/quotes_2008-08.txt")
    sg = SentenceGraph(data_t.data, mode=mode).create_graph()
    print("length of edges:", len(sg.edges))
    for i in range(10):
        print(sg.edges[i])
