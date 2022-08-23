# Question_Matching

## 方法及思路

### 1. 分词阶段
* 使用中文分词工具[jieba分词](https://github.com/fxsjy/jieba)
* jieba分词模式选择：使用搜索引擎模式（cut_for_search）：在精确模式的基础上，对长词再次切分切词粒度更精细，提高召回率，适用于文本匹配任务
* 将给定的关键词列表加载至自定义词典（load_userdict），提升分词准确性
* 加载[停用词列表](https://github.com/goto456/stopwords)，在分词后去掉无实义的停用词和标点符号

### 2. 问句匹配阶段
将文本层面和句向量表征的相似度进行结合计算

#### 2.1 统计方法：BM25
* BM25是一种用来评价搜索问句(Query)和候选文本之间相关性的算法，它是一种基于概率检索模型提出的算法。
* 原理概述：
> 假如我们有一系列的候选文本D，现在要对某个Query进行匹配  
> 首先对Query进行分词，生成一系列语素Q  
> 然后对于每个搜索文档D<sub>i</sub>计算每个语素Q<sub>i</sub>与文档D<sub>j</sub>的相关性    
> 最后将所有的语素Q<sub>i</sub>与D<sub>j</sub>进行加权求和，从而得出Query与D<sub>j</sub>之间的相似度得分   
* 综上，相似度得分的计算分为三部分：语素权重、语素和候选文本的相似性、语素和Query的相似性   
* 优点：算法简单直观，计算速度快； 缺点：只有统计信息，没有语义信息 
* 改良：根据候选文本的分词结果手动配置同义词词库，从而在匹配时将同义词等同起来

#### 2.2 句向量搜索
* 总体原理：使用预训练模型对候选文本和搜索问句进行sentence encoding得到句向量，再使用距离度量算法（余弦相似度、点乘等）来计算相似度
* 弥补了统计方法对于语义信息的缺失
* 句向量表征模型选择：
> Sentence-BERT：将不同的句子输入到两个bert模型中（但这两个bert模型是参数共享的，也可以理解为是同一个bert模型），获取到每个句子的句子表征向量  
> SimCSE: 使用(自己,自己)作为正例、(自己,别人)作为负例来训练对比学习模型  
* 正在对比Sentence-BERT和SimCSE的使用效果，后续结果待补充

### 3. 结果返回阶段
* 将2.1和2.2的果进行加权计算，得到最终相似度结果
* 选择相似度计算结果TOP 5，并且大于某阈值 （query_threshold）的 N（N≤5）个问句作为匹配结果进行返回

## 其他可以提升分词和匹配的方法 （假设）
* 如果能收集到后续用户行为数据（如点击率或解决率），可结合进行加权计算，优化排序结果，也可以作为弱监督数据，优化模型训练
* 待补充

## TODO:
* 句向量表征模型选择
* 考虑为关键词设计不同权重，提升问句匹配的准确度




