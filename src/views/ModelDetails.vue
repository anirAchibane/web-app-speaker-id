<template>
    <div>
        <NavigationBar />
        
        <div class="model-details-container">
            <!-- Loading State -->
            <div v-if="loading" class="loading">
                <div class="loading-spinner"></div>
                <p>Loading model details...</p>
            </div>

            <!-- Error State -->
            <div v-else-if="error" class="error">
                <h3>Error Loading Model</h3>
                <p>{{ error }}</p>
                <button @click="fetchModelDetails" class="retry-btn">Try Again</button>
            </div>

            <!-- Model Not Found -->
            <div v-else-if="!model" class="not-found">
                <h3>Model Not Found</h3>
                <p>The requested model "{{ $route.params.id }}" could not be found.</p>
                <router-link to="/modelmanage" class="btn-primary">Back to Models</router-link>
            </div>

            <!-- Model Details Content -->
            <div v-else class="model-details">
                <!-- Header Section -->
                <div class="model-header">
                    <div class="model-icon">
                        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>
                            <path d="M2 17L12 22L22 17" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>
                            <path d="M2 12L12 17L22 12" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>
                        </svg>
                    </div>
                    <div class="model-info">
                        <h1>{{ model.name }}</h1>
                        <p class="model-description">{{ model.description || 'No description available' }}</p>
                        <div class="model-metadata">
                            <span class="metadata-item">
                                <strong>Architecture:</strong> {{ model.architecture }}
                            </span>
                            <span class="metadata-item">
                                <strong>Version:</strong> {{ model.version }}
                            </span>
                            <span class="metadata-item">
                                <strong>Created:</strong> {{ formatDate(model.created_at) }}
                            </span>
                        </div>
                    </div>
                    <div class="model-actions">
                        <button class="action-btn primary" @click="downloadModel">
                            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M21 15V19A2 2 0 0 1 19 21H5A2 2 0 0 1 3 19V15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                                <polyline points="7,10 12,15 17,10" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                                <line x1="12" y1="15" x2="12" y2="3" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                            </svg>
                            Download
                        </button>

                    </div>
                </div>

                <!-- Main Content -->
                <div class="model-content">


                    <!-- Sidebar -->
                    <div class="model-sidebar">
                        <!-- Model Information -->
                        <div class="sidebar-section">
                            <h3>Model Information</h3>
                            <div class="info-grid">
                                <div class="info-item">
                                    <span class="info-label">Accuracy</span>
                                    <span class="info-value">{{ formatPercentage(model.accuracy) }}%</span>
                                </div>
                                <div class="info-item">
                                    <span class="info-label">Training Time</span>
                                    <span class="info-value">{{ model.training_time || 'N/A' }}</span>
                                </div>
                                <div class="info-item">
                                    <span class="info-label">Model Size</span>
                                    <span class="info-value">{{ formatFileSize(model.size) }}</span>
                                </div>
                            </div>
                        </div>

                        <!-- Performance Metrics -->
                        <div class="sidebar-section">
                            <h3>Performance Metrics</h3>
                            
                            <!-- Accuracy Chart -->
                            <div class="chart-container">
                                <div class="chart-header">
                                    <span class="chart-title">Training Accuracy</span>
                                    <span class="chart-value">{{ formatPercentage(model.accuracy) }}%</span>
                                </div>
                                <div class="progress-bar">
                                    <div class="progress-fill training" :style="{ width: formatPercentage(model.accuracy) + '%' }"></div>
                                </div>
                            </div>

                            <!-- Validation Accuracy Chart -->
                            <div class="chart-container">
                                <div class="chart-header">
                                    <span class="chart-title">Validation Accuracy</span>
                                    <span class="chart-value">{{ formatPercentage(model.validation_accuracy) }}%</span>
                                </div>
                                <div class="progress-bar">
                                    <div class="progress-fill validation" :style="{ width: formatPercentage(model.validation_accuracy) + '%' }"></div>
                                </div>
                            </div>

                            <!-- Loss Chart -->
                            <div class="chart-container">
                                <div class="chart-header">
                                    <span class="chart-title">Final Loss</span>
                                    <span class="chart-value">{{ formatLoss(model.loss) }}</span>
                                </div>
                                <div class="progress-bar">
                                    <div class="progress-fill loss" :style="{ width: getLossPercentage(model.loss) + '%' }"></div>
                                </div>
                            </div>
                        </div>

                        <!-- Class Distribution -->
                        <div v-if="model.class_distribution" class="sidebar-section">
                            <h3>Class Distribution</h3>
                            <div class="distribution-list">
                                <div 
                                    v-for="(count, className) in model.class_distribution" 
                                    :key="className"
                                    class="distribution-item"
                                >
                                    <div class="distribution-header">
                                        <span class="class-name">{{ className }}</span>
                                        <span class="class-count">{{ count }}</span>
                                    </div>
                                    <div class="distribution-bar">
                                        <div 
                                            class="distribution-fill"
                                            :style="{ 
                                                width: getClassPercentage(count) + '%',
                                                backgroundColor: getClassColor(className)
                                            }"
                                        ></div>
                                    </div>
                                    <span class="distribution-percentage">{{ Math.round(getClassPercentage(count)) }}%</span>
                                </div>
                            </div>
                        </div>

                        <!-- Training Configuration -->
                        <div class="sidebar-section">
                            <h3>Training Configuration</h3>
                            <div class="config-list">
                                <div class="config-item">
                                    <span class="config-label">Epochs</span>
                                    <span class="config-value">{{ model.epochs || 'N/A' }}</span>
                                </div>
                                <div class="config-item">
                                    <span class="config-label">Batch Size</span>
                                    <span class="config-value">{{ model.batch_size || 'N/A' }}</span>
                                </div>
                                <div class="config-item">
                                    <span class="config-label">Learning Rate</span>
                                    <span class="config-value">{{ model.learning_rate || 'N/A' }}</span>
                                </div>
                                <div class="config-item">
                                    <span class="config-label">Dataset Used</span>
                                    <span class="config-value">{{ model.dataset_name || 'Unknown' }}</span>
                                </div>
                            </div>
                        </div>

                        <!-- Previous Versions -->
                        <div class="sidebar-section">
                            <h3>Previous Versions</h3>
                            
                            <!-- Loading state for versions -->
                            <div v-if="loadingVersions" class="versions-loading">
                                <div class="small-spinner"></div>
                                <span>Loading versions...</span>
                            </div>
                            
                            <!-- No previous versions -->
                            <div v-else-if="previousVersions.length === 0" class="no-versions">
                                <p>No previous versions found for this model.</p>
                            </div>
                            
                            <!-- Previous versions list -->
                            <div v-else class="versions-list">
                                <div 
                                    v-for="version in previousVersions" 
                                    :key="version.id"
                                    class="version-item"
                                    @click="$router.push(`/modeldetails/${version.id}`)"
                                >
                                    <div class="version-header">
                                        <span class="version-number">v{{ version.version }}</span>
                                        <span class="version-date">{{ formatDate(version.created_at) }}</span>
                                    </div>
                                    <div class="version-details">
                                        <span class="version-accuracy">{{ formatPercentage(version.accuracy) }}% accuracy</span>
                                        <span class="version-size">{{ formatFileSize(version.size) }}</span>
                                    </div>
                                    <div class="version-status" :class="version.status?.toLowerCase()">
                                        {{ version.status || 'Unknown' }}
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import NavigationBar from '@/components/NavigationBar.vue'
import { useModels } from '@/composables/useModels'

