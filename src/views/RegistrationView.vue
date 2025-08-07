<template>
    <div class="header">
        <h1>Speaker Identification Platform</h1>
         <p id="info">A platform for testing and training on speaker identification models.
         Inspired by VGGVox, we have implemented a speaker identification model that can be tested and trained on this platform.
         You can test the model on your own audio samples, providing a hands-on experience with speaker identification.
         You can also train the model by uploading your own datasets, enhancing its accuracy and performance for specific speaker identification tasks.</p>
    </div>

    <div class="Forms">

        <form class="login">
            <h3>Login</h3>
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
        </form>

        <form class="signup">
            <h3>Sign Up</h3>
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
        </form>

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
                confirmPassword: ''
            }
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
#info{
    text-align: justify;
    width: 50%;
    align-self: center;
}

.header{
    display: flex; flex-direction: column;
    justify-content: center;
    align-content: center;
}
</style>