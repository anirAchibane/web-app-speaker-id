<template>
    <navigation-bar></navigation-bar>
    <div class="dataset-details-container">

        <!-- Error State -->
        <div v-if="error" class="error">
            <p>{{ error }}</p>
            <button @click="fetchDatasetDetails" class="retry-btn">Retry</button>
        </div>

        <!-- Dataset Details -->
        <div v-if="!loading && !error && dataset" class="dataset-details">
            <!-- Header Section -->
            <div class="dataset-header">
                <div class="header-content">
                    <div class="title-section">
                        <div class="dataset-icon">
                            <svg width="32" height="32" fill="currentColor" viewBox="0 0 16 16">
                                <path d="M4 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H4zm0 1h8a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1z"/>
                                <path d="M6 4.5a.5.5 0 0 1 .5-.5h3a.5.5 0 0 1 0 1h-3a.5.5 0 0 1-.5-.5zm0 2a.5.5 0 0 1 .5-.5h3a.5.5 0 0 1 0 1h-3a.5.5 0 0 1-.5-.5zm0 2a.5.5 0 0 1 .5-.5h3a.5.5 0 0 1 0 1h-3a.5.5 0 0 1-.5-.5z"/>
                            </svg>
                        </div>
                        <div class="title-content">
                            <h1>{{ dataset.name }}</h1>
                        </div>
                    </div>
                    <p class="description">{{ dataset.description || 'Professional audio dataset for speaker identification and machine learning applications' }}</p>
                </div>
                <div class="header-actions">
                    <button class="btn-primary action-btn">
                        <svg width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                            <path d="M.5 9.9a.5.5 0 0 1 .5.5v2.5a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-2.5a.5.5 0 0 1 1 0v2.5a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2v-2.5a.5.5 0 0 1 .5-.5z"/>
                            <path d="M7.646 11.854a.5.5 0 0 0 .708 0l3-3a.5.5 0 0 0-.708-.708L8.5 10.293V1.5a.5.5 0 0 0-1 0v8.793L5.354 8.146a.5.5 0 1 0-.708.708l3 3z"/>
                        </svg>
                        Download Dataset
                    </button>
                    <button class="btn-secondary action-btn">
                        <svg width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                            <path d="M14 4.5V14a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V2a2 2 0 0 1 2-2h5.5L14 4.5zm-3 0A1.5 1.5 0 0 1 9.5 3V1H4a1 1 0 0 0-1 1v12a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1V4.5h-2z"/>
                        </svg>
                        Export Metadata
                    </button>
                </div>
            </div>

            <!-- Main Content Layout -->
            <div class="main-content-layout">
                <!-- Main Section - File Structure -->
                <div class="main-section">
                    <div class="section-card main-card">
                        <div class="section-header">
                            <div class="section-title">
                                <svg width="20" height="20" fill="currentColor" viewBox="0 0 16 16">
                                    <path d="M9.828 3h3.982a2 2 0 0 1 1.992 2.181l-.637 7A2 2 0 0 1 13.174 14H2.825a2 2 0 0 1-1.991-1.819l-.637-7a1.99 1.99 0 0 1 .342-1.31L2.61 1a2 2 0 0 1 1.511-.621h4.707A2 2 0 0 1 9.828 3z"/>
                                </svg>
                                <h2>File Structure</h2>
                            </div>
                            <div class="file-stats">
                                <span class="stat-item">
                                    <svg width="14" height="14" fill="currentColor" viewBox="0 0 16 16">
                                        <path d="M9.828 3h3.982a2 2 0 0 1 1.992 2.181l-.637 7A2 2 0 0 1 13.174 14H2.825a2 2 0 0 1-1.991-1.819l-.637-7a1.99 1.99 0 0 1 .342-1.31L2.61 1a2 2 0 0 1 1.511-.621h4.707A2 2 0 0 1 9.828 3z"/>
                                    </svg>
                                    {{ (dataset.speakerStructure || getDefaultSpeakers()).length }} folders
                                </span>
                                <span class="stat-item">
                                    <svg width="14" height="14" fill="currentColor" viewBox="0 0 16 16">
                                        <path d="M14 4.5V14a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V2a2 2 0 0 1 2-2h5.5L14 4.5zm-3 0A1.5 1.5 0 0 1 9.5 3V1H4a1 1 0 0 0-1 1v12a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1V4.5h-2z"/>
                                    </svg>
                                    {{ dataset.utterances || '0' }} utterances
                                </span>
                            </div>
                        </div>
                        <div class="section-content file-browser">
                            <div class="file-tree-main">
                                <div class="folder-item root-main">
                                    <div class="folder-header-main">
                                        <svg width="16" height="16" fill="currentColor" viewBox="0 0 16 16" class="folder-icon">
                                            <path d="M9.828 3h3.982a2 2 0 0 1 1.992 2.181l-.637 7A2 2 0 0 1 13.174 14H2.825a2 2 0 0 1-1.991-1.819l-.637-7a1.99 1.99 0 0 1 .342-1.31L2.61 1a2 2 0 0 1 1.511-.621h4.707A2 2 0 0 1 9.828 3z"/>
                                        </svg>
                                        <span class="folder-name-main">{{ dataset.id || 'dataset_1' }}</span>
                                        <span class="folder-badge">Root</span>
                                    </div>
                                </div>
                                
                                <div class="file-tree-content-main">
                                    <div class="file-item-main">
                                        <div class="file-row">
                                            <div class="file-info">
                                                <svg width="16" height="16" fill="currentColor" viewBox="0 0 16 16" class="file-icon">
                                                    <path d="M14 4.5V14a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V2a2 2 0 0 1 2-2h5.5L14 4.5zm-3 0A1.5 1.5 0 0 1 9.5 3V1H4a1 1 0 0 0-1 1v12a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1V4.5h-2z"/>
                                                </svg>
                                                <span class="file-name-main">metadata.csv</span>
                                            </div>
                                            <div class="file-meta">
                                                <span class="file-size-main">12 KB</span>
                                                <span class="file-type">CSV</span>
                                            </div>
                                        </div>
                                    </div>
                                    
                                    <div class="folder-item-main nested">
                                        <div class="folder-row">
                                            <div class="folder-info">
                                                <svg width="16" height="16" fill="currentColor" viewBox="0 0 16 16" class="folder-icon">
                                                    <path d="M9.828 3h3.982a2 2 0 0 1 1.992 2.181l-.637 7A2 2 0 0 1 13.174 14H2.825a2 2 0 0 1-1.991-1.819l-.637-7a1.99 1.99 0 0 1 .342-1.31L2.61 1a2 2 0 0 1 1.511-.621h4.707A2 2 0 0 1 9.828 3z"/>
                                                </svg>
                                                <span class="folder-name-main">wav/</span>
                                            </div>
                                            <div class="folder-meta">
                                                <span class="folder-count-main">{{ dataset.speakers || 4 }} speakers</span>
                                            </div>
                                        </div>
                                    </div>
                                    
                                    <div class="file-tree-content-main nested">
                                        <div v-for="(speaker, index) in (dataset.speakerStructure || getDefaultSpeakers())" :key="speaker.id || `speaker_${index + 1}`" class="speaker-section">
                                            <div class="folder-item-main nested-deep">
                                                <div class="folder-row">
                                                    <div class="folder-info">
                                                        <svg width="14" height="14" fill="currentColor" viewBox="0 0 16 16" class="folder-icon">
                                                            <path d="M9.828 3h3.982a2 2 0 0 1 1.992 2.181l-.637 7A2 2 0 0 1 13.174 14H2.825a2 2 0 0 1-1.991-1.819l-.637-7a1.99 1.99 0 0 1 .342-1.31L2.61 1a2 2 0 0 1 1.511-.621h4.707A2 2 0 0 1 9.828 3z"/>
                                                        </svg>
                                                        <span class="folder-name-main">{{ speaker.id || `speaker_00${index + 1}` }}/</span>
                                                    </div>
                                                    <div class="folder-meta">
                                                        <span class="folder-count-main">{{ speaker.videos?.length || 2 }} videos</span>
                                                    </div>
                                                </div>
                                            </div>
                                            
                                            <div class="video-tree nested-deeper">
                                                <div v-for="video in (speaker.videos || ['video_001', 'video_002'])" :key="video" class="folder-item-main nested-deeper">
                                                    <div class="folder-row">
                                                        <div class="folder-info">
                                                            <svg width="12" height="12" fill="currentColor" viewBox="0 0 16 16" class="folder-icon">
                                                                <path d="M9.828 3h3.982a2 2 0 0 1 1.992 2.181l-.637 7A2 2 0 0 1 13.174 14H2.825a2 2 0 0 1-1.991-1.819l-.637-7a1.99 1.99 0 0 1 .342-1.31L2.61 1a2 2 0 0 1 1.511-.621h4.707A2 2 0 0 1 9.828 3z"/>
                                                            </svg>
                                                            <span class="folder-name-main">{{ video }}/</span>
                                                        </div>
                                                        <div class="folder-meta">
                                                            <span class="folder-count-main">2 utterances</span>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Sidebar - Dataset Information and Distributions -->
                <div class="sidebar-section">
                    <!-- Dataset Information -->
                    <div class="sidebar-card">
                        <div class="sidebar-header">
                            <div class="sidebar-title">
                                <svg width="18" height="18" fill="currentColor" viewBox="0 0 16 16">
                                    <path d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16zm.93-9.412-1 4.705c-.07.34.029.533.304.533.194 0 .487-.07.686-.246l-.088.416c-.287.346-.92.598-1.465.598-.703 0-1.002-.422-.808-1.319l.738-3.468c.064-.293.006-.399-.287-.47l-.451-.081.082-.381 2.29-.287zM8 5.5a1 1 0 1 1 0-2 1 1 0 0 1 0 2z"/>
                                </svg>
                                <h3>About</h3>
                            </div>
                        </div>
                        <div class="sidebar-content">
                            <div class="info-list">
                                <div class="info-row">
                                    <span class="info-key">Speakers</span>
                                    <span class="info-val">{{ dataset.speakers || '0' }}</span>
                                </div>
                                <div class="info-row">
                                    <span class="info-key">Utterances</span>
                                    <span class="info-val">{{ dataset.utterances || '0' }}</span>
                                </div>
                                <div class="info-row">
                                    <span class="info-key">Size</span>
                                    <span class="info-val">{{ dataset.size || 'N/A' }}</span>
                                </div>
                                <div class="info-row">
                                    <span class="info-key">Format</span>
                                    <span class="info-val">{{ dataset.format || 'WAV' }}</span>
                                </div>
                                <div class="info-row">
                                    <span class="info-key">Created</span>
                                    <span class="info-val">{{ formatDate(dataset.created) }}</span>
                                </div>
                                <div class="info-row">
                                    <span class="info-key">Updated</span>
                                    <span class="info-val">{{ formatDate(dataset.lastUpdated) }}</span>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Distributions -->
                    <div class="sidebar-card">
                        <div class="sidebar-header">
                            <div class="sidebar-title">
                                <svg width="18" height="18" fill="currentColor" viewBox="0 0 16 16">
                                    <path d="M1 11a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1v-3zM7.5 9a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v5a1 1 0 0 1-1 1h-2a1 1 0 0 1-1-1V9zM14 7a1 1 0 0 1 1 1v6a1 1 0 0 1-1 1h-2a1 1 0 0 1-1-1V8a1 1 0 0 1 1-1h2z"/>
                                </svg>
                                <h3>Distributions</h3>
                            </div>
                        </div>
                        <div class="sidebar-content">
                            <!-- Usage Distribution -->
                            <div class="mini-distribution">
                                <h4 class="mini-title">Usage Split</h4>
                                <div class="mini-chart">
                                    <div class="mini-bar">
                                        <div class="mini-training" :style="{ width: trainingPercentage + '%' }"></div>
                                        <div class="mini-test" :style="{ width: testPercentage + '%' }"></div>
                                    </div>
                                    <div class="mini-legend">
                                        <span class="mini-legend-item">
                                            <span class="mini-dot training"></span>
                                            Training {{ trainingPercentage }}%
                                        </span>
                                        <span class="mini-legend-item">
                                            <span class="mini-dot test"></span>
                                            Test {{ testPercentage }}%
                                        </span>
                                    </div>
                                </div>
                            </div>

                            <!-- Gender Distribution -->
                            <div class="mini-distribution">
                                <h4 class="mini-title">Gender Split</h4>
                                <div class="mini-chart">
                                    <div class="mini-bar">
                                        <div class="mini-male" :style="{ width: malePercentage + '%' }"></div>
                                        <div class="mini-female" :style="{ width: femalePercentage + '%' }"></div>
                                    </div>
                                    <div class="mini-legend">
                                        <span class="mini-legend-item">
                                            <span class="mini-dot male"></span>
                                            Male {{ malePercentage }}%
                                        </span>
                                        <span class="mini-legend-item">
                                            <span class="mini-dot female"></span>
                                            Female {{ femalePercentage }}%
                                        </span>
                                    </div>
                                </div>
                            </div>

                            <!-- Nationality Distribution -->
                            <div class="mini-distribution">
                                <h4 class="mini-title">Nationalities</h4>
                                <div class="nationality-mini-grid">
                                    <div 
                                        v-for="(count, nationality) in (dataset.nationalityDistribution || getDefaultNationalities())" 
                                        :key="nationality"
                                        class="nationality-mini-item"
                                    >
                                        <div class="nationality-mini-info">
                                            <span class="nationality-mini-name">{{ nationality }}</span>
                                            <span class="nationality-mini-count">{{ count }}</span>
                                        </div>
                                        <div class="nationality-mini-bar">
                                            <div 
                                                class="nationality-mini-fill" 
                                                :style="{ width: (count / getTotalSpeakers() * 100) + '%' }"
                                            ></div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Dataset Not Found -->
        <div v-if="!loading && !error && !dataset" class="not-found">
            <h2>Dataset Not Found</h2>
            <p>The requested dataset "{{ $route.params.id }}" could not be found.</p>
            <router-link to="/datasetslibrary" class="btn-primary">Back to Datasets</router-link>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import NavigationBar from '@/components/NavigationBar.vue'
