<template>
  <div class="h-screen bg-gradient-to-br from-gray-100 to-blue-200 p-5 flex flex-col mx-auto">
    <div class="flex gap-2 mb-6">
      <button
        class="px-6 py-3 rounded-full text-base backdrop-blur-sm transition-all"
        :class="activeTab === 'all' ? 'bg-gradient-to-r from-pink-400 to-red-400 text-white font-bold' : 'bg-white/70 hover:bg-white/90'"
        @click="activeTab = 'all'"
      >
        全部({{ allWords.length }})
      </button>
      <button
        class="px-6 py-3 rounded-full text-base backdrop-blur-sm transition-all"
        :class="activeTab === 'wrong' ? 'bg-gradient-to-r from-pink-400 to-red-400 text-white font-bold' : 'bg-white/70 hover:bg-white/90'"
        @click="activeTab = 'wrong'"
      >
        近期错词({{ wrongWords.length }})
      </button>
    </div>

    <div class="flex-1 bg-white/90 rounded-xl p-6 mb-6 backdrop-blur-sm overflow-y-auto">
      <div
        v-for="(word, index) in displayWords.value"
        :key="word.id"
        class="flex items-center gap-4 py-4 border-b border-black/5 last:border-b-0"
      >
        <div class="text-lg font-bold text-gray-600 min-w-[30px]">{{ index + 1 }}.</div>
        <div class="flex-1">
          <div class="text-xl font-bold text-gray-800 mb-1">{{ word.text }}</div>
          <div class="text-base text-gray-600">{{ word.note }}</div>
        </div>
        <div v-if="word.is_wrong" class="bg-red-400 text-white rounded-full px-3 py-1 text-xs font-bold">
          错过{{ word.wrong_num }}次
        </div>
      </div>
    </div>

    <div class="flex justify-center gap-4">
      <button
        class="min-w-[160px] px-8 py-4 rounded-full font-bold text-lg bg-white/90 text-gray-800 backdrop-blur-sm hover:translate-y-[-2px] hover:shadow-lg transition"
        @click="startFromWord"
      >
        从某词开始
      </button>
      <button
        class="min-w-[160px] px-8 py-4 rounded-full font-bold text-lg text-white bg-gradient-to-r from-pink-300 to-pink-100 hover:translate-y-[-2px] hover:shadow-lg transition"
        @click="startStudy"
      >
        开始学习
      </button>
    </div>
  </div>
</template>
<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useVocabularyStore } from '../stores/vocabulary'
import { getCorpusItem } from '../api/corpus'

interface Props {
  unitId: string
  lessonId: string
}

const props = defineProps<Props>()
const router = useRouter()
const vocabularyStore = useVocabularyStore()
const { setTestPaper } = vocabularyStore

const activeTab = ref<'all' | 'wrong'>('all')

const unitId = parseInt(props.unitId)
const lessonId = parseInt(props.lessonId)



const allWords = computed(() => vocabularyStore.testPaper?.list || [])
const wrongWords = computed(() => allWords.value.filter(word => word.is_wrong))

const displayWords = computed(() => {
  return activeTab.value === 'all' ? allWords : wrongWords
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
  router.push(`/study/${unitId}/${lessonId}`)
}

onMounted(async () => {

  const res = await getCorpusItem({
    book_id: 0,
    unit_id: unitId,
    lesson_id: lessonId
  })

  setTestPaper(res.data)
})
</script>
