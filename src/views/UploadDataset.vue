<template>
    <navigation-bar></navigation-bar>
    <div class="container">
        <!-- Professional Header Section -->
        <div class="page-header">
            <div class="header-content">
                <h1 class="page-title">Upload New Dataset</h1>
                <p class="page-subtitle">Add a new dataset to the platform for training and analysis.</p>
            </div>
        </div>

        <!-- Upload Dataset Form -->
        <div class="form-section">
            <div class="card form-card">
                <div class="card-header">
                    <h3 class="card-title">Dataset Information</h3>
                </div>
                
                <form @submit.prevent="uploadDataset" class="dataset-form">
                    <div class="form-columns">
                        <!-- Column 1: Basic Information -->
                        <div class="form-column">
                            <div class="form-group">
                                <label for="datasetName">Dataset Name</label>
                                <input 
                                    id="datasetName"
                                    type="text" 
                                    v-model="datasetForm.name" 
                                    placeholder="Enter dataset name" 
                                    required
                                    :disabled="isLoading"
                                    class="form-input"
                                >
                            </div>

                            <div class="form-group">
                                <label for="datasetDescription">Description</label>
                                <textarea 
                                    id="datasetDescription"
                                    v-model="datasetForm.description" 
                                    placeholder="Enter dataset description" 
                                    required
                                    :disabled="isLoading"
                                    class="form-textarea"
                                    rows="4"
                                ></textarea>
                            </div>
                        </div>

                        <!-- Column 2: Metadata File Upload -->
                        <div class="form-column">
                            <div class="form-group">
                                <label>Metadata File</label>
                                <div 
                                    class="file-upload-area"
                                    :class="{ 
                                        'drag-over': isDraggingMetadata,
                                        'has-file': datasetForm.metadataFile
                                    }"
                                    @dragover.prevent="handleDragOver('metadata')"
                                    @dragleave.prevent="handleDragLeave('metadata')"
                                    @drop.prevent="handleDrop('metadata', $event)"
                                    @click="triggerFileInput('metadata')"
                                >
                                    <div v-if="!datasetForm.metadataFile" class="upload-placeholder">
                                        <svg class="upload-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                            <path d="M7 10L12 15L17 10" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                                            <path d="M12 15V3" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                                            <path d="M21 15V19A2 2 0 0 1 19 21H5A2 2 0 0 1 3 19V15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                                        </svg>
                                        <p>Drop metadata file here or click to browse</p>
                                        <span class="file-types">Supported: CSV, JSON, XML</span>
                                    </div>
                                    <div v-else class="uploaded-file">
                                        <svg class="file-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                            <path d="M14 2H6A2 2 0 0 0 4 4V20A2 2 0 0 0 6 22H18A2 2 0 0 0 20 20V8L14 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                                            <polyline points="14,2 14,8 20,8" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                                        </svg>
                                        <div class="file-info">
                                            <span class="file-name">{{ datasetForm.metadataFile.name }}</span>
                                            <span class="file-size">{{ formatFileSize(datasetForm.metadataFile.size) }}</span>
                                        </div>
                                        <button type="button" @click.stop="removeFile('metadata')" class="remove-file">
                                            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                                <line x1="18" y1="6" x2="6" y2="18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                                                <line x1="6" y1="6" x2="18" y2="18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                                            </svg>
                                        </button>
                                    </div>
                                </div>
                                <input 
                                    ref="metadataFileInput"
                                    type="file" 
                                    accept=".csv,.json,.xml"
                                    @change="handleFileSelect('metadata', $event)"
                                    style="display: none"
                                >
                            </div>
                        </div>

                        <!-- Column 3: Dataset Folder Upload -->
                        <div class="form-column">
                            <div class="form-group">
                                <label>Dataset Folder</label>
                                <div 
                                    class="folder-upload-area"
                                    :class="{ 
                                        'drag-over': isDraggingFolder,
                                        'has-folder': datasetForm.datasetFolder && datasetForm.datasetFolder.length > 0
                                    }"
                                    @dragover.prevent="handleDragOver('folder')"
                                    @dragleave.prevent="handleDragLeave('folder')"
                                    @drop.prevent="handleDrop('folder', $event)"
                                    @click="triggerFolderInput"
                                >
                                    <div v-if="!datasetForm.datasetFolder || datasetForm.datasetFolder.length === 0" class="upload-placeholder">
                                        <svg class="upload-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                            <path d="M22 19A2 2 0 0 1 20 21H4A2 2 0 0 1 2 19V5A2 2 0 0 1 4 3H9L11 6H20A2 2 0 0 1 22 8V19Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                                            <path d="M12 11V17" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                                            <path d="M9 14L12 11L15 14" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                                        </svg>
                                        <p>Drop dataset folder here or click to browse</p>
                                        <span class="file-types">Audio files and directory structure</span>
                                    </div>
                                    <div v-else class="uploaded-folder">
                                        <svg class="folder-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                            <path d="M22 19A2 2 0 0 1 20 21H4A2 2 0 0 1 2 19V5A2 2 0 0 1 4 3H9L11 6H20A2 2 0 0 1 22 8V19Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                                        </svg>
                                        <div class="folder-info">
                                            <span class="folder-name">{{ datasetForm.datasetFolder.length }} files selected</span>
                                            <span class="folder-size">{{ getTotalFolderSize() }}</span>
                                        </div>
                                        <button type="button" @click.stop="removeFile('folder')" class="remove-file">
                                            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                                <line x1="18" y1="6" x2="6" y2="18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                                                <line x1="6" y1="6" x2="18" y2="18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                                            </svg>
                                        </button>
                                    </div>
                                </div>
                                <input 
                                    ref="folderInput"
                                    type="file" 
                                    webkitdirectory
                                    multiple
                                    @change="handleFileSelect('folder', $event)"
                                    style="display: none"
                                >
                            </div>

                            <div class="form-group">
                                <button 
                                    type="submit" 
                                    :disabled="isLoading || !isFormValid"
                                    class="btn-primary btn-full"
                                >
                                    <span v-if="isLoading" class="loading"></span>
                                    <span v-else>Upload Dataset</span>
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

                    <!-- Upload Progress -->
                    <div v-if="isLoading" class="upload-progress">
                        <div class="progress-bar">
                            <div class="progress-fill" :style="{ width: uploadProgress + '%' }"></div>
                        </div>
                        <span class="progress-text">{{ uploadProgress }}% uploaded</span>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import NavigationBar from '@/components/NavigationBar.vue';

