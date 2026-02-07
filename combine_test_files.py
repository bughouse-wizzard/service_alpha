#!/usr/bin/env python3
"""
Скрипт для объединения всех тестовых файлов в один markdown файл
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
    """Определение категории тестового файла"""
    filepath_str = str(filepath)
    filename = filepath.name
    
    if 'tests/' in filepath_str:
        return 'tests_directory'
    elif filename.startswith('test_'):
        if 'auth' in filename.lower():
            return 'auth_tests'
        elif 'db' in filename.lower() or 'postgres' in filename.lower():
            return 'db_tests'
        elif 'api' in filename.lower():
            return 'api_tests'
        elif 'integration' in filename.lower():
            return 'integration_tests'
        else:
            return 'other_tests'
    else:
        return 'test_helpers'

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
        'node_modules',
        'htmlcov',
        '.coverage',
        'coverage.xml',
        'orchestrator.db',
        '.log',
        '.tar.gz',
        '.toml',
        '.ini',
        '.sh',
        '.sql',
        '.yml',
        '.yaml',
        '.json',
        '.map',
        '.md',
        '.html'
    ]
    
    for pattern in exclude_patterns:
        if pattern in str(filepath):
            return False
    
    # Включаем тестовые файлы
    if filepath.suffix != '.py':
        return False
    
    # Включаем файлы из директории tests или начинающиеся с test_
    return 'tests/' in str(filepath) or filename.startswith('test_')

def main():
    project_root = Path('orkestrator-bot')
    output_file = Path('TESTS_FULL_CODE.md')
    
    # Собираем все тестовые файлы
    test_files = []
    for root, dirs, files in os.walk(project_root):
        root_path = Path(root)
        for file in files:
            filepath = root_path / file
            if should_include_file(filepath):
                test_files.append(filepath)
    
    # Сортируем файлы по категориям и путям
    test_files.sort(key=lambda x: (get_file_category(x), str(x)))
    
    # Группируем файлы по категориям
    files_by_category = {}
    for filepath in test_files:
        category = get_file_category(filepath)
        if category not in files_by_category:
            files_by_category[category] = []
        files_by_category[category].append(filepath)
    
    # Создаем markdown файл
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Полный код тестов Orkestrator Bot\n\n")
        f.write("## Содержание\n")
        
        # Генерируем содержание
        category_order = [
            'tests_directory',
            'auth_tests',
            'db_tests',
            'api_tests',
            'integration_tests',
            'other_tests',
            'test_helpers'
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
        f.write(f"- Всего тестовых файлов: {len(test_files)}\n")
        
        for category in category_order:
            if category in files_by_category:
                f.write(f"- Файлов в категории '{category.replace('_', ' ')}': {len(files_by_category[category])}\n")
        
        # Добавляем информацию о покрытии тестами
        coverage_files = list(project_root.glob('*.coverage')) + list(project_root.glob('coverage.xml'))
        if coverage_files:
            f.write(f"\n## Файлы покрытия тестами\n")
            for cov_file in coverage_files:
                f.write(f"- {cov_file.name}\n")
    
    print(f"Создан файл: {output_file}")
    print(f"Всего обработано тестовых файлов: {len(test_files)}")

if __name__ == '__main__':
    main()