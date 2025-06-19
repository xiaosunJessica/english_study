import { createRouter, createWebHistory } from 'vue-router'
import Chapter from '../views/Chapter/Chaper.vue'
import WordList from '../views/WordList.vue'
import StudyMode from '../views/StudyMode.vue'
import Practice from '../views/Practice/Practice.vue'

const routes = [
  {
    path: '/',
    name: 'Chapter',
    component: Chapter
  },
  {
    path: '/wordlist/:unitId/:lessonId',
    name: 'WordList',
    component: WordList,
    props: true
  },
  {
    path: '/study/:unitId/:lessonId',
    name: 'StudyMode',
    component: StudyMode,
    props: true
  },
  {
    path: '/practice/:unitId/:lessonId/:mode',
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