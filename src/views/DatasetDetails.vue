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
                        <h1>{{ dataset.name }}</h1>
                    </div>
                    <p class="description">{{ dataset.description }}</p>
                </div>
                <div class="header-actions">
                    <button class="btn-primary">Download Dataset</button>
                    <button class="btn-secondary">Export Metadata</button>
                    <router-link to="/datasetslibrary" class="btn-secondary">Back to Library</router-link>
                </div>
            </div>

            <!-- Overview Cards -->

            <!-- Main Content Grid -->
            <div class="content-grid">
                <!-- Dataset Information -->
                <div class="info-section">
                    <div class="section-card">
                        <h2>Dataset Information</h2>
                        <div class="info-grid">
                            <div class="info-item">
                                <span class="label">Type:</span>
                                <span class="value">{{ dataset.type }}</span>
                            </div>
                            <div class="info-item">
                                <span class="label">Created:</span>
                                <span class="value">{{ formatDate(dataset.created) }}</span>
                            </div>
                            <div class="info-item">
                                <span class="label">Last Updated:</span>
                                <span class="value">{{ formatDate(dataset.lastUpdated) }}</span>
                            </div>

                            <div class="info-item">
                                <span class="label">Speakers</span>
                                <span class="value">{{ dataset.speakers }}</span>
                                
                            </div>
                            <div class="info-item">
                                <span class="label">Utterances</span>
                                <span class="value">{{ dataset.utterances }}</span>

                            </div>
                            <div class="info-item">
                                <span class="label">Total Size</span>
                                <span class="value">{{ dataset.size }}</span>

                            </div>
                            <div class="info-item">
                                <span class="label">Format</span>
                                <span class="value">{{ dataset.format }}</span>
                            </div>     
                        </div>
                    </div>

                    <!-- Usage Distribution -->
                    <div class="section-card">
                        <h2>Usage Distribution</h2>
                        <div class="usage-chart">
                            <div class="usage-bar">
                                <div class="training-bar" :style="{ width: trainingPercentage + '%' }"></div>
                                <div class="test-bar" :style="{ width: testPercentage + '%' }"></div>
                            </div>
                            <div class="usage-legend">
                                <div class="legend-item">
                                    <span class="legend-color training"></span>
                                    <span>Training: {{ dataset.usage.training }} ({{ trainingPercentage }}%)</span>
                                </div>
                                <div class="legend-item">
                                    <span class="legend-color test"></span>
                                    <span>Test: {{ dataset.usage.test }} ({{ testPercentage }}%)</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- File Structure -->
                <div class="structure-section">
                    <div class="section-card">
                        <h2>File Structure</h2>
                        <div class="file-tree">
                            <div class="folder-item">
                                <span class="folder-icon">📁</span>
                                <span class="folder-name">{{ dataset.id }}</span>
                            </div>
                            <div class="file-tree-content">
                                <div class="file-item">
                                    <span class="file-icon">📄</span>
                                    <span class="file-name">metadata.csv</span>
                                </div>
                                <div class="folder-item nested">
                                    <span class="folder-icon">📁</span>
                                    <span class="folder-name">wav</span>
                                </div>
                                <div class="file-tree-content nested">
                                    <div v-for="speaker in dataset.speakerStructure" :key="speaker.id" class="speaker-folder">
                                        <div class="folder-item nested">
                                            <span class="folder-icon">📁</span>
                                            <span class="folder-name">{{ speaker.id }}</span>
                                        </div>
                                        <div class="file-tree-content nested">
                                            <div v-for="video in speaker.videos" :key="video" class="folder-item nested">
                                                <span class="folder-icon">📁</span>
                                                <span class="folder-name">{{ video }}</span>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Sample Data Preview -->
                    <div class="section-card">
                        <h2>Gender Distribution</h2>
                        <div class="distribution-chart">
                            <div class="distribution-bar">
                                <div class="male-bar" :style="{ width: malePercentage + '%' }"></div>
                                <div class="female-bar" :style="{ width: femalePercentage + '%' }"></div>
                            </div>
                            <div class="distribution-legend">
                                <div class="legend-item">
                                    <span class="legend-color male"></span>
                                    <span>Male: {{ dataset.genderDistribution.male }} ({{ malePercentage }}%)</span>
                                </div>
                                <div class="legend-item">
                                    <span class="legend-color female"></span>
                                    <span>Female: {{ dataset.genderDistribution.female }} ({{ femalePercentage }}%)</span>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Nationality Distribution -->
                    <div class="section-card">
                        <h2>Nationality Distribution</h2>
                        <div class="nationality-grid">
                            <div 
                                v-for="(count, nationality) in dataset.nationalityDistribution" 
                                :key="nationality"
                                class="nationality-item"
                            >
                                <div class="nationality-info">
                                    <span class="nationality-name">{{ nationality }}</span>
                                    <span class="nationality-count">{{ count }} speakers</span>
                                </div>
                                <div class="nationality-bar">
                                    <div 
                                        class="nationality-fill" 
                                        :style="{ width: (count / getTotalSpeakers() * 100) + '%' }"
                                    ></div>
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
    if (!dataset.value?.nationalityDistribution) return 0
    return Object.values(dataset.value.nationalityDistribution).reduce((sum, count) => sum + count, 0)
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
    padding: var(--space-5);
    width: 70%;
    margin: 0 auto;
}

