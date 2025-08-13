<template>
    <navigation-bar></navigation-bar>
    <div class="container">
        <div class="page-header">
            <h1 class="page-title">Testing interface</h1>
            <p class="page-subtitle">Upload an audio file and identify the speaker using our advanced AI models</p>
        </div>
        
        <div class="parent">
            <div class="div1">
                <!-- Audio Upload Section -->
                <div class="card enhanced-card audio-input-section">
                    <div class="card-header">
                        <div class="header-content">
                            <h3 class="card-title">Audio Input</h3>
                        </div>
                    </div>
                    <div class="upload-area">
                        <div v-if="!uploadedFile" 
                             class="drop-zone" 
                             :class="{ dragover: isDragOver }"
                             @drop="handleDrop"
                             @dragover.prevent="isDragOver = true"
                             @dragleave="isDragOver = false"
                             @click="triggerFileInput">
                            <div class="upload-placeholder">
                                <svg class="upload-icon" width="48" height="48" viewBox="0 0 24 24" fill="currentColor">
                                    <path d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z"/>
                                </svg>
                                <h4>Drop your audio file here</h4>
                                <p>or click to browse</p>
                                <span class="file-formats">Supported: WAV, MP3, FLAC</span>
                            </div>
                        </div>
                        
                        <div v-else class="file-preview">
                            <div class="file-info">
                                <h4>{{ uploadedFile.name }}</h4>
                                <p>{{ formatFileSize(uploadedFile.size) }} • {{ getFileExtension(uploadedFile.name).toUpperCase() }}</p>
                            </div>
                            <button class="btn-secondary" @click="removeFile">
                                <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                                    <path d="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"/>
                                </svg>
                                Remove
                            </button>
                        </div>
                        
                        <input 
                            ref="fileInput" 
                            type="file" 
                            accept=".wav,.mp3,.flac" 
                            @change="handleFileSelect" 
                            style="display: none;">
                        
                        <div v-if="uploadError" class="alert alert-error">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                                <path d="M13,13H11V7H13M13,17H11V15H13M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2Z"/>
                            </svg>
                            {{ uploadError }}
                        </div>
                    </div>
                </div>
            </div>
            <div class="div2">
                <!-- Model Selection Section -->
                <div class="card enhanced-card model-selection-section">
                    <div class="card-header">
                        <div class="header-content">
                            <h3 class="card-title">Model Selection</h3>
                        </div>
                    </div>
                    <div class="model-content">
                        <!-- Search Filter -->
                        <div class="models-filter">
                            <label for="model-search">Search Models</label>
                            <input 
                                id="model-search"
                                v-model="searchQuery" 
                                type="text" 
                                class="search-input" 
                                placeholder="Filter by model name or architecture..."
                                @input="filterModels">
                        </div>

                        <!-- Loading State -->
                        <div v-if="modelsLoading" class="loading-state">
                            <div class="spinner"></div>
                            <p>Loading models...</p>
                        </div>

                        <!-- Error State -->
                        <div v-else-if="modelsError" class="error-state">
                            <svg width="48" height="48" viewBox="0 0 24 24" fill="currentColor">
                                <path d="M13,13H11V7H13M13,17H11V15H13M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2Z"/>
                            </svg>
                            <h4>Failed to load models</h4>
                            <p>{{ modelsError }}</p>
                            <button class="btn-retry" @click="loadModels">Retry</button>
                        </div>

                        <!-- Models List -->
                        <div v-else-if="filteredModels.length > 0" class="models-grid">
                            <div 
                                v-for="model in filteredModels" 
                                :key="model.id"
                                class="model-card"
                                :class="{ selected: selectedModel?.id === model.id }"
                                @click="selectModel(model)">
                                <div class="model-header">
                                    <h4 class="model-name">{{ model.name }}</h4>
                                    <span class="model-version">v{{ model.version }}</span>
                                </div>
                                <div class="model-meta">
                                    <span class="architecture-label">{{ model.architecture }}</span>
                                    <span class="accuracy-score">{{ model.accuracy }}% accuracy</span>
                                </div>
                            </div>
                        </div>

                        <!-- Empty State -->
                        <div v-else class="empty-state">
                            <svg width="48" height="48" viewBox="0 0 24 24" fill="currentColor">
                                <path d="M9.5,3A6.5,6.5 0 0,1 16,9.5C16,11.11 15.41,12.59 14.44,13.73L14.71,14H15.5L20.5,19L19,20.5L14,15.5V14.71L13.73,14.44C12.59,15.41 11.11,16 9.5,16A6.5,6.5 0 0,1 3,9.5A6.5,6.5 0 0,1 9.5,3M9.5,5C7,5 5,7 5,9.5C5,12 7,14 9.5,14C12,14 14,12 14,9.5C14,7 12,5 9.5,5Z"/>
                            </svg>
                            <h4>No models found</h4>
                            <p>Try adjusting your search terms</p>
                        </div>

                        <!-- Selected Model Info -->
                        <div v-if="selectedModel" class="selected-model-info">
                            <h4>Selected Model</h4>
                            <p><strong>{{ selectedModel.name }}</strong> v{{ selectedModel.version }}</p>
                            <p class="model-details">{{ selectedModel.architecture }} • {{ selectedModel.accuracy }}% accuracy</p>
                        </div>
                    </div>
                </div>
            </div>

            <div class="div3">
              <!-- Analysis & Results Section -->
              <div class="card enhanced-card analysis-section">
                <div class="card-header">
                  <div class="header-content">
                    <h3 class="card-title">Analysis & Results</h3>
                  </div>
                </div>
                <div class="analysis-content">
                  <!-- Action Button -->
                  <div class="actions-section">
                    <button
                      class="btn-confirm"
                      :disabled="!canRunInference"
                      @click="confirmAndRunInference()"
                    >
                      <div v-if="inferenceLoading" class="spinner-small"></div>
                      <span v-if="!inferenceLoading">Analyze Audio</span>
                      <span v-else>Analyzing...</span>
                    </button>
                  </div>

                  <!-- Results Section -->
                  <div v-if="showResults" class="results-section">
                    <!-- Audio Waveform -->
                    <div class="waveform-section">
                      <h4>Audio Waveform with Selected Segments</h4>
                      <div ref="waveformContainer" class="waveform-container"></div>
                      <div class="waveform-controls">
                        <button @click="playPause" class="control-btn">
                          <svg v-if="!isPlaying" width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                            <path d="M8,5.14V19.14L19,12.14L8,5.14Z"/>
                          </svg>
                          <svg v-else width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                            <path d="M14,19H18V5H14M6,19H10V5H6V19Z"/>
                          </svg>
                          {{ isPlaying ? 'Pause' : 'Play' }}
                        </button>
                        <span class="time-display">{{ formatTime(currentTime) }} / {{ formatTime(duration) }}</span>
                      </div>
                      <div class="segments-legend">
                        <h5>Selected Analysis Segments:</h5>
                        <div class="legend-items">
                          <div v-for="(segment, index) in analysisSegments" :key="index" class="legend-item">
                            <div class="legend-color" :style="{ backgroundColor: segment.color }"></div>
                            <span>Segment {{ index + 1 }}: {{ segment.start }}s - {{ segment.end }}s</span>
                          </div>
                        </div>
                      </div>
                    </div>

                    <!-- Predictions Section -->
                    <div class="predictions-section">
                      <h4>Speaker Identification Results</h4>
                      <div class="predictions-grid">
                        <div v-for="(prediction, index) in mockPredictions" :key="index" class="prediction-card">
                          <div class="prediction-header">
                            <div class="segment-indicator" :style="{ backgroundColor: analysisSegments[index]?.color }"></div>
                            <h5>Segment {{ index + 1 }}</h5>
                            <span class="confidence-score">{{ prediction.confidence }}%</span>
                          </div>
                          <div class="prediction-content">
                            <div class="predicted-speaker">
                              <span class="label">Predicted Speaker:</span>
                              <span class="speaker-name">{{ prediction.speaker }}</span>
                            </div>
                            <div class="time-range">
                              <span class="label">Time Range:</span>
                              <span class="time">{{ analysisSegments[index]?.start }}s - {{ analysisSegments[index]?.end }}s</span>
                            </div>
                            <div class="segment-features">

                            </div>
                          </div>
                        </div>
                      </div>
                    </div>

                  </div>

                  <!-- Empty State -->
                  <div v-else class="empty-results">
                    <svg width="64" height="64" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M12,2A3,3 0 0,1 15,5V11A3,3 0 0,1 12,14A3,3 0 0,1 9,11V5A3,3 0 0,1 12,2M19,11C19,14.53 16.39,17.44 13,17.93V21H11V17.93C7.61,17.44 5,14.53 5,11H7A5,5 0 0,0 12,16A5,5 0 0,0 17,11H19Z"/>
                    </svg>
                    <h4>No Analysis Results</h4>
                    <p>Upload an audio file and select a model to begin analysis</p>
                  </div>
                </div>
              </div>
            </div>

        </div>
    </div>
