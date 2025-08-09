<template>
    <div class="header">
        <div class="header-content">
            <div class="header-text">
                <h1 class="header-title">
                    <span class="title-main">Speaker Identification</span>
                    <span class="title-accent">Platform</span>
                </h1>
            </div>
            <div class="header-description">
                <p class="description-text">
                    A cutting-edge platform for testing and training speaker identification models.
                    Inspired by VGGVox, our implementation provides hands-on experience with state-of-the-art 
                    voice recognition technology. Test the model with your audio samples or enhance its 
                    performance by training with custom datasets.
                </p>

            </div>
        </div>
    </div>

    <div class="auth-container">
        <div class="auth-card">
            <!-- Login Form -->
            <form v-if="isLoginMode" class="auth-form">
                <h3>Welcome Back</h3>
                <p class="form-subtitle">Sign in to your account</p>
                
                <label>E-mail</label>
                <input 
                    type="email" 
                    v-model="loginForm.email" 
                    placeholder="Enter your email" 
                    required
                    :disabled="isLoading"
                >
                <label>Password</label>
                <input 
                    type="password" 
                    v-model="loginForm.password" 
                    placeholder="Enter your password" 
                    required
                    :disabled="isLoading"
                >
                <button 
                    type="submit" 
                    v-on:click.prevent="login()"
                    :disabled="isLoading"
                >
                    <span v-if="isLoading" class="loading"></span>
                    {{ isLoading ? 'Logging in...' : 'Login' }}
                </button>
                
                <div class="auth-switch">
                    <p>Don't have an account? 
                        <span class="switch-link" @click="toggleMode">Create one</span>
                    </p>
                </div>
            </form>

            <!-- Signup Form -->
            <form v-if="!isLoginMode" class="auth-form">
                <h3>Create Account</h3>
                <p class="form-subtitle">Join our speaker identification platform</p>
                
                <label>First Name</label>
                <input 
                    type="text" 
                    v-model="signupForm.firstName" 
                    placeholder="Enter your first name" 
                    required
                    :disabled="isLoading"
                >
                <label>Last Name</label>
                <input 
                    type="text" 
                    v-model="signupForm.lastName" 
                    placeholder="Enter your last name" 
                    required
                    :disabled="isLoading"
                >
                <label>E-mail</label>
                <input 
                    type="email" 
                    v-model="signupForm.email" 
                    placeholder="Enter your email" 
                    required
                    :disabled="isLoading"
                >
                <label>Password</label>
                <input 
                    type="password" 
                    v-model="signupForm.password" 
                    placeholder="Enter your password" 
                    required
                    :disabled="isLoading"
                >
                <label>Confirm Password</label>
                <input 
                    type="password" 
                    v-model="signupForm.confirmPassword" 
                    placeholder="Confirm your password" 
                    required
                    :disabled="isLoading"
                >
                <button 
                    type="submit" 
                    v-on:click.prevent="signup()"
                    :disabled="isLoading"
                >
                    <span v-if="isLoading" class="loading"></span>
                    {{ isLoading ? 'Creating Account...' : 'Sign Up' }}
                </button>
                
                <div class="auth-switch">
                    <p>Already have an account? 
                        <span class="switch-link" @click="toggleMode">Sign in</span>
                    </p>
                </div>
            </form>
        </div>
    </div>

    <div class="footer">
        <div class="footer1">
            <p>Get in touch: (Contact information)</p> 
        </div>
        <div class="footer2">
            <p>Developed by: (Developers information)</p>
        </div>
        <div class="footer3">
            <p>© UM6P College of Computing - 2025</p>
        </div>
    </div>

</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// Mode toggle state
const isLoginMode = ref(true)

// Reactive form data
const loginForm = ref({
    email: '',
    password: ''
})

const signupForm = ref({
    firstName: '',
    lastName: '',
    email: '',
    password: '',
    confirmPassword: '',
    admin: false // Default admin value
})

const isLoading = ref(false)
const errorMessage = ref('')
const successMessage = ref('')

// API base URL
const API_BASE = 'http://localhost:8000'

// Toggle between login and signup modes
const toggleMode = () => {
    isLoginMode.value = !isLoginMode.value
    // Clear any error messages when switching modes
    errorMessage.value = ''
    successMessage.value = ''
}

const signup = async () => {
    isLoading.value = true
    errorMessage.value = ''
    successMessage.value = ''

    try {
        const response = await fetch(`${API_BASE}/auth/signup`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(signupForm.value)
        })

        const data = await response.json()

        if (response.ok) {
            alert('Account created successfully! You can now login.')
            // Clear the form
            signupForm.value = {
                firstName: '',
                lastName: '',
                email: '',
                password: '',
                confirmPassword: '',
                admin: false
            }
            // Switch to login mode after successful signup
            isLoginMode.value = true
        } else {
            alert(data.detail || "Signup failed.")
        }
    } catch (error) {
        alert('Network error. Please try again.')
        console.error('Signup error:', error)
    } finally {
        isLoading.value = false
    }
}

