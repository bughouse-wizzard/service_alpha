#!/usr/bin/env python3
"""
Скрипт для объединения всех файлов бекенда в один markdown файл
"""

import os
import sys
from pathlib import Path

def read_file_content(filepath):
    """Чтение содержимого файла"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        # Попробуем другую кодировку
        with open(filepath, 'r', encoding='latin-1') as f:
            return f.read()
    except Exception as e:
        return f"# Ошибка чтения файла {filepath}: {str(e)}"

def get_file_category(filepath):
    """Определение категории файла по пути"""
    filepath_str = str(filepath)
    
    if 'dashboard/backend' in filepath_str:
        return 'dashboard_backend'
    elif 'db/postgres' in filepath_str:
        if 'models' in filepath_str:
            return 'db_models'
        elif 'migrations' in filepath_str:
            return 'db_migrations'
        else:
            return 'db'
    elif 'llm/providers' in filepath_str:
        return 'llm_providers'
    elif 'integrations' in filepath_str:
        return 'integrations'
    elif 'agents' in filepath_str:
        return 'agents'
    elif 'schemas' in filepath_str:
        return 'schemas'
    elif 'vcs' in filepath_str:
        return 'vcs'
    elif 'tests' in filepath_str:
        return 'tests'
    elif filepath.name.startswith('test_'):
        return 'tests'
    else:
        return 'core'

def should_include_file(filepath):
    """Проверка, нужно ли включать файл"""
    filename = filepath.name
    
    # Исключаем файлы
    exclude_patterns = [
        '__pycache__',
        '.pyc',
        '.pytest_cache',
        '.git',
        'venv',
        'htmlcov',
        '.coverage',
        'coverage.xml',
        'orchestrator.db',
        '.log',
        '.tar.gz',
        '.html',
        '.txt',
        '.md',
        '.toml',
        '.ini',
        '.sh',
        '.sql',
        '.yml',
        '.yaml',
        '.json'
    ]
    
    for pattern in exclude_patterns:
        if pattern in str(filepath):
            return False
    
    # Включаем только Python файлы
    return filepath.suffix == '.py'

def main():
    project_root = Path('orkestrator-bot')
    output_file = Path('BACKEND_FULL_CODE.md')
    
    # Собираем все Python файлы
    python_files = []
    for root, dirs, files in os.walk(project_root):
        root_path = Path(root)
        for file in files:
            filepath = root_path / file
            if should_include_file(filepath):
                python_files.append(filepath)
    
    # Сортируем файлы по категориям и путям
    python_files.sort(key=lambda x: (get_file_category(x), str(x)))
    
    # Группируем файлы по категориям
    files_by_category = {}
    for filepath in python_files:
        category = get_file_category(filepath)
        if category not in files_by_category:
            files_by_category[category] = []
        files_by_category[category].append(filepath)
    
    # Создаем markdown файл
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Полный код бекенда Orkestrator Bot\n\n")
        f.write("## Содержание\n")
        
        # Генерируем содержание
        category_order = [
            'core',
            'dashboard_backend',
            'auth',
            'db',
            'db_models',
            'db_migrations',
            'schemas',
            'llm_providers',
            'integrations',
            'agents',
            'vcs',
            'tests'
        ]
        
        for i, category in enumerate(category_order, 1):
            if category in files_by_category:
                f.write(f"{i}. [{category.replace('_', ' ').title()}](#{category.replace('_', '-')})\n")
        
        f.write("\n---\n\n")
        
        # Записываем файлы по категориям
        for category in category_order:
            if category in files_by_category and files_by_category[category]:
                f.write(f"## {category.replace('_', ' ').title()}\n\n")
                
                for filepath in files_by_category[category]:
                    relative_path = filepath.relative_to(project_root)
                    f.write(f"### {relative_path}\n\n")
                    f.write("```python\n")
                    
                    content = read_file_content(filepath)
                    f.write(content)
                    
                    if not content.endswith('\n'):
                        f.write('\n')
                    f.write("```\n\n")
        
        f.write("---\n\n")
        f.write(f"## Статистика\n")
        f.write(f"- Всего файлов: {len(python_files)}\n")
        
        for category in category_order:
            if category in files_by_category:
                f.write(f"- Файлов в категории '{category.replace('_', ' ')}': {len(files_by_category[category])}\n")
    
    print(f"Создан файл: {output_file}")
    print(f"Всего обработано файлов: {len(python_files)}")

if __name__ == '__main__':
    main()