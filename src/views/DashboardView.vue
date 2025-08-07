<template>
   <navigation-bar></navigation-bar>
   
   <div class="container">

       <div class="dashboard-grid">
           <div class="recent-section">
               <div class="card">
                   <div class="card-header">
                       <h3 class="card-title">Recent Datasets</h3>
                   </div>
                   <div class="recent-datasets">
                       <div v-if="false" class="list">
                           <!-- Dataset list will go here -->
                       </div>
                       <div v-else class="empty-state">
                           <p>No dataset uploaded yet...</p>
                           <button class="btn-secondary" @click="UploadDataset()">Upload Dataset</button>
                       </div>
                   </div>
               </div>

               <div class="card">
                   <div class="card-header">
                       <h3 class="card-title">Recent Models</h3>
                   </div>
                   <div class="recent-models">
                       <div v-if="false">
                           <!-- Model list will go here -->
                       </div>
                       <div v-else class="empty-state">
                           <p>No model available yet...</p>
                           <button class="btn-secondary" @click="goToModels()">View Models</button>
                       </div>
                   </div>
               </div>
           </div>

           <div class="actions-section">
               <div class="card">
                   <div class="card-header">
                       <h3 class="card-title">Quick Actions</h3>
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
                                  <path d="M8.5 2.687c.654-.689 1.782-.886 3.112-.752 1.234.124 2.503.523 3.388.893v9.923c-.918-.35-2.107-.692-3.287-.81-1.094-.111-2.278-.039-3.213.492V2.687zM8 1.783C7.015.936 5.587.81 4.287.94c-1.514.153-3.042.672-3.994 1.105A.5.5 0 0 0 0 2.5v11a.5.5 0 0 0 .707.455c.882-.4 2.303-.881 3.68-1.02 1.409-.142 2.59.087 3.223.877a.5.5 0 0 0 .78 0c.633-.79 1.814-1.019 3.222-.877 1.378.139 2.8.62 3.681 1.02A.5.5 0 0 0 16 13.5v-11a.5.5 0 0 0-.293-.455c-.952-.433-2.48-.952-3.994-1.105C10.413.809 8.985.936 8 1.783z"/>
                              </svg>
                              <div class="btn-content">
                                  <span class="btn-title">Request admin privilege</span>
                                  <span class="btn-subtitle">Access training functionalities</span>
                              </div>
                      </button>

                       
                       <router-link to="/serving">
                          <button class="btn-secondary action-btn">
                              <svg width="20" height="20" fill="currentColor" viewBox="0 0 16 16">
                                  <path d="M6 9a.5.5 0 0 1 .5-.5h3a.5.5 0 0 1 0 1h-3A.5.5 0 0 1 6 9zM3.854 4.146a.5.5 0 1 0-.708.708L4.793 6.5 3.146 8.146a.5.5 0 1 0 .708.708l2-2a.5.5 0 0 0 0-.708l-2-2z"/>
                                  <path d="M2 1a2 2 0 0 0-2 2v10a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V3a2 2 0 0 0-2-2H2zm12 1a1 1 0 0 1 1 1v10a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1V3a1 1 0 0 1 1-1h12z"/>
                              </svg>
                              <div class=" btn-content">
                                  <span class="btn-title">Run Inference</span>
                                  <span class="btn-subtitle">Test models with audio samples</span>
                              </div>
                          </button>
                       </router-link>
                       
                       <router-link to="/datasetslibrary">
                          <button class="btn-secondary action-btn">
                              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
                                <path d="M12 6m-8 0a8 3 0 1 0 16 0a8 3 0 1 0 -16 0" />
                                <path d="M4 6v6a8 3 0 0 0 16 0v-6" />
                                <path d="M4 12v6a8 3 0 0 0 16 0v-6" />
                              </svg>
                              <div class="btn-content">
                                  <span class="btn-title">Datasets list</span>
                                  <span class="btn-subtitle">Check list of available datasets</span>
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
import { onMounted, ref} from 'vue';

const user = ref(null)

onMounted( ()=> {
  try {
      user.value = JSON.parse(localStorage.getItem('user')) || null
      
      if (!user.value) {
        alert("An error has occured, please login again")
      
        router.push('/')
      }
  } catch (error) {
      console.error("Error fetching user:", error)
  }

})
const router = useRouter()

const UploadDataset = () => {
 /* Upload dataset popup + form + validity check */
}

const requestAdminPrivilege = () => {
  /* Send request to access admin */
}

const goToModels = () => {
    router.push('/models')
}
</script>

<style scoped>
/* Dashboard-specific styles */
.dashboard-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: var(--space-5);
  margin-bottom: var(--space-6);
  margin-top: var(--space-6)
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

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--space-6) var(--space-4);
  text-align: center;
  color: var(--text-muted);
}

.empty-icon {
  color: var(--text-disabled);
  margin-bottom: var(--space-3);
  opacity: 0.6;
}

.empty-state p {
  margin-bottom: var(--space-3);
  color: var(--text-muted);
}

.action-buttons {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: var(--space-3);
}

.action-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-3);
  padding: var(--space-4);
  text-align: left;
  background-color: var(--bg-tertiary);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-medium);
  transition: all 0.2s ease;
  cursor: pointer;
  font-family: var(--font-family-sans);
}

.action-btn:hover {
  box-shadow: 0 0 0 1px var(--accent-secondary);
}

/* Remove underline from router-link */
a {
  text-decoration: none;
}

a:hover {
  text-decoration: none;
}

.btn-content {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}

.btn-title {
  font-weight: 600;
  font-size: 1rem;
  color: var(--text-primary);
}

.btn-subtitle {
  font-size: 0.875rem;
  color: var(--text-secondary);
  font-weight: 400;
}

.action-btn svg {
  flex-shrink: 0;
  color: var(--accent-secondary);
}

.btn-primary.action-btn svg {
  color: var(--text-primary);
}

.btn-secondary.action-btn svg {
  color: var(--text-secondary);
}

/* Responsive design */
@media (max-width: 968px) {
  .dashboard-grid {
    grid-template-columns: 1fr;
    gap: var(--space-4);
  }
}

@media (max-width: 768px) {
  .action-btn {
    padding: var(--space-3);
  }
  
  .btn-title {
    font-size: 0.9rem;
  }
  
  .btn-subtitle {
    font-size: 0.8rem;
  }
  
  .action-btn svg {
    width: 18px;
    height: 18px;
  }
}

@media (max-width: 480px) {
  .dashboard-grid {
    gap: var(--space-3);
  }
  
  .recent-section {
    gap: var(--space-3);
  }
  
  .action-buttons {
    gap: var(--space-2);
  }
  
  .action-btn {
    padding: var(--space-3);
    gap: var(--space-2);
  }
  
  .btn-subtitle {
    display: none;
  }
}
</style>

