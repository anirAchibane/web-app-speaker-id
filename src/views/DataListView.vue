<template>
    <navigation-bar></navigation-bar>
    <div class="data-list-container">
        <!-- Professional Header Section -->
        <div class="page-header">
            <div class="header-content">
                <h1 class="page-title">Dataset Library</h1>
                <p class="page-subtitle">Explore available audio datasets.</p>
            </div>
            <div class="header-actions">
                <button class="btn-primary" @click="$router.push('/upload')">
                    <svg width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                        <path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4z"/>
                    </svg>
                    Upload Dataset
                </button>
            </div>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="loading-state">
            <div class="loading-spinner"></div>
            <p>Loading datasets...</p>
        </div>

        <!-- Error State -->
        <div v-else-if="error" class="error-state">
            <div class="error-icon">
                <svg width="48" height="48" fill="currentColor" viewBox="0 0 16 16">
                    <path d="M8.982 1.566a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767L8.982 1.566zM8 5c.535 0 .954.462.9.995l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 5.995A.905.905 0 0 1 8 5zm.002 6a1 1 0 1 1 0 2 1 1 0 0 1 0-2z"/>
                </svg>
            </div>
            <h3>Failed to load datasets</h3>
            <p>{{ error }}</p>
            <button @click="fetchDatasets" class="btn-primary retry-btn">
                <svg width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                    <path fill-rule="evenodd" d="M8 3a5 5 0 1 0 4.546 2.914.5.5 0 0 1 .908-.417A6 6 0 1 1 8 2v1z"/>
                    <path d="M8 4.466V.534a.25.25 0 0 1 .41-.192l2.36 1.966c.12.1.12.284 0 .384L8.41 4.658A.25.25 0 0 1 8 4.466z"/>
                </svg>
                Retry
            </button>
        </div>

        <!-- Empty State -->
        <div v-else-if="!datasets || !datasets.length" class="empty-state">
            <div class="empty-icon">
                <svg width="64" height="64" fill="currentColor" viewBox="0 0 16 16">
                    <path d="M4 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H4zm0 1h8a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1z"/>
                    <path d="M6 4.5a.5.5 0 0 1 .5-.5h3a.5.5 0 0 1 0 1h-3a.5.5 0 0 1-.5-.5zm0 2a.5.5 0 0 1 .5-.5h3a.5.5 0 0 1 0 1h-3a.5.5 0 0 1-.5-.5zm0 2a.5.5 0 0 1 .5-.5h3a.5.5 0 0 1 0 1h-3a.5.5 0 0 1-.5-.5z"/>
                </svg>
            </div>
            <h3>No datasets found</h3>
            <p>Start by uploading your first dataset to begin building your collection</p>
            <button class="btn-primary" @click="$router.push('/upload')">
                <svg width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                    <path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4z"/>
                </svg>
                Upload Dataset
            </button>
        </div>

        <!-- Dataset Grid -->
        <div v-else class="datasets-section">
            <div class="section-header">
                <div class="filters-container">
                    <!-- Search Bar -->
                    <div class="search-container">
                        <input 
                            type="text" 
                            v-model="searchQuery"
                            placeholder="Search datasets..."
                            class="search-input"
                        />
                    </div>

                    <!-- Format Filter -->
                    <div class="filter-container">
                        <select v-model="formatFilter" class="filter-select">
                            <option value="">All Formats</option>
                            <option value="WAV">WAV</option>
                            <option value="MP3">MP3</option>
                            <option value="FLAC">FLAC</option>
                            <option value="M4A">M4A</option>
                        </select>
                    </div>

                    <!-- Size Filter -->
                    <div class="filter-container">
                        <select v-model="sizeFilter" class="filter-select">
                            <option value="">All Sizes</option>
                            <option value="small">Small (&lt; 100MB)</option>
                            <option value="medium">Medium (100MB - 1GB)</option>
                            <option value="large">Large (> 1GB)</option>
                        </select>
                    </div>
                </div>

                <span class="dataset-count">{{ filteredDatasets.length }} dataset{{ filteredDatasets.length !== 1 ? 's' : '' }}</span>
            </div>
            
            <!-- Show datasets grid when there are filtered results -->
            <div v-if="filteredDatasets.length > 0" class="datasets-grid">
                <router-link 
                    v-for="dataset in filteredDatasets" 
                    :key="dataset.id" 
                    :to="`/dataset/${dataset.id}`"
                    class="dataset-card professional-card clickable-card"
                >
                    <div class="card-header">
                        <div class="dataset-icon">
                            <svg width="24" height="24" fill="currentColor" viewBox="0 0 16 16">
                                <path d="M4 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H4zm0 1h8a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1z"/>
                                <path d="M6 4.5a.5.5 0 0 1 .5-.5h3a.5.5 0 0 1 0 1h-3a.5.5 0 0 1-.5-.5zm0 2a.5.5 0 0 1 .5-.5h3a.5.5 0 0 1 0 1h-3a.5.5 0 0 1-.5-.5zm0 2a.5.5 0 0 1 .5-.5h3a.5.5 0 0 1 0 1h-3a.5.5 0 0 1-.5-.5z"/>
                            </svg>
                        </div>
                        <h3 class="dataset-title">{{ dataset.name }}</h3>
                    </div>
                    
                    <div class="dataset-content">
                        <p class="dataset-description">{{ dataset.description || 'Audio dataset for speaker identification training and evaluation' }}</p>
                        
                        <div class="dataset-info">
                            <div class="info-item">
                                <span class="info-label">Size</span>
                                <span class="info-value">{{ dataset.size || 'N/A' }}</span>
                            </div>
                            <div class="info-item">
                                <span class="info-label">Format</span>
                                <span class="info-value">{{ dataset.format || 'WAV' }}</span>
                            </div>
                            <div class="info-item">
                                <span class="info-label">Utterances</span>
                                <span class="info-value">{{ dataset.utterances || 'N/A' }}</span>
                            </div>
                        </div>
                    </div>
                </router-link>
            </div>

            <!-- Show no results state when filters applied but no matches -->
            <div v-else class="no-results-state">
                <div class="empty-icon">
                    <svg width="64" height="64" fill="currentColor" viewBox="0 0 16 16">
                        <path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001c.03.04.062.078.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1.007 1.007 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0z"/>
                    </svg>
                </div>
                <h3>No datasets match your filters</h3>
                <p>Try adjusting your search terms or filters to find datasets</p>
                <button class="btn-secondary" @click="searchQuery = ''; formatFilter = ''; sizeFilter = ''">
                    Clear Filters
                </button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { onMounted, ref, computed } from 'vue'
