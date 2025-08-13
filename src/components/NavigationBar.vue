<template>
    <nav class="navbar">
        <div class="navbar-container">
            
            <div class="navbar-nav">
                <router-link to="/dashboard" class="nav-item">
                    <svg width="16" height="16" fill="currentColor" viewBox="0 0 16 16" class="nav-icon">
                        <path d="M8 4a.5.5 0 0 1 .5.5V6a.5.5 0 0 1-1 0V4.5A.5.5 0 0 1 8 4zM3.732 5.732a.5.5 0 0 1 .707 0l.915.914a.5.5 0 1 1-.708.708l-.914-.915a.5.5 0 0 1 0-.707zM2 10a.5.5 0 0 1 .5-.5h1.586a.5.5 0 0 1 0 1H2.5A.5.5 0 0 1 2 10zm9.5 0a.5.5 0 0 1 .5-.5h1.5a.5.5 0 0 1 0 1H12a.5.5 0 0 1-.5-.5zm.754-4.246a.389.389 0 0 0-.527-.02L7.547 9.31a.91.91 0 1 0 1.302 1.258l3.434-4.297a.389.389 0 0 0-.029-.518z"/>
                        <path fill-rule="evenodd" d="M0 10a8 8 0 1 1 15.547 2.661c-.442 1.253-1.845 1.602-2.932 1.25C11.309 13.488 9.475 13 8 13c-1.474 0-3.31.488-4.615.911-1.087.352-2.49.003-2.932-1.25A7.988 7.988 0 0 1 0 10zm8-7a7 7 0 0 0-6.603 9.329c.203.575.923.876 1.68.63C4.312 12.533 6.974 12 8 12s3.688.533 4.923.959c.757.245 1.477-.056 1.68-.63A7 7 0 0 0 8 3z"/>
                    </svg>
                    <span>Dashboard</span>
                </router-link>
                
                <router-link to="/training" class="nav-item" v-if="user && user.admin">
                    <svg width="16" height="16" fill="currentColor" viewBox="0 0 16 16" class="nav-icon">
                        <path d="M8.5 2.687c.654-.689 1.782-.886 3.112-.752 1.234.124 2.503.523 3.388.893v9.923c-.918-.35-2.107-.692-3.287-.81-1.094-.111-2.278-.039-3.213.492V2.687zM8 1.783C7.015.936 5.587.81 4.287.94c-1.514.153-3.042.672-3.994 1.105A.5.5 0 0 0 0 2.5v11a.5.5 0 0 0 .707.455c.882-.4 2.303-.881 3.68-1.02 1.409-.142 2.59.087 3.223.877a.5.5 0 0 0 .78 0c.633-.79 1.814-1.019 3.222-.877 1.378.139 2.8.62 3.681 1.02A.5.5 0 0 0 16 13.5v-11a.5.5 0 0 0-.293-.455c-.952-.433-2.48-.952-3.994-1.105C10.413.809 8.985.936 8 1.783z"/>
                    </svg>
                    <span>Training</span>
                </router-link>
                
                <router-link to="/serving" class="nav-item">
                    <svg width="16" height="16" fill="currentColor" viewBox="0 0 16 16" class="nav-icon">
                        <path d="M6 9a.5.5 0 0 1 .5-.5h3a.5.5 0 0 1 0 1h-3A.5.5 0 0 1 6 9zM3.854 4.146a.5.5 0 1 0-.708.708L4.793 6.5 3.146 8.146a.5.5 0 1 0 .708.708l2-2a.5.5 0 0 0 0-.708l-2-2z"/>
                        <path d="M2 1a2 2 0 0 0-2 2v10a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V3a2 2 0 0 0-2-2H2zm12 1a1 1 0 0 1 1 1v10a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1V3a1 1 0 0 1 1-1h12z"/>
                    </svg>
                    <span>Serving</span>
                </router-link>

                <router-link to="/users" class="nav-item" v-if="user && user.admin">
                    <svg width="16" height="16" fill="currentColor" viewBox="0 0 16 16" class="nav-icon">
                        <path d="M7 14s-1 0-1-1 1-4 5-4 5 3 5 4-1 1-1 1H7Zm4-6a3 3 0 1 0 0-6 3 3 0 0 0 0 6Zm-5.784 6A2.238 2.238 0 0 1 5 13c0-1.355.68-2.75 1.936-3.72A6.325 6.325 0 0 0 5 9c-4 0-5 3-5 4s1 1 1 1h4.216ZM4.5 8a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5Z"/>
                    </svg>
                    <span>Users</span>
                </router-link>
            </div>
            
            <div class="navbar-actions">
                <router-link to="/profile" class="nav-item profile-link">
                    <svg width="16" height="16" fill="currentColor" viewBox="0 0 16 16" class="nav-icon">
                        <path d="M8 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm2-3a2 2 0 1 1-4 0 2 2 0 0 1 4 0zm4 8c0 1-1 1-1 1H3s-1 0-1-1 1-4 6-4 6 3 6 4zm-1-.004c-.001-.246-.154-.986-.832-1.664C11.516 10.68 10.289 10 8 10c-2.29 0-3.516.68-4.168 1.332-.678.678-.83 1.418-.832 1.664h10z"/>
                    </svg>
                    <span>Profile</span>
                </router-link>
                
                <button class="nav-item logout-btn" @click="logout()">
                    <svg width="16" height="16" fill="currentColor" viewBox="0 0 16 16" class="nav-icon">
                        <path fill-rule="evenodd" d="M10 12.5a.5.5 0 0 1-.5.5h-8a.5.5 0 0 1-.5-.5v-9a.5.5 0 0 1 .5-.5h8a.5.5 0 0 1 .5.5v2a.5.5 0 0 0 1 0v-2A1.5 1.5 0 0 0 9.5 2h-8A1.5 1.5 0 0 0 0 3.5v9A1.5 1.5 0 0 0 1.5 14h8a1.5 1.5 0 0 0 1.5-1.5v-2a.5.5 0 0 0-1 0v2z"/>
                        <path fill-rule="evenodd" d="M15.854 8.354a.5.5 0 0 0 0-.708l-3-3a.5.5 0 0 0-.708.708L14.293 7.5H5.5a.5.5 0 0 0 0 1h8.793l-2.147 2.146a.5.5 0 0 0 .708.708l3-3z"/>
                    </svg>
                    <span>Logout</span>
                </button>
            </div>
        </div>
    </nav>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { onMounted, ref } from 'vue'
