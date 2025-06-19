<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-100 via-indigo-100 to-indigo-200 p-5">
    <h1 class="text-3xl font-bold text-gray-900 mb-2">雅思王语料库</h1>
    <p class="text-gray-600 mb-8">选择章节开始学习</p>
    <!-- Chapters Section -->
    <section class="mx-auto flex flex-col gap-4">
      <chapter-item :chapters="chapters" @test-paper-click="goToWordList" />
    </section>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useVocabularyStore } from '@/stores/vocabulary'
import { getCorpusList } from '@/api/corpus'
import ChapterItem from './ChapterItem.vue'

const regex = /^(Chapter\s*\d+)\s*(.*)$/;

const router = useRouter()
const vocabularyStore = useVocabularyStore()

const { chapters, setChapters } = vocabularyStore

const goToWordList = (chapterId: string, paperId: string) => {
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
