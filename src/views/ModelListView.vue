<template>
    <navigation-bar></navigation-bar>
    <div class="data-list-container">
        <!-- Professional Header Section -->
        <div class="page-header">
            <div class="header-content">
                <h1 class="page-title">Model Library</h1>
                <p class="page-subtitle">Explore available trained models.</p>
            </div>
            <div class="header-actions">
                <button class="btn-primary" @click="$router.push('/training')">
                    <svg width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                        <path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4z"/>
                    </svg>
                    Train Model
                </button>
            </div>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="loading-state">
            <div class="loading-spinner"></div>
            <p>Loading models...</p>
        </div>

        <!-- Error State -->
        <div v-else-if="error" class="error-state">
            <div class="error-icon">
                <svg width="48" height="48" fill="currentColor" viewBox="0 0 16 16">
                    <path d="M8.982 1.566a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767L8.982 1.566zM8 5c.535 0 .954.462.9.995l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 5.995A.905.905 0 0 1 8 5zm.002 6a1 1 0 1 1 0 2 1 1 0 0 1 0-2z"/>
                </svg>
            </div>
            <h3>Failed to load models</h3>
            <p>{{ error }}</p>
            <button @click="fetchModels" class="btn-primary retry-btn">
                <svg width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                    <path fill-rule="evenodd" d="M8 3a5 5 0 1 0 4.546 2.914.5.5 0 0 1 .908-.417A6 6 0 1 1 8 2v1z"/>
                    <path d="M8 4.466V.534a.25.25 0 0 1 .41-.192l2.36 1.966c.12.1.12.284 0 .384L8.41 4.658A.25.25 0 0 1 8 4.466z"/>
                </svg>
                Retry
            </button>
        </div>

        <!-- Empty State -->
        <div v-else-if="!models || !models.length" class="empty-state">
            <div class="empty-icon">
                <svg width="64" height="64" fill="currentColor" viewBox="0 0 16 16">
                    <path d="M8 4.754a3.246 3.246 0 1 0 0 6.492 3.246 3.246 0 0 0 0-6.492zM5.754 8a2.246 2.246 0 1 1 4.492 0 2.246 2.246 0 0 1-4.492 0z"/>
                    <path d="M9.796 1.343c-.527-1.79-3.065-1.79-3.592 0l-.094.319a.873.873 0 0 1-1.255.52l-.292-.16c-1.64-.892-3.433.902-2.54 2.541l.159.292a.873.873 0 0 1-.52 1.255l-.319.094c-1.79.527-1.79 3.065 0 3.592l.319.094a.873.873 0 0 1 .52 1.255l-.16.292c-.892 1.64.901 3.434 2.541 2.54l.292-.159a.873.873 0 0 1 1.255.52l.094.319c.527 1.79 3.065 1.79 3.592 0l.094-.319a.873.873 0 0 1 1.255-.52l.292.16c1.64.893 3.434-.902 2.54-2.541l-.159-.292a.873.873 0 0 1 .52-1.255l.319-.094c1.79-.527 1.79-3.065 0-3.592l-.319-.094a.873.873 0 0 1-.52-1.255l.16-.292c.893-1.64-.902-3.433-2.541-2.54l-.292.159a.873.873 0 0 1-1.255-.52l-.094-.319z"/>
                </svg>
            </div>
            <h3>No models found</h3>
            <p>Start by training your first model to begin building your collection</p>
            <button class="btn-primary" @click="$router.push('/training')">
                <svg width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                    <path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4z"/>
                </svg>
                Train Model
            </button>
        </div>

        <!-- Model Grid -->
        <div v-else class="datasets-section">
            <div class="section-header">
                <div class="filters-container">
                    <!-- Search Bar -->
                    <div class="search-container">
                        <input 
                            type="text" 
                            v-model="searchQuery"
                            placeholder="Search by name or architecture..."
                            class="search-input"
                        />
                    </div>
                </div>

                <span class="dataset-count">{{ filteredModels.length }} model{{ filteredModels.length !== 1 ? 's' : '' }}</span>
            </div>
            
            <!-- Show models grid when there are filtered results -->
            <div v-if="filteredModels.length > 0" class="datasets-grid">
                <div 
                    v-for="model in filteredModels" 
                    :key="model.id" 
                    class="dataset-card professional-card clickable-card"
                >
                    <router-link :to="`/model/${model.id}`">
                    <div class="card-header">
                        <div class="dataset-icon">
                        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>
                            <path d="M2 17L12 22L22 17" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>
                            <path d="M2 12L12 17L22 12" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>
                        </svg>
                        </div>
                        <h3 class="dataset-title">{{ model.name }}</h3>
                    </div>
                    
                    <div class="dataset-content">
                        <p class="dataset-description">{{ model.description || 'AI model for speaker identification and analysis' }}</p>
                        
                        <div class="dataset-info">
                            <div class="info-item">
                                <span class="info-label">Architecture</span>
                                <span class="info-value">{{ model.architecture || 'N/A' }}</span>
                            </div>
                            <div class="info-item">
                                <span class="info-label">Accuracy</span>
                                <span class="info-value">{{ model.accuracy || 'N/A' }}%</span>
                            </div>
                            <div class="info-item">
                                <span class="info-label">Version</span>
                                <span class="info-value">{{ model.version || 'N/A' }}</span>
                            </div>
                        </div>
                    </div>
                    </router-link>
                </div>
            </div>

            <!-- Show no results state when filters applied but no matches -->
            <div v-else class="no-results-state">
                <div class="empty-icon">
                    <svg width="64" height="64" fill="currentColor" viewBox="0 0 16 16">
                        <path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001c.03.04.062.078.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1.007 1.007 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0z"/>
                    </svg>
                </div>
                <h3>No models match your filters</h3>
                <p>Try adjusting your search terms or filters to find models</p>
                <button class="btn-secondary" @click="searchQuery = ''">
                    Clear Filters
                </button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { onMounted, ref, computed } from 'vue'
