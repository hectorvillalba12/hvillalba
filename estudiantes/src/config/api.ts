import Constants from 'expo-constants';
import { Platform } from 'react-native';

const API_PORT = 80;

// Si la detección automática no te funciona, poné acá la IP de tu PC.
// Ejemplo: 'http://192.168.0.15:8000'
const MANUAL_API_URL = '';

function resolveApiUrl(): string {
  if (MANUAL_API_URL) return MANUAL_API_URL;

  // Expo sabe la IP de tu PC (ej: "192.168.0.15:8081"); le cambiamos el puerto al del back
  const host = Constants.expoConfig?.hostUri?.split(':')[0];
  //if (host) return `http://${host}:${API_PORT}`;
  // Fallback: emulador Android usa 10.0.2.2 para llegar a la PC
  return Platform.OS === 'android'
    ? `http://10.0.2.2:${API_PORT}`
  // : `http://localhost:${API_PORT}`;
      : `https://api.montenegroariel.com.ar/tasks/`
}

export const API_URL = `https://api.montenegroariel.com.ar`;//resolveApiUrl();
export const REQUEST_TIMEOUT_MS = 10000;