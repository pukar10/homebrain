import { ChatPanel } from './components/ChatPanel'
import { StatusPanel } from './components/StatusPanel'

function App() {
  return (
    <div className="app-root" style={rootStyle}>
      <header style={headerStyle}>
        <span style={{ fontSize: '1.75rem', fontWeight: 600 }}>🧠 Homebrain</span>
        <span style={{ opacity: 0.7, fontSize: '0.9rem' }}>
          Homelab's brain • Central knowledge
        </span>
      </header>

      <main style={mainStyle}>
        <section style={chatSectionStyle}>
          <ChatPanel />
        </section>
        <aside style={asideStyle}>
          <StatusPanel />
        </aside>
      </main>
    </div>
  )
}

const rootStyle: React.CSSProperties = {
  minHeight: '100vh',
  display: 'flex',
  flexDirection: 'column',
  background: '#020617', // slate-950-ish
  color: '#e5e7eb', // zinc-200
  fontFamily: 'system-ui, -apple-system, BlinkMacSystemFont, sans-serif',
}

const headerStyle: React.CSSProperties = {
  padding: '1rem 1.5rem',
  borderBottom: '1px solid #1f2937',
  display: 'flex',
  flexDirection: 'column',
  gap: '0.25rem',
}

const mainStyle: React.CSSProperties = {
  display: 'grid',
  gridTemplateColumns: 'minmax(0, 2.5fr) minmax(260px, 1fr)',
  gap: '1rem',
  padding: '1rem',
  flex: 1,
}

const chatSectionStyle: React.CSSProperties = {
  background: '#020617',
  borderRadius: '0.75rem',
  border: '1px solid #1f2937',
  padding: '0.75rem',
  display: 'flex',
  flexDirection: 'column',
}

const asideStyle: React.CSSProperties = {
  background: '#020617',
  borderRadius: '0.75rem',
  border: '1px solid #1f2937',
  padding: '0.75rem',
}

export default App
