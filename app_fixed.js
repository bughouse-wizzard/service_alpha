// ФИНАЛЬНАЯ ВЕРСИЯ APP.JS ДЛЯ СИСТЕМЫ ПОИСКА КОНТРАКТОВ ПО КТРУ
console.log('NMCK System JavaScript loaded - FINAL VERSION');

class NMCKSystem {
    constructor() {
        this.apiBaseUrl = '';
        this.currentSession = null;
        this.currentTasks = [];
        this.taskUpdateInterval = null;
        
        console.log('NMCK System initialized');
        
        // Инициализация
        this.init();
    }
    
    async init() {
        try {
            // Проверяем API
            const apiHealthy = await this.checkAPI();
            if (!apiHealthy) {
                this.showError('API недоступен. Проверьте подключение к серверу.');
                return;
            }
            
            // Создаем сессию
            await this.createSession();
            
            // Загружаем интерфейс
            this.loadInterface();
            
            // Загружаем задачи
            await this.loadTasks();
            
            // Запускаем обновление задач
            this.startTaskUpdates();
            
            console.log('System initialized successfully');
            
        } catch (error) {
            console.error('Initialization error:', error);
            this.showError('Ошибка инициализации системы: ' + error.message);
        }
    }
    
    async checkAPI() {
        try {
            const response = await fetch('/health');
            const data = await response.json();
            console.log('API Health:', data);
            return true;
        } catch (error) {
            console.error('API Check failed:', error);
            return false;
        }
    }
    
