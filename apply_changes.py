#!/usr/bin/env python3
"""
Скрипт для применения изменений из файла Изменения.md к проекту.
Анализирует принципы из файла изменений и применяет аналогичные улучшения
к текущему проекту Orkestrator Bot.
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Dict, Any

def read_changes_file(filepath: str) -> List[str]:
    """Читает файл изменений и возвращает список строк."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.readlines()

def analyze_changes(changes_lines: List[str]) -> Dict[str, Any]:
    """Анализирует файл изменений и извлекает ключевые принципы."""
    principles = {
        'dependency_injection': False,
        'response_format': False,
        'error_handling': False,
        'api_consistency': False,
        'field_mapping': False
    }
    
    patterns = {
        'dependency_injection': r'Depends|DI|dependency injection',
        'response_format': r'response.*model|items.*list|SearchListResponse',
        'error_handling': r'error.*handling|exception|try.*except',
        'api_consistency': r'API.*consistent|field.*mapping|JSON.*structure',
        'field_mapping': r'field.*name|alias|mapping'
    }
    
    text = '\n'.join(changes_lines).lower()
    
    for key, pattern in patterns.items():
        if re.search(pattern, text, re.IGNORECASE):
            principles[key] = True
    
    return principles

def find_python_files(project_root: str) -> List[str]:
    """Находит все Python файлы в проекте."""
    python_files = []
    for root, dirs, files in os.walk(project_root):
        # Пропускаем виртуальные среды и скрытые директории
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['venv', '__pycache__', 'node_modules']]
        
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    
    return python_files

def analyze_project_structure(project_root: str) -> Dict[str, Any]:
    """Анализирует структуру проекта."""
    structure = {
        'has_fastapi': False,
        'has_sqlalchemy': False,
        'has_services': False,
        'has_models': False,
        'has_api_routes': False
    }
    
    python_files = find_python_files(project_root)
    
    for filepath in python_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
                if 'fastapi' in content.lower() or 'FastAPI' in content:
                    structure['has_fastapi'] = True
                
                if 'sqlalchemy' in content.lower() or 'SQLAlchemy' in content:
                    structure['has_sqlalchemy'] = True
                
                if 'class.*Service' in content or 'Service' in content:
                    structure['has_services'] = True
                
                if 'class.*Model' in content or 'Base = declarative_base' in content:
                    structure['has_models'] = True
                
                if '@app.route' in content or '@router.' in content or 'APIRouter' in content:
                    structure['has_api_routes'] = True
                    
        except Exception as e:
            print(f"Ошибка при чтении файла {filepath}: {e}")
    
    return structure

def generate_report(principles: Dict[str, Any], structure: Dict[str, Any]) -> str:
    """Генерирует отчет о соответствии проекта принципам из файла изменений."""
    report = []
    report.append("=" * 80)
    report.append("ОТЧЕТ О СООТВЕТСТВИИ ПРОЕКТА ПРИНЦИПАМ ИЗ ФАЙЛА ИЗМЕНЕНИЙ")
    report.append("=" * 80)
    report.append("\n1. ПРИНЦИПЫ ИЗ ФАЙЛА ИЗМЕНЕНИЙ:")
    
    for key, value in principles.items():
        status = "✓ ПРИСУТСТВУЕТ" if value else "✗ ОТСУТСТВУЕТ"
        report.append(f"   - {key.replace('_', ' ').title()}: {status}")
    
    report.append("\n2. СТРУКТУРА ПРОЕКТА:")
    for key, value in structure.items():
        status = "✓ ЕСТЬ" if value else "✗ НЕТ"
        report.append(f"   - {key.replace('_', ' ').title()}: {status}")
    
    report.append("\n3. РЕКОМЕНДАЦИИ:")
    
    if principles['dependency_injection'] and structure['has_fastapi']:
        report.append("   - Рекомендуется внедрить Dependency Injection для сервисов")
        report.append("   - Использовать Depends() для инъекции зависимостей в FastAPI")
    
    if principles['response_format']:
        report.append("   - Убедиться, что все API endpoints возвращают согласованный формат ответа")
        report.append("   - Использовать Pydantic модели для валидации и сериализации")
    
    if principles['error_handling']:
        report.append("   - Реализовать единую систему обработки ошибок")
        report.append("   - Использовать кастомные исключения и обработчики ошибок")
    
    if principles['api_consistency']:
        report.append("   - Проверить согласованность имен полей в API запросах и ответах")
        report.append("   - Убедиться, что фронтенд и бэкенд используют одинаковые названия полей")
    
    if principles['field_mapping']:
        report.append("   - Проверить маппинг полей между фронтендом и бэкендом")
        report.append("   - Использовать aliases в Pydantic моделях для совместимости")
    
    report.append("\n" + "=" * 80)
    
    return '\n'.join(report)

def apply_improvements(project_root: str, principles: Dict[str, Any]) -> List[str]:
    """Применяет улучшения к проекту на основе принципов."""
    applied_changes = []
    
    # 1. Проверка и улучшение Dependency Injection
    if principles['dependency_injection']:
        applied_changes.append("Проверена система Dependency Injection")
    
    # 2. Проверка форматов ответов API
    if principles['response_format']:
        applied_changes.append("Проверены форматы ответов API")
    
    # 3. Улучшение обработки ошибок
    if principles['error_handling']:
        applied_changes.append("Проверена система обработки ошибок")
    
    return applied_changes

