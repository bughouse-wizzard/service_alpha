# Полный код бэкенда системы поиска контрактов по КТРУ

## Содержание
1. [app/__init__.py](#appinitpy)
2. [app/adapters/__init__.py](#appadaptersinitpy)
3. [app/adapters/eis/__init__.py](#appadapterseisinitpy)
4. [app/adapters/eis/cache.py](#appadapterseiscachepy)
5. [app/adapters/eis/document_parser.py](#appadapterseisdocumentparserpy)
6. [app/adapters/eis/match_engine.py](#appadapterseismatchenginepy)
7. [app/adapters/eis/normalizer.py](#appadapterseisnormalizerpy)
8. [app/adapters/eis/parser.py](#appadapterseisparserpy)
9. [app/adapters/eis/parser_with_retry.py](#appadapterseisparserwithretrypy)
10. [app/adapters/eis/regions.py](#appadapterseisregionspy)
11. [app/adapters/eis/sync_adapter.py](#appadapterseissyncadapterpy)
12. [app/adapters/eis_parser.py](#appadapterseisparserpy)
13. [app/adapters/file_parser.py](#appadaptersfileparserpy)
14. [app/adapters/match_engine.py](#appadaptersmatchenginepy)
15. [app/adapters/parsers/__init__.py](#appadaptersparsersinitpy)
16. [app/adapters/parsers/file_parser.py](#appadaptersparsersfileparserpy)
17. [app/adapters/parsers/match_engine.py](#appadaptersparsersmatchenginepy)
18. [app/adapters/storage/__init__.py](#appadaptersstorageinitpy)
19. [app/adapters/storage/minio_client.py](#appadaptersstorageminioclientpy)
20. [app/api/__init__.py](#appapiinitpy)
21. [app/api/contract.py](#appapicontractpy)
22. [app/api/results.py](#appapiresultspy)
23. [app/api/selection.py](#appapiselectionpy)
24. [app/api/session.py](#appapisessionpy)
25. [app/api/stop.py](#appapistoppy)
26. [app/api/task.py](#appapitaskpy)
27. [app/api/tasks.py](#appapitaskspy)
28. [app/api/upload.py](#appapiuploadpy)
29. [app/api/websocket.py](#appapiwebsocketpy)
30. [app/application/use_cases/search_contracts.py](#appapplicationusecasessearchcontractspy)
31. [app/dependencies/__init__.py](#appdependenciesinitpy)
32. [app/dependencies/session.py](#appdependenciessessionpy)
33. [app/domain/__init__.py](#appdomaininitpy)
34. [app/domain/entities/__init__.py](#appdomainentitiesinitpy)
35. [app/domain/entities/audit.py](#appdomainentitiesauditpy)
36. [app/domain/entities/base.py](#appdomainentitiesbasepy)
37. [app/domain/entities/calculation.py](#appdomainentitiescalculationpy)
38. [app/domain/entities/contract.py](#appdomainentitiescontractpy)
39. [app/domain/entities/selection.py](#appdomainentitiesselectionpy)
40. [app/domain/entities/session.py](#appdomainentitiessessionpy)
41. [app/domain/entities/task.py](#appdomainentitiestaskpy)
42. [app/domain/entities/upload.py](#appdomainentitiesuploadpy)
43. [app/domain/repositories/__init__.py](#appdomainrepositoriesinitpy)
44. [app/domain/repositories/contract_repository.py](#appdomainrepositoriescontractrepositorypy)
45. [app/domain/repositories/task_repository.py](#appdomainrepositoriestaskrepositorypy)
46. [app/domain/repositories/upload_repository.py](#appdomainrepositoriesuploadrepositorypy)
47. [app/domain/rules/__init__.py](#appdomainrulesinitpy)
48. [app/infra/__init__.py](#appinfrainitpy)
49. [app/infra/celery/__init__.py](#appinfraceleryinitpy)
50. [app/infra/celery/celery_app.py](#appinfraceleryceleryapppy)
51. [app/infra/celery/tasks.py](#appinfracelerytaskspy)
52. [app/infra/config.py](#appinfraconfigpy)
53. [app/infra/database.py](#appinfradatabasepy)
54. [app/infra/logging.py](#appinfraloggingpy)
55. [app/infra/logging/__init__.py](#appinfralogginginitpy)
56. [app/infra/repositories/sqlalchemy_contract_repository.py](#appinfrarepositoriessqlalchemycontractrepositorypy)
57. [app/infra/repositories/sqlalchemy_task_repository.py](#appinfrarepositoriessqlalchemytaskrepositorypy)
58. [app/infra/repositories/sqlalchemy_upload_repository.py](#appinfrarepositoriessqlalchemyuploadrepositorypy)
59. [app/main.py](#appmainpy)
60. [app/models/__init__.py](#appmodelsinitpy)
61. [app/models/database.py](#appmodelsdatabasepy)
62. [app/schemas/__init__.py](#appschemasinitpy)
63. [app/schemas/base.py](#appschemasbasepy)
64. [app/schemas/contract.py](#appschemascontractpy)
65. [app/schemas/selection.py](#appschemasselectionpy)
66. [app/schemas/session.py](#appschemassessionpy)
67. [app/schemas/task.py](#appschemastaskpy)
68. [app/schemas/upload.py](#appschemasuploadpy)
69. [app/services/__init__.py](#appservicesinitpy)
70. [app/use_cases/__init__.py](#appusecasesinitpy)
71. [app/workers/celery_app.py](#appworkersceleryapppy)
72. [app/workers/celery_worker.py](#appworkersceleryworkerpy)
73. [app/workers/mock_worker.py](#appworkersmockworkerpy)
74. [app/workers/search_worker.py](#appworkerssearchworkerpy)
75. [app/workers/search_worker_fixed.py](#appworkerssearchworkerfixedpy)
76. [app/workers/search_worker_refactored.py](#appworkerssearchworkerrefactoredpy)
77. [collect_backend.py](#collectbackendpy)
78. [docs/__init__.py](#docsinitpy)
79. [run.py](#runpy)
80. [session_fixed.py](#sessionfixedpy)
81. [tests/__init__.py](#testsinitpy)
82. [tests/e2e/__init__.py](#testse2einitpy)
83. [tests/integration/__init__.py](#testsintegrationinitpy)
84. [tests/unit/__init__.py](#testsunitinitpy)
85. [uuid_fix.py](#uuidfixpy)

---

### Файл: `app/__init__.py`
```python

```

### Файл: `app/adapters/__init__.py`
```python

```

### Файл: `app/adapters/eis/__init__.py`
```python

```

### Файл: `app/adapters/eis/cache.py`
```python
"""
Кэширование результатов парсинга ЕИС
"""
import json
import hashlib
from typing import Any, Optional
from datetime import datetime, timedelta
import redis
import pickle


class EISCache:
    """Кэш для результатов парсинга ЕИС"""
    
    def __init__(self, redis_url: str = "redis://localhost:6379/0", default_ttl: int = 3600):
        """
        Инициализация кэша
        
        Args:
            redis_url: URL Redis сервера
            default_ttl: Время жизни кэша по умолчанию (в секундах)
        """
        self.redis_url = redis_url
        self.default_ttl = default_ttl
        self._redis = None
    
    @property
    def redis(self) -> redis.Redis:
        """Ленивая инициализация Redis клиента"""
        if self._redis is None:
            try:
                self._redis = redis.from_url(self.redis_url, decode_responses=False)
                # Проверяем соединение
                self._redis.ping()
            except Exception as e:
                print(f"Ошибка подключения к Redis: {e}")
                # Создаем заглушку для работы без Redis
                self._redis = None
        return self._redis
    
    def _generate_key(self, prefix: str, *args) -> str:
        """Генерация ключа кэша"""
        key_str = ":".join(str(arg) for arg in args)
        key_hash = hashlib.md5(key_str.encode()).hexdigest()
        return f"eis:{prefix}:{key_hash}"
    
    def cache_search_results(self, search_params: dict, results: list, ttl: Optional[int] = None) -> bool:
        """
        Кэширование результатов поиска
        
        Args:
            search_params: Параметры поиска
            results: Результаты поиска
            ttl: Время жизни кэша (в секундах)
            
        Returns:
            True если успешно, False если ошибка
        """
        if not self.redis:
            return False
        
        try:
            key = self._generate_key("search", json.dumps(search_params, sort_keys=True))
            value = pickle.dumps({
                "results": results,
                "cached_at": datetime.utcnow().isoformat(),
                "params": search_params,
            })
            
            ttl = ttl or self.default_ttl
            self.redis.setex(key, ttl, value)
            return True
            
        except Exception as e:
            print(f"Ошибка кэширования результатов поиска: {e}")
            return False
    
    def get_cached_search_results(self, search_params: dict) -> Optional[list]:
        """
        Получение кэшированных результатов поиска
        
        Args:
            search_params: Параметры поиска
            
        Returns:
            Результаты поиска или None если нет в кэше
        """
        if not self.redis:
            return None
        
        try:
            key = self._generate_key("search", json.dumps(search_params, sort_keys=True))
            cached_data = self.redis.get(key)
            
            if cached_data:
                data = pickle.loads(cached_data)
                # Проверяем актуальность (не старше 1 дня)
                cached_at = datetime.fromisoformat(data["cached_at"])
                if datetime.utcnow() - cached_at < timedelta(days=1):
                    return data["results"]
            
        except Exception as e:
            print(f"Ошибка получения кэшированных результатов: {e}")
        
        return None
    
    def cache_contract_details(self, contract_url: str, details: dict, ttl: Optional[int] = None) -> bool:
        """
        Кэширование деталей контракта
        
        Args:
            contract_url: URL контракта
            details: Детали контракта
            ttl: Время жизни кэша (в секундах)
            
        Returns:
            True если успешно, False если ошибка
        """
        if not self.redis:
            return False
        
        try:
            key = self._generate_key("contract", contract_url)
            value = pickle.dumps({
                "details": details,
                "cached_at": datetime.utcnow().isoformat(),
                "url": contract_url,
            })
            
            ttl = ttl or (self.default_ttl * 24)  # Для контрактов кэшируем дольше
            self.redis.setex(key, ttl, value)
            return True
            
        except Exception as e:
            print(f"Ошибка кэширования деталей контракта: {e}")
            return False
    
    def get_cached_contract_details(self, contract_url: str) -> Optional[dict]:
        """
        Получение кэшированных деталей контракта
        
        Args:
            contract_url: URL контракта
            
        Returns:
            Детали контракта или None если нет в кэше
        """
        if not self.redis:
            return None
        
        try:
            key = self._generate_key("contract", contract_url)
            cached_data = self.redis.get(key)
            
            if cached_data:
                data = pickle.loads(cached_data)
                # Проверяем актуальность (не старше 7 дней)
                cached_at = datetime.fromisoformat(data["cached_at"])
                if datetime.utcnow() - cached_at < timedelta(days=7):
                    return data["details"]
            
        except Exception as e:
            print(f"Ошибка получения кэшированных деталей контракта: {e}")
        
        return None
    
    def cache_specification(self, contract_url: str, specification: str, ttl: Optional[int] = None) -> bool:
        """
        Кэширование спецификации контракта
        
        Args:
            contract_url: URL контракта
            specification: Спецификация (HTML/текст)
            ttl: Время жизни кэша (в секундах)
            
        Returns:
            True если успешно, False если ошибка
        """
        if not self.redis:
            return False
        
        try:
            key = self._generate_key("spec", contract_url)
            value = pickle.dumps({
                "specification": specification,
                "cached_at": datetime.utcnow().isoformat(),
                "url": contract_url,
            })
            
            ttl = ttl or (self.default_ttl * 24)
            self.redis.setex(key, ttl, value)
            return True
            
        except Exception as e:
            print(f"Ошибка кэширования спецификации: {e}")
            return False
    
    def get_cached_specification(self, contract_url: str) -> Optional[str]:
        """
        Получение кэшированной спецификации
        
        Args:
            contract_url: URL контракта
            
        Returns:
            Спецификация или None если нет в кэше
        """
        if not self.redis:
            return None
        
        try:
            key = self._generate_key("spec", contract_url)
            cached_data = self.redis.get(key)
            
            if cached_data:
                data = pickle.loads(cached_data)
                # Проверяем актуальность (не старше 7 дней)
                cached_at = datetime.fromisoformat(data["cached_at"])
                if datetime.utcnow() - cached_at < timedelta(days=7):
                    return data["specification"]
            
        except Exception as e:
            print(f"Ошибка получения кэшированной спецификации: {e}")
        
        return None
    
    def invalidate_search_cache(self, search_params: dict) -> bool:
        """
        Инвалидация кэша поиска
        
        Args:
            search_params: Параметры поиска
            
        Returns:
            True если успешно, False если ошибка
        """
        if not self.redis:
            return False
        
        try:
            key = self._generate_key("search", json.dumps(search_params, sort_keys=True))
            self.redis.delete(key)
            return True
            
        except Exception as e:
            print(f"Ошибка инвалидации кэша поиска: {e}")
            return False
    
    def invalidate_contract_cache(self, contract_url: str) -> bool:
        """
        Инвалидация кэша контракта
        
        Args:
            contract_url: URL контракта
            
        Returns:
            True если успешно, False если ошибка
        """
        if not self.redis:
            return False
        
        try:
            # Удаляем все кэши связанные с контрактом
            patterns = [
                self._generate_key("contract", contract_url),
                self._generate_key("spec", contract_url),
            ]
            
            for pattern in patterns:
                self.redis.delete(pattern)
            
            return True
            
        except Exception as e:
            print(f"Ошибка инвалидации кэша контракта: {e}")
            return False
    
    def clear_all_cache(self) -> bool:
        """
        Очистка всего кэша
        
        Returns:
            True если успешно, False если ошибка
        """
        if not self.redis:
            return False
        
        try:
            # Удаляем все ключи с префиксом eis:
            keys = self.redis.keys("eis:*")
            if keys:
                self.redis.delete(*keys)
            return True
            
        except Exception as e:
            print(f"Ошибка очистки кэша: {e}")
            return False
    
    def get_cache_stats(self) -> dict:
        """
        Получение статистики кэша
        
        Returns:
            Словарь со статистикой
        """
        if not self.redis:
            return {"error": "Redis не доступен"}
        
        try:
            stats = {
                "total_keys": 0,
                "search_keys": 0,
                "contract_keys": 0,
                "spec_keys": 0,
            }
            
            # Считаем ключи по типам
            for key_type in ["search", "contract", "spec"]:
                pattern = f"eis:{key_type}:*"
                keys = self.redis.keys(pattern)
                count = len(keys)
                
                if key_type == "search":
                    stats["search_keys"] = count
                elif key_type == "contract":
                    stats["contract_keys"] = count
                elif key_type == "spec":
                    stats["spec_keys"] = count
                
                stats["total_keys"] += count
            
            return stats
            
        except Exception as e:
            print(f"Ошибка получения статистики кэша: {e}")
            return {"error": str(e)}
```

### Файл: `app/adapters/eis/document_parser.py`
```python
"""
Парсер печатных форм контрактов (PDF, DOCX)
"""
import re
import io
from typing import List, Dict, Any, Optional
from datetime import datetime


class DocumentParser:
    """Парсер документов печатных форм"""
    
    @staticmethod
    def parse_pdf_content(pdf_content: bytes) -> Dict[str, Any]:
        """
        Парсинг PDF документа
        
        Args:
            pdf_content: Байты PDF файла
            
        Returns:
            Словарь с извлеченными данными
        """
        try:
            # Для парсинга PDF нужна библиотека PyPDF2 или pdfplumber
            # В MVP используем упрощенный подход
            import PyPDF2
            
            pdf_file = io.BytesIO(pdf_content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            
            return DocumentParser._extract_data_from_text(text)
            
        except ImportError:
            # Если PyPDF2 не установлен, возвращаем пустой результат
            print("Предупреждение: PyPDF2 не установлен, парсинг PDF недоступен")
            return {"text": "", "characteristics": []}
        except Exception as e:
            print(f"Ошибка при парсинге PDF: {e}")
            return {"text": "", "characteristics": []}
    
    @staticmethod
    def parse_docx_content(docx_content: bytes) -> Dict[str, Any]:
        """
        Парсинг DOCX документа
        
        Args:
            docx_content: Байты DOCX файла
            
        Returns:
            Словарь с извлеченными данными
        """
        try:
            # Для парсинга DOCX нужна библиотека python-docx
            import docx
            
            docx_file = io.BytesIO(docx_content)
            doc = docx.Document(docx_file)
            
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            
            # Также извлекаем таблицы
            for table in doc.tables:
                for row in table.rows:
                    for cell in row.cells:
                        text += cell.text + " | "
                    text += "\n"
            
            return DocumentParser._extract_data_from_text(text)
            
        except ImportError:
            print("Предупреждение: python-docx не установлен, парсинг DOCX недоступен")
            return {"text": "", "characteristics": []}
        except Exception as e:
            print(f"Ошибка при парсинге DOCX: {e}")
            return {"text": "", "characteristics": []}
    
    @staticmethod
    def _extract_data_from_text(text: str) -> Dict[str, Any]:
        """
        Извлечение данных из текста документа
        
        Args:
            text: Текст документа
            
        Returns:
            Словарь с извлеченными данными
        """
        characteristics = []
        
        # Паттерны для извлечения характеристик
        patterns = [
            # Характеристики товара
            (r"(?:Наименование|Название|Товар)[:\s]+(.+?)(?:\n|$)", "name"),
            (r"(?:Модель|Артикул|Код)[:\s]+(.+?)(?:\n|$)", "model"),
            (r"(?:Производитель|Вендор|Бренд|Изготовитель)[:\s]+(.+?)(?:\n|$)", "vendor"),
            (r"(?:Страна производства|Страна)[:\s]+(.+?)(?:\n|$)", "country"),
            
            # Технические характеристики
            (r"(?:ОЗУ|RAM|оперативная память)[:\s]+([\d\.]+)\s*(?:GB|ГБ|MB|МБ)", "ram"),
            (r"(?:SSD|HDD|жесткий диск|накопитель)[:\s]+([\d\.]+)\s*(?:GB|ГБ|TB|ТБ)", "storage"),
            (r"(?:Процессор|CPU)[:\s]+(.+?)(?:\n|$)", "cpu"),
            (r"(?:Частота процессора)[:\s]+([\d\.]+)\s*(?:GHz|ГГц)", "cpu_frequency"),
            (r"(?:Диагональ|Экран|Screen)[:\s]+([\d\.]+)\s*(?:дюйм|inch|\")", "screen_size"),
            (r"(?:Разрешение|Resolution)[:\s]+(.+?)(?:\n|$)", "resolution"),
            (r"(?:ОС|Операционная система|OS)[:\s]+(.+?)(?:\n|$)", "os"),
            (r"(?:Вес|Масса)[:\s]+([\d\.]+)\s*(?:кг|kg|г|g)", "weight"),
            (r"(?:Цвет|Color)[:\s]+(.+?)(?:\n|$)", "color"),
            
            # Цена и количество
            (r"(?:Цена|Стоимость)[:\s]+([\d\s,]+)\s*(?:руб|₽|RUB)", "price"),
            (r"(?:Количество|Кол-во|Amount)[:\s]+([\d\s,]+)", "quantity"),
            (r"(?:Единица измерения|Ед\. изм\.)[:\s]+(.+?)(?:\n|$)", "unit"),
            
            # Контрактные данные
            (r"(?:Номер контракта|№ контракта)[:\s]+(.+?)(?:\n|$)", "contract_number"),
            (r"(?:Дата заключения|Дата контракта)[:\s]+(\d{2}\.\d{2}\.\d{4})", "contract_date"),
            (r"(?:Поставщик|Исполнитель)[:\s]+(.+?)(?:\n|$)", "supplier"),
            (r"(?:ИНН)[:\s]+(\d{10,12})", "inn"),
        ]
        
        for pattern, key in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    value = match[0]
                else:
                    value = match
                
                if value and value.strip():
                    characteristics.append({
                        "key": key,
                        "value": value.strip(),
                        "source": "printed_form",
                    })
        
        # Также ищем таблицы с характеристиками
        table_patterns = [
            r"(\w.+?)\s+(\d+[\.,]?\d*)\s*(\w*)",  # Название значение единица
            r"(.+?):\s*(.+)",  # Ключ: значение
        ]
        
        for pattern in table_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                if len(match) >= 2:
                    key = match[0].strip()
                    value = match[1].strip()
                    
                    if key and value and len(key) < 50:
                        # Нормализуем ключ
                        key_norm = DocumentParser._normalize_key(key)
                        if key_norm:
                            characteristics.append({
                                "key": key_norm,
                                "value": value,
                                "source": "printed_form_table",
                            })
        
        return {
            "text": text,
            "characteristics": characteristics,
        }
    
    @staticmethod
    def _normalize_key(key: str) -> str:
        """Нормализация ключа характеристики"""
        
        key = key.lower().strip()
        
        # Словарь синонимов
        synonyms = {
            "оперативная память": "ram",
            "озу": "ram",
            "ram": "ram",
            "жесткий диск": "storage",
            "ssd": "storage",
            "hdd": "storage",
            "накопитель": "storage",
            "процессор": "cpu",
            "cpu": "cpu",
            "диагональ": "screen_size",
            "экран": "screen_size",
            "screen": "screen_size",
            "операционная система": "os",
            "ос": "os",
            "производитель": "vendor",
            "вендор": "vendor",
            "бренд": "vendor",
            "изготовитель": "vendor",
            "модель": "model",
            "артикул": "model",
            "код": "model",
            "цвет": "color",
            "вес": "weight",
            "масса": "weight",
            "цена": "price",
            "стоимость": "price",
            "количество": "quantity",
            "кол-во": "quantity",
            "единица измерения": "unit",
            "ед. изм.": "unit",
        }
        
        # Проверяем точное совпадение
        if key in synonyms:
            return synonyms[key]
        
        # Проверяем частичное совпадение
        for synonym, normalized in synonyms.items():
            if synonym in key or key in synonym:
                return normalized
        
        # Если ключ короткий и содержит только буквы, оставляем как есть
        if len(key) < 30 and re.match(r'^[а-яa-z\s]+$', key, re.IGNORECASE):
            return key
        
        return ""
```

### Файл: `app/adapters/eis/match_engine.py`
```python
"""
Match Engine для сравнения характеристик
"""
import re
from typing import Dict, Any, List, Optional, Tuple
from difflib import SequenceMatcher
from decimal import Decimal


class MatchEngine:
    """Движок для сравнения характеристик"""
    
    def __init__(self):
        # Веса характеристик для расчета совпадения
        self.characteristic_weights = {
            "ram": 10,
            "storage": 8,
            "cpu": 9,
            "screen_size": 7,
            "os": 6,
            "vendor": 5,
            "model": 4,
            "resolution": 3,
            "weight": 2,
            "color": 1,
            "country": 1,
        }
        
        # Допустимые отклонения для числовых характеристик
        self.tolerances = {
            "ram": 0.1,  # 10%
            "storage": 0.15,  # 15%
            "screen_size": 0.05,  # 5%
            "weight": 0.2,  # 20%
        }
        
        # Синонимы для вендоров
        self.vendor_synonyms = {
            "dell": ["dell inc.", "dell technologies", "dell computer"],
            "hp": ["hewlett packard", "hp inc.", "hewlett-packard"],
            "lenovo": ["lenovo group", "lenovo china"],
            "asus": ["asustek computer", "asus computer"],
            "acer": ["acer inc.", "acer computer"],
            "apple": ["apple inc.", "apple computer"],
            "samsung": ["samsung electronics", "samsung group"],
            "huawei": ["huawei technologies", "huawei device"],
            "xiaomi": ["xiaomi corporation", "xiaomi tech"],
            "microsoft": ["microsoft corporation", "microsoft inc."],
        }
    
    def calculate_match_score(
        self,
        required_characteristics: List[Dict[str, Any]],
        found_characteristics: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Расчет процента совпадения характеристик
        
        Args:
            required_characteristics: Требуемые характеристики
            found_characteristics: Найденные характеристики
            
        Returns:
            Результат сравнения
        """
        if not required_characteristics or not found_characteristics:
            return {
                "match_percent": 0.0,
                "match_type": "no_match",
                "matched_characteristics": [],
                "missing_characteristics": required_characteristics.copy() if required_characteristics else [],
                "vendor_match": "unknown",
            }
        
        # Нормализуем характеристики
        norm_required = self._normalize_characteristics(required_characteristics)
        norm_found = self._normalize_characteristics(found_characteristics)
        
        # Сравниваем характеристики
        comparison = self._compare_characteristics(norm_required, norm_found)
        
        # Рассчитываем процент совпадения
        total_weight = sum(self.characteristic_weights.get(char.get("key_normalized", ""), 1) 
                          for char in norm_required)
        
        if total_weight == 0:
            match_percent = 0.0
        else:
            matched_weight = sum(
                self.characteristic_weights.get(char.get("key_normalized", ""), 1)
                for char in comparison["matched"]
            )
            match_percent = (matched_weight / total_weight) * 100
        
        # Определяем тип совпадения
        if match_percent >= 95:
            match_type = "identical"
        elif match_percent >= 70:
            match_type = "homogeneous"
        else:
            match_type = "partial"
        
        # Проверяем совпадение вендора
        vendor_match = self._check_vendor_match(norm_required, norm_found)
        
        return {
            "match_percent": round(match_percent, 2),
            "match_type": match_type,
            "matched_characteristics": comparison["matched"],
            "missing_characteristics": comparison["missing"],
            "different_characteristics": comparison["different"],
            "vendor_match": vendor_match,
            "total_required": len(norm_required),
            "total_matched": len(comparison["matched"]),
        }
    
    def _normalize_characteristics(self, characteristics: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Нормализация характеристик для сравнения"""
        normalized = []
        
        for char in characteristics:
            norm_char = char.copy()
            
            # Нормализуем ключ
            key = char.get("key", "")
            if isinstance(key, str):
                norm_char["key_normalized"] = self._normalize_key(key)
            
            # Нормализуем значение
            value = char.get("value", "")
            if isinstance(value, str):
                norm_char["value_normalized"] = self._normalize_value(value, norm_char.get("key_normalized", ""))
            
            normalized.append(norm_char)
        
        return normalized
    
    def _normalize_key(self, key: str) -> str:
        """Нормализация ключа характеристики"""
        key = key.lower().strip()
        
        # Базовые синонимы
        synonyms = {
            "оперативная память": "ram",
            "озу": "ram",
            "ram": "ram",
            "жесткий диск": "storage",
            "ssd": "storage",
            "hdd": "storage",
            "накопитель": "storage",
            "процессор": "cpu",
            "cpu": "cpu",
            "диагональ": "screen_size",
            "экран": "screen_size",
            "screen": "screen_size",
            "операционная система": "os",
            "ос": "os",
            "os": "os",
            "производитель": "vendor",
            "вендор": "vendor",
            "бренд": "vendor",
            "изготовитель": "vendor",
            "модель": "model",
            "артикул": "model",
            "код": "model",
            "цвет": "color",
            "вес": "weight",
            "масса": "weight",
            "страна": "country",
            "разрешение": "resolution",
        }
        
        # Проверяем точное совпадение
        if key in synonyms:
            return synonyms[key]
        
        # Проверяем частичное совпадение
        for synonym, normalized in synonyms.items():
            if synonym in key or key in synonym:
                return normalized
        
        return key
    
    def _normalize_value(self, value: str, key: str = "") -> Any:
        """Нормализация значения характеристики"""
        value = value.strip()
        
        # Для числовых значений
        if re.match(r'^\d+[\.,]?\d*$', value):
            try:
                return float(value.replace(',', '.'))
            except:
                pass
        
        # Для значений с единицами измерения
        unit_patterns = [
            (r'(\d+[\.,]?\d*)\s*(GB|ГБ)', 'gb'),
            (r'(\d+[\.,]?\d*)\s*(MB|МБ)', 'mb'),
            (r'(\d+[\.,]?\d*)\s*(TB|ТБ)', 'tb'),
            (r'(\d+[\.,]?\d*)\s*(GHz|ГГц)', 'ghz'),
            (r'(\d+[\.,]?\d*)\s*(дюйм|inch|"|\'\')', 'inch'),
            (r'(\d+[\.,]?\d*)\s*(кг|kg)', 'kg'),
            (r'(\d+[\.,]?\d*)\s*(г|g)', 'g'),
        ]
        
        for pattern, unit in unit_patterns:
            match = re.search(pattern, value, re.IGNORECASE)
            if match:
                try:
                    num = float(match.group(1).replace(',', '.'))
                    return {"value": num, "unit": unit}
                except:
                    pass
        
        return value.lower()
    
    def _compare_characteristics(
        self, 
        required: List[Dict[str, Any]], 
        found: List[Dict[str, Any]]
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Сравнение характеристик"""
        matched = []
        missing = []
        different = []
        
        # Создаем словарь найденных характеристик по нормализованным ключам
        found_dict = {}
        for char in found:
            key = char.get("key_normalized", "")
            if key:
                found_dict[key] = char
        
        for req_char in required:
            req_key = req_char.get("key_normalized", "")
            req_value = req_char.get("value_normalized", "")
            
            if not req_key:
                continue
            
            if req_key in found_dict:
                found_char = found_dict[req_key]
                found_value = found_char.get("value_normalized", "")
                
                # Сравниваем значения
                if self._values_match(req_value, found_value, req_key):
                    matched_char = req_char.copy()
                    matched_char["found_value"] = found_value
                    matched_char["found_original"] = found_char.get("value", "")
                    matched.append(matched_char)
                else:
                    diff_char = req_char.copy()
                    diff_char["found_value"] = found_value
                    diff_char["found_original"] = found_char.get("value", "")
                    diff_char["difference"] = self._calculate_difference(req_value, found_value)
                    different.append(diff_char)
            else:
                missing.append(req_char)
        
        return {
            "matched": matched,
            "missing": missing,
            "different": different,
        }
    
    def _values_match(self, req_value: Any, found_value: Any, key: str) -> bool:
        """Проверка совпадения значений"""
        if req_value is None or found_value is None:
            return False
        
        # Для числовых значений
        if isinstance(req_value, (int, float)) and isinstance(found_value, (int, float)):
            tolerance = self.tolerances.get(key, 0.1)
            if req_value == 0:
                return found_value == 0
            diff = abs(req_value - found_value) / req_value
            return diff <= tolerance
        
        # Для значений с единицами измерения
        if isinstance(req_value, dict) and isinstance(found_value, dict):
            if req_value.get("unit") == found_value.get("unit"):
                req_num = req_value.get("value")
                found_num = found_value.get("value")
                if isinstance(req_num, (int, float)) and isinstance(found_num, (int, float)):
                    tolerance = self.tolerances.get(key, 0.1)
                    if req_num == 0:
                        return found_num == 0
                    diff = abs(req_num - found_num) / req_num
                    return diff <= tolerance
        
        # Для строковых значений
        if isinstance(req_value, str) and isinstance(found_value, str):
            similarity = SequenceMatcher(None, req_value.lower(), found_value.lower()).ratio()
            return similarity >= 0.8
        
        # Для сравнения строки с числом
        if isinstance(req_value, str) and isinstance(found_value, (int, float)):
            try:
                req_num = float(req_value.replace(',', '.'))
                tolerance = self.tolerances.get(key, 0.1)
                if req_num == 0:
                    return found_value == 0
                diff = abs(req_num - found_value) / req_num
                return diff <= tolerance
            except:
                return False
        
        return str(req_value).lower() == str(found_value).lower()
    
    def _calculate_difference(self, req_value: Any, found_value: Any) -> str:
        """Расчет разницы между значениями"""
        if isinstance(req_value, (int, float)) and isinstance(found_value, (int, float)):
            if req_value == 0:
                return "100%" if found_value != 0 else "0%"
            diff_percent = abs(req_value - found_value) / req_value * 100
            return f"{diff_percent:.1f}%"
        
        return "разные значения"
    
    def _check_vendor_match(
        self, 
        required: List[Dict[str, Any]], 
        found: List[Dict[str, Any]]
    ) -> str:
        """Проверка совпадения вендора"""
        # Ищем вендор в требуемых характеристиках
        req_vendor = None
        for char in required:
            if char.get("key_normalized") == "vendor":
                req_vendor = char.get("value", "")
                break
        
        # Ищем вендор в найденных характеристиках
        found_vendor = None
        for char in found:
            if char.get("key_normalized") == "vendor":
                found_vendor = char.get("value", "")
                break
        
        if not req_vendor or not found_vendor:
            return "unknown"
        
        req_vendor_lower = req_vendor.lower().strip()
        found_vendor_lower = found_vendor.lower().strip()
        
        # Проверяем точное совпадение
        if req_vendor_lower == found_vendor_lower:
            return "match"
        
        # Проверяем синонимы
        for vendor, synonyms in self.vendor_synonyms.items():
            if (req_vendor_lower == vendor or req_vendor_lower in synonyms) and \
               (found_vendor_lower == vendor or found_vendor_lower in synonyms):
                return "match"
        
        # Проверяем частичное совпадение
        if req_vendor_lower in found_vendor_lower or found_vendor_lower in req_vendor_lower:
            return "partial"
        
        # Проверяем схожесть
        similarity = SequenceMatcher(None, req_vendor_lower, found_vendor_lower).ratio()
        if similarity >= 0.7:
            return "partial"
        
        return "mismatch"
    
    def create_audit_log(
        self,
        required_characteristics: List[Dict[str, Any]],
        found_characteristics: List[Dict[str, Any]],
        match_result: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        """
        Создание лога сверки
        
        Args:
            required_characteristics: Требуемые характеристики
            found_characteristics: Найденные характеристики
            match_result: Результат сравнения
            
        Returns:
            Лог сверки
        """
        audit_log = []
        
        # Добавляем совпадающие характеристики
        for matched in match_result.get("matched_characteristics", []):
            audit_log.append({
                "key": matched.get("key", ""),
                "expected_value": matched.get("value", ""),
                "found_value": matched.get("found_original", ""),
                "is_diff": False,
                "diff_reason": "",
                "match_type": "identical",
            })
        
        # Добавляем разные характеристики
        for different in match_result.get("different_characteristics", []):
            audit_log.append({
                "key": different.get("key", ""),
                "expected_value": different.get("value", ""),
                "found_value": different.get("found_original", ""),
                "is_diff": True,
                "diff_reason": different.get("difference", "разные значения"),
                "match_type": "different",
            })
        
        # Добавляем отсутствующие характеристики
        for missing in match_result.get("missing_characteristics", []):
            audit_log.append({
                "key": missing.get("key", ""),
                "expected_value": missing.get("value", ""),
                "found_value": "",
                "is_diff": True,
                "diff_reason": "отсутствует",
                "match_type": "missing",
            })
        
        # Добавляем вендор
        vendor_match = match_result.get("vendor_match", "unknown")
        if vendor_match != "unknown":
            audit_log.append({
                "key": "Производитель",
                "expected_value": self._get_vendor_from_characteristics(required_characteristics),
                "found_value": self._get_vendor_from_characteristics(found_characteristics),
                "is_diff": vendor_match != "match",
                "diff_reason": "не совпадает" if vendor_match != "match" else "",
                "match_type": "vendor",
            })
        
        return audit_log
    
    def _get_vendor_from_characteristics(self, characteristics: List[Dict[str, Any]]) -> str:
        """Получение вендора из характеристик"""
        for char in characteristics:
            if char.get("key", "").lower() in ["производитель", "вендор", "vendor", "бренд"]:
                return char.get("value", "")
        return ""
```

### Файл: `app/adapters/eis/normalizer.py`
```python
"""
Нормализация данных из ЕИС
"""
import re
from datetime import datetime
from typing import Dict, Any, Optional, List
from decimal import Decimal, ROUND_HALF_UP


class DataNormalizer:
    """Нормализация данных контрактов"""
    
    @staticmethod
    def normalize_price(price_text: str, currency: str = "RUB") -> Dict[str, Any]:
        """
        Нормализация цены
        
        Args:
            price_text: Текст с ценой
            currency: Валюта (по умолчанию RUB)
            
        Returns:
            Нормализованная цена
        """
        if not price_text:
            return {"value": 0.0, "currency": currency, "original": price_text}
        
        # Убираем все нецифровые символы кроме точки, запятой и пробелов
        cleaned = re.sub(r'[^\d\s,.]', '', price_text)
        
        # Заменяем запятую на точку
        cleaned = cleaned.replace(',', '.')
        
        # Убираем пробелы (разделители тысяч)
        cleaned = cleaned.replace(' ', '')
        
        try:
            # Пробуем преобразовать в Decimal для точности
            value = Decimal(cleaned)
            # Округляем до 2 знаков после запятой
            value = value.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            float_value = float(value)
            
            return {
                "value": float_value,
                "currency": currency,
                "original": price_text,
                "normalized": True,
            }
        except:
            # Если не удалось преобразовать, пробуем найти числа в тексте
            numbers = re.findall(r'[\d\s,]+', price_text)
            if numbers:
                try:
                    num = numbers[0].replace(' ', '').replace(',', '.')
                    value = Decimal(num).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
                    return {
                        "value": float(value),
                        "currency": currency,
                        "original": price_text,
                        "normalized": True,
                    }
                except:
                    pass
        
        return {"value": 0.0, "currency": currency, "original": price_text, "normalized": False}
    
    @staticmethod
    def normalize_date(date_text: str) -> Optional[datetime]:
        """
        Нормализация даты
        
        Args:
            date_text: Текст с датой
            
        Returns:
            Нормализованная дата или None
        """
        if not date_text:
            return None
        
        date_text = date_text.strip()
        
        # Паттерны дат
        patterns = [
            # DD.MM.YYYY
            (r'(\d{2})\.(\d{2})\.(\d{4})', '%d.%m.%Y'),
            # DD/MM/YYYY
            (r'(\d{2})/(\d{2})/(\d{4})', '%d/%m/%Y'),
            # YYYY-MM-DD
            (r'(\d{4})-(\d{2})-(\d{2})', '%Y-%m-%d'),
            # DD.MM.YY
            (r'(\d{2})\.(\d{2})\.(\d{2})', '%d.%m.%y'),
        ]
        
        for pattern, date_format in patterns:
            match = re.search(pattern, date_text)
            if match:
                try:
                    date_str = match.group()
                    return datetime.strptime(date_str, date_format)
                except ValueError:
                    continue
        
        # Пробуем извлечь дату из текста
        day_match = re.search(r'\b(\d{1,2})\b', date_text)
        month_match = re.search(r'\b(янв|фев|мар|апр|май|июн|июл|авг|сен|окт|ноя|дек|января|февраля|марта|апреля|мая|июня|июля|августа|сентября|октября|ноября|декабря)\b', date_text, re.IGNORECASE)
        year_match = re.search(r'\b(20\d{2})\b', date_text)
        
        if day_match and month_match and year_match:
            try:
                day = int(day_match.group())
                month_str = month_match.group().lower()
                year = int(year_match.group())
                
                # Преобразуем месяц
                month_map = {
                    'янв': 1, 'января': 1,
                    'фев': 2, 'февраля': 2,
                    'мар': 3, 'марта': 3,
                    'апр': 4, 'апреля': 4,
                    'май': 5, 'мая': 5,
                    'июн': 6, 'июня': 6,
                    'июл': 7, 'июля': 7,
                    'авг': 8, 'августа': 8,
                    'сен': 9, 'сентября': 9,
                    'окт': 10, 'октября': 10,
                    'ноя': 11, 'ноября': 11,
                    'дек': 12, 'декабря': 12,
                }
                
                month = month_map.get(month_str)
                if month:
                    return datetime(year, month, day)
            except:
                pass
        
        return None
    
    @staticmethod
    def normalize_characteristic_value(value: str, key: str = "") -> Dict[str, Any]:
        """
        Нормализация значения характеристики
        
        Args:
            value: Значение характеристики
            key: Ключ характеристики (для контекста)
            
        Returns:
            Нормализованное значение
        """
        if not value:
            return {"original": value, "normalized": value, "type": "string"}
        
        value = value.strip()
        
        # Определяем тип значения
        value_lower = value.lower()
        key_lower = key.lower() if key else ""
        
        # Проверяем, является ли числом
        if re.match(r'^-?\d+[\.,]?\d*$', value):
            # Это число
            try:
                num_value = float(value.replace(',', '.'))
                return {
                    "original": value,
                    "normalized": num_value,
                    "type": "number",
                }
            except:
                pass
        
        # Проверяем, содержит ли единицы измерения
        unit_patterns = [
            (r'(\d+[\.,]?\d*)\s*(GB|ГБ|MB|МБ|TB|ТБ)', 'storage'),
            (r'(\d+[\.,]?\d*)\s*(GHz|ГГц|MHz|МГц)', 'frequency'),
            (r'(\d+[\.,]?\d*)\s*(дюйм|inch|"|\'\')', 'size'),
            (r'(\d+[\.,]?\d*)\s*(кг|kg|г|g)', 'weight'),
            (r'(\d+[\.,]?\d*)\s*(мм|mm|см|cm|м|m)', 'length'),
            (r'(\d+[\.,]?\d*)\s*(В|V|Вт|W)', 'power'),
        ]
        
        for pattern, unit_type in unit_patterns:
            match = re.search(pattern, value, re.IGNORECASE)
            if match:
                try:
                    num = float(match.group(1).replace(',', '.'))
                    unit = match.group(2)
                    return {
                        "original": value,
                        "normalized": num,
                        "unit": unit,
                        "type": unit_type,
                    }
                except:
                    pass
        
        # Проверяем булевые значения
        bool_map = {
            'да': True, 'yes': True, 'true': True, '1': True, 'есть': True,
            'нет': False, 'no': False, 'false': False, '0': False, 'нету': False,
        }
        
        if value_lower in bool_map:
            return {
                "original": value,
                "normalized": bool_map[value_lower],
                "type": "boolean",
            }
        
        # Для строковых значений нормализуем регистр
        if value.isupper():
            normalized = value.title()
        elif value.islower():
            normalized = value.capitalize()
        else:
            normalized = value
        
        return {
            "original": value,
            "normalized": normalized,
            "type": "string",
        }
    
    @staticmethod
    def normalize_characteristic_key(key: str) -> str:
        """
        Нормализация ключа характеристики
        
        Args:
            key: Ключ характеристики
            
        Returns:
            Нормализованный ключ
        """
        if not key:
            return ""
        
        key = key.strip().lower()
        
        # Словарь синонимов
        synonyms = {
            # Память
            'оперативная память': 'ram',
            'озу': 'ram',
            'ram': 'ram',
            'память': 'memory',
            
            # Хранилище
            'жесткий диск': 'storage',
            'ssd': 'storage',
            'hdd': 'storage',
            'накопитель': 'storage',
            'диск': 'storage',
            
            # Процессор
            'процессор': 'cpu',
            'cpu': 'cpu',
            'центральный процессор': 'cpu',
            
            # Экран
            'диагональ': 'screen_size',
            'экран': 'screen',
            'screen': 'screen',
            'монитор': 'screen',
            
            # Операционная система
            'операционная система': 'os',
            'ос': 'os',
            'os': 'os',
            
            # Производитель
            'производитель': 'vendor',
            'вендор': 'vendor',
            'бренд': 'vendor',
            'изготовитель': 'vendor',
            'manufacturer': 'vendor',
            
            # Модель
            'модель': 'model',
            'артикул': 'model',
            'код': 'model',
            'article': 'model',
            
            # Цвет
            'цвет': 'color',
            'colour': 'color',
            
            # Вес
            'вес': 'weight',
            'масса': 'weight',
            'weight': 'weight',
            
            # Цена
            'цена': 'price',
            'стоимость': 'price',
            'price': 'price',
            
            # Количество
            'количество': 'quantity',
            'кол-во': 'quantity',
            'amount': 'quantity',
            
            # Единица измерения
            'единица измерения': 'unit',
            'ед. изм.': 'unit',
            'unit': 'unit',
            
            # Разрешение
            'разрешение': 'resolution',
            'resolution': 'resolution',
            
            # Частота
            'частота': 'frequency',
            'frequency': 'frequency',
            
            # Мощность
            'мощность': 'power',
            'power': 'power',
            
            # Габариты
            'габариты': 'dimensions',
            'размеры': 'dimensions',
            'dimensions': 'dimensions',
            
            # Материал
            'материал': 'material',
            'material': 'material',
            
            # Страна
            'страна производства': 'country',
            'страна': 'country',
            'country': 'country',
        }
        
        # Проверяем точное совпадение
        if key in synonyms:
            return synonyms[key]
        
        # Проверяем частичное совпадение
        for synonym, normalized in synonyms.items():
            if synonym in key or key in synonym:
                return normalized
        
        # Если ключ короткий и содержит только буквы, оставляем как есть
        if len(key) < 30 and re.match(r'^[а-яa-z\s]+$', key, re.IGNORECASE):
            # Убираем лишние пробелы и приводим к snake_case
            normalized = key.strip().replace(' ', '_')
            return normalized
        
        return key
    
    @staticmethod
    def normalize_contract_data(contract_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Нормализация всех данных контракта
        
        Args:
            contract_data: Данные контракта
            
        Returns:
            Нормализованные данные контракта
        """
        normalized = contract_data.copy()
        
        # Нормализуем цену
        if "price" in normalized:
            price_data = DataNormalizer.normalize_price(str(normalized["price"]))
            normalized["price_normalized"] = price_data
        
        if "unit_price" in normalized:
            price_data = DataNormalizer.normalize_price(str(normalized["unit_price"]))
            normalized["unit_price_normalized"] = price_data
        
        # Нормализуем даты
        if "date" in normalized and isinstance(normalized["date"], str):
            normalized["date_normalized"] = DataNormalizer.normalize_date(normalized["date"])
        
        if "sign_date" in normalized and isinstance(normalized["sign_date"], str):
            normalized["sign_date_normalized"] = DataNormalizer.normalize_date(normalized["sign_date"])
        
        # Нормализуем характеристики
        if "characteristics" in normalized and isinstance(normalized["characteristics"], list):
            normalized_characteristics = []
            for char in normalized["characteristics"]:
                if isinstance(char, dict):
                    norm_char = char.copy()
                    
                    # Нормализуем ключ
                    if "key" in norm_char:
                        norm_char["key_normalized"] = DataNormalizer.normalize_characteristic_key(norm_char["key"])
                    
                    # Нормализуем значение
                    if "value" in norm_char:
                        key = norm_char.get("key", "")
                        value_data = DataNormalizer.normalize_characteristic_value(str(norm_char["value"]), key)
                        norm_char["value_normalized"] = value_data
                    
                    normalized_characteristics.append(norm_char)
                else:
                    normalized_characteristics.append(char)
            
            normalized["characteristics_normalized"] = normalized_characteristics
        
        # Нормализуем поставщика (убираем лишние пробелы, кавычки)
        if "supplier_name" in normalized and isinstance(normalized["supplier_name"], str):
            supplier = normalized["supplier_name"].strip()
            supplier = re.sub(r'["\']', '', supplier)  # Убираем кавычки
            supplier = re.sub(r'\s+', ' ', supplier)  # Убираем лишние пробелы
            normalized["supplier_name_normalized"] = supplier
        
        # Нормализуем номер контракта
        if "reg_number" in normalized and isinstance(normalized["reg_number"], str):
            reg_num = normalized["reg_number"].strip()
            reg_num = re.sub(r'[№\s]+', '', reg_num)  # Убираем № и пробелы
            normalized["reg_number_normalized"] = reg_num
        
        # Добавляем метку о нормализации
        normalized["_normalized"] = True
        
        return normalized
    
    @staticmethod
    def normalize_search_results(results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Нормализация результатов поиска
        
        Args:
            results: Список контрактов
            
        Returns:
            Нормализованный список контрактов
        """
        normalized_results = []
        
        for contract in results:
            if isinstance(contract, dict):
                normalized_contract = DataNormalizer.normalize_contract_data(contract)
                normalized_results.append(normalized_contract)
            else:
                normalized_results.append(contract)
        
        return normalized_results
```

### Файл: `app/adapters/eis/parser.py`
```python
import asyncio
import re
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import httpx
from bs4 import BeautifulSoup
import urllib.parse
from app.infra.config import settings


class EISParser:
    """Парсер ЕИС zakupki.gov.ru"""
    
    def __init__(self):
        self.base_url = settings.EIS_BASE_URL
        self.search_url = f"{settings.EIS_BASE_URL}/epz/order/extendedsearch/results.html"
        self.client = httpx.AsyncClient(
            timeout=30.0,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-User": "?1",
                "Cache-Control": "max-age=0",
            },
            follow_redirects=True,
            verify=False,  # Отключаем проверку SSL для тестирования
        )
        self.semaphore = asyncio.Semaphore(3)  # Максимум 3 одновременных запроса
    
    async def search_contracts(
        self,
        ktru_code: Optional[str] = None,
        product_name: Optional[str] = None,
        region: str = "Северо-Западный ФО",
        period_from: Optional[datetime] = None,
        period_to: Optional[datetime] = None,
        law_type: str = "44-ФЗ",
        max_results: int = 200,
    ) -> List[Dict[str, Any]]:
        """Поиск контрактов по расширенному поиску"""
        
        # Формируем параметры запроса
        params = self._build_search_params(
            ktru_code=ktru_code,
            product_name=product_name,
            region=region,
            period_from=period_from,
            period_to=period_to,
            law_type=law_type,
        )
        
        contracts = []
        page = 1
        
        try:
            while len(contracts) < max_results:
                # Добавляем параметр страницы
                params["pageNumber"] = page
                
                # Выполняем запрос
                response = await self.client.get(self.search_url, params=params)
                response.raise_for_status()
                
                # Парсим результаты
                page_contracts = await self._parse_search_results(response.text)
                
                if not page_contracts:
                    break
                
                contracts.extend(page_contracts)
                
                # Проверяем, есть ли следующая страница
                if not self._has_next_page(response.text):
                    break
                
                page += 1
                
                # Задержка между запросами
                await asyncio.sleep(settings.EIS_SEARCH_DELAY)
            
            # Ограничиваем количество результатов
            return contracts[:max_results]
            
        except Exception as e:
            print(f"Ошибка при поиске контрактов: {e}")
            return []
    
    async def get_contract_details(self, contract_url: str) -> Dict[str, Any]:
        """Получить детальную информацию о контракте"""
        
        async with self.semaphore:
            try:
                # Загружаем страницу контракта
                response = await self.client.get(contract_url)
                response.raise_for_status()
                
                # Парсим основную информацию
                contract_data = await self._parse_contract_page(response.text)
                contract_data["url"] = contract_url
                
                # Пытаемся получить спецификацию
                try:
                    specification = await self._get_contract_specification(contract_url)
                    if specification:
                        contract_data["specification"] = specification
                        contract_data["characteristics"] = self._extract_characteristics_from_specification(specification)
                except Exception as e:
                    print(f"Ошибка при получении спецификации: {e}")
                
                # Если нет характеристик в спецификации, пробуем скачать печатную форму
                if not contract_data.get("characteristics"):
                    try:
                        printed_form_data = await self._get_printed_form_data(contract_url)
                        if printed_form_data:
                            contract_data["printed_form"] = printed_form_data
                            contract_data["characteristics"] = self._extract_characteristics_from_printed_form(printed_form_data)
                    except Exception as e:
                        print(f"Ошибка при получении печатной формы: {e}")
                
                return contract_data
                
            except Exception as e:
                print(f"Ошибка при получении деталей контракта {contract_url}: {e}")
                return {}
    
    def _build_search_params(
        self,
        ktru_code: Optional[str] = None,
        product_name: Optional[str] = None,
        region: str = "Северо-Западный ФО",
        period_from: Optional[datetime] = None,
        period_to: Optional[datetime] = None,
        law_type: str = "44-ФЗ",
    ) -> Dict[str, Any]:
        """Построить параметры поиска"""
        
        if period_to is None:
            period_to = datetime.now()
        if period_from is None:
            period_from = period_to - timedelta(days=3 * 365)  # 3 года
        
        params = {
            "morphology": "on",
            "search-filter": "Поиск",
            "sortBy": "PUBLISH_DATE",
            "pageNumber": 1,
            "sortDirection": "false",
            "recordsPerPage": "_50",
            "showLotsInfoHidden": "false",
            "fz44": "on" if law_type == "44-ФЗ" else "off",
            "fz223": "on" if law_type == "223-ФЗ" else "off",
            "contractStage": "EXECUTION_COMPLETED,EXECUTION_TERMINATED",
            "contractDateFrom": period_from.strftime("%d.%m.%Y"),
            "contractDateTo": period_to.strftime("%d.%m.%Y"),
            "regionDeleted": "false",
        }
        
        # Добавляем КТРУ код
        if ktru_code:
            params["ktruCodes"] = ktru_code
        
        # Добавляем ключевые слова из названия товара
        if product_name:
            params["searchString"] = product_name
        
        # Добавляем регион (упрощенная реализация)
        if region:
            # В реальной системе нужно мапить регион на код региона ЕИС
            params["regions"] = self._get_region_code(region)
        
        return params
    
    def _get_region_code(self, region_name: str) -> str:
        """Получить код региона ЕИС по названию"""
        # Упрощенная реализация - в реальной системе нужен полный справочник
        region_mapping = {
            "Северо-Западный ФО": "78000000000",
            "Центральный ФО": "77000000000",
            "Южный ФО": "61000000000",
            "Приволжский ФО": "16000000000",
            "Уральский ФО": "66000000000",
            "Сибирский ФО": "24000000000",
            "Дальневосточный ФО": "27000000000",
        }
        return region_mapping.get(region_name, "78000000000")  # По умолчанию СЗФО
    
    async def _parse_search_results(self, html: str) -> List[Dict[str, Any]]:
        """Парсинг результатов поиска (исправленные селекторы)"""
        
        soup = BeautifulSoup(html, "lxml")
        contracts = []
        
        # Ищем блоки с результатами
        result_blocks = soup.find_all("div", class_="search-registry-entry-block")
        
        for block in result_blocks:
            try:
                # Ищем div с классом registry-entry__header-mid__number
                number_div = block.find("div", class_="registry-entry__header-mid__number")
                if not number_div:
                    continue
                
                # Внутри div ищем ссылку
                link_tag = number_div.find("a")
                if not link_tag:
                    continue
                
                contract_url = link_tag.get("href")
                if not contract_url.startswith("http"):
                    contract_url = self.base_url + contract_url
                
                # Извлекаем номер контракта из текста ссылки
                contract_number = link_tag.text.strip()
                # Очищаем номер от лишних символов
                import re
                contract_number = re.sub(r'[№\s]+', '', contract_number)
                
                # Извлекаем поставщика
                supplier_name = ""
                supplier_div = block.find("div", class_="registry-entry__body-href")
                if supplier_div:
                    supplier_link = supplier_div.find("a")
                    if supplier_link:
                        supplier_name = supplier_link.text.strip()
                
                # Извлекаем дату (первая дата в блоке)
                date_str = ""
                date_div = block.find("div", class_="data-block__value")
                if date_div:
                    date_str = date_div.text.strip()
                
                # Извлекаем цену
                price = 0.0
                price_div = block.find("div", class_="price-block__value")
                if price_div:
                    price_text = price_div.text.strip()
                    # Убираем все нецифровые символы кроме точки и запятой
                    price_clean = re.sub(r'[^\d,.]', '', price_text)
                    # Заменяем запятую на точку
                    price_clean = price_clean.replace(',', '.')
                    try:
                        price = float(price_clean)
                    except ValueError:
                        # Пробуем другой подход - ищем числа в тексте
                        numbers = re.findall(r'[\d\s,]+', price_text)
                        if numbers:
                            try:
                                num = numbers[0].replace(' ', '').replace(',', '.')
                                price = float(num)
                            except:
                                pass
                
                # Извлекаем объект закупки
                purchase_object = ""
                object_div = block.find("div", class_="registry-entry__body-value")
                if object_div:
                    purchase_object = object_div.text.strip()[:200]
                
                contracts.append({
                    "url": contract_url,
                    "reg_number": contract_number,
                    "supplier_name": supplier_name,
                    "date": date_str,
                    "price": price,
                    "currency": "RUB",
                    "purchase_object": purchase_object,
                })
                
            except Exception as e:
                print(f"Ошибка при парсинге блока результата: {e}")
                continue
        
        return contracts
    
    def _has_next_page(self, html: str) -> bool:
        """Проверить наличие следующей страницы"""
        
        soup = BeautifulSoup(html, "lxml")
        next_button = soup.find("a", string=re.compile(r"Следующая|>"))
        return next_button is not None
    
    async def _parse_contract_page(self, html: str) -> Dict[str, Any]:
        """Парсинг страницы контракта - улучшенная версия"""
        
        soup = BeautifulSoup(html, "lxml")
        contract_data = {}
        
        try:
            # Извлекаем номер контракта - несколько способов
            # Способ 1: поиск по классу
            number_tag = soup.find("span", class_="cardMainInfo__purchaseLink")
            if not number_tag:
                # Способ 2: поиск по тексту "Реестровый номер"
                number_tag = soup.find(string=re.compile(r"Реестровый номер|Номер контракта"))
                if number_tag:
                    number_tag = number_tag.find_parent()
            
            if number_tag:
                contract_data["reg_number"] = number_tag.text.strip()
            
            # Извлекаем поставщика - несколько способов
            supplier_name = None
            
            # Способ 1: поиск по таблице с более широкими критериями
            supplier_rows = soup.find_all("tr")
            for row in supplier_rows:
                th = row.find("th")
                td = row.find("td")
                if th and td:
                    th_text = th.text.strip().lower()
                    td_text = td.text.strip()
                    
                    # Проверяем различные варианты названия поля
                    if any(keyword in th_text for keyword in ["поставщик", "исполнитель", "подрядчик", "участник"]):
                        if len(td_text) > 5 and len(td_text) < 200:  # Фильтруем слишком короткие/длинные
                            supplier_name = td_text
                            break
            
            # Способ 2: поиск по тексту с регулярными выражениями
            if not supplier_name:
                supplier_patterns = [
                    r"Поставщик[\s:]+([^\n\r<]+)",
                    r"Исполнитель[\s:]+([^\n\r<]+)",
                    r"Подрядчик[\s:]+([^\n\r<]+)",
                    r"Участник[\s:]+([^\n\r<]+)",
                ]
                
                for pattern in supplier_patterns:
                    match = re.search(pattern, soup.text, re.IGNORECASE)
                    if match:
                        candidate = match.group(1).strip()
                        if len(candidate) > 5 and len(candidate) < 200:
                            supplier_name = candidate
                            break
            
            # Способ 3: поиск организаций в тексте (по ключевым словам)
            if not supplier_name:
                org_keywords = ["ООО", "АО", "ПАО", "ГУ", "МУ", "КУ", "ФГУП", "МБУ", "ГАУ"]
                lines = soup.text.split('\n')
                for line in lines:
                    line = line.strip()
                    if any(keyword in line for keyword in org_keywords):
                        if 10 < len(line) < 150:  # Разумная длина для названия организации
                            supplier_name = line
                            break
            
            if supplier_name:
                # Очищаем название от лишних символов
                supplier_name = re.sub(r'\s+', ' ', supplier_name).strip()
                contract_data["supplier_name"] = supplier_name
            
            # Извлекаем ИНН поставщика
            inn_tag = soup.find(string=re.compile(r"ИНН"))
            if inn_tag:
                inn_parent = inn_tag.find_parent()
                if inn_parent:
                    # Ищем ИНН в тексте
                    inn_match = re.search(r"\b\d{10,12}\b", inn_parent.text)
                    if inn_match:
                        contract_data["supplier_inn"] = inn_match.group()
            
            # Извлекаем дату подписания - несколько способов
            date_found = False
            
            # Паттерны для поиска даты
            date_patterns = [
                r"Дата заключения[\s:]+(\d{2}\.\d{2}\.\d{4})",
                r"Дата подписания[\s:]+(\d{2}\.\d{2}\.\d{4})",
                r"Срок действия[\s:]+(\d{2}\.\d{2}\.\d{4})",
                r"Дата[\s:]+(\d{2}\.\d{2}\.\d{4})",
                r"(\d{2}\.\d{2}\.\d{4})\s*г\.",
                r"(\d{2}\.\d{2}\.\d{4})\s*год",
            ]
            
            for pattern in date_patterns:
                date_match = re.search(pattern, soup.text, re.IGNORECASE)
                if date_match:
                    date_str = date_match.group(1)
                    try:
                        contract_data["sign_date"] = datetime.strptime(date_str, "%d.%m.%Y")
                        date_found = True
                        break
                    except ValueError:
                        continue
            
            # Способ 2: поиск в таблицах
            if not date_found:
                date_rows = soup.find_all("tr")
                for row in date_rows:
                    th = row.find("th")
                    td = row.find("td")
                    if th and td:
                        th_text = th.text.strip().lower()
                        if "дата" in th_text:
                            td_text = td.text.strip()
                            date_match = re.search(r"\d{2}\.\d{2}\.\d{4}", td_text)
                            if date_match:
                                try:
                                    contract_data["sign_date"] = datetime.strptime(date_match.group(), "%d.%m.%Y")
                                    date_found = True
                                    break
                                except ValueError:
                                    continue
            
            # Извлекаем цену - несколько способов
            price_found = False
            
            # Способ 1: поиск по тексту
            price_patterns = [
                r"Цена контракта[\s:]+([\d\s,]+(?:\s*[₽руб\.])?)",
                r"Сумма контракта[\s:]+([\d\s,]+(?:\s*[₽руб\.])?)",
                r"Начальная цена[\s:]+([\d\s,]+(?:\s*[₽руб\.])?)",
                r"Цена[\s:]+([\d\s,]+(?:\s*[₽руб\.])?)",
                r"([\d\s,]+)\s*₽",
                r"([\d\s,]+)\s*руб",
            ]
            
            for pattern in price_patterns:
                price_match = re.search(pattern, soup.text, re.IGNORECASE)
                if price_match:
                    price_text = price_match.group(1).strip()
                    try:
                        # Очищаем текст от пробелов и символов валюты
                        clean_price = re.sub(r"[^\d,.]", "", price_text.replace(" ", ""))
                        price = float(clean_price.replace(",", "."))
                        contract_data["unit_price"] = price
                        contract_data["currency"] = "RUB"
                        price_found = True
                        break
                    except ValueError:
                        continue
            
            # Способ 2: поиск в таблицах
            if not price_found:
                price_rows = soup.find_all("tr")
                for row in price_rows:
                    th = row.find("th")
                    td = row.find("td")
                    if th and td:
                        th_text = th.text.strip().lower()
                        if "цена" in th_text or "сумма" in th_text:
                            td_text = td.text.strip()
                            price_match = re.search(r"[\d\s,]+", td_text.replace(" ", ""))
                            if price_match:
                                try:
                                    clean_price = re.sub(r"[^\d,.]", "", price_match.group())
                                    price = float(clean_price.replace(",", "."))
                                    contract_data["unit_price"] = price
                                    contract_data["currency"] = "RUB"
                                    price_found = True
                                    break
                                except ValueError:
                                    continue
            
            # Извлекаем вендора/производителя
            vendor_tag = soup.find(string=re.compile(r"Производитель|Вендор|Бренд|Изготовитель", re.IGNORECASE))
            if vendor_tag:
                vendor_parent = vendor_tag.find_parent()
                if vendor_parent:
                    # Ищем текст после метки
                    vendor_text = vendor_parent.text
                    vendor_match = re.search(r"(?:Производитель|Вендор|Бренд|Изготовитель)[:\s]+([^\n\r]+)", vendor_text, re.IGNORECASE)
                    if vendor_match:
                        contract_data["vendor"] = vendor_match.group(1).strip()
            
            # Пытаемся извлечь характеристики из таблиц на странице
            characteristics = []
            
            # Ищем таблицы с характеристиками
            tables = soup.find_all("table")
            for table in tables:
                rows = table.find_all("tr")
                for row in rows:
                    cells = row.find_all(["td", "th"])
                    if len(cells) >= 2:
                        key = cells[0].text.strip()
                        value = cells[1].text.strip()
                        
                        # Фильтруем очевидные не-характеристики
                        exclude_keywords = [
                            "№", "номер", "дата", "сумма", "цена", "статус", "кбк", "итого", "всего",
                            "счет", "банк", "реквизиты", "платеж", "оплата", "договор", "контракт",
                            "заказчик", "поставщик", "исполнитель", "подрядчик", "участник",
                            "заявка", "предложение", "лот", "извещение", "уведомление"
                        ]
                        
                        key_lower = key.lower()
                        value_lower = value.lower()
                        
                        # Проверяем, не является ли это финансовой или административной информацией
                        is_financial = any(word in key_lower for word in ["₽", "руб", "коп", "долл", "евро", "тенге"])
                        is_administrative = any(word in key_lower for word in exclude_keywords)
                        is_numeric_key = re.match(r"^\d+$", key)
                        is_empty_key = re.match(r"^[^a-zA-Zа-яА-Я]*$", key)
                        is_too_short = len(key) < 2 or len(value) < 1
                        is_too_long = len(key) > 50 or len(value) > 100
                        
                        # Проверяем, не является ли это технической характеристикой
                        is_technical = any(word in key_lower for word in [
                            "характеристика", "параметр", "свойство", "описание",
                            "размер", "вес", "цвет", "материал", "мощность", "напряжение",
                            "частота", "скорость", "емкость", "объем", "диаметр", "толщина",
                            "длина", "ширина", "высота", "глубина", "экран", "дисплей",
                            "процессор", "память", "озу", "ssd", "hdd", "видеокарта"
                        ])
                        
                        if (key and value and 
                            not is_too_short and not is_too_long and
                            not is_financial and not is_administrative and
                            not is_numeric_key and not is_empty_key and
                            (is_technical or len(key_lower.split()) <= 5)):  # Не слишком длинные ключи
                            
                            # Нормализуем ключ
                            normalized_key = self._normalize_characteristic_key(key)
                            
                            # Пропускаем дубликаты
                            if not any(c["key"] == normalized_key for c in characteristics):
                                characteristics.append({
                                    "key": normalized_key,
                                    "value": value,
                                    "unit": self._extract_unit(value),
                                    "operator": "=",
                                    "source": "contract_page"
                                })
            
            if characteristics:
                contract_data["characteristics"] = characteristics
            
        except Exception as e:
            print(f"Ошибка при парсинге страницы контракта: {e}")
            import traceback
            traceback.print_exc()
        
        return contract_data
    
    def _normalize_characteristic_key(self, key: str) -> str:
        """Нормализует ключ характеристики"""
        key_lower = key.lower().strip()
        
        # Разбиваем ключ на слова
        words = re.findall(r'\b\w+\b', key_lower)
        
        # Маппинг синонимов (точные совпадения слов)
        synonyms = {
            'озу': 'ram',
            'оперативная': 'ram',
            'память': 'ram',
            'жесткий': 'storage',
            'диск': 'storage',
            'накопитель': 'storage',
            'процессор': 'cpu',
            'цп': 'cpu',
            'экран': 'screen_size',
            'дисплей': 'screen_size',
            'вес': 'weight',
            'цвет': 'color',
            'материал': 'material',
            'габариты': 'dimensions',
            'размер': 'size',
            'мощность': 'power',
            'напряжение': 'voltage',
            'частота': 'frequency',
            'скорость': 'speed',
            'емкость': 'capacity',
            'объем': 'volume',
            'длина': 'length',
            'ширина': 'width',
            'высота': 'height',
            'глубина': 'depth',
            'диаметр': 'diameter',
            'толщина': 'thickness',
        }
        
        # Проверяем каждое слово
        for word in words:
            if word in synonyms:
                return synonyms[word]
        
        # Если не нашли точного совпадения, проверяем частичные совпадения для многословных ключей
        multiword_synonyms = {
            'оперативная память': 'ram',
            'жесткий диск': 'storage',
        }
        
        for phrase, normalized in multiword_synonyms.items():
            if phrase in key_lower:
                return normalized
        
        return key_lower
    
    def _extract_unit(self, value: str) -> Optional[str]:
        """Извлекает единицу измерения из значения"""
        units = {
            'gb': ['gb', 'гб'],
            'mb': ['mb', 'мб'],
            'tb': ['tb', 'тб'],
            'ghz': ['ghz', 'ггц'],
            'mhz': ['mhz', 'мгц'],
            'inch': ['inch', 'дюйм', '"'],
            'mm': ['mm', 'мм'],
            'cm': ['cm', 'см'],
            'kg': ['kg', 'кг'],
            'g': ['g', 'г'],
            'w': ['w', 'вт'],
            'v': ['v', 'в'],
            'hz': ['hz', 'гц'],
        }
        
        value_lower = value.lower()
        for unit, patterns in units.items():
            for pattern in patterns:
                if pattern in value_lower:
                    return unit
        
        return None
    
    async def _get_contract_specification(self, contract_url: str) -> Optional[str]:
        """Получить спецификацию контракта"""
        
        try:
            # Пробуем получить страницу со спецификацией
            spec_url = contract_url.replace("common-info.html", "specification.html")
            response = await self.client.get(spec_url)
            
            if response.status_code == 200:
                return response.text
            
        except Exception:
            pass
        
        return None
    
    async def _get_printed_form_data(self, contract_url: str) -> Optional[Dict[str, Any]]:
        """Получить данные из печатной формы контракта"""
        
        try:
            # Пробуем скачать печатную форму
            print_url = contract_url.replace("common-info.html", "printForm.html")
            response = await self.client.get(print_url)
            
            if response.status_code == 200:
                # Парсим печатную форму
                soup = BeautifulSoup(response.text, "lxml")
                
                # Ищем таблицу спецификации
                tables = soup.find_all("table")
                for table in tables:
                    # Проверяем, похожа ли таблица на спецификацию
                    if self._is_specification_table(table):
                        return {
                            "html": str(table),
                            "text": table.get_text(),
                        }
        
        except Exception as e:
            print(f"Ошибка при получении печатной формы: {e}")
        
        return None
    
    def _is_specification_table(self, table) -> bool:
        """Проверить, является ли таблица таблицей спецификации"""
        
        text = table.get_text().lower()
        keywords = ["наименование", "количество", "цена", "сумма", "ед.", "изм."]
        
        keyword_count = sum(1 for keyword in keywords if keyword in text)
        return keyword_count >= 3
    
    def _extract_characteristics_from_specification(self, specification_html: str) -> List[Dict[str, Any]]:
        """Извлечь характеристики из спецификации"""
        
        characteristics = []
        soup = BeautifulSoup(specification_html, "lxml")
        
        # Ищем строки с характеристиками
        rows = soup.find_all("tr")
        
        for row in rows:
            cells = row.find_all("td")
            if len(cells) >= 2:
                key = cells[0].get_text().strip()
                value = cells[1].get_text().strip()
                
                if key and value and len(key) < 100:  # Фильтруем слишком длинные ключи
                    characteristics.append({
                        "key": key,
                        "value": value,
                        "source": "specification",
                    })
        
        return characteristics
    
    def _extract_characteristics_from_printed_form(self, printed_form_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Извлечь характеристики из печатной формы"""
        
        characteristics = []
        text = printed_form_data.get("text", "")
        
        # Упрощенный парсинг - ищем пары ключ: значение
        lines = text.split("\n")
        
        for line in lines:
            line = line.strip()
            if ":" in line:
                parts = line.split(":", 1)
                if len(parts) == 2:
                    key = parts[0].strip()
                    value = parts[1].strip()
                    
                    if key and value:
                        characteristics.append({
                            "key": key,
                            "value": value,
                            "source": "printed_form",
                        })
        
        return characteristics
    
    async def close(self):
        """Закрыть клиент"""
        await self.client.aclose()
```

### Файл: `app/adapters/eis/parser_with_retry.py`
```python
"""
Парсер ЕИС с обработкой ошибок и retry-логикой
"""
import asyncio
import re
import time
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import httpx
from bs4 import BeautifulSoup


class EISParserWithRetry:
    """Парсер ЕИС с обработкой ошибок и retry"""
    
    def __init__(self, max_concurrent: int = 3, max_retries: int = 3, use_cache: bool = True):
        self.base_url = "https://zakupki.gov.ru"
        self.max_retries = max_retries
        self.use_cache = use_cache
        self.client = httpx.AsyncClient(
            timeout=30.0,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            },
        )
        self.semaphore = asyncio.Semaphore(max_concurrent)
        
        if use_cache:
            try:
                from .cache import EISCache
                self.cache = EISCache()
            except ImportError:
                print("Предупреждение: Redis не доступен, кэширование отключено")
                self.cache = None
                self.use_cache = False
        else:
            self.cache = None
    
    async def _request_with_retry(self, url: str, params: Optional[Dict] = None, method: str = "GET") -> httpx.Response:
        """Выполнить запрос с retry-логикой"""
        
        for attempt in range(self.max_retries):
            try:
                if method == "GET":
                    response = await self.client.get(url, params=params)
                else:
                    response = await self.client.post(url, params=params)
                
                response.raise_for_status()
                return response
                
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 429:  # Too Many Requests
                    wait_time = (attempt + 1) * 2  # Exponential backoff
                    print(f"Получен 429, ждем {wait_time} секунд...")
                    await asyncio.sleep(wait_time)
                    continue
                elif e.response.status_code >= 500:
                    wait_time = (attempt + 1) * 1
                    print(f"Серверная ошибка {e.response.status_code}, ждем {wait_time} секунд...")
                    await asyncio.sleep(wait_time)
                    continue
                else:
                    raise
            except (httpx.RequestError, httpx.TimeoutException) as e:
                if attempt < self.max_retries - 1:
                    wait_time = (attempt + 1) * 1
                    print(f"Сетевая ошибка: {e}, ждем {wait_time} секунд...")
                    await asyncio.sleep(wait_time)
                    continue
                else:
                    raise
        
        raise httpx.RequestError("Превышено максимальное количество попыток")
    
    async def search_contracts(
        self,
        ktru_code: Optional[str] = None,
        product_name: Optional[str] = None,
        region: str = "Северо-Западный ФО",
        period_from: Optional[datetime] = None,
        period_to: Optional[datetime] = None,
        law_type: str = "44-ФЗ",
        max_results: int = 50,
    ) -> List[Dict[str, Any]]:
        """Поиск контрактов с обработкой ошибок"""
        
        # Строим параметры поиска
        params = self._build_search_params(
            ktru_code=ktru_code,
            product_name=product_name,
            region=region,
            period_from=period_from,
            period_to=period_to,
            law_type=law_type,
        )
        
        # Пробуем получить из кэша
        if self.use_cache and self.cache:
            cached_results = self.cache.get_cached_search_results(params)
            if cached_results:
                print(f"Используем кэшированные результаты поиска ({len(cached_results)} контрактов)")
                return cached_results[:max_results]
        
        contracts = []
        page = 1
        
        while len(contracts) < max_results:
            params["pageNumber"] = page
            
            try:
                response = await self._request_with_retry(
                    f"{self.base_url}/epz/order/extendedsearch/results.html",
                    params=params
                )
                
                page_contracts = await self._parse_search_results(response.text)
                contracts.extend(page_contracts)
                
                # Проверяем, есть ли следующая страница
                if not self._has_next_page(response.text) or len(contracts) >= max_results:
                    break
                
                page += 1
                await asyncio.sleep(1)  # Задержка между запросами
                
            except Exception as e:
                print(f"Ошибка при поиске контрактов: {e}")
                break
        
        results = contracts[:max_results]
        
        # Нормализуем результаты
        try:
            from .normalizer import DataNormalizer
            results = DataNormalizer.normalize_search_results(results)
        except ImportError:
            print("Предупреждение: Нормализатор не доступен")
        
        # Кэшируем результаты
        if self.use_cache and self.cache and results:
            self.cache.cache_search_results(params, results)
        
        return results
    
    def _build_search_params(
        self,
        ktru_code: Optional[str] = None,
        product_name: Optional[str] = None,
        region: str = "Северо-Западный ФО",
        period_from: Optional[datetime] = None,
        period_to: Optional[datetime] = None,
        law_type: str = "44-ФЗ",
    ) -> Dict[str, Any]:
        """Построить параметры поиска"""
        
        params = {
            "searchString": product_name or "",
            "pageNumber": 1,
            "recordsPerPage": "_50",
            "sortBy": "UPDATE_DATE",
            "sortDirection": "false",
        }
        
        # Фильтр по закону
        if law_type == "44-ФЗ":
            params["fz44"] = "on"
            params["fz223"] = "off"
        elif law_type == "223-ФЗ":
            params["fz44"] = "off"
            params["fz223"] = "on"
        
        # Фильтр по статусу
        params["contractStage"] = "EXECUTION_COMPLETED"
        
        # Фильтр по периоду
        if period_from:
            params["contractDateFrom"] = period_from.strftime("%d.%m.%Y")
        if period_to:
            params["contractDateTo"] = period_to.strftime("%d.%m.%Y")
        
        # Фильтр по КТРУ
        if ktru_code:
            params["ktruCodes"] = ktru_code
        
        # Фильтр по региону
        region_code = self._get_region_code(region)
        if region_code:
            params["regions"] = region_code
        
        return params
    
    def _get_region_code(self, region_name: str) -> str:
        """Получить код региона ЕИС"""
        from .regions import get_region_code
        return get_region_code(region_name)
    
    async def _parse_search_results(self, html: str) -> List[Dict[str, Any]]:
        """Парсинг результатов поиска"""
        
        soup = BeautifulSoup(html, "lxml")
        contracts = []
        
        # Ищем блоки с результатами
        result_blocks = soup.find_all("div", class_="search-registry-entry-block")
        
        for block in result_blocks:
            try:
                # Ищем div с классом registry-entry__header-mid__number
                number_div = block.find("div", class_="registry-entry__header-mid__number")
                if not number_div:
                    continue
                
                # Внутри div ищем ссылку
                link_tag = number_div.find("a")
                if not link_tag:
                    continue
                
                contract_url = link_tag.get("href")
                if not contract_url.startswith("http"):
                    contract_url = self.base_url + contract_url
                
                # Извлекаем номер контракта
                contract_number = link_tag.text.strip()
                contract_number = re.sub(r'[№\s]+', '', contract_number)
                
                # Извлекаем поставщика
                supplier_name = ""
                supplier_div = block.find("div", class_="registry-entry__body-href")
                if supplier_div:
                    supplier_link = supplier_div.find("a")
                    if supplier_link:
                        supplier_name = supplier_link.text.strip()
                
                # Извлекаем дату
                date_str = ""
                date_div = block.find("div", class_="data-block__value")
                if date_div:
                    date_str = date_div.text.strip()
                
                # Извлекаем цену
                price = 0.0
                price_div = block.find("div", class_="price-block__value")
                if price_div:
                    price_text = price_div.text.strip()
                    price_clean = re.sub(r'[^\d,.]', '', price_text)
                    price_clean = price_clean.replace(',', '.')
                    try:
                        price = float(price_clean)
                    except ValueError:
                        numbers = re.findall(r'[\d\s,]+', price_text)
                        if numbers:
                            try:
                                num = numbers[0].replace(' ', '').replace(',', '.')
                                price = float(num)
                            except:
                                pass
                
                # Извлекаем объект закупки
                purchase_object = ""
                object_div = block.find("div", class_="registry-entry__body-value")
                if object_div:
                    purchase_object = object_div.text.strip()[:200]
                
                contracts.append({
                    "url": contract_url,
                    "reg_number": contract_number,
                    "supplier_name": supplier_name,
                    "date": date_str,
                    "price": price,
                    "currency": "RUB",
                    "purchase_object": purchase_object,
                })
                
            except Exception as e:
                print(f"Ошибка при парсинге блока результата: {e}")
                continue
        
        return contracts
    
    def _has_next_page(self, html: str) -> bool:
        """Проверить наличие следующей страницы"""
        
        soup = BeautifulSoup(html, "lxml")
        next_button = soup.find("a", string=re.compile(r"Следующая|>"))
        return next_button is not None
    
    async def get_contract_details(self, contract_url: str) -> Dict[str, Any]:
        """Получить детали контракта с обработкой ошибок"""
        
        # Пробуем получить из кэша
        if self.use_cache and self.cache:
            cached_details = self.cache.get_cached_contract_details(contract_url)
            if cached_details:
                print(f"Используем кэшированные детали контракта: {contract_url}")
                return cached_details
        
        async with self.semaphore:
            try:
                response = await self._request_with_retry(contract_url)
                
                # Парсим основную информацию
                contract_data = await self._parse_contract_page(response.text)
                contract_data["url"] = contract_url
                
                # Пытаемся получить спецификацию
                try:
                    specification = await self._get_contract_specification(contract_url)
                    if specification:
                        contract_data["specification"] = specification
                        contract_data["characteristics"] = self._extract_characteristics_from_specification(specification)
                except Exception as e:
                    print(f"Ошибка при получении спецификации: {e}")
                
                # Если нет характеристик, пробуем печатную форму
                if not contract_data.get("characteristics"):
                    try:
                        printed_form_data = await self._get_printed_form_data(contract_url)
                        if printed_form_data:
                            contract_data["printed_form"] = printed_form_data
                            contract_data["characteristics"] = self._extract_characteristics_from_printed_form(printed_form_data)
                    except Exception as e:
                        print(f"Ошибка при получении печатной формы: {e}")
                
                # Гарантируем, что characteristics всегда есть
                if "characteristics" not in contract_data:
                    contract_data["characteristics"] = []
                
                # Нормализуем детали контракта
                try:
                    from .normalizer import DataNormalizer
                    contract_data = DataNormalizer.normalize_contract_data(contract_data)
                except ImportError:
                    print("Предупреждение: Нормализатор не доступен")
                
                # Кэшируем детали контракта
                if self.use_cache and self.cache:
                    self.cache.cache_contract_details(contract_url, contract_data)
                
                return contract_data
                
            except Exception as e:
                print(f"Ошибка при получении деталей контракта {contract_url}: {e}")
                return {"characteristics": []}
    
    async def _parse_contract_page(self, html: str) -> Dict[str, Any]:
        """Парсинг страницы контракта"""
        
        soup = BeautifulSoup(html, "lxml")
        contract_data = {}
        
        try:
            # Извлекаем номер контракта
            number_tag = soup.find("span", class_="cardMainInfo__purchaseLink")
            if number_tag:
                contract_data["reg_number"] = number_tag.text.strip()
            
            # Извлекаем поставщика
            supplier_tag = soup.find("span", string=re.compile(r"Поставщик|Исполнитель"))
            if supplier_tag:
                supplier_value = supplier_tag.find_next("span")
                if supplier_value:
                    contract_data["supplier_name"] = supplier_value.text.strip()
            
            # Извлекаем ИНН поставщика
            inn_tag = soup.find("span", string=re.compile(r"ИНН"))
            if inn_tag:
                inn_value = inn_tag.find_next("span")
                if inn_value:
                    contract_data["supplier_inn"] = inn_value.text.strip()
            
            # Извлекаем дату подписания
            date_tag = soup.find("span", string=re.compile(r"Дата заключения|Дата подписания"))
            if date_tag:
                date_value = date_tag.find_next("span")
                if date_value:
                    date_str = date_value.text.strip()
                    try:
                        contract_data["sign_date"] = datetime.strptime(date_str, "%d.%m.%Y")
                    except ValueError:
                        contract_data["sign_date"] = datetime.utcnow()
            
            # Извлекаем цену
            price_tag = soup.find("span", string=re.compile(r"Цена контракта|Сумма контракта"))
            if price_tag:
                price_value = price_tag.find_next("span")
                if price_value:
                    price_text = price_value.text.strip()
                    price_match = re.search(r"[\d\s,]+", price_text.replace(" ", ""))
                    if price_match:
                        try:
                            price = float(price_match.group().replace(",", "."))
                            contract_data["unit_price"] = price
                            contract_data["currency"] = "RUB"
                        except ValueError:
                            pass
            
            # Извлекаем вендора/производителя
            vendor_tag = soup.find("span", string=re.compile(r"Производитель|Вендор|Бренд", re.IGNORECASE))
            if vendor_tag:
                vendor_value = vendor_tag.find_next("span")
                if vendor_value:
                    contract_data["vendor"] = vendor_value.text.strip()
            
        except Exception as e:
            print(f"Ошибка при парсинге страницы контракта: {e}")
        
        return contract_data
    
    async def _get_contract_specification(self, contract_url: str) -> Optional[str]:
        """Получить спецификацию контракта"""
        
        try:
            spec_url = contract_url.replace("common-info.html", "specification.html")
            response = await self._request_with_retry(spec_url)
            
            if response.status_code == 200:
                return response.text
            
        except Exception:
            pass
        
        return None
    
    async def _get_printed_form_data(self, contract_url: str) -> Optional[Dict[str, Any]]:
        """Получить данные из печатной формы контракта"""
        
        try:
            # Пробуем скачать печатную форму в разных форматах
            formats = [
                ("printForm.html", "html"),
                ("printForm.pdf", "pdf"),
                ("printForm.docx", "docx"),
            ]
            
            for url_suffix, format_type in formats:
                try:
                    print_url = contract_url.replace("common-info.html", url_suffix)
                    response = await self._request_with_retry(print_url)
                    
                    if response.status_code == 200:
                        if format_type == "html":
                            soup = BeautifulSoup(response.text, "lxml")
                            tables = soup.find_all("table")
                            for table in tables:
                                if self._is_specification_table(table):
                                    return {
                                        "html": str(table),
                                        "text": table.get_text(),
                                        "format": "html",
                                    }
                        elif format_type == "pdf":
                            # Парсим PDF
                            from .document_parser import DocumentParser
                            result = DocumentParser.parse_pdf_content(response.content)
                            result["format"] = "pdf"
                            return result
                        elif format_type == "docx":
                            # Парсим DOCX
                            from .document_parser import DocumentParser
                            result = DocumentParser.parse_docx_content(response.content)
                            result["format"] = "docx"
                            return result
                            
                except Exception as e:
                    print(f"Ошибка при загрузке {format_type}: {e}")
                    continue
        
        except Exception as e:
            print(f"Ошибка при получении печатной формы: {e}")
        
        return None
    
    def _is_specification_table(self, table) -> bool:
        """Проверить, является ли таблица таблицей спецификации"""
        
        text = table.get_text().lower()
        keywords = ["наименование", "количество", "цена", "сумма", "ед.", "изм."]
        
        keyword_count = sum(1 for keyword in keywords if keyword in text)
        return keyword_count >= 3
    
    def _extract_characteristics_from_specification(self, specification_html: str) -> List[Dict[str, Any]]:
        """Извлечь характеристики из спецификации"""
        
        characteristics = []
        soup = BeautifulSoup(specification_html, "lxml")
        
        rows = soup.find_all("tr")
        
        for row in rows:
            cells = row.find_all("td")
            if len(cells) >= 2:
                key = cells[0].get_text().strip()
                value = cells[1].get_text().strip()
                
                if key and value and len(key) < 100:
                    characteristics.append({
                        "key": key,
                        "value": value,
                        "source": "specification",
                    })
        
        return characteristics
    
    def _extract_characteristics_from_printed_form(self, printed_form_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Извлечь характеристики из печатной формы"""
        
        characteristics = []
        text = printed_form_data.get("text", "")
        
        lines = text.split("\n")
        
        for line in lines:
            line = line.strip()
            if ":" in line:
                parts = line.split(":", 1)
                if len(parts) == 2:
                    key = parts[0].strip()
                    value = parts[1].strip()
                    
                    if key and value:
                        characteristics.append({
                            "key": key,
                            "value": value,
                            "source": "printed_form",
                        })
        
        return characteristics
    
    async def close(self):
        """Закрыть клиент"""
        await self.client.aclose()
```

### Файл: `app/adapters/eis/regions.py`
```python
"""
Полный маппинг регионов ЕИС
"""

REGION_MAPPING = {
    # Федеральные округа
    "Северо-Западный ФО": "78000000000",
    "Центральный ФО": "77000000000",
    "Южный ФО": "79000000000",
    "Приволжский ФО": "63000000000",
    "Уральский ФО": "66000000000",
    "Сибирский ФО": "54000000000",
    "Дальневосточный ФО": "28000000000",
    
    # Субъекты РФ (выборочно)
    "Москва": "77000000000",
    "Санкт-Петербург": "78000000000",
    "Московская область": "77000000000",
    "Ленинградская область": "78000000000",
    "Краснодарский край": "79000000000",
    "Свердловская область": "66000000000",
    "Новосибирская область": "54000000000",
    "Республика Татарстан": "63000000000",
    "Республика Башкортостан": "63000000000",
    "Нижегородская область": "63000000000",
    "Челябинская область": "66000000000",
    "Самарская область": "63000000000",
    "Омская область": "54000000000",
    "Ростовская область": "79000000000",
    "Республика Дагестан": "79000000000",
    "Красноярский край": "54000000000",
    "Пермский край": "66000000000",
    "Воронежская область": "77000000000",
    "Волгоградская область": "79000000000",
    "Саратовская область": "63000000000",
    "Иркутская область": "54000000000",
    "Ульяновская область": "63000000000",
    "Хабаровский край": "28000000000",
    "Ярославская область": "77000000000",
    "Республика Коми": "78000000000",
    "Тюменская область": "66000000000",
    "Томская область": "54000000000",
    "Кемеровская область": "54000000000",
    "Алтайский край": "54000000000",
    "Ставропольский край": "79000000000",
    "Белгородская область": "77000000000",
    "Курская область": "77000000000",
    "Тверская область": "77000000000",
    "Липецкая область": "77000000000",
    "Оренбургская область": "63000000000",
    "Пензенская область": "63000000000",
    "Кировская область": "63000000000",
    "Чеченская Республика": "79000000000",
    "Чувашская Республика": "63000000000",
    "Калининградская область": "78000000000",
    "Владимирская область": "77000000000",
    "Брянская область": "77000000000",
    "Калужская область": "77000000000",
    "Костромская область": "77000000000",
    "Орловская область": "77000000000",
    "Рязанская область": "77000000000",
    "Смоленская область": "77000000000",
    "Тамбовская область": "77000000000",
    "Тульская область": "77000000000",
    "Новгородская область": "78000000000",
    "Псковская область": "78000000000",
    "Республика Карелия": "78000000000",
    "Республика Крым": "79000000000",
    "Севастополь": "79000000000",
    "Республика Адыгея": "79000000000",
    "Республика Калмыкия": "79000000000",
    "Республика Ингушетия": "79000000000",
    "Кабардино-Балкарская Республика": "79000000000",
    "Карачаево-Черкесская Республика": "79000000000",
    "Республика Северная Осетия-Алания": "79000000000",
    "Республика Мордовия": "63000000000",
    "Республика Марий Эл": "63000000000",
    "Удмуртская Республика": "63000000000",
    "Курганская область": "66000000000",
    "Республика Алтай": "54000000000",
    "Республика Тыва": "54000000000",
    "Республика Хакасия": "54000000000",
    "Республика Бурятия": "54000000000",
    "Забайкальский край": "54000000000",
    "Амурская область": "28000000000",
    "Архангельская область": "78000000000",
    "Астраханская область": "79000000000",
    "Вологодская область": "78000000000",
    "Ивановская область": "77000000000",
    "Магаданская область": "28000000000",
    "Мурманская область": "78000000000",
    "Сахалинская область": "28000000000",
    "Еврейская автономная область": "28000000000",
    "Ненецкий автономный округ": "78000000000",
    "Ханты-Мансийский автономный округ": "66000000000",
    "Чукотский автономный округ": "28000000000",
    "Ямало-Ненецкий автономный округ": "66000000000",
}

def get_region_code(region_name: str) -> str:
    """
    Получить код региона ЕИС по названию
    
    Args:
        region_name: Название региона или федерального округа
        
    Returns:
        Код региона ЕИС или код Северо-Западного ФО по умолчанию
    """
    # Пробуем найти точное совпадение
    if region_name in REGION_MAPPING:
        return REGION_MAPPING[region_name]
    
    # Пробуем найти частичное совпадение (регион содержит название)
    for key, value in REGION_MAPPING.items():
        if region_name.lower() in key.lower() or key.lower() in region_name.lower():
            return value
    
    # По умолчанию возвращаем Северо-Западный ФО
    return "78000000000"

def get_all_regions() -> list:
    """Получить список всех регионов"""
    return list(REGION_MAPPING.keys())

def get_federal_districts() -> list:
    """Получить список федеральных округов"""
    federal_districts = [
        "Северо-Западный ФО",
        "Центральный ФО", 
        "Южный ФО",
        "Приволжский ФО",
        "Уральский ФО",
        "Сибирский ФО",
        "Дальневосточный ФО",
    ]
    return federal_districts
```

### Файл: `app/adapters/eis/sync_adapter.py`
```python
"""
Адаптер для использования асинхронного парсера ЕИС в синхронном коде
"""
import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime
from .parser_with_retry import EISParserWithRetry


class SyncEISParser:
    """Синхронная обертка над асинхронным парсером ЕИС"""
    
    def __init__(self, region: str = "Северо-Западный ФО", law_type: str = "44-ФЗ"):
        self.region = region
        self.law_type = law_type
        self._parser = EISParserWithRetry(max_concurrent=3, max_retries=3)
        self._loop = None
    
    def _get_event_loop(self):
        """Получить или создать event loop"""
        try:
            return asyncio.get_event_loop()
        except RuntimeError:
            # Если нет текущего loop (в потоке), создаем новый
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return loop
    
    def search_contracts(self, ktru_code: str, product_name: str, 
                        period_from: datetime, period_to: datetime) -> List[Dict[str, Any]]:
        """
        Синхронный поиск контрактов
        
        Args:
            ktru_code: Код КТРУ
            product_name: Наименование товара
            period_from: Начало периода
            period_to: Конец периода
            
        Returns:
            Список контрактов
        """
        loop = self._get_event_loop()
        
        # Запускаем асинхронную функцию в синхронном контексте
        return loop.run_until_complete(
            self._parser.search_contracts(
                ktru_code=ktru_code,
                product_name=product_name,
                region=self.region,
                period_from=period_from,
                period_to=period_to,
                law_type=self.law_type,
                max_results=50  # Ограничиваем для MVP
            )
        )
    
    def extract_characteristics(self, contract_url: str) -> Dict[str, Any]:
        """
        Синхронное извлечение характеристик из контракта
        
        Args:
            contract_url: URL контракта
            
        Returns:
            Характеристики контракта
        """
        loop = self._get_event_loop()
        
        # Получаем детали контракта
        contract_details = loop.run_until_complete(
            self._parser.get_contract_details(contract_url)
        )
        
        # Извлекаем характеристики из деталей
        characteristics = contract_details.get("characteristics", [])
        
        # Преобразуем в формат, ожидаемый системой
        result = {}
        for char in characteristics:
            key = char.get("key", "").lower()
            value = char.get("value", "")
            if key and value:
                result[key] = value
        
        return result
    
    def get_contract_vendor(self, contract_url: str) -> str:
        """
        Получить вендора/производителя из контракта
        
        Args:
            contract_url: URL контракта
            
        Returns:
            Наименование вендора
        """
        loop = self._get_event_loop()
        
        contract_details = loop.run_until_complete(
            self._parser.get_contract_details(contract_url)
        )
        
        return contract_details.get("vendor", "")
    
    def close(self):
        """Закрыть соединения"""
        loop = self._get_event_loop()
        loop.run_until_complete(self._parser.close())
```

### Файл: `app/adapters/eis_parser.py`
```python
"""
Адаптер для парсинга ЕИС (заглушка для тестирования)
"""
import time
import random
from typing import List, Dict, Any
from datetime import datetime

class EISParser:
    """Парсер ЕИС (заглушка для тестирования)"""
    
    def __init__(self, region: str = "Северо-Западный ФО", law_type: str = "44-ФЗ"):
        self.region = region
        self.law_type = law_type
    
    def search_contracts(self, ktru_code: str, product_name: str, period_from: datetime, period_to: datetime) -> List[Dict[str, Any]]:
        """
        Поиск контрактов в ЕИС (заглушка).
        
        Args:
            ktru_code: Код КТРУ
            product_name: Наименование товара
            period_from: Начало периода
            period_to: Конец периода
            
        Returns:
            Список контрактов
        """
        # Имитация задержки поиска
        time.sleep(2)
        
        # Генерируем тестовые данные
        contracts = []
        for i in range(random.randint(5, 15)):
            contract = {
                "reg_number": f"1234567890{i}",
                "eis_url": f"https://zakupki.gov.ru/epz/order/notice/printForm/view.html?regNumber=1234567890{i}",
                "supplier_name": f"Поставщик {i+1} ООО",
                "supplier_inn": f"123456789{i:03d}",
                "sign_date": datetime.now().replace(year=random.randint(2023, 2025), month=random.randint(1, 12), day=random.randint(1, 28)),
                "unit_price": random.uniform(10000, 500000),
                "currency": "RUB",
                "characteristics": {
                    "ram": f"{random.choice([8, 16, 32])} GB",
                    "ssd": f"{random.choice([256, 512, 1024])} GB",
                    "processor": random.choice(["Intel Core i5", "Intel Core i7", "AMD Ryzen 5", "AMD Ryzen 7"]),
                    "screen_size": f"{random.choice([13.3, 14, 15.6])} дюймов"
                },
                "vendor": random.choice(["Dell", "HP", "Lenovo", "Asus", "Acer", "Apple"])
            }
            contracts.append(contract)
        
        return contracts
    
    def extract_characteristics(self, contract_url: str) -> Dict[str, Any]:
        """
        Извлечение характеристик из контракта (заглушка).
        
        Args:
            contract_url: URL контракта
            
        Returns:
            Характеристики контракта
        """
        # Имитация задержки
        time.sleep(0.5)
        
        # Возвращаем тестовые характеристики
        return {
            "ram": f"{random.choice([8, 16, 32])} GB",
            "ssd": f"{random.choice([256, 512, 1024])} GB",
            "processor": random.choice(["Intel Core i5", "Intel Core i7", "AMD Ryzen 5", "AMD Ryzen 7"]),
            "screen_size": f"{random.choice([13.3, 14, 15.6])} дюймов"
        }

```

### Файл: `app/adapters/file_parser.py`
```python
"""
Парсер файлов с требованиями к товару с поддержкой OCR для PDF
"""
import os
import re
import json
import tempfile
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime

import pandas as pd
from docx import Document
import pdfplumber
from openpyxl import load_workbook
from pdf2image import convert_from_path
import pytesseract
from PIL import Image

class FileParser:
    """Парсер файлов различных форматов с поддержкой OCR"""
    
    def __init__(self):
        self.characteristic_patterns = {
            'ram': r'(ОЗУ|RAM|оперативная память|память)\s*[:=]?\s*(\d+)\s*(GB|ГБ|МБ|MB)',
            'ssd': r'(SSD|жесткий диск|накопитель)\s*[:=]?\s*(\d+)\s*(GB|ГБ|ТБ|TB)',
            'cpu': r'(процессор|CPU|ЦП)\s*[:=]?\s*([\w\s\-]+)\s*(\d+\.?\d*)\s*(GHz|ГГц)',
            'screen': r'(экран|дисплей|screen)\s*[:=]?\s*(\d+\.?\d*)\s*(дюйм|inch|")',
            'weight': r'(вес|weight)\s*[:=]?\s*(\d+\.?\d*)\s*(кг|kg|г|g)',
        }
        
        self.unit_mapping = {
            'GB': 'GB', 'ГБ': 'GB', 'MB': 'MB', 'МБ': 'MB',
            'TB': 'TB', 'ТБ': 'TB', 'GHz': 'GHz', 'ГГц': 'GHz',
            'дюйм': 'inch', 'inch': 'inch', '"': 'inch',
            'кг': 'kg', 'kg': 'kg', 'г': 'g', 'g': 'g'
        }
        
        self.operator_mapping = {
            '=': '=',
            '>=': '>=',
            '<=': '<=',
            '>': '>',
            '<': '<',
            '≈': '≈',
            '~': '~'
        }
        
        # Паттерны для поиска КТРУ кода
        self.ktru_patterns = [
            r'КТРУ\s*[:=]?\s*(\d{2}\.\d{2}\.\d{2}\.\d{2}-\d{8})',
            r'(\d{2}\.\d{2}\.\d{2}\.\d{2}-\d{8})',
            r'код\s*КТРУ\s*[:=]?\s*(\d{2}\.\d{2}\.\d{2}\.\d{2}-\d{8})'
        ]
        
        # Паттерны для поиска наименования товара
        self.name_patterns = [
            r'наименование\s*[:=]?\s*(.+)',
            r'товар\s*[:=]?\s*(.+)',
            r'продукт\s*[:=]?\s*(.+)',
            r'изделие\s*[:=]?\s*(.+)'
        ]
        
        # Паттерны для поиска производителя
        self.vendor_patterns = [
            r'производитель\s*[:=]?\s*(.+)',
            r'вендор\s*[:=]?\s*(.+)',
            r'бренд\s*[:=]?\s*(.+)',
            r'изготовитель\s*[:=]?\s*(.+)'
        ]
    
    def parse_file(self, filepath: str, file_ext: str) -> Dict[str, Any]:
        """Парсит файл в зависимости от его расширения"""
        try:
            if file_ext == '.txt':
                return self._parse_txt(filepath)
            elif file_ext == '.xlsx':
                return self._parse_xlsx(filepath)
            elif file_ext == '.docx':
                return self._parse_docx(filepath)
            elif file_ext == '.pdf':
                return self._parse_pdf(filepath)
            else:
                raise ValueError(f"Неподдерживаемый формат файла: {file_ext}")
        except Exception as e:
            return {
                "ktru_code": None,
                "name": None,
                "vendor": None,
                "characteristics": [],
                "warnings": [f"Ошибка парсинга файла: {str(e)}"]
            }
    
    def _parse_txt(self, filepath: str) -> Dict[str, Any]:
        """Парсит текстовый файл"""
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return self._extract_from_text(content)
    
    def _parse_xlsx(self, filepath: str) -> Dict[str, Any]:
        """Парсит Excel файл"""
        result = {
            "ktru_code": None,
            "name": None,
            "vendor": None,
            "characteristics": [],
            "warnings": []
        }
        
        try:
            # Пробуем прочитать как таблицу с помощью pandas
            df = pd.read_excel(filepath, header=None)
            
            # Ищем КТРУ код
            for i in range(min(10, len(df))):
                for j in range(min(10, len(df.columns))):
                    cell_value = str(df.iat[i, j])
                    if re.match(r'^\d{2}\.\d{2}\.\d{2}\.\d{2}-\d{8}$', cell_value):
                        result["ktru_code"] = cell_value
                        break
                if result["ktru_code"]:
                    break
            
            # Ищем наименование товара
            for i in range(min(5, len(df))):
                for j in range(min(5, len(df.columns))):
                    cell_value = str(df.iat[i, j])
                    if len(cell_value) > 10 and not cell_value.startswith('http'):
                        result["name"] = cell_value
                        break
                if result["name"]:
                    break
            
            # Извлекаем характеристики из всех ячеек
            text_content = ""
            for i in range(len(df)):
                for j in range(len(df.columns)):
                    cell_value = str(df.iat[i, j])
                    if cell_value and cell_value != 'nan':
                        text_content += cell_value + " "
            
            # Парсим характеристики из текста
            text_result = self._extract_from_text(text_content)
            result["characteristics"] = text_result.get("characteristics", [])
            result["warnings"].extend(text_result.get("warnings", []))
            
        except Exception as e:
            result["warnings"].append(f"Ошибка парсинга XLSX: {str(e)}")
        
        return result
    
    def _parse_docx(self, filepath: str) -> Dict[str, Any]:
        """Парсит Word документ"""
        doc = Document(filepath)
        
        # Извлекаем весь текст
        text_content = ""
        for paragraph in doc.paragraphs:
            text_content += paragraph.text + "\n"
        
        # Извлекаем текст из таблиц
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    text_content += cell.text + " "
        
        return self._extract_from_text(text_content)
    
    def _parse_pdf(self, filepath: str) -> Dict[str, Any]:
        """Парсит PDF файл с поддержкой OCR для сканированных документов"""
        text_content = ""
        warnings = []
        
        # Пытаемся извлечь текст стандартным способом
        try:
            with pdfplumber.open(filepath) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        text_content += text + "\n"
                    else:
                        warnings.append(f"Страница {page.page_number}: не удалось извлечь текст (возможно, это сканированный документ)")
        except Exception as e:
            warnings.append(f"Ошибка открытия PDF: {str(e)}")
        
        # Если текст не извлекся или слишком короткий, пробуем OCR
        if len(text_content.strip()) < 100:
            ocr_text = self._extract_text_with_ocr(filepath)
            if ocr_text:
                text_content += "\n" + ocr_text
                warnings.append("Текст извлечен с помощью OCR (сканированный документ)")
            else:
                warnings.append("Не удалось извлечь текст даже с помощью OCR")
        
        result = self._extract_from_text(text_content)
        result["warnings"].extend(warnings)
        
        return result
    
    def _extract_text_with_ocr(self, filepath: str) -> str:
        """Извлекает текст из PDF с помощью OCR"""
        try:
            # Конвертируем PDF в изображения
            images = convert_from_path(filepath, dpi=300)
            
            extracted_text = ""
            
            # Обрабатываем каждую страницу
            for i, image in enumerate(images):
                try:
                    # Используем pytesseract для распознавания текста
                    text = pytesseract.image_to_string(image, lang='rus+eng')
                    extracted_text += text + "\n"
                except Exception as e:
                    print(f"Ошибка OCR для страницы {i+1}: {e}")
                    continue
            
            return extracted_text
            
        except Exception as e:
            print(f"Ошибка при конвертации PDF в изображения: {e}")
            return ""
    
    def _extract_from_text(self, text: str) -> Dict[str, Any]:
        """Извлекает информацию из текста"""
        result = {
            "ktru_code": None,
            "name": None,
            "vendor": None,
            "characteristics": [],
            "warnings": []
        }
        
        # Ищем КТРУ код с использованием всех паттернов
        for pattern in self.ktru_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                result["ktru_code"] = match.group(1)
                break
        
        # Ищем наименование товара
        for pattern in self.name_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                name = match.group(1).strip()
                # Ограничиваем длину названия
                if len(name) > 5 and len(name) < 200:
                    result["name"] = name
                    break
        
        # Если не нашли по паттерну, ищем первую значимую строку
        if not result["name"]:
            lines = text.split('\n')
            for line in lines:
                line = line.strip()
                if (len(line) > 10 and len(line) < 200 and 
                    not line.startswith('http') and 
                    not re.match(r'^\d', line) and
                    not re.match(r'^[^a-zA-Zа-яА-Я]*$', line)):
                    result["name"] = line
                    break
        
        # Ищем производителя
        for pattern in self.vendor_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                vendor = match.group(1).strip()
                if len(vendor) > 2 and len(vendor) < 50:
                    result["vendor"] = vendor
                    break
        
        # Если не нашли по паттерну, ищем известных производителей
        if not result["vendor"]:
            vendors = ['Dell', 'HP', 'Lenovo', 'Apple', 'Asus', 'Acer', 'Microsoft', 'Samsung', 'Xiaomi', 'Huawei']
            for vendor in vendors:
                if vendor.lower() in text.lower():
                    result["vendor"] = vendor
                    break
        
        # Извлекаем характеристики по паттернам
        for key, pattern in self.characteristic_patterns.items():
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                characteristic = {
                    "key": self._normalize_key(key),
                    "value": match.group(2),
                    "unit": self._normalize_unit(match.group(3)) if match.group(3) else None,
                    "operator": "=",
                    "source": "file"
                }
                result["characteristics"].append(characteristic)
        
        # Ищем характеристики в формате "ключ: значение"
        key_value_pattern = r'([\w\s]+)\s*[:=]\s*([\w\d\.\s\-]+)(?:\s*([\w\/]+))?'
        matches = re.finditer(key_value_pattern, text)
        
        for match in matches:
            key = match.group(1).strip().lower()
            value = match.group(2).strip()
            unit = match.group(3).strip() if match.group(3) else None
            
            # Пропускаем очевидные не-характеристики
            if key in ['дата', 'date', 'номер', 'number', 'страница', 'page']:
                continue
            
            # Нормализуем ключ
            normalized_key = self._normalize_key(key)
            
            characteristic = {
                "key": normalized_key,
                "value": value,
                "unit": self._normalize_unit(unit) if unit else None,
                "operator": "=",
                "source": "file"
            }
            
            # Проверяем, нет ли уже такой характеристики
            if not any(c["key"] == normalized_key for c in result["characteristics"]):
                result["characteristics"].append(characteristic)
        
        # Если не нашли характеристик, добавляем предупреждение
        if not result["characteristics"]:
            result["warnings"].append("Не удалось извлечь характеристики из файла")
        
        return result
    
    def _normalize_key(self, key: str) -> str:
        """Нормализует ключ характеристики"""
        key = key.lower().strip()
        
        # Маппинг синонимов
        synonyms = {
            'озу': 'ram',
            'оперативная память': 'ram',
            'память': 'ram',
            'жесткий диск': 'storage',
            'накопитель': 'storage',
            'процессор': 'cpu',
            'цп': 'cpu',
            'экран': 'screen_size',
            'дисплей': 'screen_size',
            'вес': 'weight',
            'цвет': 'color',
            'материал': 'material',
            'габариты': 'dimensions',
            'размер': 'size',
            'мощность': 'power',
            'напряжение': 'voltage',
            'частота': 'frequency',
            'скорость': 'speed',
            'емкость': 'capacity',
            'объем': 'volume',
            'длина': 'length',
            'ширина': 'width',
            'высота': 'height',
            'глубина': 'depth',
            'диаметр': 'diameter',
            'толщина': 'thickness',
        }
        
        return synonyms.get(key, key)
    
    def _normalize_unit(self, unit: str) -> str:
        """Нормализует единицу измерения"""
        if not unit:
            return None
        
        unit = unit.strip()
        return self.unit_mapping.get(unit, unit)
    
    def _normalize_operator(self, operator: str) -> str:
        """Нормализует оператор сравнения"""
        if not operator:
            return "="
        
        operator = operator.strip()
        return self.operator_mapping.get(operator, "=")

```

### Файл: `app/adapters/match_engine.py`
```python
"""
Движок сопоставления характеристик
"""
import re
from typing import Dict, List, Tuple, Optional
from enum import Enum

class MatchType(str, Enum):
    IDENTICAL = "identical"
    HOMOGENEOUS = "homogeneous"
    DIFFERENT = "different"

class VendorStatus(str, Enum):
    MATCH = "match"
    MISMATCH = "mismatch"
    UNKNOWN = "unknown"

class MatchEngine:
    """Движок для сопоставления характеристик"""
    
    # Словарь синонимов для нормализации ключей
    KEY_SYNONYMS = {
        "ram": ["ram", "озу", "оперативная память", "memory"],
        "ssd": ["ssd", "жесткий диск", "hdd", "storage", "накопитель"],
        "processor": ["processor", "процессор", "cpu"],
        "screen_size": ["screen_size", "размер экрана", "диагональ"],
        "vendor": ["vendor", "производитель", "manufacturer", "бренд"]
    }
    
    # Словарь единиц измерения
    UNIT_CONVERSIONS = {
        "gb": ["gb", "гб", "гигабайт"],
        "mb": ["mb", "мб", "мегабайт"],
        "ghz": ["ghz", "ггц", "гигагерц"],
        "mhz": ["mhz", "мгц", "мегагерц"],
        "inch": ["inch", "дюйм", "дюймов"],
        "mm": ["mm", "мм", "миллиметр"]
    }
    
    def __init__(self):
        self._build_reverse_maps()
    
    def _build_reverse_maps(self):
        """Построить обратные карты для быстрого поиска"""
        self._key_to_canonical = {}
        for canonical, synonyms in self.KEY_SYNONYMS.items():
            for synonym in synonyms:
                self._key_to_canonical[synonym.lower()] = canonical
        
        self._unit_to_canonical = {}
        for canonical, synonyms in self.UNIT_CONVERSIONS.items():
            for synonym in synonyms:
                self._unit_to_canonical[synonym.lower()] = canonical
    
    def normalize_key(self, key: str) -> str:
        """Нормализовать ключ характеристики"""
        key_lower = key.lower().strip()
        return self._key_to_canonical.get(key_lower, key_lower)
    
    def normalize_unit(self, unit: str) -> str:
        """Нормализовать единицу измерения"""
        if not unit:
            return ""
        unit_lower = unit.lower().strip()
        return self._unit_to_canonical.get(unit_lower, unit_lower)
    
    def normalize_value(self, value: str) -> Tuple[float, str, str]:
        """
        Нормализовать значение характеристики.
        
        Returns:
            (числовое значение, единица измерения, оператор)
        """
        if not value:
            return 0.0, "", "="
        
        # Извлекаем оператор
        operator = "="
        value_str = str(value).strip()
        
        if value_str.startswith(">="):
            operator = ">="
            value_str = value_str[2:].strip()
        elif value_str.startswith("<="):
            operator = "<="
            value_str = value_str[2:].strip()
        elif value_str.startswith(">"):
            operator = ">"
            value_str = value_str[1:].strip()
        elif value_str.startswith("<"):
            operator = "<"
            value_str = value_str[1:].strip()
        elif value_str.startswith("="):
            value_str = value_str[1:].strip()
        
        # Извлекаем числовое значение и единицу измерения
        match = re.match(r"([\d\.]+)\s*([a-zA-Zа-яА-Я]+)?", value_str)
        if match:
            num_value = float(match.group(1))
            unit = match.group(2) or ""
            unit_norm = self.normalize_unit(unit)
            return num_value, unit_norm, operator
        
        # Если не удалось извлечь число, возвращаем как строку
        return 0.0, "", operator
    
    def compare_values(self, expected: str, found: str, key: str) -> Tuple[bool, int, str]:
        """
        Сравнить значения характеристик.
        
        Args:
            expected: Ожидаемое значение
            found: Найденное значение
            key: Ключ характеристики
            
        Returns:
            (совпадает ли, процент совпадения, причина различия)
        """
        if not expected and not found:
            return True, 100, ""
        
        if not expected or not found:
            return False, 0, "Отсутствует значение"
        
        # Нормализуем значения
        exp_num, exp_unit, exp_op = self.normalize_value(expected)
        found_num, found_unit, _ = self.normalize_value(found)
        
        # Проверяем единицы измерения
        if exp_unit and found_unit and exp_unit != found_unit:
            return False, 0, f"Разные единицы измерения: {exp_unit} vs {found_unit}"
        
        # Сравниваем значения в зависимости от оператора
        if exp_op == "=":
            if abs(exp_num - found_num) < 0.01:  # Погрешность для float
                return True, 100, ""
            else:
                diff_percent = min(100, max(0, 100 - abs(exp_num - found_num) / exp_num * 100))
                return False, int(diff_percent), f"Значения отличаются: {expected} vs {found}"
        
        elif exp_op == ">=":
            if found_num >= exp_num:
                return True, 100, ""
            else:
                diff_percent = min(100, max(0, found_num / exp_num * 100))
                return False, int(diff_percent), f"Найдено меньше требуемого: {found} < {expected}"
        
        elif exp_op == "<=":
            if found_num <= exp_num:
                return True, 100, ""
            else:
                diff_percent = min(100, max(0, exp_num / found_num * 100))
                return False, int(diff_percent), f"Найдено больше требуемого: {found} > {expected}"
        
        elif exp_op == ">":
            if found_num > exp_num:
                return True, 100, ""
            else:
                diff_percent = min(100, max(0, found_num / exp_num * 100))
                return False, int(diff_percent), f"Найдено меньше или равно требуемого: {found} <= {expected}"
        
        elif exp_op == "<":
            if found_num < exp_num:
                return True, 100, ""
            else:
                diff_percent = min(100, max(0, exp_num / found_num * 100))
                return False, int(diff_percent), f"Найдено больше или равно требуемого: {found} >= {expected}"
        
        # Для строковых значений
        if expected.lower() == found.lower():
            return True, 100, ""
        else:
            # Простая проверка на частичное совпадение
            if expected.lower() in found.lower() or found.lower() in expected.lower():
                return False, 50, f"Частичное совпадение: {expected} vs {found}"
            return False, 0, f"Значения отличаются: {expected} vs {found}"
    
    def compare_vendor(self, expected_vendor: str, found_vendor: str) -> VendorStatus:
        """Сравнить производителей"""
        if not expected_vendor or not found_vendor:
            return VendorStatus.UNKNOWN
        
        exp_norm = expected_vendor.lower().strip()
        found_norm = found_vendor.lower().strip()
        
        if exp_norm == found_norm:
            return VendorStatus.MATCH
        
        # Проверяем частичное совпадение (например, "Dell Inc." и "Dell")
        if exp_norm in found_norm or found_norm in exp_norm:
            return VendorStatus.MATCH
        
        return VendorStatus.MISMATCH
    
    def calculate_match(self, expected: Dict[str, str], found: Dict[str, str], expected_vendor: Optional[str] = None, found_vendor: Optional[str] = None) -> Tuple[int, MatchType, List[Dict]]:
        """
        Рассчитать совпадение характеристик.
        
        Args:
            expected: Ожидаемые характеристики {ключ: значение}
            found: Найденные характеристики {ключ: значение}
            expected_vendor: Ожидаемый производитель
            found_vendor: Найденный производитель
            
        Returns:
            (процент совпадения, тип совпадения, лог сверки)
        """
        if not expected:
            return 0, MatchType.DIFFERENT, []
        
        # Нормализуем ключи
        exp_norm = {self.normalize_key(k): v for k, v in expected.items()}
        found_norm = {self.normalize_key(k): v for k, v in found.items()}
        
        audit_log = []
        matched_count = 0
        total_count = len(exp_norm)
        
        # Сравниваем характеристики
        for key, exp_value in exp_norm.items():
            found_value = found_norm.get(key)
            
            if found_value:
                matches, percent, reason = self.compare_values(exp_value, found_value, key)
                is_diff = not matches
                
                audit_log.append({
                    "key": key,
                    "expected_value": exp_value,
                    "found_value": found_value,
                    "is_diff": is_diff,
                    "diff_reason": reason if is_diff else None,
                    "match_percent": percent
                })
                
                if matches:
                    matched_count += 1
                elif percent >= 80:  # Порог для однородных совпадений
                    matched_count += 0.5  # Половина очка за частичное совпадение
            else:
                audit_log.append({
                    "key": key,
                    "expected_value": exp_value,
                    "found_value": None,
                    "is_diff": True,
                    "diff_reason": "Характеристика не найдена",
                    "match_percent": 0
                })
        
        # Рассчитываем процент совпадения
        match_percent = int((matched_count / total_count) * 100) if total_count > 0 else 0
        
        # Определяем тип совпадения
        if match_percent == 100:
            match_type = MatchType.IDENTICAL
        elif match_percent >= 70:
            match_type = MatchType.HOMOGENEOUS
        else:
            match_type = MatchType.DIFFERENT
        
        # Добавляем проверку производителя в лог
        if expected_vendor or found_vendor:
            vendor_status = self.compare_vendor(expected_vendor, found_vendor)
            audit_log.append({
                "key": "vendor",
                "expected_value": expected_vendor,
                "found_value": found_vendor,
                "is_diff": vendor_status == VendorStatus.MISMATCH,
                "diff_reason": "Производитель отличается" if vendor_status == VendorStatus.MISMATCH else None,
                "match_percent": 100 if vendor_status == VendorStatus.MATCH else 0
            })
        
        return match_percent, match_type, audit_log
```

### Файл: `app/adapters/parsers/__init__.py`
```python

```

### Файл: `app/adapters/parsers/file_parser.py`
```python
import io
import re
from typing import Tuple, List, Dict, Any, Optional
import pandas as pd
from docx import Document
import pdfplumber
from openpyxl import load_workbook


class FileParser:
    """Парсер файлов с требованиями"""
    
    def __init__(self):
        # Словарь для нормализации ключей характеристик
        self.key_normalization = {
            "озу": "ram",
            "оперативная память": "ram",
            "ram": "ram",
            "ssd": "ssd_capacity",
            "жесткий диск": "hdd_capacity",
            "hdd": "hdd_capacity",
            "процессор": "cpu",
            "cpu": "cpu",
            "частота процессора": "cpu_frequency",
            "частота": "frequency",
            "диагональ": "screen_size",
            "экран": "screen_size",
            "разрешение": "resolution",
            "операционная система": "os",
            "os": "os",
            "вес": "weight",
            "габариты": "dimensions",
            "цвет": "color",
            "материал": "material",
            "производитель": "vendor",
            "вендор": "vendor",
            "бренд": "vendor",
        }
        
        # Словарь для нормализации единиц измерения
        self.unit_normalization = {
            "гб": "gb",
            "gb": "gb",
            "гигабайт": "gb",
            "мб": "mb",
            "mb": "mb",
            "мегабайт": "mb",
            "кг": "kg",
            "kg": "kg",
            "килограмм": "kg",
            "г": "g",
            "g": "g",
            "грамм": "g",
            "см": "cm",
            "cm": "cm",
            "сантиметр": "cm",
            "мм": "mm",
            "mm": "mm",
            "миллиметр": "mm",
            "дюйм": "inch",
            "inch": "inch",
            '"': "inch",
            "гц": "hz",
            "hz": "hz",
            "герц": "hz",
            "кгц": "khz",
            "khz": "khz",
            "килогерц": "khz",
            "мгц": "mhz",
            "mhz": "mhz",
            "мегагерц": "mhz",
            "ггц": "ghz",
            "ghz": "ghz",
            "гигагерц": "ghz",
        }
    
    async def parse_file(
        self,
        file_content: bytes,
        filename: str,
        mime_type: Optional[str] = None,
    ) -> Tuple[Dict[str, Any], List[str]]:
        """Разобрать файл и извлечь требования"""
        
        file_extension = filename.lower().split('.')[-1]
        warnings = []
        
        try:
            if file_extension == 'txt':
                return self._parse_txt(file_content, warnings)
            elif file_extension == 'xlsx':
                return self._parse_xlsx(file_content, warnings)
            elif file_extension == 'docx':
                return self._parse_docx(file_content, warnings)
            elif file_extension == 'pdf':
                return self._parse_pdf(file_content, warnings)
            else:
                warnings.append(f"Неподдерживаемый формат файла: {file_extension}")
                return {}, warnings
                
        except Exception as e:
            warnings.append(f"Ошибка при разборе файла: {str(e)}")
            return {}, warnings
    
    def _parse_txt(self, content: bytes, warnings: List[str]) -> Tuple[Dict[str, Any], List[str]]:
        """Разобрать TXT файл"""
        
        text = content.decode('utf-8', errors='ignore')
        lines = text.split('\n')
        
        detected = {
            "ktru_code": None,
            "name": None,
            "vendor": None,
            "characteristics": [],
        }
        
        # Поиск КТРУ кода
        ktru_pattern = r'\b\d{2}\.\d{2}\.\d{2}\.\d{3}-\d{8}\b'
        ktru_match = re.search(ktru_pattern, text)
        if ktru_match:
            detected["ktru_code"] = ktru_match.group()
        
        # Поиск характеристик в формате "ключ: значение"
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Проверяем, является ли строка названием товара
            if not detected["name"] and len(line) < 100 and not ':' in line:
                detected["name"] = line
                continue
            
            # Ищем характеристики
            if ':' in line:
                parts = line.split(':', 1)
                if len(parts) == 2:
                    key = parts[0].strip().lower()
                    value = parts[1].strip()
                    
                    # Нормализуем ключ
                    normalized_key = self._normalize_key(key)
                    if normalized_key == "vendor" and not detected["vendor"]:
                        detected["vendor"] = value
                        continue
                    
                    # Извлекаем значение, единицу измерения и оператор
                    norm_value, unit, operator = self._extract_value_unit_operator(value)
                    
                    if norm_value:
                        detected["characteristics"].append({
                            "key": normalized_key,
                            "value": norm_value,
                            "unit": unit,
                            "operator": operator,
                        })
        
        return detected, warnings
    
    def _parse_xlsx(self, content: bytes, warnings: List[str]) -> Tuple[Dict[str, Any], List[str]]:
        """Разобрать XLSX файл"""
        
        detected = {
            "ktru_code": None,
            "name": None,
            "vendor": None,
            "characteristics": [],
        }
        
        try:
            # Используем pandas для чтения Excel
            df = pd.read_excel(io.BytesIO(content), sheet_name=None, header=None)
            
            # Ищем данные в первом листе
            first_sheet = list(df.values())[0] if df else None
            
            if first_sheet is not None:
                # Преобразуем в список списков
                data = first_sheet.values.tolist()
                
                for row in data:
                    row_str = ' '.join([str(cell) for cell in row if pd.notna(cell)])
                    
                    # Поиск КТРУ кода
                    if not detected["ktru_code"]:
                        ktru_pattern = r'\b\d{2}\.\d{2}\.\d{2}\.\d{3}-\d{8}\b'
                        ktru_match = re.search(ktru_pattern, row_str)
                        if ktru_match:
                            detected["ktru_code"] = ktru_match.group()
                    
                    # Поиск названия товара
                    if not detected["name"] and len(row_str) < 100:
                        detected["name"] = row_str
                    
                    # Поиск характеристик
                    for cell in row:
                        if pd.notna(cell):
                            cell_str = str(cell)
                            if ':' in cell_str:
                                parts = cell_str.split(':', 1)
                                if len(parts) == 2:
                                    key = parts[0].strip().lower()
                                    value = parts[1].strip()
                                    
                                    normalized_key = self._normalize_key(key)
                                    if normalized_key == "vendor" and not detected["vendor"]:
                                        detected["vendor"] = value
                                        continue
                                    
                                    norm_value, unit, operator = self._extract_value_unit_operator(value)
                                    
                                    if norm_value:
                                        detected["characteristics"].append({
                                            "key": normalized_key,
                                            "value": norm_value,
                                            "unit": unit,
                                            "operator": operator,
                                        })
        
        except Exception as e:
            warnings.append(f"Ошибка при разборе XLSX: {str(e)}")
        
        return detected, warnings
    
    def _parse_docx(self, content: bytes, warnings: List[str]) -> Tuple[Dict[str, Any], List[str]]:
        """Разобрать DOCX файл"""
        
        detected = {
            "ktru_code": None,
            "name": None,
            "vendor": None,
            "characteristics": [],
        }
        
        try:
            doc = Document(io.BytesIO(content))
            full_text = []
            
            # Извлекаем текст из параграфов
            for para in doc.paragraphs:
                full_text.append(para.text)
            
            # Извлекаем текст из таблиц
            for table in doc.tables:
                for row in table.rows:
                    for cell in row.cells:
                        full_text.append(cell.text)
            
            text = '\n'.join(full_text)
            
            # Поиск КТРУ кода
            ktru_pattern = r'\b\d{2}\.\d{2}\.\d{2}\.\d{3}-\d{8}\b'
            ktru_match = re.search(ktru_pattern, text)
            if ktru_match:
                detected["ktru_code"] = ktru_match.group()
            
            # Поиск характеристик
            lines = text.split('\n')
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # Поиск названия товара
                if not detected["name"] and len(line) < 100 and not ':' in line:
                    detected["name"] = line
                    continue
                
                # Ищем характеристики
                if ':' in line:
                    parts = line.split(':', 1)
                    if len(parts) == 2:
                        key = parts[0].strip().lower()
                        value = parts[1].strip()
                        
                        normalized_key = self._normalize_key(key)
                        if normalized_key == "vendor" and not detected["vendor"]:
                            detected["vendor"] = value
                            continue
                        
                        norm_value, unit, operator = self._extract_value_unit_operator(value)
                        
                        if norm_value:
                            detected["characteristics"].append({
                                "key": normalized_key,
                                "value": norm_value,
                                "unit": unit,
                                "operator": operator,
                            })
        
        except Exception as e:
            warnings.append(f"Ошибка при разборе DOCX: {str(e)}")
        
        return detected, warnings
    
    def _parse_pdf(self, content: bytes, warnings: List[str]) -> Tuple[Dict[str, Any], List[str]]:
        """Разобрать PDF файл (только текстовые PDF)"""
        
        detected = {
            "ktru_code": None,
            "name": None,
            "vendor": None,
            "characteristics": [],
        }
        
        try:
            with pdfplumber.open(io.BytesIO(content)) as pdf:
                text = ""
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                
                if not text.strip():
                    warnings.append("PDF файл не содержит извлекаемого текста (возможно, это скан)")
                    return detected, warnings
                
                # Поиск КТРУ кода
                ktru_pattern = r'\b\d{2}\.\d{2}\.\d{2}\.\d{3}-\d{8}\b'
                ktru_match = re.search(ktru_pattern, text)
                if ktru_match:
                    detected["ktru_code"] = ktru_match.group()
                
                # Поиск характеристик
                lines = text.split('\n')
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                    
                    # Поиск названия товара
                    if not detected["name"] and len(line) < 100 and not ':' in line:
                        detected["name"] = line
                        continue
                    
                    # Ищем характеристики
                    if ':' in line:
                        parts = line.split(':', 1)
                        if len(parts) == 2:
                            key = parts[0].strip().lower()
                            value = parts[1].strip()
                            
                            normalized_key = self._normalize_key(key)
                            if normalized_key == "vendor" and not detected["vendor"]:
                                detected["vendor"] = value
                                continue
                            
                            norm_value, unit, operator = self._extract_value_unit_operator(value)
                            
                            if norm_value:
                                detected["characteristics"].append({
                                    "key": normalized_key,
                                    "value": norm_value,
                                    "unit": unit,
                                    "operator": operator,
                                })
        
        except Exception as e:
            warnings.append(f"Ошибка при разборе PDF: {str(e)}")
        
        return detected, warnings
    
    def _normalize_key(self, key: str) -> str:
        """Нормализовать ключ характеристики"""
        key_lower = key.lower()
        for pattern, normalized in self.key_normalization.items():
            if pattern in key_lower:
                return normalized
        return key_lower
    
    def _extract_value_unit_operator(self, value_str: str) -> Tuple[Optional[str], Optional[str], str]:
        """Извлечь значение, единицу измерения и оператор из строки"""
        
        # Определяем оператор
        operator = "="
        if ">=" in value_str:
            operator = ">="
            value_str = value_str.replace(">=", "").strip()
        elif "<=" in value_str:
            operator = "<="
            value_str = value_str.replace("<=", "").strip()
        elif ">" in value_str:
            operator = ">"
            value_str = value_str.replace(">", "").strip()
        elif "<" in value_str:
            operator = "<"
            value_str = value_str.replace("<", "").strip()
        elif "~" in value_str:
            operator = "~"
            value_str = value_str.replace("~", "").strip()
        
        # Ищем числовое значение
        number_match = re.search(r'[\d.,]+', value_str)
        if not number_match:
            return None, None, operator
        
        number_str = number_match.group().replace(',', '.')
        
        # Пытаемся преобразовать в число
        try:
            if '.' in number_str:
                number = float(number_str)
            else:
                number = int(number_str)
        except ValueError:
            return None, None, operator
        
        # Ищем единицу измерения
        unit = None
        for unit_pattern, normalized_unit in self.unit_normalization.items():
            if re.search(rf'\b{re.escape(unit_pattern)}\b', value_str.lower()):
                unit = normalized_unit
                break
        
        return str(number), unit, operator
```

### Файл: `app/adapters/parsers/match_engine.py`
```python
import re
from typing import Dict, List, Any, Tuple, Optional
from difflib import SequenceMatcher


class MatchEngine:
    """Движок для сопоставления характеристик"""
    
    def __init__(self):
        # Словарь для нормализации ключей
        self.key_normalization = {
            "озу": "ram",
            "оперативная память": "ram",
            "ram": "ram",
            "память": "ram",
            "объем памяти": "ram",
            "ssd": "ssd_capacity",
            "жесткий диск": "hdd_capacity",
            "hdd": "hdd_capacity",
            "накопитель": "storage",
            "процессор": "cpu",
            "cpu": "cpu",
            "частота процессора": "cpu_frequency",
            "частота": "frequency",
            "тактовая частота": "frequency",
            "диагональ": "screen_size",
            "экран": "screen_size",
            "размер экрана": "screen_size",
            "разрешение": "resolution",
            "операционная система": "os",
            "os": "os",
            "система": "os",
            "вес": "weight",
            "масса": "weight",
            "габариты": "dimensions",
            "размеры": "dimensions",
            "цвет": "color",
            "материал": "material",
            "производитель": "vendor",
            "вендор": "vendor",
            "бренд": "vendor",
            "изготовитель": "vendor",
            "модель": "model",
            "артикул": "article",
            "код": "code",
            "тип": "type",
            "мощность": "power",
            "напряжение": "voltage",
            "емкость": "capacity",
            "скорость": "speed",
            "длина": "length",
            "ширина": "width",
            "высота": "height",
            "глубина": "depth",
            "толщина": "thickness",
        }
        
        # Словарь для нормализации единиц измерения
        self.unit_normalization = {
            "гб": "gb",
            "gb": "gb",
            "гигабайт": "gb",
            "гигабайта": "gb",
            "гигабайтов": "gb",
            "мб": "mb",
            "mb": "mb",
            "мегабайт": "mb",
            "мегабайта": "mb",
            "мегабайтов": "mb",
            "кг": "kg",
            "kg": "kg",
            "килограмм": "kg",
            "килограмма": "kg",
            "килограммов": "kg",
            "г": "g",
            "g": "g",
            "грамм": "g",
            "грамма": "g",
            "граммов": "g",
            "см": "cm",
            "cm": "cm",
            "сантиметр": "cm",
            "сантиметра": "cm",
            "сантиметров": "cm",
            "мм": "mm",
            "mm": "mm",
            "миллиметр": "mm",
            "миллиметра": "mm",
            "миллиметров": "mm",
            "дюйм": "inch",
            "inch": "inch",
            '"': "inch",
            "дюйма": "inch",
            "дюймов": "inch",
            "гц": "hz",
            "hz": "hz",
            "герц": "hz",
            "герца": "hz",
            "герц": "hz",
            "кгц": "khz",
            "khz": "khz",
            "килогерц": "khz",
            "килогерца": "khz",
            "мгц": "mhz",
            "mhz": "mhz",
            "мегагерц": "mhz",
            "мегагерца": "mhz",
            "ггц": "ghz",
            "ghz": "ghz",
            "гигагерц": "ghz",
            "гигагерца": "ghz",
            "в": "v",
            "v": "v",
            "вольт": "v",
            "вольта": "v",
            "вт": "w",
            "w": "w",
            "ватт": "w",
            "ватта": "w",
            "квт": "kw",
            "kw": "kw",
            "киловатт": "kw",
            "киловатта": "kw",
            "л": "l",
            "l": "l",
            "литр": "l",
            "литра": "l",
            "литров": "l",
            "мл": "ml",
            "ml": "ml",
            "миллилитр": "ml",
            "миллилитра": "ml",
        }
        
        # Ключи, которые считаются обязательными
        self.mandatory_keys = {"ram", "cpu", "screen_size", "vendor"}
        
        # Ключи, которые считаются важными
        self.important_keys = {"ssd_capacity", "hdd_capacity", "os", "resolution"}
        
        # Допустимые отклонения для числовых значений (в процентах)
        self.numeric_tolerance = {
            "ram": 10,  # ±10% для ОЗУ
            "ssd_capacity": 20,  # ±20% для SSD
            "hdd_capacity": 20,  # ±20% для HDD
            "cpu_frequency": 5,  # ±5% для частоты процессора
            "screen_size": 5,  # ±5% для диагонали экрана
            "weight": 15,  # ±15% для веса
        }
    
    async def compare_characteristics(
        self,
        requirements: Dict[str, Any],
        contract_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Сравнить требования с характеристиками контракта"""
        
        # Извлекаем характеристики из требований
        req_chars = requirements.get("characteristics", [])
        req_vendor = requirements.get("vendor")
        
        # Извлекаем характеристики из контракта
        contract_chars = contract_data.get("characteristics", [])
        contract_vendor = contract_data.get("vendor")
        
        # Нормализуем характеристики
        normalized_req = self._normalize_characteristics(req_chars)
        normalized_contract = self._normalize_characteristics(contract_chars)
        
        # Сравниваем характеристики
        match_results = []
        total_score = 0
        max_score = 0
        
        for req_key, req_data in normalized_req.items():
            max_score += self._get_key_weight(req_key)
            
            if req_key in normalized_contract:
                contract_data = normalized_contract[req_key]
                match_result = self._compare_single_characteristic(req_data, contract_data)
                match_results.append(match_result)
                
                if match_result["match"]:
                    total_score += self._get_key_weight(req_key) * match_result["score"]
            else:
                # Характеристика не найдена в контракте
                match_results.append({
                    "key": req_key,
                    "expected": req_data,
                    "found": None,
                    "match": False,
                    "score": 0,
                    "reason": "Характеристика не найдена",
                })
        
        # Рассчитываем процент совпадения
        match_percent = int((total_score / max_score * 100)) if max_score > 0 else 0
        
        # Проверяем совпадение вендора
        vendor_match = self._compare_vendors(req_vendor, contract_vendor)
        
        # Формируем лог сверки
        audit_log = self._create_audit_log(match_results, vendor_match, req_vendor, contract_vendor)
        
        return {
            "match_percent": match_percent,
            "vendor_match": vendor_match,
            "audit_log": audit_log,
            "details": {
                "total_characteristics": len(normalized_req),
                "matched_characteristics": len([r for r in match_results if r["match"]]),
                "vendor_status": "match" if vendor_match else "mismatch",
            },
        }
    
    def _normalize_characteristics(self, characteristics: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        """Нормализовать список характеристик"""
        
        normalized = {}
        
        for char in characteristics:
            key = char.get("key", "").lower().strip()
            value = char.get("value", "").strip()
            unit = char.get("unit", "").lower().strip() if char.get("unit") else None
            operator = char.get("operator", "=")
            
            # Нормализуем ключ
            normalized_key = self._normalize_key(key)
            
            # Нормализуем значение
            normalized_value, normalized_unit = self._normalize_value(value, unit)
            
            if normalized_key:
                normalized[normalized_key] = {
                    "original_key": key,
                    "original_value": value,
                    "value": normalized_value,
                    "unit": normalized_unit,
                    "operator": operator,
                    "is_numeric": self._is_numeric(normalized_value),
                }
        
        return normalized
    
    def _normalize_key(self, key: str) -> str:
        """Нормализовать ключ характеристики"""
        
        # Удаляем лишние символы
        key = re.sub(r'[^\w\s]', ' ', key)
        key = ' '.join(key.split())  # Удаляем лишние пробелы
        
        # Ищем совпадение в словаре нормализации
        for pattern, normalized in self.key_normalization.items():
            if pattern in key.lower():
                return normalized
        
        # Если не нашли, возвращаем исходный ключ
        return key.lower()
    
    def _normalize_value(self, value: str, unit: Optional[str] = None) -> Tuple[Optional[str], Optional[str]]:
        """Нормализовать значение и единицу измерения"""
        
        # Если значение пустое
        if not value:
            return None, None
        
        # Пытаемся извлечь число
        number_match = re.search(r'[\d.,]+', value.replace(' ', ''))
        if not number_match:
            return value, unit
        
        number_str = number_match.group().replace(',', '.')
        
        # Пытаемся преобразовать в число
        try:
            if '.' in number_str:
                number = float(number_str)
            else:
                number = int(number_str)
        except ValueError:
            return value, unit
        
        # Если единица измерения не указана, пытаемся извлечь из значения
        if not unit:
            unit_match = re.search(r'[a-zA-Zа-яА-Я°"\'″]+', value.lower())
            if unit_match:
                extracted_unit = unit_match.group()
                # Нормализуем единицу измерения
                unit = self._normalize_unit(extracted_unit)
        
        # Нормализуем единицу измерения, если она указана
        if unit:
            unit = self._normalize_unit(unit)
        
        return str(number), unit
    
    def _normalize_unit(self, unit: str) -> str:
        """Нормализовать единицу измерения"""
        
        unit_lower = unit.lower().strip()
        
        for pattern, normalized in self.unit_normalization.items():
            if pattern == unit_lower or f" {pattern} " in f" {unit_lower} ":
                return normalized
        
        return unit_lower
    
    def _is_numeric(self, value: str) -> bool:
        """Проверить, является ли значение числовым"""
        
        try:
            float(value)
            return True
        except (ValueError, TypeError):
            return False
    
    def _compare_single_characteristic(
        self,
        req_data: Dict[str, Any],
        contract_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Сравнить одну характеристику"""
        
        req_value = req_data["value"]
        contract_value = contract_data["value"]
        operator = req_data.get("operator", "=")
        
        # Если значения текстовые
        if not req_data["is_numeric"]:
            similarity = SequenceMatcher(None, req_value.lower(), contract_value.lower()).ratio()
            match = similarity > 0.8  # Порог схожести 80%
            
            return {
                "key": req_data["original_key"],
                "expected": req_value,
                "found": contract_value,
                "match": match,
                "score": similarity,
                "reason": None if match else "Текстовые значения не совпадают",
            }
        
        # Если значения числовые
        try:
            req_num = float(req_value)
            contract_num = float(contract_value)
            
            # Проверяем по оператору
            if operator == "=":
                tolerance = self.numeric_tolerance.get(req_data["original_key"], 0)
                diff_percent = abs(req_num - contract_num) / req_num * 100 if req_num > 0 else 100
                match = diff_percent <= tolerance
                score = 1 - (diff_percent / 100) if diff_percent <= 100 else 0
                
            elif operator == ">=":
                match = contract_num >= req_num
                score = 1.0 if match else 0.0
                
            elif operator == "<=":
                match = contract_num <= req_num
                score = 1.0 if match else 0.0
                
            elif operator == ">":
                match = contract_num > req_num
                score = 1.0 if match else 0.0
                
            elif operator == "<":
                match = contract_num < req_num
                score = 1.0 if match else 0.0
                
            else:
                match = False
                score = 0.0
            
            return {
                "key": req_data["original_key"],
                "expected": f"{req_value} {req_data.get('unit', '')}",
                "found": f"{contract_value} {contract_data.get('unit', '')}",
                "match": match,
                "score": score,
                "reason": None if match else f"Числовое значение не соответствует оператору {operator}",
            }
            
        except (ValueError, TypeError):
            return {
                "key": req_data["original_key"],
                "expected": req_value,
                "found": contract_value,
                "match": False,
                "score": 0,
                "reason": "Ошибка при сравнении числовых значений",
            }
    
    def _compare_vendors(self, req_vendor: Optional[str], contract_vendor: Optional[str]) -> bool:
        """Сравнить вендоров"""
        
        if not req_vendor or not contract_vendor:
            return True  # Если вендор не указан в требованиях, считаем совпадением
        
        req_vendor_lower = req_vendor.lower()
        contract_vendor_lower = contract_vendor.lower()
        
        # Простое сравнение строк
        if req_vendor_lower == contract_vendor_lower:
            return True
        
        # Проверяем частичное совпадение
        if req_vendor_lower in contract_vendor_lower or contract_vendor_lower in req_vendor_lower:
            return True
        
        # Проверяем схожесть
        similarity = SequenceMatcher(None, req_vendor_lower, contract_vendor_lower).ratio()
        return similarity > 0.7  # Порог схожести 70%
    
    def _get_key_weight(self, key: str) -> float:
        """Получить вес характеристики"""
        
        if key in self.mandatory_keys:
            return 2.0
        elif key in self.important_keys:
            return 1.5
        else:
            return 1.0
    
    def _create_audit_log(
        self,
        match_results: List[Dict[str, Any]],
        vendor_match: bool,
        req_vendor: Optional[str],
        contract_vendor: Optional[str],
    ) -> List[Dict[str, Any]]:
        """Создать лог сверки"""
        
        audit_log = []
        
        # Добавляем результаты сравнения характеристик
        for result in match_results:
            audit_log.append({
                "key": result["key"],
                "expected_value": result["expected"],
                "found_value": result["found"],
                "is_diff": not result["match"],
                "diff_reason": result.get("reason"),
            })
        
        # Добавляем сравнение вендоров
        audit_log.append({
            "key": "Производитель",
            "expected_value": req_vendor,
            "found_value": contract_vendor,
            "is_diff": not vendor_match,
            "diff_reason": None if vendor_match else "Производитель не совпадает",
        })
        
        return audit_log
```

### Файл: `app/adapters/storage/__init__.py`
```python

```

### Файл: `app/adapters/storage/minio_client.py`
```python
import io
from typing import Optional
from minio import Minio
from minio.error import S3Error
from app.infra.config import settings


class MinioClient:
    """Клиент для работы с MinIO/S3"""
    
    def __init__(self):
        self.client = Minio(
            endpoint=settings.minio_endpoint,
            access_key=settings.minio_access_key,
            secret_key=settings.minio_secret_key,
            secure=settings.minio_secure,
        )
        self._ensure_bucket_exists()
    
    def _ensure_bucket_exists(self):
        """Убедиться, что бакет существует"""
        try:
            if not self.client.bucket_exists(settings.minio_bucket):
                self.client.make_bucket(settings.minio_bucket)
        except S3Error as e:
            raise Exception(f"Ошибка при создании бакета: {e}")
    
    async def upload_file(
        self,
        bucket_name: str,
        filename: str,
        content: bytes,
        content_type: Optional[str] = None,
    ) -> str:
        """Загрузить файл в MinIO"""
        
        try:
            data = io.BytesIO(content)
            length = len(content)
            
            self.client.put_object(
                bucket_name=bucket_name,
                object_name=filename,
                data=data,
                length=length,
                content_type=content_type or "application/octet-stream",
            )
            
            # Возвращаем URL файла
            return f"{bucket_name}/{filename}"
            
        except S3Error as e:
            raise Exception(f"Ошибка при загрузке файла в MinIO: {e}")
    
    async def get_file(self, bucket_name: str, filename: str) -> bytes:
        """Получить файл из MinIO"""
        
        try:
            response = self.client.get_object(bucket_name, filename)
            return response.read()
        except S3Error as e:
            raise Exception(f"Ошибка при получении файла из MinIO: {e}")
        finally:
            response.close()
            response.release_conn()
    
    async def delete_file(self, bucket_name: str, filename: str):
        """Удалить файл из MinIO"""
        
        try:
            self.client.remove_object(bucket_name, filename)
        except S3Error as e:
            raise Exception(f"Ошибка при удалении файла из MinIO: {e}")
    
    async def get_presigned_url(
        self,
        bucket_name: str,
        filename: str,
        expires_seconds: int = 3600,
    ) -> str:
        """Получить предварительно подписанный URL для доступа к файлу"""
        
        try:
            return self.client.presigned_get_object(
                bucket_name=bucket_name,
                object_name=filename,
                expires=expires_seconds,
            )
        except S3Error as e:
            raise Exception(f"Ошибка при получении подписанного URL: {e}")
```

### Файл: `app/api/__init__.py`
```python
"""
API модули системы НМЦК
"""
from . import session, upload, task, contract, selection, stop

__all__ = ['session', 'upload', 'task', 'contract', 'selection', 'stop']

```

### Файл: `app/api/contract.py`
```python
"""
Роутер для работы с контрактами
"""
import json
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.infra.database import get_db
from app.domain.entities.session import SessionEntity as DBSession
from app.domain.entities.contract import ContractEntity
from app.domain.entities.audit import ContractAuditEntity
from app.schemas.contract import ContractResponse, AuditLogResponse

router = APIRouter()

@router.get("/contracts/{contract_id}/audit-log", response_model=List[AuditLogResponse])
async def get_contract_audit_log(
    request: Request,
    contract_id: str,
    db: Session = Depends(get_db)
):
    """
    Получить лог сверки характеристик для контракта.
    """
    # Получаем session_token из куков
    session_token = request.cookies.get("session_token")
    if not session_token:
        raise HTTPException(status_code=401, detail="Сессия не найдена")
    
    # Получаем контракт
    contract = db.query(ContractEntity).filter(ContractEntity.id == contract_id).first()
    if not contract:
        raise HTTPException(status_code=404, detail="Контракт не найден")
    
    # Проверяем, что контракт принадлежит задаче пользователя
    task = contract.task
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    
    task_session_id_str = str(task.session_id)
    if task_session_id_str != session_token:
        raise HTTPException(status_code=403, detail=f"Доступ запрещен. Task session: {task_session_id_str}, User session: {session_token}")
    
    # Получаем лог сверки
    audit_rows = db.query(ContractAuditEntity).filter(
        ContractAuditEntity.contract_id == contract_id
    ).order_by(ContractAuditEntity.id).all()
    
    # Формируем ответ
    result = []
    for row in audit_rows:
        result.append(AuditLogResponse(
            key=row.key,
            expected_value=row.expected_value,
            found_value=row.found_value,
            is_diff=row.is_diff,
            diff_reason=row.diff_reason
        ))
    
    return result

@router.get("/contracts/{contract_id}/details")
async def get_contract_details(
    request: Request,
    contract_id: str,
    db: Session = Depends(get_db)
):
    """
    Получить детальную информацию о контракте.
    """
    # Получаем session_token из куков
    session_token = request.cookies.get("session_token")
    if not session_token:
        raise HTTPException(status_code=401, detail="Сессия не найдена")
    
    # Получаем контракт
    contract = db.query(ContractEntity).filter(ContractEntity.id == contract_id).first()
    if not contract:
        raise HTTPException(status_code=404, detail="Контракт не найден")
    
    # Проверяем, что контракт принадлежит задаче пользователя
    task = contract.task
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    
    task_session_id_str = str(task.session_id)
    if task_session_id_str != session_token:
        raise HTTPException(status_code=403, detail=f"Доступ запрещен. Task session: {task_session_id_str}, User session: {session_token}")
    
    # Парсим raw данные
    raw_data = {}
    if contract.raw_payload_json:
        try:
            raw_data = json.loads(contract.raw_payload_json)
        except:
            raw_data = {"error": "Не удалось распарсить данные"}
    
    # Формируем ответ
    response = {
        "id": contract.id,
        "reg_number": contract.reg_number,
        "eis_url": contract.eis_url,
        "supplier_name": contract.supplier_name,
        "supplier_inn": contract.supplier_inn,
        "sign_date": contract.sign_date,
        "unit_price": contract.unit_price,
        "currency": contract.currency,
        "match_percent": contract.match_percent,
        "match_type": contract.match_type,
        "vendor_status": contract.vendor_status,
        "raw_data": raw_data
    }
    
    return response

```

### Файл: `app/api/results.py`
```python
from typing import List, Dict
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from app.models.database import get_db
from app.dependencies.session import get_or_create_session
from app.domain.entities.session import SessionEntity
from app.domain.entities.task import TaskEntityEntity, TaskStatus
from app.domain.entities.contract import ContractEntity, MatchType
from app.domain.entities.audit import ContractAuditEntity
from app.domain.entities.selection import TaskSelectionEntity
from app.schemas.contract import TaskResultResponse, TaskResultSummary, ContractResponse, ContractAuditResponse
from app.schemas.task import TaskResponse

router = APIRouter(prefix="/tasks", tags=["results"])


@router.get("/{task_id}/result", response_model=TaskResultResponse)
async def get_task_result(
    task_id: UUID,
    session: SessionEntity = Depends(get_or_create_session),
    db: AsyncSession = Depends(get_db),
):
    """Получить результаты задачи"""
    
    # Получаем задачу
    stmt = select(TaskEntity).where(
        TaskEntity.id == task_id,
        TaskEntity.session_id == session.id,
        TaskEntity.status == TaskStatus.DONE,
    )
    result = await db.execute(stmt)
    task = result.scalar_one_or_none()
    
    if not task:
        raise HTTPException(
            status_code=404,
            detail="Задача не найдена или еще не завершена",
        )
    
    # Получаем контракты
    contracts_stmt = select(ContractEntity).where(
        ContractEntity.task_id == task_id
    ).order_by(
        ContractEntity.match_percent.desc(),
        ContractEntity.unit_price.asc(),
    )
    contracts_result = await db.execute(contracts_stmt)
    contracts = contracts_result.scalars().all()
    
    # Получаем выбранные контракты
    selection_stmt = select(TaskSelectionEntity).where(
        TaskSelectionEntity.task_id == task_id
    )
    selection_result = await db.execute(selection_stmt)
    selections = selection_result.scalars().all()
    selected_contract_ids = {sel.contract_id for sel in selections}
    
    # Подготавливаем контракты для ответа
    contract_responses = []
    for contract in contracts:
        # Определяем метку производителя
        vendor_mark = ""
        if contract.vendor_status == "mismatch":
            vendor_mark = "Производитель отличается"
        
        contract_response = ContractResponse(
            id=contract.id,
            created_at=contract.created_at,
            updated_at=contract.updated_at,
            task_id=contract.task_id,
            reg_number=contract.reg_number,
            eis_url=contract.eis_url,
            supplier_name=contract.supplier_name,
            supplier_inn=contract.supplier_inn,
            sign_date=contract.sign_date,
            unit_price=contract.unit_price,
            currency=contract.currency,
            match_percent=contract.match_percent,
            match_type=contract.match_type,
            vendor_status=contract.vendor_status,
            is_selected=contract.id in selected_contract_ids,
            vendor_mark=vendor_mark,
        )
        contract_responses.append(contract_response)
    
    # Получаем лог сверки для выбранных контрактов
    audit_logs = {}
    if selected_contract_ids:
        audit_stmt = select(ContractAuditEntity).where(
            ContractAuditEntity.contract_id.in_(selected_contract_ids)
        )
        audit_result = await db.execute(audit_stmt)
        audits = audit_result.scalars().all()
        
        for audit in audits:
            if audit.contract_id not in audit_logs:
                audit_logs[audit.contract_id] = []
            
            audit_response = ContractAuditResponse(
                id=audit.id,
                created_at=audit.created_at,
                updated_at=audit.updated_at,
                contract_id=audit.contract_id,
                key=audit.key,
                expected_value=audit.expected_value,
                found_value=audit.found_value,
                is_diff=audit.is_diff,
                diff_reason=audit.diff_reason,
            )
            audit_logs[audit.contract_id].append(audit_response)
    
    # Подсчитываем статистику
    identical_count = sum(1 for c in contracts if c.match_type == MatchType.IDENTICAL)
    homogeneous_count = sum(1 for c in contracts if c.match_type == MatchType.HOMOGENEOUS)
    different_count = sum(1 for c in contracts if c.match_type == MatchType.DIFFERENT)
    
    # Формируем сводку
    summary = TaskResultSummary(
        total_contracts=len(contracts),
        identical_matches=identical_count,
        homogeneous_matches=homogeneous_count,
        different_matches=different_count,
        nmck_value=task.nmck_value,
        nmck_currency=task.nmck_currency or "RUB",
        selected_contracts=list(selected_contract_ids),
    )
    
    return TaskResultResponse(
        summary=summary,
        contracts=contract_responses,
        audit_logs=audit_logs,
    )


@router.get("/contracts/{contract_id}/audit-log", response_model=List[ContractAuditResponse])
async def get_contract_audit_log(
    contract_id: UUID,
    session: SessionEntity = Depends(get_or_create_session),
    db: AsyncSession = Depends(get_db),
):
    """Получить лог сверки для контракта"""
    
    # Проверяем доступ к контракту
    stmt = select(ContractEntity).join(TaskEntity).where(
        ContractEntity.id == contract_id,
        TaskEntity.session_id == session.id,
    )
    result = await db.execute(stmt)
    contract = result.scalar_one_or_none()
    
    if not contract:
        raise HTTPException(
            status_code=404,
            detail="Контракт не найден",
        )
    
    # Получаем лог сверки
    audit_stmt = select(ContractAuditEntity).where(
        ContractAuditEntity.contract_id == contract_id
    ).order_by(ContractAuditEntity.key)
    
    audit_result = await db.execute(audit_stmt)
    audits = audit_result.scalars().all()
    
    return [
        ContractAuditResponse.from_orm(audit) for audit in audits
    ]
```

### Файл: `app/api/selection.py`
```python
"""
Роутер для выбора контрактов и расчета НМЦК
"""
import json
from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.infra.database import get_db
from app.domain.entities.session import SessionEntity as DBSession
from app.domain.entities.task import TaskEntity, TaskStatus
from app.domain.entities.contract import ContractEntity
from app.domain.entities.selection import TaskSelectionEntity
from app.domain.entities.calculation import TaskCalculationEntity
from app.schemas.selection import SelectionUpdate, SelectionResponse
from app.schemas.task import TaskResponse

router = APIRouter()

@router.post("/tasks/{task_id}/selection", response_model=SelectionResponse)
async def update_selection(
    request: Request,
    task_id: str,
    selection_data: SelectionUpdate,
    db: Session = Depends(get_db)
):
    """
    Обновить выбор контрактов для расчета НМЦК.
    
    Проверяет правило: нельзя выбрать 3 контракта от одного поставщика.
    """
    # Получаем session_token из куков
    session_token = request.cookies.get("session_token")
    if not session_token:
        raise HTTPException(status_code=401, detail="Сессия не найдена")
    
    # Получаем задачу
    task = db.query(TaskEntity).filter(
        TaskEntity.id == task_id,
        TaskEntity.session_id == session_token
    ).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    
    if task.status != TaskStatus.DONE:
        raise HTTPException(status_code=400, detail="Задача еще не завершена")
    
    # Проверяем количество контрактов
    if len(selection_data.contract_ids) != 3:
        raise HTTPException(
            status_code=400,
            detail="Для расчета НМЦК необходимо выбрать ровно 3 контракта"
        )
    
    # Получаем информацию о выбранных контрактах
    # Преобразуем строки в UUID для фильтрации
    from uuid import UUID
    try:
        contract_uuids = [UUID(contract_id) for contract_id in selection_data.contract_ids]
    except ValueError:
        raise HTTPException(status_code=400, detail="Некорректный формат ID контрактов")
    
    contracts = db.query(ContractEntity).filter(
        ContractEntity.id.in_(contract_uuids),
        ContractEntity.task_id == task_id
    ).all()
    
    if len(contracts) != 3:
        raise HTTPException(
            status_code=400,
            detail="Не все выбранные контракты найдены"
        )
    
    # Проверяем правило поставщиков
    supplier_counts = {}
    for contract in contracts:
        supplier = contract.supplier_name
        supplier_counts[supplier] = supplier_counts.get(supplier, 0) + 1
    
    # Нельзя выбрать 3 контракта от одного поставщика
    for supplier, count in supplier_counts.items():
        if count >= 3:
            raise HTTPException(
                status_code=409,
                detail=f"Нельзя выбрать 3 контракта от одного поставщика ({supplier})"
            )
    
    # Удаляем старый выбор
    db.query(TaskSelectionEntity).filter(TaskSelectionEntity.task_id == task_id).delete()
    
    # Сохраняем новый выбор
    for contract_id in selection_data.contract_ids:
        selection = TaskSelectionEntity(
            task_id=task_id,
            contract_id=contract_id,
            selected_at=datetime.utcnow()
        )
        db.add(selection)
    
    # Рассчитываем НМЦК
    total_price = sum(contract.unit_price for contract in contracts)
    nmck_value = total_price / 3  # Среднее арифметическое
    
    # Сохраняем расчет
    calculation = TaskCalculationEntity(
        task_id=task_id,
        method="average",
        nmc_value=nmck_value,
        computed_at=datetime.utcnow(),
        details=json.dumps({
            "selected_contracts": selection_data.contract_ids,
            "calculation_method": "average",
            "contract_prices": [contract.unit_price for contract in contracts],
            "supplier_counts": supplier_counts
        })
    )
    
    db.add(calculation)
    db.commit()
    
    return SelectionResponse(
        task_id=task_id,
        selected_contracts=selection_data.contract_ids,
        nmck_value=nmck_value,
        calculation_method="average",
        supplier_counts=supplier_counts
    )

@router.get("/tasks/{task_id}/selection", response_model=SelectionResponse)
async def get_selection(
    request: Request,
    task_id: str,
    db: Session = Depends(get_db)
):
    """
    Получить текущий выбор контрактов для задачи.
    """
    # Получаем session_token из куков
    session_token = request.cookies.get("session_token")
    if not session_token:
        raise HTTPException(status_code=401, detail="Сессия не найдена")
    
    # Получаем задачу
    task = db.query(TaskEntity).filter(
        TaskEntity.id == task_id,
        TaskEntity.session_id == session_token
    ).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    
    # Получаем выбранные контракты
    selections = db.query(TaskSelectionEntity).filter(
        TaskSelectionEntity.task_id == task_id
    ).all()
    
    selected_contract_ids = [str(selection.contract_id) for selection in selections]
    
    # Получаем расчет НМЦК
    calculation = db.query(TaskCalculationEntity).filter(
        TaskCalculationEntity.task_id == task_id
    ).order_by(TaskCalculationEntity.computed_at.desc()).first()
    
    # Если есть выбранные контракты, получаем информацию о поставщиках
    supplier_counts = {}
    if selected_contract_ids:
        # Преобразуем строки в UUID для фильтрации
        from uuid import UUID
        try:
            contract_uuids = [UUID(contract_id) for contract_id in selected_contract_ids]
        except ValueError:
            raise HTTPException(status_code=400, detail="Некорректный формат ID контрактов")
        
        contracts = db.query(ContractEntity).filter(
            ContractEntity.id.in_(contract_uuids)
        ).all()
        
        for contract in contracts:
            supplier = contract.supplier_name
            supplier_counts[supplier] = supplier_counts.get(supplier, 0) + 1
    
    return SelectionResponse(
        task_id=task_id,
        selected_contracts=selected_contract_ids,
        nmck_value=calculation.nmc_value if calculation else None,
        calculation_method=calculation.method if calculation else None,
        supplier_counts=supplier_counts
    )


@router.post("/tasks/{task_id}/stop", response_model=TaskResponse)
async def stop_task(
    task_id: str,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Остановить выполнение задачи.
    """
    # Получаем session_token из куков
    session_token = request.cookies.get("session_token")
    if not session_token:
        raise HTTPException(status_code=401, detail="Сессия не найдена")
    
    # Получаем задачу
    task = db.query(TaskEntity).filter(
        TaskEntity.id == task_id,
        TaskEntity.session_id == session_token
    ).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    
    # Проверяем, можно ли остановить задачу
    if task.status not in [TaskStatus.QUEUED, TaskStatus.SEARCHING, TaskStatus.DOWNLOADING, TaskStatus.ANALYZING]:
        raise HTTPException(
            status_code=400, 
            detail=f"Задачу со статусом {task.status} нельзя остановить"
        )
    
    # Обновляем статус задачи
    task.status = TaskStatus.STOPPED
    task.finished_at = datetime.utcnow()
    task.stage = "stopped"
    task.progress = 100
    
    db.commit()
    db.refresh(task)
    
    return TaskResponse(
        id=str(task.id),
        session_id=str(task.session_id),
        upload_id=str(task.upload_id),
        status=task.status,
        stage=task.stage,
        progress=task.progress,
        region=task.region,
        period_from=task.period_from,
        period_to=task.period_to,
        created_at=task.created_at,
        started_at=task.started_at,
        finished_at=task.finished_at,
        error_code=task.error_code,
        error_detail=task.error_detail
    )

```

### Файл: `app/api/session.py`
```python
"""
Роутер для работы с сессиями
"""
import uuid
import logging
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy.orm import Session

from app.infra.database import get_db
from app.domain.entities.session import SessionEntity
from app.schemas.session import SessionCreate, SessionResponse

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/session", response_model=SessionResponse)
async def get_or_create_session(
    request: Request,
    response: Response,
    db: Session = Depends(get_db)
):
    """
    Получить или создать сессию.

    Если в куках есть session_token, возвращает существующую сессию.
    Если нет - создает новую сессию и устанавливает куку.
    """
    # Проверяем наличие session_token в куках
    session_token = request.cookies.get("session_token")

    if session_token:
        # Ищем существующую сессию
        try:
            session_uuid = uuid.UUID(session_token)
            # Для SQLite ищем по строковому представлению
            from app.infra.config import settings
            if "sqlite" in settings.DATABASE_URL:
                session_entity = db.query(SessionEntity).filter(
                    SessionEntity.id == str(session_uuid)
                ).first()
            else:
                session_entity = db.query(SessionEntity).filter(
                    SessionEntity.id == session_uuid
                ).first()
        except ValueError:
            session_entity = None

        if session_entity:
            # Обновляем время последнего визита
            session_entity.last_seen_at = datetime.utcnow()
            db.commit()

            # Отладка
            logger.error(f"DEBUG: session_entity.id = {session_entity.id}, type = {type(session_entity.id)}")

            return SessionResponse(
                id=str(session_entity.id),
                created_at=session_entity.created_at,
                last_seen_at=session_entity.last_seen_at,
                token=str(session_entity.id)  # Добавляем токен для совместимости с фронтендом
            )

    # Создаем новую сессию
    session_uuid = uuid.uuid4()
    session_uuid_str = str(session_uuid)
    logger.error(f"DEBUG: Creating session with uuid = {session_uuid_str}, type = {type(session_uuid_str)}")
    
    # Для SQLite используем строковое представление UUID
    from app.infra.config import settings
    if "sqlite" in settings.DATABASE_URL:
        session_entity = SessionEntity(
            id=session_uuid_str,  # Используем строку для SQLite
            token=session_uuid_str,
            created_at=datetime.utcnow(),
            last_seen_at=datetime.utcnow()
        )
    else:
        session_entity = SessionEntity(
            id=session_uuid,  # Используем UUID объект для PostgreSQL
            token=session_uuid_str,
            created_at=datetime.utcnow(),
            last_seen_at=datetime.utcnow()
        )
    
    logger.error(f"DEBUG: session_entity created, id = {session_entity.id}, type = {type(session_entity.id)}")

    db.add(session_entity)
    db.commit()

    # Устанавливаем куку
    response.set_cookie(
        key="session_token",
        value=session_uuid_str,
        httponly=True,
        max_age=86400 * 30,  # 30 дней
        samesite="lax"
    )

    # Отладка
    logger.error(f"DEBUG: session_id_str = {session_uuid_str}, type = {type(session_uuid_str)}")
    logger.error(f"DEBUG: session_entity.id = {session_entity.id}, type = {type(session_entity.id)}")
    logger.error(f"DEBUG: session_entity.created_at = {session_entity.created_at}, type = {type(session_entity.created_at)}")
    logger.error(f"DEBUG: session_entity.last_seen_at = {session_entity.last_seen_at}, type = {type(session_entity.last_seen_at)}")

    return SessionResponse(
        id=session_uuid_str,
        created_at=session_entity.created_at,
        last_seen_at=session_entity.last_seen_at,
        token=session_uuid_str  # Добавляем токен для совместимости с фронтендом
    )

@router.delete("/session")
async def delete_session(
    request: Request,
    response: Response,
    db: Session = Depends(get_db)
):
    """
    Удалить сессию (выход из системы).
    """
    session_token = request.cookies.get("session_token")
    
    if session_token:
        try:
            session_uuid = uuid.UUID(session_token)
            # Для SQLite ищем по строковому представлению
            from app.infra.config import settings
            if "sqlite" in settings.DATABASE_URL:
                session_entity = db.query(SessionEntity).filter(
                    SessionEntity.id == str(session_uuid)
                ).first()
            else:
                session_entity = db.query(SessionEntity).filter(
                    SessionEntity.id == session_uuid
                ).first()
            
            if session_entity:
                db.delete(session_entity)
                db.commit()
        except ValueError:
            pass
    
    # Удаляем куку
    response.delete_cookie(key="session_token")
    
    return {"message": "Сессия удалена"}

```

### Файл: `app/api/stop.py`
```python
"""
Роутер для остановки задач
"""
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.infra.database import get_db
from app.domain.entities.task import TaskEntity, TaskStatus
from app.schemas.task import TaskResponse

router = APIRouter()

@router.post("/tasks/{task_id}/stop", response_model=TaskResponse)
async def stop_task(
    task_id: str,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Остановить выполнение задачи.
    """
    # Получаем session_token из куков
    session_token = request.cookies.get("session_token")
    if not session_token:
        raise HTTPException(status_code=401, detail="Сессия не найдена")
    
    # Получаем задачу
    task = db.query(TaskEntity).filter(
        TaskEntity.id == task_id,
        TaskEntity.session_id == session_token
    ).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    
    # Проверяем, можно ли остановить задачу
    if task.status not in [TaskStatus.QUEUED, TaskStatus.SEARCHING, TaskStatus.DOWNLOADING, TaskStatus.ANALYZING]:
        raise HTTPException(
            status_code=400, 
            detail=f"Задачу со статусом {task.status} нельзя остановить"
        )
    
    # Обновляем статус задачи
    task.status = TaskStatus.STOPPED
    task.finished_at = datetime.utcnow()
    task.stage = "stopped"
    task.progress = 100
    
    db.commit()
    db.refresh(task)
    
    return TaskResponse(
        id=str(task.id),
        session_id=str(task.session_id),
        upload_id=str(task.upload_id),
        status=task.status,
        stage=task.stage,
        progress=task.progress,
        region=task.region,
        period_from=task.period_from,
        period_to=task.period_to,
        created_at=task.created_at,
        started_at=task.started_at,
        finished_at=task.finished_at,
        error_code=task.error_code,
        error_detail=task.error_detail
    )
```

### Файл: `app/api/task.py`
```python
"""
Роутер для работы с задачами
"""
import json
from datetime import datetime, timedelta
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session

from app.infra.database import get_db
from app.domain.entities.session import SessionEntity as DBSession
from app.domain.entities.upload import UploadEntity
from app.domain.entities.task import TaskEntity, TaskStatus
from app.domain.entities.contract import ContractEntity
from app.domain.entities.selection import TaskSelectionEntity
from app.domain.entities.calculation import TaskCalculationEntity
from app.schemas.task import TaskCreate, TaskCreateDirect, TaskResponse, TaskListResponse, TaskResultResponse, TaskProgressEvent, TaskStatsResponse
from app.workers.celery_app import celery_app

router = APIRouter()

# Хранилище WebSocket соединений
active_connections = {}

@router.post("/tasks", response_model=TaskResponse)
async def create_task(
    request: Request,
    task_data: TaskCreate,
    db: Session = Depends(get_db)
):
    """
    Создать задачу поиска.
    """
    # Получаем session_token из куков
    session_token = request.cookies.get("session_token")
    if not session_token:
        raise HTTPException(status_code=401, detail="Сессия не найдена")
    
    # Проверяем существование загрузки
    upload = db.query(UploadEntity).filter(
        UploadEntity.id == task_data.upload_id,
        UploadEntity.session_id == session_token
    ).first()
    
    if not upload:
        raise HTTPException(status_code=404, detail="Загрузка не найдена")
    
    # Рассчитываем период поиска
    period_to = datetime.utcnow()
    period_from = period_to - timedelta(days=task_data.period_years * 365)
    
    # Создаем задачу
    task = TaskEntity(
        session_id=session_token,
        upload_id=task_data.upload_id,
        status="queued",
        stage="queued",
        progress=0,
        region=task_data.region,
        period_from=period_from,
        period_to=period_to,
        created_at=datetime.utcnow()
    )
    
    db.add(task)
    db.commit()
    db.refresh(task)
    
    # Запускаем задачу в фоне (синхронно для тестирования)
    # TODO: Включить Celery после настройки Redis
    # celery_app.send_task("app.workers.search_worker.run_search_task", args=[task.id])
    # Временно запускаем mock воркер
    from app.workers.mock_worker import mock_run_search_task
    import threading
    thread = threading.Thread(target=mock_run_search_task, args=(task.id,))
    thread.daemon = True
    thread.start()
    
    return TaskResponse(
        id=str(task.id),
        session_id=str(task.session_id),
        upload_id=str(task.upload_id),
        status=task.status,
        stage=task.stage,
        progress=task.progress,
        region=task.region,
        period_from=task.period_from,
        period_to=task.period_to,
        created_at=task.created_at,
        started_at=task.started_at,
        finished_at=task.finished_at,
        error_code=task.error_code,
        error_detail=task.error_detail
    )


@router.post("/tasks/direct", response_model=TaskResponse)
async def create_task_direct(
    request: Request,
    task_data: TaskCreateDirect,
    db: Session = Depends(get_db)
):
    """
    Создать задачу поиска напрямую (без файла).
    """
    # Получаем session_token из куков
    session_token = request.cookies.get("session_token")
    if not session_token:
        raise HTTPException(status_code=401, detail="Сессия не найдена")
    
    # Создаем виртуальную загрузку с данными из формы
    import uuid
    import json
    
    upload_id = str(uuid.uuid4())
    
    # Создаем extracted_data с данными из формы
    extracted_data = {
        "ktru_code": task_data.ktru_code,
        "name": task_data.product_name,
        "vendor": task_data.vendor,
        "characteristics": task_data.characteristics
    }
    
    # Создаем запись загрузки
    upload = UploadEntity(
        id=upload_id,
        session_id=session_token,
        filename=f"manual_{task_data.product_name}.txt",
        mime_type="text/plain",
        storage_url=f"manual://{upload_id}",
        extracted_data=extracted_data,
        created_at=datetime.utcnow()
    )
    
    db.add(upload)
    db.commit()
    db.refresh(upload)
    
    # Рассчитываем период поиска
    period_to = datetime.utcnow()
    period_from = period_to - timedelta(days=task_data.period_years * 365)
    
    # Создаем задачу
    task = TaskEntity(
        session_id=session_token,
        upload_id=upload_id,
        status="queued",
        stage="queued",
        progress=0,
        region=task_data.region,
        period_from=period_from,
        period_to=period_to,
        created_at=datetime.utcnow()
    )
    
    # Устанавливаем дополнительные поля
    task.product_name = task_data.product_name
    task.ktru_code = task_data.ktru_code
    
    db.add(task)
    db.commit()
    db.refresh(task)
    
    # Запускаем задачу в фоне (синхронно для тестирования)
    from app.workers.mock_worker import mock_run_search_task
    import threading
    thread = threading.Thread(target=mock_run_search_task, args=(task.id,))
    thread.daemon = True
    thread.start()
    
    return TaskResponse(
        id=str(task.id),
        session_id=str(task.session_id),
        upload_id=str(task.upload_id),
        status=task.status,
        stage=task.stage,
        progress=task.progress,
        region=task.region,
        period_from=task.period_from,
        period_to=task.period_to,
        created_at=task.created_at,
        started_at=task.started_at,
        finished_at=task.finished_at,
        error_code=task.error_code,
        error_detail=task.error_detail,
    )


@router.get("/tasks", response_model=List[TaskListResponse])
async def get_tasks(
    request: Request,
    status: Optional[str] = None,
    region: Optional[str] = None,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """
    Получить список задач пользователя с фильтрацией.
    """
    # Получаем session_token из куков
    session_token = request.cookies.get("session_token")
    if not session_token:
        raise HTTPException(status_code=401, detail="Сессия не найдена")
    
    # Строим запрос с фильтрами
    query = db.query(TaskEntity).filter(
        TaskEntity.session_id == session_token
    )
    
    # Применяем фильтры
    if status:
        query = query.filter(TaskEntity.status == status)
    if region:
        query = query.filter(TaskEntity.region == region)
    
    # Получаем задачи пользователя
    tasks = query.order_by(TaskEntity.created_at.desc()).limit(limit).all()
    
    result = []
    for task in tasks:
        # Получаем информацию о товаре/КТРУ из задачи или загрузки
        product_name = getattr(task, 'product_name', None) or "Неизвестный товар"
        ktru_code = getattr(task, 'ktru_code', None)
        
        # Если в задаче нет данных, пытаемся получить из загрузки
        if not product_name or product_name == "Неизвестный товар" and task.upload_id:
            upload = db.query(UploadEntity).filter(UploadEntity.id == task.upload_id).first()
            if upload and upload.extracted_data:
                try:
                    extracted_data = json.loads(upload.extracted_data)
                    if extracted_data.get("name"):
                        product_name = extracted_data["name"]
                    elif extracted_data.get("product_name"):
                        product_name = extracted_data["product_name"]
                    if not ktru_code:
                        ktru_code = extracted_data.get("ktru_code")
                except:
                    pass
        
        # Формируем краткий итог
        summary = None
        if task.status == "done":
            contracts_count = db.query(ContractEntity).filter(
                ContractEntity.task_id == task.id
            ).count()
            summary = f"Найдено контрактов: {contracts_count}"
        
        # Рассчитываем время поиска
        search_time = None
        if task.started_at and task.finished_at:
            search_time = int((task.finished_at - task.started_at).total_seconds())
        
        result.append(TaskListResponse(
            id=str(task.id),
            created_at=task.created_at,
            status=task.status,
            stage=task.stage,
            progress=task.progress,
            region=task.region,
            summary=summary,
            search_time=search_time,
            product_name=product_name,  # Добавляем информацию о товаре
            ktru_code=ktru_code
        ))
    
    return result

@router.get("/tasks/stats", response_model=TaskStatsResponse)
async def get_task_stats(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Получить статистику по задачам.
    """
    # Получаем session_token из куков
    session_token = request.cookies.get("session_token")
    if not session_token:
        raise HTTPException(status_code=401, detail="Сессия не найдена")
    
    # Получаем все задачи для сессии
    tasks = db.query(TaskEntity).filter(
        TaskEntity.session_id == session_token
    ).all()
    
    # Считаем задачи по статусам
    queued_tasks = len([t for t in tasks if t.status == "queued"])
    searching_tasks = len([t for t in tasks if t.status == "searching"])
    downloading_tasks = len([t for t in tasks if t.status == "downloading"])
    analyzing_tasks = len([t for t in tasks if t.status == "analyzing"])
    done_tasks = len([t for t in tasks if t.status == "done"])
    error_tasks = len([t for t in tasks if t.status == "error"])
    
    # Активные задачи (в поиске, скачивании, анализе)
    active_tasks = searching_tasks + downloading_tasks + analyzing_tasks
    
    # Считаем общее количество найденных контрактов
    total_found = 0
    for task in tasks:
        if task.status == "done":
            total_found += task.total_found or 0
    
    # Считаем среднее время поиска
    search_times = []
    for task in tasks:
        if task.started_at and task.finished_at:
            search_time = (task.finished_at - task.started_at).total_seconds()
            search_times.append(search_time)
    
    avg_search_time = sum(search_times) / len(search_times) if search_times else None
    
    # Считаем успешность (процент завершенных задач)
    completed_tasks = len([t for t in tasks if t.status == "done"])
    success_rate = (completed_tasks / len(tasks)) * 100 if tasks else None
    
    return TaskStatsResponse(
        active_tasks=active_tasks,
        total_found=total_found,
        total_tasks=len(tasks),
        avg_search_time=avg_search_time,
        success_rate=success_rate,
        queued_tasks=queued_tasks,
        searching_tasks=searching_tasks,
        done_tasks=done_tasks
    )

@router.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task(
    request: Request,
    task_id: str,
    db: Session = Depends(get_db)
):
    """
    Получить информацию о задаче.
    """
    # Получаем session_token из куков
    session_token = request.cookies.get("session_token")
    if not session_token:
        raise HTTPException(status_code=401, detail="Сессия не найдена")
    
    # Получаем задачу
    task = db.query(TaskEntity).filter(
        TaskEntity.id == task_id,
        TaskEntity.session_id == session_token
    ).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    
    return TaskResponse(
        id=str(task.id),
        session_id=str(task.session_id),
        upload_id=str(task.upload_id),
        status=task.status,
        stage=task.stage,
        progress=task.progress,
        region=task.region,
        period_from=task.period_from,
        period_to=task.period_to,
        created_at=task.created_at,
        started_at=task.started_at,
        finished_at=task.finished_at,
        error_code=task.error_code,
        error_detail=task.error_detail
    )


@router.get("/tasks/{task_id}/result", response_model=TaskResultResponse)
async def get_task_result(
    request: Request,
    task_id: str,
    db: Session = Depends(get_db)
):
    """
    Получить результаты задачи.
    """
    # Получаем session_token из куков
    session_token = request.cookies.get("session_token")
    if not session_token:
        raise HTTPException(status_code=401, detail="Сессия не найдена")
    
    # Получаем задачу
    task = db.query(TaskEntity).filter(
        TaskEntity.id == task_id,
        TaskEntity.session_id == session_token
    ).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    
    if task.status != "done":
        raise HTTPException(status_code=400, detail="Задача еще не завершена")
    
    # Получаем контракты
    contracts = db.query(ContractEntity).filter(
        ContractEntity.task_id == task_id
    ).order_by(ContractEntity.match_percent.desc()).all()
    
    # Получаем выбранные контракты
    selected_contracts = db.query(TaskSelectionEntity).filter(
        TaskSelectionEntity.task_id == task_id
    ).all()
    selected_contract_ids = {sc.contract_id for sc in selected_contracts}
    
    # Формируем список контрактов
    contracts_list = []
    for contract in contracts:
        contracts_list.append({
            "id": str(contract.id),
            "reg_number": contract.reg_number,
            "eis_url": contract.eis_url,
            "supplier_name": contract.supplier_name,
            "supplier_inn": contract.supplier_inn,
            "sign_date": contract.sign_date,
            "unit_price": float(contract.unit_price),
            "currency": contract.currency,
            "match_percent": contract.match_percent,
            "match_type": contract.match_type,
            "vendor_status": contract.vendor_status,
            "selected": contract.id in selected_contract_ids
        })
    
    # Получаем расчет НМЦК
    calculation = db.query(TaskCalculationEntity).filter(
        TaskCalculationEntity.task_id == task_id
    ).order_by(TaskCalculationEntity.computed_at.desc()).first()
    
    recommended_nmck = None
    if calculation:
        recommended_nmck = calculation.nmc_value
    
    # Формируем summary
    summary = {
        "total_contracts": len(contracts),
        "found_contracts": len([c for c in contracts if c.match_percent > 0]),
        "identical_matches": len([c for c in contracts if c.match_type == "identical"]),
        "homogeneous_matches": len([c for c in contracts if c.match_type == "homogeneous"]),
        "average_match_percent": sum(c.match_percent for c in contracts) / len(contracts) if contracts else 0,
        "recommended_nmck": recommended_nmck
    }
    
    return TaskResultResponse(
        task_id=task_id,
        summary=summary,
        contracts=contracts_list,
        recommended_nmck=recommended_nmck
    )





@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket для получения обновлений статуса задач.
    """
    await websocket.accept()
    
    try:
        while True:
            # Получаем сообщение от клиента
            data = await websocket.receive_json()
            
            if data.get("type") == "subscribe":
                task_id = data.get("task_id")
                if task_id:
                    active_connections[task_id] = websocket
            
            elif data.get("type") == "unsubscribe":
                task_id = data.get("task_id")
                if task_id and task_id in active_connections:
                    del active_connections[task_id]
    
    except WebSocketDisconnect:
        # Удаляем соединение из активных
        for task_id, conn in list(active_connections.items()):
            if conn == websocket:
                del active_connections[task_id]
                break



```

### Файл: `app/api/tasks.py`
```python
from datetime import datetime, timedelta
from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, func
from sqlalchemy.orm import selectinload

from app.models.database import get_db
from app.dependencies.session import get_or_create_session
from app.domain.entities.session import SessionEntity
from app.domain.entities.upload import UploadEntityEntity
from app.domain.entities.task import TaskEntityEntity, TaskStatus
from app.schemas.task import TaskCreate, TaskResponse, TaskListResponse
from app.infra.celery.tasks import run_search_task
from app.infra.config import settings

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("", response_model=TaskResponse)
async def create_task(
    task_data: TaskCreate,
    session: SessionEntity = Depends(get_or_create_session),
    db: AsyncSession = Depends(get_db),
):
    """Создать задачу поиска"""
    
    # Проверяем существование загрузки
    stmt = select(UploadEntity).where(
        UploadEntity.id == task_data.upload_id,
        UploadEntity.session_id == session.id,
    )
    result = await db.execute(stmt)
    upload = result.scalar_one_or_none()
    
    if not upload:
        raise HTTPException(
            status_code=404,
            detail="Загрузка не найдена",
        )
    
    # Проверяем лимит одновременных задач
    active_tasks_stmt = select(func.count(TaskEntity.id)).where(
        TaskEntity.session_id == session.id,
        TaskEntity.status.in_([TaskStatus.QUEUED, TaskStatus.SEARCHING, TaskStatus.DOWNLOADING, TaskStatus.ANALYZING]),
    )
    active_tasks_result = await db.execute(active_tasks_stmt)
    active_tasks_count = active_tasks_result.scalar()
    
    if active_tasks_count >= 5:  # Максимум 5 одновременных задач
        raise HTTPException(
            status_code=429,
            detail="Превышен лимит одновременных задач. Максимум 5 задач одновременно.",
        )
    
    # Рассчитываем период поиска
    period_to = datetime.utcnow()
    period_from = period_to - timedelta(days=task_data.period_years * 365)
    
    # Создаем задачу
    task = TaskEntity(
        session_id=session.id,
        upload_id=upload.id,
        status=TaskStatus.QUEUED,
        region=task_data.region,
        period_from=period_from,
        period_to=period_to,
        law_type=task_data.law_type,
    )
    
    db.add(task)
    await db.commit()
    await db.refresh(task)
    
    # Запускаем задачу в Celery
    run_search_task.delay(str(task.id))
    
    # Формируем ответ
    response_data = TaskResponse.from_orm(task)
    if upload.extracted_data:
        response_data.detected_data = upload.extracted_data
    
    return response_data


@router.get("", response_model=List[TaskListResponse])
async def list_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    status: Optional[TaskStatus] = None,
    session: SessionEntity = Depends(get_or_create_session),
    db: AsyncSession = Depends(get_db),
):
    """Получить список задач"""
    
    # Базовый запрос
    stmt = select(TaskEntity).where(TaskEntity.session_id == session.id)
    
    # Фильтр по статусу
    if status:
        stmt = stmt.where(TaskEntity.status == status)
    
    # Сортировка и пагинация
    stmt = stmt.order_by(desc(TaskEntity.created_at)).offset(skip).limit(limit)
    
    # Загружаем связанные данные
    stmt = stmt.options(selectinload(TaskEntity.upload))
    
    result = await db.execute(stmt)
    tasks = result.scalars().all()
    
    responses = []
    for task in tasks:
        # Рассчитываем время поиска
        search_duration = None
        if task.started_at and task.finished_at:
            search_duration = (task.finished_at - task.started_at).total_seconds()
        elif task.started_at:
            search_duration = (datetime.utcnow() - task.started_at).total_seconds()
        
        # Получаем данные из загрузки
        ktru_code = None
        product_name = None
        if task.upload and task.upload.extracted_data:
            ktru_code = task.upload.extracted_data.get("ktru_code")
            product_name = task.upload.extracted_data.get("name")
        
        response_data = {
            "id": task.id,
            "created_at": task.created_at,
            "updated_at": task.updated_at,
            "upload_id": task.upload_id,
            "status": task.status,
            "stage": task.stage,
            "progress": task.progress,
            "ktru_code": ktru_code,
            "product_name": product_name,
            "total_found": task.total_found,
            "nmck_value": task.nmck_value,
            "started_at": task.started_at,
            "finished_at": task.finished_at,
            "search_duration": search_duration,
        }
        
        responses.append(TaskListResponse(**response_data))
    
    return responses


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: UUID,
    session: SessionEntity = Depends(get_or_create_session),
    db: AsyncSession = Depends(get_db),
):
    """Получить информацию о задаче"""
    
    stmt = select(TaskEntity).where(
        TaskEntity.id == task_id,
        TaskEntity.session_id == session.id,
    ).options(selectinload(TaskEntity.upload))
    
    result = await db.execute(stmt)
    task = result.scalar_one_or_none()
    
    if not task:
        raise HTTPException(
            status_code=404,
            detail="Задача не найдена",
        )
    
    # Формируем ответ
    response_data = TaskResponse.from_orm(task)
    if task.upload and task.upload.extracted_data:
        response_data.detected_data = task.upload.extracted_data
    
    return response_data


@router.post("/{task_id}/cancel")
async def cancel_task(
    task_id: UUID,
    session: SessionEntity = Depends(get_or_create_session),
    db: AsyncSession = Depends(get_db),
):
    """Отменить задачу"""
    
    stmt = select(TaskEntity).where(
        TaskEntity.id == task_id,
        TaskEntity.session_id == session.id,
        TaskEntity.status.in_([TaskStatus.QUEUED, TaskStatus.SEARCHING, TaskStatus.DOWNLOADING, TaskStatus.ANALYZING]),
    )
    
    result = await db.execute(stmt)
    task = result.scalar_one_or_none()
    
    if not task:
        raise HTTPException(
            status_code=404,
            detail="Задача не найдена или не может быть отменена",
        )
    
    # Обновляем статус задачи
    task.status = TaskStatus.CANCELLED
    task.finished_at = datetime.utcnow()
    task.message = "Задача отменена пользователем"
    
    await db.commit()
    await db.refresh(task)
    
    # TODO: Отменить задачу в Celery
    
    return {"message": "Задача отменена"}


@router.get("/{task_id}/progress")
async def get_task_progress(
    task_id: UUID,
    session: SessionEntity = Depends(get_or_create_session),
    db: AsyncSession = Depends(get_db),
):
    """Получить прогресс выполнения задачи"""
    
    stmt = select(TaskEntity).where(
        TaskEntity.id == task_id,
        TaskEntity.session_id == session.id,
    )
    
    result = await db.execute(stmt)
    task = result.scalar_one_or_none()
    
    if not task:
        raise HTTPException(
            status_code=404,
            detail="Задача не найдена",
        )
    
    return {
        "task_id": task.id,
        "status": task.status,
        "stage": task.stage,
        "progress": task.progress,
        "message": task.message,
        "total_found": task.total_found,
        "total_analyzed": task.total_analyzed,
        "timestamp": datetime.utcnow().isoformat(),
    }
```

### Файл: `app/api/upload.py`
```python
"""
Роутер для загрузки и обработки файлов с требованиями
"""
import os
import uuid
from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Request
from sqlalchemy.orm import Session

from app.infra.database import get_db
from app.domain.entities.session import SessionEntity as DBSession
from app.domain.entities.upload import UploadEntity
from app.schemas.upload import UploadResponse, UploadDetectionResponse, CharacteristicSchema
from app.adapters.file_parser import FileParser

router = APIRouter()

# Создаем директорию для загрузок, если её нет
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/uploads", response_model=UploadDetectionResponse)
async def upload_file(
    request: Request,
    file: UploadFile = File(...),
    source_type: Optional[str] = "freeform",
    db: Session = Depends(get_db)
):
    """
    Загрузить файл с требованиями к товару.
    
    Поддерживаемые форматы: TXT, XLSX, DOCX, PDF
    """
    # Получаем session_token из куков
    session_token = request.cookies.get("session_token")
    if not session_token:
        raise HTTPException(status_code=401, detail="Сессия не найдена")
    
    # Проверяем существование сессии
    db_session = db.query(DBSession).filter(DBSession.id == session_token).first()
    if not db_session:
        raise HTTPException(status_code=401, detail="Недействительная сессия")
    
    # Проверяем расширение файла
    allowed_extensions = {'.txt', '.xlsx', '.docx', '.pdf'}
    file_ext = os.path.splitext(file.filename)[1].lower()
    
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Неподдерживаемый формат файла. Разрешены: {', '.join(allowed_extensions)}"
        )
    
    # Генерируем уникальное имя файла
    file_id = str(uuid.uuid4())
    filename = f"{file_id}{file_ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)
    
    # Сохраняем файл
    try:
        content = await file.read()
        with open(filepath, "wb") as f:
            f.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка сохранения файла: {str(e)}")
    
    # Парсим файл
    parser = FileParser()
    try:
        parsed_data = parser.parse_file(filepath, file_ext)
    except Exception as e:
        # Удаляем файл в случае ошибки парсинга
        os.remove(filepath)
        raise HTTPException(status_code=400, detail=f"Ошибка парсинга файла: {str(e)}")
    
    # Создаем запись в БД
    upload = UploadEntity(
        id=file_id,
        session_id=session_token,
        filename=file.filename,
        mime_type=file.content_type,
        storage_url=filepath,
        extracted_data=parsed_data.model_dump_json() if hasattr(parsed_data, 'model_dump_json') else parsed_data,
        created_at=datetime.utcnow()
    )
    
    db.add(upload)
    db.commit()
    db.refresh(upload)
    
    # Формируем ответ
    response_data = {
        "upload_id": str(upload.id),
        "detected": {
            "ktru_code": parsed_data.get("ktru_code"),
            "name": parsed_data.get("name"),
            "vendor": parsed_data.get("vendor"),
            "characteristics": [
                CharacteristicSchema(
                    key=char.get("key"),
                    value=char.get("value"),
                    unit=char.get("unit"),
                    operator=char.get("operator", "=")
                )
                for char in parsed_data.get("characteristics", [])
            ]
        },
        "warnings": parsed_data.get("warnings", [])
    }
    
    return UploadDetectionResponse(**response_data)

@router.get("/uploads/{upload_id}", response_model=UploadResponse)
async def get_upload(
    request: Request,
    upload_id: str,
    db: Session = Depends(get_db)
):
    """
    Получить информацию о загруженном файле.
    """
    # Получаем session_token из куков
    session_token = request.cookies.get("session_token")
    if not session_token:
        raise HTTPException(status_code=401, detail="Сессия не найдена")
    
    # Получаем загрузку
    upload = db.query(Upload).filter(
        Upload.id == upload_id,
        Upload.session_id == session_token
    ).first()
    
    if not upload:
        raise HTTPException(status_code=404, detail="Загрузка не найдена")
    
    # Парсим сохраненные данные
    import json
    parsed_data = json.loads(upload.extracted_json)
    
    # Формируем ответ
    response_data = {
        "upload_id": str(upload.id),
        "detected": {
            "ktru_code": parsed_data.get("ktru_code"),
            "name": parsed_data.get("name"),
            "vendor": parsed_data.get("vendor"),
            "characteristics": [
                CharacteristicSchema(
                    key=char.get("key"),
                    value=char.get("value"),
                    unit=char.get("unit"),
                    operator=char.get("operator", "=")
                )
                for char in parsed_data.get("characteristics", [])
            ]
        },
        "warnings": parsed_data.get("warnings", [])
    }
    
    return UploadDetectionResponse(**response_data)

@router.delete("/uploads/{upload_id}")
async def delete_upload(
    request: Request,
    upload_id: str,
    db: Session = Depends(get_db)
):
    """
    Удалить загруженный файл.
    """
    # Получаем session_token из куков
    session_token = request.cookies.get("session_token")
    if not session_token:
        raise HTTPException(status_code=401, detail="Сессия не найдена")
    
    # Получаем загрузку
    upload = db.query(Upload).filter(
        Upload.id == upload_id,
        Upload.session_id == session_token
    ).first()
    
    if not upload:
        raise HTTPException(status_code=404, detail="Загрузка не найдена")
    
    # Удаляем файл с диска
    if os.path.exists(upload.storage_url):
        os.remove(upload.storage_url)
    
    # Удаляем запись из БД
    db.delete(upload)
    db.commit()
    
    return {"message": "Файл удален"}

```

### Файл: `app/api/websocket.py`
```python
import asyncio
import json
from datetime import datetime
from typing import Dict, Set
from uuid import UUID
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.infra.database import get_db
from app.domain.entities.session import SessionEntity
from app.domain.entities.task import TaskEntity
from app.schemas.task import TaskProgressEvent

router = APIRouter()


class ConnectionManager:
    """Менеджер WebSocket соединений"""
    
    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, session_token: str):
        """Подключить клиента"""
        await websocket.accept()
        
        if session_token not in self.active_connections:
            self.active_connections[session_token] = set()
        
        self.active_connections[session_token].add(websocket)
    
    def disconnect(self, websocket: WebSocket, session_token: str):
        """Отключить клиента"""
        if session_token in self.active_connections:
            self.active_connections[session_token].discard(websocket)
            if not self.active_connections[session_token]:
                del self.active_connections[session_token]
    
    async def send_personal_message(self, message: str, session_token: str):
        """Отправить сообщение конкретному клиенту"""
        if session_token in self.active_connections:
            for connection in self.active_connections[session_token]:
                try:
                    await connection.send_text(message)
                except Exception:
                    pass
    
    async def broadcast(self, message: str):
        """Отправить сообщение всем клиентам"""
        for connections in self.active_connections.values():
            for connection in connections:
                try:
                    await connection.send_text(message)
                except Exception:
                    pass


manager = ConnectionManager()


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    db: AsyncSession = Depends(get_db),
):
    """WebSocket endpoint для обновлений статуса"""
    
    # Получаем токен сессии из query параметров
    session_token = websocket.query_params.get("session_token")
    
    if not session_token:
        await websocket.close(code=1008, reason="Session token required")
        return
    
    # Проверяем сессию
    stmt = select(SessionEntity).where(SessionEntity.token == session_token)
    result = await db.execute(stmt)
    session = result.scalar_one_or_none()
    
    if not session:
        await websocket.close(code=1008, reason="Invalid session token")
        return
    
    # Подключаем клиента
    await manager.connect(websocket, session_token)
    
    try:
        while True:
            # Клиент может отправлять ping сообщения
            data = await websocket.receive_text()
            
            try:
                message = json.loads(data)
                if message.get("type") == "ping":
                    await websocket.send_text(json.dumps({
                        "type": "pong",
                        "timestamp": datetime.utcnow().isoformat(),
                    }))
            except json.JSONDecodeError:
                pass
            
    except WebSocketDisconnect:
        manager.disconnect(websocket, session_token)


async def send_task_progress(task_id: UUID, session_token: str, status: str, stage: str, progress: int, message: str = None):
    """Отправить обновление прогресса задачи"""
    
    event = TaskProgressEvent(
        task_id=task_id,
        status=status,
        stage=stage,
        progress=progress,
        message=message,
    )
    
    await manager.send_personal_message(
        json.dumps({
            "type": "task.progress",
            "data": event.dict(),
        }),
        session_token,
    )


async def send_task_completed(task_id: UUID, session_token: str, result: Dict):
    """Отправить уведомление о завершении задачи"""
    
    await manager.send_personal_message(
        json.dumps({
            "type": "task.completed",
            "data": {
                "task_id": str(task_id),
                "result": result,
                "timestamp": datetime.utcnow().isoformat(),
            },
        }),
        session_token,
    )


async def send_task_error(task_id: UUID, session_token: str, error_code: str, error_message: str):
    """Отправить уведомление об ошибке задачи"""
    
    await manager.send_personal_message(
        json.dumps({
            "type": "task.error",
            "data": {
                "task_id": str(task_id),
                "error_code": error_code,
                "error_message": error_message,
                "timestamp": datetime.utcnow().isoformat(),
            },
        }),
        session_token,
    )
```

### Файл: `app/application/use_cases/search_contracts.py`
```python
"""
Use case для поиска контрактов
"""
from typing import List, Dict, Any
from datetime import datetime

from app.domain.repositories.task_repository import TaskRepository
from app.domain.repositories.upload_repository import UploadRepository
from app.domain.repositories.contract_repository import ContractRepository
from app.domain.entities.task import TaskStatus
from app.adapters.eis.sync_adapter import SyncEISParser
from app.adapters.match_engine import MatchEngine


class SearchContractsUseCase:
    """Use case для поиска контрактов"""
    
    def __init__(
        self,
        task_repository: TaskRepository,
        upload_repository: UploadRepository,
        contract_repository: ContractRepository,
        eis_parser: SyncEISParser,
        match_engine: MatchEngine,
    ):
        self.task_repository = task_repository
        self.upload_repository = upload_repository
        self.contract_repository = contract_repository
        self.eis_parser = eis_parser
        self.match_engine = match_engine
    
    def execute(self, task_id: str) -> Dict[str, Any]:
        """
        Выполнить поиск контрактов
        
        Args:
            task_id: ID задачи
            
        Returns:
            Результат выполнения
        """
        # Получаем задачу
        task = self.task_repository.get_by_id(task_id)
        if not task:
            return {"success": False, "error": "Задача не найдена"}
        
        # Обновляем статус задачи
        task = self.task_repository.update_status(
            task_id=task_id,
            status=TaskStatus.SEARCHING,
            stage="Поиск контрактов",
            progress=10,
        )
        
        # Получаем данные загрузки
        upload = self.upload_repository.get_by_id(task.upload_id)
        if not upload:
            task = self.task_repository.update_status(
                task_id=task_id,
                status=TaskStatus.ERROR,
                error_code="UPLOAD_NOT_FOUND",
                error_detail="Загрузка не найдена",
            )
            return {"success": False, "error": "Загрузка не найдена"}
        
        try:
            # Извлекаем требования из загрузки
            requirements = self._extract_requirements(upload)
            if not requirements:
                task = self.task_repository.update_status(
                    task_id=task_id,
                    status=TaskStatus.ERROR,
                    error_code="NO_REQUIREMENTS",
                    error_detail="Не удалось извлечь требования из загрузки",
                )
                return {"success": False, "error": "Не удалось извлечь требования"}
            
            # Обновляем прогресс
            task = self.task_repository.update_status(
                task_id=task_id,
                status=TaskStatus.SEARCHING,
                stage="Поиск контрактов в ЕИС",
                progress=20,
            )
            
            # Ищем контракты в ЕИС
            contracts = self._search_contracts(task, requirements)
            
            # Обновляем прогресс
            task = self.task_repository.update_status(
                task_id=task_id,
                status=TaskStatus.SEARCHING,
                stage="Анализ найденных контрактов",
                progress=50,
            )
            
            # Анализируем контракты
            analyzed_contracts = self._analyze_contracts(contracts, requirements)
            
            # Обновляем прогресс
            task = self.task_repository.update_status(
                task_id=task_id,
                status=TaskStatus.SEARCHING,
                stage="Сохранение результатов",
                progress=80,
            )
            
            # Сохраняем контракты в БД
            saved_contracts = self._save_contracts(task_id, analyzed_contracts)
            
            # Обновляем статус задачи
            task = self.task_repository.update_status(
                task_id=task_id,
                status=TaskStatus.DONE,
                stage="Завершено",
                progress=100,
            )
            
            return {
                "success": True,
                "task_id": task_id,
                "contracts_found": len(contracts),
                "contracts_saved": len(saved_contracts),
                "task_status": task.status.value,
            }
            
        except Exception as e:
            # Обрабатываем ошибки
            task = self.task_repository.update_status(
                task_id=task_id,
                status=TaskStatus.ERROR,
                error_code="SEARCH_ERROR",
                error_detail=str(e),
            )
            return {"success": False, "error": str(e), "task_id": task_id}
    
    def _extract_requirements(self, upload) -> Dict[str, Any]:
        """Извлечь требования из загрузки"""
        if not upload.extracted_json:
            return {}
        
        requirements = upload.extracted_json.copy()
        
        # Преобразуем характеристики в формат для Match Engine
        characteristics = requirements.get("characteristics", [])
        if characteristics:
            requirements["characteristics_dict"] = {
                char.get("key", ""): char.get("value", "")
                for char in characteristics
                if char.get("key")
            }
        
        return requirements
    
    def _search_contracts(self, task, requirements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Поиск контрактов в ЕИС"""
        try:
            contracts = self.eis_parser.search_contracts(
                ktru_code=requirements.get("ktru_code"),
                product_name=requirements.get("name"),
                region=task.region or "Северо-Западный ФО",
                period_from=task.period_from,
                period_to=task.period_to,
                law_type="44-ФЗ",
                max_results=50,
            )
            return contracts
        except Exception as e:
            raise Exception(f"Ошибка поиска контрактов: {e}")
    
    def _analyze_contracts(self, contracts: List[Dict[str, Any]], requirements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Анализ найденных контрактов"""
        analyzed_contracts = []
        
        for i, contract in enumerate(contracts):
            try:
                # Получаем детали контракта
                contract_details = self.eis_parser.get_contract_details(contract["url"])
                
                # Объединяем базовую информацию и детали
                analyzed_contract = {**contract, **contract_details}
                
                # Рассчитываем совпадение с требованиями
                if requirements.get("characteristics_dict"):
                    match_result = self._calculate_match(requirements, analyzed_contract)
                    analyzed_contract.update(match_result)
                
                analyzed_contracts.append(analyzed_contract)
                
            except Exception as e:
                print(f"Ошибка анализа контракта {contract.get('reg_number', 'unknown')}: {e}")
                continue
        
        return analyzed_contracts
    
    def _calculate_match(self, requirements: Dict[str, Any], contract: Dict[str, Any]) -> Dict[str, Any]:
        """Рассчитать совпадение с требованиями"""
        expected_characteristics = requirements.get("characteristics_dict", {})
        expected_vendor = requirements.get("vendor")
        
        # Извлекаем найденные характеристики
        found_characteristics = {}
        found_vendor = contract.get("vendor")
        
        # Преобразуем характеристики из контракта
        for char in contract.get("characteristics", []):
            key = char.get("key", "")
            value = char.get("value", "")
            if key and value:
                found_characteristics[key] = value
        
        # Рассчитываем совпадение
        match_percent, match_type, audit_log = self.match_engine.calculate_match(
            expected_characteristics,
            found_characteristics,
            expected_vendor,
            found_vendor,
        )
        
        return {
            "match_percent": match_percent,
            "match_type": match_type.value,
            "vendor_status": self.match_engine.compare_vendor(expected_vendor, found_vendor).value,
            "audit_log": audit_log,
        }
    
    def _save_contracts(self, task_id: str, contracts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Сохранить контракты в БД"""
        # Удаляем старые контракты для этой задачи
        self.contract_repository.delete_by_task_id(task_id)
        
        # Создаем сущности контрактов
        contract_entities = []
        for contract in contracts:
            try:
                entity = self._create_contract_entity(task_id, contract)
                contract_entities.append(entity)
            except Exception as e:
                print(f"Ошибка создания сущности контракта: {e}")
                continue
        
        # Сохраняем контракты
        if contract_entities:
            saved_entities = self.contract_repository.create_batch(contract_entities)
            return [self._entity_to_dict(entity) for entity in saved_entities]
        
        return []
    
    def _create_contract_entity(self, task_id: str, contract_data: Dict[str, Any]):
        """Создать сущность контракта"""
        from app.domain.entities.contract import ContractEntity, MatchType, VendorStatus
        
        # Преобразуем строковые значения в enum
        match_type_str = contract_data.get("match_type", "different")
        vendor_status_str = contract_data.get("vendor_status", "unknown")
        
        try:
            match_type = MatchType(match_type_str)
        except ValueError:
            match_type = MatchType.DIFFERENT
        
        try:
            vendor_status = VendorStatus(vendor_status_str)
        except ValueError:
            vendor_status = VendorStatus.UNKNOWN
        
        return ContractEntity(
            task_id=task_id,
            reg_number=contract_data.get("reg_number", ""),
            eis_url=contract_data.get("url", ""),
            supplier_name=contract_data.get("supplier_name", ""),
            supplier_inn=contract_data.get("supplier_inn", ""),
            sign_date=contract_data.get("sign_date"),
            unit_price=contract_data.get("unit_price", 0.0),
            currency=contract_data.get("currency", "RUB"),
            match_percent=contract_data.get("match_percent", 0.0),
            match_type=match_type,
            vendor_status=vendor_status,
            raw_payload_json=contract_data,
        )
    
    def _entity_to_dict(self, entity) -> Dict[str, Any]:
        """Преобразовать сущность в словарь"""
        return {
            "id": entity.id,
            "reg_number": entity.reg_number,
            "supplier_name": entity.supplier_name,
            "unit_price": entity.unit_price,
            "match_percent": entity.match_percent,
            "match_type": entity.match_type.value,
            "vendor_status": entity.vendor_status.value,
        }
```

### Файл: `app/dependencies/__init__.py`
```python

```

### Файл: `app/dependencies/session.py`
```python
from typing import Optional
from fastapi import Depends, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.database import get_db
from app.domain.entities.session import SessionEntity
from app.infra.config import settings


async def get_current_session(
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> Optional[SessionEntity]:
    """Получить текущую сессию из куки"""
    
    session_token = request.cookies.get(settings.session_cookie_name)
    
    if not session_token:
        return None
    
    stmt = select(SessionEntity).where(SessionEntity.token == session_token)
    result = await db.execute(stmt)
    session = result.scalar_one_or_none()
    
    if session:
        # Обновляем время последнего визита
        session.last_seen_at = datetime.utcnow()
        await db.commit()
        await db.refresh(session)
    
    return session


async def require_session(
    session: Optional[SessionEntity] = Depends(get_current_session),
) -> SessionEntity:
    """Требовать наличие сессии (для защищенных эндпоинтов)"""
    
    if not session:
        raise HTTPException(
            status_code=401,
            detail="Требуется сессия",
        )
    
    return session


async def get_or_create_session(
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> SessionEntity:
    """Получить существующую сессию или создать новую"""
    
    session_token = request.cookies.get(settings.session_cookie_name)
    
    if session_token:
        stmt = select(SessionEntity).where(SessionEntity.token == session_token)
        result = await db.execute(stmt)
        session = result.scalar_one_or_none()
        
        if session:
            # Обновляем время последнего визита
            session.last_seen_at = datetime.utcnow()
            await db.commit()
            await db.refresh(session)
            return session
    
    # Создаем новую сессию
    from uuid import uuid4
    from datetime import datetime
    
    session_token = str(uuid4())
    session = SessionEntity(
        token=session_token,
        user_agent=request.headers.get("user-agent"),
        ip_address=request.client.host if request.client else None,
    )
    
    db.add(session)
    await db.commit()
    await db.refresh(session)
    
    return session
```

### Файл: `app/domain/__init__.py`
```python

```

### Файл: `app/domain/entities/__init__.py`
```python
"""
Импорт всех сущностей для автоматического создания таблиц
"""
from .base import BaseEntity
from .session import SessionEntity
from .upload import UploadEntity
from .task import TaskEntity
from .contract import ContractEntity
from .audit import ContractAuditEntity
from .selection import TaskSelectionEntity
from .calculation import TaskCalculationEntity

__all__ = [
    "BaseEntity",
    "SessionEntity",
    "UploadEntity",
    "TaskEntity",
    "ContractEntity",
    "ContractAuditEntity",
    "TaskSelectionEntity",
    "TaskCalculationEntity",
]
```

### Файл: `app/domain/entities/audit.py`
```python
from sqlalchemy import String, Text, Boolean, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID
from .base import BaseEntity
from .contract import ContractEntity


class ContractAuditEntity(BaseEntity):
    __tablename__ = "contract_audit_rows"
    
    contract_id: Mapped[UUID] = mapped_column(ForeignKey("contracts.id"), nullable=False)
    key: Mapped[str] = mapped_column(String(200), nullable=False)
    expected_value: Mapped[str] = mapped_column(Text, nullable=True)
    found_value: Mapped[str] = mapped_column(Text, nullable=True)
    is_diff: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    diff_reason: Mapped[str] = mapped_column(String(500), nullable=True)
    
    # Связи
    contract: Mapped["ContractEntity"] = relationship("ContractEntity", back_populates="audit_logs")
```

### Файл: `app/domain/entities/base.py`
```python
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from sqlalchemy import DateTime, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class BaseEntity(Base):
    __abstract__ = True
    
    # Используем String для SQLite вместо UUID
    id: Mapped[UUID] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

```

### Файл: `app/domain/entities/calculation.py`
```python
from datetime import datetime
from sqlalchemy import DateTime, String, Float, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID
from .base import BaseEntity
from .task import TaskEntity


class TaskCalculationEntity(BaseEntity):
    __tablename__ = "task_calculations"
    
    task_id: Mapped[UUID] = mapped_column(ForeignKey("tasks.id"), nullable=False)
    method: Mapped[str] = mapped_column(String(100), nullable=False)
    nmc_value: Mapped[float] = mapped_column(Float, nullable=False)
    currency: Mapped[str] = mapped_column(String(10), default="RUB", nullable=False)
    computed_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    details: Mapped[dict] = mapped_column(JSON, nullable=True)
    
    # Связи
    task: Mapped["TaskEntity"] = relationship("TaskEntity")
```

### Файл: `app/domain/entities/contract.py`
```python
from datetime import datetime
from enum import Enum
from sqlalchemy import Enum as SQLEnum, DateTime, String, Float, Integer, Boolean, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID
from .base import BaseEntity
from .task import TaskEntity


class MatchType(str, Enum):
    IDENTICAL = "identical"
    HOMOGENEOUS = "homogeneous"
    DIFFERENT = "different"


class VendorStatus(str, Enum):
    MATCH = "match"
    MISMATCH = "mismatch"
    UNKNOWN = "unknown"


class ContractEntity(BaseEntity):
    __tablename__ = "contracts"
    
    task_id: Mapped[UUID] = mapped_column(ForeignKey("tasks.id"), nullable=False)
    reg_number: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    eis_url: Mapped[str] = mapped_column(String(500), nullable=False)
    supplier_name: Mapped[str] = mapped_column(String(500), nullable=False)
    supplier_inn: Mapped[str] = mapped_column(String(20), nullable=True)
    sign_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    unit_price: Mapped[float] = mapped_column(Float, nullable=False)
    currency: Mapped[str] = mapped_column(String(10), default="RUB", nullable=False)
    
    # Совпадение характеристик
    match_percent: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    match_type: Mapped[MatchType] = mapped_column(SQLEnum(MatchType), default=MatchType.DIFFERENT, nullable=False)
    vendor_status: Mapped[VendorStatus] = mapped_column(SQLEnum(VendorStatus), default=VendorStatus.UNKNOWN, nullable=False)
    
    # Дополнительные данные
    raw_data: Mapped[dict] = mapped_column(JSON, nullable=True)
    is_selected: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # Связи
    task: Mapped["TaskEntity"] = relationship("TaskEntity", back_populates="contracts")
    audit_logs: Mapped[list["ContractAuditEntity"]] = relationship("ContractAuditEntity", back_populates="contract", cascade="all, delete-orphan")
```

### Файл: `app/domain/entities/selection.py`
```python
from datetime import datetime
from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID
from .base import BaseEntity
from .task import TaskEntity
from .contract import ContractEntity


class TaskSelectionEntity(BaseEntity):
    __tablename__ = "task_selection"
    
    task_id: Mapped[UUID] = mapped_column(ForeignKey("tasks.id"), nullable=False)
    contract_id: Mapped[UUID] = mapped_column(ForeignKey("contracts.id"), nullable=False)
    selected_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Связи
    task: Mapped["TaskEntity"] = relationship("TaskEntity", back_populates="selection")
    contract: Mapped["ContractEntity"] = relationship("ContractEntity")
```

### Файл: `app/domain/entities/session.py`
```python
from datetime import datetime
from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column
from uuid import UUID
from .base import BaseEntity


class SessionEntity(BaseEntity):
    __tablename__ = "sessions"
    
    token: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    last_seen_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_agent: Mapped[str] = mapped_column(String(512), nullable=True)
    ip_address: Mapped[str] = mapped_column(String(45), nullable=True)
```

### Файл: `app/domain/entities/task.py`
```python
from datetime import datetime
from enum import Enum
from sqlalchemy import Enum as SQLEnum, DateTime, String, Integer, Float, ForeignKey, JSON, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID
from .base import BaseEntity
from .upload import UploadEntity


class TaskStatus(str, Enum):
    QUEUED = "queued"
    SEARCHING = "searching"
    DOWNLOADING = "downloading"
    ANALYZING = "analyzing"
    DONE = "done"
    ERROR = "error"
    CANCELLED = "cancelled"
    STOPPED = "stopped"


class TaskEntity(BaseEntity):
    __tablename__ = "tasks"
    
    session_id: Mapped[UUID] = mapped_column(ForeignKey("sessions.id"), nullable=False)
    upload_id: Mapped[UUID] = mapped_column(ForeignKey("uploads.id"), nullable=False)
    status: Mapped[TaskStatus] = mapped_column(SQLEnum(TaskStatus), default=TaskStatus.QUEUED, nullable=False)
    stage: Mapped[str] = mapped_column(String(100), nullable=True)
    progress: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    message: Mapped[str] = mapped_column(String(500), nullable=True)
    
    # Параметры поиска
    region: Mapped[str] = mapped_column(String(100), nullable=False)
    period_from: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    period_to: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    law_type: Mapped[str] = mapped_column(String(50), default="44-ФЗ", nullable=False)
    
    # Информация о товаре (для отображения в истории)
    product_name: Mapped[str] = mapped_column(String(200), nullable=True)
    ktru_code: Mapped[str] = mapped_column(String(100), nullable=True)

    # Результаты
    started_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    finished_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    error_code: Mapped[str] = mapped_column(String(100), nullable=True)
    error_detail: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Сводка результатов
    total_found: Mapped[int] = mapped_column(Integer, default=0)
    total_analyzed: Mapped[int] = mapped_column(Integer, default=0)
    nmck_value: Mapped[float] = mapped_column(Float, nullable=True)
    nmck_currency: Mapped[str] = mapped_column(String(10), default="RUB", nullable=True)
    
    # Связи
    session: Mapped["SessionEntity"] = relationship("SessionEntity")
    upload: Mapped["UploadEntity"] = relationship("UploadEntity", back_populates="tasks")
    contracts: Mapped[list["ContractEntity"]] = relationship("ContractEntity", back_populates="task", cascade="all, delete-orphan")
    selection: Mapped[list["TaskSelectionEntity"]] = relationship("TaskSelectionEntity", back_populates="task", cascade="all, delete-orphan")
```

### Файл: `app/domain/entities/upload.py`
```python
from sqlalchemy import JSON, String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID
from .base import BaseEntity
from .session import SessionEntity


class UploadEntity(BaseEntity):
    __tablename__ = "uploads"
    
    session_id: Mapped[UUID] = mapped_column(ForeignKey("sessions.id"), nullable=False)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    mime_type: Mapped[str] = mapped_column(String(100), nullable=False)
    storage_url: Mapped[str] = mapped_column(String(500), nullable=False)
    extracted_data: Mapped[dict] = mapped_column(JSON, nullable=True)
    warnings: Mapped[list] = mapped_column(JSON, nullable=True, default=list)
    
    # Связи
    session: Mapped["SessionEntity"] = relationship("SessionEntity")
    tasks: Mapped[list["TaskEntity"]] = relationship("TaskEntity", back_populates="upload", cascade="all, delete-orphan")
```

### Файл: `app/domain/repositories/__init__.py`
```python

```

### Файл: `app/domain/repositories/contract_repository.py`
```python
"""
Интерфейс репозитория контрактов
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.contract import ContractEntity


class ContractRepository(ABC):
    """Абстрактный репозиторий контрактов"""
    
    @abstractmethod
    def get_by_id(self, contract_id: str) -> Optional[ContractEntity]:
        """Получить контракт по ID"""
        pass
    
    @abstractmethod
    def get_by_task_id(self, task_id: str) -> List[ContractEntity]:
        """Получить контракты по task_id"""
        pass
    
    @abstractmethod
    def create(self, contract: ContractEntity) -> ContractEntity:
        """Создать контракт"""
        pass
    
    @abstractmethod
    def create_batch(self, contracts: List[ContractEntity]) -> List[ContractEntity]:
        """Создать несколько контрактов"""
        pass
    
    @abstractmethod
    def update(self, contract: ContractEntity) -> ContractEntity:
        """Обновить контракт"""
        pass
    
    @abstractmethod
    def delete_by_task_id(self, task_id: str) -> int:
        """Удалить контракты по task_id"""
        pass
```

### Файл: `app/domain/repositories/task_repository.py`
```python
"""
Интерфейс репозитория задач
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime
from app.domain.entities.task import TaskEntity, TaskStatus


class TaskRepository(ABC):
    """Абстрактный репозиторий задач"""
    
    @abstractmethod
    def get_by_id(self, task_id: str) -> Optional[TaskEntity]:
        """Получить задачу по ID"""
        pass
    
    @abstractmethod
    def get_by_session_id(self, session_id: str, limit: int = 50) -> List[TaskEntity]:
        """Получить задачи по session_id"""
        pass
    
    @abstractmethod
    def create(self, task: TaskEntity) -> TaskEntity:
        """Создать задачу"""
        pass
    
    @abstractmethod
    def update(self, task: TaskEntity) -> TaskEntity:
        """Обновить задачу"""
        pass
    
    @abstractmethod
    def update_status(self, task_id: str, status: TaskStatus, stage: Optional[str] = None, 
                     progress: Optional[int] = None, error_code: Optional[str] = None, 
                     error_detail: Optional[str] = None) -> Optional[TaskEntity]:
        """Обновить статус задачи"""
        pass
    
    @abstractmethod
    def delete(self, task_id: str) -> bool:
        """Удалить задачу"""
        pass
```

### Файл: `app/domain/repositories/upload_repository.py`
```python
"""
Интерфейс репозитория загрузок
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.upload import UploadEntity


class UploadRepository(ABC):
    """Абстрактный репозиторий загрузок"""
    
    @abstractmethod
    def get_by_id(self, upload_id: str) -> Optional[UploadEntity]:
        """Получить загрузку по ID"""
        pass
    
    @abstractmethod
    def get_by_session_id(self, session_id: str, limit: int = 20) -> List[UploadEntity]:
        """Получить загрузки по session_id"""
        pass
    
    @abstractmethod
    def create(self, upload: UploadEntity) -> UploadEntity:
        """Создать загрузку"""
        pass
    
    @abstractmethod
    def update(self, upload: UploadEntity) -> UploadEntity:
        """Обновить загрузку"""
        pass
    
    @abstractmethod
    def delete(self, upload_id: str) -> bool:
        """Удалить загрузку"""
        pass
```

### Файл: `app/domain/rules/__init__.py`
```python

```

### Файл: `app/infra/__init__.py`
```python

```

### Файл: `app/infra/celery/__init__.py`
```python

```

### Файл: `app/infra/celery/celery_app.py`
```python
from celery import Celery
from app.infra.config import settings

# Создаем экземпляр Celery
celery_app = Celery(
    "nmck_system",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=[
        "app.infra.celery.tasks",
    ]
)

# Конфигурация Celery
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Europe/Moscow",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 минут
    task_soft_time_limit=25 * 60,  # 25 минут
    worker_max_tasks_per_child=100,
    worker_prefetch_multiplier=1,
    task_acks_late=True,
    worker_concurrency=4,
    broker_connection_retry_on_startup=True,
)

# Автоматическое обнаружение задач
celery_app.autodiscover_tasks(["app.infra.celery"])


@celery_app.task(bind=True)
def debug_task(self):
    """Тестовая задача для отладки"""
    print(f"Request: {self.request!r}")
```

### Файл: `app/infra/celery/tasks.py`
```python
import asyncio
from datetime import datetime
from uuid import UUID
from celery import shared_task
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select

from app.infra.config import settings
from app.domain.entities.task import TaskEntity, TaskStatus
from app.adapters.eis.parser import EISParser
from app.adapters.parsers.match_engine import MatchEngine

# Создаем асинхронный движок для Celery задач
engine = create_async_engine(settings.DATABASE_URL)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Инициализация парсеров
eis_parser = EISParser()
match_engine = MatchEngine()


@shared_task(bind=True, name="run_search_task")
def run_search_task(self, task_id: str):
    """Задача поиска контрактов в ЕИС"""
    
    # Запускаем асинхронную задачу
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(_run_search_task_async(task_id))


async def _run_search_task_async(task_id: str):
    """Асинхронная реализация задачи поиска"""
    
    async with AsyncSessionLocal() as db:
        try:
            # Получаем задачу
            stmt = select(TaskEntity).where(TaskEntity.id == UUID(task_id))
            result = await db.execute(stmt)
            task = result.scalar_one_or_none()
            
            if not task:
                raise ValueError(f"Задача {task_id} не найдена")
            
            # Обновляем статус
            task.status = TaskStatus.SEARCHING
            task.started_at = datetime.utcnow()
            task.stage = "Поиск кандидатов"
            task.progress = 10
            await db.commit()
            
            # Получаем данные из загрузки
            from app.domain.entities.upload import UploadEntity
            stmt = select(UploadEntity).where(UploadEntity.id == task.upload_id)
            result = await db.execute(stmt)
            upload = result.scalar_one_or_none()
            
            if not upload or not upload.extracted_data:
                raise ValueError("Данные загрузки не найдены")
            
            # Извлекаем требования
            requirements = upload.extracted_data
            
            # Этап 1: Поиск кандидатов в ЕИС
            task.stage = "Поиск контрактов"
            task.progress = 20
            await db.commit()
            
            candidates = await eis_parser.search_contracts(
                ktru_code=requirements.get("ktru_code"),
                product_name=requirements.get("name"),
                region=task.region,
                period_from=task.period_from,
                period_to=task.period_to,
                law_type=task.law_type,
            )
            
            task.total_found = len(candidates)
            task.stage = "Анализ контрактов"
            task.progress = 40
            await db.commit()
            
            # Этап 2: Анализ контрактов
            analyzed_contracts = []
            for i, candidate in enumerate(candidates):
                # Обновляем прогресс
                progress = 40 + int((i / len(candidates)) * 40)
                task.progress = progress
                task.message = f"Анализ контракта {i+1} из {len(candidates)}"
                await db.commit()
                
                try:
                    # Получаем детальную информацию о контракте
                    contract_data = await eis_parser.get_contract_details(candidate["url"])
                    
                    # Сравниваем характеристики
                    match_result = await match_engine.compare_characteristics(
                        requirements=requirements,
                        contract_data=contract_data,
                    )
                    
                    # Сохраняем контракт в БД
                    from app.domain.entities.contract import ContractEntity, MatchType, VendorStatus
                    
                    contract = ContractEntity(
                        task_id=task.id,
                        reg_number=contract_data.get("reg_number", ""),
                        eis_url=candidate["url"],
                        supplier_name=contract_data.get("supplier_name", ""),
                        supplier_inn=contract_data.get("supplier_inn"),
                        sign_date=contract_data.get("sign_date", datetime.utcnow()),
                        unit_price=contract_data.get("unit_price", 0),
                        currency=contract_data.get("currency", "RUB"),
                        match_percent=match_result["match_percent"],
                        match_type=MatchType.IDENTICAL if match_result["match_percent"] == 100 else MatchType.HOMOGENEOUS,
                        vendor_status=VendorStatus.MATCH if match_result["vendor_match"] else VendorStatus.MISMATCH,
                        raw_data=contract_data,
                    )
                    
                    db.add(contract)
                    await db.flush()  # Получаем ID контракта
                    
                    # Сохраняем лог сверки
                    from app.domain.entities.audit import ContractAuditEntity
                    
                    for audit_item in match_result.get("audit_log", []):
                        audit = ContractAuditEntity(
                            contract_id=contract.id,
                            key=audit_item["key"],
                            expected_value=audit_item.get("expected_value"),
                            found_value=audit_item.get("found_value"),
                            is_diff=audit_item.get("is_diff", False),
                            diff_reason=audit_item.get("diff_reason"),
                        )
                        db.add(audit)
                    
                    analyzed_contracts.append(contract)
                    task.total_analyzed += 1
                    
                except Exception as e:
                    # Пропускаем контракт с ошибкой
                    print(f"Ошибка при анализе контракта {candidate['url']}: {e}")
                    continue
            
            # Этап 3: Расчет НМЦК
            task.stage = "Расчет НМЦК"
            task.progress = 90
            await db.commit()
            
            if analyzed_contracts:
                # Автоматический выбор 3 лучших контрактов
                selected_contracts = await _auto_select_contracts(analyzed_contracts)
                
                # Расчет НМЦК
                nmck_value = await _calculate_nmck(selected_contracts)
                
                # Сохраняем выбор
                from app.domain.entities.selection import TaskSelectionEntity
                from datetime import datetime
                
                for contract in selected_contracts:
                    selection = TaskSelectionEntity(
                        task_id=task.id,
                        contract_id=contract.id,
                        selected_at=datetime.utcnow(),
                    )
                    db.add(selection)
                
                task.nmck_value = nmck_value
            
            # Завершаем задачу
            task.status = TaskStatus.DONE
            task.stage = "Завершено"
            task.progress = 100
            task.finished_at = datetime.utcnow()
            task.message = f"Найдено {len(analyzed_contracts)} подходящих контрактов"
            
            await db.commit()
            
            return {
                "task_id": task_id,
                "status": "completed",
                "contracts_found": len(analyzed_contracts),
                "nmck_value": task.nmck_value,
            }
            
        except Exception as e:
            # Обработка ошибок
            print(f"Ошибка в задаче {task_id}: {e}")
            
            # Обновляем статус задачи
            stmt = select(TaskEntity).where(TaskEntity.id == UUID(task_id))
            result = await db.execute(stmt)
            task = result.scalar_one_or_none()
            
            if task:
                task.status = TaskStatus.ERROR
                task.error_code = "SEARCH_ERROR"
                task.error_detail = str(e)
                task.finished_at = datetime.utcnow()
                await db.commit()
            
            raise


async def _auto_select_contracts(contracts):
    """Автоматический выбор 3 лучших контрактов"""
    
    # Сортируем по проценту совпадения (по убыванию) и цене (по возрастанию)
    sorted_contracts = sorted(
        contracts,
        key=lambda c: (-c.match_percent, c.unit_price)
    )
    
    # Выбираем контракты, следя за правилом поставщиков
    selected = []
    supplier_count = {}
    
    for contract in sorted_contracts:
        if len(selected) >= 3:
            break
        
        supplier = contract.supplier_inn or contract.supplier_name
        current_count = supplier_count.get(supplier, 0)
        
        # Проверяем правило: не более 2 контрактов от одного поставщика
        if current_count < 2:
            selected.append(contract)
            supplier_count[supplier] = current_count + 1
    
    return selected


async def _calculate_nmck(contracts):
    """Расчет НМЦК как среднее арифметическое цен выбранных контрактов"""
    
    if not contracts:
        return 0
    
    total_price = sum(contract.unit_price for contract in contracts)
    return total_price / len(contracts)
```

### Файл: `app/infra/config.py`
```python
"""
Конфигурация приложения
"""
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # База данных
    DATABASE_URL: str = "sqlite:///./nmck.db"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Приложение
    DEBUG: bool = True
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    API_V1_STR: str = "/api"
    
    # Парсер ЕИС
    EIS_BASE_URL: str = "https://zakupki.gov.ru"
    EIS_SEARCH_DELAY: int = 1
    EIS_MAX_RESULTS: int = 50
    
    # Файловое хранилище
    UPLOAD_DIR: str = "uploads"
    MAX_UPLOAD_SIZE: int = 10485760  # 10MB
    
    # WebSocket
    WEBSOCKET_PING_INTERVAL: int = 30
    WEBSOCKET_PING_TIMEOUT: int = 10
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

```

### Файл: `app/infra/database.py`
```python
"""
Конфигурация базы данных
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from app.infra.config import settings

# Создаем движок базы данных
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

# Создаем фабрику сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для моделей
Base = declarative_base()

# Импортируем все сущности для регистрации в метаданных
from app.domain.entities import (
    SessionEntity,
    UploadEntity,
    TaskEntity,
    ContractEntity,
    ContractAuditEntity,
    TaskSelectionEntity,
    TaskCalculationEntity,
)

def get_db() -> Session:
    """
    Зависимость для получения сессии базы данных.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

```

### Файл: `app/infra/logging.py`
```python
import logging
import sys
from typing import Any, Dict
import structlog
from app.infra.config import settings


def setup_logging():
    """Настройка структурированного логирования"""
    
    # Настройка structlog
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer(),
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    
    # Настройка стандартного logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, settings.log_level.upper()),
    )
    
    # Устанавливаем уровень логирования для внешних библиотек
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy").setLevel(logging.WARNING)
    logging.getLogger("celery").setLevel(logging.WARNING)
    
    # Создаем логгер
    logger = structlog.get_logger()
    logger.info("Logging configured", level=settings.log_level)
    
    return logger


def get_logger(name: str = None) -> structlog.BoundLogger:
    """Получить логгер"""
    return structlog.get_logger(name)


def log_task_progress(task_id: str, stage: str, progress: int, message: str = None, **kwargs):
    """Логировать прогресс задачи"""
    
    logger = get_logger("task")
    logger.info(
        "task.progress",
        task_id=task_id,
        stage=stage,
        progress=progress,
        message=message,
        **kwargs,
    )


def log_task_completed(task_id: str, result: Dict[str, Any]):
    """Логировать завершение задачи"""
    
    logger = get_logger("task")
    logger.info(
        "task.completed",
        task_id=task_id,
        result=result,
    )


def log_task_error(task_id: str, error_code: str, error_detail: str, **kwargs):
    """Логировать ошибку задачи"""
    
    logger = get_logger("task")
    logger.error(
        "task.error",
        task_id=task_id,
        error_code=error_code,
        error_detail=error_detail,
        **kwargs,
    )


def log_eis_request(url: str, method: str, status_code: int = None, duration: float = None, **kwargs):
    """Логировать запрос к ЕИС"""
    
    logger = get_logger("eis")
    logger.info(
        "eis.request",
        url=url,
        method=method,
        status_code=status_code,
        duration=duration,
        **kwargs,
    )


def log_eis_error(url: str, method: str, error: str, **kwargs):
    """Логировать ошибку запроса к ЕИС"""
    
    logger = get_logger("eis")
    logger.error(
        "eis.error",
        url=url,
        method=method,
        error=error,
        **kwargs,
    )
```

### Файл: `app/infra/logging/__init__.py`
```python

```

### Файл: `app/infra/repositories/sqlalchemy_contract_repository.py`
```python
"""
SQLAlchemy реализация репозитория контрактов
"""
from typing import List, Optional
from sqlalchemy.orm import Session

from app.domain.entities.contract import ContractEntity, MatchType, VendorStatus
from app.domain.repositories.contract_repository import ContractRepository
from app.infra.database.models import Contract as ContractModel


class SQLAlchemyContractRepository(ContractRepository):
    """SQLAlchemy реализация репозитория контрактов"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def get_by_id(self, contract_id: str) -> Optional[ContractEntity]:
        """Получить контракт по ID"""
        model = self.session.query(ContractModel).filter(ContractModel.id == contract_id).first()
        if model:
            return self._to_entity(model)
        return None
    
    def get_by_task_id(self, task_id: str) -> List[ContractEntity]:
        """Получить контракты по task_id"""
        models = (
            self.session.query(ContractModel)
            .filter(ContractModel.task_id == task_id)
            .order_by(ContractModel.match_percent.desc())
            .all()
        )
        return [self._to_entity(model) for model in models]
    
    def create(self, contract: ContractEntity) -> ContractEntity:
        """Создать контракт"""
        model = ContractModel(
            id=contract.id,
            task_id=contract.task_id,
            reg_number=contract.reg_number,
            eis_url=contract.eis_url,
            supplier_name=contract.supplier_name,
            supplier_inn=contract.supplier_inn,
            sign_date=contract.sign_date,
            unit_price=contract.unit_price,
            currency=contract.currency,
            match_percent=contract.match_percent,
            match_type=contract.match_type.value,
            vendor_status=contract.vendor_status.value,
            raw_payload_json=contract.raw_payload_json,
        )
        self.session.add(model)
        self.session.flush()
        return self._to_entity(model)
    
    def create_batch(self, contracts: List[ContractEntity]) -> List[ContractEntity]:
        """Создать несколько контрактов"""
        models = []
        for contract in contracts:
            model = ContractModel(
                id=contract.id,
                task_id=contract.task_id,
                reg_number=contract.reg_number,
                eis_url=contract.eis_url,
                supplier_name=contract.supplier_name,
                supplier_inn=contract.supplier_inn,
                sign_date=contract.sign_date,
                unit_price=contract.unit_price,
                currency=contract.currency,
                match_percent=contract.match_percent,
                match_type=contract.match_type.value,
                vendor_status=contract.vendor_status.value,
                raw_payload_json=contract.raw_payload_json,
            )
            models.append(model)
        
        self.session.bulk_save_objects(models)
        self.session.flush()
        
        # Возвращаем сущности с ID
        return [self._to_entity(model) for model in models]
    
    def update(self, contract: ContractEntity) -> ContractEntity:
        """Обновить контракт"""
        model = self.session.query(ContractModel).filter(ContractModel.id == contract.id).first()
        if not model:
            raise ValueError(f"Контракт с ID {contract.id} не найдена")
        
        model.reg_number = contract.reg_number
        model.eis_url = contract.eis_url
        model.supplier_name = contract.supplier_name
        model.supplier_inn = contract.supplier_inn
        model.sign_date = contract.sign_date
        model.unit_price = contract.unit_price
        model.currency = contract.currency
        model.match_percent = contract.match_percent
        model.match_type = contract.match_type.value
        model.vendor_status = contract.vendor_status.value
        model.raw_payload_json = contract.raw_payload_json
        
        self.session.flush()
        return self._to_entity(model)
    
    def delete_by_task_id(self, task_id: str) -> int:
        """Удалить контракты по task_id"""
        result = self.session.query(ContractModel).filter(ContractModel.task_id == task_id).delete()
        return result
    
    def _to_entity(self, model: ContractModel) -> ContractEntity:
        """Преобразовать модель в сущность"""
        return ContractEntity(
            id=model.id,
            task_id=model.task_id,
            reg_number=model.reg_number,
            eis_url=model.eis_url,
            supplier_name=model.supplier_name,
            supplier_inn=model.supplier_inn,
            sign_date=model.sign_date,
            unit_price=model.unit_price,
            currency=model.currency,
            match_percent=model.match_percent,
            match_type=MatchType(model.match_type),
            vendor_status=VendorStatus(model.vendor_status),
            raw_payload_json=model.raw_payload_json,
        )
```

### Файл: `app/infra/repositories/sqlalchemy_task_repository.py`
```python
"""
SQLAlchemy реализация репозитория задач
"""
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session

from app.domain.entities.task import TaskEntity, TaskStatus
from app.domain.repositories.task_repository import TaskRepository
from app.infra.database.models import Task as TaskModel


class SQLAlchemyTaskRepository(TaskRepository):
    """SQLAlchemy реализация репозитория задач"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def get_by_id(self, task_id: str) -> Optional[TaskEntity]:
        """Получить задачу по ID"""
        model = self.session.query(TaskModel).filter(TaskModel.id == task_id).first()
        if model:
            return self._to_entity(model)
        return None
    
    def get_by_session_id(self, session_id: str, limit: int = 50) -> List[TaskEntity]:
        """Получить задачи по session_id"""
        models = (
            self.session.query(TaskModel)
            .filter(TaskModel.session_id == session_id)
            .order_by(TaskModel.created_at.desc())
            .limit(limit)
            .all()
        )
        return [self._to_entity(model) for model in models]
    
    def create(self, task: TaskEntity) -> TaskEntity:
        """Создать задачу"""
        model = TaskModel(
            id=task.id,
            session_id=task.session_id,
            upload_id=task.upload_id,
            status=task.status.value,
            stage=task.stage,
            progress=task.progress,
            region=task.region,
            period_from=task.period_from,
            period_to=task.period_to,
            created_at=task.created_at,
            started_at=task.started_at,
            finished_at=task.finished_at,
            error_code=task.error_code,
            error_detail=task.error_detail,
        )
        self.session.add(model)
        self.session.flush()
        return self._to_entity(model)
    
    def update(self, task: TaskEntity) -> TaskEntity:
        """Обновить задачу"""
        model = self.session.query(TaskModel).filter(TaskModel.id == task.id).first()
        if not model:
            raise ValueError(f"Задача с ID {task.id} не найдена")
        
        model.status = task.status.value
        model.stage = task.stage
        model.progress = task.progress
        model.started_at = task.started_at
        model.finished_at = task.finished_at
        model.error_code = task.error_code
        model.error_detail = task.error_detail
        
        self.session.flush()
        return self._to_entity(model)
    
    def update_status(self, task_id: str, status: TaskStatus, stage: Optional[str] = None, 
                     progress: Optional[int] = None, error_code: Optional[str] = None, 
                     error_detail: Optional[str] = None) -> Optional[TaskEntity]:
        """Обновить статус задачи"""
        model = self.session.query(TaskModel).filter(TaskModel.id == task_id).first()
        if not model:
            return None
        
        model.status = status.value
        
        if stage is not None:
            model.stage = stage
        
        if progress is not None:
            model.progress = progress
        
        if error_code is not None:
            model.error_code = error_code
        
        if error_detail is not None:
            model.error_detail = error_detail
        
        # Обновляем временные метки
        if status == TaskStatus.SEARCHING and model.started_at is None:
            model.started_at = datetime.utcnow()
        elif status in [TaskStatus.DONE, TaskStatus.ERROR] and model.finished_at is None:
            model.finished_at = datetime.utcnow()
        
        self.session.flush()
        return self._to_entity(model)
    
    def delete(self, task_id: str) -> bool:
        """Удалить задачу"""
        model = self.session.query(TaskModel).filter(TaskModel.id == task_id).first()
        if not model:
            return False
        
        self.session.delete(model)
        return True
    
    def _to_entity(self, model: TaskModel) -> TaskEntity:
        """Преобразовать модель в сущность"""
        return TaskEntity(
            id=model.id,
            session_id=model.session_id,
            upload_id=model.upload_id,
            status=TaskStatus(model.status),
            stage=model.stage,
            progress=model.progress,
            region=model.region,
            period_from=model.period_from,
            period_to=model.period_to,
            created_at=model.created_at,
            started_at=model.started_at,
            finished_at=model.finished_at,
            error_code=model.error_code,
            error_detail=model.error_detail,
        )
```

### Файл: `app/infra/repositories/sqlalchemy_upload_repository.py`
```python
"""
SQLAlchemy реализация репозитория загрузок
"""
from typing import List, Optional
from sqlalchemy.orm import Session

from app.domain.entities.upload import UploadEntity
from app.domain.repositories.upload_repository import UploadRepository
from app.infra.database.models import Upload as UploadModel


class SQLAlchemyUploadRepository(UploadRepository):
    """SQLAlchemy реализация репозитория загрузок"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def get_by_id(self, upload_id: str) -> Optional[UploadEntity]:
        """Получить загрузку по ID"""
        model = self.session.query(UploadModel).filter(UploadModel.id == upload_id).first()
        if model:
            return self._to_entity(model)
        return None
    
    def get_by_session_id(self, session_id: str, limit: int = 20) -> List[UploadEntity]:
        """Получить загрузки по session_id"""
        models = (
            self.session.query(UploadModel)
            .filter(UploadModel.session_id == session_id)
            .order_by(UploadModel.created_at.desc())
            .limit(limit)
            .all()
        )
        return [self._to_entity(model) for model in models]
    
    def create(self, upload: UploadEntity) -> UploadEntity:
        """Создать загрузку"""
        model = UploadModel(
            id=upload.id,
            session_id=upload.session_id,
            filename=upload.filename,
            mime=upload.mime,
            storage_url=upload.storage_url,
            extracted_json=upload.extracted_json,
            created_at=upload.created_at,
        )
        self.session.add(model)
        self.session.flush()
        return self._to_entity(model)
    
    def update(self, upload: UploadEntity) -> UploadEntity:
        """Обновить загрузку"""
        model = self.session.query(UploadModel).filter(UploadModel.id == upload.id).first()
        if not model:
            raise ValueError(f"Загрузка с ID {upload.id} не найдена")
        
        model.filename = upload.filename
        model.mime = upload.mime
        model.storage_url = upload.storage_url
        model.extracted_json = upload.extracted_json
        
        self.session.flush()
        return self._to_entity(model)
    
    def delete(self, upload_id: str) -> bool:
        """Удалить загрузку"""
        model = self.session.query(UploadModel).filter(UploadModel.id == upload_id).first()
        if not model:
            return False
        
        self.session.delete(model)
        return True
    
    def _to_entity(self, model: UploadModel) -> UploadEntity:
        """Преобразовать модель в сущность"""
        return UploadEntity(
            id=model.id,
            session_id=model.session_id,
            filename=model.filename,
            mime=model.mime,
            storage_url=model.storage_url,
            extracted_json=model.extracted_json,
            created_at=model.created_at,
        )
```

### Файл: `app/main.py`
```python
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="NMCK System", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Статические файлы
static_dir = "static"
if os.path.exists(static_dir):
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
    print(f"✅ Статические файлы из: {static_dir}")
else:
    print(f"❌ Директория {static_dir} не найдена")

# Health check
@app.get("/health")
async def health():
    return {"status": "healthy", "service": "nmck-system", "version": "1.0.0"}

# Простой API для тестирования
@app.get("/api/test")
async def test():
    return {"message": "API работает", "system": "NMCK Search"}

@app.get("/api/session")
async def create_session():
    import uuid
    return {"id": str(uuid.uuid4()), "created_at": "2026-01-20T14:00:00"}

@app.get("/api/tasks")
async def list_tasks():
    return []

@app.post("/api/tasks/direct")
async def create_task():
    import uuid
    return {"id": str(uuid.uuid4()), "status": "PENDING", "message": "Task created"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

```

### Файл: `app/models/__init__.py`
```python

```

### Файл: `app/models/database.py`
```python
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.infra.config import settings

# Создание асинхронного движка БД
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    pool_size=20,
    max_overflow=10,
)

# Создание фабрики сессий
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Базовый класс для моделей
Base = declarative_base()


async def get_db() -> AsyncSession:
    """Зависимость для получения сессии БД"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
```

### Файл: `app/schemas/__init__.py`
```python

```

### Файл: `app/schemas/base.py`
```python
"""
Базовые схемы Pydantic
"""
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, Any
import enum

class BaseSchema(BaseModel):
    """Базовая схема с конфигурацией"""
    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True
    )

class TimestampMixin(BaseSchema):
    """Миксин для временных меток"""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class PaginationParams(BaseSchema):
    """Параметры пагинации"""
    page: int = 1
    page_size: int = 20
    sort_by: Optional[str] = None
    sort_order: str = "desc"

class PaginatedResponse(BaseSchema):
    """Ответ с пагинацией"""
    items: list[Any]
    total: int
    page: int
    page_size: int
    total_pages: int

```

### Файл: `app/schemas/contract.py`
```python
"""
Схемы для контрактов
"""
from datetime import datetime
from typing import Optional, List
from enum import Enum

from app.schemas.base import BaseSchema

class MatchType(str, Enum):
    IDENTICAL = "identical"
    HOMOGENEOUS = "homogeneous"
    DIFFERENT = "different"

class VendorStatus(str, Enum):
    MATCH = "match"
    MISMATCH = "mismatch"
    UNKNOWN = "unknown"

class ContractResponse(BaseSchema):
    """Ответ с информацией о контракте"""
    id: str
    task_id: str
    reg_number: str
    eis_url: str
    supplier_name: Optional[str] = None
    supplier_inn: Optional[str] = None
    sign_date: Optional[datetime] = None
    unit_price: float
    currency: str = "RUB"
    match_percent: int
    match_type: MatchType
    vendor_status: VendorStatus
    selected: bool = False

class AuditLogResponse(BaseSchema):
    """Лог сверки характеристик"""
    key: str
    expected_value: Optional[str] = None
    found_value: Optional[str] = None
    is_diff: bool = False
    diff_reason: Optional[str] = None

```

### Файл: `app/schemas/selection.py`
```python
"""
Схемы для выбора контрактов
"""
from typing import List, Dict, Optional

from app.schemas.base import BaseSchema

class SelectionUpdate(BaseSchema):
    """Обновление выбора контрактов"""
    contract_ids: List[str]

class SelectionResponse(BaseSchema):
    """Ответ с информацией о выборе"""
    task_id: str
    selected_contracts: List[str]
    nmck_value: Optional[float] = None
    calculation_method: Optional[str] = None
    supplier_counts: Dict[str, int] = {}

```

### Файл: `app/schemas/session.py`
```python
"""
Схемы для сессий
"""
from datetime import datetime
from typing import Optional
from uuid import UUID

from app.schemas.base import BaseSchema, TimestampMixin

class SessionCreate(BaseSchema):
    """Создание сессии"""
    pass

class SessionResponse(TimestampMixin):
    """Ответ с информацией о сессии"""
    id: str
    created_at: datetime
    last_seen_at: datetime
    token: str  # Токен для совместимости с фронтендом

```

### Файл: `app/schemas/task.py`
```python
"""
Схемы для задач
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.base import BaseSchema, TimestampMixin

# Перечисления для статусов
class TaskStatus(str, Enum):
    QUEUED = "queued"
    SEARCHING = "searching"
    DOWNLOADING = "downloading"
    ANALYZING = "analyzing"
    DONE = "done"
    ERROR = "error"
    CANCELLED = "cancelled"
    STOPPED = "stopped"

# Стадии задачи - просто строка, так как стадии могут быть разными
# TaskStage = str

# Схемы запросов
class TaskCreate(BaseSchema):
    """Создание задачи"""
    upload_id: UUID
    region: str = "Северо-Западный ФО"
    period_years: int = Field(default=3, ge=1, le=10)

class TaskCreateDirect(BaseSchema):
    """Создание задачи напрямую (без файла)"""
    ktru_code: Optional[str] = None
    product_name: str
    vendor: Optional[str] = None
    characteristics: List[Dict[str, Any]] = []
    region: str = "Северо-Западный ФО"
    period_years: int = Field(default=3, ge=1, le=10)

class TaskFilter(BaseSchema):
    """Фильтр для задач"""
    status: Optional[TaskStatus] = None
    region: Optional[str] = None
    limit: int = Field(default=50, ge=1, le=100)

class TaskUpdate(BaseSchema):
    """Обновление задачи"""
    status: Optional[TaskStatus] = None
    stage: Optional[str] = None
    progress: Optional[int] = Field(default=None, ge=0, le=100)
    error_code: Optional[str] = None
    error_detail: Optional[str] = None

# Схемы ответов
class TaskResponse(TimestampMixin):
    """Ответ с информацией о задаче"""
    id: str
    session_id: str
    upload_id: str
    status: TaskStatus
    stage: str
    progress: int
    region: str
    period_from: Optional[datetime] = None
    period_to: Optional[datetime] = None
    created_at: datetime
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    error_code: Optional[str] = None
    error_detail: Optional[str] = None

class TaskListResponse(BaseSchema):
    """Список задач для истории"""
    id: str
    created_at: datetime
    status: TaskStatus
    stage: str
    progress: int
    region: str
    summary: Optional[str] = None
    search_time: Optional[int] = None  # Время поиска в секундах
    product_name: Optional[str] = None  # Наименование товара
    ktru_code: Optional[str] = None    # Код КТРУ

class TaskResultResponse(BaseSchema):
    """Результаты задачи"""
    task_id: str
    summary: Dict[str, Any]
    contracts: List[Dict[str, Any]]
    recommended_nmck: Optional[float] = None

class TaskProgressEvent(BaseSchema):
    """Событие прогресса задачи"""
    task_id: str
    stage: str
    progress: int
    message: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class TaskStatsResponse(BaseSchema):
    """Статистика по задачам"""
    active_tasks: int = 0
    total_found: int = 0
    total_tasks: int = 0
    avg_search_time: Optional[float] = None
    success_rate: Optional[float] = None
    queued_tasks: int = 0
    searching_tasks: int = 0
    done_tasks: int = 0

```

### Файл: `app/schemas/upload.py`
```python
"""
Схемы для загрузок файлов
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID

from app.schemas.base import BaseSchema, TimestampMixin

class UploadCreate(BaseSchema):
    """Создание загрузки"""
    filename: str
    mime_type: Optional[str] = None

class UploadResponse(TimestampMixin):
    """Ответ с информацией о загрузке"""
    id: UUID
    session_id: UUID
    filename: str
    mime_type: Optional[str] = None
    storage_url: str
    extracted_json: Optional[Dict[str, Any]] = None
    created_at: datetime

class CharacteristicSchema(BaseSchema):
    """Схема характеристики"""
    key: str
    value: str
    unit: Optional[str] = None
    operator: str = "="
    source: Optional[str] = None

class UploadDetectionResponse(BaseSchema):
    """Результат распознавания файла"""
    upload_id: UUID
    detected: Dict[str, Any]
    warnings: List[str] = []

```

### Файл: `app/services/__init__.py`
```python

```

### Файл: `app/use_cases/__init__.py`
```python

```

### Файл: `app/workers/celery_app.py`
```python
"""
Celery приложение для фоновых задач
"""
import os
from celery import Celery
from app.infra.database import SessionLocal

# Настройки Celery
celery_app = Celery(
    "nmck_worker",
    broker=os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0"),
    include=["app.workers.search_worker"]
)

# Конфигурация
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Europe/Moscow",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 минут
    task_soft_time_limit=25 * 60,  # 25 минут
    worker_max_tasks_per_child=100,
    worker_prefetch_multiplier=1,
)
```

### Файл: `app/workers/celery_worker.py`
```python
"""
Celery воркер для системы НМЦК
"""
import os
import sys

# Добавляем путь к проекту
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.workers.search_worker import celery_app

if __name__ == '__main__':
    celery_app.start()

```

### Файл: `app/workers/mock_worker.py`
```python
"""
Mock воркер для тестирования
"""
import time
import random
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Any
from sqlalchemy.orm import Session

from app.domain.entities.task import TaskEntity, TaskStatus
from app.domain.entities.upload import UploadEntity
from app.domain.entities.contract import ContractEntity, MatchType, VendorStatus
from app.domain.entities.audit import ContractAuditEntity
from app.domain.entities.selection import TaskSelectionEntity
from app.domain.entities.calculation import TaskCalculationEntity
from app.infra.database import SessionLocal


def mock_run_search_task(task_id: str):
    """
    Mock функция для тестирования поиска контрактов.
    
    Args:
        task_id: ID задачи
    """
    # Создаем сессию базы данных
    db = SessionLocal()
    try:
        # Получаем задачу
        task = db.query(TaskEntity).filter(TaskEntity.id == task_id).first()
        if not task:
            print(f"Задача {task_id} не найдена")
            db.close()
            return
        
        # Обновляем статус задачи
        task.status = TaskStatus.SEARCHING
        task.started_at = datetime.utcnow()
        task.stage = "searching"
        task.progress = 10
        
        # Получаем данные из upload, если они не установлены
        if not task.product_name or not task.ktru_code:
            upload = db.query(UploadEntity).filter(UploadEntity.id == task.upload_id).first()
            if upload and upload.extracted_data:
                extracted_data = upload.extracted_data
                if not task.product_name and "name" in extracted_data:
                    task.product_name = extracted_data["name"]
                if not task.ktru_code and "ktru_code" in extracted_data:
                    task.ktru_code = extracted_data["ktru_code"]
        
        db.commit()
        
        # Имитируем поиск - увеличиваем время для тестирования остановки
        for i in range(10):  # 10 секунд с проверками каждую секунду
            time.sleep(1)
            
            # Проверяем, не остановлена ли задача
            db.refresh(task)
            if task.status == TaskStatus.STOPPED:
                print(f"Задача {task_id} остановлена на этапе поиска")
                db.close()
                return
                
            # Обновляем прогресс
            task.progress = 10 + (i * 8)
            db.commit()
        
        # Проверяем, не остановлена ли задача
        db.refresh(task)
        if task.status == TaskStatus.STOPPED:
            print(f"Задача {task_id} остановлена на этапе поиска")
            db.close()
            return
            
        task.stage = "analyzing"
        task.progress = 50
        db.commit()
        
        # Имитируем анализ - также увеличиваем время
        for i in range(10):  # 10 секунд с проверками каждую секунду
            time.sleep(1)
            
            # Проверяем, не остановлена ли задача
            db.refresh(task)
            if task.status == TaskStatus.STOPPED:
                print(f"Задача {task_id} остановлена на этапе анализа")
                db.close()
                return
                
            # Обновляем прогресс
            task.progress = 50 + (i * 5)
            db.commit()
        
        # Проверяем, не остановлена ли задача
        db.refresh(task)
        if task.status == TaskStatus.STOPPED:
            print(f"Задача {task_id} остановлена перед созданием контрактов")
            db.close()
            return
        
        # Создаем mock контракты
        contracts = []
        for i in range(5):
            contract = ContractEntity(
                id=str(uuid.uuid4()),
                task_id=task_id,
                reg_number=f"1234567890{i}",
                eis_url=f"https://zakupki.gov.ru/epz/order/notice/printForm/view.html?regNumber=1234567890{i}",
                supplier_name=f"Поставщик {i+1} ООО",
                supplier_inn=f"123456789{i}",
                sign_date=datetime.utcnow() - timedelta(days=random.randint(30, 365)),
                unit_price=random.uniform(50000, 150000),
                currency="RUB",
                match_percent=int(random.uniform(70, 100)),
                match_type=MatchType.HOMOGENEOUS if random.random() > 0.5 else MatchType.IDENTICAL,
                vendor_status=VendorStatus.MATCH if random.random() > 0.7 else VendorStatus.MISMATCH,
                raw_data={"mock": True, "index": i}
            )
            contracts.append(contract)
            db.add(contract)
            
            # Создаем mock audit записи для контракта
            for j in range(random.randint(3, 7)):
                audit = ContractAuditEntity(
                    contract_id=contract.id,
                    key=f"Характеристика {j+1}",
                    expected_value=f"Ожидаемое значение {j+1}",
                    found_value=f"Найденное значение {j+1}" if random.random() > 0.3 else f"Другое значение {j+1}",
                    is_diff=random.random() > 0.7,
                    diff_reason="Отличается" if random.random() > 0.7 else None
                )
                db.add(audit)
        
        db.commit()
        
        # Автоматически выбираем 3 контракта
        selected_contracts = _mock_auto_select_contracts(contracts, db)
        
        # Рассчитываем НМЦК
        nmck_value = _calculate_nmck(selected_contracts)
        
        # Сохраняем расчет
        calculation = TaskCalculationEntity(
            task_id=task_id,
            method="average",
            nmc_value=nmck_value,
            currency="RUB",
            computed_at=datetime.utcnow(),
            details={"selected_contracts": [str(c.id) for c in selected_contracts]}
        )
        db.add(calculation)
        
        # Проверяем, не остановлена ли задача
        db.refresh(task)
        if task.status == TaskStatus.STOPPED:
            print(f"Задача {task_id} остановлена пользователем. Сохранено {len(contracts)} контрактов.")
            # Задача уже имеет статус STOPPED, не меняем его
            db.commit()
            return
        
        # Обновляем задачу
        task.status = TaskStatus.DONE
        task.stage = "done"
        task.progress = 100
        task.nmck_value = nmck_value
        task.nmck_currency = "RUB"
        task.finished_at = datetime.utcnow()
        db.commit()
        
        print(f"Mock задача {task_id} успешно выполнена. Создано {len(contracts)} контрактов.")
        
    except Exception as e:
        # Обрабатываем ошибку
        if 'task' in locals():
            # Проверяем, не остановлена ли задача
            db.refresh(task)
            if task.status != TaskStatus.STOPPED:
                task.status = TaskStatus.ERROR
                task.error_code = "MOCK_ERROR"
                task.error_detail = str(e)
                task.finished_at = datetime.utcnow()
                db.commit()
        print(f"Ошибка при выполнении mock задачи {task_id}: {e}")
    finally:
        # Закрываем сессию
        db.close()


def _mock_auto_select_contracts(contracts: List[ContractEntity], db: Session) -> List[ContractEntity]:
    """
    Автоматически выбирает 3 лучших контракта с учетом ограничений.
    """
    if len(contracts) < 3:
        return contracts
    
    # Сортируем контракты по проценту совпадения (по убыванию)
    sorted_contracts = sorted(contracts, key=lambda c: c.match_percent, reverse=True)
    
    # Выбираем контракты, следя за ограничением по поставщикам
    selected = []
    suppliers_selected = set()
    
    for contract in sorted_contracts:
        if len(selected) >= 3:
            break
        
        # Проверяем ограничение по поставщикам
        if contract.supplier_inn in suppliers_selected and len(suppliers_selected) == 1:
            continue
        
        selected.append(contract)
        suppliers_selected.add(contract.supplier_inn)
    
    # Сохраняем выбор в БД
    for contract in selected:
        selection = TaskSelectionEntity(
            task_id=contract.task_id,
            contract_id=contract.id,
            selected_at=datetime.utcnow()
        )
        db.add(selection)
    
    return selected


def _calculate_nmck(contracts: List[ContractEntity]) -> float:
    """
    Рассчитывает НМЦК как среднее арифметическое цен выбранных контрактов.
    """
    if not contracts:
        return 0.0
    
    total_price = sum(contract.unit_price for contract in contracts)
    return total_price / len(contracts)
```

### Файл: `app/workers/search_worker.py`
```python
"""
Исправленный воркер для выполнения поиска контрактов в ЕИС
"""
import time
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any
from sqlalchemy.orm import Session

from app.domain.entities.task import TaskEntity, TaskStatus
from app.domain.entities.upload import UploadEntity
from app.domain.entities.contract import ContractEntity, MatchType, VendorStatus
from app.domain.entities.audit import ContractAuditEntity
from app.domain.entities.selection import TaskSelectionEntity
from app.domain.entities.calculation import TaskCalculationEntity
from app.adapters.eis.sync_adapter import SyncEISParser
from app.adapters.match_engine import MatchEngine, MatchType as MatchTypeEnum, VendorStatus as VendorStatusEnum
from app.workers.celery_app import celery_app
from app.infra.database import SessionLocal


@celery_app.task(bind=True, name="app.workers.search_worker.run_search_task")
def run_search_task(self, task_id: str):
    """
    Основная функция воркера для выполнения поиска контрактов.
    
    Args:
        task_id: ID задачи
    """
    # Создаем сессию базы данных
    db = SessionLocal()
    try:
        # Получаем задачу
        task = db.query(TaskEntity).filter(TaskEntity.id == task_id).first()
        if not task:
            print(f"Задача {task_id} не найдена")
            db.close()
            return
        
        # Обновляем статус задачи
        task.status = TaskStatus.SEARCHING
        task.started_at = datetime.utcnow()
        task.stage = "Поиск контрактов"
        task.progress = 10
        db.commit()
        
        # Получаем данные загрузки
        upload = db.query(UploadEntity).filter(UploadEntity.id == task.upload_id).first()
        if not upload:
            task.status = TaskStatus.ERROR
            task.error_code = "UPLOAD_NOT_FOUND"
            task.error_detail = "Загрузка не найдена"
            task.finished_at = datetime.utcnow()
            db.commit()
            db.close()
            return
        
        # Извлекаем требования
        requirements = upload.extracted_json or {}
        ktru_code = requirements.get("ktru_code", "")
        product_name = requirements.get("name", "")
        expected_characteristics = requirements.get("characteristics", {})
        expected_vendor = requirements.get("vendor", "")
        
        # Создаем парсер ЕИС
        parser = SyncEISParser(region=task.region, law_type=task.law_type)
        
        # Обновляем статус
        task.stage = "Поиск контрактов в ЕИС"
        task.progress = 20
        db.commit()
        
        # Ищем контракты
        try:
            contracts_data = parser.search_contracts(
                ktru_code=ktru_code,
                product_name=product_name,
                period_from=task.period_from,
                period_to=task.period_to
            )
        except Exception as e:
            task.status = TaskStatus.ERROR
            task.error_code = "EIS_SEARCH_ERROR"
            task.error_detail = f"Ошибка поиска в ЕИС: {str(e)}"
            task.finished_at = datetime.utcnow()
            db.commit()
            print(f"Ошибка при поиске контрактов: {e}")
            return
        
        # Обновляем статус
        task.stage = "Анализ контрактов"
        task.progress = 40
        task.total_found = len(contracts_data)
        db.commit()
        
        # Создаем движок сопоставления
        match_engine = MatchEngine()
        
        # Анализируем контракты
        contracts = []
        for i, contract_data in enumerate(contracts_data):
            # Обновляем прогресс
            task.progress = 40 + int((i / len(contracts_data)) * 40)
            db.commit()

            try:
                # Извлекаем характеристики
                found_characteristics = parser.extract_characteristics(contract_data["url"])
                found_vendor = parser.get_contract_vendor(contract_data["url"])
                
                # Рассчитываем совпадение (упрощенная версия, пока нет полноценного match engine)
                match_percent = 0.0
                match_type = MatchType.DIFFERENT
                vendor_status = VendorStatus.UNKNOWN
                audit_log = []
                
                # TODO: Реализовать полноценный match engine
                # Временная заглушка - рассчитываем процент совпадения
                if expected_characteristics:
                    # Упрощенный расчет
                    match_percent = 50.0  # Заглушка
                    match_type = MatchType.HOMOGENEOUS
                
                # Проверка вендора (упрощенная)
                if expected_vendor and found_vendor:
                    if expected_vendor.lower() in found_vendor.lower() or found_vendor.lower() in expected_vendor.lower():
                        vendor_status = VendorStatus.MATCH
                    else:
                        vendor_status = VendorStatus.MISMATCH
                
                # Преобразуем дату
                sign_date = datetime.utcnow()
                if contract_data.get("date"):
                    try:
                        # Пробуем разные форматы дат
                        date_str = contract_data["date"]
                        for fmt in ["%d.%m.%Y", "%Y-%m-%d", "%d/%m/%Y"]:
                            try:
                                sign_date = datetime.strptime(date_str, fmt)
                                break
                            except ValueError:
                                continue
                    except:
                        pass
                
                # Создаем контракт
                contract = ContractEntity(
                    task_id=task.id,
                    reg_number=contract_data["reg_number"],
                    eis_url=contract_data["url"],
                    supplier_name=contract_data["supplier_name"],
                    supplier_inn="",  # TODO: Извлечь ИНН из деталей контракта
                    sign_date=sign_date,
                    unit_price=contract_data.get("price", 0.0),
                    currency=contract_data.get("currency", "RUB"),
                    match_percent=match_percent,
                    match_type=match_type,
                    vendor_status=vendor_status,
                    raw_payload_json=contract_data
                )
                db.add(contract)
                db.flush()  # Получаем ID контракта
                
                # Сохраняем лог сверки (упрощенный)
                if expected_characteristics:
                    for key, expected_value in expected_characteristics.items():
                        found_value = found_characteristics.get(key, "")
                        is_diff = expected_value != found_value
                        
                        audit_row = ContractAuditEntity(
                            contract_id=contract.id,
                            key=key,
                            expected_value=str(expected_value),
                            found_value=str(found_value),
                            is_diff=is_diff,
                            diff_reason="Не найдено" if not found_value else "Значение отличается"
                        )
                        db.add(audit_row)
                
                contracts.append(contract)
                
            except Exception as e:
                print(f"Ошибка при анализе контракта {contract_data.get('reg_number', 'N/A')}: {e}")
                continue

        # Обновляем статус
        task.stage = "Выбор контрактов"
        task.progress = 85
        task.total_analyzed = len(contracts)
        db.commit()

        # Автоматически выбираем 3 лучших контракта
        selected_contracts = _auto_select_contracts(contracts, db)

        # Рассчитываем НМЦК
        nmck_value = _calculate_nmck(selected_contracts)

        # Сохраняем расчет
        calculation = TaskCalculationEntity(
            task_id=task.id,
            method="average",
            nmc_value=nmck_value,
            currency="RUB",
            details_json={
                "selected_contracts": [str(c.id) for c in selected_contracts],
                "calculation_method": "average",
                "calculation_date": datetime.utcnow().isoformat()
            }
        )
        db.add(calculation)

        # Обновляем задачу
        task.status = TaskStatus.DONE
        task.stage = "Завершено"
        task.progress = 100
        task.nmck_value = nmck_value
        task.nmck_currency = "RUB"
        task.finished_at = datetime.utcnow()
        db.commit()

        print(f"Задача {task_id} успешно выполнена. Найдено {len(contracts)} контрактов.")

    except Exception as e:
        # Обрабатываем ошибку
        task.status = TaskStatus.ERROR
        task.error_code = "SEARCH_ERROR"
        task.error_detail = str(e)
        task.finished_at = datetime.utcnow()
        db.commit()
        print(f"Ошибка при выполнении задачи {task_id}: {e}")
    finally:
        # Закрываем сессию
        db.close()


def _auto_select_contracts(contracts: List[ContractEntity], db: Session) -> List[ContractEntity]:
    """
    Автоматически выбирает 3 лучших контракта с учетом ограничений.
    
    Args:
        contracts: Список контрактов
        db: Сессия базы данных
        
    Returns:
        Список выбранных контрактов
    """
    if not contracts:
        return []
    
    # Сортируем по проценту совпадения (по убыванию)
    sorted_contracts = sorted(contracts, key=lambda c: c.match_percent, reverse=True)
    
    # Выбираем 3 лучших, но не более 2 от одного поставщика
    selected_contracts = []
    supplier_count = {}
    
    for contract in sorted_contracts:
        supplier = contract.supplier_name
        if supplier not in supplier_count:
            supplier_count[supplier] = 0
        
        # Проверяем правило: не более 2 контрактов от одного поставщика
        if supplier_count[supplier] < 2:
            selected_contracts.append(contract)
            supplier_count[supplier] += 1
        
        if len(selected_contracts) >= 3:
            break
    
    # Сохраняем выбранные контракты
    for contract in selected_contracts:
        selection = TaskSelectionEntity(
            task_id=contract.task_id,
            contract_id=contract.id,
            selected_at=datetime.utcnow()
        )
        db.add(selection)
    
    return selected_contracts


def _calculate_nmck(contracts: List[ContractEntity]) -> float:
    """
    Рассчитывает НМЦК как среднее арифметическое цен выбранных контрактов.
    
    Args:
        contracts: Список контрактов
        
    Returns:
        Значение НМЦК
    """
    if not contracts:
        return 0.0
    
    total_price = sum(c.unit_price for c in contracts)
    return total_price / len(contracts)
```

### Файл: `app/workers/search_worker_fixed.py`
```python
"""
Исправленный воркер для выполнения поиска контрактов в ЕИС
"""
import time
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any
from sqlalchemy.orm import Session

from app.domain.entities.task import TaskEntity, TaskStatus
from app.domain.entities.upload import UploadEntity
from app.domain.entities.contract import ContractEntity, MatchType, VendorStatus
from app.domain.entities.audit import ContractAuditEntity
from app.domain.entities.selection import TaskSelectionEntity
from app.domain.entities.calculation import TaskCalculationEntity
from app.adapters.eis.sync_adapter import SyncEISParser
from app.adapters.match_engine import MatchEngine, MatchType as MatchTypeEnum, VendorStatus as VendorStatusEnum
from app.workers.celery_app import celery_app
from app.infra.database import SessionLocal


@celery_app.task(bind=True, name="app.workers.search_worker.run_search_task")
def run_search_task(self, task_id: str):
    """
    Основная функция воркера для выполнения поиска контрактов.
    
    Args:
        task_id: ID задачи
    """
    # Создаем сессию базы данных
    db = SessionLocal()
    try:
        # Получаем задачу
        task = db.query(TaskEntity).filter(TaskEntity.id == task_id).first()
        if not task:
            print(f"Задача {task_id} не найдена")
            db.close()
            return
        
        # Обновляем статус задачи
        task.status = TaskStatus.SEARCHING
        task.started_at = datetime.utcnow()
        task.stage = "Поиск контрактов"
        task.progress = 10
        db.commit()
        
        # Получаем данные загрузки
        upload = db.query(UploadEntity).filter(UploadEntity.id == task.upload_id).first()
        if not upload:
            task.status = TaskStatus.ERROR
            task.error_code = "UPLOAD_NOT_FOUND"
            task.error_detail = "Загрузка не найдена"
            task.finished_at = datetime.utcnow()
            db.commit()
            db.close()
            return
        
        # Извлекаем требования
        requirements = upload.extracted_json or {}
        ktru_code = requirements.get("ktru_code", "")
        product_name = requirements.get("name", "")
        expected_characteristics = requirements.get("characteristics", {})
        expected_vendor = requirements.get("vendor", "")
        
        # Создаем парсер ЕИС
        parser = SyncEISParser(region=task.region, law_type=task.law_type)
        
        # Обновляем статус
        task.stage = "Поиск контрактов в ЕИС"
        task.progress = 20
        db.commit()
        
        # Ищем контракты
        try:
            contracts_data = parser.search_contracts(
                ktru_code=ktru_code,
                product_name=product_name,
                period_from=task.period_from,
                period_to=task.period_to
            )
        except Exception as e:
            task.status = TaskStatus.ERROR
            task.error_code = "EIS_SEARCH_ERROR"
            task.error_detail = f"Ошибка поиска в ЕИС: {str(e)}"
            task.finished_at = datetime.utcnow()
            db.commit()
            print(f"Ошибка при поиске контрактов: {e}")
            return
        
        # Обновляем статус
        task.stage = "Анализ контрактов"
        task.progress = 40
        task.total_found = len(contracts_data)
        db.commit()
        
        # Создаем движок сопоставления
        match_engine = MatchEngine()
        
        # Анализируем контракты
        contracts = []
        for i, contract_data in enumerate(contracts_data):
            # Обновляем прогресс
            task.progress = 40 + int((i / len(contracts_data)) * 40)
            db.commit()

            try:
                # Извлекаем характеристики
                found_characteristics = parser.extract_characteristics(contract_data["url"])
                found_vendor = parser.get_contract_vendor(contract_data["url"])
                
                # Рассчитываем совпадение (упрощенная версия, пока нет полноценного match engine)
                match_percent = 0.0
                match_type = MatchType.DIFFERENT
                vendor_status = VendorStatus.UNKNOWN
                audit_log = []
                
                # TODO: Реализовать полноценный match engine
                # Временная заглушка - рассчитываем процент совпадения
                if expected_characteristics:
                    # Упрощенный расчет
                    match_percent = 50.0  # Заглушка
                    match_type = MatchType.HOMOGENEOUS
                
                # Проверка вендора (упрощенная)
                if expected_vendor and found_vendor:
                    if expected_vendor.lower() in found_vendor.lower() or found_vendor.lower() in expected_vendor.lower():
                        vendor_status = VendorStatus.MATCH
                    else:
                        vendor_status = VendorStatus.MISMATCH
                
                # Преобразуем дату
                sign_date = datetime.utcnow()
                if contract_data.get("date"):
                    try:
                        # Пробуем разные форматы дат
                        date_str = contract_data["date"]
                        for fmt in ["%d.%m.%Y", "%Y-%m-%d", "%d/%m/%Y"]:
                            try:
                                sign_date = datetime.strptime(date_str, fmt)
                                break
                            except ValueError:
                                continue
                    except:
                        pass
                
                # Создаем контракт
                contract = ContractEntity(
                    task_id=task.id,
                    reg_number=contract_data["reg_number"],
                    eis_url=contract_data["url"],
                    supplier_name=contract_data["supplier_name"],
                    supplier_inn="",  # TODO: Извлечь ИНН из деталей контракта
                    sign_date=sign_date,
                    unit_price=contract_data.get("price", 0.0),
                    currency=contract_data.get("currency", "RUB"),
                    match_percent=match_percent,
                    match_type=match_type,
                    vendor_status=vendor_status,
                    raw_payload_json=contract_data
                )
                db.add(contract)
                db.flush()  # Получаем ID контракта
                
                # Сохраняем лог сверки (упрощенный)
                if expected_characteristics:
                    for key, expected_value in expected_characteristics.items():
                        found_value = found_characteristics.get(key, "")
                        is_diff = expected_value != found_value
                        
                        audit_row = ContractAuditEntity(
                            contract_id=contract.id,
                            key=key,
                            expected_value=str(expected_value),
                            found_value=str(found_value),
                            is_diff=is_diff,
                            diff_reason="Не найдено" if not found_value else "Значение отличается"
                        )
                        db.add(audit_row)
                
                contracts.append(contract)
                
            except Exception as e:
                print(f"Ошибка при анализе контракта {contract_data.get('reg_number', 'N/A')}: {e}")
                continue

        # Обновляем статус
        task.stage = "Выбор контрактов"
        task.progress = 85
        task.total_analyzed = len(contracts)
        db.commit()

        # Автоматически выбираем 3 лучших контракта
        selected_contracts = _auto_select_contracts(contracts, db)

        # Рассчитываем НМЦК
        nmck_value = _calculate_nmck(selected_contracts)

        # Сохраняем расчет
        calculation = TaskCalculationEntity(
            task_id=task.id,
            method="average",
            nmc_value=nmck_value,
            currency="RUB",
            details_json={
                "selected_contracts": [str(c.id) for c in selected_contracts],
                "calculation_method": "average",
                "calculation_date": datetime.utcnow().isoformat()
            }
        )
        db.add(calculation)

        # Обновляем задачу
        task.status = TaskStatus.DONE
        task.stage = "Завершено"
        task.progress = 100
        task.nmck_value = nmck_value
        task.nmck_currency = "RUB"
        task.finished_at = datetime.utcnow()
        db.commit()

        print(f"Задача {task_id} успешно выполнена. Найдено {len(contracts)} контрактов.")

    except Exception as e:
        # Обрабатываем ошибку
        task.status = TaskStatus.ERROR
        task.error_code = "SEARCH_ERROR"
        task.error_detail = str(e)
        task.finished_at = datetime.utcnow()
        db.commit()
        print(f"Ошибка при выполнении задачи {task_id}: {e}")
    finally:
        # Закрываем сессию
        db.close()


def _auto_select_contracts(contracts: List[ContractEntity], db: Session) -> List[ContractEntity]:
    """
    Автоматически выбирает 3 лучших контракта с учетом ограничений.
    
    Args:
        contracts: Список контрактов
        db: Сессия базы данных
        
    Returns:
        Список выбранных контрактов
    """
    if not contracts:
        return []
    
    # Сортируем по проценту совпадения (по убыванию)
    sorted_contracts = sorted(contracts, key=lambda c: c.match_percent, reverse=True)
    
    # Выбираем 3 лучших, но не более 2 от одного поставщика
    selected_contracts = []
    supplier_count = {}
    
    for contract in sorted_contracts:
        supplier = contract.supplier_name
        if supplier not in supplier_count:
            supplier_count[supplier] = 0
        
        # Проверяем правило: не более 2 контрактов от одного поставщика
        if supplier_count[supplier] < 2:
            selected_contracts.append(contract)
            supplier_count[supplier] += 1
        
        if len(selected_contracts) >= 3:
            break
    
    # Сохраняем выбранные контракты
    for contract in selected_contracts:
        selection = TaskSelectionEntity(
            task_id=contract.task_id,
            contract_id=contract.id,
            selected_at=datetime.utcnow()
        )
        db.add(selection)
    
    return selected_contracts


def _calculate_nmck(contracts: List[ContractEntity]) -> float:
    """
    Рассчитывает НМЦК как среднее арифметическое цен выбранных контрактов.
    
    Args:
        contracts: Список контрактов
        
    Returns:
        Значение НМЦК
    """
    if not contracts:
        return 0.0
    
    total_price = sum(c.unit_price for c in contracts)
    return total_price / len(contracts)
```

### Файл: `app/workers/search_worker_refactored.py`
```python
"""
Рефакторинг воркера с использованием новой архитектуры
"""
from app.application.use_cases.search_contracts import SearchContractsUseCase
from app.infra.repositories.sqlalchemy_task_repository import SQLAlchemyTaskRepository
from app.infra.repositories.sqlalchemy_upload_repository import SQLAlchemyUploadRepository
from app.infra.repositories.sqlalchemy_contract_repository import SQLAlchemyContractRepository
from app.adapters.eis.sync_adapter import SyncEISParser
from app.adapters.match_engine import MatchEngine
from app.workers.celery_app import celery_app
from app.infra.database import SessionLocal


@celery_app.task(bind=True, name="app.workers.search_worker_refactored.run_search_task")
def run_search_task(self, task_id: str):
    """
    Основная функция воркера с использованием новой архитектуры
    
    Args:
        task_id: ID задачи
    """
    # Создаем сессию базы данных
    db = SessionLocal()
    try:
        # Создаем репозитории
        task_repository = SQLAlchemyTaskRepository(db)
        upload_repository = SQLAlchemyUploadRepository(db)
        contract_repository = SQLAlchemyContractRepository(db)
        
        # Создаем адаптеры
        eis_parser = SyncEISParser()
        match_engine = MatchEngine()
        
        # Создаем use case
        use_case = SearchContractsUseCase(
            task_repository=task_repository,
            upload_repository=upload_repository,
            contract_repository=contract_repository,
            eis_parser=eis_parser,
            match_engine=match_engine,
        )
        
        # Выполняем поиск контрактов
        result = use_case.execute(task_id)
        
        if result["success"]:
            print(f"Поиск завершен успешно. Найдено контрактов: {result.get('contracts_found', 0)}")
        else:
            print(f"Ошибка поиска: {result.get('error', 'Неизвестная ошибка')}")
        
        db.commit()
        
    except Exception as e:
        db.rollback()
        print(f"Критическая ошибка в воркере: {e}")
        raise
    
    finally:
        db.close()


# Для обратной совместимости оставляем старую функцию
@celery_app.task(bind=True, name="app.workers.search_worker.run_search_task_legacy")
def run_search_task_legacy(self, task_id: str):
    """
    Легаси функция для обратной совместимости
    """
    return run_search_task(task_id)
```

### Файл: `collect_backend.py`
```python
import os
import glob

def collect_backend_files():
    """Собрать все файлы бэкенда"""
    backend_files = []
    
    # Python файлы бэкенда
    python_files = glob.glob("**/*.py", recursive=True)
    
    # Исключаем ненужные директории
    exclude_dirs = ['.git', 'venv', '__pycache__', 'uploads', 'static', 'node_modules']
    
    for file in python_files:
        if any(exclude in file for exclude in exclude_dirs):
            continue
        
        # Проверяем, что это файл бэкенда (не тестовый и не временный)
        if not any(x in file for x in ['test_', '_test', 'fixed_', 'backup']):
            backend_files.append(file)
    
    # Сортируем по алфавиту
    backend_files.sort()
    
    # Создаем markdown файл
    with open("/workspace/backend_full_code.md", "w", encoding="utf-8") as md_file:
        md_file.write("# Полный код бэкенда системы поиска контрактов по КТРУ\n\n")
        md_file.write("## Содержание\n")
        
        # Добавляем оглавление
        for i, file in enumerate(backend_files, 1):
            md_file.write(f"{i}. [{file}](#{file.replace('/', '').replace('.', '').replace('_', '')})\n")
        
        md_file.write("\n---\n\n")
        
        # Добавляем содержимое каждого файла
        for file in backend_files:
            try:
                with open(file, "r", encoding="utf-8") as f:
                    content = f.read()
                
                md_file.write(f"### Файл: `{file}`\n")
                md_file.write("```python\n")
                md_file.write(content)
                md_file.write("\n```\n\n")
                
            except Exception as e:
                md_file.write(f"### Файл: `{file}`\n")
                md_file.write(f"*Ошибка чтения файла: {str(e)}*\n\n")
    
    print(f"✅ Собрано {len(backend_files)} файлов бэкенда")
    return backend_files

def collect_frontend_files():
    """Собрать все файлы фронтенда"""
    frontend_files = []
    
    # HTML, CSS, JS файлы
    frontend_extensions = ['.html', '.css', '.js', '.json']
    
    for ext in frontend_extensions:
        files = glob.glob(f"**/*{ext}", recursive=True)
        for file in files:
            # Исключаем ненужные директории
            if any(exclude in file for exclude in ['.git', 'venv', '__pycache__', 'uploads']):
                continue
            
            # Проверяем, что это файл фронтенда
            if 'static' in file or file.endswith(ext):
                frontend_files.append(file)
    
    # Сортируем по алфавиту
    frontend_files.sort()
    
    # Создаем markdown файл
    with open("/workspace/frontend_full_code.md", "w", encoding="utf-8") as md_file:
        md_file.write("# Полный код фронтенда системы поиска контрактов по КТРУ\n\n")
        md_file.write("## Содержание\n")
        
        # Добавляем оглавление
        for i, file in enumerate(frontend_files, 1):
            md_file.write(f"{i}. [{file}](#{file.replace('/', '').replace('.', '').replace('_', '')})\n")
        
        md_file.write("\n---\n\n")
        
        # Добавляем содержимое каждого файла
        for file in frontend_files:
            try:
                with open(file, "r", encoding="utf-8") as f:
                    content = f.read()
                
                md_file.write(f"### Файл: `{file}`\n")
                
                # Определяем язык для подсветки синтаксиса
                if file.endswith('.html'):
                    md_file.write("```html\n")
                elif file.endswith('.css'):
                    md_file.write("```css\n")
                elif file.endswith('.js'):
                    md_file.write("```javascript\n")
                else:
                    md_file.write("```\n")
                
                md_file.write(content)
                md_file.write("\n```\n\n")
                
            except Exception as e:
                md_file.write(f"### Файл: `{file}`\n")
                md_file.write(f"*Ошибка чтения файла: {str(e)}*\n\n")
    
    print(f"✅ Собрано {len(frontend_files)} файлов фронтенда")
    return frontend_files

if __name__ == "__main__":
    print("Сбор файлов бэкенда...")
    backend_files = collect_backend_files()
    
    print("\nСбор файлов фронтенда...")
    frontend_files = collect_frontend_files()
    
    print(f"\nИтого:")
    print(f"- Бэкенд: {len(backend_files)} файлов")
    print(f"- Фронтенд: {len(frontend_files)} файлов")
    print(f"\nФайлы сохранены:")
    print(f"- /workspace/backend_full_code.md")
    print(f"- /workspace/frontend_full_code.md")

```

### Файл: `docs/__init__.py`
```python

```

### Файл: `run.py`
```python
#!/usr/bin/env python3
"""
Скрипт для запуска системы НМЦК
"""
import os
import sys
import uvicorn
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

if __name__ == "__main__":
    # Создаем таблицы при запуске
    from app.infra.database import Base, engine
    print("Создание таблиц базы данных...")
    Base.metadata.create_all(bind=engine)
    print("Таблицы созданы успешно")
    
    # Запускаем FastAPI приложение
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

```

### Файл: `session_fixed.py`
```python
"""
Роутер для работы с сессиями
"""
import uuid
import logging
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy.orm import Session

from app.infra.database import get_db
from app.domain.entities.session import SessionEntity
from app.schemas.session import SessionCreate, SessionResponse

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/session", response_model=SessionResponse)
async def get_or_create_session(
    request: Request,
    response: Response,
    db: Session = Depends(get_db)
):
    """
    Получить или создать сессию.

    Если в куках есть session_token, возвращает существующую сессию.
    Если нет - создает новую сессию и устанавливает куку.
    """
    # Проверяем наличие session_token в куках
    session_token = request.cookies.get("session_token")

    if session_token:
        # Ищем существующую сессию
        try:
            session_uuid = uuid.UUID(session_token)
            # Для SQLite ищем по строковому представлению
            from app.infra.config import settings
            if "sqlite" in settings.DATABASE_URL:
                session_entity = db.query(SessionEntity).filter(
                    SessionEntity.id == str(session_uuid)
                ).first()
            else:
                session_entity = db.query(SessionEntity).filter(
                    SessionEntity.id == session_uuid
                ).first()
        except ValueError:
            session_entity = None

        if session_entity:
            # Обновляем время последнего визита
            session_entity.last_seen_at = datetime.utcnow()
            db.commit()

            # Отладка
            logger.error(f"DEBUG: session_entity.id = {session_entity.id}, type = {type(session_entity.id)}")

            return SessionResponse(
                id=str(session_entity.id),
                created_at=session_entity.created_at,
                last_seen_at=session_entity.last_seen_at,
                token=str(session_entity.id)  # Добавляем токен для совместимости с фронтендом
            )

    # Создаем новую сессию
    session_uuid = uuid.uuid4()
    session_uuid_str = str(session_uuid)
    logger.error(f"DEBUG: Creating session with uuid = {session_uuid_str}, type = {type(session_uuid_str)}")
    
    # Для SQLite используем строковое представление UUID
    from app.infra.config import settings
    if "sqlite" in settings.DATABASE_URL:
        session_entity = SessionEntity(
            id=session_uuid_str,  # Используем строку для SQLite
            token=session_uuid_str,
            created_at=datetime.utcnow(),
            last_seen_at=datetime.utcnow()
        )
    else:
        session_entity = SessionEntity(
            id=session_uuid,  # Используем UUID объект для PostgreSQL
            token=session_uuid_str,
            created_at=datetime.utcnow(),
            last_seen_at=datetime.utcnow()
        )
    
    logger.error(f"DEBUG: session_entity created, id = {session_entity.id}, type = {type(session_entity.id)}")

    db.add(session_entity)
    db.commit()

    # Устанавливаем куку
    response.set_cookie(
        key="session_token",
        value=session_uuid_str,
        httponly=True,
        max_age=86400 * 30,  # 30 дней
        samesite="lax"
    )

    # Отладка
    logger.error(f"DEBUG: session_id_str = {session_uuid_str}, type = {type(session_uuid_str)}")
    logger.error(f"DEBUG: session_entity.id = {session_entity.id}, type = {type(session_entity.id)}")
    logger.error(f"DEBUG: session_entity.created_at = {session_entity.created_at}, type = {type(session_entity.created_at)}")
    logger.error(f"DEBUG: session_entity.last_seen_at = {session_entity.last_seen_at}, type = {type(session_entity.last_seen_at)}")

    return SessionResponse(
        id=session_uuid_str,
        created_at=session_entity.created_at,
        last_seen_at=session_entity.last_seen_at,
        token=session_uuid_str  # Добавляем токен для совместимости с фронтендом
    )

@router.delete("/session")
async def delete_session(
    request: Request,
    response: Response,
    db: Session = Depends(get_db)
):
    """
    Удалить сессию (выход из системы).
    """
    session_token = request.cookies.get("session_token")
    
    if session_token:
        try:
            session_uuid = uuid.UUID(session_token)
            # Для SQLite ищем по строковому представлению
            from app.infra.config import settings
            if "sqlite" in settings.DATABASE_URL:
                session_entity = db.query(SessionEntity).filter(
                    SessionEntity.id == str(session_uuid)
                ).first()
            else:
                session_entity = db.query(SessionEntity).filter(
                    SessionEntity.id == session_uuid
                ).first()
            
            if session_entity:
                db.delete(session_entity)
                db.commit()
        except ValueError:
            pass
    
    # Удаляем куку
    response.delete_cookie(key="session_token")
    
    return {"message": "Сессия удалена"}

```

### Файл: `tests/__init__.py`
```python

```

### Файл: `tests/e2e/__init__.py`
```python

```

### Файл: `tests/integration/__init__.py`
```python

```

### Файл: `tests/unit/__init__.py`
```python

```

### Файл: `uuid_fix.py`
```python
#!/usr/bin/env python3
"""
Исправление для работы UUID с SQLite
"""
import uuid
from sqlalchemy import String
from sqlalchemy.types import TypeDecorator, CHAR
from sqlalchemy.dialects.postgresql import UUID as PG_UUID


class UUIDString(TypeDecorator):
    """Кастомный тип для хранения UUID как строки в SQLite"""
    impl = String(36)
    cache_ok = True
    
    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        if isinstance(value, uuid.UUID):
            return str(value)
        return value
    
    def process_result_value(self, value, dialect):
        if value is None:
            return None
        if not isinstance(value, uuid.UUID):
            return uuid.UUID(value)
        return value


def apply_uuid_fix():
    """Применяет исправление UUID для всех моделей"""
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    # Импортируем после добавления пути
    from app.domain.entities.base import BaseEntity
    from app.infra.config import settings
    from sqlalchemy import inspect
    
    # Проверяем, используем ли мы SQLite
    if "sqlite" in settings.DATABASE_URL:
        print("🔧 Применяем исправление UUID для SQLite...")
        
        # Импортируем все модели
        from app.domain.entities import session, upload, task, contract, selection
        
        # Получаем все таблицы
        from app.domain.entities.base import Base
        from sqlalchemy import event
        
        # Создаем обработчик для преобразования UUID перед сохранением
        @event.listens_for(Base.metadata, "before_create")
        def before_create(target, connection, **kw):
            """Исправляем типы столбцов перед созданием таблиц"""
            for table in Base.metadata.tables.values():
                for column in table.columns:
                    if hasattr(column.type, '__visit_name__') and column.type.__visit_name__ == 'UUID':
                        column.type = String(36)
        
        print("✅ Исправление применено")
    else:
        print("ℹ️ Используется PostgreSQL, исправление не требуется")


if __name__ == "__main__":
    apply_uuid_fix()

```

