import { useLocation, useNavigate } from 'react-router-dom'

const tabs = [
  { id: 'home', path: '/', label: '首页', icon: '🏠' },
  { id: 'syndromes', path: '/syndromes', label: '辨证', icon: '📋' },
  { id: 'acupuncture', path: '/acupuncture', label: '针灸', icon: '💉' },
  { id: 'formulas', path: '/formulas', label: '方剂', icon: '🌿' },
  { id: 'knowledge-graph', path: '/knowledge-graph', label: '知识图谱', icon: '🔗' },
  { id: 'bookmarks', path: '/bookmarks', label: '收藏', icon: '⭐' }
]

export default function Navigation() {
  const location = useLocation()
  const navigate = useNavigate()

  // 首页需精确匹配（否则 /syndromes 也会命中 '/' 前缀）；其余用前缀匹配
  const isActive = (tab) =>
    tab.path === '/' ? location.pathname === '/' : location.pathname.startsWith(tab.path)

  return (
    <div className="nav-wrapper">
      <nav className="nav-container">
        {tabs.map(tab => (
          <button
            key={tab.id}
            className={`nav-item ${isActive(tab) ? 'active' : ''}`}
            onClick={() => navigate(tab.path)}
          >
            <span className="nav-icon">{tab.icon}</span>
            {tab.label}
          </button>
        ))}
      </nav>
    </div>
  )
}
