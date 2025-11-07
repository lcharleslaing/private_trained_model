import { useState, useRef, useEffect } from 'react'
import { sendChatMessage } from '../services/api'

function ChatInterface() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [conversationId, setConversationId] = useState(null)
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSend = async (e) => {
    e.preventDefault()
    if (!input.trim() || loading) return

    const userMessage = input.trim()
    setInput('')
    setLoading(true)

    // Add user message to UI
    const newUserMessage = {
      role: 'user',
      content: userMessage,
      sources: [],
    }
    setMessages((prev) => [...prev, newUserMessage])

    try {
      const response = await sendChatMessage(userMessage, conversationId)
      
      // Update conversation ID
      if (response.conversation_id) {
        setConversationId(response.conversation_id)
      }

      // Add assistant response
      const assistantMessage = {
        role: 'assistant',
        content: response.response,
        sources: response.sources || [],
      }
      setMessages((prev) => [...prev, assistantMessage])
    } catch (error) {
      console.error('Error sending message:', error)
      const errorMessage = {
        role: 'assistant',
        content: `Error: ${error.response?.data?.detail || error.message}`,
        sources: [],
        isError: true,
      }
      setMessages((prev) => [...prev, errorMessage])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex flex-col h-[calc(100vh-200px)]">
      <div className="card bg-base-100 shadow-xl flex-1 flex flex-col">
        <div className="card-body flex-1 overflow-y-auto">
          {messages.length === 0 && (
            <div className="text-center text-base-content/60 py-8">
              <p className="text-lg mb-2">Welcome to Private GPT-OSS Chat</p>
              <p className="text-sm">Start a conversation by typing a message below.</p>
              <p className="text-xs mt-2">Your documents will be used to provide context-aware responses.</p>
            </div>
          )}

          {messages.map((message, index) => (
            <div
              key={index}
              className={`chat ${message.role === 'user' ? 'chat-end' : 'chat-start'} mb-4`}
            >
              <div className="chat-header">
                {message.role === 'user' ? 'You' : 'Assistant'}
              </div>
              <div
                className={`chat-bubble ${
                  message.role === 'user'
                    ? 'chat-bubble-primary'
                    : message.isError
                    ? 'chat-bubble-error'
                    : 'chat-bubble-secondary'
                }`}
              >
                {message.content}
              </div>
              {message.sources && message.sources.length > 0 && (
                <div className="chat-footer opacity-70 text-xs mt-1">
                  Sources: {message.sources.join(', ')}
                </div>
              )}
            </div>
          ))}

          {loading && (
            <div className="chat chat-start">
              <div className="chat-header">Assistant</div>
              <div className="chat-bubble chat-bubble-secondary">
                <span className="loading loading-dots loading-sm"></span>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        <div className="card-actions p-4 border-t border-base-300">
          <form onSubmit={handleSend} className="w-full flex gap-2">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type your message..."
              className="input input-bordered flex-1"
              disabled={loading}
            />
            <button
              type="submit"
              className="btn btn-primary"
              disabled={loading || !input.trim()}
            >
              Send
            </button>
          </form>
        </div>
      </div>
    </div>
  )
}

export default ChatInterface

