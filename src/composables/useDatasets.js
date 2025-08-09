import { ref } from 'vue'

export function useDatasets() {
  const datasets = ref([])
  const loading = ref(false)
  const error = ref(null)

  const fetchDatasets = async () => {
    loading.value = true
    error.value = null
    
    try {
      const response = await fetch('http://localhost:8000/datasets')
      if (!response.ok) {
        throw new Error('Failed to fetch datasets')
      }
      const data = await response.json()
      datasets.value = data.datasets
    } catch (err) {
      error.value = 'Failed to fetch datasets'
      console.error('Error fetching datasets:', err)
    } finally {
      loading.value = false
    }
  }
  return {
    datasets,
    loading,
    error,
    fetchDatasets,
  }
}