    async createSession() {
        try {
            const response = await fetch('/api/session', {
                method: 'GET',
                headers: {
                    'Accept': 'application/json'
                }
            });
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }
            
            const data = await response.json();
            this.currentSession = data.id;
            console.log('Session created:', this.currentSession);
            
            return data;
        } catch (error) {
            console.error('Session creation failed:', error);
            // Пробуем создать локальную сессию
            this.currentSession = 'local-' + Date.now();
            console.log('Using local session:', this.currentSession);
            return { id: this.currentSession };
        }
    }
    
    loadInterface() {
        const app = document.getElementById('app');
        app.innerHTML = `
            <div class="app-container">
                <header class="header">
                    <div>
                        <h1><i class="fas fa-search"></i> Система поиска контрактов по КТРУ</h1>
                        <div class="version-badge">Версия 1.0.0 | Стабильная сборка</div>
                    </div>
                    <div class="system-info">
                        <div class="status-item status-ok">
                            <i class="fas fa-check-circle"></i>
                            <div>API: Работает</div>
                        </div>
                    </div>
                </header>
                
                <div class="main-grid">
                    <!-- Левая колонка: История поисков -->
                    <div class="card">
                        <div class="card-header">
                            <h2><i class="fas fa-history"></i> История поисков</h2>
                            <div class="filter-controls">
                                <select class="filter-select" id="statusFilter" onchange="window.nmckSystem.filterTasks()">
                                    <option value="all">Все статусы</option>
                                    <option value="PENDING">Ожидание</option>
                                    <option value="SEARCHING">Поиск</option>
                                    <option value="DONE">Завершено</option>
                                    <option value="ERROR">Ошибка</option>
                                </select>
                                <button class="btn" onclick="window.nmckSystem.loadTasks()">
                                    <i class="fas fa-sync-alt"></i>
                                </button>
                            </div>
                        </div>
                        <div class="task-list" id="taskList">
                            <div class="task-item">
                                <div class="task-header">
                                    <div class="task-title">Загрузка задач...</div>
                                    <div class="task-status status-pending">Загрузка</div>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Правая колонка: Новый поиск -->
                    <div class="card">
                        <div class="card-header">
                            <h2><i class="fas fa-plus-circle"></i> Новый поиск</h2>
                        </div>
                        
                        <form id="searchForm" onsubmit="window.nmckSystem.startSearch(event)">
                            <div class="form-group">
                                <label class="form-label">КТРУ код:</label>
                                <input type="text" class="form-input" id="ktruCode" 
                                       placeholder="26.20.16.110-00000106" required>
                            </div>
                            
                            <div class="form-row">
                                <div class="form-group">
                                    <label class="form-label">Наименование:</label>
                                    <input type="text" class="form-input" id="productName" 
                                           placeholder="Ноутбук" required>
                                </div>
                                
                                <div class="form-group">
                                    <label class="form-label">Поставщик:</label>
                                    <input type="text" class="form-input" id="vendor" 
                                           placeholder="ООО 'Технопарк'">
                                </div>
                            </div>
                            
                            <div class="form-group">
                                <label class="form-label">Характеристики (JSON):</label>
                                <textarea class="form-input" id="characteristics" rows="3" 
                                          placeholder='[{"key": "processor", "value": "Intel Core i5"}, {"key": "ram", "value": "8GB"}]'></textarea>
                            </div>
                            
                            <div class="form-group">
                                <div class="dropzone" id="dropzone" onclick="document.getElementById('fileInput').click()">
                                    <i class="fas fa-cloud-upload-alt"></i>
                                    <p>Перетащите файл с КТРУ кодами или нажмите для выбора</p>
                                    <small>Поддерживаются файлы: .txt, .csv, .xlsx</small>
                                </div>
                                <input type="file" id="fileInput" style="display: none" 
                                       onchange="window.nmckSystem.handleFileSelect(event)">
                            </div>
                            
                            <div class="form-row">
                                <div class="form-group">
                                    <label class="form-label">Период поиска (лет):</label>
                                    <select class="form-input" id="periodYears">
                                        <option value="1">1 год</option>
                                        <option value="2">2 года</option>
                                        <option value="3">3 года</option>
                                        <option value="5">5 лет</option>
                                    </select>
                                </div>
                                
                                <div class="form-group">
                                    <label class="form-label">Регион:</label>
                                    <select class="form-input" id="region">
                                        <option value="all">Все регионы</option>
                                        <option value="77">Москва</option>
                                        <option value="78">Санкт-Петербург</option>
                                        <option value="52">Нижегородская область</option>
                                        <option value="66">Свердловская область</option>
                                    </select>
                                </div>
                            </div>
                            
                            <button type="submit" class="btn btn-primary btn-full">
                                <i class="fas fa-search"></i> Начать поиск контрактов
                            </button>
                        </form>
                    </div>
                </div>
                
                <!-- Статус системы -->
                <div class="card">
                    <div class="card-header">
                        <h2><i class="fas fa-info-circle"></i> Статус системы</h2>
                    </div>
                    <div class="system-status">
                        <div class="status-item status-ok">
                            <i class="fas fa-server"></i>
                            <div>Сервер API</div>
                            <div class="status-text">Работает</div>
                        </div>
                        <div class="status-item status-ok">
                            <i class="fas fa-database"></i>
                            <div>База данных</div>
                            <div class="status-text">Доступна</div>
                        </div>
                        <div class="status-item status-ok">
                            <i class="fas fa-search"></i>
                            <div>Поиск контрактов</div>
                            <div class="status-text">Активен</div>
                        </div>
                        <div class="status-item status-ok">
                            <i class="fas fa-bolt"></i>
                            <div>Парсер ЕИС</div>
                            <div class="status-text">Готов</div>
                        </div>
                    </div>
                </div>
                
                <footer class="footer">
                    <p>Система поиска контрактов по КТРУ © 2026 | Стабильная версия с фильтром по статусу и красной кнопкой остановки</p>
                    <p>Коммит: 981b533 | Сервер: 192.168.88.170:8000</p>
                </footer>
            </div>
        `;
        
        // Настраиваем обработчики
        this.setupEventHandlers();
    }
    setupEventHandlers() {
        // Настройка dropzone
        const dropzone = document.getElementById('dropzone');
        if (dropzone) {
            dropzone.addEventListener('dragover', (e) => {
                e.preventDefault();
                dropzone.style.borderColor = '#2563eb';
                dropzone.style.background = '#f0f7ff';
            });
            
            dropzone.addEventListener('dragleave', () => {
                dropzone.style.borderColor = '#d1d5db';
                dropzone.style.background = '#f9fafb';
            });
            
            dropzone.addEventListener('drop', (e) => {
                e.preventDefault();
                dropzone.style.borderColor = '#d1d5db';
                dropzone.style.background = '#f9fafb';
                
                if (e.dataTransfer.files.length > 0) {
                    this.handleFileSelect({ target: { files: e.dataTransfer.files } });
                }
            });
        }
    }
    
    async loadTasks() {
        try {
            const response = await fetch('/api/tasks', {
                headers: {
                    'Accept': 'application/json'
                }
            });
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }
            
            const tasks = await response.json();
            this.currentTasks = tasks;
            this.renderTasks(tasks);
            
            console.log(`Loaded ${tasks.length} tasks`);
            
        } catch (error) {
            console.error('Failed to load tasks:', error);
            this.showError('Не удалось загрузить список задач');
        }
    }
    
    renderTasks(tasks) {
        const taskList = document.getElementById('taskList');
        if (!taskList) return;
        
        if (tasks.length === 0) {
            taskList.innerHTML = `
                <div class="task-item">
                    <div class="task-header">
                        <div class="task-title">Задачи не найдены</div>
                    </div>
                    <div class="task-details">
                        <div>Создайте первую задачу поиска</div>
                    </div>
                </div>
            `;
            return;
        }
        
        taskList.innerHTML = tasks.map(task => `
            <div class="task-item" onclick="window.nmckSystem.showTaskResults('${task.id}')">
                <div class="task-header">
                    <div class="task-title">${task.ktru_code || 'КТРУ код не указан'}</div>
                    <div class="task-status status-${task.status.toLowerCase()}">
                        ${this.getStatusText(task.status)}
                    </div>
                </div>
                <div class="task-details">
                    <div>
                        <i class="fas fa-box"></i>
                        ${task.product_name || 'Без названия'}
                    </div>
                    <div>
                        <i class="fas fa-calendar"></i>
                        ${new Date(task.created_at).toLocaleDateString('ru-RU')}
                    </div>
                </div>
                ${task.progress !== undefined ? `
                <div class="task-progress">
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: ${task.progress}%"></div>
                    </div>
                    <div style="text-align: right; font-size: 12px; margin-top: 4px;">
                        ${task.progress}% ${task.stage ? `- ${task.stage}` : ''}
                    </div>
                </div>
                ` : ''}
                ${task.status === 'SEARCHING' ? `
                <div style="margin-top: 10px;">
                    <button class="btn btn-danger btn-full" onclick="event.stopPropagation(); window.nmckSystem.stopTask('${task.id}')">
                        <i class="fas fa-stop-circle"></i> Остановить поиск
                    </button>
                </div>
                ` : ''}
            </div>
        `).join('');
    }
    
    getStatusText(status) {
        const statusMap = {
            'PENDING': 'Ожидание',
            'SEARCHING': 'Поиск',
            'DONE': 'Завершено',
            'ERROR': 'Ошибка'
        };
        return statusMap[status] || status;
    }
    
    filterTasks() {
        const filter = document.getElementById('statusFilter').value;
        let filteredTasks = this.currentTasks;
        
        if (filter !== 'all') {
            filteredTasks = this.currentTasks.filter(task => task.status === filter);
        }
        
        this.renderTasks(filteredTasks);
    }
    
    async startSearch(event) {
        event.preventDefault();
        
        const ktruCode = document.getElementById('ktruCode').value.trim();
        const productName = document.getElementById('productName').value.trim();
        const vendor = document.getElementById('vendor').value.trim();
        const characteristics = document.getElementById('characteristics').value.trim();
        const periodYears = document.getElementById('periodYears').value;
        const region = document.getElementById('region').value;
        
        if (!ktruCode) {
            this.showError('Введите КТРУ код');
            return;
        }
        
        if (!productName) {
            this.showError('Введите наименование товара');
            return;
        }
        
        try {
            // Создаем задачу через прямой ввод
            const taskData = {
                ktru_code: ktruCode,
                product_name: productName,
                vendor: vendor || undefined,
                characteristics: characteristics ? JSON.parse(characteristics) : [],
                period_years: parseInt(periodYears),
                region: region
            };
            
            console.log('Creating task:', taskData);
            
            const response = await fetch('/api/tasks/direct', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify(taskData)
            });
            
            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`HTTP ${response.status}: ${errorText}`);
            }
            
            const task = await response.json();
            console.log('Task created:', task);
            
            this.showToast('Задача поиска создана успешно!', 'success');
            
            // Очищаем форму
            document.getElementById('searchForm').reset();
            
            // Обновляем список задач
            await this.loadTasks();
            
        } catch (error) {
            console.error('Failed to create task:', error);
            this.showError('Ошибка создания задачи: ' + error.message);
        }
    }
    
    async handleFileSelect(event) {
        const file = event.target.files[0];
        if (!file) return;
        
        console.log('File selected:', file.name);
        
        try {
            // Создаем FormData
            const formData = new FormData();
            formData.append('file', file);
            
            // Загружаем файл
            const response = await fetch('/api/uploads', {
                method: 'POST',
                body: formData
            });
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }
            
            const upload = await response.json();
            console.log('File uploaded:', upload);
            
            this.showToast('Файл загружен успешно!', 'success');
            
        } catch (error) {
            console.error('File upload failed:', error);
            this.showError('Ошибка загрузки файла: ' + error.message);
        }
    }
    async showTaskResults(taskId) {
        try {
            // Получаем детали задачи
            const taskResponse = await fetch(`/api/tasks/${taskId}`);
            if (!taskResponse.ok) throw new Error('Task not found');
            const task = await taskResponse.json();
            
            // Получаем контракты
            const contractsResponse = await fetch(`/api/tasks/${taskId}/result`);
            const contracts = contractsResponse.ok ? await contractsResponse.json() : [];
            
            // Показываем модальное окно
            const resultsContent = document.getElementById('resultsContent');
            resultsContent.innerHTML = `
                <div class="task-details">
                    <div><strong>КТРУ код:</strong> ${task.ktru_code}</div>
                    <div><strong>Товар:</strong> ${task.product_name || 'Не указано'}</div>
                    <div><strong>Статус:</strong> ${this.getStatusText(task.status)}</div>
                    <div><strong>Создана:</strong> ${new Date(task.created_at).toLocaleString('ru-RU')}</div>
                    ${task.finished_at ? `<div><strong>Завершена:</strong> ${new Date(task.finished_at).toLocaleString('ru-RU')}</div>` : ''}
                </div>
                
                <h3 style="margin-top: 20px; margin-bottom: 10px;">Найдено контрактов: ${contracts.length}</h3>
                
                ${contracts.length > 0 ? `
                <div style="max-height: 400px; overflow-y: auto;">
                    ${contracts.map(contract => `
                        <div class="task-item" style="margin-bottom: 10px;">
                            <div class="task-header">
                                <div class="task-title">${contract.reg_number || 'Без номера'}</div>
                                <div class="task-status status-done">Контракт</div>
                            </div>
                            <div class="task-details">
                                <div><strong>Поставщик:</strong> ${contract.supplier_name || 'Не указан'}</div>
                                <div><strong>Цена:</strong> ${contract.unit_price ? contract.unit_price.toLocaleString('ru-RU') + ' ' + (contract.currency || 'RUB') : 'Не указана'}</div>
                                <div><strong>Дата подписания:</strong> ${contract.sign_date ? new Date(contract.sign_date).toLocaleDateString('ru-RU') : 'Не указана'}</div>
                            </div>
                        </div>
                    `).join('')}
                </div>
                ` : '<p>Контракты не найдены</p>'}
            `;
            
            // Открываем модальное окно
            window.openResultsModal();
            
        } catch (error) {
            console.error('Failed to load task results:', error);
            this.showError('Не удалось загрузить результаты задачи');
        }
    }
    
    async stopTask(taskId) {
        if (!confirm('Вы уверены, что хотите остановить поиск?')) {
            return;
        }
        
        try {
            const response = await fetch(`/api/tasks/${taskId}/stop`, {
                method: 'POST',
                headers: {
                    'Accept': 'application/json'
                }
            });
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }
            
            const result = await response.json();
            console.log('Task stopped:', result);
            
            this.showToast('Поиск остановлен успешно!', 'success');
            
            // Обновляем список задач
            await this.loadTasks();
            
        } catch (error) {
            console.error('Failed to stop task:', error);
            this.showError('Ошибка остановки задачи: ' + error.message);
        }
    }
    
    startTaskUpdates() {
        // Обновляем задачи каждые 10 секунд
        this.taskUpdateInterval = setInterval(() => {
            this.loadTasks();
        }, 10000);
    }
    
    stopTaskUpdates() {
        if (this.taskUpdateInterval) {
            clearInterval(this.taskUpdateInterval);
            this.taskUpdateInterval = null;
        }
    }
    
    showToast(message, type = 'info') {
        if (window.showToast) {
            window.showToast(message, type);
        } else {
            console.log(`Toast [${type}]: ${message}`);
        }
    }
    
    showError(message) {
        this.showToast(message, 'error');
    }
    
    showSuccess(message) {
        this.showToast(message, 'success');
    }
}

// Инициализация системы при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    window.nmckSystem = new NMCKSystem();
});
