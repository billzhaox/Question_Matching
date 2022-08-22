from rank_bm25 import BM25Okapi
import jieba
import pandas as pd
import os
from openpyxl import load_workbook

jieba.load_userdict("keywords.txt")  # 载入关键词字典
stopwords = [line.strip() for line in open('cn_stopwords.txt', encoding='UTF-8').readlines()]  # 载入中文停用词表
# print(stopwords)

exl = load_workbook("Q&A_intern.xlsx")
q_data = exl["问题"]
k_data = exl["关键词"]
# print(q_data.rows)
# print(k_data)

corpus = [q[0].value for q in list(q_data.rows)[1:]]
tokenized_corpus = [[w for w in list(jieba.cut_for_search(q)) if w not in stopwords] for q in corpus]  # jieba分词后的问题库
# print(tokenized_corpus)

bm25 = BM25Okapi(tokenized_corpus)

query = "餐饮怎么报销"
tokenized_query = [w for w in list(jieba.cut_for_search(query)) if w not in stopwords]

doc_scores = bm25.get_scores(tokenized_query)
# print(doc_scores)
print(bm25.get_top_n(tokenized_query, corpus, n=5))
