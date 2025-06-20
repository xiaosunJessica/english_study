<template>
  <div class="min-h-screen bg-gray-50 flex flex-col">
    <header
      class="flex items-center justify-between bg-white/90 px-6 py-4 mb-6 backdrop-blur-md shadow-sm"
    >
      <div class="progress-info">
        <span class="text-lg font-bold text-gray-800">
          拼写 ({{ currentIndex + 1 }}/{{ words.length }})
        </span>
      </div>
      <Countdown :seconds="countdown.timeLeft?.value" :is-active="countdown.isActive?.value" />
    </header>
    <Progress
      :current-index="currentIndex"
      :words="words"
      :is-start="isStart" />
    <SpellingInput
      ref="spellingInputRef"
      v-model="userInput"
      :current-word="currentWord"
      :is-start="isStart"
      @submit="handleSubmitAnswer"
      @toggle-play="togglePlay"
      />
    <btn-group
      :current-index="currentIndex"
      :words="words"
      :is-playing="isPlaying"
      :current-speed="currentSpeed"
      @prev="prevWord"
      @toggle-play="togglePlay"
      @next="nextWord"
      @speed-change="handleSpeedChange"
      @repeat="handleRepeat"/>

  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, nextTick } from 'vue'
import { useVocabularyStore, type Word } from '@/stores/vocabulary'
import { getCorpusItem, setErrorWord } from '@/api/corpus'
import Countdown from './components/Countdown.vue'
import { useCountdown } from '@/hooks/useCountdown'
import SpellingInput from './components/SpellingInput.vue'
import { useAudio } from '@/hooks/useAudio'
import Progress from './components/Progress.vue'
import BtnGroup from './components/BtnGroup.vue'

// props属性
interface Props {
  unitId: string
  lessonId: string
  tabId: string
}
const props = defineProps<Props>()
// 是否开始，因为浏览器不允许自动播放，需要点击才执行
const isStart = ref(false)

// 获取url参数
const unitId = parseInt(props.unitId)
const lessonId = parseInt(props.lessonId)
const tabId = props.tabId

// 倒计时
const COUNTDOWN_NUMBER = 5
const vocabularyStore = useVocabularyStore()



// 计算单词
const currentIndex = ref(0)
const words = computed <Word[]>(() => {
  if (tabId == 'all') {
    return vocabularyStore.testPaper?.list || []
  }
  return vocabularyStore.testPaper?.list.filter((t) => t.is_wrong == 2) || []
})
const currentWord = computed(() => words.value[currentIndex.value])

// 倒计时
const countdown = useCountdown(COUNTDOWN_NUMBER, () => {
  nextWord()
})

// input
const spellingInputRef = ref()
const userInput = ref('')

// 音频控件
const audio = useAudio()

// 记录错误结果
const vocabularyErrorMap = ref(new Map<string, string>())

// 正在播放
const isPlaying = ref(false)
const currentSpeed = ref(1.0)

// 上一个
const prevWord = () => {
  isStart.value = true
  if (currentIndex.value > 1) {
    currentIndex.value--
    userInput.value = ''
    nextTick(() => {
      spellingInputRef.value?.focus()
    })
    countdown.reset()
    if (currentWord.value?.url) {
      audio.play(currentWord.value?.url)
    }
    countdown.start()
  }
}

// 下一个
const nextWord = () => {
  isStart.value = true
  // 先提交
  spellingInputRef.value?.handleSubmit()
  // 切换word
  if (currentIndex.value < words.value.length - 1) {
    currentIndex.value++
    userInput.value = ''
    nextTick(() => {
      spellingInputRef.value?.focus()
    })
    countdown.reset()
    if (currentWord.value?.url) {
      audio.play(currentWord.value?.url)
    }
    countdown.start()
  } else {
    isPlaying.value = false
    setErrorWord({
      lesson_id: props.lessonId,
      unit_id: props.unitId,
      errorWords: Object.fromEntries(vocabularyErrorMap.value.entries())
    })
    // Practice completed
    // router.push(`/wordlist/${props.unitId}/${props.lessonId}`)
  }
}

//播放
const togglePlay = () => {
  isStart.value = true
  isPlaying.value = !isPlaying.value
  spellingInputRef.value?.focus()
  if (isPlaying.value) {
    countdown.reset()
    countdown.start()
    audio.play(currentWord.value?.url)
  } else {
    countdown.stop()
    audio.pause()
  }
}

// 重新播放
const handleRepeat = () => {
  isStart.value = true
  isPlaying.value = true
  countdown.reset()
  countdown.start()
  audio.play(currentWord.value?.url)
}

// 播放速度
const handleSpeedChange = (speed: number) => {
  currentSpeed.value = speed
  audio.changePlaybackRate(currentSpeed.value)
}

// handle submit answer
const handleSubmitAnswer = (answer: Partial<Word & {inputValue: string}>) => {
  // 如果校验正确，且之前错误，清除
  if (answer.inputValue == answer.text && answer.id && vocabularyErrorMap.value.get(`${answer.id}`)) {
    vocabularyErrorMap.value.delete(`${answer.id}`)
  }

  // 如果错误，不管以前是否存在，直接替换
  if (answer.inputValue != answer.text && answer.id) {
    vocabularyErrorMap.value.set(`${answer.id}`, answer.inputValue || '')
  }
}

// 获取数据
onMounted(async () => {
  // get data
  const res = await getCorpusItem({
    book_id: 0,
    unit_id: unitId,
    lesson_id: lessonId
  })
  await vocabularyStore.setTestPaper(res.data)
})
</script>

<style scoped>

</style>