.loading, .error, .not-found {
    text-align: center;
    padding: var(--space-6);
    background: var(--bg-secondary);
    border: 1px solid var(--border-default);
    border-radius: var(--radius-medium);
    margin: var(--space-5) 0;
}

.error {
    border-left: 4px solid var(--accent-danger);
    background-color: rgba(218, 54, 51, 0.15);
}

.retry-btn {
    background: var(--accent-secondary);
    color: var(--text-primary);
    border: none;
    padding: var(--space-2) var(--space-3);
    border-radius: var(--radius-small);
    cursor: pointer;
    margin-top: var(--space-3);
    font-weight: 500;
    transition: all 0.2s ease;
}

.retry-btn:hover {
    background: #4f96ff;
    box-shadow: var(--shadow-small);
}

.dataset-header {
    background: var(--bg-secondary);
    border: 1px solid var(--border-default);
    border-radius: var(--radius-medium);
    padding: var(--space-5);
    margin-bottom: var(--space-5);
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    box-shadow: var(--shadow-small);
}

.header-content {
    flex: 1;
}

.title-section {
    display: flex;
    align-items: center;
    gap: var(--space-3);
    margin-bottom: var(--space-3);
}

.title-section h1 {
    margin: 0;
    color: var(--text-primary);
    font-size: 2.5rem;
    font-weight: 600;
}

.status-badge {
    padding: var(--space-1) var(--space-2);
    border-radius: var(--radius-large);
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
}

.status-badge.active {
    background: rgba(35, 134, 54, 0.15);
    color: var(--accent-primary);
    border: 1px solid var(--accent-primary);
}

.description {
    color: var(--text-secondary);
    font-size: 1.125rem;
    line-height: 1.6;
    margin: 0;
}

.header-actions {
    display: flex;
    gap: var(--space-2);
    flex-direction: column;
}

.overview-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: var(--space-3);
    margin-bottom: var(--space-5);
}

.overview-card {
    background: var(--bg-secondary);
    border: 1px solid var(--border-default);
    border-radius: var(--radius-medium);
    padding: var(--space-4);
    text-align: center;
    box-shadow: var(--shadow-small);
}

.overview-card h3 {
    font-size: 2.5rem;
    color: var(--accent-secondary);
    margin: 0 0 var(--space-1) 0;
    font-weight: 700;
}

.overview-card p {
    color: var(--text-secondary);
    margin: 0;
    font-weight: 500;
    text-transform: uppercase;
    font-size: 0.875rem;
    letter-spacing: 0.5px;
}

.content-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: var(--space-5);
}

.section-card {
    background: var(--bg-secondary);
    border: 1px solid var(--border-default);
    border-radius: var(--radius-medium);
    padding: var(--space-4);
    margin-bottom: var(--space-4);
    box-shadow: var(--shadow-small);
}

.section-card h2 {
    color: var(--text-primary);
    margin: 0 0 var(--space-3) 0;
    font-size: 1.25rem;
    font-weight: 600;
    border-bottom: 1px solid var(--border-default);
    padding-bottom: var(--space-2);
}

.info-grid {
    display: grid;
    gap: var(--space-3);
}

.info-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: var(--space-2) 0;
}

.label {
    font-weight: 600;
    color: var(--text-primary);
    font-size: 0.875rem;
}

.value {
    color: var(--text-secondary);
    font-size: 0.875rem;
    font-family: var(--font-family-mono);
}

.language-tags {
    display: flex;
    gap: var(--space-2);
    flex-wrap: wrap;
}

.language-tag {
    background: var(--bg-tertiary);
    color: var(--accent-secondary);
    padding: var(--space-2) var(--space-3);
    border-radius: var(--radius-small);
    font-size: 0.875rem;
    border: 1px solid var(--border-default);
    font-weight: 500;
}

.usage-chart {
    margin-top: var(--space-3);
}

.usage-bar {
    display: flex;
    height: 20px;
    border-radius: var(--radius-small);
    overflow: hidden;
    margin-bottom: var(--space-3);
    background: var(--bg-tertiary);
}

