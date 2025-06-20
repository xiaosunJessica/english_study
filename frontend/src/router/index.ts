import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/Home.vue'
import Chapter from '../views/Corpus/Chapter/Chaper.vue'
import WordList from '../views/Corpus/WordList.vue'
// import StudyMode from '../views/Corpus/StudyMode.vue'
import Practice from '../views/Corpus/Practice/Practice.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: Home
  },
  {
    path: '/corpus/chapter',
    name: 'Chapter',
    component: Chapter
  },
  {
    path: '/corpus/wordlist/:unitId/:lessonId',
    name: 'WordList',
    component: WordList,
    props: true
  },
  // {
  //   path: '/corpus/study/:unitId/:lessonId',
  //   name: 'StudyMode',
  //   component: StudyMode,
  //   props: true
  // },
  {
    path: '/corpus/practice/:unitId/:lessonId/:tabId',
    name: 'Practice',
    component: Practice,
    props: true
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router