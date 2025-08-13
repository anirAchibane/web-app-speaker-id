<template>
   <navigation-bar></navigation-bar>
   
   <div class="container">

      <h1 class="welcome-title">
               Welcome back, <span class="user-name">{{ user?.firstName || 'User' }}</span>!
      </h1>

      <div class="dashboard-grid">
           <div class="recent-section">
               <div class="card enhanced-card">
                   <div class="card-header">
                       <div class="header-content">
                           <h3 class="card-title">
                               Recent Datasets
                           </h3>
                       </div>
                   </div>
                   <div class="recent-datasets">
                       <div v-if="datasets.length > 0" class="dataset-list"> 
                           <div v-for="dataset in recentDatasets" :key="dataset.id" class="dataset-item">
                            <div class="dataset-icon">
                              <svg width="20" height="20" fill="currentColor" viewBox="0 0 16 16">
                                <path d="M4 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H4zm0 1h8a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1z"/>
                                <path d="M6 4.5a.5.5 0 0 1 .5-.5h3a.5.5 0 0 1 0 1h-3a.5.5 0 0 1-.5-.5zm0 2a.5.5 0 0 1 .5-.5h3a.5.5 0 0 1 0 1h-3a.5.5 0 0 1-.5-.5zm0 2a.5.5 0 0 1 .5-.5h3a.5.5 0 0 1 0 1h-3a.5.5 0 0 1-.5-.5z"/>
                              </svg>
                            </div>
                            <div class="dataset-info">
                              <h5 class="dataset-name">{{ dataset.name }}</h5>
                              <p class="dataset-details">{{ dataset.speakers || 0 }} speakers • {{ dataset.size || 'Unknown size' }}</p>
                            </div>
                            <router-link :to="`/dataset/${dataset.id}`" class="dataset-link">
                               <button class="view-all-btn">View Details</button>
                            </router-link>
                           </div>

                       </div>
                       <div v-else-if="loading" class="loading-state">
                           <div class="loading-spinner"></div>
                           <p>Loading datasets...</p>
                       </div>
                       <div v-else class="empty-state enhanced-empty">
                           <h4>No datasets yet</h4>
                           <p>Start by uploading your first dataset</p>
                           <button class="btn-primary" @click="UploadDataset()">
                               <svg width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                                   <path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4z"/>
                               </svg>
                               Upload Dataset
                           </button>
                       </div>
                   </div>
               </div>

               <div class="card enhanced-card">
                   <div class="card-header">
                       <div class="header-content">
                           <h3 class="card-title">
                              
                               Recent Models
                           </h3>
                       </div>
                   </div>
                   <div class="recent-models">
                       <div v-if="recentModels.length > 0" class="dataset-list">
                        <div v-for="model in recentModels" :key="model.id" class="dataset-item">
                            <div class="dataset-icon">
                              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>
                                <path d="M2 17L12 22L22 17" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>
                                <path d="M2 12L12 17L22 12" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>
                              </svg>
                            </div>
                            <div class="dataset-info">
                              <h5 class="dataset-name">{{ model.name }}</h5>
                              <p class="dataset-details">{{ model.accuracy || 0 }} % • {{ model.size || 'Unknown size' }}</p>
                            </div>
                            <router-link :to="`/model/${model.id}`" class="dataset-link">
                               <button class="view-all-btn">View Details</button>
                            </router-link>
                           </div>
                      </div>
                      <div v-else-if="loadingModels" class="loading-state">
                           <div class="loading-spinner"></div>
                           <p>Loading models...</p>
                       </div>
                       <div v-else class="empty-state enhanced-empty">
                           <h4>No models available</h4>
                           <p>Start by training your first model</p>
                           <button class="btn-secondary" @click="goToModels()">
                               <svg width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                                   <path d="M1 2.828c.885-.37 2.154-.769 3.388-.893 1.33-.134 2.458.063 3.112.752v9.746c-.935-.53-2.12-.603-3.213-.493-1.18.12-2.37.461-3.287.811V2.828zm7.5-.141c.654-.689 1.782-.886 3.112-.752 1.234.124 2.503.523 3.388.893v9.923c-.918-.35-2.107-.692-3.287-.81-1.094-.111-2.278-.039-3.213.492V2.687z"/>
                               </svg>
                               Explore Models
                           </button>
                       </div>
                   </div>
               </div>
           </div>

           <div class="actions-section">
               <div class="card enhanced-card">
                   <div class="card-header">
                       <h3 class="card-title">
                           Quick Actions
                       </h3>
                   </div>
                   <div class="action-buttons">

                       <router-link to="/training" v-if="user && user.admin">
                          <button class="btn-secondary action-btn">
                              <svg width="20" height="20" fill="currentColor" viewBox="0 0 16 16">
                                  <path d="M8.5 2.687c.654-.689 1.782-.886 3.112-.752 1.234.124 2.503.523 3.388.893v9.923c-.918-.35-2.107-.692-3.287-.81-1.094-.111-2.278-.039-3.213.492V2.687zM8 1.783C7.015.936 5.587.81 4.287.94c-1.514.153-3.042.672-3.994 1.105A.5.5 0 0 0 0 2.5v11a.5.5 0 0 0 .707.455c.882-.4 2.303-.881 3.68-1.02 1.409-.142 2.59.087 3.223.877a.5.5 0 0 0 .78 0c.633-.79 1.814-1.019 3.222-.877 1.378.139 2.8.62 3.681 1.02A.5.5 0 0 0 16 13.5v-11a.5.5 0 0 0-.293-.455c-.952-.433-2.48-.952-3.994-1.105C10.413.809 8.985.936 8 1.783z"/>
                              </svg>
                              <div class="btn-content">
                                  <span class="btn-title">Train a Model</span>
                                  <span class="btn-subtitle">Start training with your datasets</span>
                              </div>
                          </button>
                       </router-link>

            
                      <button v-else class="btn-secondary action-btn" @click="requestAdminPrivilege()">
                              <svg width="20" height="20" fill="currentColor" viewBox="0 0 16 16">
                                  <path d="M8 1a2 2 0 0 1 2 2v4H6V3a2 2 0 0 1 2-2zm3 6V3a3 3 0 0 0-6 0v4a2 2 0 0 0-2 2v5a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2z"/>
                              </svg>
                              <div class="btn-content">
                                  <span class="btn-title">Request Admin Access</span>
                                  <span class="btn-subtitle">Access training functionalities</span>
                              </div>
                      </button>

                       
                       <router-link to="/serving">
                          <button class="btn-secondary action-btn">
                              <svg width="20" height="20" fill="currentColor" viewBox="0 0 16 16">
                                  <path d="M6 9a.5.5 0 0 1 .5-.5h3a.5.5 0 0 1 0 1h-3A.5.5 0 0 1 6 9zM3.854 4.146a.5.5 0 1 0-.708.708L4.793 6.5 3.146 8.146a.5.5 0 1 0 .708.708l2-2a.5.5 0 0 0 0-.708l-2-2z"/>
                                  <path d="M2 1a2 2 0 0 0-2 2v10a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V3a2 2 0 0 0-2-2H2zm12 1a1 1 0 0 1 1 1v10a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1V3a1 1 0 0 1 1-1h12z"/>
                              </svg>
                              <div class="btn-content">
                                  <span class="btn-title">Run Inference</span>
                                  <span class="btn-subtitle">Test models with audio samples</span>
                              </div>
                          </button>
                       </router-link>
                       
                       <router-link to="/datasetslibrary">
                          <button class="btn-secondary action-btn">
                              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
                                <path d="M12 6m-8 0a8 3 0 1 0 16 0a8 3 0 1 0 -16 0" />
                                <path d="M4 6v6a8 3 0 0 0 16 0v-6" />
                                <path d="M4 12v6a8 3 0 0 0 16 0v-6" />
                              </svg>
                              <div class="btn-content">
                                  <span class="btn-title">Browse Datasets</span>
                                  <span class="btn-subtitle">Explore available datasets</span>
                              </div>
                          </button>
                       </router-link>
                       
                       <router-link to="/models">
                          <button class="btn-secondary action-btn">
                              <svg width="20" height="20" fill="currentColor" viewBox="0 0 16 16">
                                  <path d="M1 2.828c.885-.37 2.154-.769 3.388-.893 1.33-.134 2.458.063 3.112.752v9.746c-.935-.53-2.12-.603-3.213-.493-1.18.12-2.37.461-3.287.811V2.828zm7.5-.141c.654-.689 1.782-.886 3.112-.752 1.234.124 2.503.523 3.388.893v9.923c-.918-.35-2.107-.692-3.287-.81-1.094-.111-2.278-.039-3.213.492V2.687z"/>
                                  <path d="M14.5 3a.5.5 0 0 0-.5.5v9a.5.5 0 0 0 .5.5h1a.5.5 0 0 0 .5-.5v-9a.5.5 0 0 0-.5-.5h-1zm-13 0a.5.5 0 0 0-.5.5v9a.5.5 0 0 0 .5.5h1a.5.5 0 0 0 .5-.5v-9a.5.5 0 0 0-.5-.5h-1z"/>
                              </svg>
                              <div class="btn-content">
                                  <span class="btn-title">Browse Models</span>
                                  <span class="btn-subtitle">Explore available models</span>
                              </div>
                          </button>
                       </router-link>
                   </div>
               </div>
           </div>
       </div>
   </div>
    