import { useDatasets } from '@/composables/useDatasets'

const route = useRoute()
const { datasets, fetchDatasets } = useDatasets()

const dataset = ref(null)
const loading = ref(false)
const error = ref(null)

const trainingPercentage = computed(() => {
    if (!dataset.value) return 0
    const total = dataset.value.usage.training + dataset.value.usage.test
    return Math.round((dataset.value.usage.training / total) * 100)
})

const testPercentage = computed(() => {
    if (!dataset.value) return 0
    const total = dataset.value.usage.training + dataset.value.usage.test
    return Math.round((dataset.value.usage.test / total) * 100)
})

const malePercentage = computed(() => {
    if (!dataset.value?.genderDistribution) return 0
    const total = dataset.value.genderDistribution.male + dataset.value.genderDistribution.female
    return Math.round((dataset.value.genderDistribution.male / total) * 100)
})

const femalePercentage = computed(() => {
    if (!dataset.value?.genderDistribution) return 0
    const total = dataset.value.genderDistribution.male + dataset.value.genderDistribution.female
    return Math.round((dataset.value.genderDistribution.female / total) * 100)
})

const getTotalSpeakers = () => {
    if (!dataset.value?.nationalityDistribution) return 1 // Avoid division by zero
    return Object.values(dataset.value.nationalityDistribution).reduce((sum, count) => sum + count, 0) || 1
}

