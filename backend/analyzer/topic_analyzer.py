import jieba
import jieba.analyse
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import numpy as np

class TopicAnalyzer:
    """话题分析器"""

    def __init__(self, stopwords_path):
        self.stopwords = self._load_stopwords(stopwords_path)
        jieba.analyse.set_stop_words(stopwords_path)

    def _load_stopwords(self, filepath):
        """加载停用词"""
        stopwords = set()
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    word = line.strip()
                    if word:
                        stopwords.add(word)
        return stopwords

    def extract_keywords(self, text, topK=10):
        """提取关键词（TF-IDF）"""
        keywords = jieba.analyse.extract_tags(text, topK=topK, withWeight=True)
        return [{'word': word, 'weight': round(weight, 4)} for word, weight in keywords]

    def extract_hotwords(self, texts, topK=20):
        """提取热词（词频统计）"""
        all_words = []
        for text in texts:
            words = jieba.lcut(text)
            words = [w for w in words if w not in self.stopwords and len(w) > 1]
            all_words.extend(words)

        word_freq = Counter(all_words)
        hotwords = word_freq.most_common(topK)
        return [{'word': word, 'count': count} for word, count in hotwords]

    def cluster_topics(self, texts, n_clusters=5):
        """话题聚类"""
        if len(texts) < n_clusters:
            n_clusters = len(texts)

        # 分词并过滤
        processed_texts = []
        for text in texts:
            words = jieba.lcut(text)
            words = [w for w in words if w not in self.stopwords and len(w) > 1]
            processed_texts.append(' '.join(words))

        # TF-IDF向量化
        vectorizer = TfidfVectorizer(max_features=100)
        X = vectorizer.fit_transform(processed_texts)

        # K-means聚类
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        labels = kmeans.fit_predict(X)

        # 提取每个簇的关键词
        topics = []
        for i in range(n_clusters):
            cluster_indices = np.where(labels == i)[0]
            cluster_texts = [processed_texts[idx] for idx in cluster_indices]

            # 提取簇的关键词
            if cluster_texts:
                cluster_text = ' '.join(cluster_texts)
                keywords = self.extract_keywords(cluster_text, topK=5)
                topics.append({
                    'topic_id': i,
                    'keywords': keywords,
                    'doc_count': len(cluster_indices)
                })

        return topics, labels.tolist()

import os
