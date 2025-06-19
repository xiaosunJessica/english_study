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
  error_num: number;
  lesson_id: number;
  is_wrong: number;
  wrong_num: number;
}

export interface Chapter {
  id: string
  title: string
  subtitle: string
  intro: string
  list: TestPaper[]
}

export interface TestPaper {
  id: string,
  name: string;
  url: string;
  word_count: number;
  error_count: number;
  extra: string;
  more: string;
  list: Word[];
}

export const useVocabularyStore = defineStore('vocabulary', () => {
  const chapters = ref<Chapter[]>([])

  const testPaper = ref<TestPaper>()

  const getChapter = (id: string) => {
    return chapters.value.find(chapter => chapter.id === id)
  }

  const setTestPaper = (newTestPaper: TestPaper) => {
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