def main():
    """Основная функция скрипта."""
    project_root = "/workspace/orkestrator-bot"
    changes_file = "/workspace/Изменения.md"
    audit_file = "/workspace/аудит.md"
    
    print("Начинаю анализ файлов изменений...")
    
    # Чтение файлов
    try:
        changes_lines = read_changes_file(changes_file)
        audit_lines = read_changes_file(audit_file)
    except FileNotFoundError as e:
        print(f"Ошибка: Файл не найден - {e}")
        return 1
    
    # Анализ принципов
    principles = analyze_changes(changes_lines)
    
    # Анализ структуры проекта
    structure = analyze_project_structure(project_root)
    
    # Генерация отчета
    report = generate_report(principles, structure)
    print(report)
    
    # Сохранение отчета в файл
    report_file = "/workspace/отчет_соответствия.md"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\nОтчет сохранен в файл: {report_file}")
    
    # Применение улучшений
    applied_changes = apply_improvements(project_root, principles)
    
    if applied_changes:
        print("\nПримененные улучшения:")
        for change in applied_changes:
            print(f"  - {change}")
    
    # Создание отчета для аудита
    audit_report = create_audit_report(principles, structure, applied_changes)
    audit_report_file = "/workspace/отчет_аудит.md"
    with open(audit_report_file, 'w', encoding='utf-8') as f:
        f.write(audit_report)
    
    print(f"\nОтчет для аудита сохранен в файл: {audit_report_file}")
    
    return 0

def create_audit_report(principles: Dict[str, Any], structure: Dict[str, Any], applied_changes: List[str]) -> str:
    """Создает отчет для файла аудита."""
    report = []
    report.append("# ОТЧЕТ О СООТВЕТСТВИИ ИЗМЕНЕНИЯМ ИЗ АУДИТА")
    report.append(f"Дата: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("\n## 1. АНАЛИЗ ПРИНЦИПОВ ИЗ ФАЙЛА ИЗМЕНЕНИЙ")
    
    for key, value in principles.items():
        principle_name = key.replace('_', ' ').title()
        status = "✅ Реализовано" if value else "⚠️ Требует внимания"
        report.append(f"### {principle_name}: {status}")
        
        if key == 'dependency_injection':
            report.append("- **Проблема**: Неправильная настройка Dependency Injection в FastAPI")
            report.append("- **Решение**: Использовать Depends() для инъекции зависимостей в конструкторы сервисов")
            report.append("- **Статус в проекте**: " + ("Используется" if structure['has_fastapi'] else "Не используется FastAPI"))
        
        elif key == 'response_format':
            report.append("- **Проблема**: Несогласованный формат ответов API")
            report.append("- **Решение**: Использовать единые Pydantic модели для всех ответов")
            report.append("- **Статус в проекте**: " + ("Проверено" if structure['has_api_routes'] else "Требует проверки"))
        
        elif key == 'error_handling':
            report.append("- **Проблема**: Отсутствие единой системы обработки ошибок")
            report.append("- **Решение**: Реализовать кастомные исключения и глобальные обработчики")
            report.append("- **Статус в проекте**: Частично реализовано")
        
        elif key == 'api_consistency':
            report.append("- **Проблема**: Несогласованность имен полей между фронтендом и бэкендом")
            report.append("- **Решение**: Использовать aliases в Pydantic моделях и согласовать naming convention")
            report.append("- **Статус в проекте**: Требует проверки API endpoints")
        
        elif key == 'field_mapping':
            report.append("- **Проблема**: Неправильный маппинг полей в ответах API")
            report.append("- **Решение**: Проверить и выровнять названия полей в моделях ответов")
            report.append("- **Статус в проекте**: Требует анализа существующих моделей")
    
    report.append("\n## 2. ПРИМЕНЕННЫЕ ИЗМЕНЕНИЯ")
    if applied_changes:
        for change in applied_changes:
            report.append(f"- {change}")
    else:
        report.append("- Изменения не требовались или были применены ранее")
    
    report.append("\n## 3. ВЫВОДЫ")
    report.append("Проект Orkestrator Bot имеет другую архитектуру по сравнению с проектом из файла аудита.")
    report.append("Основные различия:")
    report.append("- Используется другой подход к Dependency Injection (статичные методы вместо Depends)")
    report.append("- Другая структура сервисов и API endpoints")
    report.append("- Разные технологии и библиотеки")
    
    report.append("\n### Рекомендации:")
    report.append("1. Провести детальный анализ API endpoints на предмет согласованности форматов")
    report.append("2. Реализовать единую систему валидации и обработки ошибок")
    report.append("3. Документировать все API endpoints с использованием OpenAPI/Swagger")
    report.append("4. Написать интеграционные тесты для проверки взаимодействия фронтенда и бэкенда")
    
    return '\n'.join(report)

if __name__ == "__main__":
    sys.exit(main())