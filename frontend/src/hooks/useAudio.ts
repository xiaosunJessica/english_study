import { ref } from "vue";

export const useAudio = () => {
  const isPlaying = ref(false)
  const isLoading = ref(false)
  const playbackRate = ref(1.0)
  const audioRef = ref<HTMLAudioElement|null>(null)
  const currentUrl = ref<string>('')

  // const { getPreloadedAudio } = useAudioPreloader()

  const play = async (url?: string) => {
    try {
      if (url && url !== currentUrl.value) {
        if (audioRef.value) {
          audioRef.value.pause()
          audioRef.value = null
        }

        currentUrl.value = url
      }

      if (!audioRef.value && currentUrl.value) {
        isLoading.value = true

        const audio = new Audio(currentUrl.value)
        audioRef.value = audio
        audio.playbackRate = playbackRate.value

        audio.onloadstart = () => isLoading.value = true
        audio.oncanplay = () => isLoading.value = false
        audio.onplay = () => isPlaying.value = true
        audio.onpause = () => isPlaying.value = false
        audio.onended = () => isPlaying.value = false

        audio.onerror = () => {
          isLoading.value = false
          isPlaying.value = false
        }
      }

      if (audioRef.value && !isPlaying.value) {
        await audioRef.value.play()
      }
    } catch (error) {
      isLoading.value = false
      isPlaying.value = false

      if (error instanceof DOMException &&
          error.name === 'AbortError' &&
          error.message.includes('interrupted by a call to pause')) {
        console.warn('Audio play request was interrupted:', error.message)
      } else {
        console.error('Error playing audio:', error)
      }
    }
  }

  const pause = () => {
    if (audioRef.value && isPlaying.value) {
      audioRef.value.pause()
      isPlaying.value = false
    }
  }

  const replay = () => {
    if (audioRef.value) {
      audioRef.value.currentTime = 0
      return play()
    } else if (currentUrl.value) {
      return play(currentUrl.value)
    }
    return Promise.resolve()
  }

  const changePlaybackRate = (rate: number) => {
    playbackRate.value = rate
    if (audioRef.value) {
      audioRef.value.playbackRate = rate
    }
  }

    const cleanup = () => {
    if (audioRef.value) {
      audioRef.value.pause()
      audioRef.value = null
    }
    currentUrl.value = ''
    isPlaying.value = false
    isLoading.value = false
  }

  return {
    isLoading,
    isPlaying,
    playbackRate,
    play,
    pause,
    replay,
    changePlaybackRate,
    cleanup
  }
}