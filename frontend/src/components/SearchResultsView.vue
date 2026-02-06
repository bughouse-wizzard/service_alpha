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
            <h4 class="font-medium text-gray-900">Search: {{ currentSearch?.query || 'Loading...' }}</h4>
            <div class="flex items-center mt-2 space-x-4 text-sm text-gray-600">
              <span>ID: <code class="font-mono bg-gray-100 px-1 rounded">{{ searchId.substring(0, 12) }}...</code></span>
              <span>Type: {{ currentSearch?.type || 'N/A' }}</span>
              <span>Status: 
                <span :class="statusClass(currentSearch?.status || '')" class="px-2 py-0.5 rounded-full text-xs">
                  {{ currentSearch?.status || 'loading' }}
                </span>
              </span>
            </div>
          </div>
          <div class="text-right">
            <div class="text-2xl font-bold text-blue-600">{{ results.length.toLocaleString() }}</div>
            <div class="text-sm text-gray-500">Results Found</div>
          </div>
        </div>
        
        <!-- Progress Bar -->
        <div class="mt-4">
          <div class="flex justify-between text-sm text-gray-600 mb-1">
            <span>Progress</span>
            <span>{{ progress }}%</span>
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
                Title
              </th>
              <th scope="col" class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Source
              </th>
              <th scope="col" class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Relevance
              </th>
              <th scope="col" class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Found At
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="(result, index) in results" :key="result.id" class="hover:bg-gray-50">
              <td class="px-4 py-3 whitespace-nowrap text-sm text-gray-500">
                {{ index + 1 }}
              </td>
              <td class="px-4 py-3">
                <div class="text-sm font-medium text-gray-900">{{ result.title }}</div>
                <div class="text-sm text-gray-500 truncate max-w-md">{{ result.snippet }}</div>
              </td>
              <td class="px-4 py-3 whitespace-nowrap">
                <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-gray-100 text-gray-800">
                  {{ result.source }}
                </span>
              </td>
              <td class="px-4 py-3 whitespace-nowrap">
                <div class="flex items-center">
                  <div class="w-16 bg-gray-200 rounded-full h-1.5 mr-2">
                    <div 
                      class="bg-green-500 h-1.5 rounded-full"
                      :style="{ width: (result.relevance * 100) + '%' }"
                    ></div>
                  </div>
                  <span class="text-sm text-gray-900">{{ Math.round(result.relevance * 100) }}%</span>
                </div>
              </td>
              <td class="px-4 py-3 whitespace-nowrap text-sm text-gray-500">
                {{ formatTime(result.timestamp) }}
              </td>
            </tr>
            
            <!-- Loading State -->
            <tr v-if="isLoading">
              <td colspan="5" class="px-4 py-8 text-center">
                <div class="flex justify-center items-center">
                  <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-500"></div>
                  <span class="ml-2 text-gray-500">Loading results...</span>
                </div>
              </td>
            </tr>
            
            <!-- Empty Results -->
            <tr v-else-if="results.length === 0">
              <td colspan="5" class="px-4 py-8 text-center text-gray-500">
                No results yet. Results will appear here as they are found.
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

interface Props {
  searchId?: string | null
}

const props = defineProps<Props>()

interface SearchResult {
  id: string
  title: string
  snippet: string
  source: string
  relevance: number
  timestamp: number
}

interface SearchEvent {
  type: 'info' | 'warning' | 'error' | 'result' | 'progress'
  message: string
  timestamp: number
  data?: any
}

interface SearchInfo {
  query: string
  type: string
  status: string
  progress: number
}

const results = ref<SearchResult[]>([])
const events = ref<SearchEvent[]>([])
const currentSearch = ref<SearchInfo | null>(null)
const isLoading = ref(false)
const isConnected = ref(false)
const eventSource = ref<EventSource | null>(null)

const progress = computed(() => {
  return currentSearch.value?.progress || 0
})

// Mock data generator
const generateMockResult = (index: number): SearchResult => ({
  id: `result_${Date.now()}_${index}`,
  title: `Search Result ${index + 1}: Example Title`,
  snippet: 'This is a sample search result snippet that shows relevant content from the source.',
  source: ['web', 'database', 'api'][Math.floor(Math.random() * 3)],
  relevance: Math.random(),
  timestamp: Date.now() - Math.random() * 60000
})