</template><script setup>
import NavigationBar from '@/components/NavigationBar.vue';
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue';
import WaveSurfer from 'wavesurfer.js';
import RegionsPlugin from 'wavesurfer.js/dist/plugins/regions.esm.js';

const API_BASE = 'http://localhost:8000'

// Reactive variables for audio upload
const uploadedFile = ref(null);
const isDragOver = ref(false);
const uploadError = ref('');
const uploadSuccess = ref(false);
const fileInput = ref(null);

// Reactive variables for model selection
const models = ref([]);
const selectedModel = ref(null);
const searchQuery = ref('');
const modelsLoading = ref(false);
const modelsError = ref('');

// Reactive variables for analysis and results
const inferenceLoading = ref(false);
const showResults = ref(false);
const waveformContainer = ref(null);
const wavesurfer = ref(null);
const isPlaying = ref(false);
const currentTime = ref(0);
const duration = ref(0);

// Mock data for analysis results
const analysisSegments = ref([
  { start: 2.5, end: 5.5, color: '#FF6B6B' },
  { start: 8.0, end: 11.0, color: '#4ECDC4' },
  { start: 15.2, end: 18.2, color: '#45B7D1' }
]);

const mockPredictions = ref([
  {
    speaker: 'Speaker A',
    confidence: 94.2,
    features: ['High pitch variation', 'Clear articulation', 'Moderate tempo']
  },
  {
    speaker: 'Speaker B', 
    confidence: 87.8,
    features: ['Deep voice', 'Slow speech rate', 'Distinctive accent']
  },
  {
    speaker: 'Speaker A',
    confidence: 91.5,
    features: ['Consistent tone', 'Fast speech rate', 'Emotional expression']
  }
]);