import NavigationBar from '@/components/NavigationBar.vue'
import { useDatasets } from '@/composables/useDatasets'

const {
    datasets,
    loading,
    error,
    fetchDatasets,
} = useDatasets()

// Filter reactive variables
const searchQuery = ref('')
const formatFilter = ref('')
const sizeFilter = ref('')

// Computed property for filtered datasets
const filteredDatasets = computed(() => {
    if (!datasets.value) return []
    
    let filtered = [...datasets.value]
    
    // Search filter
    if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase()
        filtered = filtered.filter(dataset => 
            dataset.name?.toLowerCase().includes(query) ||
            dataset.description?.toLowerCase().includes(query)
        )
    }
    
    // Format filter
    if (formatFilter.value) {
        filtered = filtered.filter(dataset => 
            dataset.format === formatFilter.value
        )
    }
    
    // Size filter
    if (sizeFilter.value) {
        filtered = filtered.filter(dataset => {
            const size = dataset.size || ''
            switch (sizeFilter.value) {
                case 'small':
                    return size.includes('MB') && parseInt(size) < 100
                case 'medium':
                    return (size.includes('MB') && parseInt(size) >= 100) || 
                           (size.includes('GB') && parseInt(size) <= 1)
                case 'large':
                    return size.includes('GB') && parseInt(size) > 1
                default:
                    return true
            }
        })
    }
    
    return filtered
})

onMounted(() => {
    fetchDatasets()
})
</script>

<style scoped>
/* Container and Layout */
.data-list-container {
    width: 75%;
    margin: 0 auto;
    padding: var(--space-lg) var(--space-md);
    min-height: calc(100vh - 80px);
}

