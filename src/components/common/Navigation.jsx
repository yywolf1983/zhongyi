import { useLocation, useNavigate } from 'react-router-dom'

const tabs = [
  { id: 'formulas', path: '/formulas', label: '方剂', icon: 'formula' },
  { id: 'acupuncture', path: '/acupuncture', label: '针灸', icon: 'acupuncture' },
  { id: 'syndrome', path: '/', label: '辨证', icon: 'syndrome' }
]

const ICONS = {
  // 方剂：书卷
  formula: (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
      <path d="M4 5a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2z" />
      <path d="M15 3.5A2 2 0 0 1 17 5.5V19a2 2 0 0 1-2 2" />
      <line x1="7.5" y1="8.5" x2="12.5" y2="8.5" />
      <line x1="7.5" y1="12" x2="12.5" y2="12" />
      <line x1="7.5" y1="15.5" x2="11" y2="15.5" />
    </svg>
  ),
  // 针灸：银针
  acupuncture: (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
      <line x1="12" y1="3" x2="12" y2="21" />
      <path d="M12 3l-1.8 2.6h3.6z" />
      <line x1="9" y1="9.5" x2="15" y2="9.5" />
      <line x1="10" y1="13" x2="14" y2="13" />
      <line x1="10.5" y1="16.5" x2="13.5" y2="16.5" />
    </svg>
  ),
  // 辨证：阴阳
  syndrome: (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="12" r="9" />
      <path d="M12 3c5 0 9 4 9 9s-4 9-9 9a4.5 4.5 0 0 1 0-9 4.5 4.5 0 0 0 0-9z" fill="currentColor" opacity="0.18" />
      <circle cx="12" cy="7.5" r="1.4" fill="currentColor" stroke="none" />
      <circle cx="12" cy="16.5" r="1.4" fill="currentColor" stroke="none" />
    </svg>
  )
}

export default function Navigation() {
  const location = useLocation()
  const navigate = useNavigate()

  // 辨证（根路径）：列表精确匹配 /，详情 /syndromes/:id 也高亮
  const isActive = (tab) => {
    const { pathname } = location
    if (tab.path === '/') return pathname === '/' || pathname.startsWith('/syndromes/')
    if (tab.id === 'formulas') return pathname.startsWith('/formulas') || pathname.startsWith('/medicines')
    return pathname.startsWith(tab.path)
  }

  return (
    <div className="nav-wrapper">
      <nav className="nav-container" aria-label="主导航">
        {tabs.map((tab) => {
          const active = isActive(tab)
          return (
            <button
              key={tab.id}
              type="button"
              className={`nav-item ${active ? 'active' : ''}`}
              aria-current={active ? 'page' : undefined}
              onClick={() => navigate(tab.path)}
            >
              <span className="nav-icon">{ICONS[tab.icon]}</span>
              <span className="nav-label">{tab.label}</span>
            </button>
          )
        })}
      </nav>
    </div>
  )
}
