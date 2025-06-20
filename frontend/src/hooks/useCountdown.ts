import { ref } from 'vue'
export interface Countdown {
  timeLeft: number
  isActive: boolean
  start: Function
  stop: Function
  reset: Function
}
export const useCountdown = (seconds: number, onComplete?: () => void) => {
  const timeLeft = ref(seconds)
  const isActive = ref(false)
  const timer = ref<number | null>(null)

  const start = () => {
    if (isActive.value) return
    isActive.value = true
    timer.value = setInterval(() => {
      if (timeLeft.value <= 1) {
        stop()
        onComplete?.()
      } else {
        timeLeft.value--
      }
    }, 1000)
  }

  const stop = () => {
    isActive.value = false
    if (timer.value) {
      clearInterval(timer.value)
      isActive.value = false
      timer.value = null
    }
  }


  const reset = () => {
    timeLeft.value = seconds
    stop()
  }

  return {
    timeLeft,
    isActive,
    start,
    stop,
    reset
  }
}