/* Professional Page Header */
.page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: var(--space-6);
    padding: var(--space-5) 0;
    border-bottom: 1px solid var(--border-muted);
}

.header-content h1.page-title {
    font-size: 2.5rem;
    font-weight: 700;
    color: var(--text-primary);
    margin: 0 0 var(--space-2) 0;
    background: linear-gradient(135deg, var(--accent-secondary) 0%, var(--accent-primary) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.page-subtitle {
    font-size: 1.1rem;
    color: var(--text-secondary);
    margin: 0;
    font-weight: 400;
}

.header-actions .btn-primary {
    display: flex;
    align-items: center;
    gap: var(--space-2);
    padding: var(--space-3) var(--space-4);
    background: var(--accent-primary);
    color: var(--text-primary);
    border: none;
    border-radius: var(--radius-medium);
    font-weight: 600;
    font-size: 0.9rem;
    cursor: pointer;
    transition: all 0.2s ease;
    box-shadow: var(--shadow-small);
}

.header-actions .btn-primary:hover {
    background: #2ea043;
    transform: translateY(-1px);
    box-shadow: var(--shadow-medium);
}

/* Loading State */
.loading-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: var(--space-8) var(--space-4);
    text-align: center;
}

.loading-spinner {
    width: 40px;
    height: 40px;
    border: 3px solid var(--border-muted);
    border-top: 3px solid var(--accent-secondary);
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-bottom: var(--space-4);
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

.loading-state p {
    color: var(--text-secondary);
    font-size: 1.1rem;
    margin: 0;
}

/* Error State */
.error-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: var(--space-8) var(--space-4);
    text-align: center;
    background: var(--bg-secondary);
    border: 1px solid var(--border-default);
    border-radius: var(--radius-large);
    border-left: 4px solid var(--accent-danger);
}

.error-icon {
    color: var(--accent-danger);
    margin-bottom: var(--space-4);
    opacity: 0.8;
}

.error-state h3 {
    color: var(--text-primary);
    font-size: 1.25rem;
    font-weight: 600;
    margin: 0 0 var(--space-2) 0;
}

.error-state p {
    color: var(--text-secondary);
    margin: 0 0 var(--space-4) 0;
    max-width: 400px;
}

.retry-btn {
    display: flex;
    align-items: center;
    gap: var(--space-2);
    background: var(--accent-primary);
    color: var(--text-primary);
    border: none;
    padding: var(--space-3) var(--space-4);
    border-radius: var(--radius-medium);
    cursor: pointer;
    font-weight: 600;
    transition: all 0.2s ease;
}

.retry-btn:hover {
    background: #2ea043;
    box-shadow: var(--shadow-small);
}

/* Empty State */
.empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: var(--space-8) var(--space-4);
    text-align: center;
    background: var(--bg-secondary);
    border: 1px solid var(--border-default);
    border-radius: var(--radius-large);
}

.empty-icon {
    color: var(--text-disabled);
    margin-bottom: var(--space-4);
    opacity: 0.6;
}

.empty-state h3 {
    color: var(--text-primary);
    font-size: 1.25rem;
    font-weight: 600;
    margin: 0 0 var(--space-2) 0;
}

.empty-state p {
    color: var(--text-secondary);
    margin: 0 0 var(--space-4) 0;
    max-width: 400px;
}

/* No Results State (when filters applied but no matches) */


.no-results-state .empty-icon {
    color: var(--text-disabled);
    margin-bottom: var(--space-3);
    opacity: 0.5;
}

.no-results-state h3 {
    color: var(--text-primary);
    font-size: 1.1rem;
    font-weight: 600;
    margin: 0 0 var(--space-2) 0;
}

.no-results-state p {
    color: var(--text-secondary);
    margin: 0 0 var(--space-4) 0;
    max-width: 350px;
    font-size: 0.9rem;
}

/* Datasets Section */

.section-header {
    display: flex; flex-direction: row;
    justify-content: space-between;
    align-items: center;
    margin-bottom: var(--space-5);
}

.section-header h2 {
    font-size: 1.5rem;
    font-weight: 600;
    color: var(--text-primary);
    margin: 0;
}

.filters-container, .search-container {
    display: flex; flex-direction: row;
    align-items: center;
    gap: var(--space-4);
}

