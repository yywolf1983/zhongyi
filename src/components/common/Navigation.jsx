import { useLocation, useNavigate } from 'react-router-dom'

const tabs = [
  { id: 'home', path: '/', label: '首页', icon: '🏠' },
  { id: 'formulas', path: '/formulas', label: '方剂', icon: '📜' },
  { id: 'acupuncture', path: '/acupuncture', label: '针灸', icon: '💉' },
  { id: 'syndromes', path: '/syndromes', label: '辨证', icon: '☯' },
  { id: 'graph', path: '/knowledge-graph', label: '图谱', icon: '🔗' },
  { id: 'bookmarks', path: '/bookmarks', label: '我的', icon: '👤' }
]

export default function Navigation() {
  const location = useLocation()
  const navigate = useNavigate()

  // 首页需精确匹配；「方剂」菜单同时涵盖 /formulas 与 /medicines（同一门类）
  const isActive = (tab) => {
    if (tab.path === '/') return location.pathname === '/'
    if (tab.id === 'formulas') return location.pathname.startsWith('/formulas') || location.pathname.startsWith('/medicines')
    return location.pathname.startsWith(tab.path)
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
