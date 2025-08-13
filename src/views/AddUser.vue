<template>
    <navigation-bar></navigation-bar>
    <div class="container">
        <!-- Professional Header Section -->
        <div class="page-header">
            <div class="header-content">
                <h1 class="page-title">Add New User</h1>
                <p class="page-subtitle">Create a new user account for the platform.</p>
            </div>
        </div>

        <!-- Add User Form -->
        <div class="form-section">
            <div class="card form-card">
                <div class="card-header">
                    <h3 class="card-title">User Information</h3>
                </div>
                
                <form @submit.prevent="createUser" class="user-form">
                    <div class="form-columns">
                        <!-- Column 1: Name Fields -->
                        <div class="form-column">
                            <div class="form-group">
                                <label for="firstName">First Name</label>
                                <input 
                                    id="firstName"
                                    type="text" 
                                    v-model="userForm.firstName" 
                                    placeholder="Enter first name" 
                                    required
                                    :disabled="isLoading"
                                    class="form-input"
                                >
                            </div>

                            <div class="form-group">
                                <label for="lastName">Last Name</label>
                                <input 
                                    id="lastName"
                                    type="text" 
                                    v-model="userForm.lastName" 
                                    placeholder="Enter last name" 
                                    required
                                    :disabled="isLoading"
                                    class="form-input"
                                >
                            </div>
                        </div>

                        <!-- Column 2: Credentials -->
                        <div class="form-column">
                            <div class="form-group">
                                <label for="email">Email Address</label>
                                <input 
                                    id="email"
                                    type="email" 
                                    v-model="userForm.email" 
                                    placeholder="Enter email address" 
                                    required
                                    :disabled="isLoading"
                                    class="form-input"
                                >
                            </div>

                            <div class="form-group">
                                <label for="password">Password</label>
                                <input 
                                    id="password"
                                    type="password" 
                                    v-model="userForm.password" 
                                    placeholder="Enter password" 
                                    required
                                    :disabled="isLoading"
                                    class="form-input"
                                    minlength="6"
                                >
                            </div>
                        </div>

                        <!-- Column 3: Privileges & Actions -->
                        <div class="form-column">
                            <div class="form-group checkbox-group">
                                <label class="checkbox-label">
                                    <input 
                                        type="checkbox" 
                                        v-model="userForm.isAdmin" 
                                        :disabled="isLoading"
                                        class="form-checkbox"
                                    >
                                    <span class="checkbox-text">Grant Admin Privileges</span>
                                </label>
                                <p class="checkbox-description">Admin users can manage other users and access administrative features.</p>
                            </div>

                            <div class="form-group">
                                <button 
                                    type="submit" 
                                    :disabled="isLoading || !isFormValid"
                                    class="btn-primary btn-full"
                                >
                                    <span v-if="isLoading" class="loading"></span>
                                    <span v-else>Create User</span>
                                </button>
                            </div>
                        </div>
                    </div>

                    <!-- Error Message -->
                    <div v-if="errorMessage" class="alert alert-error">
                        {{ errorMessage }}
                    </div>

                    <!-- Success Message -->
                    <div v-if="successMessage" class="alert alert-success">
                        {{ successMessage }}
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import NavigationBar from '@/components/NavigationBar.vue';

const router = useRouter()
const user = ref(null)
const isLoading = ref(false)
const errorMessage = ref('')
const successMessage = ref('')

const API_BASE = 'http://localhost:8000'

// Form data
const userForm = ref({
    firstName: '',
    lastName: '',
    email: '',
    password: '',
    isAdmin: false
})

