import { useState, useEffect } from 'react'
import type { FormEvent } from 'react'

type Message = {
  id: number
  role: 'user' | 'assistant'
  text: string
}

type ChatMessage = {
  role: 'user' | 'assistant'
  content: string
}

type ChatResponse = {
  reply: string
  history: ChatMessage[]
  session_id: string
}

type SessionSummary = {
  id: string
  created_at: string
}

type SessionDetail = {
  id: string
  created_at: string
  messages: ChatMessage[]
}

function App() {

  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  
  const [isLoading, setIsLoading] = useState(false)
  const [sessionId, setSessionId] = useState<string | null>(null)

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

      // Normalize messages from backend into UI messages
      const mappedMessages: Message[] = data.messages.map((m, index) => ({
        id: index,
        role: m.role,
        text: m.content,
      }))

      setMessages(mappedMessages)
      setSessionId(data.id)
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

    // 1. Clean up input
    const userInput = input.trim()
    if (!userInput) return

    // 2. Optimistic UI update with user message
    const userMessage: Message = {
      id: Date.now(),
      role: 'user',
      text: userInput,
    }
    setMessages(prev => [...prev, userMessage])
    setInput('')
    setIsLoading(true)

    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: userInput,
          session_id: sessionId,
        }),
      })

      if (!res.ok) {
        throw new Error(`Server error! status: ${res.status}`)
      }

      const data: ChatResponse = await res.json()

      // Update current sessionId from backend
      setSessionId(data.session_id)

      // Normalize backend history data into UI messages
      const mappedMessages: Message[] = data.history.map((m, index) => ({
        id: index,
        role: m.role,
        text: m.content,
      }))

      setMessages(mappedMessages)

      // Refresh sessions list so new session appears / updated timestamp
      fetchSessions()

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



  const handleSelectSession = (id: string) => {
    // Click on a session in the sidebar: load its history
    fetchSessionDetail(id)
  }


  const handleNewChat = () => {
    // Let backend create a new session on next /api/chat call
    setSessionId(null)
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
              const isActive = session.id === sessionId

              return (
                <button
                  key={session.id}
                  type="button"
                  onClick={() => handleSelectSession(session.id)}
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
                    {session.id.slice(0, 8)}…
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
          {sessionId && (
            <p style={{ opacity: 0.6, fontSize: '0.75rem', marginTop: '0.25rem' }}>
              Session: <code>{sessionId.slice(0, 10)}…</code>
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