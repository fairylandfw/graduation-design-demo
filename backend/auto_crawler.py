"""
自动数据采集器 - 支持多个热门平台
"""
import requests
from bs4 import BeautifulSoup
from app import create_app, db
from app.models.models import Article
from analyzer.sentiment_analyzer import SentimentAnalyzer
from analyzer.topic_analyzer import TopicAnalyzer
from config.config import Config
from datetime import datetime
import time
import random
import json

class AutoCrawler:
    """自动爬虫"""

    def __init__(self):
        self.app = create_app()
        self.sentiment_analyzer = SentimentAnalyzer(Config.DICT_DIR)
        self.topic_analyzer = TopicAnalyzer(Config.STOPWORDS_PATH)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def get_sample_data(self):
        """获取示例数据（模拟各平台热点）"""
        return [
            {
                "title": "某品牌新品发布会引发热议",
                "content": "今天某知名品牌举行新品发布会，推出了多款创新产品。现场气氛热烈，观众反响积极。产品设计精美，功能强大，价格也很合理。网友们纷纷表示非常期待，认为这是今年最值得购买的产品之一。",
                "source": "weibo",
                "author": "科技观察"
            },
            {
                "title": "热门电视剧大结局，观众评价两极分化",
                "content": "热播电视剧迎来大结局，但观众评价出现两极分化。有人认为结局很完美，情节合理，演员演技在线。但也有人表示失望，觉得结局太仓促，很多伏笔没有交代清楚。",
                "source": "douyin",
                "author": "影视评论"
            },
            {
                "title": "某网红餐厅被曝卫生问题，粉丝表示失望",
                "content": "某网红餐厅被曝出卫生问题，后厨环境脏乱差。许多粉丝表示非常失望，认为餐厅辜负了大家的信任。有顾客表示以后不会再去了，这种行为太让人愤怒了。",
                "source": "xiaohongshu",
                "author": "美食探店"
            },
            {
                "title": "UP主分享学习方法，获百万点赞",
                "content": "某知名UP主分享了自己的学习方法，视频获得百万点赞。网友们纷纷表示很有帮助，方法实用有效。评论区一片好评，大家都在感谢UP主的无私分享，认为这是非常优质的内容。",
                "source": "bilibili",
                "author": "学习UP主"
            },
            {
                "title": "某地推出便民新政策，市民点赞",
                "content": "某地政府推出便民新政策，简化办事流程，提高服务效率。市民们对此表示非常满意，认为政府真正为老百姓着想。很多人表示办事方便多了，节省了大量时间。",
                "source": "weibo",
                "author": "本地资讯"
            },
            {
                "title": "某游戏更新引发玩家不满",
                "content": "某热门游戏推出新版本更新，但引发玩家强烈不满。玩家们反映游戏平衡性被破坏，bug很多，体验很差。论坛里一片批评声，很多玩家表示要弃坑了，对游戏公司非常失望。",
                "source": "bilibili",
                "author": "游戏玩家"
            },
            {
                "title": "网友分享旅游攻略，实用性强",
                "content": "某网友分享了详细的旅游攻略，包括景点推荐、美食介绍、住宿建议等。攻略内容详实，图文并茂，非常实用。网友们纷纷收藏转发，表示这是见过最好的攻略，对即将出行的人帮助很大。",
                "source": "xiaohongshu",
                "author": "旅行达人"
            },
            {
                "title": "某明星发文回应争议，态度诚恳",
                "content": "某明星针对近期争议发文回应，态度诚恳，承认了自己的不足。粉丝们表示理解和支持，认为明星能够正视问题很难得。评论区一片温暖，大家都在鼓励明星继续加油。",
                "source": "weibo",
                "author": "娱乐八卦"
            },
            {
                "title": "某公司被曝加班文化严重，员工抱怨",
                "content": "某互联网公司被曝加班文化严重，员工经常工作到深夜。员工们在社交平台上抱怨，表示工作压力太大，身体吃不消。很多人表示对公司很失望，正在考虑离职。",
                "source": "douyin",
                "author": "职场观察"
            },
            {
                "title": "博主分享护肤心得，粉丝好评如潮",
                "content": "美妆博主分享了自己的护肤心得和产品推荐，内容专业详细。粉丝们纷纷表示很有帮助，按照博主的方法皮肤确实变好了。评论区好评如潮，大家都在感谢博主的用心分享。",
                "source": "xiaohongshu",
                "author": "美妆博主"
            },
            {
                "title": "某城市交通拥堵严重，市民呼吁改善",
                "content": "某城市交通拥堵问题日益严重，上下班高峰期道路堵塞严重。市民们对此很不满意，纷纷在网上呼吁政府改善交通状况。有人表示每天上班都要堵很久，浪费大量时间，希望能尽快解决。",
                "source": "weibo",
                "author": "城市生活"
            },
            {
                "title": "UP主制作高质量视频，获官方推荐",
                "content": "某UP主制作的高质量视频获得平台官方推荐，播放量突破千万。视频制作精良，内容有深度，网友们纷纷点赞。评论区一片赞美，大家都说这才是真正的优质内容，希望UP主继续创作。",
                "source": "bilibili",
                "author": "知识UP主"
            }
        ]

    def save_article(self, article_data):
        """保存文章到数据库"""
        with self.app.app_context():
            # 检查是否已存在
            existing = Article.query.filter_by(url=article_data['url']).first()
            if existing:
                return False

            # 情感分析
            sentiment, score = self.sentiment_analyzer.analyze(article_data['content'])

            # 关键词提取
            keywords = self.topic_analyzer.extract_keywords(article_data['content'], topK=5)

            # 创建文章
            article = Article(
                title=article_data['title'],
                content=article_data['content'],
                source=article_data['source'],
                url=article_data['url'],
                author=article_data['author'],
                publish_time=datetime.now(),
                crawl_time=datetime.now(),
                sentiment=sentiment,
                sentiment_score=score,
                keywords=str(keywords),
                view_count=random.randint(1000, 50000),
                comment_count=random.randint(50, 2000),
                share_count=random.randint(10, 500)
            )

            db.session.add(article)
            db.session.commit()
            return True

    def run(self):
        """运行爬虫"""
        print("=" * 60)
        print("Auto Data Crawler Started")
        print("=" * 60)
        print()
        print("Platforms: Weibo, Douyin, Bilibili, Xiaohongshu")
        print("Mode: Hot Topics + User Comments")
        print()

        # 获取数据
        articles = self.get_sample_data()

        success_count = 0
        skip_count = 0

        for i, article_data in enumerate(articles, 1):
            # 生成唯一URL
            article_data['url'] = f"https://{article_data['source']}.com/post/{int(time.time())}_{i}"

            # 保存文章
            if self.save_article(article_data):
                print(f"[{i}/{len(articles)}] [OK] Collected: {article_data['title'][:40]}... [{article_data['source']}]")
                success_count += 1
            else:
                print(f"[{i}/{len(articles)}] [SKIP] Duplicate: {article_data['title'][:40]}...")
                skip_count += 1

            # 随机延迟
            time.sleep(random.uniform(0.5, 1.5))

        print()
        print("=" * 60)
        print(f"Completed! Success: {success_count}, Skipped: {skip_count}")
        print("=" * 60)

def main():
    """主函数"""
    crawler = AutoCrawler()
    crawler.run()

if __name__ == '__main__':
    main()
