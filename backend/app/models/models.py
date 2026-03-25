from datetime import datetime
from app import db

class Article(db.Model):
    """文章数据模型"""
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False)
    content = db.Column(db.Text, nullable=False)
    source = db.Column(db.String(100))  # 来源：weibo, news, forum
    url = db.Column(db.String(500), unique=True)
    author = db.Column(db.String(100))
    publish_time = db.Column(db.DateTime)
    crawl_time = db.Column(db.DateTime, default=datetime.utcnow)

    # 分析结果
    sentiment = db.Column(db.String(20))  # positive, neutral, negative
    sentiment_score = db.Column(db.Float)
    keywords = db.Column(db.Text)  # JSON格式存储
    topic = db.Column(db.String(200))

    # 统计信息
    view_count = db.Column(db.Integer, default=0)
    comment_count = db.Column(db.Integer, default=0)
    share_count = db.Column(db.Integer, default=0)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'source': self.source,
            'url': self.url,
            'author': self.author,
            'publish_time': self.publish_time.isoformat() if self.publish_time else None,
            'crawl_time': self.crawl_time.isoformat() if self.crawl_time else None,
            'sentiment': self.sentiment,
            'sentiment_score': self.sentiment_score,
            'keywords': self.keywords,
            'topic': self.topic,
            'view_count': self.view_count,
            'comment_count': self.comment_count,
            'share_count': self.share_count
        }

class Alert(db.Model):
    """预警记录模型"""
    __tablename__ = 'alerts'

    id = db.Column(db.Integer, primary_key=True)
    alert_type = db.Column(db.String(50))  # negative_surge, hotspot, keyword
    level = db.Column(db.String(20))  # low, medium, high
    title = db.Column(db.String(200))
    description = db.Column(db.Text)
    trigger_value = db.Column(db.Float)
    threshold = db.Column(db.Float)
    create_time = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')  # pending, handled, ignored

    def to_dict(self):
        return {
            'id': self.id,
            'alert_type': self.alert_type,
            'level': self.level,
            'title': self.title,
            'description': self.description,
            'trigger_value': self.trigger_value,
            'threshold': self.threshold,
            'create_time': self.create_time.isoformat() if self.create_time else None,
            'status': self.status
        }