const fetchDatasetDetails = async () => {
    loading.value = true
    error.value = null
    
    try {
        await fetchDatasets()
        const datasetId = route.params.id
        dataset.value = datasets.value.find(d => d.id === datasetId)
        
        if (!dataset.value) {
            error.value = `Dataset "${datasetId}" not found`
        }
    } catch (err) {
        error.value = 'Failed to fetch dataset details'
        console.error('Error fetching dataset details:', err)
    } finally {
        loading.value = false
    }
}

const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    })
}

onMounted(() => {
    fetchDatasetDetails()
})
</script>

<style scoped>
.dataset-details-container {
    width: 75%;
    margin: 0 auto;
    padding: var(--space-6) var(--space-4);
}

.loading, .error, .not-found {
    text-align: center;
    padding: var(--space-8);
    background: var(--bg-secondary);
    border: 1px solid var(--border-default);
    border-radius: var(--radius-large);
    margin: var(--space-6) 0;
    box-shadow: var(--shadow-small);
}

.error {
    border-left: 4px solid var(--accent-danger);
    background: linear-gradient(135deg, rgba(218, 54, 51, 0.08), rgba(218, 54, 51, 0.02));
}

.retry-btn {
    background: var(--accent-secondary);
    color: white;
    border: none;
    padding: var(--space-3) var(--space-4);
    border-radius: var(--radius-medium);
    cursor: pointer;
    margin-top: var(--space-4);
    font-weight: 600;
    font-size: 0.9rem;
    transition: all 0.2s ease;
    box-shadow: var(--shadow-small);
}