const route = useRoute()
const { models, fetchModels } = useModels()

const model = ref(null)
const loading = ref(false)
const error = ref(null)
const previousVersions = ref([])
const loadingVersions = ref(false)

const formatPercentage = (value) => {
    if (!value) return 0
    return Math.round(value * 100) / 100
}

const formatFileSize = (bytes) => {
    if (!bytes) return 'N/A'
    const sizes = ['B', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(1024))
    return `${(bytes / Math.pow(1024, i)).toFixed(1)} ${sizes[i]}`
}

const formatLoss = (loss) => {
    if (!loss) return 'N/A'
    return loss.toFixed(4)
}

const getLossPercentage = (loss) => {
    if (!loss) return 0
    // Invert loss for progress bar (lower loss = higher percentage)
    return Math.max(0, Math.min(100, (1 - loss) * 100))
}

const getClassPercentage = (count) => {
    if (!model.value?.class_distribution) return 0
    const total = Object.values(model.value.class_distribution).reduce((sum, c) => sum + c, 0) || 1
    return (count / total) * 100
}

const getClassColor = (className) => {
    const colors = [
        '#6366f1', '#8b5cf6', '#ec4899', '#ef4444', '#f97316',
        '#eab308', '#22c55e', '#10b981', '#06b6d4', '#0ea5e9'
    ]
    const index = className.charCodeAt(0) % colors.length
    return colors[index]
}



