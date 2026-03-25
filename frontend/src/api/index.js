import axios from 'axios'

const request = axios.create({
  baseURL: 'http://localhost:5000/api',
  timeout: 10000
})

request.interceptors.response.use(
  response => response.data,
  error => {
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)

export default {
  // 数据接口
  getArticles(params) {
    return request.get('/data/articles', { params })
  },

  // 情感分析
  analyzeSentiment(text) {
    return request.post('/sentiment/analyze', { text })
  },

  // 统计分析
  getSentimentDistribution(params) {
    return request.get('/analysis/sentiment-distribution', { params })
  },

  getHotwords(params) {
    return request.get('/analysis/hotwords', { params })
  },

  getSentimentTrend(params) {
    return request.get('/analysis/trend', { params })
  },

  // 预警
  getAlerts(params) {
    return request.get('/alert/list', { params })
  }
}