.retry-btn:hover {
    background: #4f96ff;
    transform: translateY(-1px);
    box-shadow: var(--shadow-medium);
}

/* Header Section */
.dataset-header {
    background: linear-gradient(135deg, var(--bg-secondary), var(--bg-tertiary));
    border: 1px solid var(--border-default);
    border-radius: var(--radius-large);
    padding: var(--space-6);
    margin-bottom: var(--space-6);
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    box-shadow: var(--shadow-medium);
    position: relative;
    overflow: hidden;
}

.dataset-header::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, var(--accent-primary), var(--accent-secondary));
}

.header-content {
    flex: 1;
    padding-right: var(--space-4);
}

.title-section {
    display: flex;
    align-items: center;
    gap: var(--space-4);
    margin-bottom: var(--space-4);
}

.dataset-icon {
    width: 48px;
    height: 48px;
    background: var(--accent-primary);
    border-radius: var(--radius-medium);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    box-shadow: var(--shadow-small);
}

.title-content {
    flex: 1;
}

.title-content h1 {
    margin: 0 0 var(--space-2) 0;
    color: var(--text-primary);
    font-size: 2.25rem;
    font-weight: 700;
    line-height: 1.2;
}

.status-badge {
    display: inline-flex;
    align-items: center;
    gap: var(--space-1);
    padding: var(--space-1) var(--space-3);
    border-radius: var(--radius-large);
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.status-badge.active {
    background: rgba(35, 134, 54, 0.15);
    color: var(--accent-primary);
    border: 1px solid rgba(35, 134, 54, 0.3);
}

.description {
    color: var(--text-secondary);
    font-size: 1.1rem;
    line-height: 1.6;
    margin: 0;
    max-width: 600px;
}

.header-actions {
    display: flex;
    flex-direction: column;
    gap: var(--space-2);
    flex-shrink: 0;
}

.action-btn {
    display: inline-flex;
    align-items: center;
    gap: var(--space-2);
    padding: var(--space-3) var(--space-4);
    border: 1px solid transparent;
    border-radius: var(--radius-medium);
    cursor: pointer;
    font-weight: 600;
    font-size: 0.9rem;
    transition: all 0.2s ease;
    text-decoration: none;
    white-space: nowrap;
    min-width: 160px;
    justify-content: center;
}

/* Overview Section */
.overview-section {
    margin-bottom: var(--space-6);
}

.overview-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: var(--space-4);
}