const canRunInference = computed(() => uploadedFile.value && selectedModel.value);



// Initialize WaveSurfer
const initWaveSurfer = async () => {
  if (!waveformContainer.value || !uploadedFile.value) return;

  try {
    // Destroy existing instance
    if (wavesurfer.value) {
      wavesurfer.value.destroy();
    }

    // Create new WaveSurfer instance
    wavesurfer.value = WaveSurfer.create({
      container: waveformContainer.value,
      waveColor: '#ddd',
      progressColor: '#2F81F7',
      cursorColor: '#2F81F7',
      barWidth: 2,
      barRadius: 3,
      responsive: true,
      height: 80,
      normalize: true,
      plugins: [
        RegionsPlugin.create({
          dragSelection: false,
        })
      ]
    });

    // Load audio file
    const audioUrl = URL.createObjectURL(uploadedFile.value);
    await wavesurfer.value.load(audioUrl);

    // Add event listeners
    wavesurfer.value.on('ready', () => {
      duration.value = wavesurfer.value.getDuration();
      addAnalysisRegions();
    });

    wavesurfer.value.on('audioprocess', () => {
      currentTime.value = wavesurfer.value.getCurrentTime();
    });

    wavesurfer.value.on('play', () => {
      isPlaying.value = true;
    });

    wavesurfer.value.on('pause', () => {
      isPlaying.value = false;
    });

    wavesurfer.value.on('finish', () => {
      isPlaying.value = false;
      currentTime.value = 0;
    });

  } catch (error) {
    console.error('Error initializing WaveSurfer:', error);
  }
};

