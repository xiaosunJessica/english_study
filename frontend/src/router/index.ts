import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import WordList from '../views/WordList.vue'
import StudyMode from '../views/StudyMode.vue'
import Practice from '../views/Practice.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/wordlist/:chapter/:paper',
    name: 'WordList',
    component: WordList,
    props: true
  },
  {
    path: '/study/:chapter/:paper',
    name: 'StudyMode',
    component: StudyMode,
    props: true
  },
  {
    path: '/practice/:chapter/:paper/:mode',
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