// Check if current user is admin
onMounted(() => {
    try {
        const userData = localStorage.getItem('user')
        if (userData) {
            user.value = JSON.parse(userData)
            if (!user.value.admin) {
                // Redirect non-admin users
                router.push('/')
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

// Form validation
const isFormValid = computed(() => {
    return userForm.value.firstName.trim() !== '' &&
           userForm.value.lastName.trim() !== '' &&
           userForm.value.email.trim() !== '' &&
           userForm.value.password.length >= 6
})


// Create user
const createUser = async () => {
    errorMessage.value = ''
    successMessage.value = ''
    
    if (!isFormValid.value) {
        errorMessage.value = 'Please fill in all fields correctly.'
        return
    }

    isLoading.value = true

    try {
        const response = await fetch(`${API_BASE}/auth/signup`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                firstName: userForm.value.firstName,
                lastName: userForm.value.lastName,
                email: userForm.value.email,
                password: userForm.value.password,
                confirmPassword: userForm.value.password // Send same password for both fields
            })
        })

        const data = await response.json()

        if (!response.ok) {
            throw new Error(data.detail || 'Failed to create user')
        }

        // If user should be admin, make them admin
        if (userForm.value.isAdmin) {
            try {
                const adminResponse = await fetch(`${API_BASE}/auth/make-admin/${userForm.value.email}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    }
                })
                
                if (!adminResponse.ok) {
                    console.warn('User created but failed to grant admin privileges')
                }
            } catch (adminError) {
                console.warn('User created but failed to grant admin privileges:', adminError)
            }
        }

        successMessage.value = `User "${userForm.value.firstName} ${userForm.value.lastName}" has been created successfully!`
        router.push('/users')
    } catch (error) {
        console.error('Error creating user:', error)
        errorMessage.value = error.message || 'Failed to create user. Please try again.'
    } finally {
        isLoading.value = false
    }
}
</script>

<style scoped>
/* Page Header */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-5);
  padding-bottom: var(--space-4);
  border-bottom: 1px solid var(--border-default);
}

.header-content h1.page-title {
  font-size: 2rem;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.page-subtitle {
  color: var(--text-secondary);
  font-size: 1rem;
  margin-top: var(--space-1);
  margin-bottom: 0;
}

/* Form Section */
.form-section {
  max-width: 900px;
  margin: 0 auto;
}

.form-card {
  background-color: var(--bg-secondary);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-medium);
  overflow: hidden;
}

.user-form {
  padding: var(--space-3);
}

.form-columns {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: var(--space-4);
  margin-bottom: var(--space-3);
}

.form-column {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.form-group {
  margin-bottom: 0;
}

.form-group label {
  display: block;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: var(--space-1);
  font-size: 0.875rem;
}

.form-input {
  width: 100%;
  padding: var(--space-2) var(--space-3);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-small);
  background-color: var(--bg-primary);
  color: var(--text-primary);
  font-size: 0.875rem;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.form-input:focus {
  outline: none;
  border-color: var(--accent-secondary);
  box-shadow: 0 0 0 3px rgba(47, 129, 247, 0.1);
}

.form-input:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  background-color: var(--bg-tertiary);
}

/* Checkbox Group */
.checkbox-group {
  border: 1px solid var(--border-default);
  border-radius: var(--radius-small);
  padding: var(--space-2);
  background-color: var(--bg-tertiary);
  margin-bottom: var(--space-3) !important;
}

.checkbox-label {
  display: flex;
  align-items: center;
  cursor: pointer;
  margin-bottom: var(--space-1);
}

.form-checkbox {
  margin-right: var(--space-2);
  width: 16px;
  height: 16px;
}

.checkbox-text {
  font-weight: 600;
  color: var(--text-primary);
}

.checkbox-description {
  color: var(--text-secondary);
  font-size: 0.75rem;
  margin: 0;
  line-height: 1.4;
}

/* Buttons */
.btn-primary {
  padding: var(--space-2) var(--space-3);
  border: 1px solid var(--accent-secondary);
  border-radius: var(--radius-small);
  background-color: var(--accent-secondary);
  color: white;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  min-width: 100px;
}

.btn-full {
  width: 100%;
  justify-content: center;
  display: flex;
  align-items: center;
}

.btn-primary:hover:not(:disabled) {
  background-color: #2563eb;
  border-color: #2563eb;
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Loading Spinner */
.loading {
  width: 16px;
  height: 16px;
  border: 2px solid transparent;
  border-top: 2px solid currentColor;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  display: inline-block;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Alert Messages */
.alert {
  padding: var(--space-2);
  border-radius: var(--radius-small);
  margin-bottom: var(--space-2);
  border-left: 4px solid;
  font-size: 0.875rem;
}

.alert-success {
  background-color: rgba(35, 134, 54, 0.15);
  border-left-color: var(--accent-primary);
  color: var(--accent-primary);
}

.alert-error {
  background-color: rgba(218, 54, 51, 0.15);
  border-left-color: var(--accent-danger);
  color: var(--accent-danger);
}

/* Responsive Design */
@media (max-width: 992px) {
  .form-columns {
    grid-template-columns: 1fr 1fr;
    gap: var(--space-3);
  }
  
  .form-column:last-child {
    grid-column: 1 / -1;
    display: grid;
    grid-template-columns: 1fr auto;
    gap: var(--space-3);
    align-items: start;
  }
}

@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--space-3);
  }
  
  .form-section {
    margin: 0 var(--space-2);
    max-width: none;
  }
  
  .form-columns {
    grid-template-columns: 1fr;
    gap: var(--space-3);
  }
  
  .form-column:last-child {
    grid-column: auto;
    display: flex;
    flex-direction: column;
    gap: var(--space-3);
  }
  
  .btn-full {
    width: 100%;
  }
}
</style>