// Add regions for analysis segments
const addAnalysisRegions = () => {
  if (!wavesurfer.value) return;

  const regions = wavesurfer.value.getActivePlugins().find(plugin => plugin.constructor.name === 'RegionsPlugin');
  if (!regions) return;

  // Clear existing regions
  regions.clearRegions();

  // Add analysis segments as regions
  analysisSegments.value.forEach((segment) => {
    regions.addRegion({
      start: segment.start,
      end: segment.end,
      color: segment.color,
      drag: false,
      resize: false,
    });
  });
};

// Audio controls
const playPause = () => {
  if (!wavesurfer.value) return;
  
  if (wavesurfer.value.isPlaying()) {
    wavesurfer.value.pause();
  } else {
    wavesurfer.value.play();
  }
};

// Format time display
const formatTime = (seconds) => {
  if (!seconds || isNaN(seconds)) return '0:00';
  const mins = Math.floor(seconds / 60);
  const secs = Math.floor(seconds % 60);
  return `${mins}:${secs.toString().padStart(2, '0')}`;
};

// Confirm and run inference
async function confirmAndRunInference() {
  if (!canRunInference.value) return;
  
  inferenceLoading.value = true;
  
  console.log('Running inference with:');
  console.log('- Audio file:', uploadedFile.value.name);
  console.log('- Selected model:', selectedModel.value.name);
  
  try {
    // Simulate inference process
    await new Promise(resolve => setTimeout(resolve, 3000));
    
    // Show results
    showResults.value = true;
    
    // Initialize waveform after results are shown
    await nextTick();
    await initWaveSurfer();
    
    console.log('Inference completed!');
  } catch (error) {
    console.error('Error during inference:', error);
  } finally {
    inferenceLoading.value = false;
  }
}

// Computed properties
const filteredModels = computed(() => {
  if (!searchQuery.value) return models.value;
  
  const query = searchQuery.value.toLowerCase();
  return models.value.filter(model => 
    model.name.toLowerCase().includes(query) ||
    model.architecture.toLowerCase().includes(query) ||
    model.description.toLowerCase().includes(query)
  );
});



// Supported audio formats
const supportedFormats = ['wav', 'mp3', 'flac'];
const maxFileSize = 100 * 1024 * 1024; // 100MB

// File handling functions
const validateFile = (file) => {
  // Reset previous states
  uploadError.value = '';
  uploadSuccess.value = false;
  
  if (!file) {
    uploadError.value = 'No file selected';
    return false;
  }
  
  // Check file size
  if (file.size > maxFileSize) {
    uploadError.value = 'File size too large. Maximum size is 100MB';
    return false;
  }
  
  // Check file type
  const extension = getFileExtension(file.name).toLowerCase();
  if (!supportedFormats.includes(extension)) {
    uploadError.value = 'Unsupported file format. Please use WAV, MP3, or FLAC files';
    return false;
  }
  
  return true;
};

const processFile = (file) => {
  if (validateFile(file)) {
    uploadedFile.value = file;
    uploadSuccess.value = true;
    
    // Clear success message after 3 seconds
    setTimeout(() => {
      uploadSuccess.value = false;
    }, 3000);
  }
};

const handleFileSelect = (event) => {
  const file = event.target.files[0];
  if (file) {
    processFile(file);
  }
};

const handleDrop = (event) => {
  event.preventDefault();
  isDragOver.value = false;
  
  const files = event.dataTransfer.files;
  if (files.length > 0) {
    processFile(files[0]);
  }
};

