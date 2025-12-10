import { useState, useEffect } from 'react'
import type { FormEvent } from 'react'

type Message = {
  id: number
  role: 'user' | 'assistant' | 'system'
  text: string
}

type ChatMessage = {
  role: 'user' | 'assistant' | 'system'
  content: string
}

type ChatResponse = {
  reply: string
  history: ChatMessage[]
  thread_id: string
}

type SessionSummary = {
  thread_id: string
  created_at: string
}

type SessionDetail = {
  thread_id: string
  created_at: string
  messages: ChatMessage[]
}

function App() {

  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  
  const [isLoading, setIsLoading] = useState(false)
  const [threadId, setThreadId] = useState<string | null>(null)

  const [sessions, setSessions] = useState<SessionSummary[]>([])
  const [isLoadingSessions, setIsLoadingSessions] = useState(false)


  
  // --- Helpers ---

  const formatDate = (iso: string) => {
    try {
      const d = new Date(iso)
      return d.toLocaleString(undefined, {
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
      })
    } catch {
      return iso
    }
  }


  const mapChatMessagesToUI = (msgs: ChatMessage[]): Message[] =>
    msgs.map((m, index) => ({
      id: index,
      role: m.role === 'user' ? 'user' : 'assistant',
      text: m.content,
    }))



  // --- API calls ---

  const fetchSessions = async () => {
    try {
      setIsLoadingSessions(true)
      const res = await fetch('/api/sessions')
      if (!res.ok) {
        throw new Error(`Failed to fetch sessions: ${res.status}`)
      }
      const data: SessionSummary[] = await res.json()
      setSessions(data)
    } catch (err) {
      console.error('Error fetching sessions:', err)
    } finally {
      setIsLoadingSessions(false)
    }
  }

  const fetchSessionDetail = async (id: string) => {
    try {
      setIsLoading(true)
      const res = await fetch(`/api/sessions/${id}`)
      if (!res.ok) {
        throw new Error(`Failed to fetch session detail: ${res.status}`)
      }
      const data: SessionDetail = await res.json()

      const mappedMessages = mapChatMessagesToUI(data.messages)
      setMessages(mappedMessages)
      setThreadId(data.thread_id)
    } catch (err) {
      console.error('Error fetching session detail:', err)
    } finally {
      setIsLoading(false)
    }
  }

  // Load sessions once on mount
  useEffect(() => {
    fetchSessions()
  }, [])



// --- Event handlers ---

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()

    const userInput = input.trim()
    if (!userInput) return

    // Optimistic UI update with user message
    const userMessage: Message = {
      id: Date.now(),
      role: 'user',
      text: userInput,
    }

    // Placeholder assistant message while waiting for backend
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

        // Server is sending SSE-style chunks: "data: ...\n\n"
        const parts = buffer.split('\n\n')
        // Last piece may be incomplete; keep it in buffer
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
            fetchSessions()
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

      // Replace the placeholder assistant message with an error message
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



  const handleSelectSession = (id: string) => {
    fetchSessionDetail(id)
  }


  const handleNewChat = () => {
    // Let backend create a new thread_id on next /api/chat* call
    setThreadId(null)
    setMessages([])
    setInput('')
  }



  // --- Render ---

  return (
    <div
      style={{
        minHeight: '100vh',
        backgroundColor: '#020617',
        color: '#e5e7eb',
        fontFamily: 'system-ui, -apple-system, BlinkMacSystemFont, sans-serif',
        display: 'flex',
      }}
    >
      {/* Sidebar */}
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
        {/* Brand */}
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
          <div
            style={{
              fontSize: '0.75rem',
              opacity: 0.65,
              marginTop: '0.2rem',
            }}
          >
            Sessions
          </div>
        </div>

        {/* New chat button */}
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

        {/* Session list */}
        <div
          style={{
            flex: 1,
            overflowY: 'auto',
            paddingRight: '0.25rem',
            marginTop: '0.25rem',
          }}
        >
          {isLoadingSessions && (
            <div style={{ fontSize: '0.8rem', opacity: 0.7 }}>
              Loading sessions…
            </div>
          )}

          {!isLoadingSessions && sessions.length === 0 && (
            <div style={{ fontSize: '0.8rem', opacity: 0.7 }}>
              No sessions yet. Start a chat to create one.
            </div>
          )}

          {!isLoadingSessions &&
            sessions.map(session => {
              const isActive = session.thread_id === threadId

              return (
                <button
                  key={session.thread_id}
                  type="button"
                  onClick={() => handleSelectSession(session.thread_id)}
                  style={{
                    width: '100%',
                    textAlign: 'left',
                    border: 'none',
                    backgroundColor: isActive ? '#111827' : 'transparent',
                    borderRadius: '0.6rem',
                    padding: '0.55rem 0.6rem',
                    marginBottom: '0.25rem',
                    cursor: 'pointer',
                    borderColor: isActive ? '#4b5563' : 'transparent',
                    borderStyle: 'solid',
                    borderWidth: '1px',
                    display: 'flex',
                    flexDirection: 'column',
                    gap: '0.15rem',
                    transition: 'background-color 120ms ease, border-color 120ms ease, transform 80ms ease',
                  }}
                >
                  <div
                    style={{
                      fontSize: '0.8rem',
                      fontWeight: 500,
                      whiteSpace: 'nowrap',
                      overflow: 'hidden',
                      textOverflow: 'ellipsis',
                    }}
                  >
                    {session.thread_id.slice(0, 8)}…
                  </div>
                  <div
                    style={{
                      fontSize: '0.7rem',
                      opacity: 0.6,
                    }}
                  >
                    {formatDate(session.created_at)}
                  </div>
                </button>
              )
            })}
        </div>

        {/* Small footer label */}
        <div
          style={{
            fontSize: '0.7rem',
            opacity: 0.6,
          }}
        >
          🧪 Homelab build · v0.3
        </div>
      </aside>

      {/* Main chat area */}
      <main
        style={{
          flex: 1,
          display: 'flex',
          flexDirection: 'column',
          padding: '1.5rem 1.5rem 3rem',
          boxSizing: 'border-box',
        }}
      >
        {/* Header */}
        <header style={{ marginBottom: '1rem' }}>
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