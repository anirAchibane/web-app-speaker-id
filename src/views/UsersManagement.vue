<template>
    <navigation-bar></navigation-bar>
    <div class="container">
        <!-- Professional Header Section -->
        <div class="page-header">
            <div class="header-content">
                <h1 class="page-title">User Management</h1>
                <p class="page-subtitle">Manage all registered users.</p>
            </div>
                <button class="btn-primary" @click="$router.push('/addUser')">
                    <svg width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                        <path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4z"/>
                    </svg>
                    Add User
                </button>
        </div>

        <!-- Loading State -->
        <div v-if="!users.length && !error" class="loading-state">
            <div class="loading-spinner"></div>
            <p>Loading users...</p>
        </div>

        <!-- Error State -->
        <div v-else-if="error" class="error-state">
            <div class="error-icon">
                <svg width="48" height="48" fill="currentColor" viewBox="0 0 16 16">
                    <path d="M8.982 1.566a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767L8.982 1.566zM8 5c.535 0 .954.462.9.995l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 5.995A.905.905 0 0 1 8 5zm.002 6a1 1 0 1 1 0 2 1 1 0 0 1 0-2z"/>
                </svg>
            </div>
            <h3>Error Loading Users</h3>
            <p>{{ error }}</p>
        </div>

        <!-- Users Table -->
        <div v-else class="users-section">
            <div class="card users-table-card">
                <div class="card-header">
                    <h3 class="card-title">All Users ({{ users.length }})</h3>
                </div>
                <div class="table-container">
                    <table class="users-table">
                        <thead>
                            <tr>
                                <th>First Name</th>
                                <th>Last Name</th>
                                <th>Email</th>
                                <th>Role</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="tableUser in users" :key="tableUser.email" class="user-row">
                                <td class="user-firstname">{{ tableUser.firstName }}</td>
                                <td class="user-lastname">{{ tableUser.lastName }}</td>
                                <td class="user-email">{{ tableUser.email }}</td>
                                <td class="user-role-cell">
                                    <span v-if="tableUser.admin" class="role-badge admin">Admin</span>
                                    <span v-else class="role-badge user">User</span>
                                </td>
                                <td class="user-actions">
                                    <div class="action-buttons" v-if="user && user.email !== tableUser.email">
                                        <button v-if="!tableUser.admin"
                                            class="btn-action btn-role" 
                                            @click="MakeAdmin(tableUser)"
                                            :title="'Make Admin'"
                                        >
                                            <svg width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                                                <path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/>
                                                <path d="M1.38 8.28a.5.5 0 0 1 0-.566l6.717-6.717a.5.5 0 0 1 .566 0l6.717 6.717a.5.5 0 0 1 0 .566l-6.717 6.717a.5.5 0 0 1-.566 0L1.38 8.28ZM2.5 8l6-6 6 6-6 6-6-6Z"/>
                                            </svg>
                                            {{ "Make Admin" }}
                                        </button>
                                        <button v-else 
                                            class="btn-action btn-role" 
                                            @click="RemoveAdmin(tableUser)"
                                            :title="'Remove Admin Role'"
                                        >
                                            <svg width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                                                <path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/>
                                                <path d="M1.38 8.28a.5.5 0 0 1 0-.566l6.717-6.717a.5.5 0 0 1 .566 0l6.717 6.717a.5.5 0 0 1 0 .566l-6.717 6.717a.5.5 0 0 1-.566 0L1.38 8.28ZM2.5 8l6-6 6 6-6 6-6-6Z"/>
                                            </svg>
                                            {{ "Remove Admin" }}
                                        </button>
                                        <button 
                                            class="btn-action btn-delete" 
                                            @click="deleteUser(tableUser)"
                                            title="Delete User"
                                        >
                                            <svg width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                                                <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5Zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5Zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6Z"/>
                                                <path d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1ZM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118ZM2.5 3h11V2h-11v1Z"/>
                                            </svg>
                                            Delete
                                        </button>
                                    </div>
                                    <span v-else class="current-user-indicator">You</span>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</template>


<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import NavigationBar from '@/components/NavigationBar.vue';

