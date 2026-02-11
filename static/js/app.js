// Main application JavaScript for Search Dashboard

function app() {
    return {
        // State
        searchForm: {
            objectName: '',
            inputSource: 'manual',
            ktruCode: '',
            limitContracts: 10,
            nmcValue: ''
        },
        isSearching: false,
        currentSearchId: null,
        progressPercentage: 0,
        progressMessage: '',
        processedCount: 0,
        totalCount: 0,
        currentResults: [],
        searchHistory: [],
        comparisonData: null,
        eventSource: null,

        // Initialize
        init() {
            console.log('App initialized');
        },

        // Format price with commas
        formatPrice(price) {
            if (!price) return 'N/A';
            return new Intl.NumberFormat('ru-RU', {
                style: 'currency',
                currency: 'RUB',
                minimumFractionDigits: 2
            }).format(price);
        },

        // Format date
        formatDate(dateString) {
            if (!dateString) return 'N/A';
            const date = new Date(dateString);
            return date.toLocaleDateString('ru-RU', {
                year: 'numeric',
                month: 'short',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            });
        },

        // Get status badge class
        getStatusBadgeClass(status) {
            switch (status) {
                case 'RUNNING':
                    return 'bg-warning';
                case 'COMPLETED':
                    return 'bg-success';
                case 'STOPPED':
                    return 'bg-danger';
                case 'FAILED':
                    return 'bg-danger';
                default:
                    return 'bg-secondary';
            }
        },

        // Load search history
        async loadHistory() {
            try {
                console.log('Loading search history...');
                // In a real implementation, this would fetch from an API endpoint
                // For now, we'll simulate with a timeout
                await new Promise(resolve => setTimeout(resolve, 500));
                
                // Simulated history data
                this.searchHistory = [
                    {
                        id: 'search-001',
                        object_name: 'Laptop Computers',
                        status: 'COMPLETED',
                        found_total: 45,
                        created_at: '2024-01-15T10:30:00Z'
                    },
                    {
                        id: 'search-002',
                        object_name: 'Office Chairs',
                        status: 'RUNNING',
                        found_total: 12,
                        created_at: '2024-01-16T14:20:00Z'
                    },
                    {
                        id: 'search-003',
                        object_name: 'Printer Supplies',
                        status: 'STOPPED',
                        found_total: 8,
                        created_at: '2024-01-14T09:15:00Z'
                    }
                ];
                
                console.log('History loaded:', this.searchHistory.length, 'searches');
            } catch (error) {
                console.error('Error loading history:', error);
            }
        },

        // Start a new search
        async startSearch() {
            if (!this.searchForm.objectName.trim()) {
                alert('Please enter an object name');
                return;
            }

            this.isSearching = true;
            this.progressPercentage = 0;
            this.progressMessage = 'Starting search...';
            this.currentResults = [];

            try {
                console.log('Starting search with data:', this.searchForm);
                
                // Make API call to start search
                const response = await fetch('/api/search', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        input_source: this.searchForm.inputSource,
                        object_name: this.searchForm.objectName,
                        ktru_code: this.searchForm.ktruCode || null,
                        nmc_value: this.searchForm.nmcValue || null,
                        limit_contracts: this.searchForm.limitContracts
                    })
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const searchData = await response.json();
                this.currentSearchId = searchData.id;
                console.log('Search started with ID:', this.currentSearchId);
                
                // Start listening for events
                this.startEventStream();
                
                // Add to history
                this.searchHistory.unshift({
                    id: searchData.id,
                    object_name: searchData.object_name,
                    status: searchData.status,
                    found_total: searchData.found_total || 0,
                    created_at: new Date().toISOString()
                });

            } catch (error) {
                console.error('Error starting search:', error);
                this.isSearching = false;
                this.progressMessage = 'Error starting search: ' + error.message;
                alert('Failed to start search: ' + error.message);
            }
        },

        // Start EventSource for real-time updates
        startEventStream() {
            if (!this.currentSearchId) return;

            // Close existing connection if any
            if (this.eventSource) {
                this.eventSource.close();
            }

            const eventSourceUrl = `/api/search/${this.currentSearchId}/events`;
            console.log('Connecting to EventSource:', eventSourceUrl);
            
            this.eventSource = new EventSource(eventSourceUrl);

            this.eventSource.onopen = () => {
                console.log('EventSource connection opened');
                this.progressMessage = 'Connected to search updates...';
            };

            this.eventSource.onmessage = (event) => {
                console.log('Raw EventSource message:', event.data);
                try {
                    const data = JSON.parse(event.data);
                    this.handleEvent(data);
                } catch (e) {
                    console.error('Error parsing EventSource data:', e);
                }
            };

            this.eventSource.addEventListener('status', (event) => {
                try {
                    const data = JSON.parse(event.data);
                    console.log('Status event:', data);
                    this.handleStatusEvent(data);
                } catch (e) {
                    console.error('Error parsing status event:', e);
                }
            });

            this.eventSource.addEventListener('progress', (event) => {
                try {
                    const data = JSON.parse(event.data);
                    console.log('Progress event:', data);
                    this.handleProgressEvent(data);
                } catch (e) {
                    console.error('Error parsing progress event:', e);
                }
            });

            this.eventSource.addEventListener('error', (event) => {
                console.error('EventSource error:', event);
                this.progressMessage = 'Connection error. Attempting to reconnect...';
                
                // Try to reconnect after delay
                setTimeout(() => {
                    if (this.isSearching && this.currentSearchId) {
                        console.log('Attempting to reconnect EventSource...');
                        this.startEventStream();
                    }
                }, 3000);
            });
        },

        // Handle generic events
        handleEvent(data) {
            console.log('Handling event:', data);
            // Update progress based on event type
            if (data.status === 'COMPLETED') {
                this.handleSearchCompleted();
            } else if (data.status === 'STOPPED') {
                this.handleSearchStopped();
            }
        },

        // Handle status events
        handleStatusEvent(data) {
            this.progressMessage = data.message || 'Processing...';
            
            if (data.status === 'COMPLETED') {
                this.handleSearchCompleted();
            } else if (data.status === 'STOPPED') {
                this.handleSearchStopped();
            } else if (data.status === 'FAILED') {
                this.handleSearchFailed(data.message || 'Search failed');
            }
        },

        // Handle progress events
        handleProgressEvent(data) {
            this.processedCount = data.processed || 0;
            this.totalCount = data.total || 100;
            this.progressPercentage = data.percentage || 0;
            
            if (data.processed && data.total) {
                this.progressMessage = `Processing ${data.processed} of ${data.total} items`;
            }
        },

        // Handle search completion
        async handleSearchCompleted() {
            console.log('Search completed');
            this.isSearching = false;
            this.progressMessage = 'Search completed successfully!';
            this.progressPercentage = 100;
            
            // Close EventSource
            if (this.eventSource) {
                this.eventSource.close();
                this.eventSource = null;
            }
            
            // Load results
            await this.loadSearchResults();
            
            // Update history
            await this.loadHistory();
        },

        // Handle search stopped
        handleSearchStopped() {
            console.log('Search stopped');
            this.isSearching = false;
            this.progressMessage = 'Search was stopped';
            
            // Close EventSource
            if (this.eventSource) {
                this.eventSource.close();
                this.eventSource = null;
            }
            
            // Load partial results
            this.loadSearchResults();
        },

        // Handle search failed
        handleSearchFailed(message) {
            console.log('Search failed:', message);
            this.isSearching = false;
            this.progressMessage = 'Search failed: ' + message;
            
            // Close EventSource
            if (this.eventSource) {
                this.eventSource.close();
                this.eventSource = null;
            }
        },

        // Stop current search
        async stopSearch() {
            if (!this.currentSearchId) {
                alert('No active search to stop');
                return;
            }

            try {
                console.log('Stopping search:', this.currentSearchId);
                
                const response = await fetch(`/api/search/${this.currentSearchId}/stop`, {
                    method: 'POST'
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const result = await response.json();
                console.log('Search stopped:', result);
                
                this.progressMessage = 'Stopping search...';
                
                // EventSource will handle the actual stop event
                
            } catch (error) {
                console.error('Error stopping search:', error);
                alert('Failed to stop search: ' + error.message);
            }
        },

        // Load search results
        async loadSearchResults() {
            if (!this.currentSearchId) return;

            try {
                console.log('Loading results for search:', this.currentSearchId);
                
                const response = await fetch(`/api/search/${this.currentSearchId}/results`);
                
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const results = await response.json();
                console.log('Results loaded:', results.length, 'items');
                
                this.currentResults = results;
                
            } catch (error) {
                console.error('Error loading results:', error);
                this.currentResults = [];
            }
        },

        // View results from history
        async viewSearchResults(searchId) {
            try {
                console.log('Viewing results for search:', searchId);
                
                // Load search details
                const response = await fetch(`/api/search/${searchId}`);
                
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const searchDetails = await response.json();
                console.log('Search details:', searchDetails);
                
                // Set as current search
                this.currentSearchId = searchId;
                this.currentResults = [];
                
                // Load results
                await this.loadSearchResults();
                
                // Scroll to results section
                document.querySelector('.card:has(.card-header:contains("Current Search Results"))')?.scrollIntoView({ behavior: 'smooth' });
                
            } catch (error) {
                console.error('Error viewing search results:', error);
                alert('Failed to load search results: ' + error.message);
            }
        },

        // Open comparison modal
        async openComparisonModal(result) {
            try {
                console.log('Opening comparison modal for result:', result.id);
                this.comparisonData = null;
                
                // Show modal
                const modal = new bootstrap.Modal(document.getElementById('comparisonModal'));
                modal.show();
                
                // In a real implementation, we would fetch detailed comparison data
                // For now, we'll use the result data directly
                await new Promise(resolve => setTimeout(resolve, 500));
                
                this.comparisonData = {
                    ...result,
                    // Add some mock data for demonstration
                    customer_name: result.customer_name || 'Government Agency',
                    sign_date: result.sign_date || '2024-01-15',
                    execution_date: result.execution_date || '2024-06-15'
                };
                
                console.log('Comparison data loaded:', this.comparisonData);
                
            } catch (error) {
                console.error('Error opening comparison modal:', error);
                alert('Failed to load comparison data: ' + error.message);
            }
        }
    };
}