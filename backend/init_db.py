"""
数据库初始化脚本
创建数据库和表
"""
import pymysql

# 数据库配置
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = '123456'
DB_NAME = 'sentiment_db'

def init_database():
    """初始化数据库"""
    try:
        # 连接MySQL（不指定数据库）
        connection = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            charset='utf8mb4'
        )

        cursor = connection.cursor()

        # 创建数据库（如果不存在）
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print(f"[OK] Database '{DB_NAME}' created/verified")

        cursor.close()
        connection.close()

        # 创建表
        from app import create_app, db
        app = create_app()
        with app.app_context():
            db.create_all()
            print("[OK] Tables created successfully")

        print("\nDatabase initialization completed!")
        return True

    except Exception as e:
        print(f"\nError: {e}")
        print("\nPlease check:")
        print("1. MySQL service is running")
        print("2. Username and password are correct (current: root/123456)")
        print("3. To change password, edit backend/init_db.py")
        return False

if __name__ == '__main__':
    print("=" * 50)
    print("Database Initialization")
    print("=" * 50)
    print()
    init_database()