.overview-card {
    background: linear-gradient(135deg, var(--bg-secondary), var(--bg-tertiary));
    border: 1px solid var(--border-default);
    border-radius: var(--radius-large);
    padding: var(--space-5);
    text-align: center;
    box-shadow: var(--shadow-small);
    transition: all 0.2s ease;
    position: relative;
    overflow: hidden;
}

.overview-card:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-medium);
}

.overview-card.primary-metric {
    background: linear-gradient(135deg, var(--accent-primary), #2ea043);
    color: white;
    border-color: var(--accent-primary);
}

.overview-card.primary-metric .metric-content h3,
.overview-card.primary-metric .metric-content p {
    color: white;
}

.metric-icon {
    width: 48px;
    height: 48px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: var(--radius-medium);
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto var(--space-3);
    color: var(--accent-secondary);
}

.overview-card.primary-metric .metric-icon {
    background: rgba(255, 255, 255, 0.2);
    color: white;
}

.metric-content h3 {
    font-size: 2.5rem;
    color: var(--text-primary);
    margin: 0 0 var(--space-1) 0;
    font-weight: 800;
    line-height: 1;
}

.metric-content p {
    color: var(--text-secondary);
    margin: 0;
    font-weight: 600;
    text-transform: uppercase;
    font-size: 0.8rem;
    letter-spacing: 0.5px;
}

/* Content Grid */
.main-content-layout {
    display: grid;
    grid-template-columns: 1fr 320px;
    gap: 2rem;
    margin-top: 2rem;
}

/* Main Section - File Structure */
.main-section {
    min-width: 0; /* Prevents grid overflow */
}

.main-card {
    border: 1px solid var(--border-default);
    background: var(--bg-secondary);
    border-radius: var(--radius-large);
    overflow: hidden;
    box-shadow: var(--shadow-small);
}

.section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: var(--space-4) var(--space-5);
    border-bottom: 1px solid var(--border-default);
    background: linear-gradient(135deg, var(--bg-tertiary), var(--bg-secondary));
}

