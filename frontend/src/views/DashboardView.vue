<template>
  <div class="space-y-6">
    <!-- New Search Form -->
    <div class="bg-white rounded-lg shadow p-6">
      <h3 class="text-lg font-semibold mb-4">New Search</h3>
      <new-search-form @search-started="handleSearchStarted" />
    </div>
    
    <!-- Two Column Layout for History and Results -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Search History -->
      <div class="bg-white rounded-lg shadow p-6">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-lg font-semibold">Search History</h3>
          <button class="text-sm text-blue-500 hover:text-blue-700">Refresh</button>
        </div>
        <search-history-table @select-search="handleSelectSearch" />
      </div>
      
      <!-- Results View -->
      <div class="bg-white rounded-lg shadow p-6">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-lg font-semibold">Search Results</h3>
          <div v-if="activeSearchId" class="flex space-x-2">
            <button 
              @click="stopSearch" 
              class="px-3 py-1 bg-red-500 text-white text-sm rounded hover:bg-red-600"
            >
              Stop
            </button>
            <button class="px-3 py-1 bg-gray-200 text-gray-700 text-sm rounded hover:bg-gray-300">
              Export
            </button>
          </div>
        </div>
        <search-results-view :search-id="activeSearchId" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import NewSearchForm from '../components/NewSearchForm.vue'
import SearchHistoryTable from '../components/SearchHistoryTable.vue'
import SearchResultsView from '../components/SearchResultsView.vue'

const activeSearchId = ref<string | null>(null)

const handleSearchStarted = (searchId: string) => {
  activeSearchId.value = searchId
}

const handleSelectSearch = (searchId: string) => {
  activeSearchId.value = searchId
}

const stopSearch = () => {
  if (activeSearchId.value) {
    // API call to stop search would go here
    console.log(`Stopping search ${activeSearchId.value}`)
    // For now, just clear the active search
    activeSearchId.value = null
  }
}
</script>