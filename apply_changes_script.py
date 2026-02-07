#!/usr/bin/env python3
"""
Скрипт для применения изменений из файла Изменения.md к проекту.
Парсит файл изменений и применяет патчи к соответствующим файлам.
"""

import os
import re
import sys
from pathlib import Path

def parse_changes_file(file_path):
    """
    Парсит файл изменений и возвращает список изменений.
    Формат файла:
    filename (description)
    Function: function_name
    Old Code: (description)
    код...
    New Code: (description)
    код...
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    changes = []
    
    # Регулярное выражение для поиска блоков изменений
    # Ищем паттерн: filename (description)\nFunction: function_name\nOld Code:...
    pattern = r'([^\n]+)\s+\(([^)]+)\)\s*\nFunction:\s*([^\n]+)\s*\nOld Code:\s*\(([^)]+)\)\s*\n(.*?)\nNew Code:\s*\(([^)]+)\)\s*\n(.*?)(?=\n[^\n]+\s+\(|$)'
    
    matches = re.findall(pattern, content, re.DOTALL)
    
    for match in matches:
        filename, description, function_name, old_desc, old_code, new_desc, new_code = match
        
        # Очистка кода от лишних пробелов
        old_code = old_code.strip()
        new_code = new_code.strip()
        
        changes.append({
            'filename': filename.strip(),
            'description': description.strip(),
            'function_name': function_name.strip(),
            'old_code': old_code,
            'new_code': new_code
        })
    
    # Если регулярное выражение не нашло совпадений, попробуем другой подход
    if not changes:
        # Разделим файл по строкам и попробуем найти изменения вручную
        lines = content.split('\n')
        i = 0
        while i < len(lines):
            line = lines[i]
            if '(' in line and ')' in line and ('tsx' in line or 'ts' in line or 'js' in line or 'jsx' in line):
                # Нашли начало блока с файлом
                filename_desc = line.strip()
                # Извлекаем имя файла (до первой скобки)
                filename = filename_desc.split('(')[0].strip()
                
                # Ищем Function:
                i += 1
                while i < len(lines) and not lines[i].startswith('Function:'):
                    i += 1
                
                if i < len(lines):
                    function_name = lines[i].replace('Function:', '').strip()
                    
                    # Ищем Old Code:
                    i += 1
                    while i < len(lines) and not lines[i].startswith('Old Code:'):
                        i += 1
                    
                    if i < len(lines):
                        old_desc = lines[i].replace('Old Code:', '').strip()
                        
                        # Собираем старый код
                        i += 1
                        old_code_lines = []
                        while i < len(lines) and not lines[i].startswith('New Code:'):
                            old_code_lines.append(lines[i])
                            i += 1
                        
                        old_code = '\n'.join(old_code_lines).strip()
                        
                        # Ищем New Code:
                        if i < len(lines):
                            new_desc = lines[i].replace('New Code:', '').strip()
                            
                            # Собираем новый код
                            i += 1
                            new_code_lines = []
                            while i < len(lines) and not (lines[i] and '(' in lines[i] and ')' in lines[i] and ('tsx' in lines[i] or 'ts' in lines[i] or 'js' in lines[i] or 'jsx' in lines[i])):
                                new_code_lines.append(lines[i])
                                i += 1
                            
                            new_code = '\n'.join(new_code_lines).strip()
                            
                            changes.append({
                                'filename': filename,
                                'description': filename_desc.split('(')[1].split(')')[0].strip() if '(' in filename_desc and ')' in filename_desc else '',
                                'function_name': function_name,
                                'old_code': old_code,
                                'new_code': new_code
                            })
                            continue
            i += 1
    
    return changes

def find_file_in_project(filename, project_root):
    """
    Ищет файл в проекте по имени.
    Возвращает полный путь к файлу или None если не найден.
    """
    # Удаляем префикс frontend/src/ если он есть
    if filename.startswith('frontend/src/'):
        filename = filename.replace('frontend/src/', '')
    
    # Ищем файл в проекте
    for root, dirs, files in os.walk(project_root):
        # Пропускаем node_modules и другие служебные директории
        if 'node_modules' in root or '.git' in root:
            continue
        
        for file in files:
            if file == os.path.basename(filename) or file.endswith(os.path.basename(filename)):
                return os.path.join(root, file)
    
    return None

def apply_change(change, project_root):
    """
    Применяет одно изменение к файлу.
    """
    filename = change['filename']
    old_code = change['old_code']
    new_code = change['new_code']
    
    print(f"\nПрименение изменения для файла: {filename}")
    print(f"Функция: {change['function_name']}")
    print(f"Описание: {change['description']}")
    
    # Находим файл в проекте
    file_path = find_file_in_project(filename, project_root)
    
    if not file_path:
        print(f"❌ Файл не найден: {filename}")
        # Попробуем найти по частичному совпадению
        possible_files = []
        for root, dirs, files in os.walk(project_root):
            if 'node_modules' in root or '.git' in root:
                continue
            for file in files:
                if filename in file or os.path.basename(filename) in file:
                    possible_files.append(os.path.join(root, file))
        
        if possible_files:
            print(f"Возможные файлы:")
            for pf in possible_files:
                print(f"  - {pf}")
            # Используем первый найденный файл
            file_path = possible_files[0]
            print(f"Используем: {file_path}")
        else:
            return False
    
    # Читаем содержимое файла
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Ошибка чтения файла {file_path}: {e}")
        return False
    
    # Проверяем, есть ли старый код в файле
    if old_code in content:
        # Заменяем старый код на новый
        new_content = content.replace(old_code, new_code)
        
        # Записываем изменения
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"✅ Изменение успешно применено к {file_path}")
            return True
        except Exception as e:
            print(f"❌ Ошибка записи файла {file_path}: {e}")
            return False
    else:
        print(f"⚠️ Старый код не найден в файле {file_path}")
        print(f"Ищем частичное совпадение...")
        
        # Попробуем найти частичное совпадение
        old_lines = old_code.split('\n')
        if len(old_lines) > 3:
            # Ищем первые 3 строки
            search_pattern = '\n'.join(old_lines[:3])
            if search_pattern in content:
                print(f"Найдено частичное совпадение (первые 3 строки)")
                # Заменяем найденную часть
                new_content = content.replace(search_pattern, '\n'.join(new_code.split('\n')[:3]))
                try:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"✅ Частичное изменение применено к {file_path}")
                    return True
                except Exception as e:
                    print(f"❌ Ошибка записи файла {file_path}: {e}")
                    return False
        
        print(f"❌ Не удалось найти код для замены")
        return False

def main():
    project_root = '/workspace/orkestrator-bot'
    changes_file = '/workspace/Изменения.md'
    
    print("=" * 80)
    print("Скрипт применения изменений из файла Изменения.md")
    print("=" * 80)
    
    # Парсим файл изменений
    print(f"\nПарсинг файла изменений: {changes_file}")
    changes = parse_changes_file(changes_file)
    
    if not changes:
        print("❌ Не удалось распарсить изменения из файла")
        return 1
    
    print(f"Найдено {len(changes)} изменений")
    
    # Применяем изменения
    successful = 0
    failed = 0
    
    for i, change in enumerate(changes, 1):
        print(f"\n[{i}/{len(changes)}] ", end='')
        if apply_change(change, project_root):
            successful += 1
        else:
            failed += 1
    
    print("\n" + "=" * 80)
    print(f"Итог: успешно применено {successful} изменений, не удалось {failed}")
    print("=" * 80)
    
    return 0 if failed == 0 else 1

if __name__ == '__main__':
    sys.exit(main())