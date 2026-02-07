# Production код фронтенда системы поиска контрактов по КТРУ

## Содержание (только production код)
1. [static/app.js](#staticappjs)
2. [static/app_old.js](#staticappoldjs)
3. [static/debug.html](#staticdebughtml)
4. [static/index.html](#staticindexhtml)
5. [static/style.css](#staticstylecss)
6. [static/test.html](#statictesthtml)

---

### Файл: `static/app.js`
```javascript
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

```

### Файл: `static/app_old.js`
```javascript
// Основной JavaScript для фронтенда системы НМЦК - обновленный по демо-интерфейсу

class NMCKSystem {
    constructor() {
        this.apiBaseUrl = "/api";
        this.wsBaseUrl = window.location.origin.replace("http", "ws") + "/api/ws";
        this.sessionToken = null;
        this.wsConnection = null;
        this.currentTaskId = null;
        this.selectedContracts = new Set();
        this.currentTaskResults = null;
        
        this.initialize();
    }

    async initialize() {
        // Инициализация сессии
        await this.initializeSession();
        
        // Инициализация WebSocket
        await this.initializeWebSocket();
        
        // Загрузка истории задач
        await this.loadTaskHistory();
        
        // Настройка обработчиков событий
        this.setupEventHandlers();
        
        // Обновление статистики
        await this.updateStats();
        
        // Показываем уведомление о готовности
        this.showToast("Система готова к работе", "success");
    }

    async initializeSession() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/session`);
            const data = await response.json();
            this.sessionToken = data.token;
            console.log("Сессия инициализирована:", this.sessionToken);
        } catch (error) {
            console.error("Ошибка инициализации сессии:", error);
            this.showToast("Ошибка инициализации сессии", "error");
        }
    }

    async initializeWebSocket() {
        if (!this.sessionToken) {
            console.warn("Нет токена сессии для WebSocket");
            return;
        }
        
        try {
            this.wsConnection = new WebSocket(`${this.wsBaseUrl}?session_token=${this.sessionToken}`);
            
            this.wsConnection.onopen = () => {
                console.log("WebSocket подключен");
            };
            
            this.wsConnection.onmessage = (event) => {
                this.handleWebSocketMessage(event.data);
            };
            
            this.wsConnection.onclose = () => {
                console.log("WebSocket отключен, переподключение через 5 секунд...");
                setTimeout(() => this.initializeWebSocket(), 5000);
            };
            
            this.wsConnection.onerror = (error) => {
                console.error("WebSocket ошибка:", error);
            };
            
        } catch (error) {
            console.error("Ошибка подключения WebSocket:", error);
        }
    }

    handleWebSocketMessage(message) {
        try {
            const data = JSON.parse(message);
            
            switch (data.type) {
                case "task.progress":
                    this.updateTaskProgress(data.data);
                    break;
                    
                case "task.completed":
                    this.handleTaskCompleted(data.data);
                    break;
                    
                case "task.error":
                    this.handleTaskError(data.data);
                    break;
                    
                case "pong":
                    // Ответ на ping, ничего не делаем
                    break;
                    
                default:
                    console.log("Неизвестное сообщение WebSocket:", data);
            }
        } catch (error) {
            console.error("Ошибка обработки WebSocket сообщения:", error, message);
        }
    }

    async loadTaskHistory() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/tasks?limit=20`);
            const tasks = await response.json();
            
            this.renderTaskHistory(tasks);
        } catch (error) {
            console.error("Ошибка загрузки истории задач:", error);
            this.showToast("Ошибка загрузки истории", "error");
        }
    }

    renderTaskHistory(tasks) {
        const tbody = document.getElementById("historyTbody");
        if (!tbody) return;
        
        tbody.innerHTML = "";
        
        tasks.forEach(task => {
            const row = document.createElement("tr");
            row.className = "rowlink";
            row.dataset.taskId = task.id;
            
            // Форматируем дату
            const createdDate = new Date(task.created_at);
            const dateStr = createdDate.toLocaleDateString("ru-RU") + " " + 
                           createdDate.toLocaleTimeString("ru-RU", { hour: "2-digit", minute: "2-digit" });
            
            // Форматируем время поиска
            let durationStr = "-";
            if (task.search_duration) {
                const minutes = Math.floor(task.search_duration / 60);
                const seconds = Math.floor(task.search_duration % 60);
                durationStr = `${minutes}м ${seconds}с`;
            }
            
            // Определяем статус
            const statusMap = {
                "queued": { text: "В очереди", class: "tag blue" },
                "searching": { text: "Идет поиск", class: "tag blue" },
                "downloading": { text: "Загрузка", class: "tag blue" },
                "analyzing": { text: "Анализ", class: "tag blue" },
                "done": { text: "Готово", class: "tag ok" },
                "error": { text: "Ошибка", class: "tag bad" },
                "cancelled": { text: "Отменено", class: "tag warn" },
            };
            
            const statusInfo = statusMap[task.status] || { text: task.status, class: "tag" };
            
            // Краткий итог
            let summary = "-";
            if (task.status === "done" && task.total_found > 0) {
                summary = `Найдено: ${task.total_found}, НМЦК: ${task.nmck_value ? task.nmck_value.toLocaleString("ru-RU") + " ₽" : "-"}`;
            } else if (task.status === "error") {
                summary = "Ошибка при выполнении";
            }
            
            row.innerHTML = `
                <td class="nowrap">${dateStr}</td>
                <td>
                    <div>${task.product_name || "Не указано"}</div>
                    <div class="mono" style="font-size:11px; color:var(--muted); margin-top:2px">
                        ${task.ktru_code || "КТРУ не указан"}
                    </div>
                </td>
                <td class="nowrap">
                    <span class="${statusInfo.class}">
                        <span class="p"></span>
                        ${statusInfo.text}
                    </span>
                </td>
                <td>${summary}</td>
                <td class="nowrap">${durationStr}</td>
            `;
            
            // Добавляем обработчик клика для готовых задач
            if (task.status === "done") {
                row.style.cursor = "pointer";
                row.addEventListener("click", () => {
                    this.showTaskResults(task.id);
                });
            }
            
            tbody.appendChild(row);
        });
    }
    setupEventHandlers() {
        // Обработчик загрузки файла
        const fileInput = document.getElementById("fileInput");
        const uploadBtn = document.getElementById("uploadBtn");
        
        if (uploadBtn) {
            uploadBtn.addEventListener("click", () => {
                fileInput.click();
            });
        }
        
        if (fileInput) {
            fileInput.addEventListener("change", (e) => {
                this.handleFileUpload(e.target.files[0]);
            });
        }
        
        // Обработчик кнопки запуска поиска
        const startSearchBtn = document.getElementById("startSearchBtn");
        if (startSearchBtn) {
            startSearchBtn.addEventListener("click", () => {
                this.startSearch();
            });
        }
        
        // Обработчики навигации
        document.querySelectorAll(".navbtn").forEach(btn => {
            btn.addEventListener("click", (e) => {
                this.handleNavigation(e.target.id);
            });
        });
        
        // Обработчик закрытия модального окна
        const closeModalBtn = document.getElementById("closeAuditLog");
        if (closeModalBtn) {
            closeModalBtn.addEventListener("click", () => {
                this.closeAuditLogModal();
            });
        }
        
        // Обработчик клика вне модального окна
        const modal = document.getElementById("auditLogModal");
        if (modal) {
            modal.addEventListener("click", (e) => {
                if (e.target === modal) {
                    this.closeAuditLogModal();
                }
            });
        }
        
        // Обработчик кнопки обновления истории
        const refreshBtn = document.getElementById("refreshHistory");
        if (refreshBtn) {
            refreshBtn.addEventListener("click", () => {
                this.loadTaskHistory();
                this.showToast("История обновлена", "success");
            });
        }
    }

    async handleFileUpload(file) {
        if (!file) return;
        
        // Показываем индикатор загрузки
        this.showToast(`Загрузка файла: ${file.name}`, "info");
        
        const formData = new FormData();
        formData.append("file", file);
        
        try {
            const response = await fetch(`${this.apiBaseUrl}/uploads`, {
                method: "POST",
                body: formData,
            });
            
            if (response.ok) {
                const uploadData = await response.json();
                this.showToast("Файл успешно загружен", "success");
                
                // Сохраняем upload_id для использования при запуске поиска
                this.currentUploadId = uploadData.upload_id;
                
                // Показываем распознанные данные
                this.showUploadDetails(uploadData);
                
            } else {
                const error = await response.json();
                this.showToast(`Ошибка загрузки: ${error.message}`, "error");
            }
            
        } catch (error) {
            console.error("Ошибка загрузки файла:", error);
            this.showToast("Ошибка загрузки файла", "error");
        }
    }

    showUploadDetails(uploadData) {
        const container = document.getElementById("uploadDetails");
        if (!container) return;
        
        const detected = uploadData.detected;
        
        let html = `
            <div class="upload-summary">
                <h3>Распознанные данные</h3>
                <div class="upload-details">
                    <div class="detail-row">
                        <span class="label">Код КТРУ:</span>
                        <span class="value mono">${detected.ktru_code || "Не распознан"}</span>
                    </div>
                    <div class="detail-row">
                        <span class="label">Наименование:</span>
                        <span class="value">${detected.name || "Не распознано"}</span>
                    </div>
                    <div class="detail-row">
                        <span class="label">Производитель:</span>
                        <span class="value">${detected.vendor || "Не указан"}</span>
                    </div>
                </div>
        `;
        
        // Характеристики
        if (detected.characteristics && detected.characteristics.length > 0) {
            html += `
                <div class="characteristics">
                    <h4>Характеристики:</h4>
                    <table class="compact">
                        <thead>
                            <tr>
                                <th>Параметр</th>
                                <th>Значение</th>
                                <th>Ед. изм.</th>
                                <th>Оператор</th>
                            </tr>
                        </thead>
                        <tbody>
            `;
            
            detected.characteristics.forEach(char => {
                html += `
                    <tr>
                        <td>${char.key}</td>
                        <td>${char.value}</td>
                        <td>${char.unit || "-"}</td>
                        <td>${char.operator || "="}</td>
                    </tr>
                `;
            });
            
            html += `
                        </tbody>
                    </table>
                </div>
            `;
        }
        
        // Предупреждения
        if (uploadData.warnings && uploadData.warnings.length > 0) {
            html += `
                <div class="warnings">
                    <h4>Предупреждения:</h4>
                    <ul>
            `;
            
            uploadData.warnings.forEach(warning => {
                html += `<li>${warning}</li>`;
            });
            
            html += `
                    </ul>
                </div>
            `;
        }
        
        html += `</div>`;
        
        container.innerHTML = html;
        container.style.display = "block";
        
        // Активируем кнопку запуска поиска
        const startSearchBtn = document.getElementById("startSearchBtn");
        if (startSearchBtn) {
            startSearchBtn.disabled = false;
        }
    }

    async startSearch() {
        if (!this.currentUploadId) {
            this.showToast("Сначала загрузите файл с требованиями", "warning");
            return;
        }
        
        // Получаем параметры поиска из формы
        const region = document.getElementById("regionSelect").value;
        const period = document.getElementById("periodSelect").value;
        
        try {
            const response = await fetch(`${this.apiBaseUrl}/tasks`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    upload_id: this.currentUploadId,
                    region: region,
                    period_years: parseInt(period),
                }),
            });
            
            if (response.ok) {
                const taskData = await response.json();
                this.showToast("Задача поиска создана", "success");
                
                // Переключаемся на вкладку истории
                document.getElementById("navHistory").click();
                
                // Обновляем историю задач
                await this.loadTaskHistory();
                
            } else {
                const error = await response.json();
                this.showToast(`Ошибка создания задачи: ${error.message}`, "error");
            }
            
        } catch (error) {
            console.error("Ошибка запуска поиска:", error);
            this.showToast("Ошибка запуска поиска", "error");
        }
    }

    handleNavigation(navId) {
        // Скрываем все секции
        document.querySelectorAll(".section").forEach(section => {
            section.style.display = "none";
        });
        
        // Убираем активный класс со всех кнопок
        document.querySelectorAll(".navbtn").forEach(btn => {
            btn.classList.remove("active");
        });
        
        // Показываем нужную секцию и активируем кнопку
        const targetSection = document.getElementById(navId.replace("nav", ""));
        const targetBtn = document.getElementById(navId);
        
        if (targetSection) {
            targetSection.style.display = "block";
        }
        
        if (targetBtn) {
            targetBtn.classList.add("active");
        }
    }

    closeAuditLogModal() {
        const modal = document.getElementById("auditLogModal");
        if (modal) {
            modal.classList.remove("open");
            setTimeout(() => {
                modal.style.display = "none";
            }, 300);
        }
    }

    showToast(message, type = "info") {
        const toastContainer = document.getElementById("toastContainer");
        if (!toastContainer) return;
        
        const toast = document.createElement("div");
        toast.className = `toast ${type}`;
        toast.textContent = message;
        
        toastContainer.appendChild(toast);
        
        // Автоматическое удаление через 5 секунд
        setTimeout(() => {
            toast.classList.add("fade-out");
            setTimeout(() => {
                toast.remove();
            }, 300);
        }, 5000);
    }

    // Вспомогательные методы
    formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString("ru-RU") + " " + 
               date.toLocaleTimeString("ru-RU", { hour: "2-digit", minute: "2-digit" });
    }
    
    formatCurrency(amount, currency = "RUB") {
        const formatter = new Intl.NumberFormat("ru-RU", {
            style: "currency",
            currency: currency,
            minimumFractionDigits: 2,
            maximumFractionDigits: 2,
        });
        return formatter.format(amount);
    }
}

// Инициализация системы при загрузке страницы
document.addEventListener("DOMContentLoaded", () => {
    window.nmckSystem = new NMCKSystem();
});

```

### Файл: `static/debug.html`
```html
<!DOCTYPE html>
<html>
<head>
    <title>Debug</title>
</head>
<body>
    <h1>Debug Frontend</h1>
    <div id="output"></div>
    <script>
        async function debug() {
            const output = document.getElementById('output');
            
            // Test session
            output.innerHTML += '<p>Testing session...</p>';
            const sessionRes = await fetch('/api/session');
            const sessionData = await sessionRes.json();
            output.innerHTML += `<p>Session token: ${sessionData.token}</p>`;
            
            // Test tasks
            output.innerHTML += '<p>Testing tasks...</p>';
            const tasksRes = await fetch('/api/tasks?limit=20', {
                credentials: 'include'
            });
            const tasksData = await tasksRes.json();
            output.innerHTML += `<p>Tasks count: ${tasksData.length}</p>`;
            output.innerHTML += `<pre>${JSON.stringify(tasksData, null, 2)}</pre>`;
            
            // Test if table would render
            if (tasksData.length > 0) {
                const task = tasksData[0];
                output.innerHTML += `<p>Sample task: ${task.id}, product_name: ${task.product_name}, ktru_code: ${task.ktru_code}</p>`;
            }
        }
        debug();
    </script>
</body>
</html>

```

### Файл: `static/index.html`
```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Система поиска контрактов по КТРУ</title>
    <link rel="stylesheet" href="style.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #2563eb;
            --primary-dark: #1d4ed8;
            --secondary: #10b981;
            --danger: #ef4444;
            --warning: #f59e0b;
            --gray-50: #f9fafb;
            --gray-100: #f3f4f6;
            --gray-200: #e5e7eb;
            --gray-300: #d1d5db;
            --gray-700: #374151;
            --gray-900: #111827;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: var(--gray-900);
        }
        
        .app-container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            background: white;
            border-radius: 16px;
            padding: 24px 32px;
            margin-bottom: 24px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .header h1 {
            color: var(--gray-900);
            font-size: 28px;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 12px;
        }
        
        .header h1 i {
            color: var(--primary);
        }
        
        .version-badge {
            background: var(--primary);
            color: white;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: 600;
        }
        
        .main-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 24px;
            margin-bottom: 24px;
        }
        
        .card {
            background: white;
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
            transition: transform 0.2s, box-shadow 0.2s;
        }
        
        .card:hover {
            transform: translateY(-2px);
            box-shadow: 0 15px 30px rgba(0, 0, 0, 0.15);
        }
        
        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 16px;
            border-bottom: 2px solid var(--gray-100);
        }
        
        .card-header h2 {
            font-size: 20px;
            font-weight: 600;
            color: var(--gray-900);
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .card-header i {
            color: var(--primary);
        }
        
        .filter-controls {
            display: flex;
            gap: 12px;
            align-items: center;
        }
        
        .filter-select {
            padding: 8px 16px;
            border: 1px solid var(--gray-300);
            border-radius: 8px;
            background: white;
            font-size: 14px;
            color: var(--gray-700);
            cursor: pointer;
        }
        
        .task-list {
            max-height: 500px;
            overflow-y: auto;
        }
        
        .task-item {
            background: var(--gray-50);
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 12px;
            border-left: 4px solid var(--primary);
            transition: all 0.2s;
        }
        
        .task-item:hover {
            background: var(--gray-100);
            transform: translateX(4px);
        }
        
        .task-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px;
        }
        
        .task-title {
            font-weight: 600;
            color: var(--gray-900);
            font-size: 16px;
        }
        
        .task-status {
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
        }
        
        .status-pending { background: #fef3c7; color: #92400e; }
        .status-searching { background: #dbeafe; color: #1e40af; }
        .status-done { background: #d1fae5; color: #065f46; }
        .status-error { background: #fee2e2; color: #991b1b; }
        
        .task-details {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
            margin-top: 12px;
            font-size: 14px;
            color: var(--gray-700);
        }
        
        .task-progress {
            margin-top: 12px;
        }
        
        .progress-bar {
            height: 8px;
            background: var(--gray-200);
            border-radius: 4px;
            overflow: hidden;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, var(--primary), var(--secondary));
            border-radius: 4px;
            transition: width 0.3s;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        .form-label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: var(--gray-900);
            font-size: 14px;
        }
        
        .form-input {
            width: 100%;
            padding: 12px 16px;
            border: 2px solid var(--gray-200);
            border-radius: 10px;
            font-size: 15px;
            transition: all 0.2s;
        }
        
        .form-input:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
        }
        
        .form-row {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px;
        }
        
        .btn {
            padding: 14px 28px;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
        }
        
        .btn-primary {
            background: linear-gradient(135deg, var(--primary), var(--primary-dark));
            color: white;
        }
        
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(37, 99, 235, 0.3);
        }
        
        .btn-danger {
            background: var(--danger);
            color: white;
        }
        
        .btn-danger:hover {
            background: #dc2626;
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(239, 68, 68, 0.3);
        }
        
        .btn-full {
            width: 100%;
        }
        
        .dropzone {
            border: 2px dashed var(--gray-300);
            border-radius: 12px;
            padding: 40px;
            text-align: center;
            background: var(--gray-50);
            cursor: pointer;
            transition: all 0.2s;
        }
        
        .dropzone:hover {
            border-color: var(--primary);
            background: var(--gray-100);
        }
        
        .dropzone i {
            font-size: 48px;
            color: var(--gray-400);
            margin-bottom: 16px;
        }
        
        .dropzone p {
            color: var(--gray-600);
            margin-bottom: 8px;
        }
        
        .dropzone small {
            color: var(--gray-500);
            font-size: 14px;
        }
        
        .system-status {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
            margin-top: 20px;
        }
        
        .status-item {
            background: var(--gray-50);
            padding: 16px;
            border-radius: 12px;
            text-align: center;
        }
        
        .status-item i {
            font-size: 24px;
            margin-bottom: 8px;
        }
        
        .status-ok i { color: var(--secondary); }
        .status-warning i { color: var(--warning); }
        .status-error i { color: var(--danger); }
        
        .footer {
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid var(--gray-200);
            color: var(--gray-600);
            font-size: 14px;
        }
        
        .loading {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            background: white;
        }
        
        .spinner {
            font-size: 48px;
            color: var(--primary);
            margin-bottom: 20px;
            animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.5);
            z-index: 1000;
            align-items: center;
            justify-content: center;
        }
        
        .modal.active {
            display: flex;
        }
        
        .modal-content {
            background: white;
            border-radius: 16px;
            padding: 32px;
            max-width: 600px;
            width: 90%;
            max-height: 80vh;
            overflow-y: auto;
        }
        
        .toast {
            position: fixed;
            top: 20px;
            right: 20px;
            background: white;
            border-radius: 12px;
            padding: 16px 24px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
            display: flex;
            align-items: center;
            gap: 12px;
            z-index: 1001;
            transform: translateX(400px);
            transition: transform 0.3s;
        }
        
        .toast.show {
            transform: translateX(0);
        }
        
        .toast-success { border-left: 4px solid var(--secondary); }
        .toast-error { border-left: 4px solid var(--danger); }
        .toast-info { border-left: 4px solid var(--primary); }
        
        @media (max-width: 1024px) {
            .main-grid {
                grid-template-columns: 1fr;
            }
            
            .form-row {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div id="app">
        <div class="loading" id="loadingScreen">
            <div class="spinner"><i class="fas fa-spinner"></i></div>
            <h2>Загрузка системы поиска контрактов...</h2>
            <p>Пожалуйста, подождите</p>
        </div>
    </div>
    
    <!-- Модальное окно результатов -->
    <div class="modal" id="resultsModal">
        <div class="modal-content">
            <div class="card-header">
                <h2><i class="fas fa-chart-bar"></i> Результаты поиска</h2>
                <button class="btn" onclick="closeResultsModal()">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            <div id="resultsContent">
                <!-- Контент результатов будет загружен здесь -->
            </div>
        </div>
    </div>
    
    <!-- Тосты -->
    <div id="toastContainer"></div>
    
    <script src="app.js"></script>
    <script>
        console.log('NMCK System loading...');
        
        // Проверяем API при загрузке
        fetch('/health')
            .then(r => r.json())
            .then(data => {
                console.log('System health:', data);
                showToast('Система загружена успешно', 'success');
            })
            .catch(err => {
                console.error('Health check failed:', err);
                showToast('Ошибка подключения к API', 'error');
            });
            
        // Функции для работы с интерфейсом
        function showToast(message, type = 'info') {
            const container = document.getElementById('toastContainer');
            const toast = document.createElement('div');
            toast.className = `toast toast-${type}`;
            toast.innerHTML = `
                <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
                <span>${message}</span>
            `;
            container.appendChild(toast);
            
            setTimeout(() => toast.classList.add('show'), 10);
            setTimeout(() => {
                toast.classList.remove('show');
                setTimeout(() => toast.remove(), 300);
            }, 3000);
        }
        
        function openResultsModal() {
            document.getElementById('resultsModal').classList.add('active');
        }
        
        function closeResultsModal() {
            document.getElementById('resultsModal').classList.remove('active');
        }
        
        // Глобальные функции для app.js
        window.showToast = showToast;
        window.openResultsModal = openResultsModal;
        window.closeResultsModal = closeResultsModal;
    </script>
</body>
</html>

```

### Файл: `static/style.css`
```css
/* Основные стили системы НМЦК - обновленные по демо-интерфейсу */

:root {
    --bg: #f6f7fb;
    --panel: #ffffff;
    --text: #0f172a;
    --muted: #64748b;
    --border: #e5e7eb;
    --primary: #2563eb;
    --primary-weak: #dbeafe;
    --danger: #dc2626;
    --danger-weak: #fee2e2;
    --ok: #16a34a;
    --ok-weak: #dcfce7;
    --warn: #d97706;
    --warn-weak: #ffedd5;
    --shadow: 0 10px 30px rgba(15,23,42,.08);
    --radius: 14px;
    --focus: 0 0 0 4px rgba(37,99,235,.18);
    --mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
    --sans: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, "Helvetica Neue", Arial, "Noto Sans", "Liberation Sans", sans-serif;
}

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

html, body {
    height: 100%;
}

body {
    margin: 0;
    font-family: var(--sans);
    background: linear-gradient(180deg, #f8fafc 0%, var(--bg) 100%);
    color: var(--text);
}

a {
    color: var(--primary);
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
}

.app {
    min-height: 100%;
    display: flex;
    flex-direction: column;
}

/* Header */
header {
    position: sticky;
    top: 0;
    z-index: 5;
    backdrop-filter: saturate(180%) blur(10px);
    background: rgba(246,247,251,.75);
    border-bottom: 1px solid var(--border);
}

.topbar {
    width: 100%;
    padding: 14px 16px;
    display: flex;
    gap: 12px;
    align-items: center;
    justify-content: space-between;
}

.brand {
    display: flex;
    gap: 10px;
    align-items: center;
    min-width: 260px;
}

.logo {
    width: 38px;
    height: 38px;
    border-radius: 12px;
    background: radial-gradient(circle at 30% 20%, #93c5fd 0%, #2563eb 40%, #1e40af 100%);
    box-shadow: 0 10px 20px rgba(37,99,235,.25);
}

.brand h1 {
    margin: 0;
    font-size: 14px;
    line-height: 1.2;
    font-weight: 800;
    letter-spacing: .2px;
}

.brand p {
    margin: 0;
    font-size: 12px;
    color: var(--muted);
}

.nav {
    display: flex;
    gap: 8px;
    align-items: center;
}

.chip {
    border: 1px solid var(--border);
    background: var(--panel);
    padding: 8px 10px;
    border-radius: 999px;
    font-size: 13px;
    color: var(--text);
    display: flex;
    gap: 8px;
    align-items: center;
    cursor: pointer;
    user-select: none;
    border: none;
    font-family: inherit;
}

.chip[aria-pressed="true"] {
    border-color: rgba(37,99,235,.35);
    background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
    box-shadow: 0 8px 20px rgba(2,6,23,.06);
}

.chip .dot {
    width: 8px;
    height: 8px;
    border-radius: 999px;
    background: var(--muted);
}

.chip[aria-pressed="true"] .dot {
    background: var(--primary);
}

.actions {
    display: flex;
    gap: 8px;
    align-items: center;
    justify-content: flex-end;
    min-width: 260px;
}

.btn {
    border: 1px solid var(--border);
    background: var(--panel);
    color: var(--text);
    padding: 10px 12px;
    border-radius: 12px;
    font-size: 13px;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    gap: 8px;
    transition: transform .05s ease, box-shadow .15s ease, border-color .15s ease;
    border: none;
    font-family: inherit;
}

.btn:hover {
    border-color: #cbd5e1;
}

.btn:active {
    transform: translateY(1px);
}

.btn.primary {
    background: linear-gradient(180deg, #2563eb 0%, #1d4ed8 100%);
    border-color: rgba(29,78,216,.4);
    color: #fff;
    box-shadow: 0 12px 25px rgba(37,99,235,.22);
}

.btn.primary:hover {
    box-shadow: 0 16px 30px rgba(37,99,235,.28);
}

.btn:focus {
    outline: none;
    box-shadow: var(--focus);
}

.kbd {
    font-family: var(--mono);
    font-size: 11px;
    color: var(--muted);
    border: 1px solid var(--border);
    padding: 2px 6px;
    border-radius: 8px;
    background: #fff;
}

/* Main layout */
main {
    width: 100%;
    padding: 18px 16px 40px;
    flex: 1;
}

.grid {
    display: grid;
    grid-template-columns: 1.25fr .75fr;
    gap: 14px;
    align-items: start;
    width: 100%;
}

@media (max-width: 980px) {
    .grid {
        grid-template-columns: 1fr;
    }
    .brand, .actions {
        min-width: unset;
    }
}

/* Cards */
.card {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    box-shadow: var(--shadow);
    overflow: hidden;
    width: 100%;
}

.card .hd {
    padding: 14px 14px 12px;
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 12px;
}

.card .hd h2 {
    margin: 0;
    font-size: 14px;
    font-weight: 800;
    letter-spacing: .2px;
}

.sub {
    margin-top: 4px;
    font-size: 12px;
    color: var(--muted);
    line-height: 1.35;
}

.card .bd {
    padding: 14px;
}

/* Form elements */
.row {
    display: flex;
    gap: 10px;
    align-items: center;
    flex-wrap: wrap;
}

.spacer {
    flex: 1;
}

.field {
    display: flex;
    flex-direction: column;
    gap: 6px;
    min-width: 180px;
    flex: 1;
}

.label {
    font-size: 12px;
    color: var(--muted);
}

input[type="text"], input[type="number"], select, textarea {
    width: 100%;
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 10px 12px;
    font-size: 13px;
    background: #fff;
    color: var(--text);
    transition: box-shadow .15s ease, border-color .15s ease;
    border: 1px solid var(--border);
    font-family: inherit;
}

textarea {
    min-height: 92px;
    resize: vertical;
}

input:focus, select:focus, textarea:focus {
    outline: none;
    border-color: rgba(37,99,235,.45);
    box-shadow: var(--focus);
}

.hint {
    font-size: 12px;
    color: var(--muted);
}

.divider {
    height: 1px;
    background: var(--border);
    margin: 12px 0;
}

/* Tables */
.tablewrap {
    overflow: auto;
    border-radius: 12px;
    border: 1px solid var(--border);
    background: #fff;
    width: 100%;
}

table {
    width: 100%;
    border-collapse: collapse;
    min-width: 860px;
}

@media (min-width: 1280px) {
    table {
        min-width: 0;
    }
}

th, td {
    text-align: left;
    padding: 10px 10px;
    border-bottom: 1px solid var(--border);
    font-size: 13px;
    vertical-align: top;
}

th {
    font-size: 12px;
    color: var(--muted);
    background: #fafafa;
    position: sticky;
    top: 0;
    z-index: 2;
}

.mono {
    font-family: var(--mono);
    font-size: 12px;
}

/* Tags */
.tag {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    border-radius: 999px;
    padding: 4px 8px;
    border: 1px solid var(--border);
    background: #fff;
    font-size: 12px;
    white-space: nowrap;
}

.tag .p {
    width: 8px;
    height: 8px;
    border-radius: 999px;
    background: var(--muted);
}

.tag.ok {
    border-color: rgba(22,163,74,.28);
    background: var(--ok-weak);
}

.tag.ok .p {
    background: var(--ok);
}

.tag.warn {
    border-color: rgba(217,119,6,.28);
    background: var(--warn-weak);
}

.tag.warn .p {
    background: var(--warn);
}

.tag.bad {
    border-color: rgba(220,38,38,.28);
    background: var(--danger-weak);
}

.tag.bad .p {
    background: var(--danger);
}

.tag.blue {
    border-color: rgba(37,99,235,.25);
    background: var(--primary-weak);
}

.tag.blue .p {
    background: var(--primary);
}

.rightcol {
    position: sticky;
    top: 78px;
    display: flex;
    flex-direction: column;
    gap: 14px;
    width: 100%;
}

@media (max-width: 980px) {
    .rightcol {
        position: static;
    }
}

/* Stats */
.stat {
    display: flex;
    flex-direction: column;
    gap: 6px;
    padding: 12px;
    border-radius: 14px;
    border: 1px solid var(--border);
    background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
}

.stat .k {
    font-size: 12px;
    color: var(--muted);
}

.stat .v {
    font-size: 18px;
    font-weight: 900;
    letter-spacing: .2px;
}

.stat .mini {
    font-size: 12px;
    color: var(--muted);
}

.statrow {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
}

@media (max-width: 520px) {
    .statrow {
        grid-template-columns: 1fr;
    }
}

/* History row click UX */
tr.rowlink {
    cursor: pointer;
}

tr.rowlink:hover td {
    background: #f8fbff;
}

tr.rowlink:active td {
    background: #eef6ff;
}

/* Toasts */
.toasts {
    position: fixed;
    z-index: 50;
    right: 16px;
    bottom: 16px;
    display: flex;
    flex-direction: column;
    gap: 10px;
    max-width: 360px;
}

.toast {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 14px;
    box-shadow: var(--shadow);
    padding: 10px 10px;
    display: flex;
    gap: 10px;
    align-items: flex-start;
    animation: pop .18s ease-out;
}

@keyframes pop {
    from {
        transform: translateY(6px);
        opacity: .0;
    }
    to {
        transform: translateY(0);
        opacity: 1;
    }
}

.toast .ico {
    width: 28px;
    height: 28px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #f1f5f9;
    border: 1px solid var(--border);
    flex: 0 0 auto;
    font-weight: 900;
}

.toast.ok .ico {
    background: var(--ok-weak);
    border-color: rgba(22,163,74,.25);
    color: var(--ok);
}

.toast.warn .ico {
    background: var(--warn-weak);
    border-color: rgba(217,119,6,.25);
    color: var(--warn);
}

.toast.bad .ico {
    background: var(--danger-weak);
    border-color: rgba(220,38,38,.25);
    color: var(--danger);
}

.toast .t {
    font-weight: 800;
    font-size: 13px;
    margin: 0;
}

.toast .d {
    margin: 2px 0 0;
    font-size: 12px;
    color: var(--muted);
    line-height: 1.35;
}

.toast .x {
    margin-left: auto;
    border: 0;
    background: transparent;
    cursor: pointer;
    color: var(--muted);
    padding: 4px 6px;
    border-radius: 10px;
    border: none;
    font-family: inherit;
}

.toast .x:hover {
    background: #f1f5f9;
}

/* Modal */
.modalback {
    position: fixed;
    inset: 0;
    z-index: 60;
    background: rgba(2,6,23,.48);
    display: none;
    align-items: center;
    justify-content: center;
    padding: 16px;
}

.modalback.open {
    display: flex;
}

.modal {
    width: min(980px, 100%);
    max-height: min(86vh, 900px);
    overflow: auto;
    border-radius: 18px;
    background: var(--panel);
    border: 1px solid rgba(148,163,184,.35);
    box-shadow: 0 30px 80px rgba(2,6,23,.32);
}

.modal .mhd {
    padding: 14px 14px 12px;
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: flex-start;
    gap: 10px;
    justify-content: space-between;
}

.modal .mhd h3 {
    margin: 0;
    font-size: 14px;
    font-weight: 900;
}

.modal .mbd {
    padding: 14px;
}

.modal .mft {
    padding: 12px 14px;
    border-top: 1px solid var(--border);
    display: flex;
    gap: 10px;
    justify-content: flex-end;
    align-items: center;
    background: #fafafa;
}

/* File upload */
.drop {
    border: 1px dashed #cbd5e1;
    background: linear-gradient(180deg, #fff 0%, #f8fafc 100%);
    border-radius: 14px;
    padding: 12px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
}

.drop.drag {
    border-color: rgba(37,99,235,.55);
    box-shadow: var(--focus);
}

.filelist {
    display: flex;
    flex-direction: column;
    gap: 8px;
    margin-top: 10px;
}

.fileitem {
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 10px 12px;
    display: flex;
    gap: 10px;
    align-items: flex-start;
    background: #fff;
}

.fileitem .name {
    font-weight: 800;
    font-size: 13px;
}

.fileitem .meta {
    font-size: 12px;
    color: var(--muted);
}

.fileitem .rm {
    margin-left: auto;
}

.minirow {
    display: flex;
    gap: 8px;
    align-items: center;
    flex-wrap: wrap;
}

/* Status indicators */
.sstatus {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    font-size: 12px;
    color: var(--muted);
}

.sstatus .s {
    width: 10px;
    height: 10px;
    border-radius: 999px;
    background: var(--muted);
    box-shadow: 0 0 0 4px rgba(100,116,139,.12);
}

.sstatus.ok .s {
    background: var(--ok);
    box-shadow: 0 0 0 4px rgba(22,163,74,.12);
}

.sstatus.warn .s {
    background: var(--warn);
    box-shadow: 0 0 0 4px rgba(217,119,6,.12);
}

.sstatus.bad .s {
    background: var(--danger);
    box-shadow: 0 0 0 4px rgba(220,38,38,.12);
}

.sstatus.blue .s {
    background: var(--primary);
    box-shadow: 0 0 0 4px rgba(37,99,235,.14);
}

/* Diff highlighting */
.diff {
    background: var(--danger-weak) !important;
    border-radius: 10px;
    padding: 2px 6px;
    display: inline-block;
    border: 1px dashed rgba(220,38,38,.35);
    color: #7f1d1d;
}

.nowrap {
    white-space: nowrap;
}

.sr {
    position: absolute;
    left: -9999px;
    top: auto;
    width: 1px;
    height: 1px;
    overflow: hidden;
}

/* Pill */
.pill {
    font-size: 12px;
    border: 1px solid var(--border);
    padding: 5px 8px;
    border-radius: 999px;
    background: #fff;
    color: var(--muted);
}

/* Filter styles */
.filter-header {
    display: flex;
    align-items: center;
    gap: 6px;
    position: relative;
}

.filter-btn {
    background: transparent;
    border: none;
    color: var(--muted);
    cursor: pointer;
    padding: 2px 4px;
    border-radius: 6px;
    font-size: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 24px;
    height: 24px;
}

.filter-btn:hover {
    background: var(--primary-weak);
    color: var(--primary);
}

.filter-btn.active {
    background: var(--primary);
    color: white;
}

.filter-dropdown {
    position: absolute;
    top: 100%;
    left: 0;
    background: white;
    border: 1px solid var(--border);
    border-radius: 12px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    padding: 12px;
    z-index: 100;
    min-width: 200px;
    margin-top: 4px;
}

.filter-options {
    display: flex;
    flex-direction: column;
    gap: 8px;
    margin-bottom: 12px;
}

.filter-options label {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 13px;
    cursor: pointer;
    padding: 4px 0;
}

.filter-options input[type="checkbox"] {
    width: 16px;
    height: 16px;
    margin: 0;
}

.filter-actions {
    display: flex;
    gap: 8px;
    justify-content: flex-end;
}

.btn-sm {
    padding: 6px 10px;
    font-size: 12px;
}

.btn-danger {
    background: linear-gradient(180deg, #dc2626 0%, #b91c1c 100%);
    border-color: rgba(185,28,28,.4);
    color: #fff;
    box-shadow: 0 12px 25px rgba(220,38,38,.22);
}

.btn-danger:hover {
    box-shadow: 0 16px 30px rgba(220,38,38,.28);
}

.btn-outline-danger {
    border: 1px solid var(--danger);
    background: transparent;
    color: var(--danger);
}

.btn-outline-danger:hover {
    background: var(--danger-weak);
}
```

### Файл: `static/test.html`
```html
<!DOCTYPE html>
<html>
<head>
    <title>Test Frontend</title>
</head>
<body>
    <h1>Test API Calls</h1>
    <div id="result"></div>
    <script>
        async function test() {
            const resultDiv = document.getElementById('result');
            try {
                // Test session
                const sessionRes = await fetch('/api/session');
                const sessionData = await sessionRes.json();
                resultDiv.innerHTML += `<p>Session: ${sessionData.token}</p>`;
                
                // Test tasks with cookie
                const tasksRes = await fetch('/api/tasks?limit=20', {
                    credentials: 'include'
                });
                const tasksData = await tasksRes.json();
                resultDiv.innerHTML += `<p>Tasks count: ${tasksData.length}</p>`;
                resultDiv.innerHTML += `<pre>${JSON.stringify(tasksData, null, 2)}</pre>`;
            } catch (error) {
                resultDiv.innerHTML += `<p>Error: ${error}</p>`;
            }
        }
        test();
    </script>
</body>
</html>

```

