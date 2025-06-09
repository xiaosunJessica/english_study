<template>
  <div class="home">
    <header class="header">
      <div class="header-content">
        <div class="notebook-section">
          <div class="notebook-icon">📖</div>
          <span class="notebook-text">错词本</span>
          <span class="notebook-count">{{ wrongWords }}</span>
        </div>
        <div class="share-section">
          <div class="share-icon">🔗</div>
          <span class="share-text">分享</span>
        </div>
      </div>
    </header>

    <div class="live-section">
      <div class="live-badge">直播</div>
      <div class="live-info">
        <span class="live-time">06月06日 21:00</span>
        <span class="live-schedule">每周一至每周五 早7点</span>
      </div>
      <div class="live-title">口语带练 | Part2描述一个你的儿时好友</div>
      <button class="live-btn">去查看></button>
    </div>

    <div class="content">
      <div class="chapters-section">
        <div
          v-for="chapter in chapters"
          :key="chapter.id"
          class="chapter-card"
          @click="toggleChapter(chapter.id)"
        >
          <div class="chapter-header">
            <h3 class="chapter-title">{{ chapter.title }}</h3>
            <div class="chapter-icon" :class="{ expanded: expandedChapters.includes(chapter.id) }">
              ▼
            </div>
          </div>
          <p class="chapter-subtitle">{{ chapter.subtitle }}</p>

          <div v-if="expandedChapters.includes(chapter.id)" class="test-papers">
            <div
              v-for="paper in chapter.testPapers"
              :key="paper.id"
              class="test-paper"
              @click.stop="goToWordList(chapter.id, paper.id)"
            >
              <span class="paper-name">{{ paper.name }}</span>
              <span class="paper-accuracy">正确率{{ paper.accuracy }}%</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useVocabularyStore } from '../stores/vocabulary'
import { getCorpusList } from '../api/corpus'

const regex = /^(Chapter\s*\d+)\s*(.*)$/;

const router = useRouter()
const vocabularyStore = useVocabularyStore()

const { chapters, wrongWords, setChapters } = vocabularyStore
const expandedChapters = ref<number[]>([])

const toggleChapter = (chapterId: number) => {
  const index = expandedChapters.value.indexOf(chapterId)
  if (index > -1) {
    expandedChapters.value.splice(index, 1)
  } else {
    expandedChapters.value.push(chapterId)
  }
}

const goToWordList = (chapterId: number, paperId: number) => {
  router.push(`/wordlist/${chapterId}/${paperId}`)
}

onMounted(async () => {
  try {
    const res = await getCorpusList()
    console.log(res, '00000')
    console.log(res.data?.filter((item: any) => item.style === '2').map((item: any) => ({
      ...item,
      title: item.name.match(regex)?.[1] || '',
      subtitle: item.name.match(regex)?.[2] || '',
    })), '00000')
    setChapters(res.data?.filter((item: any) => item.style === '2').map((item: any) => ({
      ...item,
      title: item.name.match(regex)?.[1] || '',
      subtitle: item.name.match(regex)?.[2] || '',
      testPapers: item.list.map((paper: any) => ({
        ...paper,
        title: paper.name.match(regex)?.[1] || '',
        accuracy: paper.accuracy,
        words: paper.words
      }))
    })))
  } catch (error) {
    console.error('Failed to fetch corpus list:', error)
  }
})
</script>

<style scoped>
.home {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 20px;
}

.header {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 16px;
  padding: 16px 24px;
  margin-bottom: 20px;
  backdrop-filter: blur(10px);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.notebook-section {
  display: flex;
  align-items: center;
  gap: 8px;
}

.notebook-icon {
  font-size: 24px;
}

.notebook-text {
  font-size: 18px;
  font-weight: 500;
  color: #333;
}

.notebook-count {
  background: #e74c3c;
  color: white;
  border-radius: 20px;
  padding: 4px 12px;
  font-size: 14px;
  font-weight: bold;
}

.share-section {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.share-icon {
  font-size: 20px;
}

.share-text {
  font-size: 16px;
  color: #666;
}

.live-section {
  background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 50%, #fecfef 100%);
  border-radius: 16px;
  padding: 20px;
  margin-bottom: 24px;
  display: flex;
  align-items: center;
  gap: 16px;
  position: relative;
}

.live-badge {
  background: #e67e22;
  color: white;
  padding: 4px 12px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: bold;
}

.live-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.live-time {
  font-size: 16px;
  font-weight: bold;
  color: #333;
}

.live-schedule {
  font-size: 14px;
  color: #666;
}

.live-title {
  flex: 1;
  font-size: 18px;
  font-weight: 500;
  color: #333;
}

.live-btn {
  background: linear-gradient(135deg, #ff7b7b, #f9ca24);
  border: none;
  border-radius: 24px;
  padding: 12px 24px;
  color: white;
  font-weight: bold;
  cursor: pointer;
  transition: transform 0.2s;
}

.live-btn:hover {
  transform: translateY(-2px);
}

.content {
  max-width: 1200px;
  margin: 0 auto;
}

.chapters-section {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.chapter-card {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 16px;
  padding: 24px;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}

.chapter-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.chapter-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.chapter-title {
  font-size: 24px;
  font-weight: bold;
  color: #333;
  margin: 0;
}

.chapter-icon {
  font-size: 16px;
  color: #666;
  transition: transform 0.3s ease;
}

.chapter-icon.expanded {
  transform: rotate(180deg);
}

.chapter-subtitle {
  font-size: 16px;
  color: #666;
  margin: 0;
}

.test-papers {
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.test-paper {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  border-radius: 12px;
  padding: 16px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.test-paper:hover {
  transform: translateX(4px);
  box-shadow: 0 4px 16px rgba(240, 147, 251, 0.3);
}

.paper-name {
  font-size: 18px;
  font-weight: 500;
  color: white;
}

.paper-accuracy {
  font-size: 16px;
  color: rgba(255, 255, 255, 0.9);
}
</style>