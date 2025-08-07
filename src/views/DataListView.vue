<template>
    <navigation-bar></navigation-bar>
    <div class="data-list-container">
        <div class="header">
            <h1>Dataset Library</h1>
        </div>

        <!-- Error State -->
        <div v-if="error" class="error">
            <p>{{ error }}</p>
            <button @click="fetchDatasets" class="retry-btn">Retry</button>
        </div>

        <!-- Dataset Grid -->
        <div v-if="!loading && !error" class="datasets-grid">
            <div 
                v-for="dataset in datasets" 
                :key="dataset.id" 
                class="dataset-card"
            >
                <div class="dataset-header">
                    <h3>{{ dataset.name }}</h3>

                </div>
                
                <p class="description">{{ dataset.description }}</p>
                
                <div class="dataset-info">
                    <div class="info-row">
                        <span class="label">Format:</span>
                        <span class="value">{{ dataset.format }}</span>
                    </div>
                    <div class="info-row">
                        <span class="label">Size:</span>
                        <span class="value">{{ dataset.size }}</span>
                    </div>
                    <div class="info-row">
                        <span class="label">Speakers:</span>
                        <span class="value">{{ dataset.speakers }}</span>
                    </div>
                    <div class="info-row">
                        <span class="label">Utterances:</span>
                        <span class="value">{{ dataset.utterances }}</span>
                    </div>
                    <div class="info-row">
                        <span class="label">Training:</span>
                        <span class="value">{{ dataset.usage.training }}</span>
                    </div>
                    <div class="info-row">
                        <span class="label">Test:</span>
                        <span class="value">{{ dataset.usage.test }}</span>
                    </div>
                </div>

                <div class="dataset-actions">
                    <router-link
                            :to="`/dataset/${dataset.id}`"
                            class="btn-primary">
                            View details
                    </router-link>
                    <button class="btn-secondary">Download</button>
                </div>

                <div class="dataset-footer">
                    <small>Upload date: {{ formatDate(dataset.lastUpdated) }}</small>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { onMounted } from 'vue'
import NavigationBar from '@/components/NavigationBar.vue'
import { useDatasets } from '@/composables/useDatasets'

const {
    datasets,
    loading,
    error,
    fetchDatasets,
} = useDatasets()

const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    })
}

onMounted(() => {
    fetchDatasets()
})
</script>

<style scoped>
.data-list-container {
    padding: var(--space-5);
    max-width: 1200px;
    margin: 0 auto;
}

.header {
    text-align: left;
    background-color: transparent;
    height: 100px;
    margin-bottom: var(--space-5);
}

.header h1 {
    margin-left: var(--space-1);
    color: var(--text-primary);
    font-size: 2rem;
    font-weight: 600;
}

.subtitle {
    color: var(--text-secondary);
    font-size: 1.1rem;
}

.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: var(--space-3);
    margin-bottom: var(--space-5);
}

.stat-card {
    background: var(--bg-secondary);
    padding: var(--space-4);
    border-radius: var(--radius-medium);
    text-align: center;
    border: 1px solid var(--border-default);
    box-shadow: var(--shadow-small);
}

.stat-card h3 {
    font-size: 2rem;
    color: var(--accent-secondary);
    margin: 0 0 var(--space-1) 0;
}

.stat-card p {
    color: var(--text-secondary);
    margin: 0;
    font-weight: 500;
}

.loading, .error {
    text-align: center;
    padding: var(--space-5);
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

.datasets-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
    gap: var(--space-4);
}

.dataset-card {
    background: var(--bg-secondary);
    border: 1px solid var(--border-default);
    border-radius: var(--radius-medium);
    padding: var(--space-4);
    box-shadow: var(--shadow-small);
    transition: all 0.2s ease;
}

.dataset-card:hover {
    box-shadow: var(--shadow-medium);
    border-color: var(--border-subtle);
}

.dataset-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: var(--space-3);
    padding-bottom: var(--space-3);
    border-bottom: 1px solid var(--border-default);
}

.dataset-header h3 {
    color: var(--text-primary);
    margin: 0;
    font-size: 1.25rem;
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
    margin-bottom: var(--space-3);
    line-height: 1.6;
}

.dataset-info {
    margin-bottom: var(--space-3);
}

.info-row {
    display: flex;
    justify-content: space-between;
    margin-bottom: var(--space-2);
    padding: var(--space-1) 0;
}

.label {
    font-weight: 600;
    color: var(--text-primary);
    font-size: 0.875rem;
}

.value {
    color: var(--text-secondary);
    font-size: 0.875rem;
}

.languages {
    margin-bottom: var(--space-3);
}

.language-tags {
    display: flex;
    gap: var(--space-1);
    margin-top: var(--space-2);
    flex-wrap: wrap;
}

.language-tag {
    background: var(--bg-tertiary);
    color: var(--accent-secondary);
    padding: var(--space-1) var(--space-2);
    border-radius: var(--radius-small);
    font-size: 0.75rem;
    border: 1px solid var(--border-default);
    font-weight: 500;
}

.usage-stats {
    display: flex;
    gap: var(--space-3);
    margin-bottom: var(--space-3);
    padding: var(--space-3);
    background: var(--bg-tertiary);
    border-radius: var(--radius-small);
    border: 1px solid var(--border-default);
}

.usage-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    flex: 1;
}

.usage-label {
    font-size: 0.75rem;
    color: var(--text-muted);
    margin-bottom: var(--space-1);
    font-weight: 500;
    text-transform: uppercase;
}

.usage-value {
    font-weight: 600;
    color: var(--text-primary);
    font-size: 1.125rem;
}

.dataset-actions {
    display: flex;
    gap: var(--space-2);
    margin-bottom: var(--space-3);
}

.btn-primary, .btn-secondary {
    display: flex; justify-content: center; align-content: center;
    padding: var(--space-2) var(--space-3);
    border: 1px solid transparent;
    border-radius: var(--radius-small);
    cursor: pointer;
    font-weight: 500;
    font-size: 0.875rem;
    transition: all 0.2s ease;
    flex: 1;
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

.dataset-footer {
    border-top: 1px solid var(--border-default);
    padding-top: var(--space-3);
    text-align: center;
}

.dataset-footer small {
    color: var(--text-muted);
    font-size: 0.75rem;
}

a:hover{
    text-decoration: none;
}
</style>