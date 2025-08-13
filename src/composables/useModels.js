import { ref } from 'vue'

export function useModels() {
  const models = ref([])
  const loading = ref(false)
  const error = ref(null)

  const fetchModels = async () => {
    loading.value = true
    error.value = null
    
    try {
      const response = await fetch('http://localhost:8000/models')
      if (!response.ok) {
        throw new Error('Failed to fetch models')
      }
      const data = await response.json()
      models.value = data.models || data || []
    } catch (err) {
      error.value = 'Failed to fetch models'
      console.error('Error fetching models:', err)
    } finally {
      loading.value = false
    }
  }

  return {
    models,
    loading,
    error,
    fetchModels,
  }
}