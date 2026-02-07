#!/usr/bin/env python3
"""
Простой скрипт для внесения изменений в проект zakupki-analyzer
"""

import os
import sys

PROJECT_ROOT = "/workspace/zakupki-analyzer"
BACKEND_DIR = os.path.join(PROJECT_ROOT, "backend")

def main():
    print("Начинаем внесение изменений в проект zakupki-analyzer")
    
    # 1. Сначала обновим файл deps.py
    deps_file = os.path.join(BACKEND_DIR, "app/api/deps.py")
    print(f"\n1. Обновление файла: {deps_file}")
    
    with open(deps_file, 'r', encoding='utf-8') as f:
        deps_content = f.read()
    
    # Добавим импорты
    new_imports = """from app.infra.events.event_broker import RedisEventBroker
from app.core.settings import settings"""
    
    # Добавим функцию get_event_broker
    new_function = """
def get_event_broker() -> RedisEventBroker:
    \"\"\"Dependency provider for a Redis event broker.\"\"\"
    # Используем singleton или создаем новый, исходя из настроек
    return RedisEventBroker(settings.redis_url)"""
    
    # Вставим импорты после существующих
    lines = deps_content.split('\n')
    new_lines = []
    imports_added = False
    for line in lines:
        new_lines.append(line)
        if 'from app.infra.db.session import async_sessionmaker' in line and not imports_added:
            new_lines.append(new_imports)
            imports_added = True
    
    deps_content = '\n'.join(new_lines)
    
    # Добавим функцию после get_db
    if 'def get_event_broker()' not in deps_content:
        get_db_end = deps_content.find('def get_request_id')
        if get_db_end != -1:
            deps_content = deps_content[:get_db_end] + new_function + '\n\n' + deps_content[get_db_end:]
    
    with open(deps_file, 'w', encoding='utf-8') as f:
        f.write(deps_content)
    
    print("✓ Файл deps.py обновлен")
    
    # 2. Обновим файл search_service.py
    service_file = os.path.join(BACKEND_DIR, "app/services/search_service.py")
    print(f"\n2. Обновление файла: {service_file}")
    
    with open(service_file, 'r', encoding='utf-8') as f:
        service_content = f.read()
    
    # Добавим импорт Depends
    if "from fastapi import Depends" not in service_content:
        lines = service_content.split('\n')
        new_lines = []
        for line in lines:
            new_lines.append(line)
            if "from app.api.deps import" in line:
                new_lines[-1] = "from fastapi import Depends\nfrom app.api.deps import get_db, get_event_broker"
        
        service_content = '\n'.join(new_lines)
    
    # Обновим конструктор __init__
    old_init = "def __init__(self, *, db: AsyncSession, broker: RedisEventBroker) -> None:"
    new_init = """def __init__(
        self,
        db: AsyncSession = Depends(get_db),
        broker: RedisEventBroker = Depends(get_event_broker)
    ) -> None:"""
    
    service_content = service_content.replace(old_init, new_init)
    
    # Добавим функцию calc_nmc_avg в конец файла
    calc_function = """
def calc_nmc_avg(prices: list[Decimal]) -> Decimal:
    \"\"\"Рассчитывает среднее значение НМЦК из списка цен.\"\"\"
    if not prices:
        return Decimal('0')
    total = sum(prices, Decimal('0'))
    return total / len(prices)"""
    
    if 'def calc_nmc_avg' not in service_content:
        service_content += calc_function
    
    with open(service_file, 'w', encoding='utf-8') as f:
        f.write(service_content)
    
    print("✓ Файл search_service.py обновлен")
    
    # 3. Обновим файл search.py
    search_file = os.path.join(BACKEND_DIR, "app/api/search.py")
    print(f"\n3. Обновление файла: {search_file}")
    
    with open(search_file, 'r', encoding='utf-8') as f:
        search_content = f.read()
    
    # Добавим импорт SearchResultListResponse
    if "SearchResultListResponse" not in search_content:
        lines = search_content.split('\n')
        for i, line in enumerate(lines):
            if 'from app.schemas.search import' in line and 'SearchResultItem' in line:
                lines[i] = line.replace('SearchResultItem', 'SearchResultItem, SearchResultListResponse')
                break
        
        search_content = '\n'.join(lines)
    
    with open(search_file, 'w', encoding='utf-8') as f:
        f.write(search_content)
    
    print("✓ Файл search.py обновлен")
    
    print("\n✅ Все основные изменения внесены!")
    print("\nПримечание: Для полного внесения всех изменений из файла Изменения.md")
    print("необходимо также вручную обновить методы list_searches, get_search_results")
    print("и update_selection в search_service.py, а также эндпоинты в search.py")
    print("в соответствии с требованиями из файла Изменения.md")

if __name__ == '__main__':
    main()