const triggerFileInput = () => {
  fileInput.value.click();
};

const removeFile = () => {
  uploadedFile.value = null;
  uploadError.value = '';
  uploadSuccess.value = false;
  showResults.value = false;
  
  // Destroy wavesurfer instance
  if (wavesurfer.value) {
    wavesurfer.value.destroy();
    wavesurfer.value = null;
  }
  
  if (fileInput.value) {
    fileInput.value.value = '';
  }
};

// Model selection functions
const loadModels = async () => {
  modelsLoading.value = true;
  modelsError.value = '';
  
  try {
    const response = await fetch(`${API_BASE}/models`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    models.value = data.models || data; // Handle different response formats
  } catch (error) {
    modelsError.value = error.message || 'Failed to load models from server';
    console.error('Error loading models:', error);
  } finally {
    modelsLoading.value = false;
  }
};

const selectModel = (model) => {
  selectedModel.value = model;
};

// Lifecycle hooks
onMounted(() => {
  loadModels();
});

onUnmounted(() => {
  // Cleanup WaveSurfer instance
  if (wavesurfer.value) {
    wavesurfer.value.destroy();
    wavesurfer.value = null;
  }
});

// Utility functions
const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
};

const getFileExtension = (filename) => {
  return filename.slice((filename.lastIndexOf('.') - 1 >>> 0) + 2);
};
</script>

<style scoped>
/* Container and Layout */
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: var(--space-4);
  min-height: calc(100vh - 80px);
  margin-bottom: var(--space-5);
}

.page-header {
  margin-bottom: var(--space-5);
  padding-bottom: var(--space-3);
  border-bottom: 1px solid var(--border-default);
}

.page-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: var(--space-2);
  background: linear-gradient(135deg, var(--accent-secondary), var(--accent-primary));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.page-subtitle {
  font-size: 1.1rem;
  color: var(--text-secondary);
  margin: 0;
  margin: 0 auto;
  line-height: 1.5;
}

/* Grid Layout */
.parent {
    display: grid;
    grid-template-columns: 1fr 2fr;
    grid-template-rows: repeat(2, 1fr);
    grid-column-gap: var(--space-4);
    grid-row-gap: var(--space-4);
    height: 80vh;
    min-height: 600px;
    margin-bottom: 100px;

  }

.div1 { grid-area: 1 / 1 / 2 / 2; }
.div2 { grid-area: 2 / 1 / 3 / 2; }
.div3 { grid-area: 1 / 2 / 3 / 3; }

/* Actions Styles */
.analysis-section {
  height: 100%;
}

.analysis-content {
  padding: var(--space-4);
  height: calc(100% - 60px);
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}

.actions-section {
  margin-bottom: var(--space-4);
}

.results-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.empty-results {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  color: var(--text-secondary);
  gap: var(--space-3);
}

.empty-results svg {
  opacity: 0.6;
}

.empty-results h4 {
  margin: 0;
  color: var(--text-primary);
  font-size: 1.2rem;
}

.empty-results p {
  margin: 0;
  max-width: 300px;
  line-height: 1.5;
}

/* Waveform Section */
.waveform-section {
  background: var(--bg-tertiary);
  border-radius: var(--radius-medium);
  padding: var(--space-4);
  border: 1px solid var(--border-default);
}

.waveform-section h4 {
  margin: 0 0 var(--space-3) 0;
  color: var(--text-primary);
  font-size: 1.1rem;
  font-weight: 600;
}

.waveform-container {
  background: var(--bg-secondary);
  border-radius: var(--radius-small);
  padding: var(--space-3);
  margin-bottom: var(--space-3);
  border: 1px solid var(--border-default);
}

.waveform-controls {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  margin-bottom: var(--space-3);
}

.control-btn {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  background: var(--accent-secondary);
  color: white;
  border: none;
  padding: var(--space-2) var(--space-3);
  border-radius: var(--radius-medium);
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 500;
  transition: all 0.2s ease;
}