.section-title {
    display: flex;
    align-items: center;
    gap: var(--space-3);
    color: var(--text-primary);
}

.section-title h2 {
    margin: 0;
    font-size: 1.1rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.section-title svg {
    color: var(--accent-secondary);
}

.file-stats {
    display: flex;
    gap: 1rem;
}

.stat-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    color: var(--text-secondary);
    font-size: 0.875rem;
}

/* File Browser Styles */
.file-browser {
    padding: 0;
}

.file-tree-main {
    font-family: var(--font-family-mono);
    font-size: 0.85rem;
}

.folder-item.root-main {
    padding: var(--space-4) var(--space-5);
    border-bottom: 1px solid var(--border-default);
    background: var(--bg-tertiary);
}

.folder-header-main {
    display: flex;
    align-items: center;
    gap: var(--space-3);
}

.folder-name-main {
    font-weight: 600;
    color: var(--text-primary);
}

.folder-badge {
    background: var(--accent-primary);
    color: white;
    padding: 0.25rem 0.5rem;
    border-radius: var(--radius-large);
    font-size: 0.75rem;
    font-weight: 500;
}

.file-tree-content-main {
    padding: 0;
}

.file-item-main {
    border-bottom: 1px solid var(--border-muted);
}

.file-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: var(--space-3) var(--space-5);
    transition: background-color 0.15s ease;
}

.file-row:hover {
    background: var(--bg-tertiary);
}

.file-info {
    display: flex;
    align-items: center;
    gap: var(--space-3);
}

.file-name-main {
    color: var(--text-primary);
    font-weight: 500;
}

.file-meta {
    display: flex;
    gap: 1rem;
    align-items: center;
}

.file-size-main {
    color: var(--text-secondary);
    font-size: 0.875rem;
}

.file-type {
    background: #e3f2fd;
    color: #1976d2;
    padding: 0.25rem 0.5rem;
    border-radius: var(--radius-small);
    font-size: 0.75rem;
    font-weight: 500;
}

.folder-item-main.nested {
    border-bottom: 1px solid var(--border-muted);
}

.folder-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: var(--space-3) var(--space-5);
    transition: background-color 0.15s ease;
}

.folder-row:hover {
    background: var(--bg-tertiary);
}

