<template>
  <div class="dashboard">
    <h1>网络舆情分析平台</h1>

    <el-row :gutter="20" style="margin-top: 20px">
      <!-- 情感分布 -->
      <el-col :span="8">
        <el-card>
          <template #header>
            <span>情感分布</span>
          </template>
          <div v-if="loading">加载中...</div>
          <v-chart v-else :option="sentimentOption" style="height: 300px" />
        </el-card>
      </el-col>

      <!-- 数据统计 -->
      <el-col :span="16">
        <el-card>
          <template #header>
            <span>数据统计</span>
          </template>
          <div style="padding: 20px">
            <el-statistic title="总数据量" :value="totalCount" />
            <div style="margin-top: 20px">
              <el-tag type="success">正面: {{ stats.positive }}</el-tag>
              <el-tag type="info" style="margin-left: 10px">中性: {{ stats.neutral }}</el-tag>
              <el-tag type="danger" style="margin-left: 10px">负面: {{ stats.negative }}</el-tag>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px">
      <!-- 文章列表 -->
      <el-col :span="24">
        <el-card>
          <template #header>
            <span>最新舆情 (共{{ totalCount }}条)</span>
          </template>
          <el-table :data="articles" height="500" v-loading="loading">
            <el-table-column prop="title" label="标题" width="400" />
            <el-table-column prop="source" label="来源" width="120">
              <template #default="{ row }">
                <el-tag>{{ getSourceLabel(row.source) }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="sentiment" label="情感" width="100">
              <template #default="{ row }">
                <el-tag :type="getSentimentType(row.sentiment)">
                  {{ getSentimentLabel(row.sentiment) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="sentiment_score" label="得分" width="100" />
            <el-table-column prop="view_count" label="浏览量" width="120" />
            <el-table-column prop="publish_time" label="发布时间" width="180" />
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import VChart from 'vue-echarts'
import api from '@/api'
import { ElMessage } from 'element-plus'

const loading = ref(true)
const sentimentOption = ref({})
const articles = ref([])
const totalCount = ref(0)
const stats = ref({ positive: 0, neutral: 0, negative: 0 })

const loadData = async () => {
  try {
    loading.value = true

    // 获取情感分布
    const distribution = await api.getSentimentDistribution()
    console.log('Distribution:', distribution)

    stats.value = {
      positive: distribution.data.positive || 0,
      neutral: distribution.data.neutral || 0,
      negative: distribution.data.negative || 0
    }

    totalCount.value = stats.value.positive + stats.value.neutral + stats.value.negative

    // 设置饼图
    sentimentOption.value = {
      tooltip: {
        trigger: 'item',
        formatter: '{b}: {c} ({d}%)'
      },
      legend: {
        orient: 'vertical',
        left: 'left'
      },
      series: [{
        type: 'pie',
        radius: '60%',
        data: [
          { value: stats.value.positive, name: '正面', itemStyle: { color: '#67C23A' } },
          { value: stats.value.neutral, name: '中性', itemStyle: { color: '#909399' } },
          { value: stats.value.negative, name: '负面', itemStyle: { color: '#F56C6C' } }
        ],
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
      }]
    }

    // 获取文章列表
    const articlesRes = await api.getArticles({ per_page: 20 })
    console.log('Articles:', articlesRes)
    articles.value = articlesRes.data.items || []

    ElMessage.success(`成功加载 ${totalCount.value} 条数据`)

  } catch (error) {
    console.error('加载数据失败:', error)
    ElMessage.error('加载数据失败: ' + error.message)
  } finally {
    loading.value = false
  }
}

const getSentimentType = (sentiment) => {
  const map = { positive: 'success', neutral: 'info', negative: 'danger' }
  return map[sentiment] || 'info'
}

const getSentimentLabel = (sentiment) => {
  const map = { positive: '正面', neutral: '中性', negative: '负面' }
  return map[sentiment] || '未知'
}

const getSourceLabel = (source) => {
  const map = {
    weibo: '微博',
    douyin: '抖音',
    bilibili: 'B站',
    xiaohongshu: '小红书'
  }
  return map[source] || source
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.dashboard {
  padding: 20px;
  background: #f0f2f5;
  min-height: 100vh;
}

h1 {
  color: #303133;
  margin-bottom: 20px;
}
</style>