const login = async () => {
    isLoading.value = true
    errorMessage.value = ''
    successMessage.value = ''

    try {
        const response = await fetch(`${API_BASE}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(loginForm.value)
        })

        const data = await response.json()

        if (response.ok) {
            alert(`Welcome back, ${data.user.firstName}!`)
            // Store user data in localStorage (to be changed)
            localStorage.setItem('user', JSON.stringify(data.user))
            // Redirect to dashboard after successful login
            setTimeout(() => {
                router.push('/dashboard')
            }, 1500)
        } else {
            alert(data.detail || 'Login failed')
        }
    } catch (error) {
        alert('Network error. Please try again.')
        console.error('Login error:', error)
    } finally {
        isLoading.value = false
    }
}
</script>

<style scoped>
/* Enhanced Header Styles */
.header {
    background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-tertiary) 100%);
    border-bottom: 2px solid var(--border-default);
    padding: var(--space-6) 0;
    margin-bottom: var(--space-6);
    position: relative;
    overflow: hidden;
}

.header::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: radial-gradient(circle at 20% 50%, rgba(47, 129, 247, 0.1) 0%, transparent 50%),
                radial-gradient(circle at 80% 20%, rgba(35, 134, 54, 0.1) 0%, transparent 50%);
    pointer-events: none;
}

.header-content {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 var(--space-4);
    position: relative;
    z-index: 1;
}

.header-text {
    text-align: center;
    margin-bottom: var(--space-5);
}

.header-title {
    font-size: 3.5rem;
    font-weight: 700;
    line-height: 1.1;
    margin-bottom: var(--space-3);
    background: linear-gradient(135deg, var(--text-primary) 0%, var(--accent-secondary) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: var(--space-1);
}

.title-main {
    font-weight: 700;
}

.title-accent {
    font-weight: 300;
    font-size: 0.85em;
    color: var(--accent-secondary);
    -webkit-text-fill-color: var(--accent-secondary);
}

.header-subtitle {
    font-size: 1.25rem;
    color: var(--text-secondary);
    font-weight: 400;
    letter-spacing: 0.5px;
    margin-bottom: 0;
}

.header-description {
    max-width: 800px;
    margin: 0 auto;
    text-align: center;
}

.description-text {
    font-size: 1.1rem;
    line-height: 1.7;
    color: var(--text-secondary);
    margin-bottom: var(--space-5);
    text-align: justify;
}

.feature-highlights {
    display: flex;
    justify-content: center;
    gap: var(--space-6);
    flex-wrap: wrap;
}

.feature-item {
    display: flex;
    align-items: center;
    gap: var(--space-2);
    padding: var(--space-2) var(--space-3);
    background-color: rgba(255, 255, 255, 0.05);
    border: 1px solid var(--border-muted);
    border-radius: var(--radius-large);
    backdrop-filter: blur(10px);
    transition: all 0.3s ease;
}

.feature-item:hover {
    transform: translateY(-2px);
    background-color: rgba(255, 255, 255, 0.1);
    border-color: var(--accent-secondary);
    box-shadow: 0 4px 12px rgba(47, 129, 247, 0.2);
}

.feature-icon {
    font-size: 1.5rem;
    filter: grayscale(0.3);
    transition: filter 0.3s ease;
}

.feature-item:hover .feature-icon {
    filter: none;
}

.feature-text {
    font-size: 0.9rem;
    font-weight: 500;
    color: var(--text-primary);
    white-space: nowrap;
}

/* Auth container for centering the card */
.auth-container {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 60vh;
    padding: var(--space-4);
}

/* Single auth card */
.auth-card {
    width: 100%;
    max-width: 450px;
    margin: 0 auto;
}

/* Auth form styling */
.auth-form {
    background-color: var(--bg-secondary);
    border: 1px solid var(--border-default);
    border-radius: var(--radius-large);
    padding: var(--space-6);
    box-shadow: var(--shadow-medium);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.auth-form:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-large);
}

/* Form title and subtitle */
.auth-form h3 {
    font-size: 1.75rem;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: var(--space-2);
    text-align: center;
}

.form-subtitle {
    color: var(--text-secondary);
    text-align: center;
    margin-bottom: var(--space-5);
    font-size: 0.9rem;
}

/* Auth switch section */
.auth-switch {
    margin-top: var(--space-4);
    text-align: center;
    padding-top: var(--space-3);
    border-top: 1px solid var(--border-muted);
}

.auth-switch p {
    color: var(--text-secondary);
    font-size: 0.875rem;
    margin-bottom: 0;
}

.switch-link {
    color: var(--accent-secondary);
    cursor: pointer;
    font-weight: 500;
    text-decoration: none;
    transition: color 0.2s ease;
}

.switch-link:hover {
    color: var(--text-primary);
    text-decoration: underline;
}

/* Responsive design */
@media (max-width: 768px) {
    .header {
        padding: var(--space-4) 0;
        margin-bottom: var(--space-4);
    }
    
    .header-content {
        padding: 0 var(--space-3);
    }
    
    .header-title {
        font-size: 2.5rem;
    }
    
    .header-subtitle {
        font-size: 1.1rem;
    }
    
    .description-text {
        font-size: 1rem;
        text-align: center;
    }
    
    .feature-highlights {
        gap: var(--space-3);
    }
    
    .feature-item {
        padding: var(--space-1) var(--space-2);
    }
    
    .feature-text {
        font-size: 0.8rem;
    }
    
    .auth-container {
        padding: var(--space-2);
        min-height: 50vh;
    }
    
    .auth-card {
        max-width: 100%;
    }
    
    .auth-form {
        padding: var(--space-4);
    }
    
    .auth-form h3 {
        font-size: 1.5rem;
    }
}

@media (max-width: 480px) {
    .header-title {
        font-size: 2rem;
    }
    
    .header-subtitle {
        font-size: 1rem;
    }
    
    .feature-highlights {
        flex-direction: column;
        align-items: center;
        gap: var(--space-2);
    }
    
    .feature-item {
        width: fit-content;
    }
    
    .auth-form {
        padding: var(--space-3);
    }
    
    .auth-form h3 {
        font-size: 1.25rem;
    }
}
</style>