.control-btn:hover {
  background: var(--accent-primary);
  transform: translateY(-1px);
}

.time-display {
  font-family: monospace;
  font-size: 0.9rem;
  color: var(--text-secondary);
  background: var(--bg-overlay);
  padding: var(--space-1) var(--space-2);
  border-radius: var(--radius-small);
}

.segments-legend {
  border-top: 1px solid var(--border-default);
  padding-top: var(--space-3);
}

.segments-legend h5 {
  margin: 0 0 var(--space-2) 0;
  color: var(--text-primary);
  font-size: 0.95rem;
  font-weight: 600;
}

.legend-items {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.legend-item {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  font-size: 0.85rem;
  color: var(--text-secondary);
}

.legend-color {
  width: 16px;
  height: 16px;
  border-radius: var(--radius-small);
  border: 1px solid var(--border-default);
}

/* Predictions Section */
.predictions-section {
  background: var(--bg-tertiary);
  border-radius: var(--radius-medium);
  padding: var(--space-4);
  border: 1px solid var(--border-default);
}

.predictions-section h4 {
  margin: 0 0 var(--space-3) 0;
  color: var(--text-primary);
  font-size: 1.1rem;
  font-weight: 600;
}

.predictions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: var(--space-3);
}

.prediction-card {
  background: var(--bg-secondary);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-medium);
  padding: var(--space-3);
  transition: all 0.2s ease;
}

.prediction-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-medium);
}

.prediction-header {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  margin-bottom: var(--space-3);
  padding-bottom: var(--space-2);
  border-bottom: 1px solid var(--border-default);
}

.segment-indicator {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  border: 1px solid var(--border-default);
}

.prediction-header h5 {
  margin: 0;
  flex: 1;
  color: var(--text-primary);
  font-size: 0.95rem;
  font-weight: 600;
}

.confidence-score {
  background: var(--accent-primary);
  color: white;
  padding: 2px 8px;
  border-radius: var(--radius-small);
  font-size: 0.8rem;
  font-weight: 600;
}

.prediction-content {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.predicted-speaker,
.time-range {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.label {
  font-size: 0.85rem;
  color: var(--text-secondary);
  font-weight: 500;
}

.speaker-name {
  font-size: 0.9rem;
  color: var(--text-primary);
  font-weight: 600;
}

.time {
  font-family: monospace;
  font-size: 0.85rem;
  color: var(--text-secondary);
  background: var(--bg-overlay);
  padding: 2px 6px;
  border-radius: var(--radius-small);
}

.segment-features {
  margin-top: var(--space-1);
}

.features-list {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-1);
  margin-top: var(--space-1);
}

.feature-tag {
  background: var(--bg-overlay);
  color: var(--text-secondary);
  padding: 2px 8px;
  border-radius: var(--radius-small);
  font-size: 0.75rem;
  border: 1px solid var(--border-default);
}

/* Summary Section */
.summary-section {
  background: var(--bg-tertiary);
  border-radius: var(--radius-medium);
  padding: var(--space-4);
  border: 1px solid var(--border-default);
}

.summary-section h4 {
  margin: 0 0 var(--space-3) 0;
  color: var(--text-primary);
  font-size: 1.1rem;
  font-weight: 600;
}

.summary-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--space-3);
}

.stat-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: var(--bg-secondary);
  padding: var(--space-3);
  border-radius: var(--radius-medium);
  border: 1px solid var(--border-default);
}

.stat-label {
  font-size: 0.9rem;
  color: var(--text-secondary);
  font-weight: 500;
}

.stat-value {
  font-size: 0.95rem;
  color: var(--text-primary);
  font-weight: 600;
}

.btn-confirm {
  background: linear-gradient(135deg, var(--accent-secondary), var(--accent-primary));
  color: white;
  border: none;
  padding: var(--space-3) var(--space-6);
  border-radius: var(--radius-medium);
  cursor: pointer;
  font-size: 1rem;
  font-weight: 600;
  transition: all 0.3s ease;
  width: 100%;
  box-shadow: var(--shadow-medium);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-2);
}