.folder-info {
    display: flex;
    align-items: center;
    gap: var(--space-3);
}

.folder-meta {
    display: flex;
    align-items: center;
}

.folder-count-main {
    color: var(--text-secondary);
    font-size: 0.875rem;
}

.folder-item-main.nested-deep .folder-row {
    padding-left: calc(var(--space-5) + var(--space-4));
}

.folder-item-main.nested-deeper .folder-row {
    padding-left: calc(var(--space-5) + var(--space-8));
}

.video-tree {
    border-left: 2px solid var(--border-muted);
    margin-left: calc(var(--space-5) + var(--space-4));
}

.speaker-section {
    border-bottom: 1px solid var(--border-muted);
}

.folder-icon,
.file-icon {
    color: var(--accent-secondary);
    flex-shrink: 0;
}

/* Sidebar Styles */
.sidebar-section {
    display: flex;
    flex-direction: column;
    gap: var(--space-4);
}

.sidebar-card {
    border: 1px solid var(--border-default);
    background: var(--bg-secondary);
    border-radius: var(--radius-large);
    overflow: hidden;
    box-shadow: var(--shadow-small);
}

.sidebar-header {
    padding: var(--space-4) var(--space-5);
    border-bottom: 1px solid var(--border-default);
    background: linear-gradient(135deg, var(--bg-tertiary), var(--bg-secondary));
}

.sidebar-title {
    display: flex;
    align-items: center;
    gap: var(--space-2);
    color: var(--text-primary);
}

.sidebar-title h3 {
    margin: 0;
    font-size: 1rem;
    font-weight: 600;
}

.sidebar-title svg {
    color: var(--accent-secondary);
}

.sidebar-content {
    padding: var(--space-5);
}

/* Information List */
.info-list {
    display: flex;
    flex-direction: column;
    gap: var(--space-3);
}

.info-row {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    padding: var(--space-2) 0;
    border-bottom: 1px solid var(--border-muted);
}

.info-row:last-child {
    border-bottom: none;
}

.info-key {
    color: var(--text-secondary);
    font-size: 0.875rem;
    font-weight: 500;
}

.info-val {
    color: var(--text-primary);
    font-size: 0.875rem;
    text-align: right;
    max-width: 60%;
    word-break: break-word;
    font-weight: 600;
}

/* Mini Distributions */
.mini-distribution {
    margin-bottom: var(--space-4);
}

.mini-distribution:last-child {
    margin-bottom: 0;
}

.mini-title {
    margin: 0 0 var(--space-3) 0;
    font-size: 0.875rem;
    font-weight: 600;
    color: var(--text-primary);
}

.mini-chart {
    display: flex;
    flex-direction: column;
    gap: var(--space-2);
}

.mini-bar {
    height: 8px;
    background: var(--bg-tertiary);
    border-radius: var(--radius-small);
    overflow: hidden;
    display: flex;
}

