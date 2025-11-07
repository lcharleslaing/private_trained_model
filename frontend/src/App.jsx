import { useState, useEffect, useRef } from 'react'
import ChatInterface from './components/ChatInterface'
import DocumentManager from './components/DocumentManager'
import { checkHealth } from './services/api'

function App() {
  const [isHealthy, setIsHealthy] = useState(false)
  const [ollamaAvailable, setOllamaAvailable] = useState(false)
  const [healthData, setHealthData] = useState(null)
  const [activeTab, setActiveTab] = useState('chat')

  const checkHealthStatus = async () => {
    try {
      const health = await checkHealth()
      setIsHealthy(health.status === 'healthy')
      setOllamaAvailable(health.ollama_available || false)
      setHealthData(health)
    } catch (error) {
      setIsHealthy(false)
      setOllamaAvailable(false)
      setHealthData(null)
    }
  }

  useEffect(() => {
    checkHealthStatus()
    const interval = setInterval(checkHealthStatus, 30000) // Check every 30 seconds
    return () => clearInterval(interval)
  }, [])

  return (
    <div className="min-h-screen bg-base-200">
      <div className="navbar bg-base-100 shadow-lg">
        <div className="flex-1">
          <a className="btn btn-ghost text-xl">Private GPT-OSS Chat</a>
        </div>
        <div className="flex-none">
          <div className="flex items-center gap-2">
            <div className={`badge ${isHealthy ? 'badge-success' : 'badge-error'}`}>
              API {isHealthy ? 'Online' : 'Offline'}
            </div>
            <div className={`badge ${ollamaAvailable ? 'badge-success' : 'badge-warning'}`}>
              Ollama {ollamaAvailable ? 'Connected' : 'Not Connected'}
            </div>
            {healthData?.vision_model_available && (
              <div className="badge badge-info">
                Vision: {healthData.vision_model || 'Available'}
              </div>
            )}
          </div>
        </div>
      </div>

      <div className="container mx-auto p-4">
        <div className="tabs tabs-boxed mb-4">
          <a
            className={`tab ${activeTab === 'chat' ? 'tab-active' : ''}`}
            onClick={() => setActiveTab('chat')}
          >
            Chat
          </a>
          <a
            className={`tab ${activeTab === 'documents' ? 'tab-active' : ''}`}
            onClick={() => setActiveTab('documents')}
          >
            Documents
          </a>
        </div>

        {activeTab === 'chat' && <ChatInterface />}
        {activeTab === 'documents' && <DocumentManager onUpdate={checkHealthStatus} />}
      </div>
    </div>
  )
}

export default App

