import { useState } from 'react'
import type { FormEvent } from 'react'

type Message = {
  id: number
  role: 'user' | 'assistant'
  text: string
}

function App() {
  // States
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault() // stop page reload

    const trimmed = input.trim()
    if (!trimmed) return // ignore empty messages

    const userMessage: Message = {
      id: Date.now(),
      role: 'user',
      text: trimmed,
    }

    // Append new message to list
    setMessages(prev => [...prev, userMessage])
    setInput('')
    setIsLoading(true)

    // Send message to backend
    try{
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: trimmed }),
      })

      if (!res.ok) {
        throw new Error(`Server error! status: ${res.status}`)
      }

      const data: { reply: string } = await res.json()

      // Add LLM's response to messages
      const assistantMessage: Message = {
        id: Date.now() + 1,
        role: 'assistant',
        text: data.reply,
      }
      setMessages(prev => [...prev, assistantMessage])
    } catch (error) {
      console.error('Error during fetch:', error)
      const errorMessage: Message = {
        id: Date.now() + 2,
        role: 'assistant',
        text: "HomeBrain: I hit an error talking to the backend. Check backend logs for more details.",
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div
      style={{
        minHeight: '100vh',
        backgroundColor: '#020617',
        color: '#e5e7eb',
        fontFamily: 'system-ui, -apple-system, BlinkMacSystemFont, sans-serif',
        display: 'flex',
        flexDirection: 'column',
        // ⬇️ extra bottom padding so the input isn't flush with the screen edge
        padding: '1.5rem 1.5rem 3rem',
        boxSizing: 'border-box',
      }}
    >
      {/* Header */}
      <header style={{ marginBottom: '1rem' }}>
        <h1 style={{ fontSize: '1.75rem', marginBottom: '0.25rem' }}>🧠 Homebrain</h1>
        <p style={{ opacity: 0.8, fontSize: '0.9rem' }}>
          Central Homelab Knowledge ⚪ AI assistant
        </p>
      </header>

      {/* Chat container */}
      <div
        style={{
          flex: 1,
          display: 'flex',
          flexDirection: 'column',
          borderRadius: '0.75rem',
          border: '1px solid #1f2937',
          backgroundColor: '#020617',
          padding: '0.75rem',
        }}
      >
        {/* Scrollable messages */}
        <div
          style={{
            flex: 1,
            overflowY: 'auto',
            display: 'flex',
            flexDirection: 'column',
            gap: '0.5rem',
            paddingBottom: '0.5rem',
          }}
        >
          {messages.length === 0 ? (
            <span style={{ opacity: 0.7, fontSize: '0.9rem' }}>
              No messages yet. Type something below to get started.
            </span>
          ) : (
            messages.map(message => (
              <div
                key={message.id}
                style={{
                  alignSelf: message.role === 'user' ? 'flex-end' : 'flex-start',
                  padding: '0.5rem 0.75rem',
                  borderRadius: '0.5rem',
                  backgroundColor:
                    message.role === 'user' ? '#4b5563' : '#0b1120',
                  border: '1px solid #1f2937',
                  fontSize: '0.9rem',
                  maxWidth: '80%',
                }}
              >
                <div
                  style={{
                    fontSize: '0.7rem',
                    opacity: 0.7,
                    marginBottom: '0.15rem',
                  }}
                >
                  {message.role === 'user' ? 'You' : 'Homebrain'}
                </div>
              {message.text}
            </div>
            ))
          )}
          {isLoading && (
            <div style={{ opacity: 0.7, fontSize: '0.8rem', marginTop: '0.25rem' }}>
              Homebrain is thinking…
            </div>
          )}
        </div>

        {/* Input bar */}
        <form
          onSubmit={handleSubmit}
          style={{
            borderTop: '1px solid #1f2937',
            paddingTop: '0.5rem',
            display: 'flex',
            gap: '0.5rem',
            marginTop: '0.5rem',
          }}
        >
          <input
            type="text"
            value={input}
            onChange={event => setInput(event.target.value)}
            placeholder="Type a message..."
            style={{
              flex: 1,
              padding: '0.5rem 0.75rem',
              borderRadius: '0.5rem',
              border: '1px solid #374151',
              backgroundColor: '#020617',
              color: '#e5e7eb',
              fontSize: '0.9rem',
            }}
          />
          <button
            type="submit"
            disabled={isLoading}
            style={{
              opacity: isLoading ? 0.6 : 1,
              cursor: isLoading ? 'not-allowed' : 'pointer',
              padding: '0.5rem 0.9rem',
              borderRadius: '0.5rem',
              border: 'none',
              fontWeight: 500,
              backgroundColor: '#22c55e',
              color: '#022c22',
              fontSize: '0.9rem',
            }}
          >
            {isLoading ? 'Sending...' : 'Send'}
          </button>
        </form>
      </div>
    </div>
  )
}

export default App