.btn-confirm:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: var(--shadow-large);
}

.btn-confirm:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.spinner-small {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top: 2px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

/* Enhanced Card Styles */
.card {
  background: var(--bg-secondary);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-large);
  box-shadow: var(--shadow-medium);
  height: 100%;
  display: flex;
  flex-direction: column;
  transition: all 0.3s ease;
}

.enhanced-card {
  background: var(--bg-secondary);
  border: 1px solid var(--border-default);
  box-shadow: var(--shadow-large);
}

.card-header {
  border-bottom: 1px solid var(--border-default);
  border-radius: var(--radius-large) var(--radius-large) 0 0;
}

.header-content {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.card-title {
  margin: 0;
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--text-primary);
  font-family: var(--font-family-sans);
}


.upload-area {
  height: 200px;
  max-height: 200px;
}

.drop-zone {
  border: 2px dashed var(--border-default);
  border-radius: var(--radius-medium);
  padding: var(--space-3);
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-tertiary);
}

.drop-zone:hover {
  border-color: var(--accent-secondary);
  background: var(--bg-overlay);
  transform: translateY(-2px);
}

.drop-zone.dragover {
  border-color: var(--accent-primary);
  background: var(--bg-overlay);
  box-shadow: 0 0 20px rgba(35, 134, 54, 0.3);
}

.upload-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-3);
}

.upload-icon {
  color: var(--text-secondary);
  transition: color 0.3s ease;
}

.drop-zone:hover .upload-icon {
  color: var(--accent-secondary);
}

.upload-placeholder h4 {
  margin: 0;
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--text-primary);
}

.upload-placeholder p {
  margin: 0;
  color: var(--text-secondary);
}

.file-formats {
  font-size: 0.9rem;
  background: var(--bg-overlay);
  padding: var(--space-1) var(--space-2);
  border-radius: var(--radius-small);
}

.file-preview {
  display: flex;
  align-items: center;
  gap: var(--space-4);
  padding: var(--space-4);
  background: var(--bg-overlay);
  border-radius: var(--radius-medium);
  border: 1px solid var(--border-default);
}
/* Alert Styles */
.alert {
  padding: var(--space-3);
  border-radius: var(--radius-medium);
  margin-top: var(--space-3);
  font-size: 0.9rem;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.alert-error {
  background: rgba(218, 54, 51, 0.1);
  color: var(--accent-danger);
  border: 1px solid var(--accent-danger);
}

.alert-success {
  background: rgba(35, 134, 54, 0.1);
  color: var(--accent-primary);
  border: 1px solid var(--accent-primary);
}

/* Model Selection Styles */
.model-selection-section {
  height: 100%;
}

.model-content {
  padding: var(--space-3);
  height: 200px;
  max-height: 200px;
  overflow-y: auto;
}

.loading-state, .error-state, .empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  height: 150px;
  gap: var(--space-2);
}

.spinner {
  width: 24px;
  height: 24px;
  border: 2px solid var(--border-default);
  border-top: 2px solid var(--accent-secondary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.models-filter {
  margin-bottom: var(--space-3);
}

.models-filter label {
  display: block;
  font-size: 0.9rem;
  font-weight: 500;
  color: var(--text-primary);
  margin-bottom: var(--space-2);
}

.search-input {
  width: 100%;
  padding: var(--space-2);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-medium);
  font-size: 0.9rem;
  background: var(--bg-tertiary);
  color: var(--text-primary);
  transition: all 0.2s ease;
  font-family: var(--font-family-sans);
}

.search-input:focus {
  outline: none;
  border-color: var(--accent-secondary);
  box-shadow: 0 0 0 2px rgba(47, 129, 247, 0.1);
}

.models-grid {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.model-card {
  border: 1px solid var(--border-default);
  border-radius: var(--radius-medium);
  padding: var(--space-3);
  cursor: pointer;
  transition: all 0.3s ease;
  background: var(--bg-tertiary);
}

.model-card:hover {
  border-color: var(--accent-secondary);
  background: var(--bg-overlay);
  transform: translateY(-1px);
  box-shadow: var(--shadow-medium);
}

.model-card.selected {
  border-color: var(--accent-primary);
  background: rgba(35, 134, 54, 0.1);
  box-shadow: 0 0 0 2px rgba(35, 134, 54, 0.2);
}

.model-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-2);
}