.dataset-count {
    color: var(--text-secondary);
    font-size: 0.9rem;
    font-weight: 500;
    padding: var(--space-1) var(--space-3);
    background: var(--bg-tertiary);
    border: 1px solid var(--border-default);
    border-radius: var(--radius-large);
}

/* Dataset Grid */
.datasets-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    max-width: 100%;
    gap: var(--space-4);
}

@media (min-width: 1400px) {
    .datasets-grid {
        grid-template-columns: repeat(5, 1fr);
    }
}

@media (min-width: 1200px) and (max-width: 1399px) {
    .datasets-grid {
        grid-template-columns: repeat(4, 1fr);
    }
}

@media (min-width: 900px) and (max-width: 1199px) {
    .datasets-grid {
        grid-template-columns: repeat(3, 1fr);
    }
}

@media (min-width: 600px) and (max-width: 899px) {
    .datasets-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

/* Professional Card Design */
.dataset-card.professional-card {
    background: var(--bg-secondary);
    border: 1px solid var(--border-default);
    border-radius: var(--radius-large);
    padding: 0;
    box-shadow: var(--shadow-small);
    transition: all 0.3s ease;
    overflow: hidden;
    position: relative;
    display: block;
    text-decoration: none;
    color: inherit;
}

.dataset-card.professional-card.clickable-card {
    cursor: pointer;
}

.dataset-card.professional-card:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-large);
    border-color: var(--accent-secondary);
    text-decoration: none;
}

.card-header {
    display: flex;
    align-items: center;
    gap: var(--space-2);
    padding: var(--space-3) var(--space-4);
    border-bottom: 1px solid var(--border-muted);
    position: relative;
}

.dataset-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 36px;
    height: 36px;
    background: linear-gradient(135deg, var(--accent-secondary), var(--accent-primary));
    border-radius: var(--radius-medium);
    color: white;
    flex-shrink: 0;
}

.dataset-icon svg {
    width: 18px;
    height: 18px;
}

.dataset-title {
    flex: 1;
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--text-primary);
    margin: 0;
    line-height: 1.3;
}

.dataset-content {
    padding: var(--space-3) var(--space-4);
}

.dataset-description {
    color: var(--text-secondary);
    line-height: 1.5;
    height: 100px;
    margin: 0 0 var(--space-3) 0;
    font-size: 0.85rem;
}

/* Dataset Info */
.dataset-info {
    display: flex;
    flex-direction: column;
    gap: var(--space-2);
}

.info-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: var(--space-1) 0;
}

.info-label {
    font-size: 0.8rem;
    color: var(--text-secondary);
    font-weight: 500;
}

.info-value {
    font-size: 0.8rem;
    color: var(--text-primary);
    font-weight: 600;
}

/* Card Footer */
.card-footer {
    padding: var(--space-2) var(--space-4);
    border-top: 1px solid var(--border-muted);
    background: var(--bg-tertiary);
}

.upload-date {
    display: flex;
    align-items: center;
    gap: var(--space-1);
    color: var(--text-muted);
    font-size: 0.7rem;
    font-weight: 500;
}

.upload-date svg {
    width: 10px;
    height: 10px;
}

/* Responsive Design */
@media (max-width: 768px) {
    .data-list-container {
        padding: var(--space-4) var(--space-3);
    }
    
    .page-header {
        flex-direction: column;
        align-items: flex-start;
        gap: var(--space-4);
    }
    
    .header-content h1.page-title {
        font-size: 2rem;
    }
    
    .datasets-grid {
        grid-template-columns: 1fr;
        gap: var(--space-3);
    }
}

@media (max-width: 480px) {
    .card-header {
        padding: var(--space-2) var(--space-3);
    }
    
    .dataset-content,
    .card-footer {
        padding-left: var(--space-3);
        padding-right: var(--space-3);
    }
    
    .dataset-icon {
        width: 32px;
        height: 32px;
    }
    
    .dataset-icon svg {
        width: 16px;
        height: 16px;
    }
    
    .dataset-title {
        font-size: 1rem;
    }
    
    .info-label,
    .info-value {
        font-size: 0.75rem;
    }
}
</style>