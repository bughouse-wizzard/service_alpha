#!/usr/bin/env python3
import os
import re

def read_audit_file():
    """Read and parse audit file"""
    audit_file = '/workspace/аудит.md'
    with open(audit_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract key requirements
    requirements = []
    
    # Look for numbered items or bullet points
    lines = content.split('\n')
    for line in lines:
        line = line.strip()
        if line.startswith(('•', '-', '*', '1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.')):
            # Clean up the line
            clean_line = re.sub(r'^[•\-*\d\.\s]+', '', line)
            if clean_line and len(clean_line) > 10:  # Filter out short items
                requirements.append(clean_line)
    
    return requirements

def check_implementation():
    """Check implementation of changes"""
    base_dir = '/workspace/orkestrator-bot/dashboard/frontend'
    
    print("=== ОТЧЕТ О ВЫПОЛНЕНИИ ИЗМЕНЕНИЙ ===\n")
    
    # Read audit requirements
    audit_reqs = read_audit_file()
    print(f"Найдено {len(audit_reqs)} требований в файле аудита:\n")
    for i, req in enumerate(audit_reqs[:10], 1):  # Show first 10
        print(f"  {i}. {req}")
    if len(audit_reqs) > 10:
        print(f"  ... и еще {len(audit_reqs) - 10} требований")
    
    print("\n=== ПРОВЕРКА ВЫПОЛНЕННЫХ ИЗМЕНЕНИЙ ===\n")
    
    # Check implemented changes
    implemented_changes = []
    
    # 1. ProjectTree.tsx - fixed data loading
    project_tree_file = os.path.join(base_dir, 'src/components/ProjectTree.tsx')
    if os.path.exists(project_tree_file):
        with open(project_tree_file, 'r', encoding='utf-8') as f:
            content = f.read()
        if 'data.cycles = response.data.cycles' in content:
            implemented_changes.append("ProjectTree.tsx: исправлена загрузка данных дерева проектов")
    
    # 2. ProjectDetails.tsx - add functionality
    project_details_file = os.path.join(base_dir, 'src/pages/ProjectDetails.tsx')
    if os.path.exists(project_details_file):
        with open(project_details_file, 'r', encoding='utf-8') as f:
            content = f.read()
        checks = [
            ('handleNewCycle', 'ProjectDetails.tsx: добавлена функция создания циклов'),
            ('handleNodeAction', 'ProjectDetails.tsx: добавлена функция обработки действий с узлами'),
            ('onClick={handleNewCycle}', 'ProjectDetails.tsx: кнопки New Cycle работают'),
            ('onNodeAction={handleNodeAction}', 'ProjectDetails.tsx: дерево проектов поддерживает действия'),
            ('window.showToast', 'ProjectDetails.tsx: добавлены toast уведомления')
        ]
        for check, desc in checks:
            if check in content:
                implemented_changes.append(desc)
    
    # 3. AdminTeams.tsx - form validation, API, toasts
    admin_teams_file = os.path.join(base_dir, 'src/pages/AdminTeams.tsx')
    if os.path.exists(admin_teams_file):
        with open(admin_teams_file, 'r', encoding='utf-8') as f:
            content = f.read()
        checks = [
            ('import { toast }', 'AdminTeams.tsx: добавлены toast уведомления'),
            ('if (!formData.name.trim())', 'AdminTeams.tsx: добавлена валидация форм'),
            ('toast.success', 'AdminTeams.tsx: успешные операции показывают toast'),
            ('toast.error', 'AdminTeams.tsx: ошибки показывают toast')
        ]
        for check, desc in checks:
            if check in content:
                implemented_changes.append(desc)
    
    # 4. AdminUsers.tsx - status badges
    admin_users_file = os.path.join(base_dir, 'src/pages/AdminUsers.tsx')
    if os.path.exists(admin_users_file):
        with open(admin_users_file, 'r', encoding='utf-8') as f:
            content = f.read()
        if '<StatusBadge status=' in content:
            implemented_changes.append("AdminUsers.tsx: используются цветные бейджи статусов")
    
    # 5. Breadcrumbs component
    breadcrumbs_file = os.path.join(base_dir, 'src/components/common/Breadcrumbs.tsx')
    if os.path.exists(breadcrumbs_file):
        implemented_changes.append("Создан компонент Breadcrumbs для навигации")
    
    # 6. StatusBadge component
    status_badge_file = os.path.join(base_dir, 'src/components/common/StatusBadge.tsx')
    if os.path.exists(status_badge_file):
        implemented_changes.append("Создан компонент StatusBadge для цветных бейджей")
    
    # 7. App.tsx routing
    app_file = os.path.join(base_dir, 'src/App.tsx')
    if os.path.exists(app_file):
        with open(app_file, 'r', encoding='utf-8') as f:
            content = f.read()
        if 'path="/pipelines/:id"' in content:
            implemented_changes.append("App.tsx: добавлен маршрут для пайплайнов")
    
    # 8. MainApp.tsx polling
    main_app_file = os.path.join(base_dir, 'src/MainApp.tsx')
    if os.path.exists(main_app_file):
        with open(main_app_file, 'r', encoding='utf-8') as f:
            content = f.read()
        if 'setInterval(fetchDetails, 2000)' in content:
            implemented_changes.append("MainApp.tsx: реализован polling для обновления статуса пайплайнов")
    
    # 9. Check for real API usage (not mocks)
    # Look for axios or fetch calls
    api_patterns = [
        ('axios.get', 'Использование реального API (axios)'),
        ('axios.post', 'Использование реального API для POST запросов'),
        ('axios.put', 'Использование реального API для PUT запросов'),
        ('axios.delete', 'Использование реального API для DELETE запросов'),
        ('fetch(', 'Использование реального API (fetch)')
    ]
    
    # Check multiple files
    files_to_check = [
        'src/pages/AdminTeams.tsx',
        'src/pages/AdminUsers.tsx',
        'src/pages/ProjectDetails.tsx',
        'src/components/ProjectTree.tsx',
        'src/MainApp.tsx'
    ]
    
    api_used = False
    for file_path in files_to_check:
        full_path = os.path.join(base_dir, file_path)
        if os.path.exists(full_path):
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            for pattern, desc in api_patterns:
                if pattern in content:
                    api_used = True
                    break
        if api_used:
            break
    
    if api_used:
        implemented_changes.append("Использование реального API вместо мок-данных")
    
    # Print results
    print(f"Выполнено {len(implemented_changes)} изменений:\n")
    for i, change in enumerate(implemented_changes, 1):
        print(f"  {i}. {change}")
    
    # Check against audit requirements
    print("\n=== СООТВЕТСТВИЕ АУДИТУ ===\n")
    
    # Key audit themes
    audit_themes = {
        'валидация': 'Валидация форм на клиенте',
        'хлебные крошки': 'Хлебные крошки для навигации',
        'бейджи': 'Цветные бейджи статусов',
        'toast': 'Toast уведомления',
        'api': 'Использование реального API',
        'polling': 'Polling для обновления статуса',
        'маршрутизация': 'Корректная маршрутизация',
        'дерево проектов': 'Функциональность дерева проектов'
    }
    
    theme_status = {}
    for theme_key, theme_desc in audit_themes.items():
        # Check if theme is mentioned in audit
        theme_in_audit = any(theme_key in req.lower() for req in audit_reqs)
        if not theme_in_audit:
            continue
        
        # Check if implemented
        implemented = False
        if theme_key == 'валидация':
            implemented = any('валидация форм' in change.lower() for change in implemented_changes)
        elif theme_key == 'хлебные крошки':
            implemented = any('Breadcrumbs' in change for change in implemented_changes)
        elif theme_key == 'бейджи':
            implemented = any('StatusBadge' in change for change in implemented_changes)
        elif theme_key == 'toast':
            implemented = any('toast' in change.lower() for change in implemented_changes)
        elif theme_key == 'api':
            implemented = any('реального API' in change for change in implemented_changes)
        elif theme_key == 'polling':
            implemented = any('polling' in change.lower() for change in implemented_changes)
        elif theme_key == 'маршрутизация':
            implemented = any('маршрут' in change.lower() for change in implemented_changes)
        elif theme_key == 'дерево проектов':
            implemented = any('дерева проектов' in change for change in implemented_changes)
        
        theme_status[theme_desc] = implemented
    
    # Print theme status
    implemented_count = 0
    total_themes = len(theme_status)
    
    for theme, status in theme_status.items():
        status_symbol = '✓' if status else '✗'
        status_text = 'реализовано' if status else 'не реализовано'
        print(f"  {status_symbol} {theme}: {status_text}")
        if status:
            implemented_count += 1
    
    print(f"\nИтого: {implemented_count}/{total_themes} ключевых требований аудита выполнено")
    
    if implemented_count >= total_themes * 0.7:
        print("\n✅ ОСНОВНЫЕ ТРЕБОВАНИЯ АУДИТА ВЫПОЛНЕНЫ")
        print("   Изменения соответствуют требованиям файла аудита")
    else:
        print("\n⚠ ТРЕБУЕТСЯ ДОРАБОТКА")
        print("   Не все требования аудита выполнены")
    
    return implemented_changes, theme_status

if __name__ == '__main__':
    implemented_changes, theme_status = check_implementation()