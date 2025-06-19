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

    <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
      <h3 class="text-lg font-semibold text-gray-800 mb-4">进度统计</h3>
      <div class="space-y-3">
        <div class="flex justify-between">
          <span class="text-gray-600">当前进度</span>
          <span class="font-medium">{{ currentIndex }}/{{ words.length }}</span>
        </div>
        <div class="w-full bg-gray-200 rounded-full h-2">
          <div
            class="bg-pink-500 h-2 rounded-full transition-all duration-300"
            :style="{ width: `${((currentIndex) / words.length) * 100}%` }"
          ></div>
        </div>
        <div class="flex justify-between text-sm text-gray-500">
          <span>完成度: {{ Math.round(((currentIndex) / words.length) * 100) }}%</span>
          <span>剩余: {{ words.length - currentIndex }}</span>
        </div>
      </div>
    </div>

    <div class="flex flex-col flex-1">
      <div class="flex-1 flex flex-col justify-center">
        <SpellingInput
          ref="spellingInputRef"
          v-model="userInput"
          :current-word="currentWord"
          :is-correct="isCorrect"
          @submit="handleSubmitAnswer"
        />
      </div>

      <div class="bg-white border-t border-gray-200 space-y-4">
        <div
          class="flex justify-center items-center gap-6 px-6 py-4"
        >

        <button
          type="button"
          class="p-4 bg-gray-100 rounded-full hover:bg-gray-200 transition-colors active:scale-95"
          title="调整播放速度"
        >
          <Volume2 :size="24" class="text-gray-600" />
        </button>
        <button
          class="p-0 rounded-full bg-white/90 border-none py-2 px-5 text-sm cursor-pointer backdrop-blur-md hover:shadow-md transition-transform duration-200 ease-in-out"
          @click="toggleSpeed"
        >
          🔄 {{ currentSpeed }}倍速
        </button>

        <button
          type="button"
          class="cursor-pointer p-4 bg-gray-100 rounded-full hover:bg-gray-200 transition-colors disabled:opacity-50 disabled:cursor-not-allowed active:scale-95"
          :disabled="currentIndex === 0"
          @click="prevWord"
        >
          <SkipBack :size="24" class="text-gray-600" />
        </button>

        <button
          type="button"
          class="cursor-pointer p-4 bg-pink-500 rounded-full hover:bg-pink-600 transition-colors shadow-lg active:scale-95"
          @click="togglePlay"
        >
          <Pause v-if="isPlaying" :size="26" class="text-white" />
          <Play v-else :size="26" class="text-white ml-1" />
        </button>
        <button
          type="button"
          class="cursor-pointer p-4 bg-gray-100 rounded-full hover:bg-gray-200 transition-colors disabled:opacity-50 disabled:cursor-not-allowed active:scale-95"
          :disabled="currentIndex === words.length - 1"
        >
          <SkipForward :size="24" class="text-gray-600" />
        </button>
        <button
          type="button"
          class="cursor-pointer p-4 bg-gray-100 rounded-full hover:bg-gray-200 transition-colors active:scale-95"
          title="重新播放"
          @click="repeat"
          >
            <RotateCcw :size="24" class="text-gray-600" />
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
import { ref, computed, onMounted, nextTick } from 'vue'
// import { useRouter } from 'vue-router'
import { useVocabularyStore, type Word } from '@/stores/vocabulary'
import { getCorpusItem, setErrorWord } from '@/api/corpus'
import Countdown from './components/Countdown.vue'
import { useCountdown } from '@/hooks/useCountdown'
import SpellingInput from './components/SpellingInput.vue'
import { useAudio } from '@/hooks/useAudio'
import { Play, Pause, SkipBack, SkipForward, RotateCcw, Volume2 } from 'lucide-vue-next'

interface Props {
  unitId: string
  lessonId: string
  mode: string
}

const COUNTDOWN_NUMBER = 5
const props = defineProps<Props>()
// const router = useRouter()
const vocabularyStore = useVocabularyStore()

// 倒计时
const countdown = useCountdown(COUNTDOWN_NUMBER, () => {
  nextWord()
})

const spellingInputRef = ref()

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
const totalWords = computed<number>(() => Number(vocabularyStore.testPaper?.word_count) || 0)
const currentWord = computed(() => words.value[currentIndex.value])

const speeds = [1.0, 1.2, 1.4, 1.6]

// 记录错误结果
const vocabularyErrorMap = ref(new Map<string, string>())


const toggleSpeed = () => {
  const currentSpeedIndex = speeds.indexOf(currentSpeed.value)
  const nextIndex = (currentSpeedIndex + 1) % speeds.length
  currentSpeed.value = speeds[nextIndex]
  audio.changePlaybackRate(currentSpeed.value)
}



const togglePlay = () => {
  isPlaying.value = !isPlaying.value
  if (isPlaying.value) {
    countdown.reset()
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


// 上一个
const prevWord = () => {
  isListening.value = true
  if (currentIndex.value > 1) {
    currentIndex.value--
    userInput.value = ''
    nextTick(() => {
      inputRef.value?.focus()
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
  // 先提交
  spellingInputRef.value?.handleSubmit()
  // 切换word
  if (currentIndex.value < totalWords.value - 1) {
    currentIndex.value++
    userInput.value = ''
    nextTick(() => {
      inputRef.value?.focus()
    })
    countdown.reset()
    if (currentWord.value?.url) {
      audio.play(currentWord.value?.url)
    }
    countdown.start()
  } else {
    console.log(totalWords, '00000--finished', vocabularyErrorMap)
    setErrorWord({
      lesson_id: props.lessonId,
      unit_id: props.unitId,
      errorWords: Object.fromEntries(vocabularyErrorMap.value.entries())
    })
    // Practice completed
    // router.push(`/wordlist/${props.unitId}/${props.lessonId}`)
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
const handleSubmitAnswer = (answer: {
  inputValue: string;
  id: string;
  text: string
}) => {
  // 如果校验正确，且之前错误，清除
  if (answer.inputValue == answer.text && vocabularyErrorMap.value.get(answer.id)) {
    vocabularyErrorMap.value.delete(answer.id)
  }

  // 如果错误，不管以前是否存在，直接替换
  if (answer.inputValue != answer.text) {
    vocabularyErrorMap.value.set(answer.id, answer.inputValue)
  }
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