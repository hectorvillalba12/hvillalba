# schemas.py
from typing import Literal

from pydantic import BaseModel, ConfigDict, field_validator

Priority = Literal["alta", "media", "baja"]


class TaskBase(BaseModel):
    title: str
    description: str | None = None
    completed: bool = False
    priority: Priority = "media"

    @field_validator("title")
    @classmethod
    def title_not_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("El título no puede estar vacío")
        if len(value) > 100:
            raise ValueError("El título no puede superar los 100 caracteres")
        return value


class TaskCreate(TaskBase):
    pass


# NUEVO: para actualizaciones parciales (PATCH), todos los campos son opcionales
class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    completed: bool | None = None
    priority: Priority | None = None

    @field_validator("title")
    @classmethod
    def title_not_blank(cls, value: str | None) -> str | None:
        if value is None:
            return value
        value = value.strip()
        if not value:
            raise ValueError("El título no puede estar vacío")
        if len(value) > 100:
            raise ValueError("El título no puede superar los 100 caracteres")
        return value


class TaskResponse(TaskBase):
    id: int

    # Configuración para permitir la lectura de modelos ORM directamente (equivalente a orm_mode en v1)
    model_config = ConfigDict(from_attributes=True)