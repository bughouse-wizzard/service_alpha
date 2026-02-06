<template>
  <form @submit.prevent="submitSearch" class="space-y-4">
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <!-- Search Query -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">
          Search Query *
        </label>
        <input
          v-model="form.query"
          type="text"
          required
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Enter search terms..."
        />
      </div>
      
      <!-- Search Type -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">
          Search Type *
        </label>
        <select
          v-model="form.searchType"
          required
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="">Select type...</option>
          <option value="web">Web Search</option>
          <option value="database">Database Search</option>
          <option value="api">API Search</option>
          <option value="custom">Custom Search</option>
        </select>
      </div>
      
      <!-- Max Results -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">
          Max Results
        </label>
        <input
          v-model="form.maxResults"
          type="number"
          min="1"
          max="1000"
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="100"
        />
      </div>
      
      <!-- Priority -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">
          Priority
        </label>
        <select
          v-model="form.priority"
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="low">Low</option>
          <option value="medium" selected>Medium</option>
          <option value="high">High</option>
        </select>
      </div>
    </div>
    
    <!-- Advanced Options -->
    <div class="border-t pt-4">
      <button
        type="button"
        @click="showAdvanced = !showAdvanced"
        class="text-sm text-blue-500 hover:text-blue-700 flex items-center"
      >
        <span>{{ showAdvanced ? '▼' : '▶' }}</span>
        <span class="ml-2">Advanced Options</span>
      </button>
      
      <div v-if="showAdvanced" class="mt-4 grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Timeout (seconds)
          </label>
          <input
            v-model="form.timeout"
            type="number"
            min="10"
            max="3600"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="300"
          />
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Filters
          </label>
          <input
            v-model="form.filters"
            type="text"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="e.g., language:en, date:2024"
          />
        </div>
      </div>
    </div>
    
    <!-- Form Actions -->
    <div class="flex justify-end space-x-3 pt-4 border-t">
      <button
        type="button"
        @click="resetForm"
        class="px-4 py-2 border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50"
      >
        Reset
      </button>
      <button
        type="submit"
        :disabled="isSubmitting"
        class="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        <span v-if="isSubmitting">
          <i class="animate-spin mr-2">⟳</i> Starting...
        </span>
        <span v-else>
          <i class="mr-2">🔍</i> Start Search
        </span>
      </button>
    </div>
  </form>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'

const emit = defineEmits<{
  searchStarted: [searchId: string]
}>()

interface SearchForm {
  query: string
  searchType: string
  maxResults: number
  priority: string
  timeout: number
  filters: string
}

const form = reactive<SearchForm>({
  query: '',
  searchType: '',
  maxResults: 100,
  priority: 'medium',
  timeout: 300,
  filters: ''
})

const showAdvanced = ref(false)
const isSubmitting = ref(false)

const submitSearch = async () => {
  isSubmitting.value = true
  
  try {
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // Generate a mock search ID
    const searchId = `search_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
    
    // Emit event with search ID
    emit('searchStarted', searchId)
    
    // Reset form
    resetForm()
    
    console.log(`Search started with ID: ${searchId}`)
  } catch (error) {
    console.error('Failed to start search:', error)
  } finally {
    isSubmitting.value = false
  }
}

const resetForm = () => {
  form.query = ''
  form.searchType = ''
  form.maxResults = 100
  form.priority = 'medium'
  form.timeout = 300
  form.filters = ''
  showAdvanced.value = false
}
</script>