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
    }