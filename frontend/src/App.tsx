import { useState } from 'react'
import type { FormEvent } from 'react'

type Message = {
  id: number
  role: 'user' | 'assistant'
  text: string
}

function App() {

  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  
  const [isLoading, setIsLoading] = useState(false)
  const [threadId, setThreadId] = useState<string | null>(null)

  
  // --- Helpers ---
  const handleNewChat = () => {
    setThreadId(null)
    setMessages([])
    setInput('')
  }


  // --- Event handlers ---

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()

    const userInput = input.trim()
    if (!userInput) return

    const userMessage: Message = {
      id: Date.now(),
      role: 'user',
      text: userInput,
    }

    const assistantMessage: Message = {
      id: Date.now() + 1,
      role: 'assistant',
      text: '...',
    }

    setMessages(prev => [...prev, userMessage, assistantMessage])
    setInput('')
    setIsLoading(true)

    const currentAssistantId = assistantMessage.id

    try {
      const res = await fetch('/api/chat/stream', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: userInput,
          thread_id: threadId,
        }),
      })

      if (!res.ok || !res.body) {
        throw new Error(`Server error! status: ${res.status}`)
      }

      const reader = res.body.getReader()
      const decoder = new TextDecoder('utf-8')
      let buffer = ''

      while (true) {
        const { value, done } = await reader.read()
        if (done) break

        buffer += decoder.decode(value, { stream: true })
        const parts = buffer.split('\n\n')
        buffer = parts.pop() ?? ''

        for (const part of parts) {
          const line = part.trim()
          if (!line.startsWith('data: ')) continue

          const payload = line.slice(6) // remove "data: "

          // DONE marker from backend: [DONE]|<thread_id>
          if (payload.startsWith('[DONE]|')) {
            const newThreadId = payload.slice('[DONE]|'.length)
            if (newThreadId) {
              setThreadId(newThreadId)
            }
            // Refresh session list when a turn is fully complete
            continue
          }

          // Normal text chunk: append to the last assistant message
          if (payload) {
            setMessages(prev =>
              prev.map(msg =>
                msg.id === currentAssistantId
                  ? { ...msg, text: msg.text + payload }
                  : msg
              )
            )
          }
        }
      }
    } catch (error) {
        console.error('Error during streaming chat:', error)

      setMessages(prev => [
        ...prev.filter(m => m.id !== currentAssistantId),
        {
          id: Date.now() + 2,
          role: 'assistant',
          text:
            'Homebrain: I hit an error talking to the backend. Check backend logs for more details.',
        },
      ])
    } finally {
        setIsLoading(false)
    }
  }


  return (
    // Main container (left sidebar + main chat)
    <div
      style={{
        minHeight: '100vh',
        backgroundColor: '#020617',
        color: '#e5e7eb',
        fontFamily: 'system-ui, -apple-system, BlinkMacSystemFont, sans-serif',
        display: 'flex',
      }}
    >
      {/* LEFT SIDEBAR */}
      <aside
        style={{
          width: '260px',
          borderRight: '1px solid #1f2937',
          padding: '1rem',
          boxSizing: 'border-box',
          display: 'flex',
          flexDirection: 'column',
          gap: '1rem',
          background: 'radial-gradient(circle at top, #111827 0, #020617 55%)',
        }}
      >
        {/* header */}
        <div>
          <div
            style={{
              fontSize: '1.1rem',
              fontWeight: 600,
              display: 'flex',
              alignItems: 'center',
              gap: '0.4rem',
            }}
          >
            <span
              style={{
                width: '1.4rem',
                height: '1.4rem',
                borderRadius: '0.5rem',
                background:
                  'linear-gradient(135deg, #22c55e, #4ade80, #22c55e)',
              }}
            />
            <span>Homebrain</span>
          </div>
          {/* Subtitle */}
          <div style={{fontSize: '0.75rem', opacity: 0.65, marginTop: '0.2rem'}}>
            Sessions (no sessions yet)
          </div>
        </div>
        {/* new chat button */}
        <button
          type="button"
          onClick={handleNewChat}
          style={{
            width: '100%',
            borderRadius: '999px',
            padding: '0.55rem 0.9rem',
            border: 'none',
            fontWeight: 500,
            fontSize: '0.85rem',
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            gap: '0.4rem',
            background:
              'linear-gradient(135deg, #22c55e, #16a34a, #22c55e)',
            color: '#022c22',
            boxShadow: '0 8px 20px rgba(34,197,94,0.25)',
          }}
        >
          <span>＋</span>
          <span>New chat</span>
        </button>
        {/* footer label */}
        <div
          style={{
            fontSize: '0.7rem',
            opacity: 0.6,
          }}
        >
          🧪 Homelab build · v0.3
        </div>
      </aside>

      {/* CHAT AREA */}
      <main
        style={{
          flex: 1,
          display: 'flex',
          flexDirection: 'column',
          padding: '1.5rem 1.5rem 3rem',
          boxSizing: 'border-box',
        }}
      >
        {/* header */}
        <header style={{ marginBottom: '1rem' }}
        >
          <h1 style={{ fontSize: '1.75rem', marginBottom: '0.25rem' }}>
            🧠 Homebrain
          </h1>
          <p style={{ opacity: 0.8, fontSize: '0.9rem' }}>
            Central Homelab Knowledge ⚪ AI assistant
          </p>
          {threadId && (
            <p
              style={{ 
                opacity: 0.6, 
                fontSize: '0.75rem', 
                marginTop: '0.25rem' 
              }}
            >
              Thread:{' '} 
              <code>
                {threadId.slice(0, 10)}…
              </code>
            </p>
          )}
        </header>
        {/* chat container */}
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
          {/* message list */}
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
                    alignSelf:
                      message.role === 'user' ? 'flex-end' : 'flex-start',
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
              <div
                style={{
                  opacity: 0.7,
                  fontSize: '0.8rem',
                  marginTop: '0.25rem',
                }}
              >
                Homebrain is thinking…
              </div>
            )}
          </div>
          
          {/* message composer */}
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
            {/* Input field */}
            <input
              type="text"
              value={input}
              onChange={event => setInput(event.target.value)}
              placeholder="Inquire Homebrain..."
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
            {/* submit button */}
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
      </main>
    </div>
  )
}


export default App