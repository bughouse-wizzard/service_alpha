<template>
  <div>
    <!-- No Search Selected -->
    <div v-if="!searchId" class="text-center py-12">
      <div class="text-gray-400 mb-4">
        <svg class="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
      </div>
      <h3 class="text-lg font-medium text-gray-900 mb-2">No Search Selected</h3>
      <p class="text-gray-500">Select a search from the history or start a new search to view results.</p>
    </div>
    
    <!-- Search Results -->
    <div v-else>
      <!-- Search Info Header -->
      <div class="mb-6 p-4 bg-blue-50 rounded-lg">
        <div class="flex justify-between items-start">
          <div>
            <h4 class="font-medium text-gray-900">Search Results</h4>
            <div class="flex items-center mt-2 space-x-4 text-sm text-gray-600">
              <span>ID: <code class="font-mono bg-gray-100 px-1 rounded">{{ searchId.substring(0, 12) }}...</code></span>
              <span>Input Source: {{ currentSearch?.input_source || 'N/A' }}</span>
              <span>KTRU: {{ currentSearch?.ktru_code || 'N/A' }}</span>
              <span>Status: 
                <span :class="statusClass(currentSearch?.status || '')" class="px-2 py-0.5 rounded-full text-xs">
                  {{ currentSearch?.status || 'loading' }}
                </span>
              </span>
            </div>
          </div>
          <div class="text-right">
            <div class="text-2xl font-bold text-blue-600">{{ results.length.toLocaleString() }}</div>
            <div class="text-sm text-gray-500">Contracts Found</div>
          </div>
        </div>
        
        <!-- Progress Bar -->
        <div class="mt-4">
          <div class="flex justify-between text-sm text-gray-600 mb-1">
            <span>Progress</span>
            <span>{{ currentSearch?.contracts_processed || 0 }}/{{ currentSearch?.total_contracts_found || 0 }} contracts</span>
          </div>
          <div class="w-full bg-gray-200 rounded-full h-2.5">
            <div 
              class="bg-blue-600 h-2.5 rounded-full transition-all duration-300"
              :style="{ width: progress + '%' }"
            ></div>
          </div>
          <div class="mt-2 text-xs text-gray-500">
            <span v-if="isConnected" class="text-green-600 flex items-center">
              <span class="w-2 h-2 bg-green-500 rounded-full mr-1 animate-pulse"></span>
              Real-time updates connected
            </span>
            <span v-else class="text-red-600 flex items-center">
              <span class="w-2 h-2 bg-red-500 rounded-full mr-1"></span>
              Disconnected
            </span>
          </div>
        </div>
      </div>
      
      <!-- Results Table -->
      <div class="overflow-x-auto border rounded-lg">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th scope="col" class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                #
              </th>
              <th scope="col" class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Contract Link
              </th>
              <th scope="col" class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Contract Number
              </th>
              <th scope="col" class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Year
              </th>
              <th scope="col" class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Price per Unit
              </th>
              <th scope="col" class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Match Type
              </th>
              <th scope="col" class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Manufacturer
              </th>
              <th scope="col" class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                AI Score
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="(result, index) in results" :key="result.id" class="hover:bg-gray-50">
              <td class="px-4 py-3 whitespace-nowrap text-sm text-gray-500">
                {{ index + 1 }}
              </td>
              <td class="px-4 py-3">
                <a :href="result.source_url" target="_blank" class="text-blue-500 hover:text-blue-700 text-sm font-medium">
                  View Contract
                </a>
              </td>
              <td class="px-4 py-3 whitespace-nowrap text-sm text-gray-900">
                {{ result.reestr_number }}
              </td>
              <td class="px-4 py-3 whitespace-nowrap text-sm text-gray-900">
                {{ result.contract_year || 'N/A' }}
              </td>
              <td class="px-4 py-3 whitespace-nowrap text-sm text-gray-900">
                {{ formatCurrency(result.contract_price) }}
              </td>
              <td class="px-4 py-3 whitespace-nowrap">
                <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full"
                      :class="matchTypeClass(result.match_type)">
                  {{ result.match_type }}
                </span>
              </td>
              <td class="px-4 py-3 whitespace-nowrap text-sm text-gray-900">
                {{ result.supplier_name || 'N/A' }}
              </td>
              <td class="px-4 py-3 whitespace-nowrap">
                <div class="flex items-center">
                  <div class="w-16 bg-gray-200 rounded-full h-1.5 mr-2">
                    <div 
                      class="bg-green-500 h-1.5 rounded-full"
                      :style="{ width: result.ai_score + '%' }"
                    ></div>
                  </div>
                  <span class="text-sm text-gray-900">{{ Math.round(result.ai_score) }}%</span>
                </div>
              </td>
            </tr>
            
            <!-- Loading State -->
            <tr v-if="isLoading">
              <td colspan="8" class="px-4 py-8 text-center">
                <div class="flex justify-center items-center">
                  <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-500"></div>
                  <span class="ml-2 text-gray-500">Loading contract results...</span>
                </div>
              </td>
            </tr>
            
            <!-- Empty Results -->
            <tr v-else-if="results.length === 0">
              <td colspan="8" class="px-4 py-8 text-center text-gray-500">
                No contract results yet. Results will appear here as they are found.
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <!-- Event Log -->
      <div class="mt-6">
        <h5 class="text-sm font-medium text-gray-700 mb-2">Event Log</h5>
        <div class="bg-gray-50 rounded-lg p-4 max-h-48 overflow-y-auto">
          <div v-for="(event, index) in events" :key="index" class="text-sm font-mono mb-1">
            <span class="text-gray-500">[{{ formatTime(event.timestamp) }}]</span>
            <span :class="eventClass(event.type)" class="ml-2">{{ event.message }}</span>
          </div>
          <div v-if="events.length === 0" class="text-gray-400 text-sm">
            No events yet. Events will appear here as they occur.
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onUnmounted } from 'vue'
import api from "../services/api"

