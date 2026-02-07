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