.training-bar {
    background: var(--accent-primary);
    transition: width 0.3s ease;
}

.test-bar {
    background: var(--accent-warning);
    transition: width 0.3s ease;
}

.usage-legend {
    display: flex;
    gap: var(--space-4);
}

.legend-item {
    display: flex;
    align-items: center;
    gap: var(--space-2);
    font-size: 0.875rem;
    color: var(--text-secondary);
}

.legend-color {
    width: 12px;
    height: 12px;
    border-radius: 2px;
}

.legend-color.training {
    background: var(--accent-primary);
}

.legend-color.test {
    background: var(--accent-warning);
}

.file-tree {
    font-family: var(--font-family-mono);
    font-size: 0.875rem;
}

.folder-item, .file-item {
    display: flex;
    align-items: center;
    gap: var(--space-2);
    padding: var(--space-1) 0;
    color: var(--text-secondary);
}

.folder-item.nested, .file-item.nested {
    margin-left: var(--space-4);
}

.file-tree-content.nested {
    margin-left: var(--space-4);
}

.folder-name, .file-name {
    color: var(--text-primary);
}

.file-count {
    color: var(--text-muted);
    font-size: 0.75rem;
    margin-left: var(--space-2);
}

.metadata-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: var(--space-3);
}

.metadata-table th,
.metadata-table td {
    padding: var(--space-2) var(--space-3);
    text-align: left;
    border-bottom: 1px solid var(--border-default);
    font-size: 0.875rem;
}

.metadata-table th {
    background: var(--bg-tertiary);
    font-weight: 600;
    color: var(--text-primary);
}

.metadata-table td {
    color: var(--text-secondary);
}

.usage-badge {
    padding: var(--space-1) var(--space-2);
    border-radius: var(--radius-small);
    font-size: 0.75rem;
    font-weight: 500;
    text-transform: uppercase;
}

.usage-badge.training {
    background: rgba(35, 134, 54, 0.15);
    color: var(--accent-primary);
}

.usage-badge.test {
    background: rgba(210, 153, 34, 0.15);
    color: var(--accent-warning);
}

.distribution-chart {
    margin-top: var(--space-3);
}

.distribution-bar {
    display: flex;
    height: 20px;
    border-radius: var(--radius-small);
    overflow: hidden;
    margin-bottom: var(--space-3);
    background: var(--bg-tertiary);
}

.male-bar {
    background: var(--accent-secondary);
    transition: width 0.3s ease;
}

.female-bar {
    background: #e91e63;
    transition: width 0.3s ease;
}

.distribution-legend {
    display: flex;
    gap: var(--space-4);
}

.legend-color.male {
    background: var(--accent-secondary);
}

.legend-color.female {
    background: #e91e63;
}

.nationality-grid {
    display: grid;
    gap: var(--space-3);
    margin-top: var(--space-3);
}

.nationality-item {
    display: flex;
    flex-direction: column;
    gap: var(--space-2);
}

.nationality-info {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.nationality-name {
    font-weight: 600;
    color: var(--text-primary);
    font-size: 0.875rem;
}

.nationality-count {
    color: var(--text-secondary);
    font-size: 0.875rem;
}

.nationality-bar {
    height: 8px;
    background: var(--bg-tertiary);
    border-radius: var(--radius-small);
    overflow: hidden;
}

.nationality-fill {
    height: 100%;
    background: var(--accent-primary);
    transition: width 0.3s ease;
}

.btn-primary, .btn-secondary {
    padding: var(--space-2) var(--space-3);
    border: 1px solid transparent;
    border-radius: var(--radius-small);
    cursor: pointer;
    font-weight: 500;
    font-size: 0.875rem;
    transition: all 0.2s ease;
    text-decoration: none;
    display: inline-flex;
    align-items: center;
    justify-content: center;
}

.btn-primary {
    background: var(--accent-primary);
    color: var(--text-primary);
    border-color: rgba(240, 246, 252, 0.1);
}

.btn-primary:hover {
    background: #2ea043;
    box-shadow: var(--shadow-small);
}

.btn-secondary {
    background: var(--bg-tertiary);
    color: var(--text-primary);
    border-color: var(--border-default);
}

.btn-secondary:hover {
    background: var(--bg-overlay);
    border-color: var(--text-muted);
}

@media (max-width: 768px) {
    .content-grid {
        grid-template-columns: 1fr;
    }
    
    .dataset-header {
        flex-direction: column;
        gap: var(--space-4);
    }
    
    .header-actions {
        flex-direction: row;
        width: 100%;
    }
    
    .overview-grid {
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    }
}
</style>