<template>
  <div class="overflow-x-auto">
    <table class="min-w-full divide-y divide-gray-200">
      <thead class="bg-gray-50">
        <tr>
          <th scope="col" class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
            ID
          </th>
          <th scope="col" class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
            Input Source
          </th>
          <th scope="col" class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
            KTRU Code
          </th>
          <th scope="col" class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
            Status
          </th>
          <th scope="col" class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
            Contracts
          </th>
          <th scope="col" class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
            Created
          </th>
          <th scope="col" class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
            Actions
          </th>
        </tr>
      </thead>
      <tbody class="bg-white divide-y divide-gray-200">
        <tr 
          v-for="search in searches" 
          :key="search.id"
          class="hover:bg-gray-50 cursor-pointer"
          @click="selectSearch(search.id)"
        >
          <td class="px-4 py-3 whitespace-nowrap text-sm font-mono text-gray-900">
            {{ search.id.substring(0, 8) }}...
          </td>
          <td class="px-4 py-3 text-sm text-gray-900 max-w-xs truncate">
            {{ search.input_source }}
          </td>
          <td class="px-4 py-3 whitespace-nowrap text-sm text-gray-900">
            {{ search.ktru_code || '-' }}
          </td>
          <td class="px-4 py-3 whitespace-nowrap">
            <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full"
                  :class="statusClass(search.status)">
              {{ search.status }}
            </span>
          </td>
          <td class="px-4 py-3 whitespace-nowrap text-sm text-gray-900">
            {{ search.contracts_processed }}/{{ search.total_contracts_found }}
          </td>
          <td class="px-4 py-3 whitespace-nowrap text-sm text-gray-500">
            {{ formatDate(search.created_at) }}
          </td>
          <td class="px-4 py-3 whitespace-nowrap text-sm font-medium">
            <button 
              @click.stop="viewSearch(search.id)"
              class="text-blue-500 hover:text-blue-700 mr-3"
            >
              View
            </button>
            <button 
              v-if="search.status === 'RUNNING'"
              @click.stop="stopSearch(search.id)"
              class="text-red-500 hover:text-red-700"
            >
              Stop
            </button>
          </td>
        </tr>
        
        <!-- Loading State -->
        <tr v-if="isLoading">
          <td colspan="7" class="px-4 py-8 text-center">
            <div class="flex justify-center items-center">
              <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-500"></div>
              <span class="ml-2 text-gray-500">Loading search history...</span>
            </div>
          </td>
        </tr>
        
        <!-- Empty State -->
        <tr v-else-if="searches.length === 0">
          <td colspan="7" class="px-4 py-8 text-center text-gray-500">
            No search history found. Start a new search to see results here.
          </td>
        </tr>
      </tbody>
    </table>
    
    <!-- Pagination -->
    <div v-if="searches.length > 0" class="flex items-center justify-between border-t border-gray-200 px-4 py-3">
      <div class="flex-1 flex justify-between sm:hidden">
        <button 
          @click="prevPage"
          :disabled="currentPage === 1"
          class="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50"
        >
          Previous
        </button>
        <button 
          @click="nextPage"
          :disabled="currentPage === totalPages"
          class="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50"
        >
          Next
        </button>
      </div>
      <div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
        <div>
          <p class="text-sm text-gray-700">
            Showing <span class="font-medium">{{ startItem }}</span> to <span class="font-medium">{{ endItem }}</span> of{' '}
            <span class="font-medium">{{ totalItems }}</span> results
          </p>
        </div>
        <div>
          <nav class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px" aria-label="Pagination">
            <button 
              @click="prevPage"
              :disabled="currentPage === 1"
              class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50"
            >
              <span class="sr-only">Previous</span>
              &larr;
            </button>
            <button 
              v-for="page in visiblePages"
              :key="page"
              @click="goToPage(page)"
              :class="[
                'relative inline-flex items-center px-4 py-2 border text-sm font-medium',
                page === currentPage 
                  ? 'z-10 bg-blue-50 border-blue-500 text-blue-600' 
                  : 'bg-white border-gray-300 text-gray-500 hover:bg-gray-50'
              ]"
            >
              {{ page }}
            </button>
            <button 
              @click="nextPage"
              :disabled="currentPage === totalPages"
              class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50"
            >
              <span class="sr-only">Next</span>
              &rarr;
            </button>
          </nav>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import api from "../services/api"