const router = useRouter()

const user = ref()

onMounted( async () => {
    try{
      user.value = JSON.parse(localStorage.getItem('user')) || null
      if (!user.value) {
        // If no user is found, redirect to the home page
        router.push('/')
      }
    } catch (error) {
        console.error("Error fetching user data:", error)
        alert("An error has occurred, please login again")
        router.push('/')
    }

    
})

const logout = () => {
    router.push("/")
}
</script>

<style scoped>
/* Navigation Bar Styles */
.navbar {
  background-color: var(--bg-secondary);
  border-bottom: 1px solid var(--border-default);
  position: sticky;
  top: 0;
  z-index: 100;
  backdrop-filter: blur(10px);
}

.navbar-container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 var(--space-4);
  height: 64px;
}

.navbar-brand .brand-link {
  color: var(--text-primary);
  text-decoration: none;
  font-weight: 600;
}

.navbar-brand .brand-link:hover {
  color: var(--text-primary);
  text-decoration: none;
}

.navbar-brand h3 {
  margin: 0;
  font-size: 1.25rem;
  color: var(--text-primary);
}

.navbar-nav {
  display: flex;
  align-items: center;
  gap: var(--space-1);
}

.navbar-actions {
  display: flex;
  align-items: center;
  gap: var(--space-1);
}

.nav-item {
  display: flex;
  align-items: center;
  gap: var(--space-1);
  padding: var(--space-2) var(--space-3);
  border-radius: var(--radius-small);
  color: var(--text-secondary);
  text-decoration: none;
  font-weight: 500;
  font-size: 0.875rem;
  transition: all 0.2s ease;
  border: none;
  background: none;
  cursor: pointer;
  font-family: var(--font-family-sans);
}

.nav-item:hover {
  background-color: var(--bg-tertiary);
  color: var(--text-primary);
  text-decoration: none;
}

.nav-item.router-link-exact-active {
  background-color: var(--bg-tertiary);
  color: var(--text-primary);
}

.nav-icon {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
}

.profile-link {
  position: relative;
}

.logout-btn {
  color: var(--text-secondary);
  border: 1px solid var(--border-default);
}

.logout-btn:hover {
  background-color: var(--accent-danger);
  color: var(--text-primary);
  border-color: var(--accent-danger);
}

/* Mobile responsiveness */
@media (max-width: 768px) {
  .navbar-container {
    padding: 0 var(--space-3);
    height: 56px;
  }
  
  .navbar-brand h3 {
    font-size: 1rem;
  }
  
  .navbar-nav {
    gap: 0;
  }
  
  .navbar-actions {
    gap: 0;
  }
  
  .nav-item {
    padding: var(--space-2);
  }
  
  .nav-item span {
    display: none;
  }
  
  .nav-icon {
    width: 18px;
    height: 18px;
  }
}

@media (max-width: 480px) {
  .navbar-brand h3 {
    font-size: 0.9rem;
  }
  
  .navbar-nav .nav-item:not(.router-link-exact-active) {
    display: none;
  }
}
</style>