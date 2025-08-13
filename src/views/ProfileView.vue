<template>
    <navigation-bar></navigation-bar>

    <div class="profile-grid">
            <div class="user_info">
                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title">Profile Information</h3>
                    </div>
                    <div v-if="user" class="user-form">
                        <form @submit.prevent="saveProfile">
                            <div class="form-group">
                                <label>First Name</label>
                                <input 
                                    type="text" 
                                    v-model="editForm.firstName" 
                                    placeholder="Enter your first name" 
                                    required
                                    :disabled="isSaving"
                                >
                            </div>
                            <div class="form-group">
                                <label>Last Name</label>
                                <input 
                                    type="text" 
                                    v-model="editForm.lastName" 
                                    placeholder="Enter your last name" 
                                    required
                                    :disabled="isSaving"
                                >
                            </div>
                            <div class="form-group">
                                <label>Email</label>
                                <input 
                                    type="email" 
                                    v-model="editForm.email" 
                                    placeholder="Enter your email" 
                                    required
                                    :disabled="isSaving"
                                >
                            </div>
                            <div class="form-group">
                                <label>Account Type</label>
                                <div class="account-type-display">
                                    <span v-if="user.admin" class="admin-badge">Administrator</span>
                                    <span v-else class="user-badge">Regular User</span>
                                </div>
                            </div>
                            <div class="form-group">
                                <button 
                                    type="submit" 
                                    class="btn-primary save-btn"
                                    :disabled="isSaving"
                                >
                                    <span v-if="isSaving" class="loading"></span>
                                    {{ isSaving ? 'Saving...' : 'Save Changes' }}
                                </button>
                            </div>
                        </form>
                    </div>
                    <div v-else class="empty-state">
                        <p>No user information available</p>
                        <button class="btn-primary" @click="goToLogin">Login</button>
                    </div>
                </div>
            </div>

            <div class="user_actions">
                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title">Account Actions</h3>
                    </div>
                    <div class="action-list">
                        <button class="action-item" @click="viewActivity">
                            <svg width="20" height="20" fill="currentColor" viewBox="0 0 16 16">
                                <path fill-rule="evenodd" d="M1 14s-1 0-1-1 1-4 6-4 6 3 6 4-1 1-1 1H1zm5-6a3 3 0 1 0 0-6 3 3 0 0 0 0 6z"/>
                            </svg>
                            <div class="action-content">
                                <span class="action-title">Activity Log</span>
                                <span class="action-subtitle">View your recent activity</span>
                            </div>
                        </button>

                        <button class="action-item danger" @click="deleteAccount">
                            <svg width="20" height="20" fill="currentColor" viewBox="0 0 16 16">
                                <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z"/>
                                <path fill-rule="evenodd" d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z"/>
                            </svg>
                            <div class="action-content">
                                <span class="action-title">Delete Account</span>
                                <span class="action-subtitle">Permanently delete your account</span>
                            </div>
                        </button>

                    </div>
                </div>
            </div>
    </div>
</template>


<script setup>
import NavigationBar from '@/components/NavigationBar.vue';
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const user = ref(null)
const editForm = ref({
    firstName: '',
    lastName: '',
    email: ''
})
const isSaving = ref(false)

// API base URL
const API_BASE = 'http://localhost:8000'

onMounted(() => {
    try {
        const userData = localStorage.getItem('user')
        if (userData) {
            user.value = JSON.parse(userData)
            // Initialize edit form with current user data
            editForm.value = {
                firstName: user.value.firstName,
                lastName: user.value.lastName,
                email: user.value.email
            }
        } else {
            // No user data, redirect to login
            router.push('/')
        }
    } catch (error) {
        console.error('Error loading user data:', error)
        router.push('/')
    }
})