import NavigationBar from '@/components/NavigationBar.vue'
import { useModels } from '@/composables/useModels'

const { models, loading, error, fetchModels } = useModels()

// Filter reactive variables
const searchQuery = ref('')

// Computed property for filtered models
const filteredModels = computed(() => {
    if (!models.value) return []
    
    let filtered = [...models.value]
    
    // Search filter
    if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase()
        filtered = filtered.filter(model => 
            model.name?.toLowerCase().includes(query) ||
            model.architecture?.toLowerCase().includes(query)
        )
    }
    
    return filtered
})

onMounted(() => {
    fetchModels()
})
</script>

<style scoped>
/* Container and Layout */
.dataset-card a{
    text-decoration: none;
    color: inherit;
}
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
.no-results-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: var(--space-6) var(--space-4);
    text-align: center;
}

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

/* Models Section */
.section-header {
    display: flex; 
    flex-direction: row;
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
    display: flex; 
    flex-direction: row;
    align-items: center;
    gap: var(--space-4);
}

.search-input {
    width: 250px;
    padding: var(--space-2) var(--space-3);
    border: 1px solid var(--border-default);
    border-radius: var(--radius-medium);
    font-size: 0.9rem;
    background: var(--bg-tertiary);
    color: var(--text-primary);
    transition: all 0.2s ease;
}

.search-input:focus {
    outline: none;
    border-color: var(--accent-secondary);
    box-shadow: 0 0 0 2px rgba(47, 129, 247, 0.1);
}

.filter-select {
    padding: var(--space-2) var(--space-3);
    border: 1px solid var(--border-default);
    border-radius: var(--radius-medium);
    font-size: 0.9rem;
    background: var(--bg-tertiary);
    color: var(--text-primary);
    cursor: pointer;
    transition: all 0.2s ease;
}

.filter-select:focus {
    outline: none;
    border-color: var(--accent-secondary);
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

/* Model Grid */
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

/* Model Info */
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

/* Button Styles */
.btn-secondary {
    background: var(--bg-tertiary);
    color: var(--text-primary);
    border: 1px solid var(--border-default);
    padding: var(--space-2) var(--space-4);
    border-radius: var(--radius-medium);
    cursor: pointer;
    font-size: 0.9rem;
    font-weight: 500;
    transition: all 0.2s ease;
}

.btn-secondary:hover {
    background: var(--bg-overlay);
    border-color: var(--accent-secondary);
    transform: translateY(-1px);
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
    
    .filters-container {
        flex-direction: column;
        align-items: stretch;
        gap: var(--space-2);
    }
    
    .search-input {
        width: 100%;
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
