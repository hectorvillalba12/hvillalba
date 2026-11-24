# main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import engine, Base, get_db
from models import TaskModel
from schemas import TaskCreate, TaskResponse, TaskUpdate

# Evento de inicio para crear las tablas automáticamente
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        # Migración mínima: si test.db ya existía sin la columna "priority", la agrega
        columns = await conn.execute(text("PRAGMA table_info(tasks)"))
        names = [row[1] for row in columns.fetchall()]
        if "priority" not in names:
            await conn.execute(
                text("ALTER TABLE tasks ADD COLUMN priority VARCHAR(10) NOT NULL DEFAULT 'media'")
            )
    yield

app = FastAPI(
    title="FastAPI con SQLAlchemy 2.0",
    description="Ejemplo práctico de integración asíncrona",
    version="1.0.0",
    lifespan=lifespan
)

# CORS: necesario si abrís el front en navegador (Expo web). La app nativa no lo requiere.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. Crear una Tarea (CREATE)
@app.post("/tasks/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreate, db: AsyncSession = Depends(get_db)):
    db_task = TaskModel(
        title=task.title,
        description=task.description,
        completed=task.completed,
        priority=task.priority,
    )
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task

# 2. Listar Tareas (READ - List)
@app.get("/tasks/", response_model=list[TaskResponse])
async def read_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(TaskModel).order_by(TaskModel.id.desc()).offset(skip).limit(limit)
    )
    tasks = result.scalars().all()
    return list(tasks)

# 3. Obtener una Tarea por ID (READ - Detail)
@app.get("/tasks/{task_id}", response_model=TaskResponse)
async def read_task(task_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TaskModel).where(TaskModel.id == task_id))
    task = result.scalars().first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada")
    return task

# 4. Actualizar una Tarea (UPDATE)
@app.put("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(task_id: int, task_data: TaskCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TaskModel).where(TaskModel.id == task_id))
    task = result.scalars().first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada")
    
    task.title = task_data.title
    task.description = task_data.description
    task.completed = task_data.completed
    task.priority = task_data.priority
    
    await db.commit()
    await db.refresh(task)
    return task

# 4b. Actualizar parcialmente una Tarea (PATCH) - el front lo usa para completar/descompletar
@app.patch("/tasks/{task_id}", response_model=TaskResponse)
async def patch_task(task_id: int, task_data: TaskUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TaskModel).where(TaskModel.id == task_id))
    task = result.scalars().first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada")

    for field, value in task_data.model_dump(exclude_unset=True).items():
        setattr(task, field, value)

    await db.commit()
    await db.refresh(task)
    return task

# 5. Eliminar una Tarea (DELETE)
@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TaskModel).where(TaskModel.id == task_id))
    task = result.scalars().first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada")
    
    await db.delete(task)
    await db.commit()
    return None