.mini-training {
    background: linear-gradient(90deg, var(--accent-primary), #2ea043);
}

.mini-test {
    background: linear-gradient(90deg, var(--accent-warning), #f1c40f);
}

.mini-male {
    background: linear-gradient(90deg, var(--accent-secondary), #4f96ff);
}

.mini-female {
    background: linear-gradient(90deg, #e91e63, #ff6b9d);
}

.mini-legend {
    display: flex;
    flex-wrap: wrap;
    gap: var(--space-3);
}

.mini-legend-item {
    display: flex;
    align-items: center;
    gap: var(--space-1);
    font-size: 0.75rem;
    color: var(--text-secondary);
}

.mini-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
}

.mini-dot.training {
    background: var(--accent-primary);
}

.mini-dot.test {
    background: var(--accent-warning);
}

.mini-dot.male {
    background: var(--accent-secondary);
}

.mini-dot.female {
    background: #e91e63;
}

/* Nationality Mini Grid */
.nationality-mini-grid {
    display: flex;
    flex-direction: column;
    gap: var(--space-2);
}

.nationality-mini-item {
    display: flex;
    flex-direction: column;
    gap: var(--space-1);
}

.nationality-mini-info {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.nationality-mini-name {
    font-size: 0.75rem;
    color: var(--text-primary);
    font-weight: 500;
}

.nationality-mini-count {
    font-size: 0.75rem;
    color: var(--text-secondary);
}

.nationality-mini-bar {
    height: 4px;
    background: var(--bg-tertiary);
    border-radius: var(--radius-small);
    overflow: hidden;
}

.nationality-mini-fill {
    height: 100%;
    background: linear-gradient(90deg, var(--accent-primary), #2ea043);
    transition: width 0.3s ease;
}

/* Responsive Design */
@media (max-width: 1024px) {
    .main-content-layout {
        grid-template-columns: 1fr;
        gap: var(--space-4);
    }
    
    .sidebar-section {
        order: -1;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        display: grid;
    }
}

@media (max-width: 768px) {
    .section-header {
        flex-direction: column;
        align-items: flex-start;
        gap: var(--space-3);
    }
    
    .file-stats {
        flex-wrap: wrap;
    }
    
    .folder-item-main.nested-deep .folder-row {
        padding-left: calc(var(--space-5) + var(--space-2));
    }
    
    .folder-item-main.nested-deeper .folder-row {
        padding-left: calc(var(--space-5) + var(--space-4));
    }
    
    .video-tree {
        margin-left: calc(var(--space-5) + var(--space-2));
    }
    
    .sidebar-section {
        grid-template-columns: 1fr;
    }
}

/* Button Styles */
.btn-primary,
.btn-secondary,
.btn-tertiary {
    padding: var(--space-3) var(--space-4);
    border: 1px solid transparent;
    border-radius: var(--radius-medium);
    cursor: pointer;
    font-weight: 600;
    font-size: 0.9rem;
    transition: all 0.2s ease;
    text-decoration: none;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: var(--space-2);
    box-shadow: var(--shadow-small);
}

.btn-primary {
    background: linear-gradient(135deg, var(--accent-primary), #2ea043);
    color: white;
    border-color: var(--accent-primary);
}

.btn-primary:hover {
    background: linear-gradient(135deg, #2ea043, var(--accent-primary));
    transform: translateY(-1px);
    box-shadow: var(--shadow-medium);
}

.btn-secondary {
    background: var(--bg-tertiary);
    color: var(--text-primary);
    border-color: var(--border-default);
}

.btn-secondary:hover {
    background: var(--bg-overlay);
    border-color: var(--accent-secondary);
    transform: translateY(-1px);
}

.btn-tertiary {
    background: transparent;
    color: var(--text-secondary);
    border-color: var(--border-default);
}

.btn-tertiary:hover {
    background: var(--bg-tertiary);
    color: var(--text-primary);
    border-color: var(--accent-secondary);
}

/* Responsive Design */
@media (max-width: 1024px) {
    .dataset-details-container {
        padding: var(--space-4) var(--space-3);
    }
    
    .overview-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (max-width: 768px) {
    .dataset-header {
        flex-direction: column;
        gap: var(--space-4);
        text-align: center;
    }
    
    .header-content {
        padding-right: 0;
    }
    
    .header-actions {
        flex-direction: row;
        width: 100%;
        justify-content: center;
        flex-wrap: wrap;
    }
    
    .action-btn {
        min-width: auto;
        flex: 1;
        min-width: 120px;
    }
    
    .overview-grid {
        grid-template-columns: 1fr;
    }
    
    .title-content h1 {
        font-size: 1.8rem;
    }
}

@media (max-width: 480px) {
    .dataset-details-container {
        padding: var(--space-3) var(--space-2);
    }
    
    .title-section {
        flex-direction: column;
        text-align: center;
        gap: var(--space-3);
    }
    
    .dataset-icon {
        width: 40px;
        height: 40px;
    }
    
    .header-actions {
        flex-direction: column;
    }
    
    .section-header {
        padding: var(--space-3) var(--space-4);
    }
    
    .section-content {
        padding: var(--space-4);
    }
}
</style>