const downloadModel = () => {
    // Placeholder for download functionality
    console.log('Downloading model:', model.value.id)
}

const fetchPreviousVersions = async () => {
    if (!model.value?.name) return
    
    loadingVersions.value = true
    try {
        // Filter models with the same name but different versions
        const sameNameModels = models.value.filter(m => 
            m.name === model.value.name && m.id !== model.value.id
        )
        
        // Sort by creation date (newest first) or version number
        previousVersions.value = sameNameModels.sort((a, b) => {
            // Try to sort by version if it's a number
            const versionA = parseFloat(a.version) || 0
            const versionB = parseFloat(b.version) || 0
            if (versionA !== versionB) {
                return versionB - versionA
            }
            // Fallback to creation date
            return new Date(b.created_at) - new Date(a.created_at)
        })
    } catch (err) {
        console.error('Error fetching previous versions:', err)
    } finally {
        loadingVersions.value = false
    }
}

const fetchModelDetails = async () => {
    loading.value = true
    error.value = null
    
    try {
        await fetchModels()
        const modelId = route.params.id
        model.value = models.value.find(m => m.id === modelId)
        
        if (!model.value) {
            error.value = `Model "${modelId}" not found`
        } else {
            // Fetch previous versions after finding the model
            await fetchPreviousVersions()
        }
    } catch (err) {
        error.value = 'Failed to fetch model details'
        console.error('Error fetching model details:', err)
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
    fetchModelDetails()
})
</script>

