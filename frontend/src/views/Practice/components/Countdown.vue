<template>
  <div :class="[
    'text-2xl font-bold transition-colors duration-300',
    isActive && seconds <= 3 ? 'text-red-500' : 'text-gray-400'
  ]">
    {{ seconds }}s
  </div>
</template>

<script setup lang="ts">
interface Props {
  seconds: number
  isActive: boolean
}

defineProps<Props>()

</script>