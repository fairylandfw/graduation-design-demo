from flask import Blueprint, request, jsonify
from app.models.models import Article
from app import db
from analyzer.sentiment_analyzer import SentimentAnalyzer
from analyzer.topic_analyzer import TopicAnalyzer
from config.config import Config
from datetime import datetime, timedelta

sentiment_bp = Blueprint('sentiment', __name__)
data_bp = Blueprint('data', __name__)
analysis_bp = Blueprint('analysis', __name__)
alert_bp = Blueprint('alert', __name__)

# 初始化分析器
sentiment_analyzer = SentimentAnalyzer(Config.DICT_DIR)
topic_analyzer = TopicAnalyzer(Config.STOPWORDS_PATH)

@data_bp.route('/articles', methods=['GET'])
def get_articles():
    """获取文章列表"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    source = request.args.get('source')
    sentiment = request.args.get('sentiment')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    query = Article.query

    if source:
        query = query.filter_by(source=source)
    if sentiment:
        query = query.filter_by(sentiment=sentiment)
    if start_date:
        query = query.filter(Article.publish_time >= datetime.fromisoformat(start_date))
    if end_date:
        query = query.filter(Article.publish_time <= datetime.fromisoformat(end_date))

    pagination = query.order_by(Article.publish_time.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return jsonify({
        'code': 200,
        'data': {
            'items': [article.to_dict() for article in pagination.items],
            'total': pagination.total,
            'page': page,
            'per_page': per_page
        }
    })

@sentiment_bp.route('/analyze', methods=['POST'])
def analyze_sentiment():
    """分析文本情感"""
    data = request.get_json()
    text = data.get('text', '')

    if not text:
        return jsonify({'code': 400, 'message': '文本不能为空'}), 400

    sentiment, score = sentiment_analyzer.analyze(text)
    keywords = topic_analyzer.extract_keywords(text, topK=5)

    return jsonify({
        'code': 200,
        'data': {
            'sentiment': sentiment,
            'score': score,
            'keywords': keywords
        }
    })

@analysis_bp.route('/sentiment-distribution', methods=['GET'])
def sentiment_distribution():
    """情感分布统计"""
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    query = Article.query
    if start_date:
        query = query.filter(Article.publish_time >= datetime.fromisoformat(start_date))
    if end_date:
        query = query.filter(Article.publish_time <= datetime.fromisoformat(end_date))

    articles = query.all()

    distribution = {'positive': 0, 'neutral': 0, 'negative': 0}
    for article in articles:
        if article.sentiment:
            distribution[article.sentiment] = distribution.get(article.sentiment, 0) + 1

    return jsonify({
        'code': 200,
        'data': distribution
    })

@analysis_bp.route('/hotwords', methods=['GET'])
def get_hotwords():
    """获取热词"""
    days = request.args.get('days', 7, type=int)
    topK = request.args.get('topK', 50, type=int)

    start_date = datetime.now() - timedelta(days=days)
    articles = Article.query.filter(Article.publish_time >= start_date).all()

    texts = [article.content for article in articles]
    hotwords = topic_analyzer.extract_hotwords(texts, topK=topK)

    return jsonify({
        'code': 200,
        'data': hotwords
    })

@analysis_bp.route('/trend', methods=['GET'])
def sentiment_trend():
    """情感趋势分析"""
    days = request.args.get('days', 7, type=int)

    trend_data = []
    for i in range(days):
        date = datetime.now() - timedelta(days=days-i-1)
        start = date.replace(hour=0, minute=0, second=0)
        end = date.replace(hour=23, minute=59, second=59)

        articles = Article.query.filter(
            Article.publish_time >= start,
            Article.publish_time <= end
        ).all()

        sentiment_count = {'positive': 0, 'neutral': 0, 'negative': 0}
        for article in articles:
            if article.sentiment:
                sentiment_count[article.sentiment] += 1

        trend_data.append({
            'date': date.strftime('%Y-%m-%d'),
            'positive': sentiment_count['positive'],
            'neutral': sentiment_count['neutral'],
            'negative': sentiment_count['negative']
        })

    return jsonify({
        'code': 200,
        'data': trend_data
    })

@alert_bp.route('/list', methods=['GET'])
def get_alerts():
    """获取预警列表"""
    from app.models.models import Alert

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    pagination = Alert.query.order_by(Alert.create_time.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return jsonify({
        'code': 200,
        'data': {
            'items': [alert.to_dict() for alert in pagination.items],
            'total': pagination.total
        }
    })
