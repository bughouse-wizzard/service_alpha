<template>
  <form @submit.prevent="submitSearch" class="space-y-4">
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <!-- Input Source -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">
          Input Source *
        </label>
        <select
          v-model="form.input_source"
          required
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="">Select source...</option>
          <option value="zakupki.gov.ru">Zakupki.gov.ru</option>
          <option value="custom">Custom Source</option>
        </select>
      </div>
      
      <!-- KTRU Code -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">
          KTRU Code
        </label>
        <input
          v-model="form.ktru_code"
          type="text"
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="e.g., 34.12.11.110"
        />
      </div>
      
      <!-- Limit Contracts -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">
          Limit Contracts
        </label>
        <input
          v-model="form.limit_contracts"
          type="number"
          min="1"
          max="1000"
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="10"
        />
      </div>
      
      <!-- Region Filter -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">
          Region Filter
        </label>
        <input
          v-model="form.region_filter"
          type="text"
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="e.g., 77 for Moscow"
        />
      </div>
    </div>
    
    <!-- Technical Specification -->
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-1">
        Technical Specification *
      </label>
      <textarea
        v-model="form.technical_specification"
        required
        rows="4"
        class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        placeholder="Enter technical specification text for comparison..."
      ></textarea>
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
        <!-- Date Range -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Date From
          </label>
          <input
            v-model="form.date_from"
            type="date"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Date To
          </label>
          <input
            v-model="form.date_to"
            type="date"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        
        <!-- Price Range -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Price Min
          </label>
          <input
            v-model="form.price_min"
            type="number"
            min="0"
            step="0.01"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Minimum price"
          />
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Price Max
          </label>
          <input
            v-model="form.price_max"
            type="number"
            min="0"
            step="0.01"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Maximum price"
          />
        </div>
        
        <!-- NMC Value -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            NMC Value
          </label>
          <input
            v-model="form.nmc_value"
            type="number"
            min="0"
            step="0.01"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="NMC value threshold"
          />
        </div>
        
        <!-- Confidence Threshold -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Confidence Threshold
          </label>
          <input
            v-model="form.confidence_threshold"
            type="number"
            min="0"
            max="1"
            step="0.01"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="0.7"
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
import api from "../services/api"

const emit = defineEmits<{
  searchStarted: [searchId: string]
}>()

interface SearchForm {
  input_source: string
  ktru_code: string
  limit_contracts: number
  region_filter: string
  technical_specification: string
  date_from: string
  date_to: string
  price_min: number | null
  price_max: number | null
  nmc_value: number | null
  confidence_threshold: number
}

const form = reactive<SearchForm>({
  input_source: 'zakupki.gov.ru',
  ktru_code: '',
  limit_contracts: 10,
  region_filter: '',
  technical_specification: '',
  date_from: '',
  date_to: '',
  price_min: null,
  price_max: null,
  nmc_value: null,
  confidence_threshold: 0.7
})

const showAdvanced = ref(false)
const isSubmitting = ref(false)

const submitSearch = async () => {
  isSubmitting.value = true
  
  try {
    // Prepare data for API call
    const searchData = {
      input_source: form.input_source,
      ktru_code: form.ktru_code || null,
      limit_contracts: form.limit_contracts,
      region_filter: form.region_filter || null,
      technical_specification: form.technical_specification || null,
      date_from: form.date_from || null,
      date_to: form.date_to || null,
      price_min: form.price_min || null,
      price_max: form.price_max || null,
      nmc_value: form.nmc_value || null,
      confidence_threshold: form.confidence_threshold
    }
    
    // Call the API
    const response = await api.real.startSearch(searchData)
    
    // Emit event with search ID
    emit('searchStarted', response.id)
    
    // Reset form
    resetForm()
    
    console.log(`Search started with ID: ${response.id}`)
  } catch (error) {
    console.error('Failed to start search:', error)
    alert('Failed to start search. Please check the console for details.')
  } finally {
    isSubmitting.value = false
  }
}

const resetForm = () => {
  form.input_source = 'zakupki.gov.ru'
  form.ktru_code = ''
  form.limit_contracts = 10
  form.region_filter = ''
  form.technical_specification = ''
  form.date_from = ''
  form.date_to = ''
  form.price_min = null
  form.price_max = null
  form.nmc_value = null
  form.confidence_threshold = 0.7
  showAdvanced.value = false
}
</script>