</template>

<script setup>
import NavigationBar from '@/components/NavigationBar.vue';
import { useRouter } from 'vue-router'
import { onMounted, ref, computed } from 'vue';
import { useDatasets } from '@/composables/useDatasets';
import { useModels } from '@/composables/useModels';

const router = useRouter()
const user = ref(null)

// Datasets functionality
const { datasets, loading, error, fetchDatasets } = useDatasets()
const { models, loadingModels, errorModels, fetchModels } = useModels()

if (error) {
  console.log(error)
}
if (errorModels) {
  console.log(errorModels)
}


// Computed property to get at most 3 recent datasets and models
const recentDatasets = computed(() => {
  return datasets.value.slice(0, 3)
})
const recentModels = computed(() => {
  return models.value.slice(0, 3)
})

onMounted(async () => {
  try {
      user.value = JSON.parse(localStorage.getItem('user')) || null
      
      if (!user.value) {
        alert("An error has occured, please login again")
        router.push('/')
        return
      }
      
      // Fetch datasets when component mounts
      await fetchDatasets()
      await fetchModels()
  } catch (error) {
      console.error("Error fetching user:", error)
  }
})

const UploadDataset = () => {
 /* Upload dataset popup + form + validity check */
}

const requestAdminPrivilege = () => {
  if(confirm("An email request will be sent to one of the admins, continue ?")){
      alert("Request sent, you will be notified once it's approved")
      // Send request to access admin

  }
}

