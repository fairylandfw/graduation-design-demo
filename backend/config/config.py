import os
from datetime import timedelta

class Config:
    """基础配置"""
    # 应用配置
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')

    # 数据库配置 - 使用MySQL
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'mysql+pymysql://root:123456@localhost:3306/sentiment_db?charset=utf8mb4'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    # 爬虫配置
    CRAWLER_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    CRAWLER_DELAY = 2  # 请求延迟（秒）
    CRAWLER_TIMEOUT = 30

    # 分析配置
    SENTIMENT_THRESHOLD_POSITIVE = 0.1
    SENTIMENT_THRESHOLD_NEGATIVE = -0.1

    # 预警配置
    ALERT_NEGATIVE_RATIO = 0.6  # 负面舆情比例阈值
    ALERT_HOTSPOT_THRESHOLD = 100  # 热点话题阈值

    # 文件路径
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR = os.path.join(BASE_DIR, '..', 'data')
    DICT_DIR = os.path.join(DATA_DIR, 'dictionaries')
    STOPWORDS_PATH = os.path.join(DATA_DIR, 'stopwords', 'stopwords.txt')

class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    SQLALCHEMY_ECHO = True

class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
