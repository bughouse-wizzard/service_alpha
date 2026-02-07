// Основной JavaScript для фронтенда системы НМЦК - обновленный по демо-интерфейсу

class NMCKSystem {
    constructor() {
        this.apiBaseUrl = "/api";
        this.wsBaseUrl = window.location.origin.replace("http", "ws") + "/api/ws";
        this.sessionToken = null;
        this.wsConnection = null;
        // Восстанавливаем currentTaskId из localStorage
        this.currentTaskId = localStorage.getItem('nmck_current_task_id') || null;
        this.selectedContracts = new Set();
        this.currentTaskResults = null;
        this.currentFile = null;

        // Фильтры
        this.statusFilter = new Set(['all']); // По умолчанию показываем все
        this.allTasks = []; // Все задачи для фильтрации

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

        // Восстанавливаем результаты задачи, если есть сохраненный ID
        if (this.currentTaskId) {
            try {
                await this.showTaskResults(this.currentTaskId);
                this.showView("detail");
            } catch (error) {
                console.warn("Не удалось восстановить результаты задачи:", error);
                // Очищаем невалидный ID
                this.currentTaskId = null;
                localStorage.removeItem('nmck_current_task_id');
            }
        }

        // Запускаем периодическое обновление статистики каждые 10 секунд
        setInterval(() => {
            this.updateStats();
        }, 10000);

        // Показываем уведомление о готовности
        this.showToast("Система готова к работе", "success");
    }