const saveProfile = async () => {
    isSaving.value = true
    
    try {
        const response = await fetch(`${API_BASE}/auth/update-profile`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                currentEmail: user.value.email,
                ...editForm.value
            })
        })

        const data = await response.json()

        if (response.ok) {
            // Update user data in localStorage
            const updatedUser = { ...user.value, ...editForm.value }
            localStorage.setItem('user', JSON.stringify(updatedUser))
            user.value = updatedUser
            alert('Profile updated successfully!')
        } else {
            alert(data.detail || 'Failed to update profile')
        }
    } catch (error) {
        alert('Network error. Please try again.')
        console.error('Update profile error:', error)
    } finally {
        isSaving.value = false
    }
}

const deleteAccount = async () => {
    const confirmDelete = confirm(
        'Are you sure you want to delete your account? This action cannot be undone and all your data will be permanently deleted.'
    )
    
    if (confirmDelete) {
        try {
            const response = await fetch(`${API_BASE}/auth/delete-account`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    email: user.value.email
                })
            })

            const data = await response.json()

            if (response.ok) {
                alert('Account deleted successfully.')
                user.value = null
                localStorage.removeItem('user')
                router.push('/')
            } else {
                alert(data.detail || 'Failed to delete account')
            }
        } catch (error) {
            alert('Network error. Please try again.')
            console.error('Delete account error:', error)
        }
    }
}

const viewActivity = () => {
    //Implement activity log functionality
    alert('Activity log functionality coming soon!')
}

const goToLogin = () => {
    router.push('/')
}
</script>

<style scoped>
/* Profile-specific styles */
.profile-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: var(--space-5);
  margin-top: var(--space-6);
  width: 70%;
  justify-self: center; align-self: center;
}

.user-details {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}

.detail-item label {
  font-weight: 600;
  color: var(--text-secondary);
  font-size: 0.875rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.detail-item p {
  font-size: 1rem;
  color: var(--text-primary);
  margin: 0;
  padding: var(--space-2) 0;
  border-bottom: 1px solid var(--border-muted);
}

.admin-badge {
  background-color: var(--accent-primary);
  color: var(--text-primary);
  padding: var(--space-1) var(--space-2);
  border-radius: var(--radius-small);
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.user-badge {
  background-color: var(--bg-tertiary);
  color: var(--text-secondary);
  padding: var(--space-1) var(--space-2);
  border-radius: var(--radius-small);
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.action-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.action-item {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3);
  background-color: var(--bg-tertiary);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-medium);
  cursor: pointer;
  transition: all 0.2s ease;
  text-align: left;
  font-family: var(--font-family-sans);
}

.action-item:hover {
  border-color: var(--accent-secondary);
  box-shadow: 0 0 0 1px var(--accent-secondary);
}

.action-item.danger:hover {
  border-color: var(--accent-danger);
  box-shadow: 0 0 0 1px var(--accent-danger);
}

.action-item svg {
  flex-shrink: 0;
  color: var(--accent-secondary);
}

.action-item.danger svg {
  color: var(--accent-danger);
}

.action-content {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}

.action-title {
  font-weight: 600;
  color: var(--text-primary);
  font-size: 0.9rem;
}

.action-subtitle {
  font-size: 0.8rem;
  color: var(--text-muted);
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

.empty-state p {
  margin-bottom: var(--space-3);
  color: var(--text-muted);
}

/* Responsive design */
@media (max-width: 968px) {
  .profile-grid {
    grid-template-columns: 1fr;
    gap: var(--space-4);
  }
}

@media (max-width: 768px) {
  .action-item {
    padding: var(--space-2);
    gap: var(--space-2);
  }
  
  .action-title {
    font-size: 0.85rem;
  }
  
  .action-subtitle {
    font-size: 0.75rem;
  }
}

@media (max-width: 480px) {
  .profile-grid {
    gap: var(--space-3);
  }
  
  .user-details {
    gap: var(--space-3);
  }
  
  .action-list {
    gap: var(--space-1);
  }
  
  .action-subtitle {
    display: none;
  }
}

.form-group{
    margin-top: var(--space-3);
}
</style>
