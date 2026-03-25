import os
import jieba

class SentimentAnalyzer:
    """基于词典的情感分析器"""

    def __init__(self, dict_dir):
        self.positive_words = self._load_dict(os.path.join(dict_dir, 'positive.txt'))
        self.negative_words = self._load_dict(os.path.join(dict_dir, 'negative.txt'))
        self.degree_words = self._load_degree_dict(os.path.join(dict_dir, 'degree.txt'))
        self.negation_words = self._load_dict(os.path.join(dict_dir, 'negation.txt'))

    def _load_dict(self, filepath):
        """加载词典文件"""
        words = set()
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    word = line.strip()
                    if word:
                        words.add(word)
        return words

    def _load_degree_dict(self, filepath):
        """加载程度副词词典（词:权重）"""
        degree_dict = {}
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) == 2:
                        word, weight = parts
                        degree_dict[word] = float(weight)
        return degree_dict

    def analyze(self, text):
        """
        分析文本情感（优化版 - 提高区分度）
        返回: (sentiment, score)
        sentiment: 'positive', 'neutral', 'negative'
        score: 情感得分 [-1, 1]
        """
        words = jieba.lcut(text)
        score = 0.0
        sentiment_word_count = 0  # 情感词数量
        i = 0

        while i < len(words):
            word = words[i]

            # 检查是否为情感词
            if word in self.positive_words:
                word_score = 1.5  # 提高基础权重
                sentiment_word_count += 1
            elif word in self.negative_words:
                word_score = -1.5  # 提高基础权重
                sentiment_word_count += 1
            else:
                i += 1
                continue

            # 检查前面的程度副词（扩大范围到2个词）
            degree_multiplier = 1.0
            for j in range(max(0, i-2), i):
                if words[j] in self.degree_words:
                    degree_multiplier *= self.degree_words[words[j]]

            word_score *= degree_multiplier

            # 检查前面的否定词（扩大范围到4个词）
            negation_count = 0
            for j in range(max(0, i-4), i):
                if words[j] in self.negation_words:
                    negation_count += 1

            if negation_count % 2 == 1:
                word_score *= -1.2  # 否定词加强效果

            score += word_score
            i += 1

        # 改进的归一化方法
        if sentiment_word_count > 0:
            # 根据情感词数量归一化，而不是总词数
            score = score / max(sentiment_word_count, 1)
            # 应用sigmoid函数增强区分度
            score = 2 / (1 + pow(2.718, -score)) - 1
            score = max(-1.0, min(1.0, score))
        else:
            score = 0.0

        # 降低中性阈值，提高区分度
        if score > 0.05:  # 从0.1降到0.05
            sentiment = 'positive'
        elif score < -0.05:  # 从-0.1降到-0.05
            sentiment = 'negative'
        else:
            sentiment = 'neutral'

        return sentiment, round(score, 4)

    def batch_analyze(self, texts):
        """批量分析"""
        results = []
        for text in texts:
            sentiment, score = self.analyze(text)
            results.append({'sentiment': sentiment, 'score': score})
        return results