const generateMockEvent = (type: SearchEvent['type'], message: string): SearchEvent => ({
  type,
  message,
  timestamp: Date.now(),
  data: {}
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
    // Simulate API call to get search info
    await new Promise(resolve => setTimeout(resolve, 500))
    
    currentSearch.value = {
      query: 'Example search query',
      type: 'web',
      status: 'running',
      progress: 25
    }
    
    // Add initial mock results for demonstration
    for (let i = 0; i < 5; i++) {
      results.value.push(generateMockResult(i))
    }
    
    // Add initial events
    events.value = [
      generateMockEvent('info', 'Search started'),
      generateMockEvent('info', 'Connected to data sources'),
      generateMockEvent('result', 'Found 5 initial results'),
      generateMockEvent('progress', 'Processing 25% complete')
    ]
  } catch (error) {
    console.error('Failed to load search info:', error)
    events.value.push(generateMockEvent('error', 'Failed to load search information'))
  } finally {
    isLoading.value = false
  }
}

const connectToEventStream = (searchId: string) => {
  // In a real implementation, this would connect to /api/search/{id}/events
  // For now, simulate the connection with mock events
  
  isConnected.value = true
  
  // Simulate EventSource connection
  const simulateEventStream = () => {
    if (!props.searchId || props.searchId !== searchId) return
    
    // Simulate receiving events
    const eventTypes: SearchEvent['type'][] = ['info', 'result', 'progress', 'warning']
    const eventMessages = [
      'Processing batch of results',
      'Found new matching document',
      'Updated search progress',
      'Connected to additional data source',
      'Filtering results by relevance',
      'Exporting intermediate results'
    ]
    
    const interval = setInterval(() => {
      if (!props.searchId || props.searchId !== searchId) {
        clearInterval(interval)
        return
      }
      
      const type = eventTypes[Math.floor(Math.random() * eventTypes.length)]
      const message = eventMessages[Math.floor(Math.random() * eventMessages.length)]
      
      const event = generateMockEvent(type, message)
      events.value.unshift(event)
      
      // Keep only last 20 events
      if (events.value.length > 20) {
        events.value = events.value.slice(0, 20)
      }
      
      // Occasionally add a new result
      if (type === 'result' && Math.random() > 0.7) {
        const newResult = generateMockResult(results.value.length)
        results.value.unshift(newResult)
        
        // Update progress
        if (currentSearch.value) {
          currentSearch.value.progress = Math.min(100, currentSearch.value.progress + 5)
          if (currentSearch.value.progress >= 100) {
            currentSearch.value.status = 'completed'
            clearInterval(interval)
            isConnected.value = false
            events.value.unshift(generateMockEvent('info', 'Search completed successfully'))
          }
        }
      }
      
      // Update progress
      if (type === 'progress' && currentSearch.value) {
        currentSearch.value.progress = Math.min(100, currentSearch.value.progress + 1)
      }
      
    }, 2000 + Math.random() * 3000)
    
    // Cleanup on unmount or search change
    onUnmounted(() => {
      clearInterval(interval)
    })
  }
  
  simulateEventStream()
}

const statusClass = (status: string) => {
  const classes: Record<string, string> = {
    pending: 'bg-yellow-100 text-yellow-800',
    running: 'bg-blue-100 text-blue-800',
    completed: 'bg-green-100 text-green-800',
    failed: 'bg-red-100 text-red-800',
    stopped: 'bg-gray-100 text-gray-800'
  }
  return classes[status] || 'bg-gray-100 text-gray-800'
}

const eventClass = (type: string) => {
  const classes: Record<string, string> = {
    info: 'text-blue-600',
    warning: 'text-yellow-600',
    error: 'text-red-600',
    result: 'text-green-600',
    progress: 'text-purple-600'
  }
  return classes[type] || 'text-gray-600'
}

const formatTime = (timestamp: number) => {
  const date = new Date(timestamp)
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' })
}

// Cleanup on component unmount
onUnmounted(() => {
  if (eventSource.value) {
    eventSource.value.close()
  }
})
</script>