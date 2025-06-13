<template>
  <div class="mx-auto min-w-[30rem] max-w-[40rem]mx-auto">
    <label class="block text-lg font-medium text-gray-700 mb-4 text-center"> 请输入您听到的单词 </label>
    <input
     v-model="inputValue"
     @keyup.enter="handleSubmit"
     placeholder="请输入单词拼写..."
     class="w-full text-center text-3xl py-6 border-b-2 border-gray-300 bg-transparent focus:border-pink-500 focus:outline-none transition-colors placeholder:text-gray-400"
    />

     <div class="cursor-line" v-if="!inputValue"></div>
  </div>
</template>

<script lang="ts" setup>
import { computed, watch } from 'vue'
interface Props {
  modelValue: string
  currentWord: string
  isCorrect?: boolean
  showResult?: boolean
}

const props = defineProps<Props>()

const emit = defineEmits<{
  'update:modelValue': [value: string]
  submit: [value: string]
}>()

const inputValue = computed({
  get: () => props.modelValue,
  set: (val: string) => emit('update:modelValue', val)
})

watch(() => props.currentWord, () => {
  inputValue.value = ''
})

const handleSubmit = () => {
   emit('submit', inputValue.value)
}
</script>
