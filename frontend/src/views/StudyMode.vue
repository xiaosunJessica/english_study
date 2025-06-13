<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-100 via-blue-200 to-blue-300 p-5 max-w-3xl mx-auto">
    <header
      class="bg-white bg-opacity-90 rounded-2xl p-4 mb-6 backdrop-blur-md"
    >
      <div class="flex justify-between items-center">
        <span class="text-lg font-bold text-gray-800">听写 (1/112)</span>
        <div class="flex gap-2">
          <button
            class="bg-white bg-opacity-80 border border-gray-300 rounded-full px-4 py-2 text-sm cursor-pointer transition duration-200 hover:bg-white"
          >
            对答案
          </button>
          <button
            class="bg-white bg-opacity-80 border border-gray-300 rounded-full px-4 py-2 text-sm cursor-pointer transition duration-200 hover:bg-white"
          >
            巩固错词
          </button>
        </div>
      </div>
    </header>

    <section
      class="bg-gradient-to-br from-pink-600 to-pink-400 rounded-2xl p-6 mb-6"
    >
      <div class="mb-5">
        <h2 class="text-white text-xl font-semibold m-0">学习模式</h2>
      </div>
      <div class="grid grid-cols-4 gap-3">
        <button
          v-for="mode in studyModes"
          :key="mode.id"
          @click="selectedMode = mode.id"
          :class="[
            'rounded-xl px-4 py-4 text-sm font-medium text-center cursor-pointer transition duration-200',
            selectedMode === mode.id
              ? 'bg-gradient-to-br from-pink-300 to-pink-100 text-white font-bold'
              : 'bg-white bg-opacity-90 hover:bg-white hover:-translate-y-0.5',
          ]"
        >
          {{ mode.name }}
        </button>
      </div>
    </section>

    <section
      class="bg-white bg-opacity-90 rounded-2xl p-6 mb-6 backdrop-blur-md"
    >
      <div class="mb-6">
        <label class="block text-gray-800 font-semibold mb-3 text-lg">播放倍速</label>
        <div class="flex flex-wrap gap-2">
          <button
            v-for="speed in playbackSpeeds"
            :key="speed"
            @click="selectedSpeed = speed"
            :class="[
              'rounded-full px-4 py-2 text-sm cursor-pointer transition duration-200 border-2',
              selectedSpeed === speed
                ? 'bg-white border-pink-400 text-pink-400 font-bold'
                : 'bg-gray-100 border-transparent',
            ]"
          >
            x{{ speed }}
          </button>
          <button
            class="rounded-full px-4 py-2 text-sm bg-gray-100 cursor-pointer transition duration-200 border-2 border-transparent hover:border-pink-400 hover:text-pink-400"
          >
            自适应
          </button>
        </div>
      </div>

      <div>
        <label class="block text-gray-800 font-semibold mb-3 text-lg">对错反馈</label>
        <div class="flex gap-2 flex-wrap">
          <button
            @click="showFeedback = false"
            :class="[
              'rounded-full px-4 py-2 text-sm cursor-pointer transition duration-200 border-2',
              !showFeedback
                ? 'bg-white border-pink-400 text-pink-400 font-bold'
                : 'bg-gray-100 border-transparent',
            ]"
          >
            拼写中不反馈
          </button>
          <button
            @click="showFeedback = true"
            :class="[
              'rounded-full px-4 py-2 text-sm cursor-pointer transition duration-200 border-2',
              showFeedback
                ? 'bg-white border-pink-400 text-pink-400 font-bold'
                : 'bg-gray-100 border-transparent',
            ]"
          >
            拼写中反馈
          </button>
        </div>
      </div>
    </section>

    <section
      class="bg-white bg-opacity-90 rounded-2xl p-6 mb-6 backdrop-blur-md"
    >
      <h3 class="text-gray-800 font-bold text-lg mb-3">什么是拼写模式？</h3>
      <p class="text-pink-600 text-base mb-4">
        拼写模式专门为机考考生设计，是可以练习打字的语料库版本
      </p>

      <div class="flex flex-wrap gap-2 mb-5">
        <span
          class="bg-pink-100 text-pink-600 rounded-full px-3 py-1 text-xs font-semibold"
        >
          自动识别错词
        </span>
        <span
          class="bg-pink-100 text-pink-600 rounded-full px-3 py-1 text-xs font-semibold"
        >
          自动计算正确率
        </span>
        <span
          class="bg-pink-100 text-pink-600 rounded-full px-3 py-1 text-xs font-semibold"
        >
          自动标记错词
        </span>
      </div>

      <div class="mb-4">
        <p class="text-pink-600 font-semibold mb-1">Tips: 建议用电脑版访问小程序练习</p>
        <p class="text-gray-600 text-sm">更贴近雅思机考场景</p>
      </div>

      <p class="text-gray-600 text-xs leading-relaxed">
        * 自适应倍速需要在提交单词后手动播放下一个单词<br />
        电脑端使用时按
        <span class="text-pink-600 font-bold">空格键</span>可快速提交
      </p>
    </section>

    <button
      @click="startPractice"
      class="w-full bg-gradient-to-br from-pink-600 to-pink-400 rounded-3xl py-4 text-white text-xl font-bold cursor-pointer transition duration-200 hover:-translate-y-0.5 hover:shadow-lg"
    >
      确定
    </button>
  </div>
</template>


<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

interface Props {
  unitId: string
  lessonId: string
}

const props = defineProps<Props>()
const router = useRouter()

const selectedMode = ref('spelling')
const selectedSpeed = ref(1.4)
const showFeedback = ref(false)

const studyModes = [
  { id: 'test', name: '测一测' },
  { id: 'recite', name: '背词模式' },
  { id: 'dictation', name: '听写对答案' },
  { id: 'spelling', name: '在线拼写' }
]

const playbackSpeeds = [1.0, 1.2, 1.4, 1.6]

const startPractice = () => {
  router.push(`/practice/${props.unitId}/${props.lessonId}/${selectedMode.value}`)
}
</script>
