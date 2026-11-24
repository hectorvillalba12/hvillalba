import { API_URL, REQUEST_TIMEOUT_MS } from '../config/api';
import type { Task, TaskPriority } from '../types/task';

// Forma de la tarea tal como la devuelve el backend FastAPI
type ApiTask = {
  id: number;
  title: string;
  description: string | null;
  completed: boolean;
  priority: TaskPriority;
};

function fromApi(task: ApiTask): Task {
  return {
    id: String(task.id), // el front trabaja con ids string
    title: task.title,
    description: task.description ?? '',
    priority: task.priority,
    completed: task.completed,
  };
}

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);
  try {
    const response = await fetch(`${API_URL}${path}`, {
      ...options,
      headers: { 'Content-Type': 'application/json', ...(options.headers ?? {}) },
      signal: controller.signal,
    });
    if (!response.ok) {
      let detail = '';
      try {
        const body = await response.json();
        detail = typeof body.detail === 'string' ? body.detail : JSON.stringify(body.detail);
      } catch {
        // la respuesta no tenía cuerpo JSON
      }
      throw new Error(`HTTP ${response.status}${detail ? `: ${detail}` : ''}`);
    }
    if (response.status === 204) return undefined as T;
    return (await response.json()) as T;
  } catch (caught) {
    if (caught instanceof Error && caught.name === 'AbortError') {
      throw new Error('Tiempo de espera agotado: el servidor no respondió.');
    }
    throw caught;
  } finally {
    clearTimeout(timer);
  }
}

// Mantiene el botón «Simular error API» del laboratorio
export async function fetchTasks(simulateFailure = false): Promise<Task[]> {
  if (simulateFailure) {
    throw new Error('HTTP 503: servidor temporalmente indisponible (simulado)');
  }
  const records = await request<ApiTask[]>('/tasks/?limit=200');
  return records.map(fromApi);
}

export async function createTask(
  input: { title: string; description?: string; priority?: TaskPriority },
): Promise<Task> {
  const created = await request<ApiTask>('/tasks/', {
    method: 'POST',
    body: JSON.stringify({
      title: input.title,
      description: input.description ?? null,
      priority: input.priority ?? 'media',
      completed: false,
    }),
  });
  return fromApi(created);
}

export async function setTaskCompleted(id: string, completed: boolean): Promise<Task> {
  const updated = await request<ApiTask>(`/tasks/${id}`, {
    method: 'PATCH',
    body: JSON.stringify({ completed }),
  });
  return fromApi(updated);
}

export async function removeTask(id: string): Promise<void> {
  await request<void>(`/tasks/${id}`, { method: 'DELETE' });
}