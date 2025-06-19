<template>
  <div
    v-for="chapter in chapters"
    :key="chapter.id"
    class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden hover:shadow-md transition-shadow cursor-pointer"
  >
    <div
      @click="toggleChapter(chapter.id)"
      class="w-full p-6 text-left hover:bg-gray-50 transition-colors"
    >
      <div class="flex items-center justify-between">
        <div class="flex-1 min-w-0 ">
          <h3 class="text-xl font-bold text-gray-800 mb-2">
            {{ chapter.title }}
          </h3>
          <p class="text-sm text-gray-500 leading-relaxed">{{ chapter.intro }}</p>
        </div>
        <div class="ml-4 flex-shrink-0">
          <ChevronUp v-if="expandedChapter === chapter.id" class="text-gray-400" :size="24" />
          <ChevronDown v-else class="text-gray-400" :size="24" />
        </div>
      </div>
    </div>

    <div v-if="expandedChapter === chapter.id" class="px-6 pb-6 space-y-3">
      <div
        v-for="testPaper in chapter.list"
        :key="testPaper.id"
        @click="$emit('testPaperClick', chapter.id, testPaper.id)"
        class="w-full p-4 bg-gradient-to-r from-pink-400 to-pink-500 text-white rounded-xl hover:from-pink-500 hover:to-pink-600 transition-all duration-200 shadow-sm hover:shadow-md transform hover:scale-[1.02]"
      >
        <div class="flex items-center justify-between">
          <span class="font-medium">{{ testPaper.name }}</span>
          <div class="flex items-center space-x-3">
            <span class="text-sm opacity-90">{{ testPaper.word_count }} 词</span>
            <span class="text-sm opacity-90">{{ testPaper.more }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ChevronDown, ChevronUp } from 'lucide-vue-next'
import type { Chapter } from '../../stores/vocabulary'

interface Props {
  chapters: Chapter[]
}

defineProps<Props>()

defineEmits<{
  testPaperClick: [chapterId: string, paperId: string]
}>()

const expandedChapter = ref<string | null>()

const toggleChapter = (chapterId: string) => {
  expandedChapter.value = expandedChapter.value === chapterId ? null : chapterId
}
</script>