const emit = defineEmits<{
  selectSearch: [searchId: string]
}>()

interface SearchItem {
  id: string
  input_source: string
  ktru_code: string | null
  status: string
  limit_contracts: number
  region_filter: string | null
  technical_specification: string | null
  total_contracts_found: number
  contracts_processed: number
  created_at: string
  updated_at: string
}

const searches = ref<SearchItem[]>([])
const isLoading = ref(true)
const currentPage = ref(1)
const itemsPerPage = 10
const totalItems = ref(0)

onMounted(async () => {
  await loadSearches()
})

const loadSearches = async () => {
  isLoading.value = true
  try {
    // Call the API to get search history
    const params = {
      skip: (currentPage.value - 1) * itemsPerPage,
      limit: itemsPerPage
    }
    
    const data = await api.real.getSearchHistory(params)
    searches.value = data
    totalItems.value = data.length // Note: backend returns all items, not paginated
  } catch (error) {
    console.error('Failed to load search history:', error)
    // Fall back to mock data if real API fails
    try {
      const mockData = await api.mock.getSearchHistory()
      searches.value = mockData
      totalItems.value = mockData.length
    } catch (mockError) {
      console.error('Failed to load mock data:', mockError)
    }
  } finally {
    isLoading.value = false
  }
}

const statusClass = (status: string) => {
  const classes: Record<string, string> = {
    'PENDING': 'bg-yellow-100 text-yellow-800',
    'RUNNING': 'bg-blue-100 text-blue-800',
    'COMPLETED': 'bg-green-100 text-green-800',
    'FAILED': 'bg-red-100 text-red-800',
    'STOPPED': 'bg-gray-100 text-gray-800',
    'PROCESSING': 'bg-blue-100 text-blue-800',
    'CANCELLED': 'bg-gray-100 text-gray-800'
  }
  return classes[status] || 'bg-gray-100 text-gray-800'
}

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

const selectSearch = (searchId: string) => {
  emit('selectSearch', searchId)
}

const viewSearch = (searchId: string) => {
  console.log('View search:', searchId)
  selectSearch(searchId)
}

const stopSearch = async (searchId: string) => {
  if (confirm('Are you sure you want to stop this search?')) {
    try {
      // Call the API to stop the search
      await api.real.stopSearch(searchId)
      
      // Update local state
      const search = searches.value.find(s => s.id === searchId)
      if (search) {
        search.status = 'STOPPED'
      }
      
      console.log(`Search ${searchId} stopped successfully`)
    } catch (error) {
      console.error('Failed to stop search:', error)
      alert('Failed to stop search. Please check the console for details.')
    }
  }
}

// Pagination calculations
const totalPages = computed(() => Math.ceil(totalItems.value / itemsPerPage))
const startItem = computed(() => (currentPage.value - 1) * itemsPerPage + 1)
const endItem = computed(() => Math.min(currentPage.value * itemsPerPage, totalItems.value))

const visiblePages = computed(() => {
  const pages = []
  const maxVisible = 5
  let start = Math.max(1, currentPage.value - Math.floor(maxVisible / 2))
  let end = Math.min(totalPages.value, start + maxVisible - 1)
  
  if (end - start + 1 < maxVisible) {
    start = Math.max(1, end - maxVisible + 1)
  }
  
  for (let i = start; i <= end; i++) {
    pages.push(i)
  }
  
  return pages
})

const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--
    loadSearches()
  }
}

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
    loadSearches()
  }
}

const goToPage = (page: number) => {
  if (page >= 1 && page <= totalPages.value && page !== currentPage.value) {
    currentPage.value = page
    loadSearches()
  }
}
</script>