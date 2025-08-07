import { ref, computed } from 'vue'

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

  const totalDatasets = computed(() => datasets.value.length)
  const totalUtterances = computed(() => 
    datasets.value.reduce((sum, dataset) => sum + dataset.utterances, 0)
  )
  const totalSpeakers = computed(() => 
    datasets.value.reduce((sum, dataset) => sum + dataset.speakers, 0)
  )

  return {
    datasets,
    loading,
    error,
    fetchDatasets,
    totalDatasets,
    totalUtterances,
    totalSpeakers
  }
}