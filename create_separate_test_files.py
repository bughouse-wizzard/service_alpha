#!/usr/bin/env python3
"""
Скрипт для создания отдельных файлов тестов бекенда и фронтенда
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
        with open(filepath, 'r', encoding='latin-1') as f:
            return f.read()
    except Exception as e:
        return f"# Ошибка чтения файла {filepath}: {str(e)}"

def is_backend_test(filepath):
    """Проверка, является ли файл тестом бекенда"""
    return filepath.suffix == '.py' and ('test' in filepath.name.lower() or 'tests/' in str(filepath))

def is_frontend_test(filepath):
    """Проверка, является ли файл тестом фронтенда"""
    frontend_extensions = ['.test.js', '.spec.js', '.test.jsx', '.spec.jsx', '.test.ts', '.spec.ts', '.test.tsx', '.spec.tsx']
    for ext in frontend_extensions:
        if filepath.name.endswith(ext):
            return True
    return False

def should_include_file(filepath):
    """Проверка, нужно ли включать файл"""
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
    
    return is_backend_test(filepath) or is_frontend_test(filepath)

def create_backend_tests_file(project_root, output_file):
    """Создание файла с тестами бекенда"""
    backend_test_files = []
    
    for root, dirs, files in os.walk(project_root):
        root_path = Path(root)
        for file in files:
            filepath = root_path / file
            if is_backend_test(filepath) and should_include_file(filepath):
                backend_test_files.append(filepath)
    
    # Сортируем файлы
    backend_test_files.sort(key=lambda x: str(x))
    
    # Создаем markdown файл
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Тесты бекенда Orkestrator Bot\n\n")
        f.write("## Содержание\n")
        
        # Группируем по категориям
        categories = {}
        for filepath in backend_test_files:
            if 'tests/' in str(filepath):
                category = 'tests_directory'
            elif 'auth' in str(filepath).lower():
                category = 'auth_tests'
            elif 'db' in str(filepath).lower() or 'postgres' in str(filepath).lower():
                category = 'db_tests'
            elif 'api' in str(filepath).lower():
                category = 'api_tests'
            elif 'integration' in str(filepath).lower():
                category = 'integration_tests'
            else:
                category = 'other_tests'
            
            if category not in categories:
                categories[category] = []
            categories[category].append(filepath)
        
        # Записываем содержание
        category_order = ['tests_directory', 'auth_tests', 'db_tests', 'api_tests', 'integration_tests', 'other_tests']
        for i, category in enumerate(category_order, 1):
            if category in categories and categories[category]:
                category_name = category.replace('_', ' ').title()
                f.write(f"{i}. [{category_name}](#{category.replace('_', '-')})\n")
        
        f.write("\n---\n\n")
        
        # Записываем файлы по категориям
        for category in category_order:
            if category in categories and categories[category]:
                category_name = category.replace('_', ' ').title()
                f.write(f"## {category_name}\n\n")
                
                for filepath in categories[category]:
                    relative_path = filepath.relative_to(project_root)
                    f.write(f"### {relative_path}\n\n")
                    
                    f.write("```python\n")
                    content = read_file_content(filepath)
                    f.write(content)
                    
                    if not content.endswith('\n'):
                        f.write('\n')
                    f.write("```\n\n")
        
        f.write("---\n\n")
        f.write(f"## Статистика тестов бекенда\n")
        f.write(f"- Всего тестовых файлов: {len(backend_test_files)}\n")
        
        for category in category_order:
            if category in categories:
                category_name = category.replace('_', ' ').title()
                f.write(f"- Файлов в категории '{category_name}': {len(categories[category])}\n")
    
    print(f"Создан файл: {output_file}")
    print(f"Всего тестовых файлов бекенда: {len(backend_test_files)}")
    return backend_test_files

def create_frontend_tests_file(project_root, output_file):
    """Создание файла с тестами фронтенда"""
    frontend_test_files = []
    
    for root, dirs, files in os.walk(project_root):
        root_path = Path(root)
        for file in files:
            filepath = root_path / file
            if is_frontend_test(filepath) and should_include_file(filepath):
                frontend_test_files.append(filepath)
    
    # Сортируем файлы
    frontend_test_files.sort(key=lambda x: str(x))
    
    # Создаем markdown файл
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Тесты фронтенда Orkestrator Bot\n\n")
        f.write("## Содержание\n")
        
        if not frontend_test_files:
            f.write("## ⚠️ Тесты фронтенда не найдены\n\n")
            f.write("В проекте не обнаружено тестовых файлов фронтенда.\n")
            f.write("Рекомендуется создать тесты для:\n")
            f.write("- Компонентов React\n")
            f.write("- JavaScript функций\n")
            f.write("- Интеграции с API\n")
            f.write("- UI взаимодействий\n")
        else:
            # Группируем по расширениям
            categories = {}
            for filepath in frontend_test_files:
                ext = filepath.suffix
                if ext not in categories:
                    categories[ext] = []
                categories[ext].append(filepath)
            
            # Записываем содержание
            for i, (ext, files) in enumerate(categories.items(), 1):
                ext_name = ext.upper().replace('.', '')
                f.write(f"{i}. [Тесты {ext_name}](#{ext_name.lower()}-tests)\n")
            
            f.write("\n---\n\n")
            
            # Записываем файлы по категориям
            for ext, files in categories.items():
                ext_name = ext.upper().replace('.', '')
                f.write(f"## Тесты {ext_name}\n\n")
                
                for filepath in files:
                    relative_path = filepath.relative_to(project_root)
                    f.write(f"### {relative_path}\n\n")
                    
                    # Определяем язык для подсветки
                    if ext in ['.js', '.jsx']:
                        lang = 'javascript'
                    elif ext in ['.ts', '.tsx']:
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
        f.write(f"## Статистика тестов фронтенда\n")
        f.write(f"- Всего тестовых файлов: {len(frontend_test_files)}\n")
        
        if frontend_test_files:
            for ext, files in categories.items():
                ext_name = ext.upper().replace('.', '')
                f.write(f"- Файлов {ext_name}: {len(files)}\n")
        else:
            f.write("- Тесты не обнаружены, требуется создание\n")
    
    print(f"Создан файл: {output_file}")
    print(f"Всего тестовых файлов фронтенда: {len(frontend_test_files)}")
    return frontend_test_files

def main():
    project_root = Path('orkestrator-bot')
    
    # Создаем файлы
    backend_tests_file = Path('BACKEND_TESTS_FULL.md')
    frontend_tests_file = Path('FRONTEND_TESTS_FULL.md')
    
    print("Создание файлов тестов...")
    print("-" * 50)
    
    backend_files = create_backend_tests_file(project_root, backend_tests_file)
    print("-" * 50)
    frontend_files = create_frontend_tests_file(project_root, frontend_tests_file)
    print("-" * 50)
    
    print("\nИтоговая статистика:")
    print(f"- Тестов бекенда: {len(backend_files)} файлов")
    print(f"- Тестов фронтенда: {len(frontend_files)} файлов")
    print(f"- Всего тестов: {len(backend_files) + len(frontend_files)} файлов")

if __name__ == '__main__':
    main()