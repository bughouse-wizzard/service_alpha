import axios from 'axios'

// API base URL - would be configured based on environment
const API_BASE_URL = (import.meta as any).env?.VITE_API_URL || 'http://localhost:50600'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor for adding auth tokens if needed
api.interceptors.request.use(
  (config) => {
    // Add authentication token if available
    const token = localStorage.getItem('auth_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor for handling errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.status, error.response?.data)
    
    // Handle specific error cases
    if (error.response?.status === 401) {
      // Unauthorized - redirect to login
      localStorage.removeItem('auth_token')
      window.location.href = '/login'
    }
    
    return Promise.reject(error)
  }
)

// Search API
export const searchApi = {
  // Start a new search
  startSearch: async (data: {
    input_source: string
    ktru_code?: string | null
    limit_contracts?: number
    region_filter?: string | null
    technical_specification?: string | null
    date_from?: string | null
    date_to?: string | null
    price_min?: number | null
    price_max?: number | null
    nmc_value?: number | null
    confidence_threshold?: number
  }) => {
    const response = await api.post('/api/search', data)
    return response.data
  },
  
  // Get search history
  getSearchHistory: async (params?: {
    skip?: number
    limit?: number
  }) => {
    const response = await api.get('/api/searches', { params })
    return response.data
  },
  
  // Get specific search by ID
  getSearchById: async (searchId: string) => {
    const response = await api.get(`/api/search/${searchId}`)
    return response.data
  },
  
  // Stop a running search
  stopSearch: async (searchId: string) => {
    const response = await api.post(`/api/search/${searchId}/stop`)
    return response.data
  },
  
  // Get search results
  getSearchResults: async (searchId: string, params?: {
    page?: number
    limit?: number
    sortBy?: string
  }) => {
    const response = await api.get(`/api/search/${searchId}/results`, { params })
    return response.data
  },
  
  // Export search results
  exportSearchResults: async (searchId: string, format: 'json' | 'csv' | 'excel') => {
    const response = await api.get(`/api/search/${searchId}/export`, {
      params: { format },
      responseType: 'blob'
    })
    return response.data
  }
}

// Event Source for real-time updates
export class SearchEventSource {
  private eventSource: EventSource | null = null
  private listeners: Map<string, Function[]> = new Map()
  
  connect(searchId: string) {
    if (this.eventSource) {
      this.disconnect()
    }
    
    const eventSourceUrl = `${API_BASE_URL}/api/search/${searchId}/events`
    this.eventSource = new EventSource(eventSourceUrl)
    
    this.eventSource.onopen = () => {
      this.emit('connect', { searchId })
    }
    
    this.eventSource.onerror = (error) => {
      this.emit('error', { error })
    }
    
    // Listen for different event types
    this.eventSource.addEventListener('progress', (event: MessageEvent) => {
      const data = JSON.parse(event.data)
      this.emit('progress', data)
    })
    
    this.eventSource.addEventListener('result', (event: MessageEvent) => {
      const data = JSON.parse(event.data)
      this.emit('result', data)
    })
    
    this.eventSource.addEventListener('status', (event: MessageEvent) => {
      const data = JSON.parse(event.data)
      this.emit('status', data)
    })
    
    this.eventSource.addEventListener('error', (event: MessageEvent) => {
      const data = JSON.parse(event.data)
      this.emit('error', data)
    })
    
    this.eventSource.addEventListener('complete', (event: MessageEvent) => {
      const data = JSON.parse(event.data)
      this.emit('complete', data)
    })
  }
  
  disconnect() {
    if (this.eventSource) {
      this.eventSource.close()
      this.eventSource = null
      this.emit('disconnect', {})
    }
  }
  
  on(event: string, callback: Function) {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, [])
    }
    this.listeners.get(event)!.push(callback)
  }
  
  off(event: string, callback: Function) {
    if (this.listeners.has(event)) {
      const callbacks = this.listeners.get(event)!
      const index = callbacks.indexOf(callback)
      if (index > -1) {
        callbacks.splice(index, 1)
      }
    }
  }
  
  private emit(event: string, data: any) {
    if (this.listeners.has(event)) {
      this.listeners.get(event)!.forEach(callback => {
        try {
          callback(data)
        } catch (error) {
          console.error(`Error in event listener for ${event}:`, error)
        }
      })
    }
  }
  
  isConnected(): boolean {
    return this.eventSource !== null && this.eventSource.readyState === EventSource.OPEN
  }
}

// Mock API for development (when backend is not available)
export const mockApi = {
  startSearch: async (data: any) => {
    await new Promise(resolve => setTimeout(resolve, 1000))
    return {
      id: `search_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      ...data,
      status: 'RUNNING',
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
      contracts_processed: 0,
      total_contracts_found: 0
    }
  },
  
  getSearchHistory: async (params?: any) => {
    await new Promise(resolve => setTimeout(resolve, 800))
    const mockSearches = [
      {
        id: 'search_1707234567890_abc123',
        input_source: 'zakupki.gov.ru',
        ktru_code: '34.12.11.110',
        status: 'COMPLETED',
        limit_contracts: 10,
        region_filter: '77',
        technical_specification: 'Technical spec example 1',
        total_contracts_found: 245,
        contracts_processed: 245,
        created_at: '2024-02-05T10:30:00Z',
        updated_at: '2024-02-05T10:45:00Z'
      },
      {
        id: 'search_1707234567891_def456',
        input_source: 'zakupki.gov.ru',
        ktru_code: '34.12.11.120',
        status: 'RUNNING',
        limit_contracts: 20,
        region_filter: '78',
        technical_specification: 'Technical spec example 2',
        total_contracts_found: 87,
        contracts_processed: 65,
        created_at: '2024-02-05T11:15:00Z',
        updated_at: '2024-02-05T11:20:00Z'
      },
      {
        id: 'search_1707234567892_ghi789',
        input_source: 'zakupki.gov.ru',
        ktru_code: '34.12.11.130',
        status: 'FAILED',
        limit_contracts: 15,
        region_filter: '50',
        technical_specification: 'Technical spec example 3',
        total_contracts_found: 0,
        contracts_processed: 0,
        created_at: '2024-02-05T09:45:00Z',
        updated_at: '2024-02-05T09:50:00Z',
        error_message: 'Connection timeout'
      }
    ]
    
    return mockSearches
  },
  
  getSearchById: async (searchId: string) => {
    await new Promise(resolve => setTimeout(resolve, 500))
    return {
      id: searchId,
      input_source: 'zakupki.gov.ru',
      ktru_code: '34.12.11.110',
      status: 'RUNNING',
      limit_contracts: 10,
      region_filter: '77',
      technical_specification: 'Example technical specification',
      total_contracts_found: 100,
      contracts_processed: 45,
      created_at: '2024-02-05T11:15:00Z',
      updated_at: '2024-02-05T11:20:00Z'
    }
  },
  
  stopSearch: async (searchId: string) => {
    await new Promise(resolve => setTimeout(resolve, 500))
    return {
      success: true,
      message: `Search ${searchId} stopped successfully`,
      searchId
    }
  }
}

// Export both real and mock APIs
export default {
  real: searchApi,
  mock: mockApi,
  EventSource: SearchEventSource
}