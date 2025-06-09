import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export interface Word {
  id: number
  english: string
  chinese: string
  isWrong?: boolean
  wrongCount?: number
}

export interface Chapter {
  id: number
  title: string
  subtitle: string
  testPapers: TestPaper[]
}

export interface TestPaper {
  id: number
  name: string
  accuracy: number
  words: Word[]
}

export const useVocabularyStore = defineStore('vocabulary', () => {
  const chapters = ref<Chapter[]>([
    /*
    {
      id: 3,
      title: 'Chapter 3',
      subtitle: '雅思听力特别名词语料库',
      testPapers: [
        {
          id: 1,
          name: 'Test Paper 1',
          accuracy: 11.40,
          words: [
            { id: 1, english: 'ability', chinese: '能力' },
            { id: 2, english: 'abstract', chinese: '摘要' },
            { id: 3, english: 'accountant', chinese: '会计' },
            { id: 4, english: 'accuracy', chinese: '准确度' },
            { id: 5, english: 'acid', chinese: '酸', isWrong: true, wrongCount: 1 },
            { id: 6, english: 'action', chinese: '行动' },
            { id: 7, english: 'activity', chinese: '活动' },
            { id: 8, english: 'actor', chinese: '男演员' },
            { id: 9, english: 'address', chinese: '地址' },
            { id: 10, english: 'administration', chinese: '管理' }
          ]
        },
        {
          id: 2,
          name: 'Test Paper 2',
          accuracy: 10.81,
          words: []
        }
      ]
    },
    {
      id: 4,
      title: 'Chapter 4',
      subtitle: '雅思听力形容词、副词语料库',
      testPapers: [
        {
          id: 1,
          name: 'Test Paper 1',
          accuracy: 14.91,
          words: []
        },
        {
          id: 2,
          name: 'Test Paper 2',
          accuracy: 11.43,
          words: []
        }
      ]
    },
    {
      id: 5,
      title: 'Chapter 5',
      subtitle: '雅思听力容音连读、混合训练语料库',
      testPapers: []
    }
    */
  ])

  const wrongWords = ref(2224)

  const getChapter = (id: number) => {
    return chapters.value.find(chapter => chapter.id === id)
  }

  const getTestPaper = (chapterId: number, paperId: number) => {
    const chapter = getChapter(chapterId)
    return chapter?.testPapers.find(paper => paper.id === paperId)
  }

  const getWrongWords = computed(() => {
    return chapters.value.flatMap(chapter =>
      chapter.testPapers.flatMap(paper =>
        paper.words.filter(word => word.isWrong)
      )
    )
  })

  const setChapters = (newChapters: Chapter[]) => {
    console.log(newChapters, '00000')
    chapters.value.splice(0, chapters.value.length, ...newChapters)
  }

  return {
    chapters,
    wrongWords,
    getChapter,
    setChapters,
    getTestPaper,
    getWrongWords
  }
})