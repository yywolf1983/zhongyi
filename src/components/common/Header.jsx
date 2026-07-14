import { useNavigate } from 'react-router-dom'

export default function Header() {
  const navigate = useNavigate()

  return (
    <header className="header-container" onClick={() => navigate('/')}>
      <div className="header-logo">
        <span className="header-icon">🌿</span>
      </div>
      <div className="header-title">中医辨证论治</div>
      <div className="header-subtitle">传承经典 · 辨证施治</div>
    </header>
  )
}
