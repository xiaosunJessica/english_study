<template>
  <div class="study-mode">
    <header class="header">
      <div class="progress-info">
        <span class="mode-title">听写 (1/112)</span>
        <div class="toggle-group">
          <button class="toggle-btn">对答案</button>
          <button class="toggle-btn">巩固错词</button>
        </div>
      </div>
    </header>

    <div class="mode-selector">
      <div class="mode-title-section">
        <h2>学习模式</h2>
      </div>
      <div class="mode-grid">
        <button 
          v-for="mode in studyModes"
          :key="mode.id"
          class="mode-card"
          :class="{ active: selectedMode === mode.id }"
          @click="selectedMode = mode.id"
        >
          {{ mode.name }}
        </button>
      </div>
    </div>

    <div class="settings">
      <div class="setting-group">
        <label class="setting-label">播放倍速</label>
        <div class="speed-selector">
          <button 
            v-for="speed in playbackSpeeds"
            :key="speed"
            class="speed-btn"
            :class="{ active: selectedSpeed === speed }"
            @click="selectedSpeed = speed"
          >
            x{{ speed }}
          </button>
          <button class="speed-btn">自适应</button>
        </div>
      </div>

      <div class="setting-group">
        <label class="setting-label">对错反馈</label>
        <div class="feedback-selector">
          <button 
            class="feedback-btn"
            :class="{ active: !showFeedback }"
            @click="showFeedback = false"
          >
            拼写中不反馈
          </button>
          <button 
            class="feedback-btn"
            :class="{ active: showFeedback }"
            @click="showFeedback = true"
          >
            拼写中反馈
          </button>
        </div>
      </div>
    </div>

    <div class="info-section">
      <h3 class="info-title">什么是拼写模式？</h3>
      <p class="info-description">
        拼写模式专门为机考考生设计，是可以练习打字的语料库版本
      </p>
      
      <div class="features">
        <span class="feature-tag">自动识别错词</span>
        <span class="feature-tag">自动计算正确率</span>
        <span class="feature-tag">自动标记错词</span>
      </div>

      <div class="tips">
        <p class="tips-title">Tips: 建议用电脑版访问小程序练习</p>
        <p class="tips-subtitle">更贴近雅思机考场景</p>
      </div>

      <p class="note">
        * 自适应倍速需要在提交单词后手动播放下一个单词<br>
        电脑端使用时按<span class="highlight">空格键</span>可快速提交
      </p>
    </div>

    <button class="confirm-btn" @click="startPractice">确定</button>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

interface Props {
  chapter: string
  paper: string
}

const props = defineProps<Props>()
const router = useRouter()

const selectedMode = ref('spelling')
const selectedSpeed = ref(1.4)
const showFeedback = ref(false)

const studyModes = [
  { id: 'test', name: '测一测' },
  { id: 'recite', name: '背词模式' },
  { id: 'dictation', name: '听写对答案' },
  { id: 'spelling', name: '在线拼写' }
]

const playbackSpeeds = [1.0, 1.2, 1.4, 1.6]

const startPractice = () => {
  router.push(`/practice/${props.chapter}/${props.paper}/${selectedMode.value}`)
}
</script>

<style scoped>
.study-mode {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.header {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 16px;
  padding: 16px 24px;
  margin-bottom: 24px;
  backdrop-filter: blur(10px);
}

.progress-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.mode-title {
  font-size: 18px;
  font-weight: bold;
  color: #333;
}

.toggle-group {
  display: flex;
  gap: 8px;
}

.toggle-btn {
  background: rgba(255, 255, 255, 0.8);
  border: 2px solid #ddd;
  border-radius: 20px;
  padding: 8px 16px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.mode-selector {
  background: linear-gradient(135deg, #d6336c 0%, #f093fb 100%);
  border-radius: 16px;
  padding: 24px;
  margin-bottom: 24px;
}

.mode-title-section h2 {
  color: white;
  font-size: 20px;
  margin: 0 0 20px 0;
}

.mode-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
}

.mode-card {
  background: rgba(255, 255, 255, 0.9);
  border: none;
  border-radius: 12px;
  padding: 16px 12px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  text-align: center;
}

.mode-card.active {
  background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
  color: white;
  font-weight: bold;
}

.mode-card:hover:not(.active) {
  background: white;
  transform: translateY(-2px);
}

.settings {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 16px;
  padding: 24px;
  margin-bottom: 24px;
  backdrop-filter: blur(10px);
}

.setting-group {
  margin-bottom: 24px;
}

.setting-group:last-child {
  margin-bottom: 0;
}

.setting-label {
  display: block;
  font-size: 16px;
  font-weight: 500;
  color: #333;
  margin-bottom: 12px;
}

.speed-selector, .feedback-selector {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.speed-btn, .feedback-btn {
  background: rgba(240, 240, 240, 0.9);
  border: 2px solid transparent;
  border-radius: 20px;
  padding: 8px 16px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.speed-btn.active, .feedback-btn.active {
  background: white;
  border-color: #f093fb;
  color: #f093fb;
  font-weight: bold;
}

.info-section {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 16px;
  padding: 24px;
  margin-bottom: 24px;
  backdrop-filter: blur(10px);
}

.info-title {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  margin: 0 0 12px 0;
}

.info-description {
  color: #e74c3c;
  font-size: 16px;
  margin: 0 0 16px 0;
}

.features {
  display: flex;
  gap: 8px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.feature-tag {
  background: #ffebee;
  color: #e74c3c;
  border-radius: 12px;
  padding: 6px 12px;
  font-size: 12px;
  font-weight: 500;
}

.tips {
  margin-bottom: 16px;
}

.tips-title {
  color: #e74c3c;
  font-size: 16px;
  font-weight: 500;
  margin: 0 0 4px 0;
}

.tips-subtitle {
  color: #666;
  font-size: 14px;
  margin: 0;
}

.note {
  font-size: 12px;
  color: #666;
  line-height: 1.5;
  margin: 0;
}

.highlight {
  color: #e74c3c;
  font-weight: bold;
}

.confirm-btn {
  background: linear-gradient(135deg, #d6336c 0%, #f093fb 100%);
  border: none;
  border-radius: 24px;
  padding: 16px 32px;
  font-size: 18px;
  font-weight: bold;
  color: white;
  cursor: pointer;
  transition: all 0.2s ease;
  width: 100%;
}

.confirm-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(214, 51, 108, 0.3);
}
</style>