    async initializeSession() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/session`, {
                credentials: 'include'
            });
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
                console.log("WebSocket соединение установлено");
            };

            this.wsConnection.onmessage = (event) => {
                this.handleWebSocketMessage(event);
            };

            this.wsConnection.onerror = (error) => {
                console.error("WebSocket ошибка:", error);
            };

            this.wsConnection.onclose = () => {
                console.log("WebSocket соединение закрыто");
                // Пытаемся переподключиться через 5 секунд
                setTimeout(() => this.initializeWebSocket(), 5000);
            };
        } catch (error) {
            console.error("Ошибка инициализации WebSocket:", error);
        }
    }

    handleWebSocketMessage(event) {
        try {
            const message = JSON.parse(event.data);
            console.log("WebSocket сообщение:", message);

            switch (message.type) {
                case "task.created":
                    this.showToast(`Задача создана: ${message.data.product_name}`, "success");
                    this.loadTaskHistory();
                    break;

                case "task.progress":
                    this.updateTaskProgress(message.data);
                    break;

                case "task.done":
                    this.showToast(`Поиск завершен: ${message.data.summary}`, "success");
                    this.loadTaskHistory();
                    this.updateStats();
                    break;

                case "task.failed":
                    this.showToast(`Ошибка поиска: ${message.data.human_message}`, "error");
                    this.loadTaskHistory();
                    break;

                case "task.stopped":
                    this.showToast(`Поиск остановлен: ${message.data.message}`, "warn");
                    this.loadTaskHistory();
                    this.updateStats();
                    break;

                default:
                    console.log("Неизвестное сообщение WebSocket:", message);
            }
        } catch (error) {
            console.error("Ошибка обработки WebSocket сообщения:", error, event.data);
        }
    }

    async loadTaskHistory() {
        try {
            console.log("loadTaskHistory: Загрузка истории задач...");
            const response = await fetch(`${this.apiBaseUrl}/tasks?limit=50`, {
                credentials: 'include'  // Включаем cookies
            });
            console.log("loadTaskHistory: Статус ответа:", response.status);
            const tasks = await response.json();
            console.log("loadTaskHistory: Получено задач:", tasks.length, "задачи:", tasks);

            // Сохраняем все задачи для фильтрации
            this.allTasks = tasks;

            // Применяем фильтры
            const filteredTasks = this.applyFilters(tasks);

            this.renderTaskHistory(filteredTasks);
        } catch (error) {
            console.error("Ошибка загрузки истории задач:", error);
            this.showToast("Ошибка загрузки истории", "error");
        }
    }

    setupStatusFilter() {
        const filterBtn = document.getElementById("statusFilterBtn");
        const filterDropdown = document.getElementById("statusFilterDropdown");
        const applyBtn = document.getElementById("applyStatusFilter");
        const clearBtn = document.getElementById("clearStatusFilter");

        if (!filterBtn || !filterDropdown) return;

        // Открытие/закрытие выпадающего списка
        filterBtn.addEventListener("click", (e) => {
            e.stopPropagation();
            const isVisible = filterDropdown.style.display === "block";
            filterDropdown.style.display = isVisible ? "none" : "block";
            filterBtn.classList.toggle("active", !isVisible);
        });

        // Закрытие при клике вне
        document.addEventListener("click", (e) => {
            if (!filterDropdown.contains(e.target) && e.target !== filterBtn) {
                filterDropdown.style.display = "none";
                filterBtn.classList.remove("active");
            }
        });

        // Обработка выбора "Все статусы"
        const allCheckbox = filterDropdown.querySelector('.status-filter[value="all"]');
        const otherCheckboxes = filterDropdown.querySelectorAll('.status-filter:not([value="all"])');

        allCheckbox.addEventListener('change', (e) => {
            if (e.target.checked) {
                otherCheckboxes.forEach(cb => cb.checked = false);
            }
        });

        otherCheckboxes.forEach(cb => {
            cb.addEventListener('change', (e) => {
                if (e.target.checked) {
                    allCheckbox.checked = false;
                }
            });
        });

        // Применить фильтр
        applyBtn.addEventListener('click', () => {
            this.statusFilter.clear();

            const selectedCheckboxes = filterDropdown.querySelectorAll('.status-filter:checked');
            selectedCheckboxes.forEach(cb => {
                this.statusFilter.add(cb.value);
            });

            // Если ничего не выбрано или выбрано "all", показываем все
            if (this.statusFilter.size === 0 || this.statusFilter.has('all')) {
                this.statusFilter.clear();
                this.statusFilter.add('all');
            }

            // Обновляем таблицу
            const filteredTasks = this.applyFilters(this.allTasks);
            this.renderTaskHistory(filteredTasks);

            // Закрываем выпадающий список
            filterDropdown.style.display = "none";
            filterBtn.classList.remove("active");

            // Показываем уведомление
            const selectedCount = this.statusFilter.has('all') ? 'Все статусы' : `${this.statusFilter.size} статус(ов)`;
            this.showToast(`Применен фильтр: ${selectedCount}`, "success");
        });

        // Сбросить фильтр
        clearBtn.addEventListener('click', () => {
            allCheckbox.checked = true;
            otherCheckboxes.forEach(cb => cb.checked = false);
            this.statusFilter.clear();
            this.statusFilter.add('all');

            // Обновляем таблицу
            this.renderTaskHistory(this.allTasks);

            // Закрываем выпадающий список
            filterDropdown.style.display = "none";
            filterBtn.classList.remove("active");

            this.showToast("Фильтр сброшен", "success");
        });
    }

    applyFilters(tasks) {
        if (this.statusFilter.has('all') || this.statusFilter.size === 0) {
            return tasks;
        }

        return tasks.filter(task => this.statusFilter.has(task.status));
    }

    renderTaskHistory(tasks) {
        const tbody = document.getElementById("historyTbody");
        if (!tbody) return;

        tbody.innerHTML = "";

        tasks.forEach(task => {
            const row = document.createElement("tr");
            row.className = "rowlink";
            row.dataset.taskId = task.id;

            // Дата и время
            const dateCell = document.createElement("td");
            const date = new Date(task.created_at);
            dateCell.textContent = date.toLocaleString("ru-RU");
            dateCell.className = "nowrap";

            // Товар / КТРУ
            const productCell = document.createElement("td");
            productCell.innerHTML = `
                <div style="font-weight:800">${task.product_name || "Без названия"}</div>
                <div style="font-size:12px; color:var(--muted)">${task.ktru_code || "Без КТРУ"}</div>
            `;

            // Статус
            const statusCell = document.createElement("td");
            const statusTag = this.getStatusTag(task.status, task.stage);
            statusCell.innerHTML = statusTag;

            // Краткий итог
            const summaryCell = document.createElement("td");
            summaryCell.textContent = task.summary || "—";

            // Время поиска
            const timeCell = document.createElement("td");
            timeCell.className = "nowrap";
            if (task.search_time) {
                const seconds = Math.round(task.search_time);
                timeCell.textContent = seconds >= 60 ? 
                    `${Math.floor(seconds / 60)} мин ${seconds % 60} сек` : 
                    `${seconds} сек`;
            } else {
                timeCell.textContent = "—";
            }

            // Действия
            const actionsCell = document.createElement("td");
            actionsCell.className = "nowrap";
            
            if (task.status === "done") {
                actionsCell.innerHTML = `
                    <button class="btn btn-sm" onclick="nmckSystem.showTaskResults('${task.id}')" title="Просмотреть результаты">
                        <i class="fas fa-eye"></i> Детали
                    </button>
                `;
            } else if (task.status === "searching" || task.status === "downloading" || task.status === "analyzing") {
                actionsCell.innerHTML = `
                    <button class="btn btn-sm btn-danger" onclick="nmckSystem.stopTask('${task.id}')" title="Остановить поиск">
                        <i class="fas fa-stop"></i> Остановить
                    </button>
                `;
            } else {
                actionsCell.innerHTML = "—";
            }

            row.appendChild(dateCell);
            row.appendChild(productCell);
            row.appendChild(statusCell);
            row.appendChild(summaryCell);
            row.appendChild(timeCell);
            row.appendChild(actionsCell);

            // Клик по строке для просмотра результатов (только для завершенных задач)
            if (task.status === "done") {
                row.addEventListener("click", (e) => {
                    // Не срабатывает при клике на кнопки внутри ячейки
                    if (e.target.tagName === 'BUTTON' || e.target.closest('button')) return;
                    this.showTaskResults(task.id);
                });
            }

            tbody.appendChild(row);
        });

        // Если нет задач
        if (tasks.length === 0) {
            const emptyRow = document.createElement("tr");
            const emptyCell = document.createElement("td");
            emptyCell.colSpan = 6;
            emptyCell.textContent = "Нет задач для отображения";
            emptyCell.style.textAlign = "center";
            emptyCell.style.padding = "40px";
            emptyCell.style.color = "var(--muted)";
            emptyRow.appendChild(emptyCell);
            tbody.appendChild(emptyRow);
        }
    }

    getStatusTag(status, stage) {
        const statusMap = {
            "queued": { label: "В очереди", class: "tag blue" },
            "searching": { label: "Идет поиск", class: "tag blue" },
            "downloading": { label: "Загрузка", class: "tag warn" },
            "analyzing": { label: "Анализ", class: "tag warn" },
            "done": { label: "Готово", class: "tag ok" },
            "error": { label: "Ошибка", class: "tag bad" },
            "cancelled": { label: "Отменено", class: "tag" },
            "stopped": { label: "Остановлен", class: "tag" }
        };

        const config = statusMap[status] || { label: status, class: "tag" };
        
        let displayText = config.label;
        if (stage && stage !== status) {
            displayText += ` (${stage})`;
        }

        return `
            <span class="${config.class}">
                <span class="p"></span>
                ${displayText}
            </span>
        `;
    }    setupEventHandlers() {
        // Навигация
        document.getElementById("navHistory").addEventListener("click", () => {
            this.showView("history");
        });

        document.getElementById("navDetail").addEventListener("click", () => {
            if (this.currentTaskId) {
                this.showView("detail");
            } else {
                this.showToast("Сначала выберите задачу из истории", "warn");
            }
        });

        // Кнопка "Новый поиск" в хедере
        document.getElementById("btnNewSearch").addEventListener("click", () => {
            this.showView("history");
            // Прокручиваем к форме
            document.getElementById("searchForm").scrollIntoView({ behavior: "smooth" });
        });

        // Кнопка "Правила"
        document.getElementById("btnHelp").addEventListener("click", () => {
            this.showHelpModal();
        });

        // Закрытие модального окна
        document.getElementById("closeHelp").addEventListener("click", () => {
            this.hideHelpModal();
        });

        document.getElementById("closeHelpBtn").addEventListener("click", () => {
            this.hideHelpModal();
        });

        // Форма поиска
        document.getElementById("searchForm").addEventListener("submit", (e) => {
            e.preventDefault();
            this.startNewSearch();
        });

        // Загрузка файла - ИСПРАВЛЕНО: используем правильные ID из HTML
        const fileInput = document.getElementById("fileInput");
        const dropZone = document.getElementById("dropzone"); // было dropZone
        const browseFiles = document.getElementById("browseFiles"); // было btnBrowse

        if (browseFiles && fileInput) {
            browseFiles.addEventListener("click", () => {
                fileInput.click();
            });
        }

        if (fileInput) {
            fileInput.addEventListener("change", (e) => {
                if (e.target.files.length > 0) {
                    this.handleFileUpload(e.target.files[0]);
                }
            });
        }

        // Drag & drop
        if (dropZone) {
            dropZone.addEventListener("dragover", (e) => {
                e.preventDefault();
                dropZone.classList.add("drag");
            });

            dropZone.addEventListener("dragleave", () => {
                dropZone.classList.remove("drag");
            });

            dropZone.addEventListener("drop", (e) => {
                e.preventDefault();
                dropZone.classList.remove("drag");

                if (e.dataTransfer.files.length > 0) {
                    this.handleFileUpload(e.dataTransfer.files[0]);
                }
            });
        }

        // Кнопка "Назад к истории"
        const btnBack = document.getElementById("btnBack");
        if (btnBack) {
            btnBack.addEventListener("click", () => {
                this.showView("history");
            });
        }

        // Фильтр по статусу
        this.setupStatusFilter();
    }

    async startNewSearch() {
        const ktru = document.getElementById("ktru").value.trim();
        const title = document.getElementById("title").value.trim();
        const vendor = document.getElementById("vendor").value.trim();
        const region = document.getElementById("region").value;
        const period = document.getElementById("periodYears").value; // было period
        const characteristics = document.getElementById("characteristics").value;

        if (!ktru || !title) {
            this.showToast("Заполните обязательные поля: КТРУ и Наименование", "error");
            return;
        }

        try {
            // Создаем задачу через прямой endpoint
            const response = await fetch(`${this.apiBaseUrl}/tasks/direct`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                credentials: 'include',
                body: JSON.stringify({
                    ktru_code: ktru,
                    product_name: title,
                    vendor: vendor || null,
                    region: region,
                    period_years: parseInt(period),
                    characteristics: this.parseCharacteristics(characteristics)
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const task = await response.json();

            this.showToast(`Задача создана: ${title}`, "success");

            // Сбрасываем форму
            document.getElementById("searchForm").reset();
            this.clearFileUpload();

            // Обновляем историю
            await this.loadTaskHistory();

        } catch (error) {
            console.error("Ошибка создания задачи:", error);
            this.showToast("Ошибка создания задачи", "error");
        }
    }

    parseCharacteristics(text) {
        if (!text.trim()) return [];

        try {
            const parsed = JSON.parse(text);
            if (Array.isArray(parsed)) {
                return parsed.filter(item => item.name && item.value);
            }
            return [];
        } catch (error) {
            console.error("Ошибка парсинга характеристик:", error);
            return [];
        }
    }

    async handleFileUpload(file) {
        if (!file) return;

        // Проверяем размер файла (максимум 10 МБ)
        if (file.size > 10 * 1024 * 1024) {
            this.showToast("Файл слишком большой (максимум 10 МБ)", "error");
            return;
        }

        // Проверяем расширение
        const allowedExtensions = ['.txt', '.csv', '.xlsx'];
        const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
        if (!allowedExtensions.includes(fileExtension)) {
            this.showToast("Неподдерживаемый формат файла. Используйте .txt, .csv или .xlsx", "error");
            return;
        }

        try {
            const formData = new FormData();
            formData.append('file', file);

            const response = await fetch(`${this.apiBaseUrl}/uploads`, {
                method: 'POST',
                body: formData,
                credentials: 'include'
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const result = await response.json();
            this.currentFile = {
                file: file,
                uploadId: result.upload_id,
                detected: result.detected
            };

            // Обновляем список файлов
            this.updateFileList();

            this.showToast(`Файл "${file.name}" успешно загружен`, "success");

            // Автоматически заполняем форму, если есть данные
            if (result.detected) {
                if (result.detected.ktru_code) {
                    document.getElementById("ktru").value = result.detected.ktru_code;
                }
                if (result.detected.name) {
                    document.getElementById("title").value = result.detected.name;
                }
                if (result.detected.vendor) {
                    document.getElementById("vendor").value = result.detected.vendor;
                }
                if (result.detected.characteristics && result.detected.characteristics.length > 0) {
                    document.getElementById("characteristics").value = JSON.stringify(result.detected.characteristics, null, 2);
                }
            }

        } catch (error) {
            console.error("Ошибка загрузки файла:", error);
            this.showToast("Ошибка загрузки файла", "error");
        }
    }

    updateFileList() {
        const fileList = document.getElementById("fileList");
        if (!fileList) return;

        fileList.innerHTML = "";

        if (this.currentFile) {
            const fileItem = document.createElement("div");
            fileItem.className = "fileitem";
            fileItem.innerHTML = `
                <div>
                    <div class="name">${this.currentFile.file.name}</div>
                    <div class="meta">${(this.currentFile.file.size / 1024).toFixed(1)} КБ</div>
                </div>
                <button class="btn btn-sm rm" onclick="nmckSystem.clearFileUpload()">
                    <i class="fas fa-times"></i>
                </button>
            `;
            fileList.appendChild(fileItem);
        }
    }

    clearFileUpload() {
        this.currentFile = null;
        this.updateFileList();
        const fileInput = document.getElementById("fileInput");
        if (fileInput) {
            fileInput.value = "";
        }
    }

    async stopTask(taskId) {
        if (!confirm("Вы уверены, что хотите остановить поиск?")) {
            return;
        }

        try {
            const response = await fetch(`${this.apiBaseUrl}/tasks/${taskId}/stop`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                credentials: 'include',
                body: JSON.stringify({})
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const task = await response.json();
            this.showToast("Поиск остановлен", "success");

            // Обновляем список задач
            this.loadTaskHistory();

        } catch (error) {
            console.error("Ошибка остановки задачи:", error);
            this.showToast(error.message, "error");
        }
    }

    async showTaskResults(taskId) {
        try {
            const response = await fetch(`${this.apiBaseUrl}/tasks/${taskId}`, {
                credentials: 'include'
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const task = await response.json();

            // Сохраняем ID текущей задачи
            this.currentTaskId = taskId;
            localStorage.setItem('nmck_current_task_id', taskId);

            // Переключаемся на экран результатов
            this.showView("detail");

            // Обновляем заголовок
            document.getElementById("detailTitle").textContent = `Результаты поиска: ${task.product_name || "Без названия"}`;
            document.getElementById("detailSubtitle").textContent = `КТРУ: ${task.ktru_code || "Не указан"}`;

            // Загружаем результаты
            await this.loadTaskResults(taskId);

        } catch (error) {
            console.error("Ошибка загрузки результатов задачи:", error);
            this.showToast("Ошибка загрузки результатов", "error");
        }
    }

    async loadTaskResults(taskId) {
        // Здесь должна быть логика загрузки результатов задачи
        // В демо-версии просто показываем заглушку
        const detailContent = document.getElementById("detailContent");
        detailContent.innerHTML = `
            <div style="text-align: center; padding: 40px;">
                <div style="font-size: 48px; color: var(--muted); margin-bottom: 20px;">
                    <i class="fas fa-chart-line"></i>
                </div>
                <h3 style="margin-bottom: 10px;">Результаты загружаются</h3>
                <p style="color: var(--muted);">Функционал просмотра результатов в разработке</p>
            </div>
        `;
    }

    showView(viewName) {
        // Скрываем все view
        document.getElementById("viewHistory").style.display = "none";
        document.getElementById("viewDetail").style.display = "none";

        // Показываем выбранный view
        document.getElementById(`view${viewName.charAt(0).toUpperCase() + viewName.slice(1)}`).style.display = "block";

        // Обновляем навигацию
        document.getElementById("navHistory").setAttribute("aria-pressed", viewName === "history");
        document.getElementById("navDetail").setAttribute("aria-pressed", viewName === "detail");
    }

    showHelpModal() {
        document.getElementById("helpModal").classList.add("open");
    }

    hideHelpModal() {
        document.getElementById("helpModal").classList.remove("open");
    }

    async updateStats() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/tasks/stats`, {
                credentials: 'include'
            });

            if (response.ok) {
                const stats = await response.json();
                this.updateStatsDisplay(stats);
            }
        } catch (error) {
            console.error("Ошибка обновления статистики:", error);
        }
    }

    updateStatsDisplay(stats) {
        const sessionStats = document.getElementById("sessionStats");
        const sessionInfo = document.getElementById("sessionInfo");

        if (sessionStats && sessionInfo) {
            sessionStats.textContent = stats.total_tasks || 0;
            sessionInfo.textContent = `Активных: ${stats.active_tasks || 0}`;
        }
    }

    showToast(message, type = "info") {
        const toasts = document.getElementById("toasts");
        if (!toasts) return;

        const toast = document.createElement("div");
        toast.className = `toast ${type}`;
        toast.innerHTML = `
            <div class="ico">
                ${type === "success" ? "✓" : type === "error" ? "✗" : type === "warn" ? "!" : "i"}
            </div>
            <div>
                <p class="t">${message}</p>
                <p class="d">${new Date().toLocaleTimeString("ru-RU")}</p>
            </div>
            <button class="x" onclick="this.parentElement.remove()">×</button>
        `;

        toasts.appendChild(toast);

        // Автоматическое удаление через 5 секунд
        setTimeout(() => {
            if (toast.parentElement) {
                toast.remove();
            }
        }, 5000);
    }

    updateTaskProgress(data) {
        // Обновляем прогресс в таблице
        const row = document.querySelector(`tr[data-task-id="${data.task_id}"]`);
        if (row) {
            const statusCell = row.querySelector("td:nth-child(3)");
            if (statusCell) {
                statusCell.innerHTML = this.getStatusTag(data.status, data.stage);
            }

            // Обновляем прогресс в детальном view, если открыт
            if (this.currentTaskId === data.task_id) {
                const taskStatus = document.getElementById("taskStatus");
                const taskProgress = document.getElementById("taskProgress");
                if (taskStatus) taskStatus.textContent = this.getStatusLabel(data.status);
                if (taskProgress) taskProgress.textContent = `Прогресс: ${data.progress || 0}%`;
            }
        }
    }

    getStatusLabel(status) {
        const labels = {
            "queued": "В очереди",
            "searching": "Идет поиск",
            "downloading": "Загрузка",
            "analyzing": "Анализ",
            "done": "Готово",
            "error": "Ошибка",
            "cancelled": "Отменено",
            "stopped": "Остановлен"
        };
        return labels[status] || status;
    }
}

// Инициализация при загрузке страницы
let nmckSystem;
document.addEventListener("DOMContentLoaded", () => {
    nmckSystem = new NMCKSystem();
});