import Constants from 'expo-constants';
import { Platform } from 'react-native';

// Cambiá esto según dónde quieras conectarte:
//   'remote' -> https://api.montenegroariel.com.ar (no necesitás levantar FastAPI)
//   'local'  -> tu FastAPI corriendo en tu PC (uvicorn)
const MODE: 'remote' | 'local' = 'remote';

const REMOTE_API_URL = 'https://api.montenegroariel.com.ar';
const LOCAL_API_PORT = 8000;

// Si la detección automática no te funciona en modo local,
// poné acá la IP de tu PC. Ejemplo: 'http://192.168.0.15:8000'
const MANUAL_LOCAL_URL = '';

function resolveLocalUrl(): string {
  if (MANUAL_LOCAL_URL) return MANUAL_LOCAL_URL;

  // Expo conoce la IP de tu PC (ej: "192.168.0.15:8081"); le cambiamos el puerto
  const host = Constants.expoConfig?.hostUri?.split(':')[0];
  if (host) return `http://${host}:${LOCAL_API_PORT}`;

  // Fallback: el emulador de Android llega a tu PC por 10.0.2.2
  return Platform.OS === 'android'
    ? `http://10.0.2.2:${LOCAL_API_PORT}`
    : `http://localhost:${LOCAL_API_PORT}`;
}

export const API_URL = MODE === 'remote' ? REMOTE_API_URL : resolveLocalUrl();
export const REQUEST_TIMEOUT_MS = 10000;