#!/usr/bin/env python3
"""
Скрипт для объединения всех файлов фронтенда в один markdown файл
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
    
    if 'dashboard/frontend/src' in filepath_str:
        return 'frontend_src'
    elif 'dashboard/frontend' in filepath_str:
        return 'frontend'
    elif filepath.suffix == '.html':
        return 'html_templates'
    elif filepath.suffix == '.css':
        return 'styles'
    elif filepath.suffix in ['.js', '.jsx', '.ts', '.tsx']:
        return 'javascript'
    else:
        return 'other'

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
        '.md'
    ]
    
    for pattern in exclude_patterns:
        if pattern in str(filepath):
            return False
    
    # Включаем только фронтенд файлы
    allowed_extensions = ['.js', '.jsx', '.ts', '.tsx', '.html', '.css', '.scss']
    return filepath.suffix in allowed_extensions

def main():
    project_root = Path('orkestrator-bot')
    output_file = Path('FRONTEND_FULL_CODE.md')
    
    # Собираем все фронтенд файлы
    frontend_files = []
    for root, dirs, files in os.walk(project_root):
        root_path = Path(root)
        for file in files:
            filepath = root_path / file
            if should_include_file(filepath):
                frontend_files.append(filepath)
    
    # Сортируем файлы по категориям и путям
    frontend_files.sort(key=lambda x: (get_file_category(x), str(x)))
    
    # Группируем файлы по категориям
    files_by_category = {}
    for filepath in frontend_files:
        category = get_file_category(filepath)
        if category not in files_by_category:
            files_by_category[category] = []
        files_by_category[category].append(filepath)
    
    # Создаем markdown файл
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Полный код фронтенда Orkestrator Bot\n\n")
        f.write("## Содержание\n")
        
        # Генерируем содержание
        category_order = [
            'html_templates',
            'frontend_src',
            'frontend',
            'javascript',
            'styles',
            'other'
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
                    
                    # Определяем язык для подсветки синтаксиса
                    if filepath.suffix == '.html':
                        lang = 'html'
                    elif filepath.suffix == '.css':
                        lang = 'css'
                    elif filepath.suffix == '.scss':
                        lang = 'scss'
                    elif filepath.suffix in ['.js', '.jsx']:
                        lang = 'javascript'
                    elif filepath.suffix in ['.ts', '.tsx']:
                        lang = 'typescript'
                    else:
                        lang = 'text'
                    
                    f.write(f"```{lang}\n")
                    
                    content = read_file_content(filepath)
                    f.write(content)
                    
                    if not content.endswith('\n'):
                        f.write('\n')
                    f.write("```\n\n")
        
        f.write("---\n\n")
        f.write(f"## Статистика\n")
        f.write(f"- Всего файлов: {len(frontend_files)}\n")
        
        for category in category_order:
            if category in files_by_category:
                f.write(f"- Файлов в категории '{category.replace('_', ' ')}': {len(files_by_category[category])}\n")
    
    print(f"Создан файл: {output_file}")
    print(f"Всего обработано файлов: {len(frontend_files)}")

if __name__ == '__main__':
    main()