const user = ref(null)
const users = ref([])
const error = ref(null)
const API_BASE = 'http://localhost:8000'
const router = useRouter()

onMounted(async () => {
    try{
        const userData = localStorage.getItem('user')
        if (userData) {
            user.value = JSON.parse(userData)
            if (!user.value.admin){
                router.push("/")
            }
        } else {
            // No user data, redirect to login
            router.push('/')
        }
    } catch (error){
        console.error('Error fetching user data:', error)
        user.value = null
    }

    try {
        const response = await fetch(`${API_BASE}/auth/users`)
        if (!response.ok) throw new Error('Failed to fetch users')
        const data = await response.json()
        users.value = data.users || []
    } catch (err) {
        console.error('Error fetching users:', err)
        error.value = 'Failed to load users. Please try again later.'
        users.value = []
    }
})

// Toggle user role between admin and regular user
const MakeAdmin = async (targetUser) => {
    try {
        const response = await fetch(`${API_BASE}/auth/make-admin/${targetUser.email}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        
        if (!response.ok) throw new Error('Failed to update user role')
        
        // Update the user in the local array
        const userIndex = users.value.findIndex(u => u.email === targetUser.email)
        if (userIndex !== -1) {
            users.value[userIndex].admin = !users.value[userIndex].admin
        }
    } catch (err) {
        console.error('Error updating user role:', err)
        alert('Failed to update user role. Please try again.')
    }
}

const RemoveAdmin = async (targetUser) => {
    try {
        const response = await fetch(`${API_BASE}/auth/remove-admin/${targetUser.email}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        
        if (!response.ok) throw new Error('Failed to update user role')
        
        // Update the user in the local array
        const userIndex = users.value.findIndex(u => u.email === targetUser.email)
        if (userIndex !== -1) {
            users.value[userIndex].admin = !users.value[userIndex].admin
        }
    } catch (err) {
        console.error('Error updating user role:', err)
        alert('Failed to update user role. Please try again.')
    }
}


// Delete user
const deleteUser = async (targetUser) => {
    if (!confirm(`Are you sure you want to delete user "${targetUser.firstName} ${targetUser.lastName}"? This action cannot be undone.`)) {
        return
    }
    
    try {
        const response = await fetch(`${API_BASE}/auth/delete-user/${targetUser.email}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        
        if (!response.ok) throw new Error('Failed to delete user')
        
        // Remove the user from the local array
        users.value = users.value.filter(u => u.email !== targetUser.email)
    } catch (err) {
        console.error('Error deleting user:', err)
        alert('Failed to delete user. Please try again.')
    }
}
</script>

<style scoped>
/* Page Header */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: var(--space-5);
  margin-bottom: var(--space-5);
  padding-bottom: var(--space-4);
  border-bottom: 1px solid var(--border-default);
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
  color: var(--text-secondary);
  font-size: 1rem;
  margin-top: var(--space-1);
  margin-bottom: 0;
}

/* Loading State */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--space-6);
  text-align: center;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid var(--border-default);
  border-top: 3px solid var(--accent-secondary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: var(--space-3);
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Error State */
.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--space-6);
  text-align: center;
}

.error-icon {
  color: var(--accent-danger);
  margin-bottom: var(--space-3);
}

.error-state h3 {
  color: var(--text-primary);
  margin-bottom: var(--space-2);
}

.error-state p {
  color: var(--text-secondary);
}

/* Users Table */
.users-section {
  margin-top: var(--space-4);
}

.table-container {
  overflow-x: auto;
  border-radius: var(--radius-medium);
}

.users-table {
  width: 100%;
  border-collapse: collapse;
  background-color: var(--bg-secondary);
  font-size: 0.95rem;
}

.users-table thead th {
  background-color: var(--bg-tertiary);
  color: var(--text-primary);
  font-weight: 600;
  padding: var(--space-4);
  text-align: left;
  border-bottom: 2px solid var(--border-default);
  font-size: 0.875rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.users-table tbody td {
  padding: var(--space-4);
  border-bottom: 1px solid var(--border-default);
  vertical-align: middle;
}

.user-row {
  transition: background-color 0.2s ease;
}

.user-row:hover {
  background-color: var(--bg-tertiary);
}

.user-row:last-child td {
  border-bottom: none;
}

.user-avatar-cell {
  width: 60px;
  text-align: center;
}

.user-avatar {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 44px;
  height: 44px;
  background-color: var(--bg-overlay);
  border-radius: 50%;
  margin: 0 auto;
  color: var(--text-secondary);
  border: 2px solid var(--border-default);
}

.user-firstname,
.user-lastname {
  font-weight: 600;
  color: var(--text-primary);
  font-size: 0.95rem;
  min-width: 120px;
}

.user-email {
  color: var(--text-secondary);
  font-family: var(--font-family-mono);
  font-size: 0.875rem;
  min-width: 200px;
}

.user-role-cell {
  min-width: 100px;
}

.role-badge {
  display: inline-block;
  padding: var(--space-1) var(--space-3);
  border-radius: var(--radius-small);
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.role-badge.admin {
  background-color: rgba(35, 134, 54, 0.15);
  color: var(--accent-primary);
  border: 1px solid rgba(35, 134, 54, 0.3);
}

.role-badge.user {
  background-color: rgba(47, 129, 247, 0.15);
  color: var(--accent-secondary);
  border: 1px solid rgba(47, 129, 247, 0.3);
}

.user-actions {
  min-width: 200px;
  text-align: right;
}

.action-buttons {
  display: flex;
  gap: var(--space-2);
  justify-content: flex-end;
}

.btn-action {
  display: inline-flex;
  align-items: center;
  gap: var(--space-1);
  padding: var(--space-2) var(--space-3);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-small);
  background-color: var(--bg-tertiary);
  color: var(--text-secondary);
  font-size: 0.8rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  text-decoration: none;
}

.btn-action:hover {
  background-color: var(--bg-overlay);
  color: var(--text-primary);
  border-color: var(--border-muted);
}

.btn-action svg {
  width: 14px;
  height: 14px;
}

.btn-role {
  color: var(--accent-secondary);
  border-color: rgba(47, 129, 247, 0.3);
}

.btn-role:hover {
  background-color: rgba(47, 129, 247, 0.1);
  color: var(--accent-secondary);
  border-color: var(--accent-secondary);
}

.btn-delete {
  color: var(--accent-danger);
  border-color: rgba(218, 54, 51, 0.3);
}

.btn-delete:hover {
  background-color: rgba(218, 54, 51, 0.1);
  color: var(--accent-danger);
  border-color: var(--accent-danger);
}

.current-user-indicator {
  color: var(--text-secondary);
  font-style: italic;
  font-size: 0.875rem;
  text-align: center;
  display: block;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .btn-action {
    width: 32px;
    height: 32px;
  }
  
  .btn-action svg {
    width: 12px;
    height: 12px;
  }
}

@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--space-3);
  }
  
  .users-table-card {
    min-height: auto;
  }
  
  .table-container {
    overflow-x: scroll;
  }
  
  .users-table {
    min-width: 700px;
    font-size: 0.875rem;
  }
  
  .users-table thead th,
  .users-table tbody td {
    padding: var(--space-2) var(--space-3);
  }
  
  .user-avatar {
    width: 36px;
    height: 36px;
  }
  
  .user-firstname,
  .user-lastname {
    min-width: 100px;
    font-size: 0.875rem;
  }
  
  .user-email {
    min-width: 180px;
    font-size: 0.8rem;
  }
  
  .user-actions {
    min-width: 100px;
  }
  
  .btn-action {
    width: 28px;
    height: 28px;
  }
  
  .btn-action svg {
    width: 11px;
    height: 11px;
  }
}

@media (max-width: 480px) {
  .users-table {
    min-width: 600px;
  }
  
  .users-table thead th,
  .users-table tbody td {
    padding: var(--space-1) var(--space-2);
  }
  
  .user-actions {
    min-width: 80px;
  }
  
  .action-buttons {
    gap: var(--space-1);
  }
  
  .btn-action {
    width: 24px;
    height: 24px;
  }
  
  .btn-action svg {
    width: 10px;
    height: 10px;
  }
}
</style>