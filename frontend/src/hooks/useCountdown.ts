import { ref } from 'vue'

export const useCountdown = (seconds: number, onComplete?: () => void) => {
  const timeLeft = ref(seconds)
  const isActive = ref(false)
  const timer = ref<number | null>(null)

  const startCountdown = () => {
    if (isActive.value) return
    isActive.value = true
    timer.value = setInterval(() => {
      if (timeLeft.value <= 0) {
        stopCountdown()
        onComplete?.()
      } else {
        timeLeft.value--
      }
    }, 1000)
  }

  const stopCountdown = () => {
    isActive.value = false
    if (timer.value) {
      clearInterval(timer.value)
      isActive.value = false
      timer.value = null
    }
  }


  const resetCountdown = () => {
    timeLeft.value = seconds
    stopCountdown()
  }

  return {
    timeLeft,
    isActive,
    startCountdown,
    stopCountdown,
    resetCountdown
  }
}