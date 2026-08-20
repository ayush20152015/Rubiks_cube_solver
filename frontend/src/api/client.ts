import axios from 'axios'
import { UploadResponse, SolutionResponse } from '../types/index'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const uploadFaceImage = async (
  file: File,
  faceId: number
): Promise<UploadResponse> => {
  const formData = new FormData()
  formData.append('image', file)
  formData.append('face_id', String(faceId))

  const response = await axios.post(`${API_URL}/api/v1/cube/upload-face`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return response.data
}

export const solveCube = async (): Promise<SolutionResponse> => {
  const response = await api.post('/api/v1/cube/solve')
  return response.data
}

export const resetCube = async (): Promise<{ message: string }> => {
  const response = await api.post('/api/v1/cube/reset')
  return response.data
}

export const getCubeState = async (): Promise<{ cube_state: any }> => {
  const response = await api.get('/api/v1/cube/state')
  return response.data
}
