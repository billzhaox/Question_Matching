from flask import Flask, jsonify, request, make_response, abort
from flask_restful import Api, Resource
from flask_cors import CORS
from rank_bm25 import BM25Okapi
import jieba
import pandas as pd
import os
from openpyxl import load_workbook

app = Flask(__name__)
api = Api(app)
CORS(app, resources=r'/*', supports_credentials=True)

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

class Search(Resource):
    def post(self):
        data = request.get_json()
        # print(data)
        if not data:
            abort(400, "The request json is none")
        query = data.get('query')
        tokenized_query = [w for w in list(jieba.cut_for_search(query)) if w not in stopwords]
        # doc_scores = bm25.get_scores(tokenized_query)
        # print(doc_scores)
        return jsonify(bm25.get_top_n(tokenized_query, corpus, n=5))

api.add_resource(Search, '/search')

if __name__ == "__main__":
    app.run(debug=True)
    # app.run()

