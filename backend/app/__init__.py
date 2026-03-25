from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config.config import config

db = SQLAlchemy()

def create_app(config_name='default'):
    """应用工厂函数"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # 初始化扩展
    db.init_app(app)
    CORS(app)

    # 注册蓝图
    from app.api import sentiment_bp, data_bp, analysis_bp, alert_bp
    app.register_blueprint(sentiment_bp, url_prefix='/api/sentiment')
    app.register_blueprint(data_bp, url_prefix='/api/data')
    app.register_blueprint(analysis_bp, url_prefix='/api/analysis')
    app.register_blueprint(alert_bp, url_prefix='/api/alert')

    # 创建数据库表
    with app.app_context():
        db.create_all()

    return app
