import { useState } from 'react'
import type { FormEvent } from 'react'

type Message = {
  id: number
  role: 'user' | 'assistant'
  content: string
}

export function ChatPanel() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 1,
      role: 'assistant',
      content: 'Hey, I am Homebrain. I am currently running in “fake brain” mode.',
    },
    {
      id: 2,
      role: 'assistant',
      content: 'Soon I will talk to a Python backend and your homelab. For now, try sending me a message.',
    },
  ])

  const [input, setInput] = useState('')
  const [nextId, setNextId] = useState(3)
  const [isThinking, setIsThinking] = useState(false)

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault()
    const trimmed = input.trim()
    if (!trimmed || isThinking) return

    const userMessage: Message = {
      id: nextId,
      role: 'user',
      content: trimmed,
    }

    setMessages(prev => [...prev, userMessage])
    setNextId(id => id + 1)
    setInput('')
    setIsThinking(true)

    // Fake “assistant” reply for now
    setTimeout(() => {
      setMessages(prev => [
        ...prev,
        {
          id: nextId + 1,
          role: 'assistant',
          content: `You said: "${trimmed}". In the future, I’ll run this through LangChain / LangGraph.`,
        },
      ])
      setNextId(id => id + 2)
      setIsThinking(false)
    }, 600)
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
      <div
        style={{
          padding: '0.5rem 0.75rem',
          borderBottom: '1px solid #1f2937',
          marginBottom: '0.5rem',
        }}
      >
        <div style={{ fontWeight: 600 }}>Chat</div>
        <div style={{ fontSize: '0.8rem', opacity: 0.7 }}>
          Talk to Homebrain. Backend is mocked for now.
        </div>
      </div>

      <div
        style={{
          flex: 1,
          overflowY: 'auto',
          padding: '0.5rem',
          display: 'flex',
          flexDirection: 'column',
          gap: '0.5rem',
        }}
      >
        {messages.map(msg => (
          <div
            key={msg.id}
            style={{
              alignSelf: msg.role === 'user' ? 'flex-end' : 'flex-start',
              maxWidth: '80%',
              padding: '0.5rem 0.75rem',
              borderRadius: '0.75rem',
              background:
                msg.role === 'user' ? '#4b5563' : 'rgba(15, 23, 42, 0.9)',
              border:
                msg.role === 'assistant'
                  ? '1px solid #1f2937'
                  : '1px solid transparent',
              fontSize: '0.9rem',
              whiteSpace: 'pre-wrap',
            }}
          >
            <div
              style={{
                fontSize: '0.7rem',
                opacity: 0.7,
                marginBottom: '0.15rem',
                textTransform: 'uppercase',
                letterSpacing: '0.04em',
              }}
            >
              {msg.role === 'user' ? 'You' : 'Homebrain'}
            </div>
            {msg.content}
          </div>
        ))}
        {isThinking && (
          <div
            style={{
              alignSelf: 'flex-start',
              fontSize: '0.8rem',
              opacity: 0.7,
              paddingLeft: '0.25rem',
            }}
          >
            Homebrain is thinking…
          </div>
        )}
      </div>

      <form
        onSubmit={handleSubmit}
        style={{
          marginTop: '0.5rem',
          borderTop: '1px solid #1f2937',
          paddingTop: '0.5rem',
          display: 'flex',
          gap: '0.5rem',
        }}
      >
        <input
          type="text"
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder="Ask Homebrain something about your homelab…"
          style={{
            flex: 1,
            padding: '0.5rem 0.75rem',
            borderRadius: '0.5rem',
            border: '1px solid #374151',
            background: '#020617',
            color: '#e5e7eb',
            fontSize: '0.9rem',
          }}
        />
        <button
          type="submit"
          disabled={!input.trim() || isThinking}
          style={{
            padding: '0.5rem 0.9rem',
            borderRadius: '0.5rem',
            border: 'none',
            fontSize: '0.9rem',
            fontWeight: 500,
            cursor: isThinking ? 'default' : 'pointer',
            opacity: !input.trim() || isThinking ? 0.5 : 1,
            background: '#22c55e',
            color: '#022c22',
          }}
        >
          Send
        </button>
      </form>
    </div>
  )
}
