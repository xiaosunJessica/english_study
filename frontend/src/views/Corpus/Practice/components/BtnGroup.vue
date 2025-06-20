

<template>
  <div class="bg-white border-t border-gray-200 space-y-4">
    <div class="flex justify-center items-center gap-6 px-6 py-4" >
    <div class="relative">
      <button
        @click="showSpeedMenu = !showSpeedMenu"
        :class="[
          'px-4 py-2 rounded-lg font-medium transition-all duration-200 cursor-pointer',
          showSpeedMenu
            ? 'bg-pink-500 text-white shadow-lg'
            : 'bg-pink-100 text-pink-600 hover:bg-pink-200'
        ]"
      >
        {{ currentSpeed }}x倍速
      </button>

      <!-- Speed Menu -->
      <Transition
        enter-active-class="transition ease-out duration-200"
        enter-from-class="opacity-0 scale-95"
        enter-to-class="opacity-100 scale-100"
        leave-active-class="transition ease-in duration-150"
        leave-from-class="opacity-100 scale-100"
        leave-to-class="opacity-0 scale-95"
      >
        <div
          v-if="showSpeedMenu"
          class="absolute bottom-full mb-2 left-1/2 transform -translate-x-1/2 bg-white rounded-xl shadow-2xl border border-gray-100 p-2 min-w-[200px] z-10"
        >
          <div class="text-xs text-gray-500 px-3 py-2 border-b border-gray-100 mb-1">
            选择播放速度
          </div>
          <div class="grid grid-cols-3 gap-1">
            <button
              v-for="speed in speedOptions"
              :key="speed"
              @click="handleSpeedChange(speed)"
              :class="[
                'px-3 py-2 rounded-lg text-sm font-medium transition-all duration-200 cursor-pointer',
                currentSpeed === speed
                  ? 'bg-pink-500 text-white shadow-md transform scale-105'
                  : 'hover:bg-gray-100 text-gray-700'
              ]"
            >
              {{ speed }}x
            </button>
          </div>
        </div>
      </Transition>
    </div>
    <button
      type="button"
      class="cursor-pointer p-4 bg-gray-100 rounded-full hover:bg-gray-200 transition-colors disabled:opacity-50 disabled:cursor-not-allowed active:scale-95"
      :disabled="currentIndex === 0"
      @click="handlePrev"
    >
      <SkipBack :size="24" class="text-gray-600" />
    </button>

    <button
      type="button"
      class="cursor-pointer p-4 bg-pink-500 rounded-full hover:bg-pink-600 transition-colors shadow-lg active:scale-95"
      @click="handleTogglePlay"
    >
      <Pause v-if="isPlaying" :size="26" class="text-white" />
      <Play v-else :size="26" class="text-white ml-1" />
    </button>
    <button
      type="button"
      class="cursor-pointer p-4 bg-gray-100 rounded-full hover:bg-gray-200 transition-colors disabled:opacity-50 disabled:cursor-not-allowed active:scale-95"
      :disabled="currentIndex === words.length - 1"
      @click="handleNext"
    >
      <SkipForward :size="24" class="text-gray-600" />
    </button>
    <button
      type="button"
      class="cursor-pointer p-4 bg-gray-100 rounded-full hover:bg-gray-200 transition-colors active:scale-95"
      title="重新播放"
      @click="handleRepeat"
      >
      <RotateCcw :size="24" class="text-gray-600" />
    </button>
    </div>
  </div>
</template>
<script setup lang='ts'>
import { ref } from 'vue'
import { Play, Pause, SkipBack, SkipForward, RotateCcw } from 'lucide-vue-next'
import { type Word } from '@/stores/vocabulary'

interface Props {
  currentIndex: number
  words: Word[]
  isPlaying: boolean
  currentSpeed: number
}
defineProps<Props>()

const emit = defineEmits(['prev', 'next', 'togglePlay', 'repeat', 'speedChange'])

const handlePrev = () => emit('prev')
const handleNext = () => emit('next')
const handleTogglePlay = () => emit('togglePlay')
const handleSpeedChange = (speed: number) => {
  showSpeedMenu.value = false
  emit('speedChange', speed)
}

const handleRepeat = () => emit('repeat')

const showSpeedMenu = ref(false)
const speedOptions = [1.0, 1.2, 1.4, 1.6]


</script>

<style lang='scss' scoped>

</style>