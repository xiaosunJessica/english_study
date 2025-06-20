<template>
  <div class="flex flex-col flex-1 justify-center mx-auto min-w-[30rem] max-w-[40rem]">
    <label class="block text-lg font-medium text-gray-700 mb-4 text-center"> 请输入您听到的单词 </label>
    <div class="relative">
      <input
        ref="inputRef"
        v-model="inputValue"
        @keyup.enter="handleSubmit"
        placeholder="请输入单词拼写..."
        :class="[
          'w-full text-center text-3xl py-6 border-b-2 border-gray-300 bg-transparent transition-colors placeholder:text-gray-400',
          'transition-opacity duration-300',
          isStart
            ? 'opacity-100 focus:border-pink-500 focus:outline-none'
            : 'opacity-0 pointer-events-none'
        ]"
      />
      <div class="cursor-line" v-if="!inputValue"></div>
      <button
        v-show="!isStart"
        class="absolute inset-0 bg-pink-500 text-white px-6 py-4 rounded-xl font-medium shadow-md hover:bg-pink-600 transition-colors transform hover:scale-105 cursor-pointer"
        @click="$emit('togglePlay')">开始拼写</button>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { computed, watch, ref, onMounted,nextTick } from 'vue'
interface Props {
  modelValue: string
  currentWord: Object
  isStart: boolean
}

const props = defineProps<Props>()
const inputRef = ref<HTMLElement>()
const emit = defineEmits<{
  'update:modelValue': [value: string]
  submit: [value: object],
  togglePlay: [],
}>()


const inputValue = computed({
  get: () => props.modelValue,
  set: (val: string) => emit('update:modelValue', val)
})

watch(() => props.currentWord, () => {
    inputValue.value = ''
}, {flush: 'pre'})

const handleSubmit = () => {
  emit('submit', {
    ...props.currentWord,
    inputValue: inputValue.value
  })
}

const focus = () => {
  inputRef.value?.focus()
}

defineExpose({
  handleSubmit,
  focus
})

onMounted(() => {
    // input focus
  nextTick(() => {
    inputRef.value?.focus()
  })
})

</script>