const router = useRouter()
const isLoading = ref(false)
const errorMessage = ref('')
const successMessage = ref('')
const uploadProgress = ref(0)

// Drag and drop states
const isDraggingMetadata = ref(false)
const isDraggingFolder = ref(false)

// File input refs
const metadataFileInput = ref(null)
const folderInput = ref(null)

const API_BASE = 'http://localhost:8000'

// Form data
const datasetForm = ref({
    name: '',
    description: '',
    metadataFile: null,
    datasetFolder: []
})

// Form validation
const isFormValid = computed(() => {
    return datasetForm.value.name.trim() !== '' &&
           datasetForm.value.description.trim() !== '' &&
           datasetForm.value.metadataFile !== null &&
           datasetForm.value.datasetFolder.length > 0
})

// File size formatting
const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

// Get total folder size
const getTotalFolderSize = () => {
    if (!datasetForm.value.datasetFolder || datasetForm.value.datasetFolder.length === 0) return '0 Bytes'
    const totalSize = Array.from(datasetForm.value.datasetFolder).reduce((total, file) => total + file.size, 0)
    return formatFileSize(totalSize)
}

// Drag and drop handlers
const handleDragOver = (type) => {
    if (type === 'metadata') {
        isDraggingMetadata.value = true
    } else if (type === 'folder') {
        isDraggingFolder.value = true
    }
}

const handleDragLeave = (type) => {
    if (type === 'metadata') {
        isDraggingMetadata.value = false
    } else if (type === 'folder') {
        isDraggingFolder.value = false
    }
}

const handleDrop = (type, event) => {
    if (type === 'metadata') {
        isDraggingMetadata.value = false
        const files = event.dataTransfer.files
        if (files.length > 0) {
            datasetForm.value.metadataFile = files[0]
        }
    } else if (type === 'folder') {
        isDraggingFolder.value = false
        const files = event.dataTransfer.files
        if (files.length > 0) {
            datasetForm.value.datasetFolder = files
        }
    }
}

// File input handlers
const triggerFileInput = (type) => {
    if (type === 'metadata') {
        metadataFileInput.value.click()
    }
}

const triggerFolderInput = () => {
    folderInput.value.click()
}

const handleFileSelect = (type, event) => {
    const files = event.target.files
    if (type === 'metadata' && files.length > 0) {
        datasetForm.value.metadataFile = files[0]
    } else if (type === 'folder' && files.length > 0) {
        datasetForm.value.datasetFolder = files
    }
}

// Remove file handlers
const removeFile = (type) => {
    if (type === 'metadata') {
        datasetForm.value.metadataFile = null
        if (metadataFileInput.value) {
            metadataFileInput.value.value = ''
        }
    } else if (type === 'folder') {
        datasetForm.value.datasetFolder = []
        if (folderInput.value) {
            folderInput.value.value = ''
        }
    }
}

// Upload dataset
const uploadDataset = async () => {
    errorMessage.value = ''
    successMessage.value = ''
    
    if (!isFormValid.value) {
        errorMessage.value = 'Please fill in all fields and upload required files.'
        return
    }

    isLoading.value = true
    uploadProgress.value = 0

    try {
        const formData = new FormData()
        formData.append('name', datasetForm.value.name)
        formData.append('description', datasetForm.value.description)
        formData.append('metadata', datasetForm.value.metadataFile)
        
        // Append all dataset files
        for (let i = 0; i < datasetForm.value.datasetFolder.length; i++) {
            formData.append('dataset_files', datasetForm.value.datasetFolder[i])
        }

        const response = await fetch(`${API_BASE}/datasets/upload`, {
            method: 'POST',
            body: formData
        })

        const data = await response.json()

        if (!response.ok) {
            throw new Error(data.detail || 'Failed to upload dataset')
        }

        uploadProgress.value = 100
        successMessage.value = `Dataset "${datasetForm.value.name}" has been uploaded successfully!`
        
        // Reset form after successful upload
        setTimeout(() => {
            router.push('/datasetslibrary')
        }, 2000)
        
    } catch (error) {
        console.error('Error uploading dataset:', error)
        errorMessage.value = error.message || 'Failed to upload dataset. Please try again.'
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
  max-width: 1200px;
  margin: 0 auto;
}

.form-card {
  background-color: var(--bg-secondary);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-medium);
  overflow: hidden;
}