interface Props {
  searchId?: string | null
}

const props = defineProps<Props>()

interface ContractResult {
  id: string
  reestr_number: string
  contract_number: string
  contract_date: string | null
  contract_year: string | null
  match_type: string
  ai_score: number
  supplier_name: string | null
  customer_name: string | null
  contract_price: number | null
  currency: string
  source_system: string
  source_url: string
  scraped_at: string
}

interface SearchEvent {
  type: 'info' | 'warning' | 'error' | 'result' | 'progress' | 'status'
  message: string
  timestamp: number
  data?: any
}

interface SearchInfo {
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

const results = ref<ContractResult[]>([])
const events = ref<SearchEvent[]>([])
const currentSearch = ref<SearchInfo | null>(null)
const isLoading = ref(false)
const isConnected = ref(false)
const eventSource = ref<EventSource | null>(null)

const progress = computed(() => {
  if (!currentSearch.value || currentSearch.value.total_contracts_found === 0) return 0
  return (currentSearch.value.contracts_processed / currentSearch.value.total_contracts_found) * 100
})

// Mock data generator
const generateMockResult = (index: number): ContractResult => ({
  id: `contract_${Date.now()}_${index}`,
  reestr_number: `0123456789${index}`,
  contract_number: `CTR-2024-${String(index + 1).padStart(3, '0')}`,
  contract_date: '2024-01-15',
  contract_year: '2024',
  match_type: ['EXACT', 'PARTIAL', 'SIMILAR', 'NO_MATCH'][Math.floor(Math.random() * 4)],
  ai_score: Math.floor(Math.random() * 100),
  supplier_name: ['ООО "ТехноПром"', 'АО "Электросила"', 'ЗАО "МеталлСервис"'][Math.floor(Math.random() * 3)],
  customer_name: 'Государственное учреждение',
  contract_price: Math.floor(Math.random() * 1000000) + 10000,
  currency: 'RUB',
  source_system: 'zakupki.gov.ru',
  source_url: `https://zakupki.gov.ru/epz/order/notice/ea44/view/common-info.html?regNumber=0123456789${index}`,
  scraped_at: new Date().toISOString()
})

const generateMockEvent = (type: SearchEvent['type'], message: string, data?: any): SearchEvent => ({
  type,
  message,
  timestamp: Date.now(),
  data
})

// Watch for searchId changes
watch(() => props.searchId, (newSearchId, oldSearchId) => {
  if (newSearchId !== oldSearchId) {
    resetView()
    if (newSearchId) {
      loadSearchInfo(newSearchId)
      connectToEventStream(newSearchId)
    }
  }
}, { immediate: true })

const resetView = () => {
  results.value = []
  events.value = []
  currentSearch.value = null
  isLoading.value = false
  isConnected.value = false
  
  if (eventSource.value) {
    eventSource.value.close()
    eventSource.value = null
  }
}

const loadSearchInfo = async (searchId: string) => {
  isLoading.value = true
  try {
    // Call the API to get search info
    const searchInfo = await api.real.getSearchById(searchId)
    currentSearch.value = searchInfo
    
    // Add initial events
    events.value = [
      generateMockEvent('info', `Search started: ${searchInfo.input_source}`),
      generateMockEvent('info', `KTRU Code: ${searchInfo.ktru_code || 'Not specified'}`),
      generateMockEvent('status', `Status: ${searchInfo.status}`),
      generateMockEvent('progress', `Processed ${searchInfo.contracts_processed}/${searchInfo.total_contracts_found} contracts`)
    ]
    
    // TODO: In a real implementation, we would fetch contract results from the backend
    // For now, add mock results for demonstration
    for (let i = 0; i < Math.min(5, searchInfo.limit_contracts); i++) {
      results.value.push(generateMockResult(i))
    }
    
  } catch (error) {
    console.error('Failed to load search info:', error)
    events.value.push(generateMockEvent('error', 'Failed to load search information'))
    
    // Fall back to mock data
    try {
      const mockInfo = await api.mock.getSearchById(searchId)
      currentSearch.value = mockInfo
    } catch (mockError) {
      console.error('Failed to load mock data:', mockError)
    }
  } finally {
    isLoading.value = false
  }
}

const connectToEventStream = (searchId: string) => {
  // Use the EventSource from the API service
  const searchEventSource = new api.EventSource()
  
  searchEventSource.connect(searchId)
  
  searchEventSource.on('connect', (data: any) => {
    isConnected.value = true
    events.value.unshift(generateMockEvent('info', 'Connected to real-time updates', data))
  })
  
  searchEventSource.on('progress', (data: any) => {
    events.value.unshift(generateMockEvent('progress', `Progress: ${data.processed_count}/${data.total} contracts`, data))
    
    // Update current search progress
    if (currentSearch.value) {
      currentSearch.value.contracts_processed = data.processed_count
      currentSearch.value.total_contracts_found = data.total
    }
  })
  
  searchEventSource.on('status', (data: any) => {
    events.value.unshift(generateMockEvent('status', `Status: ${data.status}`, data))
    
    // Update current search status
    if (currentSearch.value && data.status) {
      currentSearch.value.status = data.status.toUpperCase()
    }
  })
  
  searchEventSource.on('result', (data: any) => {
    events.value.unshift(generateMockEvent('result', 'New contract result found', data))
    
    // Add the new result to the results list
    // Note: In a real implementation, data would contain the contract result
    // For now, we'll add a mock result
    const newResult = generateMockResult(results.value.length)
    results.value.unshift(newResult)
  })
  
  searchEventSource.on('error', (data: any) => {
    events.value.unshift(generateMockEvent('error', `Error: ${data.error || 'Unknown error'}`, data))
  })
  
  searchEventSource.on('complete', (data: any) => {
    events.value.unshift(generateMockEvent('info', 'Search completed', data))
    isConnected.value = false
    
    // Update current search status
    if (currentSearch.value) {
      currentSearch.value.status = 'COMPLETED'
    }
  })
  
  searchEventSource.on('disconnect', () => {
    isConnected.value = false
    events.value.unshift(generateMockEvent('info', 'Disconnected from real-time updates'))
  })
  
  // Store the event source for cleanup
  eventSource.value = searchEventSource as any
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

const matchTypeClass = (matchType: string) => {
  const classes: Record<string, string> = {
    'EXACT': 'bg-green-100 text-green-800',
    'PARTIAL': 'bg-yellow-100 text-yellow-800',
    'SIMILAR': 'bg-blue-100 text-blue-800',
    'NO_MATCH': 'bg-gray-100 text-gray-800'
  }
  return classes[matchType] || 'bg-gray-100 text-gray-800'
}

const eventClass = (type: string) => {
  const classes: Record<string, string> = {
    info: 'text-blue-600',
    warning: 'text-yellow-600',
    error: 'text-red-600',
    result: 'text-green-600',
    progress: 'text-purple-600',
    status: 'text-indigo-600'
  }
  return classes[type] || 'text-gray-600'
}

const formatTime = (timestamp: number) => {
  const date = new Date(timestamp)
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' })
}

const formatCurrency = (amount: number | null) => {
  if (amount === null) return 'N/A'
  return new Intl.NumberFormat('ru-RU', {
    style: 'currency',
    currency: 'RUB',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  }).format(amount)
}

// Cleanup on component unmount
onUnmounted(() => {
  if (eventSource.value) {
    // The EventSource class has a disconnect method
    if ('disconnect' in eventSource.value && typeof eventSource.value.disconnect === 'function') {
      eventSource.value.disconnect()
    }
  }
})
</script>