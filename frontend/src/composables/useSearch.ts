import { ref, computed } from 'vue'
import api, { SearchEventSource } from '../services/api'

// Use mock API for now since we don't have a real backend
const useMock = true
const searchService = useMock ? api.mock : api.real

export function useSearch() {
  const searches = ref<any[]>([])
  const currentSearch = ref<any>(null)
  const isLoading = ref(false)
  const error = ref<string | null>(null)
  
  const eventSource = ref<SearchEventSource | null>(null)
  const isConnected = ref(false)
  
  // Start a new search
  const startSearch = async (searchData: any) => {
    isLoading.value = true
    error.value = null
    
    try {
      const result = await searchService.startSearch(searchData)
      currentSearch.value = result
      
      // Connect to event stream for real-time updates
      connectToEventStream(result.id)
      
      // Refresh search history
      await loadSearchHistory()
      
      return result
    } catch (err: any) {
      error.value = err.message || 'Failed to start search'
      throw err
    } finally {
      isLoading.value = false
    }
  }
  
  // Load search history
  const loadSearchHistory = async (params?: any) => {
    isLoading.value = true
    error.value = null
    
    try {
      const result = await searchService.getSearchHistory(params)
      searches.value = result.searches || []
      return result
    } catch (err: any) {
      error.value = err.message || 'Failed to load search history'
      throw err
    } finally {
      isLoading.value = false
    }
  }
  
  // Get search by ID
  const getSearchById = async (searchId: string) => {
    isLoading.value = true
    error.value = null
    
    try {
      const result = await searchService.getSearchById(searchId)
      currentSearch.value = result
      return result
    } catch (err: any) {
      error.value = err.message || 'Failed to load search'
      throw err
    } finally {
      isLoading.value = false
    }
  }
  
  // Stop a search
  const stopSearch = async (searchId: string) => {
    isLoading.value = true
    error.value = null
    
    try {
      const result = await searchService.stopSearch(searchId)
      
      // Update local state
      const searchIndex = searches.value.findIndex(s => s.id === searchId)
      if (searchIndex !== -1) {
        searches.value[searchIndex].status = 'stopped'
      }
      
      if (currentSearch.value?.id === searchId) {
        currentSearch.value.status = 'stopped'
      }
      
      // Disconnect event stream
      disconnectEventStream()
      
      return result
    } catch (err: any) {
      error.value = err.message || 'Failed to stop search'
      throw err
    } finally {
      isLoading.value = false
    }
  }
  
  // Connect to event stream
  const connectToEventStream = (searchId: string) => {
    if (eventSource.value) {
      eventSource.value.disconnect()
    }
    
    eventSource.value = new api.EventSource()
    eventSource.value.connect(searchId)
    
    eventSource.value.on('connect', (data: any) => {
      console.log('Connected to event stream:', data)
      isConnected.value = true
    })
    
    eventSource.value.on('progress', (data: any) => {
      console.log('Progress update:', data)
      if (currentSearch.value?.id === searchId) {
        currentSearch.value.progress = data.progress
        currentSearch.value.status = data.status || currentSearch.value.status
      }
    })
    
    eventSource.value.on('result', (data: any) => {
      console.log('New result:', data)
      // Handle new result - could update a results store
    })
    
    eventSource.value.on('status', (data: any) => {
      console.log('Status update:', data)
      if (currentSearch.value?.id === searchId) {
        currentSearch.value.status = data.status
      }
    })
    
    eventSource.value.on('error', (data: any) => {
      console.error('Event stream error:', data)
      error.value = data.message || 'Event stream error'
    })
    
    eventSource.value.on('complete', (data: any) => {
      console.log('Search completed:', data)
      if (currentSearch.value?.id === searchId) {
        currentSearch.value.status = 'completed'
        currentSearch.value.progress = 100
      }
      disconnectEventStream()
    })
    
    eventSource.value.on('disconnect', () => {
      console.log('Disconnected from event stream')
      isConnected.value = false
    })
  }
  
  // Disconnect event stream
  const disconnectEventStream = () => {
    if (eventSource.value) {
      eventSource.value.disconnect()
      eventSource.value = null
      isConnected.value = false
    }
  }
  
  // Cleanup on unmount
  const cleanup = () => {
    disconnectEventStream()
  }
  
  // Computed properties
  const activeSearches = computed(() => {
    return searches.value.filter(s => s.status === 'running' || s.status === 'pending')
  })
  
  const completedSearches = computed(() => {
    return searches.value.filter(s => s.status === 'completed')
  })
  
  const failedSearches = computed(() => {
    return searches.value.filter(s => s.status === 'failed' || s.status === 'stopped')
  })
  
  return {
    // State
    searches,
    currentSearch,
    isLoading,
    error,
    isConnected,
    
    // Computed
    activeSearches,
    completedSearches,
    failedSearches,
    
    // Actions
    startSearch,
    loadSearchHistory,
    getSearchById,
    stopSearch,
    connectToEventStream,
    disconnectEventStream,
    cleanup
  }
}