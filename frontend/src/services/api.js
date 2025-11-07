import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const checkHealth = async () => {
  const response = await api.get('/health')
  return response.data
}

export const sendChatMessage = async (message, conversationId = null) => {
  const response = await api.post('/chat', {
    message,
    conversation_id: conversationId,
  })
  return response.data
}

export const uploadDocument = async (file) => {
  const formData = new FormData()
  formData.append('file', file)
  const response = await api.post('/documents/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
  return response.data
}

export const listDocuments = async () => {
  const response = await api.get('/documents')
  return response.data
}

export const deleteDocument = async (documentId) => {
  const response = await api.delete(`/documents/${documentId}`)
  return response.data
}

export const reindexDocuments = async () => {
  const response = await api.post('/documents/reindex')
  return response.data
}

