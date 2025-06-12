<template>
  <div class="practice">
    <header class="header">
      <div class="progress-info">
        <span class="mode-title">拼写 ({{ currentIndex + 1 }}/{{ totalWords }})</span>
        <div class="toggle-group">
          <button class="toggle-btn">对答案</button>
          <button class="toggle-btn">巩固错词</button>
        </div>
      </div>
      <Countdown :seconds="countdown.timeLeft" :is-active="countdown.isActive" />
    </header>

    <div class="practice-area">
      <div class="word-display">
        <SpellingInput
            v-model=userInput
            :current-word=currentWord
            :is-correct=isCorrect
            @submit="handleSubmitAnswer"/>

      </div>

      <button class="next-word-btn" @click="nextWord">下个单词</button>

      <div class="controls">
        <button class="control-btn speed" @click="toggleSpeed">
          🔄 {{ currentSpeed }}倍速
        </button>
        <button class="control-btn" @click="playAudio">
          ⏮
        </button>
        <button class="control-btn play" @click="togglePlay">
          {{ isPlaying ? '⏸' : '▶️' }}
        </button>
        <button class="control-btn more" @click="repeat">
          再念一遍
        </button>
      </div>
    </div>

    <!-- Result Modal -->
    <div v-if="showResult" class="result-modal" @click="closeResult">
      <div class="result-content" @click.stop>
        <div class="result-word">
          <h3>{{ currentWord?.text }}</h3>
          <p>{{ currentWord?.note }}</p>
        </div>
        <div class="result-input">
          <p>您的输入: <span :class="{ correct: isCorrect, wrong: !isCorrect }">{{ userInput }}</span></p>
        </div>
        <div class="result-status">
          {{ isCorrect ? '✅ 正确!' : '❌ 错误' }}
        </div>
        <button class="continue-btn" @click="continueNext">继续</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { useVocabularyStore } from '@/stores/vocabulary'
import { getCorpusItem } from '@/api/corpus'
import Countdown from './components/Countdown.vue'
import { useCountdown } from '@/hooks/useCountdown'
import SpellingInput from './components/SpellingInput.vue'

interface Props {
  unitId: string
  lessonId: string
  mode: string
}

const props = defineProps<Props>()
const router = useRouter()
const vocabularyStore = useVocabularyStore()

const countdown = useCountdown(5, () => {
  console.log('countdown')
})

const currentIndex = ref(0)
const userInput = ref('')
const isPlaying = ref(false)
const isListening = ref(false)
const currentSpeed = ref(1.4)
const showResult = ref(false)
const isCorrect = ref(false)
const inputRef = ref<HTMLInputElement>()

const unitId = parseInt(props.unitId)
const lessonId = parseInt(props.lessonId)

const words = vocabularyStore.testPaper?.list || []

const totalWords = computed(() => vocabularyStore.testPaper?.word_count)
const currentWord = computed(() => words[currentIndex.value])

const speeds = [1.0, 1.2, 1.4, 1.6]

onMounted(() => {
  nextTick(() => {
    inputRef.value?.focus()
  })
})

const toggleSpeed = () => {
  const currentSpeedIndex = speeds.indexOf(currentSpeed.value)
  const nextIndex = (currentSpeedIndex + 1) % speeds.length
  currentSpeed.value = speeds[nextIndex]
}

const playAudio = () => {
  isListening.value = true
  setTimeout(() => {
    isListening.value = false
  }, 1000)
}

const togglePlay = () => {
  isPlaying.value = !isPlaying.value
  if (isPlaying.value) {
    playAudio()
  }
}

const repeat = () => {
  playAudio()
}

const submitWord = () => {
  if (!userInput.value.trim()) return

  isCorrect.value = userInput.value.toLowerCase().trim() === currentWord.value?.english.toLowerCase()
  showResult.value = true
}

const nextWord = () => {
  if (currentIndex.value < totalWords.value - 1) {
    currentIndex.value++
    userInput.value = ''
    nextTick(() => {
      inputRef.value?.focus()
    })
  } else {
    // Practice completed
    router.push(`/wordlist/${props.chapter}/${props.paper}`)
  }
}

const continueNext = () => {
  showResult.value = false
  nextWord()
}

const closeResult = () => {
  showResult.value = false
}

// handle submit answer
const handleSubmitAnswer = () => {
  countdown.stopCountdown()

}

onMounted(async () => {
  const res = await getCorpusItem({
    book_id: 0,
    unit_id: unitId,
    lesson_id: lessonId
  })

  vocabularyStore.setTestPaper(res.data)
})
</script>

<style scoped>
.practice {
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

.practice-area {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 40px;
  padding: 40px 20px;
}

.word-display {
  width: 100%;
  max-width: 500px;
}




@keyframes blink {
  0%, 50% { opacity: 1; }
  51%, 100% { opacity: 0; }
}

.next-word-btn {
  background: linear-gradient(135deg, #d6336c 0%, #f093fb 100%);
  border: none;
  border-radius: 24px;
  padding: 16px 32px;
  font-size: 18px;
  font-weight: bold;
  color: white;
  cursor: pointer;
  transition: all 0.2s ease;
  min-width: 160px;
}

.next-word-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(214, 51, 108, 0.3);
}

.controls {
  display: flex;
  gap: 16px;
  align-items: center;
}

.control-btn {
  background: rgba(255, 255, 255, 0.9);
  border: none;
  border-radius: 50%;
  width: 60px;
  height: 60px;
  font-size: 18px;
  cursor: pointer;
  transition: all 0.2s ease;
  backdrop-filter: blur(10px);
  display: flex;
  align-items: center;
  justify-content: center;
}

.control-btn.speed {
  border-radius: 30px;
  width: auto;
  padding: 0 20px;
  font-size: 14px;
}

.control-btn.play {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  width: 80px;
  height: 80px;
  font-size: 24px;
}

.control-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.result-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.result-content {
  background: white;
  border-radius: 20px;
  padding: 32px;
  max-width: 400px;
  width: 90%;
  text-align: center;
  box-shadow: 0 16px 48px rgba(0, 0, 0, 0.2);
}

.result-word h3 {
  font-size: 28px;
  color: #333;
  margin: 0 0 8px 0;
}

.result-word p {
  font-size: 18px;
  color: #666;
  margin: 0 0 20px 0;
}

.result-input {
  margin-bottom: 20px;
}

.result-input p {
  font-size: 16px;
  color: #333;
  margin: 0;
}

.correct {
  color: #27ae60;
  font-weight: bold;
}

.wrong {
  color: #e74c3c;
  font-weight: bold;
}

.result-status {
  font-size: 24px;
  margin-bottom: 24px;
}

.continue-btn {
  background: linear-gradient(135d, #27ae60 0%, #2ecc71 100%);
  border: none;
  border-radius: 24px;
  padding: 12px 24px;
  font-size: 16px;
  font-weight: bold;
  color: white;
  cursor: pointer;
  transition: all 0.2s ease;
}

.continue-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(39, 174, 96, 0.3);
}
</style>