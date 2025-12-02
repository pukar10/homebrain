export function StatusPanel() {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
      <div
        style={{
          padding: '0.5rem 0.75rem',
          borderBottom: '1px solid #1f2937',
          marginBottom: '0.25rem',
        }}
      >
        <div style={{ fontWeight: 600 }}>System status</div>
        <div style={{ fontSize: '0.8rem', opacity: 0.7 }}>
          Static for now — later, this can poll your homelab.
        </div>
      </div>

      <div
        style={{
          fontSize: '0.85rem',
          display: 'flex',
          flexDirection: 'column',
          gap: '0.4rem',
        }}
      >
        <div>
          <span style={{ opacity: 0.6 }}>Mode: </span>
          <span>Frontend-only prototype</span>
        </div>
        <div>
          <span style={{ opacity: 0.6 }}>Backend: </span>
          <span>Not hooked up yet</span>
        </div>
        <div>
          <span style={{ opacity: 0.6 }}>Planned:</span>
          <ul style={{ marginTop: '0.25rem', paddingLeft: '1.25rem' }}>
            <li>Python API with FastAPI</li>
            <li>LangChain / LangGraph pipelines</li>
            <li>Homelab adapters (Proxmox, K3s, etc.)</li>
          </ul>
        </div>
      </div>
    </div>
  )
}