.model-name {
  margin: 0;
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--text-primary);
}

.model-version {
  font-size: 0.75rem;
  color: var(--text-secondary);
  background: var(--bg-overlay);
  padding: 2px 6px;
  border-radius: var(--radius-small);
  font-family: monospace;
}

.model-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: var(--space-2);
}

.architecture-label {
  font-size: 0.75rem;
  color: var(--accent-secondary);
  background: rgba(47, 129, 247, 0.1);
  padding: 2px 6px;
  border-radius: var(--radius-small);
  border: 1px solid rgba(47, 129, 247, 0.2);
}

.accuracy-score {
  font-size: 0.8rem;
  color: var(--accent-primary);
  font-weight: 600;
}

.selected-model-info {
  margin-top: var(--space-3);
  padding: var(--space-3);
  background: rgba(35, 134, 54, 0.1);
  border-radius: var(--radius-medium);
  border-left: 4px solid var(--accent-primary);
}

.selected-model-info h4 {
  margin: 0 0 var(--space-1) 0;
  font-size: 0.9rem;
  color: var(--accent-primary);
  font-weight: 600;
}

.selected-model-info p {
  margin: 0;
  font-size: 0.8rem;
  color: var(--text-secondary);
}

.model-details {
  margin-top: var(--space-1) !important;
}

.btn-retry {
  background: var(--accent-danger);
  color: white;
  border: none;
  padding: var(--space-2) var(--space-3);
  border-radius: var(--radius-medium);
  cursor: pointer;
  font-size: 0.8rem;
  margin-top: var(--space-2);
  font-family: var(--font-family-sans);
}

.btn-retry:hover {
  background: #d32f2f;
}

/* Button Styles */
.btn-secondary {
  background: var(--bg-tertiary);
  color: var(--text-primary);
  border: 1px solid var(--border-default);
  padding: var(--space-2) var(--space-4);
  border-radius: var(--radius-medium);
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 500;
  transition: all 0.2s ease;
  font-family: var(--font-family-sans);
  display: flex;
  align-items: center;
  gap: var(--space-1);
}

.btn-secondary:hover {
  background: var(--bg-overlay);
  border-color: var(--accent-secondary);
  transform: translateY(-1px);
}

/* Responsive Design */
@media (max-width: 768px) {
  .container {
    padding: var(--space-3);
  }
  
  .page-title {
    font-size: 2rem;
  }
  
  .parent {
    grid-template-columns: 1fr;
    grid-template-rows: auto auto 1fr;
    height: auto;
    min-height: auto;
    gap: var(--space-3);
  }
  
  .div1 { grid-area: 1 / 1 / 2 / 2; }
  .div2 { grid-area: 2 / 1 / 3 / 2; }
  .div3 { grid-area: 3 / 1 / 4 / 2; }
  
  .card {
    height: auto;
    min-height: 300px;
  }
  
  .upload-placeholder h4 {
    font-size: 1rem;
  }
  
  .predictions-grid {
    grid-template-columns: 1fr;
  }
  
  .summary-stats {
    grid-template-columns: 1fr;
  }
  
  .waveform-controls {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--space-2);
  }
  
  .legend-items {
    gap: var(--space-1);
  }
  
  .legend-item {
    font-size: 0.8rem;
  }
}

@media (max-width: 480px) {
  .page-title {
    font-size: 1.8rem;
  }
  
  .page-subtitle {
    font-size: 1rem;
  }
  
  .card-header {
    padding: var(--space-3);
  }
  
  .upload-area {
    padding: var(--space-3);
  }
}
</style>
