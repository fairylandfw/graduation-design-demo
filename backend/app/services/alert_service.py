from app import db
from app.models.models import Article, Alert
from analyzer.sentiment_analyzer import SentimentAnalyzer
from config.config import Config
from datetime import datetime, timedelta

class AlertService:
    """预警服务"""

    def __init__(self):
        self.sentiment_analyzer = SentimentAnalyzer(Config.DICT_DIR)

    def check_negative_surge(self):
        """检查负面舆情激增"""
        # 获取最近24小时的文章
        start_time = datetime.now() - timedelta(hours=24)
        articles = Article.query.filter(Article.publish_time >= start_time).all()

        if len(articles) == 0:
            return

        # 统计负面比例
        negative_count = sum(1 for a in articles if a.sentiment == 'negative')
        negative_ratio = negative_count / len(articles)

        # 判断是否触发预警
        if negative_ratio >= Config.ALERT_NEGATIVE_RATIO:
            alert = Alert(
                alert_type='negative_surge',
                level='high',
                title='负面舆情激增预警',
                description=f'最近24小时负面舆情比例达到{negative_ratio:.2%}，超过阈值{Config.ALERT_NEGATIVE_RATIO:.2%}',
                trigger_value=negative_ratio,
                threshold=Config.ALERT_NEGATIVE_RATIO
            )
            db.session.add(alert)
            db.session.commit()

    def check_hotspot(self):
        """检查热点话题"""
        from analyzer.topic_analyzer import TopicAnalyzer

        # 获取最近7天的文章
        start_time = datetime.now() - timedelta(days=7)
        articles = Article.query.filter(Article.publish_time >= start_time).all()

        if len(articles) < 10:
            return

        # 提取热词
        topic_analyzer = TopicAnalyzer(Config.STOPWORDS_PATH)
        texts = [a.content for a in articles]
        hotwords = topic_analyzer.extract_hotwords(texts, topK=10)

        # 检查是否有超高频热词
        for hotword in hotwords:
            if hotword['count'] >= Config.ALERT_HOTSPOT_THRESHOLD:
                alert = Alert(
                    alert_type='hotspot',
                    level='medium',
                    title=f'热点话题预警：{hotword["word"]}',
                    description=f'关键词"{hotword["word"]}"在最近7天出现{hotword["count"]}次，成为热点话题',
                    trigger_value=hotword['count'],
                    threshold=Config.ALERT_HOTSPOT_THRESHOLD
                )
                db.session.add(alert)

        db.session.commit()

    def run_all_checks(self):
        """运行所有预警检查"""
        self.check_negative_surge()
        self.check_hotspot()
