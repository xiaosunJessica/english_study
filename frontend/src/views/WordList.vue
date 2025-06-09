<template>
  <div class="word-list">
    <header class="header">
      <button class="back-btn" @click="goBack">←</button>
      <button class="home-btn" @click="goHome">🏠</button>
      <h1 class="title">{{ pageTitle }}</h1>
    </header>

    <div class="tabs">
      <button 
        class="tab" 
        :class="{ active: activeTab === 'all' }"
        @click="activeTab = 'all'"
      >
        全部({{ allWords.length }})
      </button>
      <button 
        class="tab" 
        :class="{ active: activeTab === 'wrong' }"
        @click="activeTab = 'wrong'"
      >
        近期错词({{ wrongWords.length }})
      </button>
    </div>

    <div class="word-container">
      <div 
        v-for="(word, index) in displayWords"
        :key="word.id"
        class="word-item"
      >
        <div class="word-number">{{ index + 1 }}.</div>
        <div class="word-content">
          <div class="word-english">{{ word.english }}</div>
          <div class="word-chinese">{{ word.chinese }}</div>
        </div>
        <div v-if="word.isWrong" class="wrong-indicator">
          错过{{ word.wrongCount }}次
        </div>
      </div>
    </div>

    <div class="actions">
      <button class="action-btn secondary" @click="startFromWord">从某词开始</button>
      <button class="action-btn primary" @click="startStudy">开始学习</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useVocabularyStore } from '../stores/vocabulary'

interface Props {
  chapter: string
  paper: string
}

const props = defineProps<Props>()
const router = useRouter()
const vocabularyStore = useVocabularyStore()

const activeTab = ref<'all' | 'wrong'>('all')

const chapterId = parseInt(props.chapter)
const paperId = parseInt(props.paper)

const testPaper = vocabularyStore.getTestPaper(chapterId, paperId)
const chapter = vocabularyStore.getChapter(chapterId)

const pageTitle = computed(() => {
  return `${chapter?.title} ${testPaper?.name}`
})

const allWords = computed(() => testPaper?.words || [])
const wrongWords = computed(() => allWords.value.filter(word => word.isWrong))

const displayWords = computed(() => {
  return activeTab.value === 'all' ? allWords.value : wrongWords.value
})

const goBack = () => {
  router.go(-1)
}

const goHome = () => {
  router.push('/')
}

const startFromWord = () => {
  // Implementation for starting from specific word
  console.log('Start from specific word')
}

const startStudy = () => {
  router.push(`/study/${chapterId}/${paperId}`)
}
</script>

<style scoped>
.word-list {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
}

.back-btn, .home-btn {
  background: rgba(255, 255, 255, 0.9);
  border: none;
  border-radius: 12px;
  width: 48px;
  height: 48px;
  font-size: 20px;
  cursor: pointer;
  transition: all 0.2s ease;
  backdrop-filter: blur(10px);
}

.back-btn:hover, .home-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.title {
  font-size: 24px;
  font-weight: bold;
  color: #333;
  margin: 0;
}

.tabs {
  display: flex;
  gap: 8px;
  margin-bottom: 24px;
}

.tab {
  background: rgba(255, 255, 255, 0.7);
  border: none;
  border-radius: 24px;
  padding: 12px 24px;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.2s ease;
  backdrop-filter: blur(10px);
}

.tab.active {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: white;
  font-weight: bold;
}

.tab:hover:not(.active) {
  background: rgba(255, 255, 255, 0.9);
}

.word-container {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 16px;
  padding: 24px;
  margin-bottom: 24px;
  backdrop-filter: blur(10px);
  max-height: 60vh;
  overflow-y: auto;
}

.word-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px 0;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.word-item:last-child {
  border-bottom: none;
}

.word-number {
  font-size: 18px;
  font-weight: bold;
  color: #666;
  min-width: 30px;
}

.word-content {
  flex: 1;
}

.word-english {
  font-size: 20px;
  font-weight: bold;
  color: #333;
  margin-bottom: 4px;
}

.word-chinese {
  font-size: 16px;
  color: #666;
}

.wrong-indicator {
  background: #ff6b6b;
  color: white;
  border-radius: 12px;
  padding: 4px 12px;
  font-size: 12px;
  font-weight: bold;
}

.actions {
  display: flex;
  gap: 16px;
  justify-content: center;
}

.action-btn {
  border: none;
  border-radius: 24px;
  padding: 16px 32px;
  font-size: 18px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.2s ease;
  min-width: 160px;
}

.action-btn.secondary {
  background: rgba(255, 255, 255, 0.9);
  color: #333;
  backdrop-filter: blur(10px);
}

.action-btn.primary {
  background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
  color: white;
}

.action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
}
</style>