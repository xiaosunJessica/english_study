
<template>
  <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
    <h3 class="text-lg font-semibold text-gray-800 mb-4">进度统计</h3>
    <div class="space-y-3">
      <div class="flex justify-between">
        <span class="text-gray-600">当前进度</span>
      </div>
      <div class="w-full bg-gray-200 rounded-full h-2">
        <div
          class="bg-pink-500 h-2 rounded-full transition-all duration-300"
          :style="{ width: `${percentage}%` }"
        ></div>
      </div>
      <div class="flex justify-between text-sm text-gray-500">
        <span>完成度: {{ percentage }}%</span>
        <span>剩余: {{ remaining }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang='ts'>
import { computed } from 'vue';
import { type Word } from '@/stores/vocabulary'
const props = defineProps<{
  currentIndex: number
  words: Word[]
  isStart: boolean
}>()

// 2️⃣ 计算属性
const total = computed(() => props.words.length)
const currentStep = computed(() => {
  if (props.isStart) {
    return props.currentIndex + 1
  }
  return 0
})
const progress = computed(() =>
  total.value === 0 ? 0 : Math.min(currentStep.value / total.value, 1)
)

const percentage = computed(() => Math.round(progress.value * 100))

const remaining = computed(() =>
  total.value === 0 ? 0 : Math.max(total.value - currentStep.value, 0)
)
</script>