<style scoped>
.model-details-container {
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

.loading-spinner {
    width: 40px;
    height: 40px;
    border: 3px solid var(--border-default);
    border-top: 3px solid var(--accent-primary);
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin: 0 auto var(--space-4);
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

.model-details {
    animation: fadeIn 0.6s ease-out;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

.model-header {
    display: flex;
    align-items: flex-start;
    gap: var(--space-6);
    padding: var(--space-6);
    background: var(--bg-secondary);
    border: 1px solid var(--border-default);
    border-radius: var(--radius-large);
    margin-bottom: var(--space-6);
    box-shadow: var(--shadow-small);
}

.model-icon {
    width: 80px;
    height: 80px;
    background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
    border-radius: var(--radius-large);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    box-shadow: var(--shadow-medium);
    flex-shrink: 0;
}

.model-icon svg {
    width: 40px;
    height: 40px;
}

.model-info {
    flex: 1;
}

.model-info h1 {
    margin: 0 0 var(--space-2);
    font-size: 2rem;
    font-weight: 700;
    color: var(--text-primary);
}

.model-description {
    margin: 0 0 var(--space-4);
    color: var(--text-secondary);
    font-size: 1.1rem;
    line-height: 1.6;
}

.model-metadata {
    display: flex;
    flex-wrap: wrap;
    gap: var(--space-6);
}

.metadata-item {
    color: var(--text-secondary);
    font-size: 0.9rem;
}

.metadata-item strong {
    color: var(--text-primary);
}

.model-actions {
    display: flex;
    flex-direction: column;
    gap: var(--space-3);
}

.action-btn {
    display: flex;
    align-items: center;
    gap: var(--space-2);
    padding: var(--space-3) var(--space-4);
    border: none;
    border-radius: var(--radius-medium);
    cursor: pointer;
    font-weight: 600;
    font-size: 0.9rem;
    transition: all 0.2s ease;
    min-width: 120px;
    justify-content: center;
}

.action-btn svg {
    width: 18px;
    height: 18px;
}

.action-btn.primary {
    background: var(--accent-primary);
    color: white;
    box-shadow: var(--shadow-small);
}

.action-btn.primary:hover {
    background: var(--accent-secondary);
    transform: translateY(-1px);
    box-shadow: var(--shadow-medium);
}

.action-btn.secondary {
    background: var(--bg-primary);
    color: var(--text-secondary);
    border: 1px solid var(--border-default);
}

.action-btn.secondary:hover {
    background: var(--bg-secondary);
    color: var(--accent-danger);
    border-color: var(--accent-danger);
}

.model-content {
    display: flex;
    justify-content: center;
}

.architecture-section {
    background: var(--bg-secondary);
    border: 1px solid var(--border-default);
    border-radius: var(--radius-large);
    overflow: hidden;
    box-shadow: var(--shadow-small);
}

.section-header {
    padding: var(--space-4) var(--space-6);
    border-bottom: 1px solid var(--border-default);
    background: var(--bg-primary);
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: var(--space-4);
}

.section-header h2 {
    margin: 0;
    font-size: 1.3rem;
    font-weight: 600;
    color: var(--text-primary);
}

.section-stats {
    display: flex;
    gap: var(--space-4);
    flex-wrap: wrap;
}

.stat-item {
    color: var(--text-secondary);
    font-size: 0.9rem;
}

.stat-item strong {
    color: var(--text-primary);
}

.architecture-browser {
    background: var(--bg-primary);
    border-radius: var(--radius-medium);
    margin: var(--space-4);
    overflow: hidden;
    border: 1px solid var(--border-default);
}

.browser-header {
    display: flex;
    align-items: center;
    padding: var(--space-3) var(--space-4);
    background: var(--bg-secondary);
    border-bottom: 1px solid var(--border-default);
}

.browser-controls {
    display: flex;
    gap: var(--space-2);
    margin-right: var(--space-4);
}

.control-dot {
    width: 12px;
    height: 12px;
    border-radius: 50%;
}

.control-dot.red { background: #ff5f57; }
.control-dot.yellow { background: #ffbd2e; }
.control-dot.green { background: #28ca42; }

.browser-title {
    font-weight: 600;
    color: var(--text-primary);
    font-size: 0.9rem;
}

.browser-content {
    padding: var(--space-4);
    min-height: 300px;
}

.architecture-tree {
    font-family: 'Courier New', monospace;
    line-height: 1.8;
}

.tree-item {
    display: flex;
    align-items: center;
    gap: var(--space-2);
    padding: var(--space-1) var(--space-2);
    border-radius: var(--radius-small);
    cursor: pointer;
    transition: background 0.2s ease;
}

.tree-item:hover {
    background: var(--bg-secondary);
}

.tree-item.folder {
    font-weight: 600;
    color: var(--accent-primary);
}

.tree-item.file {
    color: var(--text-secondary);
    margin-left: var(--space-4);
}

.folder-icon, .file-icon {
    font-size: 1.1rem;
}

.layer-info {
    margin-left: auto;
    font-size: 0.8rem;
    color: var(--text-secondary);
    font-style: italic;
}

.model-sidebar {
    display: flex;
    flex-direction: column;
    gap: var(--space-4);
    width: 100%;
}

.sidebar-section {
    background: var(--bg-secondary);
    border: 1px solid var(--border-default);
    border-radius: var(--radius-large);
    padding: var(--space-4);
    box-shadow: var(--shadow-small);
}

.sidebar-section h3 {
    margin: 0 0 var(--space-4);
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--text-primary);
    padding-bottom: var(--space-2);
    border-bottom: 1px solid var(--border-default);
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

.info-label {
    font-size: 0.9rem;
    color: var(--text-secondary);
    font-weight: 500;
}

.info-value {
    font-size: 0.9rem;
    color: var(--text-primary);
    font-weight: 600;
    text-align: right;
}

.info-value.status {
    padding: var(--space-1) var(--space-2);
    border-radius: var(--radius-small);
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.info-value.status.trained {
    background: rgba(34, 197, 94, 0.2);
    color: #16a34a;
}

.info-value.status.training {
    background: rgba(251, 191, 36, 0.2);
    color: #d97706;
}

.info-value.status.failed {
    background: rgba(239, 68, 68, 0.2);
    color: #dc2626;
}

.chart-container {
    margin-bottom: var(--space-4);
}

.chart-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: var(--space-2);
}

.chart-title {
    font-size: 0.9rem;
    color: var(--text-secondary);
    font-weight: 500;
}

.chart-value {
    font-size: 0.9rem;
    font-weight: 600;
    color: var(--text-primary);
}

.progress-bar {
    height: 8px;
    background: var(--bg-primary);
    border-radius: var(--radius-small);
    overflow: hidden;
    border: 1px solid var(--border-default);
}

.progress-fill {
    height: 100%;
    border-radius: var(--radius-small);
    transition: width 0.8s ease;
}

.progress-fill.training {
    background: linear-gradient(90deg, var(--accent-primary), var(--accent-secondary));
}

.progress-fill.validation {
    background: linear-gradient(90deg, #22c55e, #16a34a);
}

.progress-fill.loss {
    background: linear-gradient(90deg, #ef4444, #dc2626);
}

.distribution-list {
    display: flex;
    flex-direction: column;
    gap: var(--space-3);
}

.distribution-item {
    display: flex;
    flex-direction: column;
    gap: var(--space-1);
}

.distribution-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.class-name {
    font-size: 0.9rem;
    color: var(--text-primary);
    font-weight: 500;
}

.class-count {
    font-size: 0.8rem;
    color: var(--text-secondary);
}

.distribution-bar {
    height: 6px;
    background: var(--bg-primary);
    border-radius: var(--radius-small);
    overflow: hidden;
    border: 1px solid var(--border-default);
}

.distribution-fill {
    height: 100%;
    border-radius: var(--radius-small);
    transition: width 0.8s ease;
}

.distribution-percentage {
    font-size: 0.8rem;
    color: var(--text-secondary);
    text-align: right;
}

.config-list {
    display: flex;
    flex-direction: column;
    gap: var(--space-2);
}

.config-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: var(--space-2) 0;
}

.config-label {
    font-size: 0.9rem;
    color: var(--text-secondary);
    font-weight: 500;
}

.config-value {
    font-size: 0.9rem;
    color: var(--text-primary);
    font-weight: 600;
    text-align: right;
}

.btn-primary {
    display: inline-block;
    padding: var(--space-3) var(--space-4);
    background: var(--accent-primary);
    color: white;
    text-decoration: none;
    border-radius: var(--radius-medium);
    font-weight: 600;
    transition: all 0.2s ease;
    box-shadow: var(--shadow-small);
}

.btn-primary:hover {
    background: var(--accent-secondary);
    transform: translateY(-1px);
    box-shadow: var(--shadow-medium);
}

/* Previous Versions Styles */
.versions-loading {
    display: flex;
    align-items: center;
    gap: var(--space-2);
    padding: var(--space-4);
    color: var(--text-secondary);
    font-size: 0.9rem;
}

.small-spinner {
    width: 16px;
    height: 16px;
    border: 2px solid var(--border-default);
    border-top: 2px solid var(--accent-primary);
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

.no-versions {
    padding: var(--space-4);
    text-align: center;
}

.no-versions p {
    margin: 0;
    color: var(--text-secondary);
    font-size: 0.9rem;
    font-style: italic;
}

.versions-list {
    display: flex;
    flex-direction: column;
    gap: var(--space-2);
}

.version-item {
    display: flex;
    flex-direction: column;
    gap: var(--space-2);
    padding: var(--space-3);
    background: var(--bg-primary);
    border: 1px solid var(--border-default);
    border-radius: var(--radius-medium);
    cursor: pointer;
    transition: all 0.2s ease;
}

.version-item:hover {
    background: var(--bg-secondary);
    border-color: var(--accent-primary);
    transform: translateY(-1px);
    box-shadow: var(--shadow-small);
}

.version-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.version-number {
    font-weight: 600;
    color: var(--accent-primary);
    font-size: 0.9rem;
}

.version-date {
    font-size: 0.8rem;
    color: var(--text-secondary);
}

.version-details {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.8rem;
}

.version-accuracy {
    color: var(--text-primary);
    font-weight: 500;
}

.version-size {
    color: var(--text-secondary);
}

.version-status {
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    padding: var(--space-1) var(--space-2);
    border-radius: var(--radius-small);
    text-align: center;
    font-weight: 600;
}

.version-status.trained {
    background: rgba(34, 197, 94, 0.2);
    color: #16a34a;
}

.version-status.training {
    background: rgba(251, 191, 36, 0.2);
    color: #d97706;
}

.version-status.failed {
    background: rgba(239, 68, 68, 0.2);
    color: #dc2626;
}

@media (max-width: 1024px) {
    .model-details-container {
        width: 90%;
    }
    
    .model-content {
        flex-direction: column;
        align-items: center;
    }
    
    .model-header {
        flex-direction: column;
        text-align: center;
    }
    
    .model-actions {
        flex-direction: row;
        justify-content: center;
    }
    
    .section-header {
        flex-direction: column;
        align-items: flex-start;
        gap: var(--space-2);
    }
}

@media (max-width: 768px) {
    .model-details-container {
        width: 95%;
        padding: var(--space-4) var(--space-2);
    }
    
    .model-header {
        padding: var(--space-4);
    }
    
    .model-icon {
        width: 60px;
        height: 60px;
    }
    
    .model-icon svg {
        width: 30px;
        height: 30px;
    }
    
    .model-info h1 {
        font-size: 1.5rem;
    }
    
    .metadata-item {
        font-size: 0.8rem;
    }
    
    .action-btn {
        min-width: 100px;
        padding: var(--space-2) var(--space-3);
    }
}
</style>