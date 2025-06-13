<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-100 via-indigo-100 to-indigo-200 p-5">
    <!-- Chapters Section -->
    <section class="mx-auto flex flex-col gap-4">
      <div
        v-for="chapter in chapters"
        :key="chapter.id"
        @click="toggleChapter(chapter.id)"
        class="bg-white/90 backdrop-blur rounded-2xl p-6 shadow-sm cursor-pointer transition-transform hover:-translate-y-1 hover:shadow-lg"
      >
        <!-- Chapter Header -->
        <div class="flex items-center justify-between mb-2">
          <h3 class="text-xl font-bold text-gray-800">{{ chapter.title }}</h3>
          <span
            :class="[
              'text-gray-600 transition-transform',
              expandedChapters.includes(chapter.id) ? 'rotate-180' : ''
            ]"
          >▼</span>
        </div>
        <p class="text-gray-600 text-base">{{ chapter.subtitle }}</p>

        <!-- Test Papers -->
        <div v-if="expandedChapters.includes(chapter.id)" class="mt-5 flex flex-col gap-3">
          <div
            v-for="paper in chapter.testPapers"
            :key="paper.id"
            @click.stop="goToWordList(chapter.id, paper.id)"
            class="bg-gradient-to-r from-fuchsia-300 to-pink-500 rounded-xl px-5 py-4 flex items-center justify-between cursor-pointer transition-transform hover:translate-x-1 hover:shadow-lg"
          >
            <span class="text-lg font-medium text-white">{{ paper.name }}</span>
            <span class="text-white/90 text-base">{{ paper.more }}</span>
          </div>
        </div>
      </div>
    </section>
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

const { chapters, setChapters } = vocabularyStore
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
    setChapters(res.data?.filter((item: any) => item.style === '2').map((item: any) => ({
      ...item,
      subtitle: item.intro,
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
