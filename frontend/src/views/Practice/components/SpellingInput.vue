<template>
   <div class="py-8">
    <div class="relative">

     <div class="input-container">
       <input
         v-model="inputValue"
         @keyup.enter="handleSubmit"
         placeholder="请输入单词拼写..."
         :class="[
           'word-input w-full px-6 py-4 text-lg text-center border-2 rounded-2xl',
           'transition-all duration-300 focus:outline-none',
           isCorrect
               ? 'border-green-500 bg-green-50 text-green-700'
               : 'border-red-500 bg-red-50 text-red-700'
         ]"
       />

       <div class="cursor-line" v-if="!inputValue"></div>
      </div>

    </div>
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

<style scoped>

.input-container {
  position: relative;
  border-radius: 0;
  padding: 0;
  backdrop-filter: blur(10px);
  display: flex;
  align-items: center;
  max-width: 500px;
  border-bottom: 1px solid;
  margin: auto;
}

.word-input {
  width: 100%;
  border: none;
  outline: none;
  font-size: 24px;
  background: transparent;
  text-align: center;
  color: #333;
}

.word-input::placeholder {
  color: #999;
  font-style: italic;
}

.cursor-line {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  width: 2px;
  height: 30px;
  background: #333;
  animation: blink 1s infinite;
}
</style>