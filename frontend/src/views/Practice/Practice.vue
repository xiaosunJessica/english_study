<template>
  <div class="min-h-screen bg-gray-50 flex flex-col">
    <header
      class="flex items-center justify-between bg-white/90 px-6 py-4 mb-6 backdrop-blur-md shadow-sm"
    >
      <div class="progress-info">
        <span class="text-lg font-bold text-gray-800">
          拼写 ({{ currentIndex + 1 }}/{{ totalWords }})
        </span>
      </div>
      <Countdown :seconds="countdown.timeLeft?.value" :is-active="countdown.isActive?.value" />
    </header>

    <div class="flex flex-col flex-1">
      <div class="flex-1 flex flex-col justify-center">
        <SpellingInput
          v-model="userInput"
          :current-word="currentWord?.value?.note || ''"
          :is-correct="isCorrect"
          @submit="handleSubmitAnswer"
        />
      </div>

      <div class="bg-white border-t border-gray-200 space-y-4">
        <div
          class="flex justify-center items-center gap-6 px-6 py-4"
        >
          <button
            class="p-0 rounded-full bg-white/90 border-none py-2 px-5 text-sm cursor-pointer backdrop-blur-md hover:shadow-md transition-transform duration-200 ease-in-out"
            @click="toggleSpeed"
          >
            🔄 {{ currentSpeed }}倍速
          </button>
          <button
            class="p-0 rounded-full bg-white/90 border-none w-14 h-14 flex items-center justify-center cursor-pointer backdrop-blur-md hover:shadow-md transition-transform duration-200 ease-in-out"
            @click="prevWord"
          >
            <img src="@/assets/icon-prev.svg" alt="prev" />
          </button>
          <button
            class="p-0 rounded-full bg-white/90 border-none w-14 h-14 flex items-center justify-center cursor-pointer backdrop-blur-md hover:shadow-md transition-transform duration-200 ease-in-out"
            @click="togglePlay"
          >
            <img
              v-if="isPlaying"
              src="@/assets/icon-pause.svg"
              alt="pause"
            />
            <img
              v-else
              src="@/assets/icon-play.svg"
              alt="play"
            />
          </button>
          <button
            class="p-0 more rounded-full bg-white/90 border-none w-14 h-14 flex items-center justify-center cursor-pointer backdrop-blur-md hover:shadow-md transition-transform duration-200 ease-in-out"
            @click="repeat"
          >
            <img src="@/assets/icon-repeat-one.svg" alt="repeat" />
          </button>
        </div>
      </div>
    </div>

    <!-- Result Modal -->
    <div
      v-if="showResult"
      class="fixed inset-0 bg-black bg-opacity-60 flex items-center justify-center z-50"
      @click="closeResult"
    >
      <div
        class="bg-white rounded-2xl p-8 max-w-sm w-11/12 text-center shadow-2xl"
        @click.stop
      >
        <div class="mb-4">
          <h3 class="text-3xl font-semibold text-gray-800 mb-2">
            {{ currentWord?.text }}
          </h3>
          <p class="text-lg text-gray-600">{{ currentWord?.note }}</p>
        </div>
        <div class="mb-6 text-lg text-gray-800">
          <p>
            您的输入:
            <span
              :class="{
                'text-green-600 font-bold': isCorrect,
                'text-red-600 font-bold': !isCorrect,
              }"
            >
              {{ userInput }}
            </span>
          </p>
        </div>
        <div
          class="text-2xl mb-6"
          :class="{
            'text-green-600': isCorrect,
            'text-red-600': !isCorrect,
          }"
        >
          {{ isCorrect ? '✅ 正确!' : '❌ 错误' }}
        </div>
        <button
          class="bg-gradient-to-r from-green-600 to-green-500 text-white rounded-3xl px-6 py-3 font-bold text-lg hover:shadow-lg hover:translate-y-[-4px] transition-transform duration-200 ease-in-out"
          @click="continueNext"
        >
          继续
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, nextTick, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useVocabularyStore, type Word } from '@/stores/vocabulary'
import { getCorpusItem } from '@/api/corpus'
import Countdown from './components/Countdown.vue'
import { useCountdown } from '@/hooks/useCountdown'
import SpellingInput from './components/SpellingInput.vue'
import { useAudio } from '@/hooks/useAudio'

interface Props {
  unitId: string
  lessonId: string
  mode: string
}

const COUNTDOWN_NUMBER = 5
const props = defineProps<Props>()
const router = useRouter()
const vocabularyStore = useVocabularyStore()

// 倒计时
const countdown = useCountdown(5, () => {
  nextWord()
})

// 音频控件
const audio = useAudio()

const currentIndex = ref(0)
const userInput = ref('')
const isPlaying = ref(false)
const isListening = ref(false)
const currentSpeed = ref(1.0)
const showResult = ref(false)
const isCorrect = ref(false)
const inputRef = ref<HTMLInputElement>()

const unitId = parseInt(props.unitId)
const lessonId = parseInt(props.lessonId)

const words = computed <Word[]>(() => vocabularyStore.testPaper?.list || [])
const totalWords = computed(() => vocabularyStore.testPaper?.word_count)
const currentWord = computed(() => words.value[currentIndex.value])

const speeds = [1.0, 1.2, 1.4, 1.6]



const toggleSpeed = () => {
  const currentSpeedIndex = speeds.indexOf(currentSpeed.value)
  const nextIndex = (currentSpeedIndex + 1) % speeds.length
  currentSpeed.value = speeds[nextIndex]
  audio.changePlaybackRate(currentSpeed.value)
}



const togglePlay = () => {
  isPlaying.value = !isPlaying.value
  if (isPlaying.value) {
    countdown.reset(COUNTDOWN_NUMBER)
    countdown.start()
    audio.play(currentWord.value?.url)
  } else {
    countdown.stop()
    audio.pause()
  }
}

const repeat = () => {
  // playAudio()
}

const submitWord = () => {
  if (!userInput.value.trim()) return

  isCorrect.value = userInput.value.toLowerCase().trim() === currentWord.value?.english.toLowerCase()
  showResult.value = true
}

// 上一个
const prevWord = () => {
  isListening.value = true
  if (currentIndex.value > 1) {
    currentIndex.value--
    userInput.value = ''
    nextTick(() => {
      inputRef.value?.focus()
    })
    countdown.reset(COUNTDOWN_NUMBER)
    if (currentWord.value?.url) {
      audio.play(currentWord.value?.url)
    }
    countdown.start()
  }
}
// 下一个
const nextWord = () => {
  if (currentIndex.value < totalWords.value - 1) {
    currentIndex.value++
    userInput.value = ''
    nextTick(() => {
      inputRef.value?.focus()
    })
    countdown.reset(COUNTDOWN_NUMBER)
    if (currentWord.value?.url) {
      audio.play(currentWord.value?.url)
    }
    countdown.start()
  } else {
    // Practice completed
    router.push(`/wordlist/${props.unitId}/${props.lessonId}`)
  }
}

//


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
  // input focus
  nextTick(() => {
    inputRef.value?.focus()
  })
  // get data
  const res = await getCorpusItem({
    book_id: 0,
    unit_id: unitId,
    lesson_id: lessonId
  })
  vocabularyStore.setTestPaper(res.data)
})
</script>

<style scoped>
@keyframes blink {
  0%, 50% {
    opacity: 1;
  }
  51%, 100% {
    opacity: 0;
  }
}
.animate-blink {
  animation: blink 1s step-start infinite;
}
</style>