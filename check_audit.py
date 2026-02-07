#!/usr/bin/env python3
import os
import re

def check_audit_compliance():
    """Check if changes comply with audit requirements"""
    base_dir = '/workspace/orkestrator-bot/dashboard/frontend'
    
    print("=== АУДИТ СООТВЕТСТВИЯ ИЗМЕНЕНИЙ ===\n")
    
    # 1. Проверка ProjectTree.tsx
    print("1. ProjectTree.tsx - исправление загрузки данных дерева проекта:")
    project_tree_file = os.path.join(base_dir, 'src/components/ProjectTree.tsx')
    with open(project_tree_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'data.cycles = response.data.cycles' in content:
        print("   ✓ Исправлена загрузка данных дерева (комбинирование списков)")
    else:
        print("   ✗ Не исправлена загрузка данных дерева")
    
    # 2. Проверка ProjectDetails.tsx
    print("\n2. ProjectDetails.tsx - добавление функциональности создания циклов/эпох/эпиков/задач:")
    project_details_file = os.path.join(base_dir, 'src/pages/ProjectDetails.tsx')
    with open(project_details_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    checks = [
        ('handleNewCycle', 'Функция создания нового цикла'),
        ('handleNodeAction', 'Функция обработки действий с узлами дерева'),
        ('setTreeKey(prev => prev + 1)', 'Обновление ключа дерева для перезагрузки'),
        ('onClick={handleNewCycle}', 'Кнопка New Cycle с обработчиком'),
        ('onNodeAction={handleNodeAction}', 'Обработчик действий для дерева проектов')
    ]
    
    for check, description in checks:
        if check in content:
            print(f"   ✓ {description}")
        else:
            print(f"   ✗ {description}")
    
    # 3. Проверка AdminTeams.tsx
    print("\n3. AdminTeams.tsx - подключение к реальному API, валидация форм, тосты:")
    admin_teams_file = os.path.join(base_dir, 'src/pages/AdminTeams.tsx')
    with open(admin_teams_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'import { adminApi }' in content:
        print("   ✓ Добавлен импорт adminApi")
    else:
        print("   ✗ Отсутствует импорт adminApi")
    
    if 'import { toast }' in content:
        print("   ✓ Добавлен импорт toast")
    else:
        print("   ✗ Отсутствует импорт toast")
    
    # 4. Проверка AdminUsers.tsx
    print("\n4. AdminUsers.tsx - бейджи статусов:")
    admin_users_file = os.path.join(base_dir, 'src/pages/AdminUsers.tsx')
    with open(admin_users_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'import StatusBadge' in content:
        print("   ✓ Добавлен импорт StatusBadge")
    else:
        print("   ✗ Отсутствует импорт StatusBadge")
    
    if '<StatusBadge status={user.is_active' in content:
        print("   ✓ Использован StatusBadge для отображения статуса")
    else:
        print("   ✗ Не используется StatusBadge")
    
    # 5. Проверка Breadcrumbs
    print("\n5. Breadcrumbs - навигационные цепочки:")
    breadcrumbs_file = os.path.join(base_dir, 'src/components/common/Breadcrumbs.tsx')
    if os.path.exists(breadcrumbs_file):
        print("   ✓ Компонент Breadcrumbs создан")
    else:
        print("   ✗ Компонент Breadcrumbs не создан")
    
    admin_layout_file = os.path.join(base_dir, 'src/components/AdminLayout.tsx')
    if os.path.exists(admin_layout_file):
        with open(admin_layout_file, 'r', encoding='utf-8') as f:
            content = f.read()
        if 'import { Breadcrumbs }' in content:
            print("   ✓ Breadcrumbs импортирован в AdminLayout")
        else:
            print("   ✗ Breadcrumbs не импортирован в AdminLayout")
        
        if '<Breadcrumbs />' in content:
            print("   ✓ Breadcrumbs добавлен в разметку AdminLayout")
        else:
            print("   ✗ Breadcrumbs не добавлен в разметку AdminLayout")
    
    # 6. Проверка StatusBadge
    print("\n6. StatusBadge - компонент цветных бейджей статусов:")
    status_badge_file = os.path.join(base_dir, 'src/components/common/StatusBadge.tsx')
    if os.path.exists(status_badge_file):
        print("   ✓ Компонент StatusBadge создан")
    else:
        print("   ✗ Компонент StatusBadge не создан")
    
    # 7. Проверка App.tsx
    print("\n7. App.tsx - маршрутизация для просмотра пайплайнов:")
    app_file = os.path.join(base_dir, 'src/App.tsx')
    with open(app_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'path="/pipelines/:id"' in content:
        print("   ✓ Добавлен маршрут для пайплайнов")
    else:
        print("   ✗ Отсутствует маршрут для пайплайнов")
    
    # 8. Проверка MainApp.tsx
    print("\n8. MainApp.tsx - polling для обновления статуса пайплайнов:")
    main_app_file = os.path.join(base_dir, 'src/MainApp.tsx')
    with open(main_app_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'setInterval(fetchDetails, 2000)' in content:
        print("   ✓ Реализован polling для обновления статуса (2 секунды)")
    else:
        print("   ✗ Отсутствует polling для обновления статуса")
    
    # 9. Проверка соответствия аудиту
    print("\n=== СООТВЕТСТВИЕ ТРЕБОВАНИЯМ АУДИТА ===")
    
    audit_file = '/workspace/аудит.md'
    with open(audit_file, 'r', encoding='utf-8') as f:
        audit_content = f.read()
    
    # Извлечение ключевых требований из аудита
    requirements = [
        ("валидация форм", "Валидация форм на клиенте"),
        ("хлебные крошки", "Хлебные крошки для навигации"),
        ("цветные бейджи статусов", "Цветные бейджи для статусов"),
        ("toast уведомления", "Toast уведомления о результатах действий"),
        ("реальный API", "Использование реального API вместо моков"),
        ("polling статуса", "Polling для обновления статуса пайплайнов"),
        ("маршрутизация пайплайнов", "Корректная маршрутизация для пайплайнов")
    ]
    
    implemented = 0
    total = len(requirements)
    
    for req_key, req_desc in requirements:
        if req_key in audit_content.lower():
            # Проверяем, реализовано ли это
            if req_key == "валидация форм":
                # Проверяем AdminTeams.tsx
                with open(admin_teams_file, 'r', encoding='utf-8') as f:
                    teams_content = f.read()
                if 'if (!formData.name.trim())' in teams_content:
                    print(f"   ✓ {req_desc} - частично реализовано (AdminTeams)")
                    implemented += 1
                else:
                    print(f"   ⚠ {req_desc} - требует доработки")
            elif req_key == "хлебные крошки":
                if os.path.exists(breadcrumbs_file):
                    print(f"   ✓ {req_desc} - реализовано")
                    implemented += 1
                else:
                    print(f"   ✗ {req_desc} - не реализовано")
            elif req_key == "цветные бейджи статусов":
                if os.path.exists(status_badge_file):
                    print(f"   ✓ {req_desc} - реализовано")
                    implemented += 1
                else:
                    print(f"   ✗ {req_desc} - не реализовано")
            elif req_key == "toast уведомления":
                if 'import { toast }' in content or 'window.showToast' in content:
                    print(f"   ✓ {req_desc} - частично реализовано")
                    implemented += 1
                else:
                    print(f"   ⚠ {req_desc} - требует доработки")
            elif req_key == "реальный api":
                if 'adminApi.get' in content or 'axios.get' in content:
                    print(f"   ✓ {req_desc} - реализовано")
                    implemented += 1
                else:
                    print(f"   ✗ {req_desc} - не реализовано")
            elif req_key == "polling статуса":
                if 'setInterval(fetchDetails, 2000)' in content:
                    print(f"   ✓ {req_desc} - реализовано")
                    implemented += 1
                else:
                    print(f"   ✗ {req_desc} - не реализовано")
            elif req_key == "маршрутизация пайплайнов":
                if 'path="/pipelines/:id"' in content:
                    print(f"   ✓ {req_desc} - реализовано")
                    implemented += 1
                else:
                    print(f"   ✗ {req_desc} - не реализовано")
    
    print(f"\nИтого: {implemented}/{total} требований аудита выполнено")
    
    if implemented >= total * 0.7:
        print("\n✅ Основные требования аудита выполнены")
    else:
        print("\n⚠ Требуется доработка для полного соответствия аудиту")

if __name__ == '__main__':
    check_audit_compliance()