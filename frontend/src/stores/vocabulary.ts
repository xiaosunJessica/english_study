import { defineStore } from 'pinia'
import { ref } from 'vue'

export interface Word {
  id: number;
  text: string;
  note: string;
  voice: string;
  url: string;
  local_url: string;
  word_id: string;
  error_num: string;
  lesson_id: number;
  is_wrong: boolean;
  wrong_num: number;
}

export interface Chapter {
  id: number
  title: string
  subtitle: string
  testPapers: TestPaper[]
}

export interface TestPaper {
  name: string;
  url: string;
  word_count: string;
  error_count: string;
  extra: string;
  list: Word[];
}

export const useVocabularyStore = defineStore('vocabulary', () => {
  const chapters = ref<Chapter[]>([])

  const testPaper = ref<TestPaper>()

  const getChapter = (id: number) => {
    return chapters.value.find(chapter => chapter.id === id)
  }

  const setTestPaper = (newTestPaper: TestPaper) => {
    console.log(newTestPaper, '00000testPaper')
    testPaper.value = newTestPaper
  }

  const setChapters = (newChapters: Chapter[]) => {
    chapters.value.splice(0, chapters.value.length, ...newChapters)
  }

  return {
    chapters,
    getChapter,
    setChapters,
    setTestPaper,
    testPaper,
  }
})