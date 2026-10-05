import { useLocation, useNavigate } from 'react-router-dom'

const tabs = [
  { id: 'formulas', path: '/formulas', label: '方剂', icon: '📜' },
  { id: 'acupuncture', path: '/acupuncture', label: '针灸', icon: '💉' },
  { id: 'syndrome', path: '/', label: '辨证', icon: '☯' }
]

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
              <span className="nav-icon">{tab.icon}</span>
              <span className="nav-label">{tab.label}</span>
            </button>
          )
        })}
      </nav>
    </div>
  )
}