const goToModels = () => {
    router.push('/models')
}
</script>

<style scoped>

/* Professional Page Header */
.page-header {
  text-align: center;
  margin-bottom: var(--space-6);
  padding-bottom: var(--space-4);
  border-bottom: 1px solid var(--border-muted);
}

.welcome-title {
  border-bottom: 1px solid var(--border-muted);
  height: 100px; justify-content: center; align-content: center;
  margin-bottom: 30px;
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--text-primary);
  line-height: 1.2;
}

.user-name {
  background: linear-gradient(135deg, var(--accent-secondary) 0%, var(--accent-primary) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.page-subtitle {
  font-size: 1.1rem;
  color: var(--text-secondary);
  font-weight: 400;
  margin: 0;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

/* Dashboard Grid */
.dashboard-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: var(--space-5);
  margin-bottom: var(--space-6);
}

.recent-section {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.actions-section {
  display: flex;
  flex-direction: column;
}

/* Professional Cards */
.enhanced-card {
  border: 1px solid var(--border-default);
  border-radius: var(--radius-large);
  background: var(--bg-secondary);
  transition: all 0.2s ease;
  overflow: hidden;
  box-shadow: var(--shadow-small);
}

.enhanced-card:hover {
  border-color: var(--border-muted);
  box-shadow: var(--shadow-medium);
}

.card-header {
  padding: var(--space-4) var(--space-5);
  border-bottom: 2px solid var(--border-muted);
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.card-title {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.card-title svg {
  color: var(--accent-secondary);
  flex-shrink: 0;
}

.view-all-btn {
  background: none;
  border: 1px solid var(--border-default);
  color: var(--text-secondary);
  padding: var(--space-1) var(--space-2);
  border-radius: var(--radius-small);
  font-size: 0.8rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.view-all-btn:hover {
  background-color: var(--bg-overlay);
  color: var(--text-primary);
  border-color: var(--accent-secondary);
}

/* Enhanced Empty State */
.enhanced-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--space-6) var(--space-4);
  text-align: center;
}

.enhanced-empty .empty-icon {
  color: var(--text-disabled);
  margin-bottom: var(--space-3);
  opacity: 0.6;
}

.enhanced-empty h4 {
  color: var(--text-primary);
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: var(--space-2);
}

.enhanced-empty p {
  color: var(--text-muted);
  margin-bottom: var(--space-4);
  max-width: 280px;
}

/* Dataset List Styles */
.dataset-list {
  padding: var(--space-3);
}

.dataset-item {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3);
  border-radius: var(--radius-medium);
  border: 1px solid transparent;
  transition: all 0.2s ease;
  cursor: pointer;
}

.dataset-item:hover {
  background-color: var(--bg-tertiary);
  border-color: var(--border-muted);
}

.dataset-item:not(:last-child) {
  border-bottom: 1px solid var(--border-muted);
  margin-bottom: var(--space-2);
  padding-bottom: var(--space-3);
}

.dataset-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background-color: rgba(47, 129, 247, 0.1);
  border-radius: var(--radius-medium);
  flex-shrink: 0;
}

.dataset-icon svg {
  color: var(--accent-secondary);
}

.dataset-info {
  flex: 1;
  min-width: 0;
}

.dataset-name {
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 var(--space-1) 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.dataset-details {
  font-size: 0.875rem;
  color: var(--text-secondary);
  margin: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.dataset-status {
  flex-shrink: 0;
}

.status-badge {
  display: inline-block;
  padding: var(--space-1) var(--space-2);
  border-radius: var(--radius-small);
  font-size: 0.75rem;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.status-ready {
  background-color: rgba(35, 134, 54, 0.1);
  color: var(--accent-primary);
  border: 1px solid rgba(35, 134, 54, 0.3);
}

.status-processing {
  background-color: rgba(209, 153, 34, 0.1);
  color: var(--accent-warning);
  border: 1px solid rgba(209, 153, 34, 0.3);
}

.status-error {
  background-color: rgba(218, 54, 51, 0.1);
  color: var(--accent-danger);
  border: 1px solid rgba(218, 54, 51, 0.3);
}

/* Loading State */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--space-6) var(--space-4);
  text-align: center;
}

.loading-spinner {
  width: 32px;
  height: 32px;
  border: 3px solid var(--border-muted);
  border-top: 3px solid var(--accent-secondary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: var(--space-3);
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-state p {
  color: var(--text-secondary);
  margin: 0;
}

/* Simplified Action Buttons */
.action-buttons {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: var(--space-3);
  padding: var(--space-4);
}

.action-btn {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-4);
  text-align: left;
  background-color: var(--bg-tertiary);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-medium);
  transition: all 0.2s ease;
  cursor: pointer;
  font-family: var(--font-family-sans);
  text-decoration: none;
  min-height: 120px;
  min-width: 250px;
  width: 100%;
  height: 120px;
}

.action-btn:hover {
  background-color: var(--bg-overlay);
  border-color: var(--accent-secondary);
  transform: translateY(-1px);
  box-shadow: var(--shadow-small);
}

.action-btn svg {
  flex-shrink: 0;
  color: var(--accent-secondary);
  transition: color 0.2s ease;
}


.btn-content {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
  flex: 1;
}

.btn-title {
  font-weight: 600;
  font-size: 1rem;
  color: var(--text-primary);
  transition: color 0.2s ease;
}

.btn-subtitle {
  font-size: 0.875rem;
  color: var(--text-secondary);
  font-weight: 400;
  transition: color 0.2s ease;
}

.action-btn:hover .btn-subtitle {
  color: var(--text-muted);
}

/* Remove underline from router-link */
a {
  text-decoration: none;
}

a:hover {
  text-decoration: none;
}

/* Responsive design */
@media (max-width: 968px) {
  .dashboard-grid {
    grid-template-columns: 1fr;
    gap: var(--space-4);
  }
}

@media (max-width: 768px) {
  .page-header {
    margin-bottom: var(--space-4);
    padding-bottom: var(--space-3);
  }
  
  .welcome-title {
    font-size: 2rem;
  }
  
  .page-subtitle {
    font-size: 1rem;
  }
  
  .action-btn {
    padding: var(--space-3);
    gap: var(--space-2);
  }
  
  .btn-title {
    font-size: 0.9rem;
  }
  
  .btn-subtitle {
    font-size: 0.8rem;
  }
  
  /* Dataset responsive styles */
  .dataset-item {
    padding: var(--space-2);
    gap: var(--space-2);
  }
  
  .dataset-icon {
    width: 36px;
    height: 36px;
  }
  
  .dataset-name {
    font-size: 0.9rem;
  }
  
  .dataset-details {
    font-size: 0.8rem;
  }
}

@media (max-width: 480px) {
  .welcome-title {
    font-size: 1.75rem;
  }
  
  .page-subtitle {
    font-size: 0.9rem;
  }
  
  .dashboard-grid {
    gap: var(--space-3);
  }
  
  .recent-section {
    gap: var(--space-3);
  }
  
  .action-buttons {
    grid-template-columns: 1fr;
    gap: var(--space-2);
    padding: var(--space-3);
  }
  
  .action-btn {
    padding: var(--space-3);
    gap: var(--space-2);
    min-height: 100px;
    height: 150px;
    min-width: auto;
  }
  
  .btn-subtitle {
    display: none;
  }
  
  /* Dataset mobile styles */
  .dataset-list {
    padding: var(--space-2);
  }
  
  .dataset-item {
    padding: var(--space-2);
    gap: var(--space-2);
    flex-direction: row;
  }
  
  .dataset-icon {
    width: 32px;
    height: 32px;
  }
  
  .dataset-details {
    font-size: 0.75rem;
  }
  
  .status-badge {
    font-size: 0.7rem;
    padding: 2px 6px;
  }
}
</style>

