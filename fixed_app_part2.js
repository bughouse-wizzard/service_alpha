    setupEventHandlers() {
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