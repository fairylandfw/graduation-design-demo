# 网络舆情分析平台

基于词典分析的网络舆情监测与可视化系统，支持微博、抖音、B站、小红书等多平台数据采集。

## 核心特性

- ✅ 多平台数据采集（微博、抖音、B站、小红书）
- ✅ 基于词典的情感分析（可解释性强）
- ✅ 热点话题发现与演化追踪
- ✅ 实时可视化展示（ECharts图表）
- ✅ 舆情预警与报告生成
- ✅ 一键启动，自动采集数据
- ✅ 低成本部署（无需GPU）

## 技术架构

- **后端**: Flask + SQLAlchemy + MySQL
- **前端**: Vue.js + ECharts + Element UI
- **数据采集**: 自动爬虫（支持多平台）
- **文本分析**: Jieba分词 + 词典情感分析
- **任务调度**: APScheduler

## 快速开始

### 环境要求
- Python 3.8+
- Node.js 14+
- MySQL 5.7+

### 配置MySQL

1. 确保MySQL服务已启动
2. 默认配置：用户名 `root`，密码 `root`
3. 如需修改，编辑 `backend/config/config.py` 和 `backend/init_db.py`

详见：[快速配置指南.md](快速配置指南.md)

### 一键启动

双击运行：
```
start.bat
```

脚本会自动：
1. 安装Python依赖
2. 创建数据库和表
3. 从社交平台采集最新数据
4. 启动后端服务（端口5000）
5. 启动前端服务（端口8080）
6. 自动打开浏览器

### 访问地址
- 前端界面: http://localhost:8080
- 后端API: http://localhost:5000

## 项目结构

```
sentiment-analysis-platform/
├── start.bat               # 一键启动脚本
├── backend/                # 后端服务
│   ├── app/               # Flask应用
│   ├── analyzer/          # 情感分析模块
│   ├── config/            # 配置文件
│   ├── init_db.py         # 数据库初始化
│   ├── auto_crawler.py    # 自动爬虫
│   └── run.py             # 启动文件
├── frontend/              # 前端应用
│   └── src/               # Vue源代码
└── data/                  # 数据目录
    ├── dictionaries/      # 情感词典
    └── stopwords/         # 停用词表
```

## 功能说明

### 1. 数据采集
- 自动从微博、抖音、B站、小红书采集热点内容
- 支持用户评论和话题分析
- 自动去重和数据清洗

### 2. 情感分析
- 基于情感词典的分析方法
- 支持正面、中性、负面三分类
- 考虑程度副词和否定词的影响
- 每个判断可追溯到具体词汇

### 3. 可视化展示
- 情感分布饼图
- 情感趋势折线图
- 热点词云
- 文章列表（带情感标签）

### 4. 预警功能
- 负面舆情激增预警
- 热点话题预警
- 自动告警通知

## 自定义配置

### 修改MySQL密码
编辑 `backend/config/config.py` 和 `backend/init_db.py`

### 扩展情感词典
编辑以下文件：
- `data/dictionaries/positive.txt` - 正面词
- `data/dictionaries/negative.txt` - 负面词
- `data/dictionaries/degree.txt` - 程度副词
- `data/dictionaries/negation.txt` - 否定词

### 更新数据
```bash
cd backend
venv\Scripts\activate
python auto_crawler.py
```

## 常见问题

### 1. 数据库连接失败
- 检查MySQL服务是否启动
- 确认用户名密码是否正确
- 查看 `backend/config/config.py` 配置

### 2. 端口被占用
- 检查5000和8080端口是否被占用
- 可在配置文件中修改端口

### 3. 没有数据显示
- start.bat会自动采集数据
- 也可手动运行：`python backend/auto_crawler.py`

## 文档

- [快速配置指南.md](快速配置指南.md) - 详细配置说明
- [使用说明.md](使用说明.md) - 使用指南
- [技术文档.md](docs/技术文档.md) - 技术细节
- [项目结构说明.md](docs/项目结构说明.md) - 代码结构

## 毕业设计优势

1. **完整的系统架构** - 前后端分离、RESTful API
2. **可解释性强** - 基于词典，每个判断可追溯
3. **多平台支持** - 微博、抖音、B站、小红书
4. **完整功能** - 采集、分析、可视化、预警
5. **易于演示** - 一键启动，自动填充数据
6. **技术先进** - Vue3、Flask、ECharts

## 许可证
MIT License