.card-header {
  padding: var(--space-4);
  border-bottom: 1px solid var(--border-default);
  background-color: var(--bg-primary);
}

.card-title {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-primary);
}

.dataset-form {
  padding: var(--space-4);
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
  margin-bottom: var(--space-2);
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

.form-textarea {
  width: 100%;
  padding: var(--space-2) var(--space-3);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-small);
  background-color: var(--bg-primary);
  color: var(--text-primary);
  font-size: 0.875rem;
  font-family: inherit;
  resize: vertical;
  min-height: 100px;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.form-input:focus,
.form-textarea:focus {
  outline: none;
  border-color: var(--accent-secondary);
  box-shadow: 0 0 0 3px rgba(47, 129, 247, 0.1);
}

.form-input:disabled,
.form-textarea:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  background-color: var(--bg-tertiary);
}

/* File Upload Areas */
.file-upload-area,
.folder-upload-area {
  border: 2px dashed var(--border-default);
  border-radius: var(--radius-medium);
  padding: var(--space-4);
  text-align: center;
  cursor: pointer;
  transition: all 0.2s ease;
  background-color: var(--bg-primary);
  min-height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.file-upload-area:hover,
.folder-upload-area:hover {
  border-color: var(--accent-secondary);
  background-color: rgba(47, 129, 247, 0.05);
}

.file-upload-area.drag-over,
.folder-upload-area.drag-over {
  border-color: var(--accent-primary);
  background-color: rgba(47, 129, 247, 0.1);
}

.file-upload-area.has-file,
.folder-upload-area.has-folder {
  border-color: var(--accent-primary);
  background-color: rgba(34, 197, 94, 0.05);
}

.upload-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-2);
}

.upload-icon {
  width: 48px;
  height: 48px;
  color: var(--text-secondary);
  margin-bottom: var(--space-2);
}

.upload-placeholder p {
  margin: 0;
  font-weight: 500;
  color: var(--text-primary);
  font-size: 0.9rem;
}

.file-types {
  font-size: 0.75rem;
  color: var(--text-secondary);
}

/* Uploaded File Display */
.uploaded-file,
.uploaded-folder {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-2);
  background-color: var(--bg-secondary);
  border-radius: var(--radius-small);
  width: 100%;
}

.file-icon,
.folder-icon {
  width: 32px;
  height: 32px;
  color: var(--accent-primary);
  flex-shrink: 0;
}

.file-info,
.folder-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}

.file-name,
.folder-name {
  font-weight: 500;
  color: var(--text-primary);
  font-size: 0.875rem;
}

.file-size,
.folder-size {
  font-size: 0.75rem;
  color: var(--text-secondary);
}

.remove-file {
  background: none;
  border: none;
  color: var(--accent-danger);
  cursor: pointer;
  padding: var(--space-1);
  border-radius: var(--radius-small);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.2s ease;
}

.remove-file:hover {
  background-color: rgba(239, 68, 68, 0.1);
}

.remove-file svg {
  width: 16px;
  height: 16px;
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
  padding: var(--space-3);
  border-radius: var(--radius-small);
  margin-bottom: var(--space-3);
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

/* Upload Progress */
.upload-progress {
  margin-top: var(--space-4);
  padding: var(--space-3);
  background-color: var(--bg-primary);
  border-radius: var(--radius-small);
  border: 1px solid var(--border-default);
}

.progress-bar {
  width: 100%;
  height: 8px;
  background-color: var(--bg-tertiary);
  border-radius: var(--radius-small);
  overflow: hidden;
  margin-bottom: var(--space-2);
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--accent-primary), var(--accent-secondary));
  border-radius: var(--radius-small);
  transition: width 0.3s ease;
}

.progress-text {
  font-size: 0.875rem;
  color: var(--text-secondary);
  font-weight: 500;
}

/* Responsive Design */
@media (max-width: 992px) {
  .form-columns {
    grid-template-columns: 1fr 1fr;
    gap: var(--space-3);
  }
  
  .form-column:last-child {
    grid-column: 1 / -1;
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
  }
  
  .btn-full {
    width: 100%;
  }
  
  .upload-placeholder p {
    font-size: 0.8rem;
  }
  
  .upload-icon {
    width: 36px;
    height: 36px;
  }
}

@media (max-width: 480px) {
  .file-upload-area,
  .folder-upload-area {
    padding: var(--space-3);
    min-height: 100px;
  }
  
  .uploaded-file,
  .uploaded-folder {
    flex-direction: column;
    text-align: center;
    gap: var(--space-2);
  }
}
</style>